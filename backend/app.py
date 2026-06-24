import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import chess

from engine.minimax import minimax_root
from engine.evaluation import get_evaluation_breakdown, evaluate_board
from engine.explain import explain_move

app = Flask(
    __name__,
    static_folder="static",
    static_url_path=""
)
CORS(app)

@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, "index.html")


@app.route("/new-game", methods=["POST"])
def new_game():
    board = chess.Board()
    return jsonify({
        "fen": board.fen()
    })

@app.route("/move", methods=["POST"])
def make_move():
    data = request.json
    fen = data.get("fen")
    player_move_str = data.get("move")
    difficulty = data.get("difficulty", "Easy")
    
    # Map difficulty to depth
    depth_map = {
        "Easy": 2,
        "Medium": 3,
        "Hard": 4,
        "Expert": 5
    }
    depth = depth_map.get(difficulty, 2)
    
    board = chess.Board(fen)
    
    # If the player provided a move, make it first
    if player_move_str:
        try:
            player_move = chess.Move.from_uci(player_move_str)
            if player_move in board.legal_moves:
                board.push(player_move)
            else:
                return jsonify({"error": "Illegal move"}), 400
        except ValueError:
            return jsonify({"error": "Invalid move format"}), 400
            
    # Check if game over after player move
    if board.is_game_over():
        return jsonify({
            "fen": board.fen(),
            "game_over": True,
            "result": board.result()
        })
        
    # AI's turn
    is_white = board.turn == chess.WHITE
    start_time = time.time()
    
    # Run minimax
    best_move, _ = minimax_root(depth, board, is_maximizing=is_white)
    
    end_time = time.time()
    
    if best_move is None:
        # Should not happen unless game over, but fallback
        best_move = list(board.legal_moves)[0]
        
    # Generate explanation before pushing the move
    explanation = explain_move(board, best_move)
    
    # Make the move
    board.push(best_move)
    
    # Get the evaluation breakdown after the move
    eval_breakdown = get_evaluation_breakdown(board)
    
    # We want the evaluation relative to white for display
    # but the current engine gives it from white's perspective natively
    
    response = {
        "ai_move": best_move.uci(),
        "fen": board.fen(),
        "evaluation": eval_breakdown,
        "explanation": explanation,
        "time_taken": round(end_time - start_time, 2),
        "game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else "*"
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

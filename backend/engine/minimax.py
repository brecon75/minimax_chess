import chess
from .evaluation import evaluate_board

# Track nodes evaluated for curiosity/debugging
nodes_evaluated = 0

def minimax_root(depth, board: chess.Board, is_maximizing):
    global nodes_evaluated
    nodes_evaluated = 0
    
    best_move = None
    best_value = -99999 if is_maximizing else 99999
    
    # Simple move ordering: captures first
    moves = list(board.legal_moves)
    moves.sort(key=lambda move: board.is_capture(move), reverse=True)
    
    alpha = -100000
    beta = 100000
    
    for move in moves:
        board.push(move)
        value = minimax(depth - 1, board, alpha, beta, not is_maximizing)
        board.pop()
        
        if is_maximizing:
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            
    return best_move, best_value

def minimax(depth, board: chess.Board, alpha, beta, is_maximizing):
    global nodes_evaluated
    nodes_evaluated += 1
    
    if depth == 0 or board.is_game_over():
        # Quiescence search could go here, but keeping it simple for now
        return evaluate_board(board)
        
    moves = list(board.legal_moves)
    # Simple move ordering
    moves.sort(key=lambda move: board.is_capture(move), reverse=True)
    
    if is_maximizing:
        best_value = -99999
        for move in moves:
            board.push(move)
            best_value = max(best_value, minimax(depth - 1, board, alpha, beta, not is_maximizing))
            board.pop()
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break # Beta cut-off
        return best_value
    else:
        best_value = 99999
        for move in moves:
            board.push(move)
            best_value = min(best_value, minimax(depth - 1, board, alpha, beta, not is_maximizing))
            board.pop()
            beta = min(beta, best_value)
            if beta <= alpha:
                break # Alpha cut-off
        return best_value

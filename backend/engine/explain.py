import chess
from .evaluation import get_evaluation_breakdown

def explain_move(board_before: chess.Board, move: chess.Move):
    """
    Generate an explanation for a move by comparing board evaluation before and after.
    board_before is the board BEFORE the move is made.
    """
    is_white_move = board_before.turn == chess.WHITE
    
    # 1. Get before breakdown
    eval_before = get_evaluation_breakdown(board_before)
    
    # 2. Get after breakdown
    board_after = board_before.copy()
    board_after.push(move)
    eval_after = get_evaluation_breakdown(board_after)
    
    explanations = []
    
    # Determine the perspective modifier
    # Our evaluation function returns scores from White's perspective
    # If Black just moved, Black wants the score to be LOWER.
    mod = 1 if is_white_move else -1
    
    # 1. Capture?
    if board_before.is_capture(move):
        piece_captured = board_before.piece_at(move.to_square)
        if piece_captured:
            explanations.append(f"Captured opponent's {chess.piece_name(piece_captured.piece_type)}")
            
    # 2. Material
    mat_diff = (eval_after["material"] - eval_before["material"]) * mod
    if mat_diff > 0 and not board_before.is_capture(move):
        # Could happen on promotion
        if move.promotion:
            explanations.append("Promoted pawn to increase material")
            
    # 3. Position (Piece-Square)
    pos_diff = (eval_after["position"] - eval_before["position"]) * mod
    piece_moved = board_before.piece_at(move.from_square)
    
    if pos_diff > 0:
        if piece_moved and piece_moved.piece_type == chess.KNIGHT:
            explanations.append(f"Developed knight to a better square (+{pos_diff})")
        elif piece_moved and piece_moved.piece_type == chess.PAWN:
            explanations.append(f"Advanced pawn to control more space (+{pos_diff})")
        else:
            name = chess.piece_name(piece_moved.piece_type) if piece_moved else "piece"
            explanations.append(f"Moved {name} to a stronger position (+{pos_diff})")
            
    # 4. Mobility
    mob_diff = (eval_after["mobility"] - eval_before["mobility"]) * mod
    if mob_diff > 0:
        explanations.append(f"Increased overall mobility (+{mob_diff})")
    elif mob_diff < 0:
        explanations.append(f"Slightly restricted mobility ({mob_diff})")
        
    # 5. King Safety
    ks_diff = (eval_after["kingSafety"] - eval_before["kingSafety"]) * mod
    if ks_diff > 0:
        explanations.append(f"Improved king safety (+{ks_diff})")
    elif ks_diff < 0:
        explanations.append(f"King slightly exposed ({ks_diff})")
        
    # 6. Check
    if board_after.is_checkmate():
        explanations.append("Delivered checkmate!")
    elif board_after.is_check():
        explanations.append("Put opponent in check")
        
    # Fallback if no specific reasons found (rare)
    if not explanations:
        explanations.append("Solid developing move")
        
    # Return top 3 explanations by some heuristic, or just top 3
    # Let's just return what we have (often 2-4 items)
    return explanations

import chess
from .piece_square_tables import PAWN_PST, KNIGHT_PST, BISHOP_PST, ROOK_PST, QUEEN_PST, KING_PST

# Piece values
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# PST lookup mapped to piece types
PST_MAP = {
    chess.PAWN: PAWN_PST,
    chess.KNIGHT: KNIGHT_PST,
    chess.BISHOP: BISHOP_PST,
    chess.ROOK: ROOK_PST,
    chess.QUEEN: QUEEN_PST,
    chess.KING: KING_PST
}

def get_pst_value(piece_type, square, color):
    """Get the positional value for a piece on a square."""
    pst = PST_MAP[piece_type]
    
    # Tables are oriented for White. Rank 8 is row 0 in table.
    # square: 0 (A1) to 63 (H8).
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    
    if color == chess.WHITE:
        # For White, A8 is top-left of the table
        # rank 7 (8th rank) corresponds to row 0 in PST
        row = 7 - rank
        col = file
    else:
        # For Black, mirror the table vertically
        # rank 0 (1st rank) corresponds to row 0 in PST for black's perspective
        row = rank
        col = file
        
    return pst[row][col]


def evaluate_board(board: chess.Board):
    """
    Evaluates the board and returns a score from White's perspective.
    Positive score -> White is better
    Negative score -> Black is better
    """
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -99999
        else:
            return 99999
            
    if board.is_stalemate() or board.is_insufficient_material() or board.is_repetition():
        return 0
        
    score = 0
    
    # 1. Material & Position
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            pst_value = get_pst_value(piece.piece_type, square, piece.color)
            
            if piece.color == chess.WHITE:
                score += value + pst_value
            else:
                score -= value + pst_value
                
    # 2. Mobility
    # Simple metric: calculate legal moves for both sides
    # To do this accurately without modifying turn, we can temporarily change turn
    white_mobility = 0
    black_mobility = 0
    
    if board.turn == chess.WHITE:
        white_mobility = board.legal_moves.count()
        board.turn = chess.BLACK
        black_mobility = board.legal_moves.count()
        board.turn = chess.WHITE
    else:
        black_mobility = board.legal_moves.count()
        board.turn = chess.WHITE
        white_mobility = board.legal_moves.count()
        board.turn = chess.BLACK
        
    score += (white_mobility - black_mobility) * 2  # Mobility weight
    
    # 3. King Safety (simple penalty for missing pawn shield in front of king)
    # We do a basic check: if king is castled, reward it, if open file, penalize
    white_king_sq = board.king(chess.WHITE)
    black_king_sq = board.king(chess.BLACK)
    
    if white_king_sq:
        file = chess.square_file(white_king_sq)
        if file in [0, 1, 2, 5, 6, 7]: # King side or queen side
            score += 10 # Bonus for being tucked away
            
    if black_king_sq:
        file = chess.square_file(black_king_sq)
        if file in [0, 1, 2, 5, 6, 7]:
            score -= 10
            
    return score

def get_evaluation_breakdown(board: chess.Board):
    """
    Returns a breakdown of the evaluation into Material, Position, Mobility, King Safety.
    Always relative to the player to move (or we can just return absolute white perspective).
    We'll return it from White's perspective to keep it consistent.
    """
    material = 0
    position = 0
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            pst_value = get_pst_value(piece.piece_type, square, piece.color)
            
            if piece.color == chess.WHITE:
                material += value
                position += pst_value
            else:
                material -= value
                position -= pst_value
                
    white_mobility = 0
    black_mobility = 0
    
    if board.turn == chess.WHITE:
        white_mobility = board.legal_moves.count()
        board.turn = chess.BLACK
        black_mobility = board.legal_moves.count()
        board.turn = chess.WHITE
    else:
        black_mobility = board.legal_moves.count()
        board.turn = chess.WHITE
        white_mobility = board.legal_moves.count()
        board.turn = chess.BLACK
        
    mobility = (white_mobility - black_mobility) * 2
    
    king_safety = 0
    white_king_sq = board.king(chess.WHITE)
    black_king_sq = board.king(chess.BLACK)
    
    if white_king_sq and chess.square_file(white_king_sq) in [0, 1, 2, 5, 6, 7]:
        king_safety += 10
    if black_king_sq and chess.square_file(black_king_sq) in [0, 1, 2, 5, 6, 7]:
        king_safety -= 10
        
    total = material + position + mobility + king_safety
    
    return {
        "material": material,
        "position": position,
        "mobility": mobility,
        "kingSafety": king_safety,
        "total": total
    }

"""AI评估函数"""
from src.game.board import Board
from src.game.pieces import Color, PieceType


PIECE_VALUES = {
    PieceType.KING: 10000,
    PieceType.ROOK: 90,
    PieceType.CANNON: 45,
    PieceType.HORSE: 40,
    PieceType.ELEPHANT: 20,
    PieceType.ADVISOR: 20,
    PieceType.PAWN: 10,
}

# 兵/卒的位置权重（过河后更有价值）
PAWN_POSITION_WEIGHTS = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 0
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Before river
    [5, 5, 5, 5, 5, 5, 5, 5, 5],  # After river
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
    [20, 20, 20, 20, 20, 20, 20, 20, 20],
    [30, 30, 30, 30, 30, 30, 30, 30, 30],
    [50, 50, 50, 50, 50, 50, 50, 50, 50],  # Row 9
]


def evaluate_board(board: Board) -> float:
    """
    评估棋盘局面，从黑方视角返回分数。
    正数 = 黑方优势，负数 = 红方优势
    """
    score = 0.0

    for row in range(10):
        for col in range(9):
            piece = board.get_piece(row, col)
            if piece is None:
                continue

            value = PIECE_VALUES[piece.piece_type]

            # 兵/卒的位置加成
            if piece.piece_type == PieceType.PAWN:
                if piece.color == Color.RED:
                    value += PAWN_POSITION_WEIGHTS[row][col]
                else:
                    # 黑方权重镜像
                    value += PAWN_POSITION_WEIGHTS[9 - row][col]

            if piece.color == Color.BLACK:
                score += value
            else:
                score -= value

    return score

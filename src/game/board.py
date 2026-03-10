from typing import Optional
from src.game.pieces import Color, Piece, PieceType


class Board:
    def __init__(self):
        self.grid: list[list[Optional[Piece]]] = [[None] * 9 for _ in range(10)]
        self._setup_initial_position()
        self.current_turn = Color.RED

    def _setup_initial_position(self):
        # Red pieces (bottom, rows 0-4)
        self.grid[0][0] = Piece(Color.RED, PieceType.ROOK)
        self.grid[0][1] = Piece(Color.RED, PieceType.HORSE)
        self.grid[0][2] = Piece(Color.RED, PieceType.ELEPHANT)
        self.grid[0][3] = Piece(Color.RED, PieceType.ADVISOR)
        self.grid[0][4] = Piece(Color.RED, PieceType.KING)
        self.grid[0][5] = Piece(Color.RED, PieceType.ADVISOR)
        self.grid[0][6] = Piece(Color.RED, PieceType.ELEPHANT)
        self.grid[0][7] = Piece(Color.RED, PieceType.HORSE)
        self.grid[0][8] = Piece(Color.RED, PieceType.ROOK)

        self.grid[2][1] = Piece(Color.RED, PieceType.CANNON)
        self.grid[2][7] = Piece(Color.RED, PieceType.CANNON)

        for col in [0, 2, 4, 6, 8]:
            self.grid[3][col] = Piece(Color.RED, PieceType.PAWN)

        # Black pieces (top, rows 5-9)
        self.grid[9][0] = Piece(Color.BLACK, PieceType.ROOK)
        self.grid[9][1] = Piece(Color.BLACK, PieceType.HORSE)
        self.grid[9][2] = Piece(Color.BLACK, PieceType.ELEPHANT)
        self.grid[9][3] = Piece(Color.BLACK, PieceType.ADVISOR)
        self.grid[9][4] = Piece(Color.BLACK, PieceType.KING)
        self.grid[9][5] = Piece(Color.BLACK, PieceType.ADVISOR)
        self.grid[9][6] = Piece(Color.BLACK, PieceType.ELEPHANT)
        self.grid[9][7] = Piece(Color.BLACK, PieceType.HORSE)
        self.grid[9][8] = Piece(Color.BLACK, PieceType.ROOK)

        self.grid[7][1] = Piece(Color.BLACK, PieceType.CANNON)
        self.grid[7][7] = Piece(Color.BLACK, PieceType.CANNON)

        for col in [0, 2, 4, 6, 8]:
            self.grid[6][col] = Piece(Color.BLACK, PieceType.PAWN)

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        return self.grid[row][col]

    def find_king(self, color: Color) -> tuple[int, int]:
        for row in range(10):
            for col in range(9):
                piece = self.grid[row][col]
                if piece and piece.color == color and piece.piece_type == PieceType.KING:
                    return (row, col)
        raise ValueError(f"King not found for color {color}")

    def get_pieces(self, color: Color) -> list[tuple[tuple[int, int], Piece]]:
        result = []
        for row in range(10):
            for col in range(9):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    result.append(((row, col), piece))
        return result

    def move_piece(self, from_pos: tuple[int, int], to_pos: tuple[int, int]) -> Optional[Piece]:
        """执行走法，返回被吃的棋子（如果有）"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.grid[from_row][from_col]
        captured = self.grid[to_row][to_col]
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        return captured

    def undo_move(self, from_pos: tuple[int, int], to_pos: tuple[int, int], captured: Optional[Piece]):
        """撤销走法，恢复被吃的棋子"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.grid[to_row][to_col]
        self.grid[from_row][from_col] = piece
        self.grid[to_row][to_col] = captured

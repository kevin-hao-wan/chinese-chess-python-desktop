import pytest
from src.game.board import Board
from src.game.pieces import Color, PieceType


def test_board_has_10_rows():
    board = Board()
    assert len(board.grid) == 10


def test_board_has_9_columns():
    board = Board()
    assert len(board.grid[0]) == 9


def test_initial_position_has_32_pieces():
    board = Board()
    count = sum(1 for row in board.grid for piece in row if piece is not None)
    assert count == 32


def test_initial_position_has_16_red_pieces():
    board = Board()
    count = sum(
        1 for row in board.grid for piece in row
        if piece is not None and piece.color == Color.RED
    )
    assert count == 16


def test_initial_position_has_16_black_pieces():
    board = Board()
    count = sum(
        1 for row in board.grid for piece in row
        if piece is not None and piece.color == Color.BLACK
    )
    assert count == 16


def test_red_rook_at_bottom_left():
    board = Board()
    piece = board.get_piece(0, 0)
    assert piece is not None
    assert piece.color == Color.RED
    assert piece.piece_type == PieceType.ROOK


def test_black_king_at_top_center():
    board = Board()
    piece = board.get_piece(9, 4)
    assert piece is not None
    assert piece.color == Color.BLACK
    assert piece.piece_type == PieceType.KING


def test_get_piece_empty_square():
    board = Board()
    piece = board.get_piece(4, 4)  # Center is empty
    assert piece is None


def test_board_initial_turn_is_red():
    board = Board()
    assert board.current_turn == Color.RED


def test_find_king_red():
    board = Board()
    pos = board.find_king(Color.RED)
    assert pos == (0, 4)  # Red king at row 0, col 4


def test_find_king_black():
    board = Board()
    pos = board.find_king(Color.BLACK)
    assert pos == (9, 4)  # Black king at row 9, col 4


def test_get_pieces_red():
    board = Board()
    pieces = board.get_pieces(Color.RED)
    assert len(pieces) == 16
    for pos, piece in pieces:
        assert piece.color == Color.RED

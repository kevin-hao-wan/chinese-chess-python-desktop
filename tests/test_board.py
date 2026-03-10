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


def test_move_piece_updates_grid():
    board = Board()
    piece = board.get_piece(0, 0)  # Red rook
    board.move_piece((0, 0), (0, 2))
    assert board.get_piece(0, 0) is None
    assert board.get_piece(0, 2) == piece


def test_move_piece_returns_captured_piece():
    from src.game.pieces import Piece, PieceType
    board = Board()
    # 设置一个可以吃子的局面
    captured_piece = Piece(Color.BLACK, PieceType.PAWN)
    board.grid[3][0] = captured_piece
    board.move_piece((0, 0), (3, 0))  # Red rook captures black pawn
    assert board.get_piece(3, 0).color == Color.RED


def test_undo_move_restores_position():
    board = Board()
    original_piece = board.get_piece(0, 0)
    board.move_piece((0, 0), (0, 2))
    board.undo_move((0, 0), (0, 2), None)
    assert board.get_piece(0, 0) == original_piece
    assert board.get_piece(0, 2) is None


def test_undo_move_restores_captured_piece():
    from src.game.pieces import Piece, PieceType
    board = Board()
    captured = Piece(Color.BLACK, PieceType.PAWN)
    board.grid[3][0] = captured
    board.move_piece((0, 0), (3, 0))
    board.undo_move((0, 0), (3, 0), captured)
    assert board.get_piece(3, 0) == captured

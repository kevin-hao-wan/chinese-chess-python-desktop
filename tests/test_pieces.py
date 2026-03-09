import pytest
from src.game.pieces import Color, PieceType, Piece


def test_color_enum_values():
    assert Color.RED.value == "red"
    assert Color.BLACK.value == "black"


def test_piece_type_enum_values():
    assert PieceType.KING.value == "king"
    assert PieceType.ROOK.value == "rook"
    assert PieceType.HORSE.value == "horse"
    assert PieceType.ELEPHANT.value == "elephant"
    assert PieceType.ADVISOR.value == "advisor"
    assert PieceType.CANNON.value == "cannon"
    assert PieceType.PAWN.value == "pawn"


def test_piece_creation():
    piece = Piece(Color.RED, PieceType.ROOK)
    assert piece.color == Color.RED
    assert piece.piece_type == PieceType.ROOK


def test_piece_display_name_red_rook():
    piece = Piece(Color.RED, PieceType.ROOK)
    assert piece.display_name == "车"


def test_piece_display_name_black_king():
    piece = Piece(Color.BLACK, PieceType.KING)
    assert piece.display_name == "将"


@pytest.mark.parametrize("color,piece_type,expected", [
    (Color.RED, PieceType.KING, "帅"),
    (Color.RED, PieceType.ADVISOR, "仕"),
    (Color.RED, PieceType.ELEPHANT, "相"),
    (Color.RED, PieceType.HORSE, "马"),
    (Color.RED, PieceType.ROOK, "车"),
    (Color.RED, PieceType.CANNON, "炮"),
    (Color.RED, PieceType.PAWN, "兵"),
    (Color.BLACK, PieceType.KING, "将"),
    (Color.BLACK, PieceType.ADVISOR, "士"),
    (Color.BLACK, PieceType.ELEPHANT, "象"),
    (Color.BLACK, PieceType.HORSE, "马"),
    (Color.BLACK, PieceType.ROOK, "车"),
    (Color.BLACK, PieceType.CANNON, "炮"),
    (Color.BLACK, PieceType.PAWN, "卒"),
])
def test_all_piece_display_names(color, piece_type, expected):
    piece = Piece(color, piece_type)
    assert piece.display_name == expected

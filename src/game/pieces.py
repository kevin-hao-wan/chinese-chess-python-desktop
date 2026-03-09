from enum import Enum
from dataclasses import dataclass


class Color(Enum):
    RED = "red"
    BLACK = "black"


class PieceType(Enum):
    KING = "king"
    ADVISOR = "advisor"
    ELEPHANT = "elephant"
    HORSE = "horse"
    ROOK = "rook"
    CANNON = "cannon"
    PAWN = "pawn"


@dataclass(frozen=True)
class Piece:
    color: Color
    piece_type: PieceType

    @property
    def display_name(self) -> str:
        names = {
            (Color.RED, PieceType.KING): "帅",
            (Color.RED, PieceType.ADVISOR): "仕",
            (Color.RED, PieceType.ELEPHANT): "相",
            (Color.RED, PieceType.HORSE): "马",
            (Color.RED, PieceType.ROOK): "车",
            (Color.RED, PieceType.CANNON): "炮",
            (Color.RED, PieceType.PAWN): "兵",
            (Color.BLACK, PieceType.KING): "将",
            (Color.BLACK, PieceType.ADVISOR): "士",
            (Color.BLACK, PieceType.ELEPHANT): "象",
            (Color.BLACK, PieceType.HORSE): "马",
            (Color.BLACK, PieceType.ROOK): "车",
            (Color.BLACK, PieceType.CANNON): "炮",
            (Color.BLACK, PieceType.PAWN): "卒",
        }
        return names[(self.color, self.piece_type)]

"""中国象棋走法生成器和规则引擎"""
from typing import Optional
from src.game.pieces import Color, Piece, PieceType
from src.game.board import Board


# 独立走法生成函数（用于测试）
def generate_rook_moves(board: Board, row: int, col: int, color: Color) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """车的走法：直线移动，不能越子"""
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 10 and 0 <= c < 9:
            target = board.get_piece(r, c)
            if not target:
                moves.append(((row, col), (r, c)))
            elif target.color != color:
                moves.append(((row, col), (r, c)))
                break
            else:
                break
            r += dr
            c += dc

    return moves


def generate_horse_moves(board: Board, row: int, col: int, color: Color) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """马的走法：日字形，蹩马腿检测"""
    moves = []
    horse_offsets = [
        (-2, -1, -1, 0), (-2, 1, -1, 0),
        (2, -1, 1, 0), (2, 1, 1, 0),
        (-1, -2, 0, -1), (1, -2, 0, -1),
        (-1, 2, 0, 1), (1, 2, 0, 1)
    ]

    for dr, dc, block_dr, block_dc in horse_offsets:
        new_r, new_c = row + dr, col + dc
        if 0 <= new_r < 10 and 0 <= new_c < 9:
            block_r, block_c = row + block_dr, col + block_dc
            if board.get_piece(block_r, block_c) is None:
                target = board.get_piece(new_r, new_c)
                if not target or target.color != color:
                    moves.append(((row, col), (new_r, new_c)))

    return moves


def generate_elephant_moves(board: Board, row: int, col: int, color: Color) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """象/相的走法：田字形，塞象眼，不能过河"""
    moves = []
    elephant_offsets = [(-2, -2), (-2, 2), (2, -2), (2, 2)]

    for dr, dc in elephant_offsets:
        new_r, new_c = row + dr, col + dc
        if 0 <= new_r < 10 and 0 <= new_c < 9:
            if color == Color.RED and new_r > 4:
                continue
            if color == Color.BLACK and new_r < 5:
                continue
            eye_r, eye_c = row + dr // 2, col + dc // 2
            if board.get_piece(eye_r, eye_c) is None:
                target = board.get_piece(new_r, new_c)
                if not target or target.color != color:
                    moves.append(((row, col), (new_r, new_c)))

    return moves


def generate_advisor_moves(board: Board, row: int, col: int, color: Color) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """士/仕的走法：九宫内斜走一格"""
    moves = []
    advisor_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in advisor_offsets:
        new_r, new_c = row + dr, col + dc
        if _in_palace(new_r, new_c, color):
            target = board.get_piece(new_r, new_c)
            if not target or target.color != color:
                moves.append(((row, col), (new_r, new_c)))

    return moves


def generate_king_moves(board: Board, row: int, col: int, color: Color) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """将/帅的走法：九宫内直走一格，或将帅对面"""
    moves = []
    king_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in king_offsets:
        new_r, new_c = row + dr, col + dc
        if _in_palace(new_r, new_c, color):
            target = board.get_piece(new_r, new_c)
            if not target or target.color != color:
                moves.append(((row, col), (new_r, new_c)))

    # 将帅对面（飞将）
    opponent = Color.BLACK if color == Color.RED else Color.RED
    try:
        opp_king_r, opp_king_c = board.find_king(opponent)
        if opp_king_c == col:  # 同一列
            # 检查中间是否有棋子
            has_piece_between = False
            start, end = min(row, opp_king_r), max(row, opp_king_r)
            for r in range(start + 1, end):
                if board.get_piece(r, col) is not None:
                    has_piece_between = True
                    break
            if not has_piece_between:
                moves.append(((row, col), (opp_king_r, opp_king_c)))
    except ValueError:
        pass  # 对方没有将/帅

    return moves


def generate_cannon_moves(board: Board, row: int, col: int, color: Color) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """炮的走法：直线移动，隔子吃子"""
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        platform_found = False

        while 0 <= r < 10 and 0 <= c < 9:
            target = board.get_piece(r, c)

            if not platform_found:
                if not target:
                    moves.append(((row, col), (r, c)))
                else:
                    platform_found = True
            else:
                if target:
                    if target.color != color:
                        moves.append(((row, col), (r, c)))
                    break

            r += dr
            c += dc

    return moves


def generate_pawn_moves(board: Board, row: int, col: int, color: Color) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """兵/卒的走法：过河前后走法不同，不可后退"""
    moves = []

    if color == Color.RED:
        forward = 1
        river_crossed = row >= 5
    else:
        forward = -1
        river_crossed = row <= 4

    new_r = row + forward
    if 0 <= new_r < 10:
        target = board.get_piece(new_r, col)
        if not target or target.color != color:
            moves.append(((row, col), (new_r, col)))

    if river_crossed:
        for dc in [-1, 1]:
            new_c = col + dc
            if 0 <= new_c < 9:
                target = board.get_piece(row, new_c)
                if not target or target.color != color:
                    moves.append(((row, col), (row, new_c)))

    return moves


def _in_palace(row: int, col: int, color: Color) -> bool:
    """检查位置是否在九宫内"""
    if color == Color.RED:
        return 0 <= row <= 2 and 3 <= col <= 5
    else:
        return 7 <= row <= 9 and 3 <= col <= 5


# MoveGenerator 类使用上述函数
class MoveGenerator:
    """生成所有合法走法并处理特殊规则"""

    def __init__(self, board: Board):
        self.board = board

    def get_legal_moves(self, row: int, col: int) -> list[tuple[int, int]]:
        """获取指定位置棋子的所有合法走法"""
        piece = self.board.get_piece(row, col)
        if not piece:
            return []

        moves = self._get_raw_moves(row, col, piece)

        legal_moves = []
        for to_row, to_col in moves:
            if self._is_legal_move(row, col, to_row, to_col):
                legal_moves.append((to_row, to_col))

        return legal_moves

    def _get_raw_moves(self, row: int, col: int, piece: Piece) -> list[tuple[int, int]]:
        """获取棋子的基础走法"""
        match piece.piece_type:
            case PieceType.ROOK:
                return [to for _, to in generate_rook_moves(self.board, row, col, piece.color)]
            case PieceType.HORSE:
                return [to for _, to in generate_horse_moves(self.board, row, col, piece.color)]
            case PieceType.ELEPHANT:
                return [to for _, to in generate_elephant_moves(self.board, row, col, piece.color)]
            case PieceType.ADVISOR:
                return [to for _, to in generate_advisor_moves(self.board, row, col, piece.color)]
            case PieceType.KING:
                return [to for _, to in generate_king_moves(self.board, row, col, piece.color)]
            case PieceType.CANNON:
                return [to for _, to in generate_cannon_moves(self.board, row, col, piece.color)]
            case PieceType.PAWN:
                return [to for _, to in generate_pawn_moves(self.board, row, col, piece.color)]
        return []

    def _is_legal_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """检查走法是否合法（不送将、不将帅对面等）"""
        piece = self.board.get_piece(from_row, from_col)
        if not piece:
            return False

        # 模拟走法
        original_target = self.board.grid[to_row][to_col]
        self.board.grid[to_row][to_col] = piece
        self.board.grid[from_row][from_col] = None

        # 检查是否被将军
        in_check = self.is_in_check(piece.color)

        # 恢复棋盘
        self.board.grid[from_row][from_col] = piece
        self.board.grid[to_row][to_col] = original_target

        return not in_check

    def is_in_check(self, color: Color) -> bool:
        """检查指定方是否被将军"""
        king_pos = self.board.find_king(color)
        opponent = Color.BLACK if color == Color.RED else Color.RED

        # 检查对方所有棋子是否可以攻击到将/帅
        for (row, col), piece in self.board.get_pieces(opponent):
            if self._can_attack(row, col, king_pos[0], king_pos[1]):
                return True

        return False

    def _can_attack(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """检查从from位置是否可以攻击到to位置（不考虑送将）"""
        piece = self.board.get_piece(from_row, from_col)
        if not piece:
            return False

        # 将帅对面特殊处理
        if piece.piece_type == PieceType.KING:
            # 检查是否同一列且中间无棋子
            if from_col == to_col:
                has_piece_between = False
                start, end = min(from_row, to_row), max(from_row, to_row)
                for r in range(start + 1, end):
                    if self.board.get_piece(r, from_col) is not None:
                        has_piece_between = True
                        break
                return not has_piece_between
            return False

        # 对于其他棋子，获取其基础走法看是否包含目标位置
        raw_moves = self._get_raw_moves(from_row, from_col, piece)
        return (to_row, to_col) in raw_moves

    def is_checkmate(self, color: Color) -> bool:
        """检查是否被将死"""
        if not self.is_in_check(color):
            return False

        # 检查是否有任何合法走法可以解除将军
        for (row, col), piece in self.board.get_pieces(color):
            legal_moves = self.get_legal_moves(row, col)
            if legal_moves:
                return False

        return True

    def is_stalemate(self, color: Color) -> bool:
        """检查是否困毙（无子可动且未被将军）"""
        if self.is_in_check(color):
            return False

        # 检查是否有任何合法走法
        for (row, col), piece in self.board.get_pieces(color):
            legal_moves = self.get_legal_moves(row, col)
            if legal_moves:
                return False

        return True

    def get_all_legal_moves(self, color: Color) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """获取指定方所有棋子的所有合法走法"""
        all_moves = []
        for (row, col), piece in self.board.get_pieces(color):
            moves = self.get_legal_moves(row, col)
            for to_row, to_col in moves:
                all_moves.append(((row, col), (to_row, to_col)))
        return all_moves

    def make_move(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """执行走法，返回是否成功"""
        legal_moves = self.get_legal_moves(from_row, from_col)
        if (to_row, to_col) not in legal_moves:
            return False

        piece = self.board.get_piece(from_row, from_col)
        self.board.grid[to_row][to_col] = piece
        self.board.grid[from_row][from_col] = None

        # 切换回合
        self.board.current_turn = Color.BLACK if self.board.current_turn == Color.RED else Color.RED

        return True

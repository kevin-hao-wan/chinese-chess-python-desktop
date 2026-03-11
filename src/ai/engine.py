"""AI引擎 - Minimax搜索与Alpha-Beta剪枝"""
from typing import Optional, Tuple
from src.game.board import Board
from src.game.pieces import Color
from src.game.rules import MoveGenerator
from src.ai.evaluate import evaluate_board

Pos = Tuple[int, int]
Move = Tuple[Pos, Pos]


class AIEngine:
    """中国象棋AI引擎"""

    def __init__(self, depth: int = 3):
        self.depth = depth

    def decide(self, board: Board) -> Move:
        """
        为当前回合方选择最佳走法
        返回 (from_pos, to_pos)
        """
        # AI 走当前轮到的一方
        ai_color = board.current_turn
        generator = MoveGenerator(board)
        legal_moves = generator.get_all_legal_moves(ai_color)

        if not legal_moves:
            raise RuntimeError("没有合法走法")

        # 使用Minimax搜索
        # AI 颜色为最大化方，对方为最小化方
        maximizing = True  # AI 总是最大化方
        _, best_move = self._minimax(board, self.depth, float('-inf'), float('inf'), maximizing, ai_color)

        if best_move is None:
            # 回退：选择第一个合法走法
            return legal_moves[0]

        return best_move

    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing: bool, ai_color: Color) -> Tuple[float, Optional[Move]]:
        """
        Minimax算法配合Alpha-Beta剪枝
        返回 (分数, 最佳走法)
        """
        # 当前要走棋的颜色
        current_color = ai_color if maximizing else self._opponent_color(ai_color)
        generator = MoveGenerator(board)

        # 终止条件
        if depth == 0:
            return evaluate_board(board), None

        legal_moves = generator.get_all_legal_moves(current_color)
        if not legal_moves:
            # 将死或困毙
            if generator.is_in_check(current_color):
                # 将死 - 最差分数
                return float('-inf') if maximizing else float('inf'), None
            else:
                # 困毙 - 平局（0分）
                return 0, None

        best_move = None
        opponent = self._opponent_color(ai_color)

        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                from_pos, to_pos = move
                # 执行走法
                captured = board.move_piece(from_pos, to_pos)
                board.current_turn = opponent

                eval_score, _ = self._minimax(board, depth - 1, alpha, beta, False, ai_color)

                # 撤销走法
                board.undo_move(from_pos, to_pos, captured)
                board.current_turn = ai_color

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta剪枝

            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                from_pos, to_pos = move
                # 执行走法
                captured = board.move_piece(from_pos, to_pos)
                board.current_turn = ai_color

                eval_score, _ = self._minimax(board, depth - 1, alpha, beta, True, ai_color)

                # 撤销走法
                board.undo_move(from_pos, to_pos, captured)
                board.current_turn = opponent

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha剪枝

            return min_eval, best_move

    def _opponent_color(self, color: Color) -> Color:
        """返回对方的颜色"""
        return Color.BLACK if color == Color.RED else Color.RED

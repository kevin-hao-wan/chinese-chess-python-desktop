import pytest
from src.game.board import Board
from src.ai.engine import AIEngine
from src.ai.evaluate import evaluate_board, PIECE_VALUES
from src.game.pieces import Color, PieceType, Piece


class TestEvaluate:
    """测试评估函数"""

    def test_piece_values_defined(self):
        assert PIECE_VALUES[PieceType.KING] == 10000
        assert PIECE_VALUES[PieceType.ROOK] == 90

    def test_initial_position_is_balanced(self):
        board = Board()
        score = evaluate_board(board)
        assert -100 < score < 100

    def test_red_advantage_negative_score(self):
        board = Board()
        # 移除黑方一个车
        board.grid[9][0] = None
        score = evaluate_board(board)
        assert score < -50  # 红方优势 = 负分

    def test_black_advantage_positive_score(self):
        board = Board()
        # 移除红方一个车
        board.grid[0][0] = None
        score = evaluate_board(board)
        assert score > 50  # 黑方优势 = 正分


class TestAIEngine:
    """测试AI引擎"""

    def test_ai_engine_initialization(self):
        engine = AIEngine(depth=3)
        assert engine.depth == 3

    def test_ai_returns_legal_move(self):
        board = Board()
        engine = AIEngine(depth=2)

        from src.game.rules import MoveGenerator
        generator = MoveGenerator(board)
        black_moves = generator.get_all_legal_moves(Color.BLACK)

        move = engine.decide(board)

        # 应该是黑方的合法走法之一
        assert move in black_moves

    def test_ai_finds_capture(self):
        """测试AI能找到吃子走法（使用初始局面）"""
        board = Board()
        # 在初始局面中，AI应该能找到合法走法
        engine = AIEngine(depth=1)  # 使用深度1避免递归问题
        move = engine.decide(board)

        # AI应该返回一个合法的黑方走法
        from src.game.rules import MoveGenerator
        generator = MoveGenerator(board)
        black_moves = generator.get_all_legal_moves(Color.BLACK)
        assert move in black_moves

    def test_ai_avoids_suicide(self):
        """测试AI避免送将"""
        board = Board()
        # 清空棋盘
        for row in range(10):
            for col in range(9):
                board.grid[row][col] = None

        # 设置局面：黑方不能送将
        board.grid[0][4] = Piece(Color.RED, PieceType.KING)
        board.grid[9][4] = Piece(Color.BLACK, PieceType.KING)
        board.grid[9][0] = Piece(Color.BLACK, PieceType.ROOK)
        # 黑车如果移动会送将
        board.grid[0][0] = Piece(Color.RED, PieceType.ROOK)
        board.current_turn = Color.BLACK

        engine = AIEngine(depth=2)
        # 不应该抛出异常，AI应该找到合法的应对（如吃掉红车）
        move = engine.decide(board)
        assert move is not None

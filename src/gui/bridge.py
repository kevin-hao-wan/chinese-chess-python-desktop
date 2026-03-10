"""Python-QML桥接类"""
from typing import List, Optional, Any
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl

from src.game.board import Board
from src.game.pieces import Color, PieceType
from src.game.rules import MoveGenerator
from src.ai.engine import AIEngine

Pos = tuple[int, int]


class GameBridge(QObject):
    """游戏桥接类，连接Python游戏逻辑和QML界面"""

    # 信号
    boardChanged = Signal()
    turnChanged = Signal()
    gameOver = Signal(str)
    selectedPosChanged = Signal()
    legalMovesChanged = Signal()

    def __init__(self):
        super().__init__()
        self._board = Board()
        self._selected_pos: Optional[Pos] = None
        self._legal_moves: List[Pos] = []

    def _get_board_data(self) -> List[dict]:
        """将棋盘转换为QML可用的列表"""
        data = []
        for row in range(10):
            for col in range(9):
                piece = self._board.get_piece(row, col)
                if piece:
                    data.append({
                        'row': row,
                        'col': col,
                        'color': piece.color.value,
                        'displayName': piece.display_name
                    })
        return data

    boardData = Property(list, _get_board_data, notify=boardChanged)

    def _get_turn_text(self) -> str:
        return "红方走棋" if self._board.current_turn == Color.RED else "黑方思考中"

    currentTurn = Property(str, _get_turn_text, notify=turnChanged)

    def _get_selected_pos(self) -> Any:
        return self._selected_pos

    selectedPos = Property('QVariant', _get_selected_pos, notify=selectedPosChanged)

    def _get_legal_moves(self) -> List[Pos]:
        return self._legal_moves

    legalMoves = Property('QVariant', _get_legal_moves, notify=legalMovesChanged)

    @Slot(int, int)
    def onCellClicked(self, row: int, col: int):
        """处理棋盘点击"""
        if self._board.current_turn != Color.RED:
            return

        if self._selected_pos is None:
            piece = self._board.get_piece(row, col)
            if piece and piece.color == Color.RED:
                self._selected_pos = (row, col)
                generator = MoveGenerator(self._board)
                all_moves = generator.get_all_legal_moves(Color.RED)
                self._legal_moves = [to for from_pos, to in all_moves if from_pos == self._selected_pos]
                self.selectedPosChanged.emit()
                self.legalMovesChanged.emit()
        else:
            if (row, col) in self._legal_moves:
                self._execute_move(self._selected_pos, (row, col))
            self._selected_pos = None
            self._legal_moves = []
            self.selectedPosChanged.emit()
            self.legalMovesChanged.emit()

    def _execute_move(self, from_pos: Pos, to_pos: Pos):
        """执行走法并触发AI"""
        self._board.move_piece(from_pos, to_pos)
        self._board.current_turn = Color.BLACK
        self.boardChanged.emit()
        self.turnChanged.emit()

        generator = MoveGenerator(self._board)
        if generator.is_checkmate(Color.BLACK):
            self.gameOver.emit("红方胜！")
            return
        if generator.is_stalemate(Color.BLACK):
            self.gameOver.emit("平局（困毙）")
            return

        self._ai_move()

    def _ai_move(self):
        """执行AI走法"""
        try:
            engine = AIEngine(depth=3)
            move = engine.decide(self._board)
            self._board.move_piece(move[0], move[1])
            self._board.current_turn = Color.RED
            self.boardChanged.emit()
            self.turnChanged.emit()

            generator = MoveGenerator(self._board)
            if generator.is_checkmate(Color.RED):
                self.gameOver.emit("黑方胜！")
            elif generator.is_stalemate(Color.RED):
                self.gameOver.emit("平局（困毙）")
        except Exception as e:
            print(f"AI错误: {e}")

    @Slot()
    def newGame(self):
        """新游戏"""
        self._board = Board()
        self._selected_pos = None
        self._legal_moves = []
        self.boardChanged.emit()
        self.turnChanged.emit()

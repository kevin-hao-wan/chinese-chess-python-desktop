"""Python-QML桥接类"""
from typing import List, Optional, Any
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QTimer

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
    playerColorChanged = Signal()

    def __init__(self):
        super().__init__()
        self._board = Board()
        self._selected_pos: Optional[Pos] = None
        self._legal_moves: List[Pos] = []
        self._player_color = Color.RED

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
        """根据玩家颜色和当前回合返回回合文本"""
        current = self._board.current_turn
        if current == self._player_color:
            # 玩家回合
            return "红方走棋" if current == Color.RED else "黑方走棋"
        else:
            # AI 回合
            return "红方思考中" if current == Color.RED else "黑方思考中"

    currentTurn = Property(str, _get_turn_text, notify=turnChanged)

    def _get_selected_row(self) -> int:
        return self._selected_pos[0] if self._selected_pos else -1

    selectedRow = Property(int, _get_selected_row, notify=selectedPosChanged)

    def _get_selected_col(self) -> int:
        return self._selected_pos[1] if self._selected_pos else -1

    selectedCol = Property(int, _get_selected_col, notify=selectedPosChanged)

    def _get_legal_moves(self) -> List[dict]:
        """将合法走法转换为QML可用的字典列表"""
        return [{'row': r, 'col': c} for r, c in self._legal_moves]

    legalMoves = Property(list, _get_legal_moves, notify=legalMovesChanged)

    @Slot(int, int)
    def onCellClicked(self, row: int, col: int):
        """处理棋盘点击"""
        if self._board.current_turn != self._player_color:
            return

        clicked_piece = self._board.get_piece(row, col)

        if self._selected_pos is None:
            # 无选中时，只能选中己方棋子
            if clicked_piece and clicked_piece.color == self._player_color:
                self._select_piece(row, col)
        else:
            # 已有选中
            if (row, col) in self._legal_moves:
                # 点击合法走法，执行移动
                self._execute_move(self._selected_pos, (row, col))
                self._clear_selection()
            elif clicked_piece and clicked_piece.color == self._player_color:
                # 点击另一个己方棋子，切换选择
                self._clear_selection()
                self._select_piece(row, col)
            else:
                # 点击非法位置，取消选择
                self._clear_selection()

    def _select_piece(self, row: int, col: int):
        """选中指定位置的棋子"""
        self._selected_pos = (row, col)
        generator = MoveGenerator(self._board)
        all_moves = generator.get_all_legal_moves(self._player_color)
        self._legal_moves = [to for from_pos, to in all_moves if from_pos == self._selected_pos]
        self.selectedPosChanged.emit()
        self.legalMovesChanged.emit()

    def _clear_selection(self):
        """清除当前选择"""
        self._selected_pos = None
        self._legal_moves = []
        self.selectedPosChanged.emit()
        self.legalMovesChanged.emit()

    def _execute_move(self, from_pos: Pos, to_pos: Pos):
        """执行走法并触发AI"""
        # 计算AI颜色
        ai_color = Color.BLACK if self._player_color == Color.RED else Color.RED

        self._board.move_piece(from_pos, to_pos)
        self._board.current_turn = ai_color
        self.boardChanged.emit()
        self.turnChanged.emit()

        generator = MoveGenerator(self._board)
        if generator.is_checkmate(ai_color):
            # 根据 player_color 判断胜者
            winner = "红方胜！" if self._player_color == Color.RED else "黑方胜！"
            self.gameOver.emit(winner)
            return
        if generator.is_stalemate(ai_color):
            self.gameOver.emit("平局（困毙）")
            return

        self._ai_move()

    def _ai_move(self):
        """执行AI走法"""
        try:
            engine = AIEngine(depth=3)
            move = engine.decide(self._board)
            self._board.move_piece(move[0], move[1])
            self._board.current_turn = self._player_color
            self.boardChanged.emit()
            self.turnChanged.emit()

            generator = MoveGenerator(self._board)
            if generator.is_checkmate(self._player_color):
                winner = "红方胜！" if self._player_color == Color.BLACK else "黑方胜！"
                self.gameOver.emit(winner)
            elif generator.is_stalemate(self._player_color):
                self.gameOver.emit("平局（困毙）")
        except Exception as e:
            print(f"AI错误: {e}")

    @Slot(int)
    def newGame(self, player_color_value: int = None):
        """新游戏"""
        # 设置玩家颜色（如果传入）
        if player_color_value is not None:
            self._set_player_color(player_color_value)

        self._board = Board()
        self._selected_pos = None
        self._legal_moves = []

        # 如果玩家选择黑方，AI（红方）先手
        if self._player_color == Color.BLACK:
            self._board.current_turn = Color.RED
            QTimer.singleShot(100, self._ai_move)
        else:
            self._board.current_turn = Color.RED

        self.boardChanged.emit()
        self.turnChanged.emit()

    def _get_player_color(self) -> int:
        """获取玩家颜色，返回 0=红方, 1=黑方"""
        return 0 if self._player_color == Color.RED else 1

    def _set_player_color(self, color_value: int):
        """设置玩家颜色，color_value: 0=红方, 1=黑方"""
        # 将整数映射到 Color 枚举
        color_map = {0: Color.RED, 1: Color.BLACK}
        self._player_color = color_map.get(color_value, Color.RED)
        self.playerColorChanged.emit()

    playerColor = Property(int, _get_player_color, _set_player_color, notify=playerColorChanged)

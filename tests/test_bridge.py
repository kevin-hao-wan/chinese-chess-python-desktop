import pytest
from src.gui.bridge import GameBridge
from src.game.pieces import Color


def test_player_color_defaults_to_red():
    """测试 player_color 默认为红方"""
    bridge = GameBridge()
    assert bridge.playerColor == Color.RED.value


def test_on_cell_clicked_respects_player_color():
    """测试 onCellClicked 根据 player_color 判断可操作方"""
    from unittest.mock import MagicMock, patch

    bridge = GameBridge()

    # 设置玩家为黑方
    bridge._player_color = Color.BLACK
    bridge._board.current_turn = Color.BLACK

    # 模拟在 (0,0) 有黑方棋子（车）
    with patch.object(bridge._board, 'get_piece') as mock_get_piece:
        mock_piece = MagicMock()
        mock_piece.color = Color.BLACK
        mock_get_piece.return_value = mock_piece

        # 应该可以选中己方（黑方）棋子
        bridge.onCellClicked(0, 0)
        assert bridge.selectedRow == 0
        assert bridge.selectedCol == 0

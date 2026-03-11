import pytest
from src.gui.bridge import GameBridge
from src.game.pieces import Color


def test_player_color_defaults_to_red():
    """测试 player_color 默认为红方"""
    bridge = GameBridge()
    assert bridge.playerColor == Color.RED.value

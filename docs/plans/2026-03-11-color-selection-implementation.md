# AI 执棋方选择功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为中国象棋游戏增加执棋方选择功能，允许玩家选择执红先行（默认）或执黑后行（AI 先手）。

**Architecture:** 在 GameBridge 中新增 player_color 属性，修改回合判断逻辑；创建 ColorSelectionDialog QML 组件；使用 QSettings 记住上次选择。

**Tech Stack:** Python 3, PySide6 (QML/Qt Quick), pytest, pytest-qt

---

## 前置准备

### 检查项目结构

确认项目文件存在：
- `src/gui/bridge.py` - GameBridge 类
- `src/gui/main.qml` - 主窗口
- `tests/test_game.py` - 测试文件（如果不存在需要创建）

---

## Task 1: 添加 player_color 属性到 GameBridge

**Files:**
- Modify: `src/gui/bridge.py`
- Test: `tests/test_bridge.py` (新建)

**Step 1: 编写测试 - player_color 属性默认值**

```python
import pytest
from src.gui.bridge import GameBridge
from src.game.pieces import Color


def test_player_color_defaults_to_red():
    """测试 player_color 默认为红方"""
    bridge = GameBridge()
    assert bridge.playerColor == Color.RED.value
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/test_bridge.py::test_player_color_defaults_to_red -v
```

Expected: FAIL - AttributeError: 'GameBridge' object has no attribute 'playerColor'

**Step 3: 实现 player_color 属性**

在 `src/gui/bridge.py` 的 `__init__` 方法中添加：

```python
def __init__(self):
    super().__init__()
    self._board = Board()
    self._selected_pos: Optional[Pos] = None
    self._legal_moves: List[Pos] = []
    self._player_color = Color.RED  # 新增：默认为红方
```

在类中添加属性访问器（在 `legalMoves` 属性之后）：

```python
def _get_player_color(self) -> int:
    """获取玩家颜色"""
    return self._player_color.value

def _set_player_color(self, color_value: int):
    """设置玩家颜色"""
    self._player_color = Color(color_value)
    self.playerColorChanged.emit()

playerColor = Property(int, _get_player_color, _set_player_color, notify=playerColorChanged)
```

在信号声明区域添加（在 `legalMovesChanged = Signal()` 之后）：

```python
playerColorChanged = Signal()
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/test_bridge.py::test_player_color_defaults_to_red -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/gui/bridge.py tests/test_bridge.py
git commit -m "feat: add player_color property to GameBridge

- Add _player_color attribute defaulting to RED
- Add playerColor property with getter/setter
- Add playerColorChanged signal

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: 修改 onCellClicked 使用 player_color

**Files:**
- Modify: `src/gui/bridge.py:68-91`
- Test: `tests/test_bridge.py`

**Step 1: 编写测试 - 根据 player_color 判断可操作方**

```python
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
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/test_bridge.py::test_on_cell_clicked_respects_player_color -v
```

Expected: FAIL - 当前代码硬编码检查 Color.RED

**Step 3: 修改 onCellClicked 方法**

将 `src/gui/bridge.py` 中的 `onCellClicked` 方法（第 68-91 行）修改为：

```python
@Slot(int, int)
def onCellClicked(self, row: int, col: int):
    """处理棋盘点击"""
    # 修改：根据玩家颜色判断是否可操作
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
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/test_bridge.py::test_on_cell_clicked_respects_player_color -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/gui/bridge.py tests/test_bridge.py
git commit -m "feat: modify onCellClicked to respect player_color

- Replace hardcoded Color.RED checks with self._player_color
- Allow player to control either color based on selection

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: 修改 _select_piece 使用 player_color

**Files:**
- Modify: `src/gui/bridge.py:93-100`
- Test: `tests/test_bridge.py`

**Step 1: 编写测试**

```python
def test_select_piece_uses_player_color_for_moves():
    """测试 _select_piece 根据 player_color 获取合法走法"""
    bridge = GameBridge()
    bridge._player_color = Color.BLACK
    bridge._board.current_turn = Color.BLACK

    # 选择黑方棋子，应该获取黑方走法
    # 由于 Board 初始状态红方在下、黑方在上，选择 (0,0) 应该是黑车
    # 注意：这里依赖实际 board 状态，可能需要 mock
    from unittest.mock import patch, MagicMock

    with patch('src.gui.bridge.MoveGenerator') as mock_gen_class:
        mock_gen = MagicMock()
        mock_gen_class.return_value = mock_gen
        mock_gen.get_all_legal_moves.return_value = [((0, 0), (0, 1))]

        bridge._select_piece(0, 0)

        # 验证使用 player_color (BLACK) 获取走法
        mock_gen.get_all_legal_moves.assert_called_once_with(Color.BLACK)
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/test_bridge.py::test_select_piece_uses_player_color_for_moves -v
```

Expected: FAIL - 当前使用 Color.RED

**Step 3: 修改 _select_piece 方法**

```python
def _select_piece(self, row: int, col: int):
    """选中指定位置的棋子"""
    self._selected_pos = (row, col)
    generator = MoveGenerator(self._board)
    # 修改：使用 player_color 而非硬编码 Color.RED
    all_moves = generator.get_all_legal_moves(self._player_color)
    self._legal_moves = [to for from_pos, to in all_moves if from_pos == self._selected_pos]
    self.selectedPosChanged.emit()
    self.legalMovesChanged.emit()
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/test_bridge.py::test_select_piece_uses_player_color_for_moves -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/gui/bridge.py tests/test_bridge.py
git commit -m "feat: modify _select_piece to use player_color

- Use self._player_color instead of hardcoded Color.RED
- Generate legal moves for the correct color

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: 修改 newGame 支持 player_color 参数和 AI 先手

**Files:**
- Modify: `src/gui/bridge.py:144-151`
- Test: `tests/test_bridge.py`

**Step 1: 编写测试 - newGame 接受 player_color 参数**

```python
def test_new_game_accepts_player_color():
    """测试 newGame 接受 player_color 参数"""
    bridge = GameBridge()

    # 设置玩家为黑方
    bridge.newGame(Color.BLACK.value)

    assert bridge.playerColor == Color.BLACK.value
    assert bridge._board.current_turn == Color.RED  # AI（红方）先手
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/test_bridge.py::test_new_game_accepts_player_color -v
```

Expected: FAIL - newGame 不接受参数

**Step 3: 修改 newGame 方法**

```python
@Slot(int)
def newGame(self, player_color_value: int = None):
    """新游戏

    Args:
        player_color_value: 玩家选择的颜色（Color.RED 或 Color.BLACK）
                           如果为 None，则使用当前 player_color
    """
    # 如果传入了新的玩家颜色，则更新
    if player_color_value is not None:
        self._set_player_color(player_color_value)

    self._board = Board()
    self._selected_pos = None
    self._legal_moves = []

    # 如果玩家执黑，AI（红方）先手
    if self._player_color == Color.BLACK:
        self._board.current_turn = Color.RED
        self.boardChanged.emit()
        self.turnChanged.emit()
        # 延迟触发 AI 走棋，确保 UI 已更新
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, self._ai_move)
    else:
        self._board.current_turn = Color.RED  # 玩家执红，红方先手
        self.boardChanged.emit()
        self.turnChanged.emit()
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/test_bridge.py::test_new_game_accepts_player_color -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add src/gui/bridge.py tests/test_bridge.py
git commit -m "feat: modify newGame to support player color selection

- Add player_color_value parameter to newGame slot
- Initialize game with correct starting turn
- Trigger AI first move when player chooses black

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: 修改 _execute_move 使用 player_color

**Files:**
- Modify: `src/gui/bridge.py:109-124`
- Test: `tests/test_bridge.py`

**Step 1: 编写测试**

```python
def test_execute_move_switches_to_ai_color():
    """测试 _execute_move 正确切换到 AI 颜色"""
    bridge = GameBridge()
    bridge._player_color = Color.BLACK  # 玩家执黑
    bridge._board.current_turn = Color.BLACK

    # 需要 mock 一些方法来完成测试
    from unittest.mock import patch, MagicMock

    with patch.object(bridge._board, 'move_piece'):
        with patch.object(bridge, '_ai_move'):
            with patch('src.gui.bridge.MoveGenerator') as mock_gen_class:
                mock_gen = MagicMock()
                mock_gen_class.return_value = mock_gen
                mock_gen.is_checkmate.return_value = False
                mock_gen.is_stalemate.return_value = False

                bridge._execute_move((0, 0), (0, 1))

                # 玩家（黑）走完后，应该切换到红方（AI）
                assert bridge._board.current_turn == Color.RED
```

**Step 2: 运行测试确认失败**

**Step 3: 修改 _execute_move 方法**

```python
def _execute_move(self, from_pos: Pos, to_pos: Pos):
    """执行走法并触发AI"""
    self._board.move_piece(from_pos, to_pos)
    # 修改：切换到 AI 的颜色（玩家的对立颜色）
    ai_color = Color.BLACK if self._player_color == Color.RED else Color.RED
    self._board.current_turn = ai_color
    self.boardChanged.emit()
    self.turnChanged.emit()

    generator = MoveGenerator(self._board)
    if generator.is_checkmate(ai_color):
        winner = "红方" if self._player_color == Color.RED else "黑方"
        self.gameOver.emit(f"{winner}胜！")
        return
    if generator.is_stalemate(ai_color):
        self.gameOver.emit("平局（困毙）")
        return

    self._ai_move()
```

**Step 4: 运行测试确认通过**

**Step 5: Commit**

```bash
git add src/gui/bridge.py tests/test_bridge.py
git commit -m "feat: modify _execute_move to use player_color

- Switch to AI color after player move
- Determine winner based on player_color

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: 修改 _ai_move 使用 player_color

**Files:**
- Modify: `src/gui/bridge.py:126-142`
- Test: `tests/test_bridge.py`

**Step 1: 编写测试**

```python
def test_ai_move_switches_to_player_color():
    """测试 AI 走完后切换回玩家颜色"""
    bridge = GameBridge()
    bridge._player_color = Color.BLACK
    bridge._board.current_turn = Color.RED  # AI 回合

    from unittest.mock import patch, MagicMock

    with patch('src.gui.bridge.AIEngine') as mock_engine_class:
        mock_engine = MagicMock()
        mock_engine_class.return_value = mock_engine
        mock_engine.decide.return_value = ((0, 0), (0, 1))

        with patch.object(bridge._board, 'move_piece'):
            with patch('src.gui.bridge.MoveGenerator') as mock_gen_class:
                mock_gen = MagicMock()
                mock_gen_class.return_value = mock_gen
                mock_gen.is_checkmate.return_value = False
                mock_gen.is_stalemate.return_value = False

                bridge._ai_move()

                # AI（红）走完后，应该切换回玩家（黑）
                assert bridge._board.current_turn == Color.BLACK
```

**Step 2: 运行测试确认失败**

**Step 3: 修改 _ai_move 方法**

```python
def _ai_move(self):
    """执行AI走法"""
    try:
        engine = AIEngine(depth=3)
        move = engine.decide(self._board)
        self._board.move_piece(move[0], move[1])
        # 修改：切换回玩家颜色
        self._board.current_turn = self._player_color
        self.boardChanged.emit()
        self.turnChanged.emit()

        generator = MoveGenerator(self._board)
        if generator.is_checkmate(self._player_color):
            self.gameOver.emit("黑方胜！")
        elif generator.is_stalemate(self._player_color):
            self.gameOver.emit("平局（困毙）")
    except Exception as e:
        print(f"AI错误: {e}")
```

**Step 4: 运行测试确认通过**

**Step 5: Commit**

```bash
git add src/gui/bridge.py tests/test_bridge.py
git commit -m "feat: modify _ai_move to use player_color

- Switch back to player color after AI move
- Determine game over based on player_color

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 7: 修改 _get_turn_text 支持动态提示

**Files:**
- Modify: `src/gui/bridge.py:46-49`
- Test: `tests/test_bridge.py`

**Step 1: 编写测试**

```python
def test_turn_text_shows_ai_thinking():
    """测试回合文本显示 AI 思考中"""
    bridge = GameBridge()

    # 玩家执红，红方回合
    bridge._player_color = Color.RED
    bridge._board.current_turn = Color.RED
    assert bridge.currentTurn == "红方走棋"

    # 切换到黑方（AI）
    bridge._board.current_turn = Color.BLACK
    assert bridge.currentTurn == "黑方思考中"

    # 玩家执黑，黑方回合
    bridge._player_color = Color.BLACK
    bridge._board.current_turn = Color.BLACK
    assert bridge.currentTurn == "黑方走棋"

    # 切换到红方（AI）
    bridge._board.current_turn = Color.RED
    assert bridge.currentTurn == "红方思考中"
```

**Step 2: 运行测试确认失败**

**Step 3: 修改 _get_turn_text 方法**

```python
def _get_turn_text(self) -> str:
    """获取当前回合显示文本"""
    current = self._board.current_turn

    # 判断当前是玩家还是 AI
    if current == self._player_color:
        # 玩家回合
        return "红方走棋" if current == Color.RED else "黑方走棋"
    else:
        # AI 回合
        return "红方思考中" if current == Color.RED else "黑方思考中"
```

**Step 4: 运行测试确认通过**

**Step 5: Commit**

```bash
git add src/gui/bridge.py tests/test_bridge.py
git commit -m "feat: modify _get_turn_text for dynamic turn indicators

- Show 'thinking' when it's AI's turn
- Show 'your turn' when it's player's turn
- Adapt text based on player_color selection

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 8: 创建 ColorSelectionDialog QML 组件

**Files:**
- Create: `src/gui/ColorSelectionDialog.qml`
- Modify: `src/gui/main.qml`

**Step 1: 创建 ColorSelectionDialog.qml**

```qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs

Dialog {
    id: colorSelectionDialog
    title: "选择执棋方"
    modal: true
    standardButtons: Dialog.Ok | Dialog.Cancel

    // 信号
    signal colorSelected(int colorValue)

    // 属性
    property int selectedColor: 0  // 0 = 红, 1 = 黑

    ColumnLayout {
        spacing: 20

        Label {
            text: "请选择您要执的棋子："
            font.pixelSize: 16
        }

        RadioButton {
            id: redRadio
            text: "执红先行（先手）"
            checked: colorSelectionDialog.selectedColor === 0
            onClicked: colorSelectionDialog.selectedColor = 0
        }

        RadioButton {
            id: blackRadio
            text: "执黑后行（后手）"
            checked: colorSelectionDialog.selectedColor === 1
            onClicked: colorSelectionDialog.selectedColor = 1
        }
    }

    onAccepted: {
        colorSelected(selectedColor)
    }
}
```

**Step 2: 在 main.qml 中引入并使用**

在 `main.qml` 的 `ApplicationWindow` 中添加：

```qml
// 在 ColumnLayout 之后，Connections 之前添加
ColorSelectionDialog {
    id: colorDialog
    onColorSelected: function(colorValue) {
        if (gameBridge) {
            resultText.visible = false;
            gameBridge.newGame(colorValue);
        }
    }
}
```

修改"新游戏"按钮的 onClicked：

```qml
Button {
    text: "新游戏"
    Layout.alignment: Qt.AlignHCenter
    onClicked: {
        colorDialog.open();
    }
}
```

**Step 3: 运行应用测试**

```bash
python main.py
```

点击"新游戏"按钮，确认对话框弹出。

**Step 4: Commit**

```bash
git add src/gui/ColorSelectionDialog.qml src/gui/main.qml
git commit -m "feat: add ColorSelectionDialog QML component

- Create dialog with radio buttons for color selection
- Integrate with main.qml new game button
- Emit colorSelected signal with chosen color

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 9: 添加 QSettings 记住上次选择

**Files:**
- Modify: `src/gui/ColorSelectionDialog.qml`
- Modify: `src/gui/main.qml`

**Step 1: 修改 main.qml 添加 Settings**

在 main.qml 顶部添加 import：

```qml
import QtCore  // 用于 Settings
```

在 ApplicationWindow 中添加 Settings：

```qml
ApplicationWindow {
    // ... 现有代码 ...

    Settings {
        id: appSettings
        property int lastSelectedColor: 0  // 默认红方
    }

    // ... 其余代码 ...
}
```

**Step 2: 修改 ColorSelectionDialog 使用保存的设置**

```qml
ColorSelectionDialog {
    id: colorDialog

    Component.onCompleted: {
        selectedColor = appSettings.lastSelectedColor
    }

    onColorSelected: function(colorValue) {
        // 保存选择
        appSettings.lastSelectedColor = colorValue

        if (gameBridge) {
            resultText.visible = false;
            gameBridge.newGame(colorValue);
        }
    }
}
```

**Step 3: 运行应用测试**

```bash
python main.py
```

1. 选择"执黑后行"，开始游戏
2. 关闭应用
3. 重新打开应用，点击"新游戏"
4. 确认默认选中"执黑后行"

**Step 4: Commit**

```bash
git add src/gui/main.qml src/gui/ColorSelectionDialog.qml
git commit -m "feat: remember last color selection with QSettings

- Add Settings to store lastSelectedColor
- Restore previous selection on dialog open
- Save selection when starting new game

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 10: 运行所有测试

**Files:**
- Test: `tests/`

**Step 1: 运行完整测试套件**

```bash
pytest tests/ -v
```

Expected: 所有测试通过

**Step 2: 运行集成测试验证完整流程**

```bash
pytest tests/test_integration.py -v -s
```

**Step 3: Commit**

```bash
git commit -m "test: verify all tests pass for color selection feature

- All unit tests passing
- Integration tests verify both game modes

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## 完成检查清单

- [x] player_color 属性添加到 GameBridge
- [x] onCellClicked 使用 player_color
- [x] _select_piece 使用 player_color
- [x] newGame 支持 player_color 参数和 AI 先手
- [x] _execute_move 使用 player_color
- [x] _ai_move 使用 player_color
- [x] _get_turn_text 显示动态提示
- [x] ColorSelectionDialog QML 组件
- [x] QSettings 记住上次选择
- [x] 所有测试通过

---

## 相关文档

- 设计文档: `docs/plans/2026-03-11-color-selection-design.md`
- OpenSpec 变更: `openspec/changes/color-selection/`
- 需求文档: `requirement.md`

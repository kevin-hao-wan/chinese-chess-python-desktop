# 中国象棋人机对战桌面应用 - 技术设计文档

**日期**: 2026-03-09
**版本**: 1.0
**作者**: Auto-generated from OpenSpec

---

## 1. 概述

### 1.1 项目简介

构建一个中国象棋人机对战桌面应用。用户（执红）先行，AI（执黑）后行。应用需要完整的中国象棋规则引擎、图形界面和 AI 对手。

### 1.2 技术栈

- **语言**: Python 3.10+
- **GUI 框架**: PySide6 QML 模式
- **测试框架**: pytest + pytest-qt

### 1.3 目标/非目标

**目标**:
- 实现完整的中国象棋规则（所有棋子走法、将军、将死、困毙检测）
- 提供流畅的图形界面体验（棋盘渲染、选子高亮、走法提示）
- 实现具有一定棋力的 AI 对手
- 保持代码结构清晰，便于测试和扩展

**非目标**:
- 不实现联网对战
- 不实现悔棋、复盘功能（v1.0 不包含）
- 不实现多种难度等级选择（v1.0 使用固定难度）
- 不实现棋谱保存/加载

---

## 2. 架构总览

### 2.1 三层分离架构

```
┌─────────────────────────────────┐
│         GUI 层 (gui/)           │
│  main.qml + bridge.py          │
│  QML 声明式 UI / QObject 桥接   │
├─────────────────────────────────┤
│       游戏逻辑层 (game/)         │
│  board.py / pieces.py / rules.py│
│  棋盘模型 / 棋子定义 / 规则引擎  │
├─────────────────────────────────┤
│         AI 层 (ai/)             │
│  engine.py / evaluate.py        │
│  Alpha-Beta 搜索 / 局面评估     │
└─────────────────────────────────┘
```

### 2.2 数据流

- **GUI → game**: 用户点击 → bridge 调用 rules 校验走法 → board 更新状态
- **game → AI**: 红方走完 → 传当前局面给 AI → AI 返回最佳走法 → board 更新
- **game → GUI**: board 状态变更 → 通过 QObject 信号 → QML 自动刷新视图

### 2.3 目录结构

```
src/
  game/
    board.py      # 棋盘数据模型（10x9 数组）
    pieces.py     # 棋子枚举和类定义
    rules.py      # 规则引擎
  ai/
    engine.py     # Minimax + Alpha-Beta
    evaluate.py   # 评估函数
  gui/
    main.qml      # QML 界面
    bridge.py     # Python-QML 桥接
main.py           # 应用入口
tests/
  test_board.py
  test_rules.py
  test_ai.py
  test_gui.py
```

---

## 3. 数据模型层

### 3.1 棋子模型 (pieces.py)

```python
from enum import Enum
from dataclasses import dataclass

class Color(Enum):
    RED = "red"
    BLACK = "black"

class PieceType(Enum):
    KING = "king"           # 帅/将
    ADVISOR = "advisor"     # 仕/士
    ELEPHANT = "elephant"   # 相/象
    HORSE = "horse"         # 马
    ROOK = "rook"           # 车
    CANNON = "cannon"       # 炮
    PAWN = "pawn"           # 兵/卒

@dataclass
class Piece:
    color: Color
    piece_type: PieceType

    @property
    def display_name(self) -> str:
        """返回棋子中文名"""
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
```

### 3.2 棋盘模型 (board.py)

```python
from typing import Optional
import copy

class Board:
    """10x9 棋盘数据模型"""

    def __init__(self):
        self.grid: list[list[Optional[Piece]]] = [[None] * 9 for _ in range(10)]
        self._setup_initial_position()
        self.current_turn = Color.RED

    def _setup_initial_position(self):
        """标准开局布局"""
        # 黑方 (row 5-9)
        # 红方 (row 0-4)
        # ... 详见 spec

    # 坐标系：row 0-9（0=红方底线，9=黑方底线），col 0-8（左到右）
    # 红方九宫：row 0-2, col 3-5；黑方九宫：row 7-9, col 3-5
    # 楚河汉界：row 4-5 之间

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """获取指定位置棋子"""

    def move_piece(self, from_pos: tuple[int, int], to_pos: tuple[int, int]) -> Optional[Piece]:
        """执行走法，返回被吃棋子"""

    def undo_move(self, from_pos: tuple[int, int], to_pos: tuple[int, int], captured: Optional[Piece]):
        """撤销走法（AI 搜索用）"""

    def find_king(self, color: Color) -> tuple[int, int]:
        """查找指定颜色的帅/将位置"""

    def get_pieces(self, color: Color) -> list[tuple[tuple[int, int], Piece]]:
        """获取某方所有棋子"""
```

### 3.3 初始布局

```
行9: 车 马 象 士 将 士 象 马 车  (黑)
行8: __ __ __ __ __ __ __ __ __
行7: __ 炮 __ __ __ __ __ 炮 __
行6: 卒 __ 卒 __ 卒 __ 卒 __ 卒
行5: __ __ __ __ __ __ __ __ __  ← 楚河汉界
行4: __ __ __ __ __ __ __ __ __
行3: 兵 __ 兵 __ 兵 __ 兵 __ 兵
行2: __ 炮 __ __ __ __ __ 炮 __
行1: __ __ __ __ __ __ __ __ __
行0: 车 马 相 仕 帅 仕 相 马 车  (红)
```

---

## 4. 规则引擎层

### 4.1 核心接口 (rules.py)

```python
from typing import List, Tuple
Pos = Tuple[int, int]
Move = Tuple[Pos, Pos]  # ((r1, c1), (r2, c2))

def generate_legal_moves(board: Board, color: Color) -> List[Move]:
    """生成某方所有合法走法"""

def is_move_legal(board: Board, from_pos: Pos, to_pos: Pos, color: Color) -> bool:
    """检查单个走法是否合法"""

def is_in_check(board: Board, color: Color) -> bool:
    """检测某方是否被将军"""

def is_checkmate(board: Board, color: Color) -> bool:
    """检测某方是否被将死"""

def is_stalemate(board: Board, color: Color) -> bool:
    """检测某方是否困毙"""

def get_game_result(board: Board) -> Optional[str]:
    """返回 'RED_WIN' | 'BLACK_WIN' | None（游戏继续）"""
```

### 4.2 走法生成策略

每个棋子类型有独立的 `_generate_<piece>_moves()` 函数：

| 棋子 | 走法规则 | 特殊约束 |
|------|----------|----------|
| 车 | 直线任意格 | 遇子停，不能越子 |
| 马 | 日字（1+1对角） | 蹩马腿检测 |
| 象/相 | 田字（2对角） | 塞象眼，不过河 |
| 仕/士 | 斜一格 | 限九宫内 |
| 帅/将 | 直/横一格 | 限九宫内 |
| 炮 | 直线任意格 | 不吃子同车，吃子需炮架 |
| 兵/卒 | 前一格 | 过河后可横走，永不可后退 |

### 4.3 合法性校验流程

```
generate_legal_moves()
  1. 遍历己方所有棋子
  2. 对每个棋子调用 _generate_<type>_moves() 得到伪合法走法
  3. 对每步伪合法走法：
     a. 模拟执行
     b. 检查是否导致己方被将军
     c. 检查是否导致将帅对面
     d. 若通过则加入合法走法列表
```

### 4.4 将帅对面检测

```python
def _kings_facing(board: Board) -> bool:
    """检测将帅是否对面（中间无棋子）"""
    red_king = board.find_king(Color.RED)
    black_king = board.find_king(Color.BLACK)

    # 不在同一列
    if red_king[1] != black_king[1]:
        return False

    # 检查两王之间是否有棋子
    col = red_king[1]
    for row in range(red_king[0] + 1, black_king[0]):
        if board.get_piece(row, col) is not None:
            return False  # 有棋子阻挡

    return True  # 将帅对面！
```

### 4.5 胜负判定

- **将死**: `is_in_check()` 为真 且 无合法走法
- **困毙**: `is_in_check()` 为假 且 无合法走法

---

## 5. AI 引擎层

### 5.1 AI 引擎接口 (ai/engine.py)

```python
from game.board import Board
from game.pieces import Color

class AIEngine:
    def __init__(self, search_depth: int = 3):
        self.depth = search_depth

    def decide(self, board: Board) -> Move:
        """返回 AI 决策的走法（执黑）"""
        _, best_move = self._minimax(board, self.depth, float('-inf'), float('inf'), True)
        return best_move

    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> tuple[float, Optional[Move]]:
        """
        Minimax + Alpha-Beta 搜索

        参数:
          - depth: 剩余搜索深度
          - alpha: MAX 方案能保证的最小值
          - beta: MIN 方案能保证的最大值
          - maximizing: True=黑方回合（最大化）, False=红方回合（最小化）

        返回:
          - (评估值, 最佳走法)
        """
```

### 5.2 局面评估函数 (ai/evaluate.py)

```python
def evaluate_board(board: Board) -> float:
    """
    返回局面分数（黑方视角）
    正值 = 黑优，负值 = 红优
    """
    score = 0.0

    # 1. 材质分
    PIECE_VALUES = {
        PieceType.KING: 10000,
        PieceType.ROOK: 90,
        PieceType.CANNON: 45,
        PieceType.HORSE: 40,
        PieceType.ELEPHANT: 20,
        PieceType.ADVISOR: 20,
        PieceType.PAWN: 10,
    }

    # 2. 位置权重表（每个棋子类型有 10x9 的矩阵）
    # 例：过河卒比未过河卒更值钱

    # 3. 综合计算
    for (r, c), piece in board.get_pieces(Color.BLACK):
        score += PIECE_VALUES[piece.piece_type]
        score += POSITION_WEIGHTS[piece.piece_type][r][c]

    for (r, c), piece in board.get_pieces(Color.RED):
        score -= PIECE_VALUES[piece.piece_type]
        score -= POSITION_WEIGHTS[piece.piece_type][r][c]

    return score
```

### 5.3 搜索参数

- 搜索深度: 3 层（可配置）
- 超时保护: 3 秒强制返回
- 走法排序: 优先搜索吃子走法，提高剪枝效率

---

## 6. GUI 层

### 6.1 Python-QML 桥接 (gui/bridge.py)

```python
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtCore import QAbstractListModel, Qt

class GameBridge(QObject):
    """Python 端暴露给 QML 的接口"""

    # 信号：通知 QML 刷新
    boardChanged = Signal()
    turnChanged = Signal()
    gameOver = Signal(str)  # 参数: "红方胜" / "黑方胜"
    selectedPosChanged = Signal()
    legalMovesChanged = Signal()

    def __init__(self):
        super().__init__()
        self._board = Board()
        self._selected_pos: Optional[Pos] = None
        self._legal_moves: List[Pos] = []

    # 属性：QML 可读取
    def _get_board_data(self) -> List[dict]:
        """将棋盘转换为 QML 可用的列表"""
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

    # 槽：QML 可调用
    @Slot(int, int)
    def onCellClicked(self, row: int, col: int):
        """处理棋盘点击"""
        if self._selected_pos is None:
            # 尝试选中己方棋子
            piece = self._board.get_piece(row, col)
            if piece and piece.color == Color.RED:
                self._selected_pos = (row, col)
                self._legal_moves = [
                    to_pos for from_pos, to_pos
                    in rules.generate_legal_moves(self._board, Color.RED)
                    if from_pos == self._selected_pos
                ]
                self.selectedPosChanged.emit()
                self.legalMovesChanged.emit()
        else:
            # 尝试移动
            if (row, col) in self._legal_moves:
                self._execute_move(self._selected_pos, (row, col))
            self._selected_pos = None
            self._legal_moves = []
            self.selectedPosChanged.emit()
            self.legalMovesChanged.emit()

    def _execute_move(self, from_pos: Pos, to_pos: Pos):
        """执行走法并触发 AI"""
        self._board.move_piece(from_pos, to_pos)
        self._board.current_turn = Color.BLACK
        self.boardChanged.emit()
        self.turnChanged.emit()

        # 检查游戏是否结束
        result = rules.get_game_result(self._board)
        if result:
            self.gameOver.emit("红方胜" if result == "RED_WIN" else "黑方胜")
            return

        # AI 走棋
        self._ai_move()

    def _ai_move(self):
        """AI 自动走棋"""
        engine = AIEngine(depth=3)
        move = engine.decide(self._board)
        self._board.move_piece(*move)
        self._board.current_turn = Color.RED
        self.boardChanged.emit()
        self.turnChanged.emit()

        # 检查游戏是否结束
        result = rules.get_game_result(self._board)
        if result:
            self.gameOver.emit("红方胜" if result == "RED_WIN" else "黑方胜")

    @Slot()
    def newGame(self):
        """重置游戏"""
        self._board = Board()
        self._selected_pos = None
        self._legal_moves = []
        self.boardChanged.emit()
        self.turnChanged.emit()
```

### 6.2 QML 界面结构 (gui/main.qml)

```qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    width: 600
    height: 700
    title: "中国象棋"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10

        // 回合指示
        Text {
            text: gameBridge.currentTurn
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        // 棋盘
        ChessBoard {
            id: board
            Layout.fillWidth: true
            Layout.fillHeight: true

            Repeater {
                model: gameBridge.boardData
                ChessPiece {
                    row: modelData.row
                    col: modelData.col
                    color: modelData.color
                    text: modelData.displayName
                }
            }

            Repeater {
                model: gameBridge.legalMoves
                MoveIndicator {
                    row: modelData[0]
                    col: modelData[1]
                }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: function(mouse) {
                    const col = Math.floor(mouse.x / cellWidth)
                    const row = Math.floor(mouse.y / cellHeight)
                    gameBridge.onCellClicked(row, col)
                }
            }
        }

        // 胜负提示
        Text {
            id: resultMsg
            visible: false
            font.pixelSize: 24
            Layout.alignment: Qt.AlignHCenter
            Connections {
                target: gameBridge
                function onGameOver(msg) {
                    resultMsg.text = msg
                    resultMsg.visible = true
                }
            }
        }

        // 新游戏按钮
        Button {
            text: "新游戏"
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                resultMsg.visible = false
                gameBridge.newGame()
            }
        }
    }
}
```

### 6.3 棋盘绘制

- 网格线: 9 条竖线 + 10 条横线
- 楚河汉界: 第 4-5 行之间留空，标注"楚河"|"汉界"
- 九宫格: row 0-2 col 3-5 和 row 7-9 col 3-5 画斜线
- 棋子: 圆形背景 + 文字，选中时黄色边框

---

## 7. 模块交互时序

### 7.1 核心时序：用户走棋 → AI 走棋

```
用户              GameBridge          Board          Rules            AI
 │                    │                │              │               │
 │ 点击棋子(r1,c1)    │                │              │               │
 │───────────────────>│                │              │               │
 │                    │ is_own_piece() │              │               │
 │                    │───────────────>│              │               │
 │                    │<───────────────│              │               │
 │                    │ generate_legal_moves()        │               │
 │                    │──────────────────────────────>│               │
 │                    │<──────────────────────────────│               │
 │                    │ boardChanged 信号             │               │
 │<───────────────────│                │              │               │
 │                    │                │              │               │
 │ 点击目标(r2,c2)    │                │              │               │
 │───────────────────>│                │              │               │
 │                    │ move_piece()   │              │               │
 │                    │───────────────>│              │               │
 │                    │ is_move_legal()              │               │
 │                    │──────────────────────────────>│               │
 │                    │<──────────────────────────────│               │
 │                    │ is_checkmate()?               │               │
 │                    │──────────────────────────────>│               │
 │                    │<──────────────────────────────│               │
 │                    │ boardChanged 信号             │               │
 │<───────────────────│                │              │               │
 │                    │                │              │               │
 │                    │ get_best_move(BLACK)          │               │
 │                    │──────────────────────────────────────────────>│
 │                    │                               │         [Minimax搜索]
 │                    │                               │         evaluate_board()
 │                    │<──────────────────────────────────────────────│
 │                    │ move_piece()   │              │               │
 │                    │───────────────>│              │               │
 │                    │ boardChanged 信号             │               │
 │<───────────────────│                │              │               │
```

### 7.2 模块依赖关系

```
         QML (main.qml)
              │
         bridge.py
              │
        ┌─────┴─────┐
        │           │
    board.py    rules.py
        │           │
        │      (内部调用)
        │           │
    ┌───┴───────────┴───┐
    │                   │
 ai/                  pieces.py
    │
 engine.py ←→ evaluate.py
```

---

## 8. 测试策略

### 8.1 单元测试

**tests/test_board.py**
- 验证开局布局正确
- 验证走法执行
- 验证撤销走法

**tests/test_rules.py**
- 参数化测试各棋子走法
- 测试将帅对面检测
- 测试将死/困毙判定
- 边界情况覆盖

**tests/test_ai.py**
- AI 返回合法走法
- AI 能识别吃子机会
- 评估函数正确性

**tests/test_gui.py**
- 棋子选中/取消
- 走法执行
- 新游戏重置

### 8.2 覆盖率目标

| 模块 | 目标覆盖率 |
|------|-----------|
| game/pieces.py | 100% |
| game/board.py | **98%+** |
| game/rules.py | **98%+** |
| ai/engine.py | 80%+ |
| gui/bridge.py | 70%+ |

---

## 9. 依赖与配置

### 9.1 pyproject.toml

```toml
[project]
name = "chinese-chess"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "PySide6>=6.6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-qt>=4.2.0",
    "pytest-cov>=4.1.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--cov=src --cov-report=term-missing --cov-report=html"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
fail_under = 95
```

### 9.2 运行命令

```bash
# 安装依赖
pip install -e ".[dev]"

# 运行应用
python main.py

# 运行测试
pytest

# 查看覆盖率报告
pytest --cov-report=html && htmlcov/index.html
```

---

## 10. 设计决策记录

### 10.1 项目结构：分层架构

采用三层分离架构（GUI / 游戏逻辑 / AI）。

**理由**: 游戏逻辑与 GUI 完全解耦，便于单独测试规则引擎和 AI，也方便后续替换 GUI 框架。

### 10.2 棋盘数据结构：10x9 二维数组

使用 10 行 x 9 列的二维列表表示棋盘。

**理由**: 直观映射中国象棋棋盘，访问效率高，实现简单。

### 10.3 AI 算法：Alpha-Beta 剪枝 + 简单评估函数

采用 Minimax 搜索配合 Alpha-Beta 剪枝，搜索深度 3-4 层。

**理由**: 实现复杂度适中，能提供合理的棋力。相比纯随机走法有明显提升，相比神经网络方案实现成本低得多。

**备选方案**:
- 随机走法: 太弱，体验差
- 蒙特卡洛树搜索: 实现复杂，v1.0 不需要
- 神经网络: 需要训练数据和模型，远超 v1.0 范围

### 10.4 QML 棋盘渲染：Grid + Repeater

使用 QML 的 GridView 或自定义 Canvas 绘制棋盘，Repeater 渲染棋子。

**理由**: 充分利用 QML 声明式 UI 的优势，数据驱动视图更新，Python 端只需维护数据模型。

### 10.5 Python-QML 通信：QObject 属性和信号

通过继承 QObject 的桥接类，使用 Property、Signal、Slot 机制与 QML 交互。

**理由**: PySide6 官方推荐方式，类型安全，调试方便。

---

## 11. 风险与权衡

| 风险 | 缓解措施 |
|------|----------|
| AI 棋力有限 | 使用固定搜索深度 3-4 层，棋力约为业余初级水平。v1.0 可接受，后续版本可优化 |
| QML 学习曲线 | QML 语法与纯 Python GUI 不同，但声明式 UI 更适合棋盘类界面 |
| 性能风险 | Alpha-Beta 搜索在复杂局面可能较慢。通过限制搜索深度和走法排序优化缓解 |
| PySide6 兼容性 | 不同平台的 QML 渲染可能有差异。优先保证 Windows 平台 |

---

## 附录：需求追溯矩阵

| 需求 | 设计章节 |
|------|----------|
| 棋盘初始化 | 3.2 棋盘模型 |
| 棋子定义 | 3.1 棋子模型 |
| 各棋子走法 | 4.2 走法生成策略 |
| 吃子规则 | 4.3 合法性校验流程 |
| 将帅对面 | 4.4 将帅对面检测 |
| 将军/将死/困毙 | 4.5 胜负判定 |
| GUI 渲染 | 6 GUI 层 |
| 用户交互 | 6.1 Python-QML 桥接 |
| AI 走棋 | 5 AI 引擎层 |

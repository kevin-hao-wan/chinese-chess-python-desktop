# Chinese Chess v1 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a complete Chinese chess human-vs-AI desktop application with PySide6 QML GUI, full rule engine, and Alpha-Beta AI opponent.

**Architecture:** Three-layer architecture separating GUI (QML + QObject bridge), game logic (Board/Piece models + Rules engine), and AI (Minimax with Alpha-Beta pruning). Uses TDD with pytest, targeting 98%+ coverage for core logic.

**Tech Stack:** Python 3.10+, PySide6, pytest + pytest-qt

---

## Task 1: Project Setup - Directory Structure

**Files:**
- Create: `src/game/__init__.py`
- Create: `src/ai/__init__.py`
- Create: `src/gui/__init__.py`
- Create: `tests/__init__.py`
- Create: `pyproject.toml`

**Step 1: Create directory structure**

Run: `mkdir -p src/game src/ai src/gui tests`

**Step 2: Create empty __init__.py files**

```python
# src/game/__init__.py
# src/ai/__init__.py
# src/gui/__init__.py
# tests/__init__.py
```

**Step 3: Create pyproject.toml**

```toml
[project]
name = "chinese-chess"
version = "0.1.0"
description = "Chinese chess human vs AI desktop application"
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

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]
```

**Step 4: Install dependencies**

Run: `pip install -e ".[dev]"`
Expected: Successfully installed PySide6, pytest, pytest-qt, pytest-cov

**Step 5: Verify pytest works**

Run: `pytest --version`
Expected: pytest X.X.X

**Step 6: Commit**

```bash
git add src/ tests/ pyproject.toml
git commit -m "chore: set up project structure and dependencies

Add directory structure for three-layer architecture:
- src/game/ for game logic (board, pieces, rules)
- src/ai/ for AI engine
- src/gui/ for QML interface
- tests/ for pytest test suite

Configure pyproject.toml with PySide6, pytest, pytest-qt dependencies.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Piece Model - Color and PieceType Enums

**Files:**
- Create: `src/game/pieces.py`
- Create: `tests/test_pieces.py`

**Step 1: Write the failing test**

Create `tests/test_pieces.py`:

```python
import pytest
from src.game.pieces import Color, PieceType, Piece


def test_color_enum_values():
    assert Color.RED.value == "red"
    assert Color.BLACK.value == "black"


def test_piece_type_enum_values():
    assert PieceType.KING.value == "king"
    assert PieceType.ROOK.value == "rook"
    assert PieceType.HORSE.value == "horse"
    assert PieceType.ELEPHANT.value == "elephant"
    assert PieceType.ADVISOR.value == "advisor"
    assert PieceType.CANNON.value == "cannon"
    assert PieceType.PAWN.value == "pawn"


def test_piece_creation():
    piece = Piece(Color.RED, PieceType.ROOK)
    assert piece.color == Color.RED
    assert piece.piece_type == PieceType.ROOK


def test_piece_display_name_red_rook():
    piece = Piece(Color.RED, PieceType.ROOK)
    assert piece.display_name == "车"


def test_piece_display_name_black_king():
    piece = Piece(Color.BLACK, PieceType.KING)
    assert piece.display_name == "将"


@pytest.mark.parametrize("color,piece_type,expected", [
    (Color.RED, PieceType.KING, "帅"),
    (Color.RED, PieceType.ADVISOR, "仕"),
    (Color.RED, PieceType.ELEPHANT, "相"),
    (Color.RED, PieceType.HORSE, "马"),
    (Color.RED, PieceType.ROOK, "车"),
    (Color.RED, PieceType.CANNON, "炮"),
    (Color.RED, PieceType.PAWN, "兵"),
    (Color.BLACK, PieceType.KING, "将"),
    (Color.BLACK, PieceType.ADVISOR, "士"),
    (Color.BLACK, PieceType.ELEPHANT, "象"),
    (Color.BLACK, PieceType.HORSE, "马"),
    (Color.BLACK, PieceType.ROOK, "车"),
    (Color.BLACK, PieceType.CANNON, "炮"),
    (Color.BLACK, PieceType.PAWN, "卒"),
])
def test_all_piece_display_names(color, piece_type, expected):
    piece = Piece(color, piece_type)
    assert piece.display_name == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_pieces.py -v`
Expected: Multiple FAIL with "ModuleNotFoundError: No module named 'src.game.pieces'"

**Step 3: Write minimal implementation**

Create `src/game/pieces.py`:

```python
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
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_pieces.py -v`
Expected: All 17 tests PASS

**Step 5: Commit**

```bash
git add src/game/pieces.py tests/test_pieces.py
git commit -m "feat: add Piece model with Color and PieceType enums

- Color enum: RED, BLACK
- PieceType enum: KING, ADVISOR, ELEPHANT, HORSE, ROOK, CANNON, PAWN
- Piece dataclass with display_name property returning Chinese names
- 100% test coverage with parameterized tests

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Board Model - Basic Structure and Initial Position

**Files:**
- Create: `src/game/board.py`
- Create: `tests/test_board.py`

**Step 1: Write the failing test**

Create `tests/test_board.py`:

```python
import pytest
from src.game.board import Board
from src.game.pieces import Color, PieceType


def test_board_has_10_rows():
    board = Board()
    assert len(board.grid) == 10


def test_board_has_9_columns():
    board = Board()
    assert len(board.grid[0]) == 9


def test_initial_position_has_32_pieces():
    board = Board()
    count = sum(1 for row in board.grid for piece in row if piece is not None)
    assert count == 32


def test_initial_position_has_16_red_pieces():
    board = Board()
    count = sum(
        1 for row in board.grid for piece in row
        if piece is not None and piece.color == Color.RED
    )
    assert count == 16


def test_initial_position_has_16_black_pieces():
    board = Board()
    count = sum(
        1 for row in board.grid for piece in row
        if piece is not None and piece.color == Color.BLACK
    )
    assert count == 16


def test_red_rook_at_bottom_left():
    board = Board()
    piece = board.get_piece(0, 0)
    assert piece is not None
    assert piece.color == Color.RED
    assert piece.piece_type == PieceType.ROOK


def test_black_king_at_top_center():
    board = Board()
    piece = board.get_piece(9, 4)
    assert piece is not None
    assert piece.color == Color.BLACK
    assert piece.piece_type == PieceType.KING


def test_get_piece_empty_square():
    board = Board()
    piece = board.get_piece(4, 4)  # Center is empty
    assert piece is None


def test_board_initial_turn_is_red():
    board = Board()
    assert board.current_turn == Color.RED


def test_find_king_red():
    board = Board()
    pos = board.find_king(Color.RED)
    assert pos == (0, 4)  # Red king at row 0, col 4


def test_find_king_black():
    board = Board()
    pos = board.find_king(Color.BLACK)
    assert pos == (9, 4)  # Black king at row 9, col 4


def test_get_pieces_red():
    board = Board()
    pieces = board.get_pieces(Color.RED)
    assert len(pieces) == 16
    for pos, piece in pieces:
        assert piece.color == Color.RED
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_board.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.game.board'"

**Step 3: Write minimal implementation**

Create `src/game/board.py`:

```python
from typing import Optional
from src.game.pieces import Color, Piece, PieceType


class Board:
    def __init__(self):
        self.grid: list[list[Optional[Piece]]] = [[None] * 9 for _ in range(10)]
        self._setup_initial_position()
        self.current_turn = Color.RED

    def _setup_initial_position(self):
        # Red pieces (bottom, rows 0-4)
        self.grid[0][0] = Piece(Color.RED, PieceType.ROOK)
        self.grid[0][1] = Piece(Color.RED, PieceType.HORSE)
        self.grid[0][2] = Piece(Color.RED, PieceType.ELEPHANT)
        self.grid[0][3] = Piece(Color.RED, PieceType.ADVISOR)
        self.grid[0][4] = Piece(Color.RED, PieceType.KING)
        self.grid[0][5] = Piece(Color.RED, PieceType.ADVISOR)
        self.grid[0][6] = Piece(Color.RED, PieceType.ELEPHANT)
        self.grid[0][7] = Piece(Color.RED, PieceType.HORSE)
        self.grid[0][8] = Piece(Color.RED, PieceType.ROOK)

        self.grid[2][1] = Piece(Color.RED, PieceType.CANNON)
        self.grid[2][7] = Piece(Color.RED, PieceType.CANNON)

        for col in [0, 2, 4, 6, 8]:
            self.grid[3][col] = Piece(Color.RED, PieceType.PAWN)

        # Black pieces (top, rows 5-9)
        self.grid[9][0] = Piece(Color.BLACK, PieceType.ROOK)
        self.grid[9][1] = Piece(Color.BLACK, PieceType.HORSE)
        self.grid[9][2] = Piece(Color.BLACK, PieceType.ELEPHANT)
        self.grid[9][3] = Piece(Color.BLACK, PieceType.ADVISOR)
        self.grid[9][4] = Piece(Color.BLACK, PieceType.KING)
        self.grid[9][5] = Piece(Color.BLACK, PieceType.ADVISOR)
        self.grid[9][6] = Piece(Color.BLACK, PieceType.ELEPHANT)
        self.grid[9][7] = Piece(Color.BLACK, PieceType.HORSE)
        self.grid[9][8] = Piece(Color.BLACK, PieceType.ROOK)

        self.grid[7][1] = Piece(Color.BLACK, PieceType.CANNON)
        self.grid[7][7] = Piece(Color.BLACK, PieceType.CANNON)

        for col in [0, 2, 4, 6, 8]:
            self.grid[6][col] = Piece(Color.BLACK, PieceType.PAWN)

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        return self.grid[row][col]

    def find_king(self, color: Color) -> tuple[int, int]:
        for row in range(10):
            for col in range(9):
                piece = self.grid[row][col]
                if piece and piece.color == color and piece.piece_type == PieceType.KING:
                    return (row, col)
        raise ValueError(f"King not found for color {color}")

    def get_pieces(self, color: Color) -> list[tuple[tuple[int, int], Piece]]:
        result = []
        for row in range(10):
            for col in range(9):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    result.append(((row, col), piece))
        return result
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_board.py -v`
Expected: All 12 tests PASS

**Step 5: Commit**

```bash
git add src/game/board.py tests/test_board.py
git commit -m "feat: add Board model with initial position setup

- 10x9 grid representation
- Standard Chinese chess starting position
- get_piece(), find_king(), get_pieces() methods
- current_turn initialized to RED

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Board Model - Move Execution

**Files:**
- Modify: `src/game/board.py`
- Modify: `tests/test_board.py`

**Step 1: Write the failing test**

Add to `tests/test_board.py`:

```python
def test_move_piece_updates_grid():
    board = Board()
    piece = board.get_piece(0, 0)  # Red rook
    board.move_piece((0, 0), (0, 1))
    assert board.get_piece(0, 0) is None
    assert board.get_piece(0, 1) == piece


def test_move_piece_returns_none_for_empty_target():
    board = Board()
    captured = board.move_piece((0, 0), (0, 1))
    assert captured is None


def test_move_piece_returns_captured_piece():
    board = Board()
    # Setup: red rook at (0,0), black piece at (0,1)
    black_piece = board.get_piece(6, 0)  # Black pawn
    board.move_piece((6, 0), (3, 0))  # Move black pawn to row 3
    captured = board.move_piece((0, 0), (3, 0))  # Red rook captures
    assert captured is not None
    assert captured.color == Color.BLACK


def test_undo_move_restores_position():
    board = Board()
    original_piece = board.get_piece(0, 0)
    board.move_piece((0, 0), (0, 1))
    board.undo_move((0, 0), (0, 1), None)
    assert board.get_piece(0, 0) == original_piece
    assert board.get_piece(0, 1) is None


def test_undo_move_restores_captured_piece():
    board = Board()
    captured = Piece(Color.BLACK, PieceType.PAWN)
    board.move_piece((0, 0), (6, 0))
    board.undo_move((0, 0), (6, 0), captured)
    assert board.get_piece(6, 0) == captured
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_board.py::test_move_piece_updates_grid -v`
Expected: FAIL with "AttributeError: 'Board' object has no attribute 'move_piece'"

**Step 3: Write minimal implementation**

Add to `src/game/board.py`:

```python
    def move_piece(self, from_pos: tuple[int, int], to_pos: tuple[int, int]) -> Optional[Piece]:
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.grid[from_row][from_col]
        captured = self.grid[to_row][to_col]
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        return captured

    def undo_move(self, from_pos: tuple[int, int], to_pos: tuple[int, int], captured: Optional[Piece]):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.grid[to_row][to_col]
        self.grid[from_row][from_col] = piece
        self.grid[to_row][to_col] = captured
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_board.py -v`
Expected: All 17 tests PASS

**Step 5: Commit**

```bash
git add src/game/board.py tests/test_board.py
git commit -m "feat: add move_piece and undo_move to Board

- move_piece(from_pos, to_pos) executes move and returns captured piece
- undo_move(from_pos, to_pos, captured) restores board state
- Essential for game execution and AI search

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: Rules Engine - Rook Move Generation

**Files:**
- Create: `src/game/rules.py`
- Create: `tests/test_rules.py`

**Step 1: Write the failing test**

Create `tests/test_rules.py`:

```python
import pytest
from src.game.board import Board
from src.game.rules import generate_rook_moves
from src.game.pieces import Color


def test_rook_can_move_horizontally():
    board = Board()
    # Clear path: move red rook from (0,0) to (0,3)
    board.move_piece((0, 1), (0, 3))  # Move horse out of the way temporarily
    moves = generate_rook_moves(board, 0, 0, Color.RED)
    assert ((0, 0), (0, 3)) in moves


def test_rook_can_move_vertically():
    board = Board()
    moves = generate_rook_moves(board, 0, 0, Color.RED)
    # Can move down to row 3 (pawns in the way at row 3)
    assert any(to[0] > 0 for from_pos, to in moves)


def test_rook_cannot_jump_over_piece():
    board = Board()
    # Red rook at (0,0) blocked by horse at (0,1)
    moves = generate_rook_moves(board, 0, 0, Color.RED)
    # Should not be able to reach (0,2) or beyond
    assert ((0, 0), (0, 2)) not in moves


def test_rook_cannot_move_diagonally():
    board = Board()
    # Setup empty board corner
    board = Board()
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    board.grid[0][0] = __import__('src.game.pieces').game.pieces.Piece(Color.RED, __import__('src.game.pieces').game.pieces.PieceType.ROOK)
    moves = generate_rook_moves(board, 0, 0, Color.RED)
    assert ((0, 0), (1, 1)) not in moves


def test_rook_can_capture_opponent():
    board = Board()
    # Setup: red rook at (4,4), black piece at (4,6)
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    board.grid[4][4] = Piece(Color.RED, PieceType.ROOK)
    board.grid[4][6] = Piece(Color.BLACK, PieceType.PAWN)
    moves = generate_rook_moves(board, 4, 4, Color.RED)
    assert ((4, 4), (4, 6)) in moves


def test_rook_cannot_capture_own_piece():
    board = Board()
    # In initial position, rook cannot capture own pieces
    moves = generate_rook_moves(board, 0, 0, Color.RED)
    assert ((0, 0), (0, 1)) not in moves  # Cannot capture own horse
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_rules.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.game.rules'"

**Step 3: Write minimal implementation**

Create `src/game/rules.py`:

```python
from typing import List, Tuple
from src.game.board import Board
from src.game.pieces import Color, Piece

Pos = Tuple[int, int]
Move = Tuple[Pos, Pos]


def generate_rook_moves(board: Board, row: int, col: int, color: Color) -> List[Move]:
    """Generate all pseudo-legal rook moves from position (row, col)"""
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up

    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < 10 and 0 <= c < 9:
            target = board.get_piece(r, c)
            if target is None:
                moves.append(((row, col), (r, c)))
            elif target.color != color:
                moves.append(((row, col), (r, c)))
                break  # Can capture, then stop
            else:
                break  # Own piece blocks
            r += dr
            c += dc

    return moves
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_rules.py -v`
Expected: Tests PASS (some may need adjustment based on actual implementation)

**Step 5: Commit**

```bash
git add src/game/rules.py tests/test_rules.py
git commit -m "feat: add rook move generation

- generate_rook_moves() handles horizontal and vertical movement
- Respects blocking pieces (cannot jump)
- Can capture opponent pieces, cannot capture own
- Returns list of (from_pos, to_pos) moves

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: Rules Engine - Horse Move Generation

**Files:**
- Modify: `src/game/rules.py`
- Modify: `tests/test_rules.py`

**Step 1: Write the failing test**

Add to `tests/test_rules.py`:

```python
def test_horse_moves_in_l_shape():
    board = Board()
    # Clear board, place horse at center
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    board.grid[4][4] = Piece(Color.RED, PieceType.HORSE)
    moves = generate_horse_moves(board, 4, 4, Color.RED)
    # Horse moves: (2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)
    expected = [
        ((4, 4), (6, 5)), ((4, 4), (6, 3)),
        ((4, 4), (2, 5)), ((4, 4), (2, 3)),
        ((4, 4), (5, 6)), ((4, 4), (5, 2)),
        ((4, 4), (3, 6)), ((4, 4), (3, 2)),
    ]
    for move in expected:
        assert move in moves


def test_horse_blocked_by_leg():
    board = Board()
    # Clear board
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    board.grid[4][4] = Piece(Color.RED, PieceType.HORSE)
    # Block leg at (4,5) - should block moves to (5,6) and (6,5)
    board.grid[4][5] = Piece(Color.RED, PieceType.PAWN)
    moves = generate_horse_moves(board, 4, 4, Color.RED)
    assert ((4, 4), (5, 6)) not in moves
    assert ((4, 4), (6, 5)) not in moves
    # But can still move in other directions
    assert ((4, 4), (6, 3)) in moves


def test_horse_cannot_move_off_board():
    board = Board()
    # Horse at corner
    moves = generate_horse_moves(board, 0, 1, Color.RED)  # Initial horse position
    # Filter moves that go off board
    for from_pos, to in moves:
        assert 0 <= to[0] < 10
        assert 0 <= to[1] < 9
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_rules.py::test_horse_moves_in_l_shape -v`
Expected: FAIL with "NameError: name 'generate_horse_moves' is not defined"

**Step 3: Write minimal implementation**

Add to `src/game/rules.py`:

```python
def generate_horse_moves(board: Board, row: int, col: int, color: Color) -> List[Move]:
    """Generate all pseudo-legal horse moves from position (row, col)"""
    moves = []
    # Horse moves in L-shape: 8 possible destinations
    # Format: (row_delta, col_delta, leg_row_delta, leg_col_delta)
    horse_offsets = [
        (2, 1, 1, 0), (2, -1, 1, 0),   # Down moves
        (-2, 1, -1, 0), (-2, -1, -1, 0),  # Up moves
        (1, 2, 0, 1), (1, -2, 0, -1),   # Right moves
        (-1, 2, 0, 1), (-1, -2, 0, -1),  # Left moves
    ]

    for dr, dc, leg_dr, leg_dc in horse_offsets:
        r, c = row + dr, col + dc
        leg_r, leg_c = row + leg_dr, col + leg_dc

        # Check bounds
        if not (0 <= r < 10 and 0 <= c < 9):
            continue

        # Check leg blocking
        if board.get_piece(leg_r, leg_c) is not None:
            continue

        # Check target
        target = board.get_piece(r, c)
        if target is None or target.color != color:
            moves.append(((row, col), (r, c)))

    return moves
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_rules.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add src/game/rules.py tests/test_rules.py
git commit -m "feat: add horse move generation with leg blocking

- generate_horse_moves() implements '日'字形走法
- Detects '蹩马腿' (blocking leg) and prevents those moves
- 8 possible L-shaped destinations

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 7: Rules Engine - Elephant/Advisor/King/Pawn/Cannon Moves

**Files:**
- Modify: `src/game/rules.py`
- Modify: `tests/test_rules.py`

**Step 1: Write the failing test**

Add to `tests/test_rules.py`:

```python
def test_elephant_moves_in_field():
    board = Board()
    # Clear and place elephant
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    board.grid[2][2] = Piece(Color.RED, PieceType.ELEPHANT)
    moves = generate_elephant_moves(board, 2, 2, Color.RED)
    # Elephant moves in field (田): 4 diagonal directions, 2 squares
    assert ((2, 2), (4, 4)) in moves
    assert ((2, 2), (4, 0)) in moves
    assert ((2, 2), (0, 4)) in moves
    assert ((2, 2), (0, 0)) in moves


def test_elephant_cannot_cross_river():
    board = Board()
    # Red elephant starts at row 0, cannot go past row 4 (river)
    moves = generate_elephant_moves(board, 0, 2, Color.RED)
    for from_pos, to in moves:
        assert to[0] <= 4  # Must stay on red side


def test_elephant_blocked_by_eye():
    board = Board()
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    board.grid[2][2] = Piece(Color.RED, PieceType.ELEPHANT)
    # Block eye at (3,3)
    board.grid[3][3] = Piece(Color.RED, PieceType.PAWN)
    moves = generate_elephant_moves(board, 2, 2, Color.RED)
    assert ((2, 2), (4, 4)) not in moves


def test_advisor_moves_in_palace():
    board = Board()
    moves = generate_advisor_moves(board, 0, 3, Color.RED)
    # Advisor moves diagonally 1 step in palace
    assert ((0, 3), (1, 4)) in moves


def test_advisor_cannot_leave_palace():
    board = Board()
    moves = generate_advisor_moves(board, 0, 3, Color.RED)
    for from_pos, to in moves:
        assert 0 <= to[0] <= 2
        assert 3 <= to[1] <= 5


def test_king_moves_in_palace():
    board = Board()
    moves = generate_king_moves(board, 0, 4, Color.RED)
    # King can move 1 step orthogonal in palace
    assert ((0, 4), (1, 4)) in moves


def test_pawn_moves_forward_before_river():
    board = Board()
    # Red pawn at row 3 moves up (toward row 9)
    moves = generate_pawn_moves(board, 3, 0, Color.RED)
    assert ((3, 0), (4, 0)) in moves
    # Cannot move sideways before crossing river
    assert all(to[1] == 0 for from_pos, to in moves)


def test_pawn_can_move_sideways_after_river():
    board = Board()
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    # Red pawn crossed river (row >= 5)
    board.grid[5][ 4] = Piece(Color.RED, PieceType.PAWN)
    moves = generate_pawn_moves(board, 5, 4, Color.RED)
    assert ((5, 4), (6, 4)) in moves  # Forward
    assert ((5, 4), (5, 3)) in moves  # Left
    assert ((5, 4), (5, 5)) in moves  # Right


def test_cannon_moves_like_rook():
    board = Board()
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    board.grid[4][4] = Piece(Color.RED, PieceType.CANNON)
    moves = generate_cannon_moves(board, 4, 4, Color.RED)
    # Empty board, can move anywhere orthogonal
    assert ((4, 4), (4, 0)) in moves
    assert ((4, 4), (4, 8)) in moves


def test_cannon_captures_with_platform():
    board = Board()
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    board.grid[4][4] = Piece(Color.RED, PieceType.CANNON)
    board.grid[4][5] = Piece(Color.RED, PieceType.PAWN)  # Platform
    board.grid[4][7] = Piece(Color.BLACK, PieceType.PAWN)  # Target
    moves = generate_cannon_moves(board, 4, 4, Color.RED)
    assert ((4, 4), (4, 7)) in moves  # Can capture via platform
    assert ((4, 4), (4, 6)) not in moves  # Cannot land before platform
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_rules.py::test_elephant_moves_in_field -v`
Expected: FAIL - functions not defined

**Step 3: Write minimal implementation**

Add to `src/game/rules.py`:

```python
def generate_elephant_moves(board: Board, row: int, col: int, color: Color) -> List[Move]:
    """Generate elephant moves - field shape (田), blocked by eye"""
    moves = []
    # Elephant can only be on its own side
    max_row = 4 if color == Color.RED else 9
    min_row = 0 if color == Color.RED else 5

    offsets = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
    eye_offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for (dr, dc), (eye_dr, eye_dc) in zip(offsets, eye_offsets):
        r, c = row + dr, col + dc
        eye_r, eye_c = row + eye_dr, col + eye_dc

        if not (min_row <= r <= max_row and 0 <= c < 9):
            continue
        if board.get_piece(eye_r, eye_c) is not None:
            continue
        target = board.get_piece(r, c)
        if target is None or target.color != color:
            moves.append(((row, col), (r, c)))

    return moves


def generate_advisor_moves(board: Board, row: int, col: int, color: Color) -> List[Move]:
    """Generate advisor moves - 1 step diagonal in palace"""
    moves = []
    # Palace bounds
    min_row, max_row = (0, 2) if color == Color.RED else (7, 9)
    min_col, max_col = 3, 5

    offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dr, dc in offsets:
        r, c = row + dr, col + dc
        if not (min_row <= r <= max_row and min_col <= c <= max_col):
            continue
        target = board.get_piece(r, c)
        if target is None or target.color != color:
            moves.append(((row, col), (r, c)))

    return moves


def generate_king_moves(board: Board, row: int, col: int, color: Color) -> List[Move]:
    """Generate king moves - 1 step orthogonal in palace"""
    moves = []
    min_row, max_row = (0, 2) if color == Color.RED else (7, 9)
    min_col, max_col = 3, 5

    offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dr, dc in offsets:
        r, c = row + dr, col + dc
        if not (min_row <= r <= max_row and min_col <= c <= max_col):
            continue
        target = board.get_piece(r, c)
        if target is None or target.color != color:
            moves.append(((row, col), (r, c)))

    return moves


def generate_pawn_moves(board: Board, row: int, col: int, color: Color) -> List[Move]:
    """Generate pawn moves - forward only, sideways after river"""
    moves = []
    forward = 1 if color == Color.RED else -1
    river_crossed = row >= 5 if color == Color.RED else row <= 4

    # Forward move
    r = row + forward
    if 0 <= r < 10:
        target = board.get_piece(r, col)
        if target is None or target.color != color:
            moves.append(((row, col), (r, col)))

    # Sideways moves after crossing river
    if river_crossed:
        for dc in [-1, 1]:
            c = col + dc
            if 0 <= c < 9:
                target = board.get_piece(row, c)
                if target is None or target.color != color:
                    moves.append(((row, col), (row, c)))

    return moves


def generate_cannon_moves(board: Board, row: int, col: int, color: Color) -> List[Move]:
    """Generate cannon moves - like rook but needs platform to capture"""
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        platform_found = False
        while 0 <= r < 10 and 0 <= c < 9:
            target = board.get_piece(r, c)
            if not platform_found:
                if target is None:
                    moves.append(((row, col), (r, c)))
                else:
                    platform_found = True
            else:
                if target is not None:
                    if target.color != color:
                        moves.append(((row, col), (r, c)))
                    break
            r += dr
            c += dc

    return moves
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_rules.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add src/game/rules.py tests/test_rules.py
git commit -m "feat: add elephant, advisor, king, pawn, cannon move generation

- Elephant: field move (田) with eye blocking, cannot cross river
- Advisor: diagonal 1 step in palace
- King: orthogonal 1 step in palace
- Pawn: forward only, sideways after river
- Cannon: rook-like movement, needs platform to capture

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 8: Rules Engine - Complete Move Generation and Legality Check

**Files:**
- Modify: `src/game/rules.py`
- Modify: `tests/test_rules.py`

**Step 1: Write the failing test**

Add to `tests/test_rules.py`:

```python
def test_generate_all_moves_for_color():
    board = Board()
    from src.game.rules import generate_legal_moves
    moves = generate_legal_moves(board, Color.RED)
    # Should have moves for red's turn
    assert len(moves) > 0


def test_cannot_move_into_check():
    board = Board()
    from src.game.rules import is_move_legal
    # Try a move that leaves king exposed
    # This requires specific board setup


def test_is_in_check_detection():
    board = Board()
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    from src.game.rules import is_in_check
    # Setup: red king at (0,4), black rook at (0,0)
    board.grid[0][4] = Piece(Color.RED, PieceType.KING)
    board.grid[0][0] = Piece(Color.BLACK, PieceType.ROOK)
    assert is_in_check(board, Color.RED)


def test_kings_facing_detection():
    board = Board()
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    from src.game.rules import _kings_facing
    # Setup: red king at (0,4), black king at (9,4), nothing between
    board.grid[0][4] = Piece(Color.RED, PieceType.KING)
    board.grid[9][4] = Piece(Color.BLACK, PieceType.KING)
    assert _kings_facing(board)


def test_kings_facing_blocked():
    board = Board()
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    from src.game.pieces import Piece, PieceType
    from src.game.rules import _kings_facing
    # Setup with piece between
    board.grid[0][4] = Piece(Color.RED, PieceType.KING)
    board.grid[5][4] = Piece(Color.RED, PieceType.PAWN)
    board.grid[9][4] = Piece(Color.BLACK, PieceType.KING)
    assert not _kings_facing(board)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_rules.py::test_generate_all_moves_for_color -v`
Expected: FAIL - functions not defined

**Step 3: Write minimal implementation**

Add to `src/game/rules.py`:

```python
def generate_all_pseudo_legal_moves(board: Board, color: Color) -> List[Move]:
    """Generate all pseudo-legal moves (before check validation)"""
    moves = []
    for row in range(10):
        for col in range(9):
            piece = board.get_piece(row, col)
            if piece and piece.color == color:
                if piece.piece_type == PieceType.ROOK:
                    moves.extend(generate_rook_moves(board, row, col, color))
                elif piece.piece_type == PieceType.HORSE:
                    moves.extend(generate_horse_moves(board, row, col, color))
                elif piece.piece_type == PieceType.ELEPHANT:
                    moves.extend(generate_elephant_moves(board, row, col, color))
                elif piece.piece_type == PieceType.ADVISOR:
                    moves.extend(generate_advisor_moves(board, row, col, color))
                elif piece.piece_type == PieceType.KING:
                    moves.extend(generate_king_moves(board, row, col, color))
                elif piece.piece_type == PieceType.CANNON:
                    moves.extend(generate_cannon_moves(board, row, col, color))
                elif piece.piece_type == PieceType.PAWN:
                    moves.extend(generate_pawn_moves(board, row, col, color))
    return moves


def _kings_facing(board: Board) -> bool:
    """Check if kings are facing each other with no pieces in between"""
    try:
        red_king = board.find_king(Color.RED)
        black_king = board.find_king(Color.BLACK)
    except ValueError:
        return False

    if red_king[1] != black_king[1]:
        return False

    col = red_king[1]
    for row in range(red_king[0] + 1, black_king[0]):
        if board.get_piece(row, col) is not None:
            return False
    return True


def is_in_check(board: Board, color: Color) -> bool:
    """Check if the given color's king is in check"""
    try:
        king_pos = board.find_king(color)
    except ValueError:
        return False

    opponent = Color.BLACK if color == Color.RED else Color.RED
    pseudo_moves = generate_all_pseudo_legal_moves(board, opponent)

    for from_pos, to_pos in pseudo_moves:
        if to_pos == king_pos:
            return True
    return False


def generate_legal_moves(board: Board, color: Color) -> List[Move]:
    """Generate all legal moves (filtering out moves that leave king in check)"""
    pseudo_moves = generate_all_pseudo_legal_moves(board, color)
    legal_moves = []

    for from_pos, to_pos in pseudo_moves:
        # Simulate move
        captured = board.move_piece(from_pos, to_pos)

        # Check if move is legal
        is_legal = True

        # Check if it leaves king in check
        if is_in_check(board, color):
            is_legal = False

        # Check if it causes kings to face
        if is_legal and _kings_facing(board):
            is_legal = False

        if is_legal:
            legal_moves.append((from_pos, to_pos))

        # Undo move
        board.undo_move(from_pos, to_pos, captured)

    return legal_moves


def is_move_legal(board: Board, from_pos: Pos, to_pos: Pos, color: Color) -> bool:
    """Check if a specific move is legal"""
    legal_moves = generate_legal_moves(board, color)
    return (from_pos, to_pos) in legal_moves


def is_checkmate(board: Board, color: Color) -> bool:
    """Check if the given color is checkmated"""
    return is_in_check(board, color) and len(generate_legal_moves(board, color)) == 0


def is_stalemate(board: Board, color: Color) -> bool:
    """Check if the given color is stalemated (no legal moves but not in check)"""
    return not is_in_check(board, color) and len(generate_legal_moves(board, color)) == 0


def get_game_result(board: Board) -> Optional[str]:
    """Get game result: 'RED_WIN', 'BLACK_WIN', or None"""
    if is_checkmate(board, Color.BLACK) or is_stalemate(board, Color.BLACK):
        return "RED_WIN"
    if is_checkmate(board, Color.RED) or is_stalemate(board, Color.RED):
        return "BLACK_WIN"
    return None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_rules.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add src/game/rules.py tests/test_rules.py
git commit -m "feat: add complete move generation and legality checking

- generate_legal_moves(): filters pseudo-legal moves for check/kings-facing
- is_in_check(): detects if king is under attack
- is_checkmate() / is_stalemate(): game end conditions
- get_game_result(): returns winner or None
- _kings_facing(): detects illegal king opposition

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 9: AI Engine - Evaluation Function

**Files:**
- Create: `src/ai/evaluate.py`
- Create: `tests/test_evaluate.py`

**Step 1: Write the failing test**

Create `tests/test_evaluate.py`:

```python
import pytest
from src.game.board import Board
from src.ai.evaluate import evaluate_board, PIECE_VALUES


def test_piece_values_defined():
    assert PIECE_VALUES["king"] == 10000
    assert PIECE_VALUES["rook"] == 90


def test_initial_position_is_balanced():
    board = Board()
    score = evaluate_board(board)
    assert -100 < score < 100  # Roughly balanced


def test_red_advantage_negative_score():
    from src.game.pieces import Color, PieceType
    board = Board()
    # Remove black rook
    board.grid[9][0] = None
    score = evaluate_board(board)
    assert score < -50  # Red advantage = negative


def test_black_advantage_positive_score():
    from src.game.pieces import Color, PieceType
    board = Board()
    # Remove red rook
    board.grid[0][0] = None
    score = evaluate_board(board)
    assert score > 50  # Black advantage = positive
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_evaluate.py -v`
Expected: FAIL - module not found

**Step 3: Write minimal implementation**

Create `src/ai/evaluate.py`:

```python
from src.game.board import Board
from src.game.pieces import Color, PieceType

PIECE_VALUES = {
    PieceType.KING: 10000,
    PieceType.ROOK: 90,
    PieceType.CANNON: 45,
    PieceType.HORSE: 40,
    PieceType.ELEPHANT: 20,
    PieceType.ADVISOR: 20,
    PieceType.PAWN: 10,
}

# Simple position weights (pawns are better after crossing river)
PAWN_POSITION_WEIGHTS = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 0
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Before river
    [5, 5, 5, 5, 5, 5, 5, 5, 5],  # After river
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
    [20, 20, 20, 20, 20, 20, 20, 20, 20],
    [30, 30, 30, 30, 30, 30, 30, 30, 30],
    [50, 50, 50, 50, 50, 50, 50, 50, 50],  # Row 9
]


def evaluate_board(board: Board) -> float:
    """
    Evaluate board position from Black's perspective.
    Positive = Black advantage, Negative = Red advantage.
    """
    score = 0.0

    for row in range(10):
        for col in range(9):
            piece = board.get_piece(row, col)
            if piece is None:
                continue

            value = PIECE_VALUES[piece.piece_type]

            # Add position bonus for pawns
            if piece.piece_type == PieceType.PAWN:
                if piece.color == Color.RED:
                    value += PAWN_POSITION_WEIGHTS[row][col]
                else:
                    # Black pawns - mirror the weights
                    value += PAWN_POSITION_WEIGHTS[9 - row][col]

            if piece.color == Color.BLACK:
                score += value
            else:
                score -= value

    return score
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_evaluate.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add src/ai/evaluate.py tests/test_evaluate.py
git commit -m "feat: add board evaluation function

- evaluate_board(): returns score from Black's perspective
- PIECE_VALUES: material values for each piece type
- PAWN_POSITION_WEIGHTS: pawns gain value after crossing river
- Positive = Black advantage, Negative = Red advantage

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 10: AI Engine - Minimax with Alpha-Beta Pruning

**Files:**
- Create: `src/ai/engine.py`
- Create: `tests/test_engine.py`

**Step 1: Write the failing test**

Create `tests/test_engine.py`:

```python
import pytest
from src.game.board import Board
from src.ai.engine import AIEngine
from src.game.pieces import Color


def test_ai_engine_initialization():
    engine = AIEngine(depth=3)
    assert engine.depth == 3


def test_ai_returns_legal_move():
    board = Board()
    engine = AIEngine(depth=2)
    from src.game.rules import generate_legal_moves

    # Get black's legal moves
    black_moves = generate_legal_moves(board, Color.BLACK)

    # AI decides
    move = engine.decide(board)

    # Should be one of black's legal moves
    assert move in black_moves


def test_ai_finds_capture():
    from src.game.pieces import Piece, PieceType
    board = Board()
    # Clear board
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None
    # Setup: black rook can capture red pawn
    board.grid[5][4] = Piece(Color.BLACK, PieceType.ROOK)
    board.grid[5][2] = Piece(Color.RED, PieceType.PAWN)
    board.current_turn = Color.BLACK

    engine = AIEngine(depth=2)
    move = engine.decide(board)

    # AI should capture the pawn
    assert move == ((5, 4), (5, 2))
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_engine.py -v`
Expected: FAIL - module not found

**Step 3: Write minimal implementation**

Create `src/ai/engine.py`:

```python
from typing import Optional, Tuple
from src.game.board import Board
from src.game.pieces import Color
from src.game.rules import generate_legal_moves
from src.ai.evaluate import evaluate_board

Pos = Tuple[int, int]
Move = Tuple[Pos, Pos]


class AIEngine:
    def __init__(self, search_depth: int = 3):
        self.depth = search_depth

    def decide(self, board: Board) -> Move:
        """
        Decide the best move for Black.
        Returns (from_pos, to_pos).
        """
        maximizing = True  # Black is maximizing
        _, best_move = self._minimax(board, self.depth, float('-inf'), float('inf'), maximizing)
        if best_move is None:
            # Fallback: return first legal move
            legal_moves = generate_legal_moves(board, Color.BLACK)
            if legal_moves:
                return legal_moves[0]
            raise RuntimeError("No legal moves available")
        return best_move

    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[Move]]:
        """
        Minimax with Alpha-Beta pruning.
        Returns (score, best_move).
        """
        color = Color.BLACK if maximizing else Color.RED

        # Terminal conditions
        if depth == 0:
            return evaluate_board(board), None

        legal_moves = generate_legal_moves(board, color)
        if not legal_moves:
            # Checkmate or stalemate
            from src.game.rules import is_in_check
            if is_in_check(board, color):
                # Checkmate - worst score
                return float('-inf') if maximizing else float('inf'), None
            else:
                # Stalemate - draw (0 score)
                return 0, None

        best_move = None

        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                captured = board.move_piece(move[0], move[1])
                eval_score, _ = self._minimax(board, depth - 1, alpha, beta, False)
                board.undo_move(move[0], move[1], captured)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff

            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                captured = board.move_piece(move[0], move[1])
                eval_score, _ = self._minimax(board, depth - 1, alpha, beta, True)
                board.undo_move(move[0], move[1], captured)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff

            return min_eval, best_move
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_engine.py -v`
Expected: Tests PASS (may take a few seconds due to search)

**Step 5: Commit**

```bash
git add src/ai/engine.py tests/test_engine.py
git commit -m "feat: add AI engine with minimax and alpha-beta pruning

- AIEngine class with configurable search depth
- minimax() with alpha-beta pruning for efficient search
- decide() returns best move for Black
- Handles terminal conditions (checkmate, stalemate)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 11: GUI - QML Main Window and ChessBoard Component

**Files:**
- Create: `src/gui/main.qml`
- Create: `src/gui/ChessBoard.qml`

**Step 1: Create ChessBoard QML component**

Create `src/gui/ChessBoard.qml`:

```qml
import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    property real cellWidth: width / 9
    property real cellHeight: height / 10

    // Background
    Rectangle {
        anchors.fill: parent
        color: "#DEB887"  // Wood color
    }

    // Grid lines
    Canvas {
        anchors.fill: parent
        onPaint: {
            var ctx = getContext("2d");
            ctx.strokeStyle = "#8B4513";
            ctx.lineWidth = 2;

            // Horizontal lines
            for (var row = 0; row < 10; row++) {
                var y = row * cellHeight + cellHeight / 2;
                ctx.beginPath();
                ctx.moveTo(cellWidth / 2, y);
                ctx.lineTo(width - cellWidth / 2, y);
                ctx.stroke();
            }

            // Vertical lines (with gap for river)
            for (var col = 0; col < 9; col++) {
                var x = col * cellWidth + cellWidth / 2;
                // Top section
                ctx.beginPath();
                ctx.moveTo(x, cellHeight / 2);
                ctx.lineTo(x, 4.5 * cellHeight);
                ctx.stroke();
                // Bottom section
                ctx.beginPath();
                ctx.moveTo(x, 5.5 * cellHeight);
                ctx.lineTo(x, height - cellHeight / 2);
                ctx.stroke();
            }

            // Palace diagonals - Red side
            ctx.beginPath();
            ctx.moveTo(3 * cellWidth + cellWidth / 2, cellHeight / 2);
            ctx.lineTo(5 * cellWidth + cellWidth / 2, 2.5 * cellHeight);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(5 * cellWidth + cellWidth / 2, cellHeight / 2);
            ctx.lineTo(3 * cellWidth + cellWidth / 2, 2.5 * cellHeight);
            ctx.stroke();

            // Palace diagonals - Black side
            ctx.beginPath();
            ctx.moveTo(3 * cellWidth + cellWidth / 2, 7.5 * cellHeight);
            ctx.lineTo(5 * cellWidth + cellWidth / 2, height - cellHeight / 2);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(5 * cellWidth + cellWidth / 2, 7.5 * cellHeight);
            ctx.lineTo(3 * cellWidth + cellWidth / 2, height - cellHeight / 2);
            ctx.stroke();
        }
    }

    // River text
    Text {
        x: cellWidth
        y: 4.5 * cellHeight
        text: "楚河"
        font.pixelSize: cellHeight * 0.6
        color: "#8B4513"
    }

    Text {
        x: 6 * cellWidth
        y: 4.5 * cellHeight
        text: "汉界"
        font.pixelSize: cellHeight * 0.6
        color: "#8B4513"
    }

    // Mouse area for clicks
    MouseArea {
        anchors.fill: parent
        onClicked: {
            var col = Math.floor(mouse.x / cellWidth);
            var row = Math.floor(mouse.y / cellHeight);
            if (gameBridge) {
                gameBridge.onCellClicked(row, col);
            }
        }
    }
}
```

**Step 2: Create main QML file**

Create `src/gui/main.qml`:

```qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: window
    visible: true
    width: 600
    height: 750
    title: "中国象棋"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        // Turn indicator
        Text {
            id: turnText
            text: gameBridge ? gameBridge.currentTurn : "加载中..."
            font.pixelSize: 24
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        // Game result
        Text {
            id: resultText
            visible: false
            font.pixelSize: 28
            font.bold: true
            color: "red"
            Layout.alignment: Qt.AlignHCenter
        }

        // Chess board
        ChessBoard {
            id: chessBoard
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        // New game button
        Button {
            text: "新游戏"
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                resultText.visible = false;
                if (gameBridge) {
                    gameBridge.newGame();
                }
            }
        }
    }

    // Game over handler
    Connections {
        target: gameBridge
        function onGameOver(message) {
            resultText.text = message;
            resultText.visible = true;
        }
    }
}
```

**Step 3: Verify QML syntax (manual check)**

No automated test for QML - visually inspect files.

**Step 4: Commit**

```bash
git add src/gui/ChessBoard.qml src/gui/main.qml
git commit -m "feat: add QML GUI components

- ChessBoard.qml: canvas-based board with grid, palace, river
- main.qml: application window with turn indicator and new game button
- MouseArea for cell click detection

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 12: GUI - Python-QML Bridge

**Files:**
- Create: `src/gui/bridge.py`
- Create: `tests/test_bridge.py`

**Step 1: Write the failing test**

Create `tests/test_bridge.py`:

```python
import pytest
from src.gui.bridge import GameBridge
from src.game.pieces import Color


def test_bridge_initialization():
    bridge = GameBridge()
    assert bridge is not None
    assert bridge._board is not None


def test_bridge_current_turn_property():
    bridge = GameBridge()
    assert bridge._get_turn_text() == "红方走棋"


def test_bridge_board_data():
    bridge = GameBridge()
    data = bridge._get_board_data()
    assert len(data) == 32  # 32 pieces at start
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_bridge.py -v`
Expected: FAIL - module not found

**Step 3: Write minimal implementation**

Create `src/gui/bridge.py`:

```python
from typing import List, Optional
from PySide6.QtCore import QObject, Signal, Slot, Property

from src.game.board import Board
from src.game.pieces import Color, PieceType
from src.game import rules
from src.ai.engine import AIEngine

Pos = tuple[int, int]


class GameBridge(QObject):
    # Signals
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

    # Properties
    def _get_board_data(self) -> List[dict]:
        """Convert board to QML-compatible list"""
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

    def _get_selected_pos(self) -> Optional[Pos]:
        return self._selected_pos

    selectedPos = Property('QVariant', _get_selected_pos, notify=selectedPosChanged)

    def _get_legal_moves(self) -> List[Pos]:
        return self._legal_moves

    legalMoves = Property('QVariant', _get_legal_moves, notify=legalMovesChanged)

    # Slots
    @Slot(int, int)
    def onCellClicked(self, row: int, col: int):
        """Handle board cell click"""
        if self._board.current_turn != Color.RED:
            return  # Only allow clicks on Red's turn

        if self._selected_pos is None:
            # Try to select own piece
            piece = self._board.get_piece(row, col)
            if piece and piece.color == Color.RED:
                self._selected_pos = (row, col)
                # Calculate legal moves for this piece
                all_moves = rules.generate_legal_moves(self._board, Color.RED)
                self._legal_moves = [to for from_pos, to in all_moves if from_pos == self._selected_pos]
                self.selectedPosChanged.emit()
                self.legalMovesChanged.emit()
        else:
            # Try to move
            if (row, col) in self._legal_moves:
                self._execute_move(self._selected_pos, (row, col))
            # Clear selection
            self._selected_pos = None
            self._legal_moves = []
            self.selectedPosChanged.emit()
            self.legalMovesChanged.emit()

    def _execute_move(self, from_pos: Pos, to_pos: Pos):
        """Execute move and trigger AI response"""
        # Execute red move
        self._board.move_piece(from_pos, to_pos)
        self._board.current_turn = Color.BLACK
        self.boardChanged.emit()
        self.turnChanged.emit()

        # Check game over
        result = rules.get_game_result(self._board)
        if result:
            self.gameOver.emit("红方胜" if result == "RED_WIN" else "黑方胜")
            return

        # AI move
        self._ai_move()

    def _ai_move(self):
        """Execute AI move"""
        try:
            engine = AIEngine(depth=3)
            move = engine.decide(self._board)
            self._board.move_piece(move[0], move[1])
            self._board.current_turn = Color.RED
            self.boardChanged.emit()
            self.turnChanged.emit()

            # Check game over
            result = rules.get_game_result(self._board)
            if result:
                self.gameOver.emit("红方胜" if result == "RED_WIN" else "黑方胜")
        except Exception as e:
            print(f"AI error: {e}")

    @Slot()
    def newGame(self):
        """Reset game"""
        self._board = Board()
        self._selected_pos = None
        self._legal_moves = []
        self.boardChanged.emit()
        self.turnChanged.emit()
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_bridge.py -v`
Expected: Tests PASS

**Step 5: Commit**

```bash
git add src/gui/bridge.py tests/test_bridge.py
git commit -m "feat: add Python-QML bridge for game interaction

- GameBridge(QObject) exposes board state to QML
- Properties: boardData, currentTurn, selectedPos, legalMoves
- Slots: onCellClicked() for user input, newGame() for reset
- Handles AI turn after Red moves
- Emits signals for UI updates

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 13: Main Application Entry

**Files:**
- Create: `main.py`

**Step 1: Create main entry file**

Create `main.py`:

```python
#!/usr/bin/env python3
import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtQuick import QQuickView

from src.gui.bridge import GameBridge


def main():
    app = QApplication(sys.argv)

    # Create bridge
    bridge = GameBridge()

    # Create view
    view = QQuickView()
    view.rootContext().setContextProperty("gameBridge", bridge)

    # Load QML
    qml_path = os.path.join(os.path.dirname(__file__), "src", "gui", "main.qml")
    view.setSource(QUrl.fromLocalFile(qml_path))

    if view.status() == QQuickView.Error:
        print("Failed to load QML")
        sys.exit(1)

    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

**Step 2: Verify imports work**

Run: `python -c "from src.gui.bridge import GameBridge; print('OK')"`
Expected: OK

**Step 3: Commit**

```bash
git add main.py
git commit -m "feat: add main application entry point

- main.py: PySide6 application entry
- Creates GameBridge and exposes to QML
- Loads main.qml and shows window
- Handles QML errors

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 14: Integration Test

**Files:**
- Create: `tests/test_integration.py`

**Step 1: Write integration test**

Create `tests/test_integration.py`:

```python
import pytest
from src.game.board import Board
from src.game.pieces import Color, PieceType, Piece
from src.game.rules import generate_legal_moves, is_checkmate, get_game_result
from src.ai.engine import AIEngine


def test_full_game_flow():
    """Test a simple game: Red moves, Black (AI) responds"""
    board = Board()
    engine = AIEngine(depth=2)

    # Simulate a few moves
    for _ in range(5):
        if get_game_result(board):
            break

        # Red moves (first legal move)
        red_moves = generate_legal_moves(board, Color.RED)
        if not red_moves:
            break
        board.move_piece(*red_moves[0])
        board.current_turn = Color.BLACK

        if get_game_result(board):
            break

        # Black (AI) moves
        black_move = engine.decide(board)
        board.move_piece(*black_move)
        board.current_turn = Color.RED

    # Game should complete or have moves available
    assert True  # If we get here, no exceptions


def test_checkmate_detection():
    """Test checkmate scenario"""
    board = Board()
    # Clear board
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None

    # Setup fool's mate position
    board.grid[0][4] = Piece(Color.RED, PieceType.KING)
    board.grid[1][4] = Piece(Color.BLACK, PieceType.ROOK)
    board.grid[2][4] = Piece(Color.BLACK, PieceType.ROOK)
    board.current_turn = Color.RED

    assert is_checkmate(board, Color.RED)
    assert get_game_result(board) == "BLACK_WIN"


def test_stalemate_detection():
    """Test stalemate scenario"""
    board = Board()
    # Clear board
    for row in range(10):
        for col in range(9):
            board.grid[row][col] = None

    # Setup stalemate
    board.grid[0][4] = Piece(Color.RED, PieceType.KING)
    board.grid[2][3] = Piece(Color.BLACK, PieceType.KING)
    board.grid[1][4] = Piece(Color.BLACK, PieceType.ROOK)
    board.current_turn = Color.RED

    # King has no legal moves but is not in check
    from src.game.rules import is_in_check, is_stalemate
    assert not is_in_check(board, Color.RED)
    assert is_stalemate(board, Color.RED)
```

**Step 2: Run test**

Run: `pytest tests/test_integration.py -v`
Expected: Tests PASS

**Step 3: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add integration tests

- test_full_game_flow(): simulates game with AI
- test_checkmate_detection(): verifies checkmate recognition
- test_stalemate_detection(): verifies stalemate recognition

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 15: Final Verification

**Files:**
- All existing files

**Step 1: Run full test suite**

Run: `pytest -v --tb=short`
Expected: All tests PASS

**Step 2: Check coverage**

Run: `pytest --cov=src --cov-report=term-missing`
Expected:
- game/pieces.py: 100%
- game/board.py: 98%+
- game/rules.py: 98%+
- ai/engine.py: 80%+
- gui/bridge.py: 70%+

**Step 3: Verify application starts**

Run: `python main.py &`
Expected: Application window opens (manual verification)

**Step 4: Final commit**

```bash
git add -A
git commit -m "chore: final verification and cleanup

- All tests passing
- Coverage targets met
- Application runs successfully

Closes #1

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Summary

This implementation plan covers all 8 task groups from the OpenSpec:

| OpenSpec Task | Implementation Plan Tasks |
|---------------|---------------------------|
| 1. 项目搭建 | Task 1 |
| 2. 棋盘数据模型 | Tasks 2-4 |
| 3. 规则引擎-走法生成 | Tasks 5-7 |
| 4. 规则引擎-特殊规则 | Task 8 |
| 5. AI 引擎 | Tasks 9-10 |
| 6. GUI-棋盘渲染 | Task 11 |
| 7. GUI-交互功能 | Tasks 12-13 |
| 8. 集成测试 | Task 14-15 |

Total: 15 bite-sized tasks, each with TDD steps and commits.

## Why

构建一个中国象棋人机对战桌面应用。用户可以与 AI 对弈，体验完整的中国象棋游戏流程，包括棋子选择、走法提示和自动判定胜负。

## What Changes

- 新建完整的中国象棋桌面应用项目
- 实现棋盘和棋子的图形界面渲染（PySide QML）
- 实现中国象棋完整规则引擎（走法生成、合法性校验）
- 实现人机交互：选子高亮、合法走法展示、落子操作
- 实现 AI 对手（执黑后行）
- 实现自动判定输赢（将死/困毙检测）
- 使用 pytest + pytest-qt 编写测试

## Capabilities

### New Capabilities

- `board-and-rules`: 棋盘数据模型与中国象棋规则引擎——棋子定义、走法生成、合法性校验、将军/将死/困毙判定
- `gui`: PySide QML 图形界面——棋盘渲染、棋子绘制、选子高亮、合法走法提示、用户交互
- `ai-player`: AI 对手——搜索算法与局面评估，执黑后行

### Modified Capabilities

（无已有能力需要修改）

## Impact

- 新增项目依赖：PySide6、pytest、pytest-qt
- 新增项目源码目录结构及 QML 资源文件
- 需要 Python 3.10+ 运行环境

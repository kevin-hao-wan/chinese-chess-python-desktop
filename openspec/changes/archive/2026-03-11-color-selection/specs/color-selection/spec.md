## ADDED Requirements

### Requirement: 执棋方选择
系统 SHALL 在游戏开始前提供执棋方选择功能，允许玩家选择执红先行或执黑后行。

#### Scenario: 显示选择界面
- **WHEN** 用户点击"新游戏"按钮
- **THEN** 系统显示选择对话框，包含"执红先行"和"执黑后行"两个选项

#### Scenario: 选择执红先行
- **WHEN** 用户选择"执红先行"并确认
- **THEN** 系统开始新游戏，玩家执红，AI 执黑，玩家先走

#### Scenario: 选择执黑后行
- **WHEN** 用户选择"执黑后行"并确认
- **THEN** 系统开始新游戏，玩家执黑，AI 执红，AI 先走

### Requirement: 默认选择
系统 SHALL 默认选择"执红先行"。

#### Scenario: 打开选择界面时的默认状态
- **WHEN** 用户打开执棋方选择界面
- **THEN** "执红先行"选项默认被选中

### Requirement: AI 先手走棋
当玩家选择执黑后行时，系统 SHALL 在游戏开始后立即触发 AI 走第一步。

#### Scenario: AI 先手
- **GIVEN** 玩家选择执黑后行
- **WHEN** 游戏开始
- **THEN** AI 执红自动执行第一步走法
- **AND** 显示"红方思考中"提示直到 AI 完成走棋

### Requirement: 记住上次选择
系统 SHALL 记住玩家上次的执棋方选择，下次打开选择界面时自动选中。

#### Scenario: 记住玩家偏好
- **GIVEN** 玩家上次选择"执黑后行"
- **WHEN** 用户再次打开选择界面
- **THEN** "执黑后行"选项默认被选中

## MODIFIED Requirements

### Requirement: 新游戏功能
系统 SHALL 提供开始新游戏的功能。

#### Scenario: 重新开始
- **WHEN** 用户点击"新游戏"按钮
- **THEN** 显示执棋方选择对话框
- **AND** 玩家选择后棋盘重置为初始布局并开始新游戏

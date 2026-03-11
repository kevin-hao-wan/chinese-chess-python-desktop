## ADDED Requirements

### Requirement: AI 执黑后行
AI SHALL 执黑方棋子，在红方（人类）走完一步后自动走棋。

#### Scenario: AI 自动走棋
- **WHEN** 红方完成一步走法
- **THEN** AI 自动选择一步合法走法并执行，然后轮到红方

### Requirement: AI 走法合法
AI 的每一步走法 MUST 是当前局面下的合法走法。

#### Scenario: AI 走法合规
- **WHEN** AI 执行走法
- **THEN** 该走法符合中国象棋所有规则

### Requirement: AI 具有基本棋力
AI SHALL 使用搜索算法（如 Alpha-Beta 剪枝）选择走法，而非随机选择。AI MUST 在合理时间内（3 秒以内）完成走法计算。

#### Scenario: AI 选择有策略的走法
- **WHEN** 局面中有明显的吃子机会
- **THEN** AI 能识别并利用该机会

#### Scenario: AI 响应时间
- **WHEN** AI 计算走法
- **THEN** 在 3 秒内完成计算并执行走法

### Requirement: AI 应对将军
AI SHALL 在被将军时选择解除将军的走法。

#### Scenario: AI 解除将军
- **WHEN** AI 方被将军
- **THEN** AI 选择一步能解除将军的合法走法

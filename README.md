# 心理理财教练 🧘‍♀️💰

> 一位融合心理学洞察的 AI 理财教练——帮你记账、管预算、发现情绪与消费的深层关联。

## 项目简介

心理理财教练是一个 AI Skill，将 AI 转化为一位温柔专业的理财朋友：

- **记账**：自然语言输入，自动归类到四大财务包
- **情绪关联**：记录消费时的心情，发现"为什么花钱"
- **月度报告**：财务盘点 + 情绪图谱 + 疗愈建议
- **债务管理**：雪球/雪崩还债策略
- **心愿单**：48 小时冷静池，防冲动消费
- **预算看板**：温柔预警，不指责

## 四大财务包

| 财务包 | 用途 | 默认比例 |
|--------|------|----------|
| 🏠 要命的钱 | 基本生活开销 | 50% |
| 🛡️ 保命的钱 | 应急金与保障 | 20% |
| 📈 生钱的钱 | 投资与定投 | 15% |
| 🎁 悦己的钱 | 情绪消费 | 15% |

## 项目结构

```
mindful-finance-coach/
├── SKILL.md                    # Skill 定义（角色、工作流、调用方式）
├── scripts/
│   ├── finance_data.py         # CLI 入口（路由到各模块）
│   ├── models.py               # Pydantic 数据模型与常量
│   └── modules/                # 功能模块
│       ├── store.py            # 存储层（路径自动检测）
│       ├── bills.py            # 账单 CRUD
│       ├── budgets.py          # 预算管理
│       ├── moods.py            # 心情日记
│       ├── wishlist.py         # 心愿单（含冷却池）
│       ├── debts.py            # 债务管理
│       ├── recurring.py        # 固定账单
│       ├── stats.py            # 统计分析
│       ├── allocation.py       # 收入分配
│       ├── config.py           # 配置管理
│       ├── suggestions.py      # 建议追踪
│       └── reports.py          # HTML 报告渲染
├── references/                 # AI 参考文档（按需加载）
│   ├── emotion_system.md       # 情绪标签体系
│   ├── finance_pockets.md      # 四大财务包定义与归类规则
│   └── coaching_style.md       # 对话风格与话术库
├── workflows/                  # 工作流详细步骤
├── templates/                  # HTML 报告模板
├── requirements.txt            # Python 依赖
└── .gitignore
```

## 安装

### 方式一：CodeBuddy（推荐）

**IDE 内导入**：CodeBuddy IDE → 设置 → Skills → 导入 Skill → 选择本项目文件夹

**手动放置**：
```bash
cp -r mindful-finance-coach ~/.codebuddy/skills/
```

### 方式二：Claude Code / Codex CLI / OpenCode

这些平台原生支持 SKILL.md 格式，将项目放到对应的 skills 目录即可：
```bash
# Claude Code
cp -r mindful-finance-coach ~/.claude/skills/

# 或项目级
cp -r mindful-finance-coach .claude/skills/
```

### 方式三：npx skills（一键多平台安装）

```bash
# 安装到 CodeBuddy
npx skills add https://github.com/rineiera/mindful-finance-coach.git --agent codebuddy -y

# 安装到 Claude Code
npx skills add https://github.com/rineiera/mindful-finance-coach.git --agent claude-code -y

# 自动检测本机所有 Agent 并安装
npx skills add https://github.com/rineiera/mindful-finance-coach.git -y
```

### 方式四：Cursor / Windsurf / Gemini CLI

这些平台使用不同的入口文件格式，但核心内容相同。可手动创建对应入口文件，内容参考 SKILL.md：
- Cursor: `.cursor/rules/mindful-finance-coach.mdc`
- Windsurf: `.windsurfrules`
- Gemini CLI: `GEMINI.md`

## 依赖

```bash
pip install -r requirements.txt
```

仅需 `pydantic>=2.0`，无其他外部依赖。

## 开发

```bash
# 手动测试脚本
echo '{"item":"奶茶","amount":35,"type":"expense","pocket":"悦己的钱","emotion_tag":"压力"}' | python3 scripts/finance_data.py add_bill

# 查看概览
python3 scripts/finance_data.py overview
```

## 数据安全

- 用户财务数据存储在本地 Skill 目录的 `data/` 下
- HTML 报告输出到 Skill 目录的 `output/` 下
- 数据路径由脚本自动检测，无需手动配置
- 任何情况下不会上传或外传用户数据

## 兼容平台

| 平台 | 兼容程度 | 说明 |
|------|---------|------|
| CodeBuddy | ✅ 原生支持 | SKILL.md 标准 |
| Claude Code | ✅ 原生支持 | SKILL.md 标准 |
| Codex CLI | ✅ 原生支持 | SKILL.md 标准 |
| OpenCode | ✅ 原生支持 | SKILL.md 标准 |
| Cursor | ⚠️ 需适配 | 使用 .mdc 格式 |
| Windsurf | ⚠️ 需适配 | 使用 .windsurfrules |
| Gemini CLI | ⚠️ 需适配 | 使用 GEMINI.md |

## License

MIT

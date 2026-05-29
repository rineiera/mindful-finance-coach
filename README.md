# 心理理财教练 🧘‍♀️💰

> 一位融合心理学洞察的 AI 理财教练——帮你记账、管预算、发现情绪与消费的深层关联。

## 项目简介

心理理财教练是一个 [CodeBuddy Skill](https://www.codebuddy.ai/docs)，将 AI 转化为一位温柔专业的理财朋友：

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
│   └── finance_data.py         # 数据管理脚本（CRUD + 统计）
├── references/
│   ├── emotion_system.md       # 情绪标签体系
│   ├── finance_pockets.md      # 四大财务包定义与归类规则
│   └── coaching_style.md       # 对话风格与话术库
├── templates/                  # HTML 报告模板
├── output/                     # 生成的 HTML 报告（运行时）
├── tests/                      # 测试
├── requirements.txt            # Python 依赖
└── .gitignore
```

## 安装

将本项目安装为 CodeBuddy Skill，数据会自动存储在 `~/.codebuddy/skills/mindful-finance-coach/`。

## 依赖

```bash
pip install -r requirements.txt
```

## 开发

```bash
# 运行测试
python3 -m pytest tests/ -v

# 手动测试脚本
echo '{"item":"奶茶","amount":35,"type":"expense","pocket":"悦己的钱","emotion_tag":"压力"}' | python3 scripts/finance_data.py add_bill
```

## 数据安全

- 用户财务数据存储在本地 `~/.codebuddy/skills/mindful-finance-coach/data/`
- HTML 报告输出到 `~/.codebuddy/skills/mindful-finance-coach/output/`
- 任何情况下不会上传或外传用户数据

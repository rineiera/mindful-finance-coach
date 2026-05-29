# 工作流5：查询模式

当用户查看最近账单时：

1. 运行 `get_bills` 获取数据
2. 将 HTML 写入 `output/` 目录，用 `preview_url` 预览，包含账单 ID（方便后续修正）和情绪标签

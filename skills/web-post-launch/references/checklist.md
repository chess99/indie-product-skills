# 上线检查清单

按代表性页面类型抽样；已发现模板问题时再扩大检查。每项记录 URL、时间、观察、影响及复测结果，简单站点可直接在对话中交付。

| 对象 | 有效检查 | 常见误判 |
|---|---|---|
| 可用性 | GET 的最终状态、正文、重定向、移动端关键操作 | HEAD 200 也可能返回空页或软 404 |
| robots | 实际规则、目标 crawler、HTTP 状态 | 缺少 robots.txt 不代表禁止抓取；robots 不能可靠保密 |
| 索引指令 | HTML robots 与 X-Robots-Tag、canonical、环境配置 | robots 阻挡后爬虫可能看不到 noindex |
| sitemap | XML 内容、命名空间、index 子文件、canonical URL | `text/xml` 也可有效；HTML fallback 的 200 无效 |
| 内容 | 首屏与主内容可见、标题与目的清晰、内链可达 | 模型可生成内容不等于有搜索价值 |
| 多语言 | 实际等价页面、双向 hreflang、canonical 一致 | 无多语言页面时无需添加 |
| 结构化数据 | 类型仍受支持、字段真实、与可见内容一致 | 合法 schema.org 类型不保证 Google 富结果资格 |
| 转化 | 从入口走到成功状态；事件去重、参数、同意状态 | 只确认脚本存在不能证明统计成功 |
| 性能 | 关键页加载与交互，区分 lab/field | 单次分数不是整站用户体验 |
| AI 可发现性 | 正文可访问、事实可溯源、官方产品信息一致 | `llms.txt`、切块或特殊 schema 不能保证引用 |

Google 当前对生成式搜索的建议见 [官方指南](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)，搜索功能变化见 [更新日志](https://developers.google.com/search/updates)。不要把特定实验或其他引擎的表现外推为通用规则。

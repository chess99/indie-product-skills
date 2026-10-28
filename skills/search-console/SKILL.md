---
name: search-console
description: 验证站点所有权、提交 sitemap、检查 Google Search Console、Bing 或百度的抓取索引状态，处理 IndexNow 与搜索提交问题。根据目标市场和现有账号选择引擎。
metadata:
  version: 2.0.0
---

# 搜索引擎提交与索引诊断

复用已知站点、市场、账号连接和授权。先查看已有 property、验证方式、sitemap 和状态，避免重复创建或重复提交。使用可用连接器或授权浏览器完成工作；仅对登录、验证码或无法取得的权限请求用户介入。

## 提交前

- 确定需覆盖的域名、协议和子域。Google Domain property 使用 DNS 验证；URL-prefix 适合限定前缀或无 DNS 权限的情况，复用有效验证。
- 对 sitemap 发出 GET，确认是可解析 XML，识别 `urlset` 与 `sitemapindex`。按命名空间解析，遍历有界的子 sitemap；子 sitemap 地址不能当页面 URL 推送。
- 检查目标 URL 所属站点、canonical、访问状态、索引指令和必要的内部链接。去重但保留路径与查询参数大小写。
- 凭据使用连接器或本地受保护配置；不要求把 token 粘贴到聊天、写入报告、命令历史或公开仓库。

## 选择引擎与动作

| 需要 | 动作 |
|---|---|
| Google | 验证适当 property，提交有效 sitemap，必要时检查重点 URL |
| Bing | 复用账号与 property；适合时使用既有 Google 验证导入；提交 sitemap |
| IndexNow | 仅对支持的引擎与真实新增/更新/删除 URL 通知，验证 host/key/keyLocation |
| 百度 | 用户面向该搜索市场或明确指定时处理；核对当前账号权限、接口和剩余配额 |

具体平台步骤、权限和回退见 [引擎参考](references/submit-engines.md)。配额和功能从当前接口/官方文档读取，不写死每日请求数。不把普通网页提交到仅支持特定内容类型的 Google Indexing API。

提交、验证文件或 DNS 修改均在用户已授权的目标范围内进行；单纯要求“检查索引”不授权新增账户或更改 DNS。完成可读检查与待提交内容后，再处理尚缺的授权。响应不明时先查状态，再决定重试。

## 验证与交付

以平台响应区分“已接收 / sitemap 已处理 / 已抓取 / 已索引 / 待处理 / 失败”。GSC URL Inspection API 查看索引状态，不能代替 UI 的请求索引功能。`site:` 搜索只作辅助观察，不能给出准确索引数量。

交付平台、property、提交对象、时间、响应及尚未解决的问题。索引速度和结果由引擎决定；不承诺 24–48 小时收录，也不为等待收录重复推送全站。

# 引擎操作参考

## Google

1. 查看现有 property 和权限；按实际范围选择 Domain 或 URL-prefix。
2. 需要验证文件时使用平台提供的原始内容，GET 检查正文，排除站点 fallback。DNS 验证记录保留以维持所有权。
3. 在已授权 property 下提交 sitemap；查询读取/处理状态。
4. 重点 URL 用 URL Inspection 查看 canonical、抓取与索引结果；确需请求索引时使用支持该动作的界面，并服从当前配额。

[Search Console](https://search.google.com/search-console/) · [sitemap 指南](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview) · [URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect) · [Indexing API 适用范围](https://developers.google.com/search/apis/indexing-api/v3/using-api)

## Bing / IndexNow

查看 [Bing Webmaster Tools](https://www.bing.com/webmasters/) 的现有站点，复用验证或在明确授权下导入 Google property。提交 sitemap 与 IndexNow 通知按需要分别使用。

IndexNow 请求的 host、key、keyLocation 与 URL 必须匹配。批量大小、状态码和 key 文件验证按 [协议](https://www.indexnow.org/documentation) 核对。只通知真正变化的页面；不把“接收”表述成“已收录”。遇到限流遵守响应，遇到状态不明先查记录。

## 百度

先看 [搜索资源平台](https://ziyuan.baidu.com/) 当前提供的验证方式、链接提交能力、接口地址与账号额度。不要预设每个账号都有主动推送权限。无接口权限时继续完成站点公开检查，并明确账号侧待办。

推送前解析 sitemap index 与子文件，排除外域、重复项和非页面地址，按实际额度分批。凭据交给连接器或本地配置读取，日志需脱敏；报告只写接受数、剩余额度和错误类型。配额用尽或权限错误时停止重试。

## 诊断顺序

先确认访问与索引资格，再查发现路径、canonical 与平台状态，最后讨论内容价值及竞争。sitemap 成功、爬虫访问、索引和排名分别记录。无账号数据时只报告公开可验证现象，不能断言引擎已经索引或惩罚站点。

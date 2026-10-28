# Link Ops Policy Boundary

执行前以 Google Search Central 当前官方 spam policies / link qualification 文档为准；如果任务涉及高风险做法，应联网重新核查最新规则。

官方入口：

- https://developers.google.com/search/docs/essentials/spam-policies
- https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links

## 默认不推荐

- 自动程序批量创建为了 SEO 的链接；
- 低质量目录/书签站批量提交；
- 关键词锚文本评论、论坛签名；
- PBN/站群；
- 规模化互链；
- 付费 followed links；
- 模板 footer、widget 中广泛分发的关键词链接；
- 为链接而生产的大量低质量 guest posts。

## 可以存在但要正确标记

广告、赞助、affiliate、付费 placement 是正常商业活动，但不应伪装成自然编辑推荐。需要时使用 `rel="sponsored"` 或 `nofollow` 等合适标记，并以最新官方说明为准。

## nofollow / ugc

不要把 `nofollow` / `ugc` 简化成“完全没价值”。这类链接仍可能带来发现、真实 referral、品牌提及和后续自然引用。Link Ops 关注业务和分发价值，不追求“100% dofollow”。

## 外部状态变更

默认无需授权即可：

- 搜索公开信息；
- 分析竞品和来源页面；
- 处理用户提供的导出；
- 在用户要求保存时建立私有 prospect 数据；
- 评分、排序；
- 寻找公开联系人；
- 生成但不发送 outreach 草稿。

必须用户明确授权才可以：

- 发邮件、DM、联系表单；
- 发帖、评论、提交目录；
- 注册外部服务；
- 建立互链；
- 购买链接/赞助；
- 修改用户网站之外的任何外部状态。

即使获得授权，也不要执行明显违反搜索垃圾政策或平台规则的自动化 link spam。

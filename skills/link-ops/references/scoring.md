# Link Opportunity Scoring

评分用于 shortlist 排序，不是 Google 排名公式。

## 维度

每项 0–5 分：

| field | weight | 5 分含义 |
|---|---:|---|
| `topic_relevance` | 25 | 来源页面、读者和目标页任务高度相关 |
| `editorial_selectivity` | 20 | 需要作者/编辑真实选择，不能自助批量制造 |
| `page_quality` | 15 | 页面有实质内容、可发现、维护正常 |
| `click_likelihood` | 15 | 用户在上下文中有明确点击动机 |
| `unique_domain` | 10 | 新的独立高相关 referring domain |
| `placement_quality` | 10 | 正文自然上下文，而非 footer/sidebar/comment spam |
| `durability` | 5 | 页面和链接预计长期存活 |

基础分为加权 0–100。

## Spam Risk

`spam_risk` 为 0–5 的整数等级，但用于扣分和硬门槛：

- 0：正常编辑/生态链接；
- 1：轻微不确定；
- 2：低质量目录或弱编辑选择，扣 10；
- 3：明显 SEO 交易味、杂站或规模化模板，扣 25；
- 4：高风险 link scheme，扣 50，并默认 reject；
- 5：明确自动垃圾链接/站群/隐藏或操纵性链接，扣 75，并 reject。

最终：

```text
opportunity_score = max(0, weighted_base - risk_penalty)
```

优先级：

- `>=75`：priority；
- `55–74.9`：consider；
- `<55`：low；
- `spam_risk >=4`：reject，无论基础分。

## 一票否决信号

以下通常直接把 `spam_risk` 评到 4–5：

- 自动批量评论/论坛签名；
- 专门按 followed link 售卖的 link insertion 网络；
- 大规模互链计划；
- 低质量目录批量提交；
- 关键词丰富的模板 footer/widget 链接；
- PBN/站群；
- 付费但要求传递排名信用、拒绝 sponsored/nofollow；
- 与主题无关、内容农场式“什么都发”的 guest-post 库存。

第三方 DR/DA/AS 可以记录在 `authority_metric`，但不直接进入评分公式。

# Link Ops Workspace Schema

Workspace 是项目私有运行数据，不应提交到 `indie-product-skills` 公共仓库。

初始化后：

```text
run/
├─ brief.json
├─ prospects.csv
├─ channels.csv
└─ outreach.csv
```

原始 Ahrefs / Semrush / Bing / 其他导出可放在 workspace 外或自行建立 `imports/`，保持私有。

## brief.json

- `schema_version`
- `site`
- `name`
- `goal`
- `target_pages[]`
- `competitors[]`
- `constraints[]`

## prospects.csv

去重键为来源 URL、目标 URL、竞品的组合。URL 仅归一化协议/主机大小写并去掉 fragment，路径和查询大小写保留。`source_domain` 是主机名，不等同于可注册根域；跨子域的独立来源统计需要额外核实。行动队列按来源页/联系人再合并，避免同页涉及多个竞品导致重复联系。

身份和来源：

- `source_domain`
- `source_url`
- `target_url`
- `competitor`
- `anchor_text`
- `link_category`
- `page_title`
- `page_language`
- `import_source`
- `authority_metric`
- `estimated_traffic`

评分：

- `topic_relevance`
- `editorial_selectivity`
- `page_quality`
- `click_likelihood`
- `unique_domain`
- `placement_quality`
- `durability`
- `spam_risk`
- `opportunity_score`
- `score_status`
- `recommended_action`

执行：

- `contact_name`
- `contact_email`
- `status`
- `notes`

建议 `status`：`new / researched / queued / drafted / contacted / won / lost / rejected / monitor`。

## channels.csv

这是跨 campaign 最有价值的长期资产：

- `channel`
- `category`
- `url`
- `topic`
- `submission_type`
- `relationship`
- `status`
- `last_verified`
- `quality_notes`
- `wins`
- `failures`

不要只记“能不能发”，要记历史成功率、主题适配和最后验证时间。

## outreach.csv

- `source_url`
- `contact_name`
- `contact_email`
- `status`
- `subject`
- `last_action`
- `next_action`
- `notes`

不要在公共仓库提交个人邮箱、私有联系人或 outreach 历史。

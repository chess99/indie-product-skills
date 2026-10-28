---
name: link-ops
description: 为网站研究竞品外链、发现和筛选相关引用渠道、维护 prospect 数据、准备外联及复盘 referral 效果。用于外链运营、referring-domain gap 和渠道积累；外部提交与联系按用户授权执行。
metadata:
  version: 2.0.0
---

# 外链与引用运营

目标是获得相关受众、可信引用和可复用的渠道关系。复用目标站、关键页面、市场、已有关系和数据；无需为了开始而要求付费 backlink 导出。没有可链接价值时先改进目标页，避免为数量铺链接。

## 选择发现路径

- **竞品反查**：有导出时比较多个直接竞品的独立来源页面，找正文引用、资源页、教程、集成和失效替代。第三方数据是发现入口，shortlist 需要打开来源页核实。
- **原因驱动**：没有导出时，从目标用户的问题、官方生态、教程/资源、社区和可引用资产找机会。来源模式见 [发现参考](references/playbook.md)。
- **已有资产**：优先查真实集成、合作、被提及未链接、旧内容与关系；陌生渠道的分数不必高于真实可达关系。

每个强候选说明来源页的具体上下文、它为何需要这条引用、目标页提供什么额外价值、可执行动作及风险。查到未链接或某个 gap 只是当前观察；未发现客户端标签、`site:` 未返回页面等都不能证明功能不存在。

## 筛选与排队

核实页面存活、相关性、真实编辑选择、链接位置、读者点击理由及成本。来源可以覆盖多个竞品，但行动应按页面/联系人合并，避免重复外联。按 [评分参考](references/scoring.md) 需要时量化；小批候选可直接给有证据的排序。

DR/DA、dofollow 比例和链接条数不作为目标本身。渠道规则与 Google 链接政策见 [政策参考](references/policy.md)；自动评论、PBN、低质量批量目录、操纵性互链和付费 followed links 不进入推荐队列。

## 数据与草稿

只有需要长期维护或用户要求保存时才初始化私有 workspace。从本技能目录运行：

```bash
python scripts/link_ops.py init --output <path> --site https://example.com
python scripts/link_ops.py import --run <path> --input <export.csv> --source ahrefs --competitor competitor.com
python scripts/link_ops.py score --run <path>
python scripts/link_ops.py validate --run <path>
```

字段说明见 [数据结构](references/schema.md)。导出用于保留不同链接关系；执行前另行合并行动，分数不自动授权联系。

草稿用真实上下文和具体价值，不制造夸张缺口、精确匹配锚文本或虚假关系。对外提交、联系、注册、评论和购买须有明确授权；已有授权无需再确认。响应不明先查状态，禁止盲目重复发送。

## 复盘

按任务成熟度跟踪：机会到有效引用的转化、链接存活、独立相关来源、referral 到注册/付费、渠道投入与可复用性。排名变化只作相关观察，不能直接归因于新增链接。

复盘节奏匹配实际信号，常规链接/排名可按周，存活可按月；不默认每天扫全量。需要持续检查时使用可用的 `marketing-loops`，仅在用户要求后安排自动化；状态未变不重复提醒。

默认交付优先队列、依据、可执行草稿和下一步。私有联系人、导出与 campaign 数据不得进入公开仓库。

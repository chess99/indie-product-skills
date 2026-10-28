# webmaster-skills

面向独立开发者的产品发现、建站与增长技能集合，支持 Codex 和 Claude Code。按当前问题选择工作流，由 Agent 完成研究、判断、修复和验证。

## 安装

```bash
/plugin install webmaster-skills --marketplace chess99/webmaster-skills
```

仓库已包含选用的营销技能，无需再安装同名 marketing-skills 插件。不同客户端的插件安装方式以其当前说明为准；兼容发现目录均指向 `skills/`。

## 从当前问题开始

| 你要解决的问题 | 技能 | 交付 |
|---|---|---|
| 接下来做什么产品 | [find-product-opportunities](skills/find-product-opportunities/SKILL.md) | 有证据的 1–3 个候选与主推荐、待验证或 NO-GO |
| 新站刚上线，哪里最值得检查 | [post-launch](skills/post-launch/SKILL.md) | 关键访问/转化、索引、测量与专项修复结果 |
| 网站慢、交互卡、布局跳动 | [performance](skills/performance/SKILL.md) | 与症状匹配的测量、原因、修改和复测 |
| 下一批搜索页面做什么、为什么掉流量 | [seo-research](skills/seo-research/SKILL.md) | 有证据的页面/修复优先队列 |
| 验证站点、提交 sitemap、检查索引 | [search-console](skills/search-console/SKILL.md) | 指定引擎的验证/提交/处理状态 |
| 找相关引用、外链渠道和 referral | [link-ops](skills/link-ops/SKILL.md) | 来源核实、机会队列、草稿与复盘 |
| 哪些营销投入带来结果 | [attribution](skills/attribution/SKILL.md) | 数据口径、归因限制和验证方案 |
| 找匹配的潜客及可验证的切入点 | [prospecting](skills/prospecting/SKILL.md) | 目标客户研究、需求信号和优先队列 |
| 定期复盘已运行的营销渠道 | [marketing-loops](skills/marketing-loops/SKILL.md) | 检查条件、状态去重、停止条件及适当节奏 |

流程可从任何一项开始。上线检查按风险推进；机会发现按证据收敛。已有明确产品时直接做该产品的验证或增长工作。

## 营销工具箱

选用 [Corey Haines 的 marketingskills](https://github.com/coreyhaines31/marketingskills)，当前快照 **2.13.9**，固定提交与文件摘要见 [上游锁定记录](vendor/marketing.lock.json)。按需加载上游内容；已记录的兼容补丁修复失效的本地引用。

| 任务 | 技能 |
|---|---|
| 搜索与网站结构 | seo-audit、ai-seo、programmatic-seo、site-architecture、schema、aso |
| 转化与留存 | cro、signup、onboarding、popups、paywalls、churn-prevention |
| 内容与创意 | content-strategy、copywriting、copy-editing、emails、social、image、video |
| 广告与测量 | ads、ad-creative、analytics、attribution、ab-testing |
| 分发与增长 | referrals、free-tools、co-marketing、community-marketing、directory-submissions、marketing-loops |
| 研究与销售 | customer-research、competitor-profiling、competitors、prospecting、cold-email、revops、sales-enablement、lead-magnets |
| 定位与策略 | product-marketing、marketing-ideas、marketing-psychology、launch、pricing |

已有产品信息直接复用；需要建立长期定位文档时使用 `product-marketing`。上游方法中的比例、平台统计和案例结论需结合当前来源与实际业务判断。第三方工具、账号、付费数据和其他未包含的技能按需使用。

## 工作方式

- **按决策投入研究**：优先验证最可能改变选择的假设，不为凑候选或固定流程消耗时间。
- **保留证据边界**：公开页面、趋势、工具估算、真实业务数据分别标注；主动查替代解释。
- **先验证真实结果**：可访问与可转化、事件可测、性能瓶颈、提交状态各自验证。`llms.txt`、统一结构化数据和 PageSpeed 90 分均不作为通用上线门槛。
- **授权范围内执行**：已授权工作直接完成。研究本身不授权发信、发布、注册或付费；自动化仅在用户要求持续执行时设置。
- **默认对话交付**：按需保存研究与运营数据，私有文件不进入插件仓库。

## 维护

```text
skills/                 本地技能与上游技能链接
vendor/marketing/       选用的上游原文与许可证
vendor/marketing.lock.json  固定来源、选用列表与 SHA-256
scripts/                仓库校验工具
tests/                  确定性回归测试
docs/                   维护方法与升级依据
```

`.claude/skills`、`.agents/skills`、`.catpaw/skills` 指向 `skills/`，`CLAUDE.md` 指向 `AGENTS.md`。

- [维护与验证](docs/maintenance.md)
- [2026-10 方法与上游审查](docs/review-2026-10.md)
- [仓库约定](AGENTS.md)

本地实现与测试使用 Python 3.11+ 标准库。官方格式校验工具单独安装，模型行为评测与结构测试分别记录。

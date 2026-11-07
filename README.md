# indie-product-skills

面向独立开发者的软件产品机会发现、验证、发布与增长技能集合，支持 Codex 和 Claude Code。按当前问题选择工作流，由 Agent 完成研究、判断、执行和验证。

产品可以是 Web、移动应用、桌面软件、扩展、CLI 或 API。先确定用户任务与商业机会，再选择合适的交付形态；通用产品方法跨形态复用，平台专项按需使用。

## 安装

Claude Code：

```bash
claude plugin install indie-product-skills --marketplace chess99/indie-product-skills
```

其他客户端按其当前插件安装方式使用 [GitHub 仓库](https://github.com/chess99/indie-product-skills)。仓库已包含选用的营销技能，无需再安装同名 marketing-skills 插件；兼容发现目录均指向 `skills/`。

从 `webmaster-skills` 升级时，插件身份与两个 Web 技能名称有变化，见 [3.0 迁移说明](docs/migration-3.0.md)。本地检出文件夹可以保留原名。

## 从当前问题开始

| 阶段 | 你要解决的问题 | 入口与交付 |
|---|---|---|
| 发现机会 | 接下来做什么产品 | [find-product-opportunities](skills/find-product-opportunities/SKILL.md)：有证据的 1–3 个候选与主推荐、待验证或 NO-GO |
| 验证需求 | 已有想法是否值得投入 | [validate-product-idea](skills/validate-product-idea/SKILL.md)：关键假设、证据与反证、最小判别实验和投入建议 |
| 确定首版 | 选择产品形态、裁剪 MVP | [validate-product-idea](skills/validate-product-idea/SKILL.md)：按任务与约束选择形态，确定首版闭环与暂缓范围 |
| 定位与定价 | 为谁服务、如何表达价值、如何收费 | [product-marketing](skills/product-marketing/SKILL.md)、[pricing](skills/pricing/SKILL.md) |
| 发布与分发 | 产品如何发布，第一批用户从哪里来 | [launch](skills/launch/SKILL.md)、[marketing-ideas](skills/marketing-ideas/SKILL.md)、[prospecting](skills/prospecting/SKILL.md) |
| 获客与转化 | 选择渠道、优化内容与购买路径 | [内容与获客技能](docs/skill-catalog.md#内容与获客)、[转化与留存技能](docs/skill-catalog.md#转化与留存) |
| 留存与复盘 | 用户是否获得价值，下一轮投入什么 | [onboarding](skills/onboarding/SKILL.md)、[churn-prevention](skills/churn-prevention/SKILL.md)、[attribution](skills/attribution/SKILL.md)、[marketing-loops](skills/marketing-loops/SKILL.md) |

流程可从任何一项开始。已有明确产品时直接处理该产品的问题；无需重新寻找机会或先填完整简报。全部技能及适用范围见 [技能目录](docs/skill-catalog.md)。

## 平台专项

| 对象 | 任务 | 技能 |
|---|---|---|
| 网站 / Web 应用 | 上线后检查访问、转化、索引与测量 | [web-post-launch](skills/web-post-launch/SKILL.md) |
| 网站 / Web 应用 | 诊断加载、交互与布局性能 | [web-performance](skills/web-performance/SKILL.md) |
| 网站 / 产品官网 | 搜索机会、抓取索引与结构化数据 | [seo-research](skills/seo-research/SKILL.md)、[seo-audit](skills/seo-audit/SKILL.md)、[search-console](skills/search-console/SKILL.md)、[schema](skills/schema/SKILL.md) |
| App Store / Google Play | 商店页面的发现与下载转化 | [aso](skills/aso/SKILL.md) |

移动应用、桌面软件和开发者工具也可使用用户研究、定位、定价、内容与分发方法；渠道、计费和测量需适配实际产品。上游部分方法以 SaaS 为例，不将注册、订阅、营销网站或搜索收录当作所有产品的前置条件。

本仓库重点覆盖产品判断与增长。框架编码、原生打包、签名、商店审核、自动更新等工程任务使用对应环境的能力；目前未提供这些任务的完整专项工作流。

## 工作方式

- **按决策投入研究**：优先验证最可能改变选择的假设，不为凑候选或固定流程消耗时间。
- **保留证据边界**：公开页面、趋势、工具估算、真实业务数据分别标注；主动查替代解释。
- **验证适用的结果**：需求承诺、核心任务完成、获客、购买与留存分别取证；网站检查不能代替原生应用的安装与运行验证。
- **授权范围内执行**：已授权工作直接完成。研究本身不授权发信、发布、注册或付费；自动化仅在用户要求持续执行时设置。
- **默认对话交付**：按需保存研究与运营数据，私有文件不进入插件仓库。

## 来源与维护

营销能力选用 [Corey Haines 的 marketingskills](https://github.com/coreyhaines31/marketingskills)，当前快照 **2.13.9**。固定提交、文件摘要与兼容补丁记录在 [上游锁定记录](vendor/marketing.lock.json)。平台统计、接口规则和案例结论按任务核对当前来源；第三方账号、工具和未包含技能按需使用。

```text
skills/                    扁平的技能安装与发现入口
vendor/marketing/          选用的上游原文与许可证
vendor/marketing.lock.json 固定来源、选用列表与 SHA-256
patches/                   上游兼容补丁
scripts/                   仓库校验工具
tests/                     确定性回归测试
docs/                      技能导航、迁移与维护说明
```

`.claude/skills`、`.agents/skills`、`.catpaw/skills` 指向 `skills/`，`CLAUDE.md` 指向 `AGENTS.md`。目录不按产品形态或生命周期拆分，跨阶段技能通过文档导航复用。

- [维护与验证](docs/maintenance.md)
- [2026-10 方法与上游审查](docs/review-2026-10.md)
- [仓库约定](AGENTS.md)

本地实现与测试使用 Python 3.11+ 标准库。官方格式校验工具单独安装，模型行为评测与结构测试分别记录。

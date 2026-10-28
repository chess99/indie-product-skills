# 独立开发者机会识别模式库

> 用外部信号生成可验证的产品假设。模式用于发现；证据门槛见 [证据规范](evidence.md)，排序见 [评分规范](scoring.md)。

## 核心原则

需要形成候选时使用下面的推理链：

`Signal → Change → Job → Friction → Payer → Wedge → Proof → Counterfactual`

优先寻找 **delta**：成本、能力、规则、价格、供给、默认值、分发、用户情绪或买家身份发生了什么变化。

进入验证的强候选应能回答：

1. **What changed?** 为什么以前不值得做、现在可能值得做？
2. **Whose job got harder/easier?** 谁的什么任务因此变化？
3. **Where is the new friction/value?** 新增的成本、风险、复杂度或价值落在哪里？
4. **Who owns the consequence?** 谁真正承担预算、事故、审核、时间或机会成本？
5. **What is the smallest wedge?** 独立开发者先拿哪一小块？
6. **What visible proof can we ship?** 能不能做成一份报告、矩阵、检查结果、导出包或明确 before/after？
7. **What else could explain the signal?** 如果另一个解释成立，这个机会是否消失？

下面的 48 个模式按 8 个家族组织。按当前信号选择相应家族，候选过度集中时再查不同方向；无需遍历全部模式。

快速定位：A 成熟产品变化；B 开源采用；C 技术能力/成本；D 工作流阻力；E 搜索与语言；F 买家与经济性；G 分发；H 市场结构。

---

# A. Incumbent disruption：大产品制造的逃离窗口

## A1. 涨价 / 免费层缩水

**Trigger**：成熟产品涨价、限额收紧、免费层取消，社区出现 bill shock、`too expensive`、`free alternative`。

**Opportunity transform**：不要自动做“更便宜的完整克隆”。先检查能否只承接最敏感的一段：低频用户、个人版、一次性任务、本地版、成本监控、用量优化或迁移。

**Ask**：用户想逃的是价格、计费不透明，还是整个工作流？哪些功能他们实际上从不用？

**False positive**：骂价格的人可能本来就不是付费用户；低价竞争也可能把自己锁进低毛利。

## A2. 产品关停 / Sunset

**Trigger**：产品宣布停止服务、停止维护、进入只读模式或明确 EOL。

**Opportunity transform**：优先寻找 migration、importer、data rescue、compatibility bridge、replacement guide，再决定是否做长期替代品。

**Ask**：哪类数据/工作流最难搬？用户迁移截止日期是什么？

**False positive**：关停产品可能本来就没有足够市场；“难迁移”只产生一次性服务收入。

## A3. 功能移除 / 体验降级

**Trigger**：厂商静默或公开砍掉一项受欢迎功能、降低配额、改变默认行为。

**Opportunity transform**：检查这个功能能否成为独立窄产品，或是否创造 compatibility / restore / monitoring / alerting 机会。

**Ask**：用户是真的依赖该功能完成任务，还是只对变化本身不爽？

**False positive**：厂商删除功能可能因为使用率极低；社区声量可能来自少数重度用户。

## A4. 收购 / 路线图不确定

**Trigger**：独立工具被大公司收购、团队加入另一家公司、产品未来承诺含糊。

**Opportunity transform**：寻找 Plan B：迁移、兼容、独立替代、数据导出、vendor-neutral layer。

**Ask**：用户害怕的是价格、关停、平台绑定、数据归属还是创新停止？

**False positive**：被收购后产品可能反而获得更多资源；恐慌不等于迁移行为。

## A5. 平台政策 / 审核 / API 规则变化

**Trigger**：App Store、Google Play、浏览器、社交平台、云厂商、支付平台改变审核/API/限制规则。

**Opportunity transform**：寻找 compliance checker、policy diff、submission assistant、fallback channel、multi-platform abstraction、risk monitor。

**Ask**：谁每天需要把新规则翻译成行动？错误一次的代价有多大？

**False positive**：政策变化可能只是短期新闻，且平台可直接提供官方工具。

## A6. 平台 / OS / 地区缺口

**Trigger**：头部产品只服务 iOS/macOS/Web/美国等一侧，另一侧用户持续搜索、抱怨或使用非官方替代品。

**Opportunity transform**：cross-platform clone、companion、sync bridge、region-localized version、missing-client。

**Ask**：缺平台本身是否足够，还是需要把价格、支付、本地服务、离线能力一起重做？

**False positive**：缺平台可能是目标用户太少或平台技术限制导致。

---

# B. Open-source commoditization：开源把价值推向相邻层

## B1. OSS 快速增长但缺成熟商业层

**Trigger**：GitHub stars/forks/adoption 快速增长，能力被大量开发者验证。

**Opportunity transform**：不要默认“hosted clone”。先扫 hosted、managed、team、support、policy、audit、cost、upgrade、backup、vertical workflow 八层。

**Ask**：采用之后最无聊、最反复、最需要负责人承担责任的工作是什么？

**False positive**：OSS 用户可能强烈拒绝付费；没有商业版也可能正是因为没有预算。

## B2. 插件 / Skill / Node 生态爆发

**Trigger**：某平台周围快速出现大量插件、skills、nodes、templates、LoRA、integrations。

**Opportunity transform**：marketplace、discovery、quality ranking、compatibility testing、dependency management、provenance、billing。

**Ask**：选择、安装、升级、信任哪一个环节最痛？

**False positive**：生态可能生命周期极短，官方市场也可能很快补齐。

## B3. 开发者工具开始进入团队

**Trigger**：个人工具在企业/团队使用增加，搜索和讨论开始出现 `team`、`workspace`、`admin`、`SSO`、`policy`、`budget`。

**Opportunity transform**：team defaults、admin console、seat governance、shared config、approval、reporting。

**Ask**：谁开始从“用户”变成“负责人”？

**False positive**：上游项目可能快速推出企业版，把外部商业层压死。

## B4. Local-first / Self-hosted 项目群同时上涨

**Trigger**：多个不同品类的 self-hosted/local-first/offline 项目同时升温。

**Opportunity transform**：不要只做另一个 self-hosted clone；检查 migration、backup、portable export、update management、health check、hosted-but-owned、deployment appliance。

**Ask**：用户为什么想“拥有”软件：隐私、成本、离线、合规、可控、避免锁定？

**False positive**：自托管热情可能来自爱好者而非买家，支持成本也可能极高。

## B5. OSS 功能强，但运营体验差

**Trigger**：用户认可核心能力，却反复抱怨安装、升级、依赖、配置、监控、恢复、兼容。

**Opportunity transform**：packaging、one-click setup、verified distribution、managed update、support bundle、smoke-test matrix。

**Ask**：用户是在抱怨“没有能力”，还是“把能力可靠跑起来很麻烦”？

**False positive**：文档修好后机会可能消失；用户未必愿意为 convenience 付钱。

## B6. 扩展能力带来安全 / 来源不明风险

**Trigger**：插件、skills、agents、browser extensions 开始执行动作或访问敏感数据。

**Opportunity transform**：scanner、permission manifest、provenance、allowlist、sandbox、policy pack、signed report。

**Ask**：采用者需要什么证据才能批准它进入生产？

**False positive**：安全预算通常集中在更大组织，小团队可能直接忽略风险。

---

# C. Technology unlock：新能力让旧需求重新算账

## C1. 单位成本突然下降

**Trigger**：模型、存储、带宽、GPU、OCR、语音、视频、支付或数据获取成本显著下降。

**Opportunity transform**：回头检查过去因 COGS 太高失败的产品，尤其是高频、低客单 consumer workflow。

**Ask**：成本下降后，哪类任务第一次能以独立开发者可承受的毛利交付？

**False positive**：成本下降会同时降低进入门槛，竞争也可能瞬间增加。

## C2. 能力跨过“够用阈值”

**Trigger**：某技术不再只是 demo，开始达到真实工作流所需的准确率、延迟、稳定性或上下文长度。

**Opportunity transform**：寻找可由软件可靠承担一段工作的窄任务，用真实输入验证质量与错误成本。

**Ask**：错误率与失误成本是否低到买家愿意使用结果？

**False positive**：榜单能力不等于真实场景；必须用目标任务验证。

## C3. 本地 / 端侧运行成为可能

**Trigger**：模型量化、小模型、WebGPU、手机芯片等让原本云端能力能在设备本地运行。

**Opportunity transform**：privacy-first、offline、zero-retention、low-latency、fixed-cost versions。

**Ask**：哪些用户过去因为隐私、延迟、联网或持续 API 成本没有采用？

**False positive**：端侧体验、安装包体积、功耗和设备碎片化可能抵消优势。

## C4. 新 API / 协议 / 标准开放

**Trigger**：平台开放新的 API、MCP/协议/数据格式开始标准化、原来封闭的数据可编程访问。

**Opportunity transform**：integration、orchestration、migration、observability、testing、vertical adapter。

**Ask**：标准化后，哪一段原来需要定制集成的工作突然可以产品化？

**False positive**：新协议可能很快被大平台原生吸收；生态尚未稳定。

## C5. 软件从“辅助”变成“代执行”

**Trigger**：AI/automation 开始代表用户操作浏览器、API、支付、代码仓库、内部系统。

**Opportunity transform**：approval、permissions、budget cap、audit trail、rollback、simulation、human-in-the-loop。

**Ask**：一旦软件能行动，谁承担错误动作的后果？

**False positive**：团队可能尚未真的大规模授权执行，只是在讨论概念。

## C6. 新硬件 / 传感器 / 平台能力普及

**Trigger**：新设备能力、传感器、浏览器 API、操作系统能力进入大众硬件。

**Opportunity transform**：重新检查过去需要专用硬件、人工测量或昂贵设备的任务。

**Ask**：能否只用用户已经拥有的设备完成一个原来昂贵的 job？

**False positive**：硬件覆盖率、权限、耗电、精度和平台审核可能限制市场。

---

# D. Workflow friction：把隐形税变成产品

## D1. 同一抱怨在多个独立用户中复现

**Trigger**：不同来源的人描述相似失败、浪费或 workaround。

**Opportunity transform**：先给 pain 分类：missing capability / UX / config / integration / price / trust / migration / verification / docs/defaults，再决定产品形态。

**Ask**：他们具体做了什么 workaround？发生频率和代价是多少？

**False positive**：高声量不代表高频，也可能只是一个事件集中引发讨论。

## D2. Setup / 配置税

**Trigger**：产品能力很强，但用户卡在安装、环境、权限、依赖、配置文件、接线步骤。

**Opportunity transform**：wizard、config generator、validator、preflight check、golden template、setup report。

**Ask**：setup 是一次性的，还是每个项目/团队都会重复发生？

**False positive**：一次性 setup 可能只适合内容或服务，不适合订阅产品。

## D3. Verification 成为新瓶颈

**Trigger**：生成/自动化速度提高后，人类花更多时间检查输出、代码、数据、内容、安装结果。

**Opportunity transform**：test harness、diff reviewer、smoke test、evidence report、acceptance gate、benchmark for real task。

**Ask**：用户怎样知道“完成了”而不是“看起来完成了”？

**False positive**：验证成本可能被现有 CI/QA 工具充分覆盖。

## D4. 隐藏成本 / Bill shock

**Trigger**：token、API、seat、云资源、后台任务、connector 等成本难预测，用户在账单后才发现。

**Opportunity transform**：preflight estimator、budget guard、cost attribution、usage receipt、anomaly alert、what-if calculator。

**Ask**：谁批准预算？能否在花钱前而不是花钱后给出决策？

**False positive**：供应商可能很快原生提供 cost dashboard；低客单用户不愿再付一层工具费。

## D5. 隐藏数据流 / 权限边界

**Trigger**：用户不知道产品读取什么、上传什么、保存什么、共享到哪里。

**Opportunity transform**：local proxy、network trace、permission report、data map、redaction、policy checker。

**Ask**：谁需要对“数据去了哪里”签字负责？

**False positive**：网络拦截技术可能脆弱；安全场景需要高可信度。

## D6. Export / Backup / Portability 脆弱

**Trigger**：用户担心服务宕机、离线场景、平台锁定，或已有真实数据丢失/无法导出案例。

**Opportunity transform**：backup、portable packet、offline mirror、restore test、migration readiness report。

**Ask**：只有“想拥有副本”，还是存在 deadline、现场约束、审计或业务连续性？

**False positive**：备份是保险型产品，痛感低时付费意愿弱。

---

# E. Search & language shift：搜索语言暴露需求状态

## E1. Generic category term breakout

**Trigger**：不是品牌名，而是 `X software`、`X tool`、`X platform` 等品类词突然增长。

**Opportunity transform**：说明用户可能处于类别探索期；优先做 buyer segmentation、comparison、narrow wedge，而不是完整 suite。

**Ask**：查询背后是谁、要完成什么任务？

**False positive**：新闻、课程、招聘和导航也会带来 generic term spike。

## E2. `free / cheaper / alternative to X` 上涨

**Trigger**：带明确替代意图的查询增长。

**Opportunity transform**：price resentment、free-tier collapse、migration demand；可做替代品、迁移器、比较页、一次性版本、本地版。

**Ask**：用户是在找“免费”，还是在拒绝某种订阅心理模型？

**False positive**：免费搜索人群可能永远不付钱。

## E3. `self-hosted / local / offline / privacy` 词簇上涨

**Trigger**：多个品类同时出现所有权型查询。

**Opportunity transform**：把它视为结构性 sentiment，再找有真实成本/风险的垂直任务，而不是泛做“隐私版”。

**Ask**：所有权诉求和哪一个可量化结果绑定？

**False positive**：爱好者/极客偏好可能被高估。

## E4. `how to / setup / configure / connect` 查询增长

**Trigger**：用户已经接受某个能力，开始搜索如何落地。

**Opportunity transform**：implementation wall；可做 setup assistant、config generator、managed workflow、template、validator。

**Ask**：用户是在学习，还是已经有必须完成的任务？

**False positive**：高搜索量可能更适合 SEO 内容而不是软件。

## E5. `X vs Y / compare / pricing` 查询增长

**Trigger**：用户开始在多个成熟选项之间做选择。

**Opportunity transform**：comparison engine、calculator、neutral benchmark、switching assistant、buyer guide。

**Ask**：比较中哪个变量最难获得可信答案：价格、隐私、性能、迁移、兼容？

**False positive**：比较页可能是一次性内容流量，难形成留存。

## E6. 新名词从零出现 + 多源同步

**Trigger**：新概念/品牌从零起飞，同时在 GitHub、社区、产品发布或官方资料出现。

**Opportunity transform**：优先做 picks-and-shovels：comparison、directory、migration、templates、monitoring，而不是立刻押注长期产品名。

**Ask**：这是新类别，还是一次 launch spike？

**False positive**：AI/开发者生态项目名生命周期极短。

---

# F. Buyer & economics：找到真正承担后果的人

## F1. 明确现有支出

**Trigger**：用户公开当前月费、服务费、人工费、广告费、云账单或工具栈成本。

**Opportunity transform**：围绕替代成本定价；优先找能减少已有支出而不是创造新预算的产品。

**Ask**：你的产品替代哪一行预算？

**False positive**：一个人的高支出不能自动外推市场规模。

## F2. 高 ROI 的手工/工具链工作流

**Trigger**：案例显示一组工具或人工流程能直接带来明显 revenue/pipeline/cost saving。

**Opportunity transform**：整合、自动化、measurement、verticalization；卖“结果的可靠复现”而不是功能集合。

**Ask**：ROI 哪一段最脆弱、最依赖手工、最难复制？

**False positive**：成功案例可能依赖 founder 技能，无法产品化。

## F3. 付费服务正在完成重复软件任务

**Trigger**：顾问、agency、freelancer、VA 持续为相似输入输出收费。

**Opportunity transform**：service-to-software、report generator、workflow assistant、semi-automated productized service。

**Ask**：服务价值来自知识判断还是机械执行？

**False positive**：如果核心是关系、定制判断或责任承担，纯软件替代率会很低。

## F4. 定价心理模型错配

**Trigger**：用户并非嫌绝对价格高，而是强烈拒绝“桌面工具订阅”“低频工具订阅”“永久服务 lifetime”等模型。

**Opportunity transform**：one-time + paid upgrades、credits、usage-based、annual maintenance、bring-your-own-key。

**Ask**：用户认为自己在“拥有工具”还是“持续购买服务”？

**False positive**：社区评论对定价常比真实购买行为更激烈。

## F5. 高错误成本 / 责任人出现

**Trigger**：错误会造成罚款、数据泄露、生产事故、昂贵返工、客户流失或职业风险。

**Opportunity transform**：preflight check、approval gate、audit evidence、monitoring、insurance-like tooling。

**Ask**：谁会因为出错被问责？能否卖给这个人而不是终端使用者？

**False positive**：高责任行业可能同时带来高合规和销售成本，不适合 indie。

## F6. 新能力进入 budget / security / workforce / payments 语言

**Trigger**：一个原来只有开发者讨论的概念开始出现在预算、安全、支付、人力、采购、治理语境。

**Opportunity transform**：第二波软件：governance、spend control、permission、workflow ownership、reporting。

**Ask**：哪一个新的组织角色开始关心它？

**False positive**：机构语言可能只是咨询/媒体叙事，尚未进入实际采购。

---

# G. Distribution leverage：产品机会要自带第一条路

## G1. 痛点人群集中在可触达社区

**Trigger**：问题反复出现在明确 subreddit、GitHub issues、forum、Discord、行业社区。

**Opportunity transform**：优先考虑能用原问题直接演示的窄产品；验证成本低。

**Ask**：能否在不买广告的情况下，把 demo 放到 20 个目标用户眼前？

**False positive**：社区允许讨论不代表允许推广，且声量可能不代表市场规模。

## G2. 生态市场 / 集成目录提供现成分发

**Trigger**：Shopify、Slack、Notion、Figma、Chrome、VS Code、AI agent 等生态有 marketplace 或 integration discovery。

**Opportunity transform**：平台补充、workflow extension、vertical adapter。

**Ask**：平台内搜索意图是否和你的产品价值直接一致？

**False positive**：平台抽成、审核、政策和原生功能竞争可能很强。

## G3. 用户搜索“问题”而不是“产品”

**Trigger**：FAQ、`how to`、错误码、专业术语、计算问题持续带来高意图流量。

**Opportunity transform**：answer-first funnel：免费答案/计算器/检查器 → 更深工具或付费工作流。

**Ask**：回答之后自然的下一步动作是什么？

**False positive**：问题流量可能只需要一次答案，没有产品留存。

## G4. Migration intent 本身就是分发

**Trigger**：`move from X to Y`、`export X`、`X alternative`、`X import` 查询或社区讨论增加。

**Opportunity transform**：migration assistant、converter、compatibility map、done-for-you import。

**Ask**：迁移完成后还能留下什么持续价值？

**False positive**：一次性需求 LTV 低，需要强 SEO/口碑或后续产品承接。

## G5. 产品输出天然可分享 / 可引用

**Trigger**：结果能生成报告、badge、benchmark、矩阵、地图、审计记录、公开 profile。

**Opportunity transform**：把输出物本身变成分发单元；每个用户使用都可能产生曝光。

**Ask**：用户为什么愿意转发这份结果？

**False positive**：为了传播而公开敏感数据会损害产品价值。

## G6. 垂直买家有专门目录/协会/工作流入口

**Trigger**：细分行业的客户集中在特定协会、论坛、软件生态、监管目录或采购渠道。

**Opportunity transform**：vertical SaaS / vertical utility；用行业语言包装通用能力。

**Ask**：是否能列出前 100 个潜在客户，而不是只描述 TAM？

**False positive**：垂直市场可能太小或销售周期太长。

---

# H. Market structure & wedge：独立开发者在哪一层更容易赢

## H1. 热门能力周围的“无聊层”

**Trigger**：新技术人人都在展示核心能力，但上线后必需的运营工作无人愿意做。

**Opportunity transform**：billing、logs、testing、backup、permissions、policy、support、deployment、migration。

**Ask**：demo 之后第一件让团队后悔采用的脏活是什么？

**False positive**：无聊层可能被基础平台快速原生化。

## H2. Generic capability 垂直化

**Trigger**：通用 AI/automation 能力成熟，但某行业仍依赖特定术语、数据格式、审批或交付物。

**Opportunity transform**：vertical workflow + domain constraints + domain output。

**Ask**：除了换 prompt 和 logo，还有什么行业特有 workflow/责任？

**False positive**：没有真实 domain moat 的 vertical wrapper 很容易被通用产品吃掉。

## H3. 多工具拼接形成稳定工作流

**Trigger**：用户反复用 A→B→C→Spreadsheet→Email 解决同一任务。

**Opportunity transform**：workflow product、orchestrator、single-purpose pipeline、data handoff layer。

**Ask**：哪个 handoff 最容易坏、最耗人工？

**False positive**：Zapier/Make/n8n 可能已足够，用户只是不愿配置。

## H4. 公共/碎片数据被手工整理

**Trigger**：价值不在独家数据，而在把公开记录、目录、文档、列表变得可搜索、可比较、可计算。

**Opportunity transform**：searchable database、vertical directory、calculator、monitor、change tracker。

**Ask**：整理后用户能做出什么原来很难的决定？

**False positive**：数据许可、更新频率和 SEO 复制风险可能很高。

## H5. 旧品类因新技术/新情绪复活

**Trigger**：老项目、旧软件、离线/本地/原生/简单工具重新获得讨论或搜索。

**Opportunity transform**：re-bundle old job with new UX/cost/privacy/platform assumptions，而不是照搬旧产品。

**Ask**：复活的是怀旧，还是一个没被现代产品满足的 job？

**False positive**：怀旧讨论通常转化率低。

## H6. 一个 2 小时可交付物能代表核心价值

**Trigger**：机会可以被压缩成单输入→单输出，例如安装矩阵、成本报告、迁移检查、离线包、权限清单。

**Opportunity transform**：优先以 report/checker/calculator/CLI/concierge artifact 验证，再决定是否建设完整 SaaS。

**Ask**：48 小时内能不能让真实用户拿到结果并问“能帮我也跑一次吗？”

**False positive**：demo 易做不代表市场大；它只是降低验证成本。

---

# 模式组合：单一 detector 通常不够

可以组合多个模式来解释候选，但模式数量不增加证据权重。

典型组合：

### 1. Migration window

`A1/A2/A3 + E2/E4 + G4`

厂商变化 + 替代/迁移搜索 + 明确迁移入口 → importer / converter / compatibility / replacement wedge。

### 2. OSS commercialization without thin hosting

`B1 + B3/B5 + F5/F6`

OSS adoption + 团队责任 + 高错误成本 → policy / audit / support / report，而不是 hosted clone。

### 3. New capability, old job

`C1/C2/C3 + H2/H5 + F1/F3`

成本或能力解锁 + 老任务/垂直任务 + 已有支出 → 重做一个过去经济性不成立的产品。

### 4. Invisible tax

`D3/D4/D5 + F5 + H6`

验证/成本/数据流不可见 + 有负责人 + 可生成凭证 → checker / guard / receipt / report。

### 5. Ownership wave

`B4 + E3 + D6 + F5`

所有权搜索 + export/backup friction + 真实连续性/合规责任 → portable/offline/backup product。

### 6. Question-to-tool funnel

`E4/E5 + G3 + H6`

实现/比较查询 + 高意图问题 + 可交互交付物 → calculator/checker/comparison tool。

---

# 使用约束

1. **不要为了覆盖模式而凑候选。** 模式只是扫描器。
2. **不要把模式当证据。** `A1` 只能告诉你“涨价值得检查”，不能证明用户会买替代品。
3. **不要把两个页面复述同一新闻当两个 pattern signal。** 独立性仍按 `evidence.md`。
4. **热门品牌名的机会必须尝试抽象为持久 job。** 如果离开品牌名就无法描述价值，decay risk 很高。
5. **每个强候选至少写一个 alternate explanation。** 例如“搜索涨是导航需求”“OSS 没商业版因为没人付费”“抱怨是文档问题”。
6. **优先 small wedge，不默认 full replacement。** 独立开发者的优势通常是窄、快、可见，而不是功能总量。
7. **优先能替代已有成本或承担明确责任的 payer。** “觉得酷”不等于预算。

## Pattern ID 在研究记录中的用法

候选建议记录：

```json
{
  "candidate": "example",
  "pattern_ids": ["A1", "E2", "G4"],
  "change": "incumbent raised price and users started migration searches",
  "job": "move existing projects without losing history",
  "payer": "small agency owner",
  "wedge": "migration preflight + importer",
  "proof": "migration readiness report",
  "alternate_explanation": "search spike may be news-driven"
}
```

Pattern IDs 用于保证推理可追溯和检测 mode collapse，不进入最终评分公式。
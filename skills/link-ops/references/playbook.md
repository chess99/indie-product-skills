# Link Ops Playbook

## 一、选择正确竞品

优先选择：

- 同一关键词/主题簇当前 SERP 前 20；
- 与目标页面类型一致：工具对工具、攻略对攻略、数据库对数据库；
- 站点体量相近，避免只分析 Wikipedia、Reddit 或超级品牌；
- 先选少量直接竞争或共享受众的站点；当新增来源改变机会队列时再扩展。

把“整个网站很强”和“这个页面靠什么拿到链接”分开看。

## 二、竞品反查分类

拿到 referring pages/domains 后，先按“链接原因”分类：

| category | 识别信号 | 常见动作 |
|---|---|---|
| marketplace | 插件、模板、应用、生态目录 | 提交真实产品/集成 |
| listicle | Best X、Alternatives、Top tools | 申请加入对比 |
| resource | Resources、Useful tools | 推荐资源 |
| tutorial | How-to、workflow、step | 提供更适合该步骤的工具 |
| review | Review、comparison | 提供试用或数据 |
| community | Reddit、论坛、问答 | 先解决问题，再自然引用 |
| integration | Partner、Integration、API | 做真实集成 |
| open-source | GitHub、Awesome List、examples | 发布 OSS/示例/SDK |
| data-citation | 数据、统计、研究 | 提供更新/原创数据 |
| broken-link | 目标 404/停服 | 提供替代 |
| press | 新闻、newsletter、记者引用 | 提供新事实/数据/专家来源 |
| guest | 专题贡献文章 | 只做真实读者价值内容 |
| directory | 泛目录、launch list | 低成本基础分发 |

优先研究同时链接多个竞品的来源；这通常说明页面本身存在稳定的“推荐同类资源”意图。

## 三、公开搜索发现模式

没有 backlink 工具时，用公开网页和搜索结果补齐：

```text
"best [category] tools"
"[competitor] alternatives"
"[competitor]" -site:competitor.com
intitle:resources "[topic]"
inurl:resources "[topic]"
"recommended tools" "[topic]"
"helpful tools" "[topic]"
"how to [task]" "[competitor]"
"[competitor]" "review"
"[competitor]" "integration"
"[competitor]" "github"
"[topic]" "awesome"
```

不要依赖 `link:` 搜索操作符作为完整 backlink 数据源，也不要把搜索结果数量当作 backlink 数量。

## 四、优先级判断

先问五个问题：

1. 这个页面与目标用户/任务真的相关吗？
2. 链接是不是作者/编辑主动选择，而非任何人都能批量制造？
3. 页面本身有人读、能被发现、长期存在吗？
4. 用户看到链接后有点击理由吗？
5. 竞争者为什么拿到这条链接，我们能否提供同等或更强的理由？

只要第 2 条明显为否，就不要被高 DR/DA 迷惑。

## 五、新站基础分发

新站第一批渠道优先帮助用户发现和使用产品：

- 对应技术/产品生态；
- GitHub / package registry / template gallery；
- 真实个人或产品资料；
- 1–3 个高相关 launch/product directory；
- 目标用户真实存在的垂直社区；
- 自己已有且主题相关的网站/项目；
- partner / integration 页面。

保留有目标用户、可解释价值和实际维护能力的入口，数量随场景决定。

## 六、Linkable Asset

优先做能被别人“引用”的东西：

- 原创数据与定期更新统计；
- 免费计算器/检查器；
- 可下载模板；
- 行业价格/兼容性数据库；
- API、SDK、示例代码；
- 可复现 benchmark；
- migration checklist；
- 对比矩阵；
- 历史数据和趋势页。

Asset 要有独立 URL、稳定标题、清晰口径和可复制的引用信息。

## 七、Outreach

每封外联至少包含：

`具体页面上下文 + 具体缺口 + 我们能补什么 + 直接验证入口`

不群发“Dear webmaster, please link to us”。

适合跟进 1 次；若无响应，默认结束，除非对方明确邀请再次联系。

## 八、Campaign 节奏

### Launch Sprint
先完成相关基础分发与直接竞品反查，再根据发现的引用原因准备资源/资产和定向外联。节奏服从页面成熟度、授权和渠道响应，不要求按固定日期凑动作。

### Mature Page
先分析排名前 10 的新增 referring domains，再补内容/产品差距和高相关链接，不为了“链接速度”制造低质量链接。

### Defense
已有排名掉落时，把链接变化与内容、索引、SERP 意图、热度变化一起检查，不能默认归因于 backlinks。

# 3.0 迁移说明

仓库与插件名称统一为 `indie-product-skills`，版本升至 3.0.0。产品范围覆盖软件产品机会发现、验证、发布与增长；平台专项保留明确边界。

## 名称与入口

| 对象 | 旧值 | 新值 |
|---|---|---|
| GitHub 仓库 | `chess99/webmaster-skills` | `chess99/indie-product-skills` |
| 插件与 marketplace 身份 | `webmaster-skills` | `indie-product-skills` |
| 展示名称 | Webmaster Skills | Indie Product Skills |
| 网站性能技能 | `performance` | `web-performance` |
| 网站上线检查技能 | `post-launch` | `web-post-launch` |

新版只提供新技能入口。旧名称不保留额外发现入口，避免同一能力重复加载；保存的提示、自动化和显式技能调用需要替换对应名称及插件前缀。其余技能名称保持不变。

## 更新安装

1. 将仓库来源更新为 [chess99/indie-product-skills](https://github.com/chess99/indie-product-skills)。已有 Git 检出可运行 `git remote set-url origin https://github.com/chess99/indie-product-skills.git`；本地文件夹无需改名。
2. 通过当前客户端添加或刷新新来源，按新身份安装插件。Claude Code 命令见 [README](../README.md#安装)。仓库改名不等于客户端已安装的旧插件身份自动迁移。
3. 在客户端停用旧插件并启用新插件，确认技能列表出现 `validate-product-idea`、`web-performance`、`web-post-launch` 后移除旧插件。避免同时启用新旧两份。
4. 更新已保存的显式调用，例如 `webmaster-skills:performance` 改为 `indie-product-skills:web-performance`；无插件前缀的 `$performance` 改为 `$web-performance`。实际调用语法按客户端使用。

手工链接 `skills/` 的安装方式继续使用同一目录；直接链接旧技能子目录的配置需更新目标。项目路径、私有研究工件和既有数据结构无需迁移。

## 能力与结构

- 新增 `validate-product-idea`：验证已有想法，按任务选择产品形态并定义首版范围。它衔接开放式机会发现与工程实现；深入访谈分析、定位文档和发布营销继续使用各自技能。
- `find-product-opportunities` 明确跨形态判断，不默认网站、SaaS 或订阅。
- Web 检查与性能技能更名并明确边界；原生应用的审核、签名、安装和更新尚无完整专项工作流。
- `skills/` 保持扁平，按任务阶段导航见 [技能目录](skill-catalog.md)。上游快照、许可证、补丁与锁定摘要保持原有维护方式。

本次没有修改私有研究文件格式。早期数据的兼容规则见 [维护与验证](maintenance.md#20-数据兼容)。

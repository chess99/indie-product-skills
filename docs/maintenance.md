# 维护与验证

## 日常修改

本地技能直接维护 `skills/<name>/`。只在任务需要时加载 references；入口描述应能区分邻近技能。改变行为时先记录实际失败场景，再修改说明或工具。清单版本在 `.claude-plugin/plugin.json`、`.codex-plugin/plugin.json` 和 marketplace metadata 中保持一致。

兼容入口保持符号链接。Windows 检出前启用 `git config --global core.symlinks true`，并使用允许创建符号链接的环境；CI 已显式启用。

## 验证层次

### 1. 确定性行为与资源

Python 3.11+：

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository.py
python -m compileall -q skills/find-product-opportunities/scripts skills/link-ops/scripts scripts
```

测试关注决策状态、独立支持来源、引用、评分边界、URL 身份和失败返回值。仓库校验检查官方快照文件摘要、技能链接、第一方 Markdown 引用与清单一致性。`vendor/` 的模板示例链接不由本地引用检查推断为有效资源。

### 2. 官方格式

将校验器装在隔离环境。CI 固定 Agent Skills 提交及 Claude CLI 版本，升级这些依赖时一起复核输出和退出状态：

```bash
python -m pip install 'git+https://github.com/agentskills/agentskills.git@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref'
npm install --global @anthropic-ai/claude-code@2.1.308
python scripts/validate_repository.py --skills-ref skills-ref --claude claude
```

`skills-ref` 对所有技能的真实路径运行。Claude 插件与 marketplace 用临时解引用安装目录进行 strict 校验，避免官方工具跳过符号链接；源仓库保持单一事实源。以退出码判断成功，不能用输出是否包含 `valid` 判断。

官方校验器不验证研究结论、真实平台访问或商业效果。Codex 清单的身份/版本/入口一致性由本地检查覆盖；不将其称为独立的 Codex 官方运行时测试。

### 3. 模型行为

本地六项技能均有 `evals/evals.json`，采用 `skill_name` / `evals` / `prompt` / `expected_output` / `files` 结构；发现模式补充集位于 `discovery-patterns.json`。

对行为改动选择相关案例，在隔离临时目录分别运行当前技能与旧版或不加载技能的基线。两组使用相同任务、输入、工具条件与模型配置，不把评分标准泄露为待执行任务。记录产出、工具调用、时间/用量、错误和副作用，由独立评分或人工复核实际结果。只运行到授权的只读/本地边界。

可按需使用 [skill-up](https://github.com/alibaba/skill-up) 导入案例和比较基线，无需成为运行依赖。格式检查通过、单元测试通过和模型行为通过分别报告；案例存在只能说明已定义评测场景。

## 同步上游

`vendor/marketing/` 基于选用的 MIT 上游快照。兼容问题通过 `patches/` 记录最小差异，lock 的 `files` 保留原始摘要，`patches` 记录修改后摘要；普通文案不要直接分叉。同步流程：

1. 查看官方仓库提交、版本和变更；固定完整 commit SHA，不跟随浮动 main 下载。
2. 从官方仓库获取该提交到临时目录，检查许可、所选技能、参考路径、工具依赖、授权要求和过时平台声明。
3. 按 lock 的选用列表同步完整技能目录和 LICENSE。新增技能先解释其价值与重叠；不自动导入账号连接、发送脚本或全量新增技能。
4. 更新 lock 的 commit、version、核查日期、下载归档 SHA-256 和每个选用文件的原始 SHA-256。文件摘要按相对 `vendor/marketing/` 的 POSIX 路径排序生成。检查已记录补丁是否仍需应用：上游已修复则移除，否则重新核对并记录补丁后摘要。
零上下文兼容补丁使用 `git apply --unidiff-zero`；应用前核对原始摘要，应用后核对补丁后摘要。

5. 审查差异，运行全部验证，再提交本次修改。原始下载、私有数据和评测运行日志留在仓库外。

当前选择原有 40 项营销技能，加 attribution、prospecting、marketing-loops。未选入的上游技能可能出现在文字建议中；运行时先检查可用性，再按实际任务继续，不能假定已经安装。平台数据和工具推荐仍需按当前任务核实。

## 2.0 数据兼容

已有 schema_version 1 的研究文件仍可读取。`recommendation` 允许 1–3 个 finalist；新增 `needs-validation`，其报告须标识 NEEDS-VALIDATION 且不设 finalist/主推荐。no-go 同样不应保留 finalist；待研究/已淘汰候选可分别记为 pending/rejected。

`source_group` 是可选的共同原始来源标识。旧数据默认按规范化 URL 去重；转载关系仍需采集者补充。背景、反对证据和低可信线索不能补足推荐支持数量。旧报告因此失败时应重新审查结论，不能仅换标签让它通过。

Link Ops 的 URL 键保留路径和查询大小写，仅规范化协议/主机并忽略 fragment。以前错误合并而丢失的行需从原始导出重新导入。`spam_risk` 使用整数等级，非有限分数与小数风险不再接受。

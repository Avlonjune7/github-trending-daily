# 日报更新流程

1. 读取当前 main 的 AGENTS.md、scripts/import_issue.py 和最近一期格式，保留用户改动。
2. 核实当日 Trending 与采集时间，使用公开项目资料。少于15项如实说明，无法核实时不发布伪造期次；不把期刊当作热榜。
3. 以 Asia/Shanghai 日期生成 daily-YYYY-MM-DD 期次 ID。公开 JSON 放 data/issues/<ID>.json，生成内容放 content/daily/YYYY-MM-DD.md。没有新事实不要重复提交相同期次。
4. 用 scripts/import_issue.py 验证并生成 Markdown；若无执行环境，可按脚本的 JSON front matter 格式构造，必须检查字段、链接、唯一仓库和数量，并明确未运行本地构建。
5. 有条件时运行 hugo --minify。以 GitHub 连接器读取当前 HEAD 和 tree，在同一提交中新增/更新本期两个文件；基于现有 tree 并用 expected_sha 更新 main，不覆盖其他路径，不强推。无需个人访问令牌。
6. GitHub Actions 在 main push 后构建并发布；按确切提交核实 actions/runs 的部署成功，不只检查提交成功。线上回读 /daily/YYYY-MM-DD/，核实日期、项目数量、内容与样式资源。
7. 成功后在原对话发送简短摘要和当期公开网址。提交成功但发布未完成时明确区分；失败时保留旧内容，报告并提供已核实的文本，不把旧网址当新刊。

只发布公开榜单资料，禁止个人信息、私有站点凭据或内部记录。原私有站点是否继续更新由既有任务要求决定；本仓库不读取或暴露其服务令牌。这里的 Actions 只部署内容，不自行采集或生成分析。

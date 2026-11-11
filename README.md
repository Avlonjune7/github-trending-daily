# 开源雷达 · Hugo

中文 GitHub Trending 日报、周榜与月榜，纯静态输出，无 Node.js、数据库或运行时服务器依赖。

## 本地运行

安装 Hugo 0.147.9 或兼容版本，执行 `hugo server`。生产构建：`hugo --minify`，产物在 `public/`。

## 更新一期

1. 核实真实 Trending 数据和采集时间，公开资料才可提交。
2. 按 `data/issues/daily-2026-11-10.json` 格式准备 JSON，保存到 `data/issues/`。
3. 执行 `python3 scripts/import_issue.py data/issues/<期次>.json`。
4. 执行 `hugo --minify`，检查本期页与来源，提交 JSON 与 Markdown。

少于15项如实注明，不用旧期刊凑数；抓取失败不生成冒充成功的数据。GitHub Actions 负责构建与发布，不自动采集或编造内容。

## GitHub Pages

仓库：https://github.com/Avlonjune7/github-trending-daily

预期站点：https://avlonjune7.github.io/github-trending-daily/ （需 Pages 部署成功后可访问）。

在 Settings → Pages 选择 GitHub Actions。推送 main 后工作流发布。本站不需要任何私有 API Key。

目前收录2026-11-10已核实日榜11项，周/月栏目为空。历史数据不是实时榜单。部署、持续更新在实际验证之前不得宣称成功。

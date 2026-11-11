# 开源雷达 · Hugo

中文 GitHub Trending 日榜、周榜、月榜与精选阅读，原生 Hugo 静态站。

## 本地运行

安装 Hugo 0.147.9 或兼容版本，执行 `hugo server`。生产构建：`hugo --minify`，产物在 `public/`。

## 交给 AI 更新内容

先阅读 [AGENTS.md](AGENTS.md) 与 [每日更新规则](UPDATE_WORKFLOW.md)，后者末尾包含可直接复制的任务提示词。

- 从 2026-11-12 起，日榜固定取官方前 10 名；跨日期不去重，核实不足 10 名暂停发布。
- 默认只写本期 `data/issues/daily-YYYY-MM-DD.json`，再由 `scripts/import_issue.py` 生成对应 Markdown。
- 分类可扩展；列表摘要和弹窗概况分开，四块介绍按官方资料核实。
- **不得修改布局、样式、交互、脚本、配置或设计规范。** 规则文档不是 GitHub 权限隔离，仍需审查提交范围。
- 提交前完成生成器校验、Hugo 构建与差异检查。提交、推送和发布需要任务明确授权。

```bash
python3 scripts/import_issue.py data/issues/daily-YYYY-MM-DD.json
hugo --minify
git diff --check
```

## 页面与发布

首页展示最新日榜；旧期保留在归档。精选阅读独立展示阮一峰周刊与 HelloGitHub。

[GitHub Pages 站点](https://avlonjune7.github.io/github-trending-daily/)

推送 `main` 后，现有 GitHub Actions 构建并发布。Actions 不负责自动采集；每日任务需要另行安排。发布完成以对应提交工作流和线上回读为准。

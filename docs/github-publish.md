# GitHub 发布说明

当前 GitHub 仓库：

```text
https://github.com/mavis-codee/lightweight-llm-pi
```

项目中文名仍是“轻量大模型”。GitHub 仓库名使用 `lightweight-llm-pi`，避免中文仓库名在 CLI 中被规范化成不可读的短横线。

如果需要重新发布到另一个仓库，可以在项目根目录运行：

```bash
git init
git add .
git commit -m "初始化轻量大模型树莓派离线助手"
gh repo create "lightweight-llm-pi" --public --source=. --remote=origin --push --description "轻量大模型：面向树莓派的离线轻量大模型助手，支持本地 GGUF 加载、基础计算和安全提示。"
```

如果不用 GitHub CLI，也可以先在 GitHub 网页创建空仓库，然后运行：

```bash
git init
git add .
git commit -m "初始化轻量大模型树莓派离线助手"
git branch -M main
git remote add origin https://github.com/mavis-codee/lightweight-llm-pi.git
git push -u origin main
```

发布后建议补充：

- 仓库 Topics：`raspberry-pi`, `llm`, `offline-ai`, `gguf`, `safety`, `public-good`
- About 描述：`面向树莓派的离线轻量大模型助手，支持本地模型加载、基础计算和安全提示。`
- README 中加入实际测试过的模型和树莓派型号。

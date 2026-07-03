# GitHub 发布说明

当前项目建议仓库名：

```text
轻量大模型
```

如果你的系统已安装 Git 和 GitHub CLI，可以在项目根目录运行：

```bash
git init
git add .
git commit -m "初始化轻量大模型树莓派离线助手"
gh repo create "轻量大模型" --public --source=. --remote=origin --push --description "面向树莓派的离线轻量大模型助手，支持本地 GGUF 加载、基础计算和安全提示。"
```

如果不用 GitHub CLI，也可以先在 GitHub 网页创建空仓库，然后运行：

```bash
git init
git add .
git commit -m "初始化轻量大模型树莓派离线助手"
git branch -M main
git remote add origin https://github.com/mavis-codee/轻量大模型.git
git push -u origin main
```

发布后建议补充：

- 仓库 Topics：`raspberry-pi`, `llm`, `offline-ai`, `gguf`, `safety`, `public-good`
- About 描述：`面向树莓派的离线轻量大模型助手，支持本地模型加载、基础计算和安全提示。`
- README 中加入实际测试过的模型和树莓派型号。

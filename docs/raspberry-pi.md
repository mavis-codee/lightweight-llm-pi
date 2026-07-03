# 树莓派部署指南

## 推荐硬件

- Raspberry Pi 5 8GB，或 Raspberry Pi 4 8GB。
- 32GB 以上 microSD 卡，建议使用 SSD。
- 主动散热。

## 安装

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip build-essential cmake
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install -e .
pip install -r requirements-pi.txt
```

如果 `llama-cpp-python` 编译较慢，这是正常现象。也可以查找适合当前系统和 Python 版本的预编译 wheel。

## 模型选择

优先从小模型开始：

- Qwen2.5-0.5B-Instruct GGUF
- TinyLlama-1.1B-Chat GGUF
- Phi 系列小参数 GGUF

建议使用 4-bit 量化模型，例如 `Q4_0`、`Q4_K_M`。把模型放到 `models/model.gguf`，然后运行：

```bash
python -m lightweight_llm_pi --model models/model.gguf
```

## 性能建议

- `--threads` 设置为 CPU 核心数或略少。
- `--context` 从 1024 或 2048 开始。
- `--max-tokens` 保持在 128 到 256，减少等待。
- 避免同时运行多个重负载服务。

## 离线公益场景

- 社区服务点：基础计算、政策材料解释、安全常识提醒。
- 乡村教育：离线问答、数学练习、阅读陪伴。
- 家庭设备：隐私优先的本地助手。

请始终把高风险问题交给专业人员处理。

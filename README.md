# 轻量大模型

面向树莓派和低成本设备的离线轻量 AI 助手实验项目。目标是让基础计算、常识问答和安全提示能力走进基层用户手中，以积极、负责任的方式造福全人类。

> 我们的口号：造福全人类。

## 项目愿景

- **离线可用**：模型文件放在本机，优先保护隐私，弱网或无网环境也能运行。
- **低成本硬件**：以 Raspberry Pi 4/5、8GB 内存设备为主要目标。
- **基础计算可靠**：内置安全计算器，不把简单数学问题完全交给语言模型猜。
- **安全提示优先**：遇到医疗、法律、金融、灾害、自伤等高风险内容时，先给出明确的安全边界和求助建议。
- **开放公益**：帮助普通家庭、乡村服务点、基层教育和公益场景低成本接触 AI。

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
python -m lightweight_llm_pi --demo
```

树莓派上：

```bash
bash scripts/install_raspberry_pi.sh
source .venv/bin/activate
python -m lightweight_llm_pi --demo
```

## 加载本地模型

本项目使用 GGUF 模型文件，通过 `llama-cpp-python` 独立加载。你可以使用 TinyLlama、Qwen2.5 0.5B/1.5B Instruct、Phi 小模型等量化版本。

```bash
mkdir -p models
# 把 .gguf 模型文件放入 models/，例如 models/model.gguf
python -m lightweight_llm_pi --model models/model.gguf
```

也可以用环境变量：

```bash
export QL_MODEL_PATH=models/model.gguf
python -m lightweight_llm_pi
```

如果没有模型，程序仍会启动，并提供基础计算和安全提示能力。

## 基础模型实测

当前已验证的第一颗基础模型：

```text
Qwen2.5-0.5B-Instruct-Q4_K_M.gguf
大小：约 398MB
运行器：llama.cpp CLI，纯 CPU
本机实测：约 54 tokens/s
```

Windows 下可以用：

```powershell
winget install --id ggml.llamacpp -e --source winget
.\scripts\run_llama_cpp_windows.ps1
```

## 命令示例

```text
/calc 128 * 36 + 7
/safe 家里闻到煤气味怎么办
我想学习怎样更安全地使用农机
```

## 树莓派建议

- Raspberry Pi 5 + 8GB 内存体验更好。
- 优先选择 `Q4_K_M`、`Q4_0` 等量化 GGUF 模型。
- 建议从 0.5B 到 1.5B 参数模型开始，保证响应速度。
- 使用主动散热，避免长时间推理时降频。

详见 [docs/raspberry-pi.md](docs/raspberry-pi.md)。

## 安全声明

本项目不是医生、律师、消防员、心理危机干预人员或金融顾问的替代品。遇到紧急危险，请立即联系当地紧急救援服务或可信赖的专业人员。项目的安全提示层只用于降低误用风险，不能保证覆盖所有情况。

## 许可证

Apache-2.0。欢迎用于公益、教育和基层服务场景，也欢迎改进安全提示和低成本部署方案。

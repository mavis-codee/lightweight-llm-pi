from __future__ import annotations

import argparse
import sys

from .calculator import CalculationError, try_calculate
from .config import AppConfig
from .llm import LocalLLM, LocalModelUnavailable
from .safety import match_safety_hint, safety_context


WELCOME = """轻量大模型离线助手
输入 /calc 进行计算，输入 /safe 获取安全提示，输入 /exit 退出。"""


class Assistant:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.llm = LocalLLM(config)

    def answer(self, text: str) -> str:
        text = text.strip()
        if not text:
            return "请输入一个问题。"

        if text in {"/help", "help", "帮助"}:
            return "示例：/calc 12 * 8 + 3；/safe 家里闻到煤气味怎么办；或直接输入普通问题。"

        if text.startswith("/safe"):
            raw = text.removeprefix("/safe").strip()
            hint = match_safety_hint(raw) if raw else None
            if hint:
                return f"{hint.level}：{hint.message}"
            return "安全提示：遇到医疗、法律、金融、灾害、自伤或危险操作问题，请优先联系当地专业人员或紧急服务。"

        try:
            result = try_calculate(text)
        except CalculationError as exc:
            return f"计算失败：{exc}"
        if result is not None:
            return result.format()

        hint = match_safety_hint(text)
        prefix = f"{hint.level}：{hint.message}\n\n" if hint else ""

        try:
            generated = self.llm.generate(text, safety_context(text))
        except LocalModelUnavailable as exc:
            return prefix + fallback_answer(str(exc))

        return prefix + generated


def fallback_answer(reason: str) -> str:
    return (
        f"当前未启用本地模型：{reason}\n"
        "我仍可离线完成基础计算和安全提示。若要开启问答能力，请把 GGUF 模型放到 models/model.gguf，"
        "或使用 --model 指定模型路径。"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline lightweight LLM assistant for Raspberry Pi.")
    parser.add_argument("question", nargs="*", help="Optional one-shot question.")
    parser.add_argument("--model", help="Path to a local GGUF model.")
    parser.add_argument("--threads", type=int, help="CPU threads for llama.cpp.")
    parser.add_argument("--context", type=int, help="Context length.")
    parser.add_argument("--max-tokens", type=int, help="Maximum generated tokens.")
    parser.add_argument("--demo", action="store_true", help="Run a short offline demo.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = AppConfig.from_values(
        model=args.model,
        threads=args.threads,
        context=args.context,
        max_tokens=args.max_tokens,
    )
    assistant = Assistant(config)

    if args.demo:
        for item in ["/calc 128 * 36 + 7", "/safe 家里闻到煤气味怎么办"]:
            print(f"> {item}")
            print(assistant.answer(item))
        return 0

    if args.question:
        print(assistant.answer(" ".join(args.question)))
        return 0

    print(WELCOME)
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if text in {"/exit", "exit", "quit", "退出"}:
            return 0
        print(assistant.answer(text))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

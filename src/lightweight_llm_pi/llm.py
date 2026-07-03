from __future__ import annotations

from pathlib import Path

from .config import AppConfig


class LocalModelUnavailable(RuntimeError):
    pass


class LocalLLM:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._llm = None

    @property
    def available(self) -> bool:
        return self.config.model_path is not None

    def load(self) -> None:
        if not self.available:
            raise LocalModelUnavailable("没有找到本地 GGUF 模型文件。")
        if self._llm is not None:
            return

        try:
            from llama_cpp import Llama
        except ImportError as exc:
            raise LocalModelUnavailable("未安装 llama-cpp-python，无法加载 GGUF 模型。") from exc

        model_path = Path(self.config.model_path)
        self._llm = Llama(
            model_path=str(model_path),
            n_ctx=self.config.context,
            n_threads=self.config.threads,
            verbose=False,
        )

    def generate(self, user_text: str, system_prompt: str) -> str:
        self.load()
        assert self._llm is not None

        prompt = (
            "<|system|>\n"
            f"{system_prompt}\n"
            "<|user|>\n"
            f"{user_text}\n"
            "<|assistant|>\n"
        )
        output = self._llm(
            prompt,
            max_tokens=self.config.max_tokens,
            temperature=0.3,
            top_p=0.9,
            stop=["<|user|>", "<|system|>"],
        )
        return output["choices"][0]["text"].strip()

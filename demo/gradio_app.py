#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step4 - Gradio 데모 UI (챗봇 전용 화면)

목표:
- “카카오톡처럼” 챗봇만 보이는 단일 화면(탭/모델 선택 UI 제거)
- 전송 시 Tabs 관련 에러를 피하기 위해 Tabs를 사용하지 않는다.

실행:
    python demo/gradio_app.py
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import gradio as gr
from dotenv import load_dotenv

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore


ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"

P_CHATBOT = PROMPTS_DIR / "step4_chatbot.md"

def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _split_prompt(md: str) -> tuple[str, str]:
    if "## System" not in md or "## User" not in md:
        raise ValueError("prompt format must include '## System' and '## User'")
    sys_part = md.split("## System", 1)[1].split("## User", 1)[0].strip()
    user_part = md.split("## User", 1)[1].strip()
    return sys_part, user_part


@dataclass(frozen=True)
class Prompts:
    bot_sys: str


def load_prompts() -> Prompts:
    bot_sys, _ = _split_prompt(_read_text(P_CHATBOT))
    return Prompts(bot_sys)


def call_openai_messages(model: str, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
    if OpenAI is None:
        raise RuntimeError("openai 패키지를 불러올 수 없습니다. requirements.txt 설치를 확인하세요.")
    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return (resp.choices[0].message.content or "").strip()

def chat_fn(message: str, history: list[tuple[str, str]]) -> tuple[str, list[tuple[str, str]]]:
    """
    수동 챗봇: (answer, updated_history) 반환.
    """
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        answer = "⚠️ OPENAI_API_KEY가 없습니다(.env 설정 필요)."
        history.append((message, answer))
        return "", history

    prompts = load_prompts()
    user_msg = (message or "").strip()
    if not user_msg:
        return "", history

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # 대화 히스토리 메시지 구성
    msgs: list[dict[str, str]] = [{"role": "system", "content": prompts.bot_sys}]
    for u, a in (history or []):
        if u:
            msgs.append({"role": "user", "content": str(u)})
        if a:
            msgs.append({"role": "assistant", "content": str(a)})
    msgs.append({"role": "user", "content": user_msg})

    try:
        bot_reply = call_openai_messages(model=model, messages=msgs, temperature=0.4)
    except Exception as e:
        bot_reply = f"⚠️ (오류) {type(e).__name__}: {e}"

    history.append((user_msg, bot_reply))
    return "", history


def main() -> None:
    css = """
    /* 카카오톡 느낌: 중앙 정렬 + 넓이 제한 */
    .gradio-container { max-width: 720px !important; margin: 0 auto !important; }
    """
    with gr.Blocks(title="CareLog 챗봇", css=css) as demo:
        gr.Markdown("## 🏥 CareLog 챗봇")
        gr.Markdown("예약/안내 중심 의료 서비스 챗봇 (건강검진/병원/약국)")

        chatbot = gr.Chatbot(label="대화", height=500)
        msg = gr.Textbox(
            label="메시지",
            placeholder="예: 오늘 건강검진 예약 가능한가요?",
            show_label=False,
        )

        with gr.Row():
            submit = gr.Button("전송", variant="primary")
            clear = gr.Button("대화 초기화")

        gr.Examples(
            examples=[
                "오늘 건강검진 예약 가능한가요?",
                "예약 변경은 언제까지 가능한가요?",
                "영업시간이 어떻게 되나요?",
            ],
            inputs=msg,
        )

        # 전송 이벤트 연결
        msg.submit(chat_fn, [msg, chatbot], [msg, chatbot])
        submit.click(chat_fn, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: ([], ""), outputs=[chatbot, msg])

    demo.launch(show_api=False, share=True, server_name="0.0.0.0")


if __name__ == "__main__":
    main()


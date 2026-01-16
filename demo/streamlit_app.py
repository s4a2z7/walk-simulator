#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step4 - Streamlit 챗봇 데모

목표:
- 카카오톡처럼 챗봇만 보이는 단일 화면
- Gradio 버전 호환 이슈를 피하기 위해 Streamlit 사용

실행:
    streamlit run demo/streamlit_app.py
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import streamlit as st
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


def _extract_system_prompt(md: str) -> str:
    """챗봇용: ## System 섹션만 추출 (## User 불필요)"""
    if "## System" not in md:
        raise ValueError("prompt format must include '## System'")
    sys_part = md.split("## System", 1)[1].strip()
    # 다음 ## 섹션이 있으면 거기까지만, 없으면 끝까지
    if "\n## " in sys_part:
        sys_part = sys_part.split("\n## ", 1)[0].strip()
    return sys_part


@dataclass(frozen=True)
class Prompts:
    bot_sys: str


def load_prompts() -> Prompts:
    bot_sys = _extract_system_prompt(_read_text(P_CHATBOT))
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


def check_evolution(total_exp: int) -> tuple[int, str, str, bool]:
    """진화 체크 함수 - 경험치 기반 진화 단계 결정"""
    stage_thresholds = {
        1: {"exp": 0, "name": "알알이", "emoji": "🥚"},
        2: {"exp": 100, "name": "보금자리", "emoji": "🦅"},
        3: {"exp": 200, "name": "날개짓", "emoji": "🦚"},
        4: {"exp": 300, "name": "불사조 어린이", "emoji": "🔥"},
        5: {"exp": 400, "name": "황금 불사조", "emoji": "✨"},
    }
    
    new_stage = 1
    new_stage_name = "알알이"
    new_stage_emoji = "🥚"
    evolved = False
    
    for stage, data in stage_thresholds.items():
        if total_exp >= data["exp"] and stage > new_stage:
            new_stage = stage
            new_stage_name = data["name"]
            new_stage_emoji = data["emoji"]
            evolved = True
    
    return new_stage, new_stage_name, new_stage_emoji, evolved


def add_steps(current_steps: int, total_steps: int, total_exp: int, steps_to_add: int) -> tuple[int, int, int]:
    """걸음수 추가 함수"""
    new_steps = current_steps + steps_to_add
    new_total_steps = total_steps + steps_to_add
    new_total_exp = (new_total_steps // 10)  # 10 걸음당 1 경험치
    return new_steps, new_total_steps, new_total_exp


def main() -> None:
    st.set_page_config(page_title="CareLog 챗봇", page_icon="🏥", layout="wide")
    
    # 탭 생성
    tab1, tab2 = st.tabs(["펫 시뮬레이터", "챗봇"])
    
    # 탭 1: 펫 시뮬레이터
    with tab1:
        st.header("🐣 CareLog 펫 시뮬레이터")
        st.caption("걸음수를 기록하고 펫을 성장시켜보세요!")
        
        # 펫 상태 초기화
        if "pet" not in st.session_state:
            st.session_state.pet = {
                "name": "불사조",
                "stage": 1,
                "stage_name": "알알이",
                "stage_emoji": "🥚",
                "level": 1,
                "experience": 0,
                "steps": 0,
                "hunger": 100,
                "happiness": 100,
                "total_steps": 0,
                "total_exp": 0,
            }
        
        pet = st.session_state.pet
        
        # 펫 정보 표시
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"<div style='text-align: center; font-size: 60px;'>{pet['stage_emoji']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold;'>{pet['name']} ({pet['stage_name']})</div>", unsafe_allow_html=True)
        
        # 펫 상태 표시
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("오늘 걸음수", f"{pet['steps']:,}", f"+{pet['steps']}")
        
        with col2:
            st.metric("레벨", f"Lv.{pet['level']}")
        
        with col3:
            st.metric("누적 걸음수", f"{pet['total_steps']:,}")
        
        with col4:
            st.metric("경험치", f"{pet['total_exp']}")
        
        # 배고픔과 행복도
        st.progress(pet['hunger'] / 100, text=f"배고픔: {pet['hunger']}/100")
        st.progress(pet['happiness'] / 100, text=f"행복도: {pet['happiness']}/100")
        
        # 걸음수 추가 버튼
        st.markdown("### 🚶 걸음수 추가")
        
        button_col1, button_col2, button_col3 = st.columns(3)
        
        with button_col1:
            if st.button("➕ 10걸음", use_container_width=True, key="add_10"):
                new_steps, new_total, new_exp = add_steps(
                    pet['steps'], 
                    pet['total_steps'], 
                    pet['total_exp'],
                    10
                )
                new_stage, new_stage_name, new_stage_emoji, evolved = check_evolution(new_exp)
                
                st.session_state.pet['steps'] = new_steps
                st.session_state.pet['total_steps'] = new_total
                st.session_state.pet['total_exp'] = new_exp
                st.session_state.pet['level'] = (new_exp // 100) + 1
                st.session_state.pet['experience'] = new_exp % 100
                st.session_state.pet['hunger'] = max(0, pet['hunger'] - 2)
                
                if evolved:
                    st.session_state.pet['stage'] = new_stage
                    st.session_state.pet['stage_name'] = new_stage_name
                    st.session_state.pet['stage_emoji'] = new_stage_emoji
                    st.success(f"🎉 축하합니다! {pet['name']}가 **{new_stage_name}**으로 진화했습니다!")
                
                st.rerun()
        
        with button_col2:
            if st.button("⭐ 100걸음", use_container_width=True, key="add_100"):
                new_steps, new_total, new_exp = add_steps(
                    pet['steps'], 
                    pet['total_steps'], 
                    pet['total_exp'],
                    100
                )
                new_stage, new_stage_name, new_stage_emoji, evolved = check_evolution(new_exp)
                
                st.session_state.pet['steps'] = new_steps
                st.session_state.pet['total_steps'] = new_total
                st.session_state.pet['total_exp'] = new_exp
                st.session_state.pet['level'] = (new_exp // 100) + 1
                st.session_state.pet['experience'] = new_exp % 100
                st.session_state.pet['hunger'] = max(0, pet['hunger'] - 5)
                
                if evolved:
                    st.session_state.pet['stage'] = new_stage
                    st.session_state.pet['stage_name'] = new_stage_name
                    st.session_state.pet['stage_emoji'] = new_stage_emoji
                    st.success(f"🎉 축하합니다! {pet['name']}가 **{new_stage_name}**으로 진화했습니다!")
                
                st.rerun()
        
        with button_col3:
            if st.button("🚀 1000걸음", use_container_width=True, key="add_1000"):
                new_steps, new_total, new_exp = add_steps(
                    pet['steps'], 
                    pet['total_steps'], 
                    pet['total_exp'],
                    1000
                )
                new_stage, new_stage_name, new_stage_emoji, evolved = check_evolution(new_exp)
                
                st.session_state.pet['steps'] = new_steps
                st.session_state.pet['total_steps'] = new_total
                st.session_state.pet['total_exp'] = new_exp
                st.session_state.pet['level'] = (new_exp // 100) + 1
                st.session_state.pet['experience'] = new_exp % 100
                st.session_state.pet['hunger'] = max(0, pet['hunger'] - 20)
                
                if evolved:
                    st.session_state.pet['stage'] = new_stage
                    st.session_state.pet['stage_name'] = new_stage_name
                    st.session_state.pet['stage_emoji'] = new_stage_emoji
                    st.success(f"🎉 축하합니다! {pet['name']}가 **{new_stage_name}**으로 진화했습니다!")
                
                st.rerun()
    
    # 탭 2: 챗봇
    with tab2:
        st.title("🏥 CareLog 챗봇")
        st.caption("예약/안내 중심 의료 서비스 챗봇 (건강검진/병원/약국)")
        
        load_dotenv(ROOT / ".env")
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            st.error("⚠️ OPENAI_API_KEY가 없습니다(.env 설정 필요).")
            st.stop()

        prompts = load_prompts()
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # 세션 상태 초기화
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 대화 히스토리 표시
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # 사용자 입력
        if user_input := st.chat_input("메시지를 입력하세요 (예: 오늘 건강검진 예약 가능한가요?)"):
            # 사용자 메시지 추가
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # 봇 응답 생성
            with st.chat_message("assistant"):
                with st.spinner("답변 생성 중..."):
                    try:
                        msgs: list[dict[str, str]] = [{"role": "system", "content": prompts.bot_sys}]
                        for m in st.session_state.messages:
                            msgs.append({"role": m["role"], "content": m["content"]})

                        bot_reply = call_openai_messages(model=model, messages=msgs, temperature=0.4)
                    except Exception as e:
                        bot_reply = f"⚠️ (오류) {type(e).__name__}: {e}"

                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        # 사이드바: 대화 초기화 버튼
        with st.sidebar:
            st.header("설정")
            if st.button("대화 초기화", use_container_width=True):
                st.session_state.messages = []
                st.rerun()


if __name__ == "__main__":
    main()

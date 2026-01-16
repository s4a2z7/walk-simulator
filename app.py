import streamlit as st
from openai import OpenAI
import base64
from dotenv import load_dotenv
import os
from prompt import build_prompt
from pathlib import Path
from typing import List, Tuple


def check_evolution(total_exp: int) -> tuple:
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


def add_steps(current_steps: int, total_steps: int, total_exp: int, steps_to_add: int) -> tuple:
    """걸음수 추가 함수"""
    new_steps = current_steps + steps_to_add
    new_total_steps = total_steps + steps_to_add
    new_total_exp = (new_total_steps // 10)  # 10 걸음당 1 경험치
    return new_steps, new_total_steps, new_total_exp

# 환경변수 로드
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="CareLog", layout="wide", page_icon="🌸")

# 탭 생성
tab1, tab2, tab3 = st.tabs(["펫 시뮬레이터", "알러지 검사", "챗봇"])

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
        if st.button("➕ 10걸음", use_container_width=True, key="pet_add_10"):
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
        if st.button("⭐ 100걸음", use_container_width=True, key="pet_add_100"):
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
        if st.button("🚀 1000걸음", use_container_width=True, key="pet_add_1000"):
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

# 탭 2: 알러지 검사
with tab2:
    # 아기자기한 커스텀 CSS 스타일
    st.markdown("""
    <style>
    /* 전체 배경 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #FFF5F5 0%, #F0FFF4 50%, #F0F9FF 100%);
        background-attachment: fixed;
    }

    /* 떠다니는 애니메이션 */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    @keyframes sparkle {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* 메인 타이틀 스타일 */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #FF9A9E 0%, #FECFEF 50%, #A8EDEA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: float 3s ease-in-out infinite;
        margin-bottom: 0.5rem;
    }

    .sub-title {
        text-align: center;
        color: #8B8B8B;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* multiselect 스타일 */
    .stMultiSelect > div > div {
        background: linear-gradient(145deg, #FFF0F5 0%, #F0FFF4 100%);
        border-radius: 15px;
        border: 2px solid #FFB6C1;
    }

    .stMultiSelect span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #FFB6C1 0%, #FFC0CB 100%);
        border-radius: 20px;
        color: white;
        font-weight: 500;
    }

    /* 파일 업로더 스타일 */
    .stFileUploader > div > div {
        background: linear-gradient(145deg, #E8F5E9 0%, #F1F8E9 100%);
        border-radius: 15px;
        border: 2px dashed #98D8AA;
    }

    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 50%, #A8EDEA 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 154, 158, 0.6);
    }

    /* 정보 박스 스타일 */
    .stAlert {
        background: linear-gradient(145deg, #FFF8E1 0%, #FFFDE7 100%);
        border-radius: 15px;
        border-left: 4px solid #FFD54F;
    }

    /* 장식용 요소 */
    .decoration {
        text-align: center;
        font-size: 1.5rem;
        animation: sparkle 2s ease-in-out infinite;
    }

    /* 섹션 헤더 */
    .section-header {
        color: #FF8A9E;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 1rem 0 0.5rem 0;
    }

    /* 결과 박스 */
    .result-header {
        background: linear-gradient(120deg, #FF9A9E 0%, #FECFEF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem;
        font-weight: 700;
    }

    /* 푸터 */
    .cute-footer {
        text-align: center;
        color: #BDBDBD;
        font-size: 0.85rem;
        margin-top: 3rem;
    }

    /* 이미지 미리보기 컨테이너 */
    .image-preview {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }

    .image-preview img {
        max-width: 250px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 3px solid #FFB6C1;
    }

    /* 결과 카드 스타일 */
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        animation: float 3s ease-in-out infinite;
    }

    .result-card.danger {
        border: 3px solid #FF6B6B;
        background: linear-gradient(145deg, #FFF5F5 0%, #FFE8E8 100%);
    }

    .result-card.warning {
        border: 3px solid #FFD93D;
        background: linear-gradient(145deg, #FFFDF5 0%, #FFF8E1 100%);
    }

    .result-card.safe {
        border: 3px solid #6BCB77;
        background: linear-gradient(145deg, #F0FFF4 0%, #E8F5E9 100%);
    }

    .result-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }

    .result-badge.danger {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%);
        color: white;
    }

    .result-badge.warning {
        background: linear-gradient(135deg, #FFD93D 0%, #FFE566 100%);
        color: #5D4E37;
    }

    .result-badge.safe {
        background: linear-gradient(135deg, #6BCB77 0%, #8ED99A 100%);
        color: white;
    }

    .result-content {
        color: #555;
        line-height: 1.8;
        font-size: 0.95rem;
    }

    .result-content strong {
        color: #FF8A9E;
    }

    /* 번개 효과 (위험) */
    @keyframes lightning {
        0%, 100% { opacity: 0; }
        10%, 30%, 50% { opacity: 1; background: rgba(255, 255, 0, 0.3); }
        20%, 40% { opacity: 0; }
    }

    .lightning-effect {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        animation: lightning 0.5s ease-out 3;
        z-index: 9999;
    }

    .lightning-bolt {
        position: fixed;
        font-size: 4rem;
        animation: boltFlash 0.3s ease-in-out 5;
        z-index: 10000;
    }

    @keyframes boltFlash {
        0%, 100% { opacity: 0; transform: scale(0.5); }
        50% { opacity: 1; transform: scale(1.2); }
    }

    /* 깜박이는 효과 (주의) */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .blink-warning {
        position: fixed;
        font-size: 3rem;
        animation: blink 0.5s ease-in-out 6, floatUp 3s ease-out forwards;
        z-index: 10000;
    }

    @keyframes floatUp {
        0% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(-100px); opacity: 0; }
    }

    /* 천천히 떨어지는 효과 (안전) */
    @keyframes slowFall {
        0% { transform: translateY(-20px) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
    }

    .gentle-float {
        position: fixed;
        font-size: 2rem;
        animation: slowFall 4s ease-in-out forwards;
        z-index: 10000;
        pointer-events: none;
    }
    </style>
    """, unsafe_allow_html=True)

    # 장식 요소
    st.markdown('<div class="decoration">🌸 ✨ 🍃 ✨ 🌸</div>', unsafe_allow_html=True)

    # 메인 타이틀
    st.markdown('<h1 class="main-title">CareLog</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">당신의 안전한 식사를 위한 귀여운 알러지 검사기 🥗💕</p>', unsafe_allow_html=True)

    # 알러지 체크리스트
    st.markdown('<p class="section-header">🎀 나의 알러지 선택하기</p>', unsafe_allow_html=True)
    allergy_list = ["계란","우유","땅콩","새우","게","밀","메밀","대두","견과류","아황산염"]
    checked = st.multiselect("해당하는 알러지를 모두 선택해주세요", allergy_list)

    # 이미지 업로드
    st.markdown('<p class="section-header">📸 식품 이미지 업로드</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader("식품 영양정보 이미지를 올려주세요", type=["jpg","jpeg","png"])

    if uploaded and checked:
        # 이미지를 작게 중앙에 표시
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(uploaded, width=250)

        # base64 인코딩
        image_bytes = uploaded.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 알러지 위험 분석하기"):
            with st.spinner("✨ AI가 열심히 분석하고 있어요..."):
                prompt = build_prompt(checked)

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    }],
                )

                result_text = response.choices[0].message.content

                # 결과에 따라 카드 스타일 결정
                if "위험" in result_text:
                    card_class = "danger"
                    badge_text = "🚨 위험해요!"
                elif "주의" in result_text:
                    card_class = "warning"
                    badge_text = "⚠️ 주의가 필요해요!"
                else:
                    card_class = "safe"
                    badge_text = "✅ 안전해요!"

                st.markdown('<p class="section-header">🌟 분석 결과</p>', unsafe_allow_html=True)

                # 아기자기한 결과 카드
                result_html = f'''
                <div class="result-card {card_class}">
                    <div style="text-align: center;">
                        <span class="result-badge {card_class}">{badge_text}</span>
                    </div>
                    <div class="result-content">
                        {result_text.replace(chr(10), "<br>")}
                    </div>
                </div>
                '''
                st.markdown(result_html, unsafe_allow_html=True)

                # 결과에 따른 효과
                if card_class == "danger":
                    # 번개 효과
                    lightning_html = '''
                    <div class="lightning-effect"></div>
                    <div class="lightning-bolt" style="top: 20%; left: 20%;">⚡</div>
                    <div class="lightning-bolt" style="top: 30%; left: 70%; animation-delay: 0.1s;">⚡</div>
                    <div class="lightning-bolt" style="top: 50%; left: 40%; animation-delay: 0.2s;">⚡</div>
                    <div class="lightning-bolt" style="top: 40%; left: 80%; animation-delay: 0.15s;">⚡</div>
                    <div class="lightning-bolt" style="top: 60%; left: 15%; animation-delay: 0.25s;">⚡</div>
                    '''
                    st.markdown(lightning_html, unsafe_allow_html=True)

                elif card_class == "warning":
                    # 깜박이는 경고 효과
                    warning_html = '''
                    <div class="blink-warning" style="top: 20%; left: 15%;">⚠️</div>
                    <div class="blink-warning" style="top: 30%; left: 75%; animation-delay: 0.2s;">💡</div>
                    <div class="blink-warning" style="top: 50%; left: 50%; animation-delay: 0.3s;">⚠️</div>
                    <div class="blink-warning" style="top: 25%; left: 85%; animation-delay: 0.4s;">💡</div>
                    <div class="blink-warning" style="top: 45%; left: 25%; animation-delay: 0.5s;">⚠️</div>
                    '''
                    st.markdown(warning_html, unsafe_allow_html=True)

                else:
                    # 천천히 떨어지는 꽃잎/하트 효과
                    safe_html = '''
                    <div class="gentle-float" style="left: 10%; animation-delay: 0s;">🌸</div>
                    <div class="gentle-float" style="left: 25%; animation-delay: 0.5s;">💚</div>
                    <div class="gentle-float" style="left: 40%; animation-delay: 1s;">🍀</div>
                    <div class="gentle-float" style="left: 55%; animation-delay: 0.3s;">🌷</div>
                    <div class="gentle-float" style="left: 70%; animation-delay: 0.8s;">💚</div>
                    <div class="gentle-float" style="left: 85%; animation-delay: 1.2s;">🌸</div>
                    <div class="gentle-float" style="left: 15%; animation-delay: 1.5s;">🍀</div>
                    <div class="gentle-float" style="left: 60%; animation-delay: 1.8s;">🌷</div>
                    '''
                    st.markdown(safe_html, unsafe_allow_html=True)

    elif not checked:
        st.info("🎀 먼저 알러지를 선택해주세요!")

    # 푸터
    st.markdown('<p class="cute-footer">Made with 💕 by CareLog Team</p>', unsafe_allow_html=True)

# 탭 3: 챗봇
with tab3:
    st.markdown("## 🏥 CareLog 챗봇")
    st.markdown("예약/안내 중심 의료 서비스 챗봇 (건강검진/병원/약국)")

    # 챗봇 프롬프트 로드
    ROOT = Path(__file__).resolve().parent
    PROMPTS_DIR = ROOT / "prompts"
    P_CHATBOT = PROMPTS_DIR / "step4_chatbot.md"

    def _read_text(path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def _split_prompt(md: str) -> tuple[str, str]:
        if "## System" not in md:
            raise ValueError("prompt format must include '## System'")
        sys_part = md.split("## System", 1)[1].split("## User", 1)[0].strip() if "## User" in md else md.split("## System", 1)[1].strip()
        user_part = md.split("## User", 1)[1].strip() if "## User" in md else ""
        return sys_part, user_part

    def load_prompts() -> str:
        bot_sys, _ = _split_prompt(_read_text(P_CHATBOT))
        return bot_sys

    def call_openai_messages(model: str, messages: List[dict[str, str]], temperature: float = 0.2) -> str:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return (resp.choices[0].message.content or "").strip()

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 채팅 히스토리 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("예: 오늘 건강검진 예약 가능한가요?"):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("생각 중..."):
                try:
                    prompts = load_prompts()
                    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
                    msgs = [{"role": "system", "content": prompts}] + st.session_state.messages
                    response = call_openai_messages(model=model, messages=msgs, temperature=0.4)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"⚠️ 오류: {e}"
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})


# GitHub에 코드 업로드하기

## 📋 현재 상태
- ✅ 로컬 Git 저장소 초기화 완료
- ✅ 모든 파일 커밋 완료
- ⏳ GitHub 원격 저장소 연결 필요

## 🚀 GitHub에 업로드 방법

### 1단계: GitHub에서 새 저장소 생성
1. [github.com](https://github.com)에 로그인
2. 우상단 `+` 버튼 → `New repository` 클릭
3. 저장소 이름: `phoenix-pet` (또는 원하는 이름)
4. **Public으로 설정** (선택사항)
5. README, gitignore 추가하지 않기 (이미 있음)
6. `Create repository` 클릭

### 2단계: 원격 저장소 연결 및 푸시
생성된 저장소에서 다음 명령어를 복사하여 실행하세요:

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/phoenix-pet.git
git branch -M main
git push -u origin main
```

### 예시:
```bash
git remote add origin https://github.com/john-doe/phoenix-pet.git
git branch -M main
git push -u origin main
```

## 📝 업데이트 후 푸시하기

코드 변경 후 GitHub에 업로드하려면:

```bash
git add .
git commit -m "변경사항 설명"
git push origin main
```

## 🔗 프로젝트 정보

**Phoenix Pet - 3D 펫 키우기 게임**

- 🔥 **펫 진화**: 알 → 병아리 → 새 → 불사조 → 황금 불사조 (5단계)
- 🎮 **게임 메커니즘**: 걸음수, 경험치, 배고픔, 먹이 시스템
- 🏆 **랭킹**: 사용자 점수 순위 시스템
- 💻 **기술 스택**:
  - 프론트엔드: React + Tailwind CSS
  - 백엔드: Node.js + Express + PostgreSQL
  - 3D: Three.js + React Three Fiber (선택적)

## 📂 프로젝트 구조

```
phoenix-pet/
├── src/                    # React 프론트엔드
│   ├── components/         # 재사용 가능한 컴포넌트
│   ├── pages/              # 페이지 컴포넌트
│   └── services/           # API 호출 서비스
├── backend/                # Node.js 백엔드
│   ├── controllers/        # 비즈니스 로직
│   ├── routes/             # API 라우트
│   ├── middleware/         # 미들웨어
│   └── database/           # 데이터베이스 스키마
├── package.json            # 프론트엔드 의존성
└── README.md               # 프로젝트 설명
```

## 🎯 주요 기능 상태

- ✅ 펫 진화 시스템 (5단계)
- ✅ 애니메이션 효과
- ✅ 게임 메커니즘 (걸음수, 먹이)
- ✅ 인증 시스템
- ✅ 랭킹 시스템
- ✅ 반응형 UI (Tailwind CSS)
- ⏳ 데이터베이스 연동 (선택적)

## 📞 질문 또는 문제

터미널에서 다음 명령어로 커밋 로그를 확인할 수 있습니다:
```bash
git log --oneline
```

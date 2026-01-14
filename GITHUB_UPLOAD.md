# Walk Simulator - GitHub 업로드 가이드 🚀

## 현재 상태
✅ 로컬 Git 저장소 완성  
✅ 프로젝트 이름: **Walk Simulator**  
✅ 모든 코드 커밋 완료  

---

## GitHub 업로드 방법

### 1️⃣ GitHub에서 새 저장소 생성

1. https://github.com/new 에 접속
2. **Repository name**: `walk-simulator`
3. **Description**: `Walk Simulator - 걸음으로 키우는 불사조 게임`
4. **Public** 선택 (원하면 Private도 가능)
5. ✅ **Create repository** 클릭
6. README, .gitignore 추가 **하지 않기** (이미 있음)

### 2️⃣ 원격 저장소 연결 및 푸시

GitHub 저장소 생성 후 나타나는 명령어를 PowerShell에서 실행하세요:

**YOUR_USERNAME을 자신의 GitHub 사용자명으로 변경하세요**

```powershell
cd "c:\Users\LG\Desktop\claude simulator"
git remote add origin https://github.com/YOUR_USERNAME/walk-simulator.git
git branch -M main
git push -u origin main
```

### 예시 (john-doe 사용자인 경우)
```powershell
git remote add origin https://github.com/john-doe/walk-simulator.git
git branch -M main
git push -u origin main
```

### 3️⃣ 원격 저장소 상태 확인
```powershell
git remote -v
```

---

## 향후 업데이트 푸시 방법

코드 변경 후 GitHub에 업로드:

```powershell
git add .
git commit -m "변경사항 설명"
git push origin main
```

---

## 📦 프로젝트 정보

**Walk Simulator** - 걸음수로 키우는 불사조 게임

### 주요 기능
- 🔥 **펫 진화 시스템**: 알 → 병아리 → 새 → 불사조 → 황금 불사조 (5단계)
- 👟 **걸음 추적**: 게임 내 걸음수 계산
- 🍖 **먹이 시스템**: 3가지 음식 (불꽃 베리, 신성한 고기, 황금 과일)
- 🏆 **랭킹 시스템**: 사용자 순위
- 📊 **통계**: 일일 통계 및 진행도
- 💡 **부드러운 애니메이션**: Tailwind CSS 기반

### 기술 스택
```
Frontend:
├── React 18.2.0
├── React Router 6
├── Tailwind CSS
└── Axios (API 통신)

Backend:
├── Node.js + Express
├── PostgreSQL
├── JWT 인증
└── Rate Limiting
```

### 디렉토리 구조
```
walk-simulator/
├── src/
│   ├── components/          # 재사용 컴포넌트
│   │   ├── PetCharacter.js  # 불사조 캐릭터
│   │   ├── PetWorld.js      # 게임 월드
│   │   ├── TopBar.js        # 상단 스탯 바
│   │   ├── FoodTray.js      # 먹이 선택 UI
│   │   ├── RankingModal.js  # 랭킹 모달
│   │   └── EvolutionModal.js # 진화 애니메이션
│   ├── pages/               # 페이지
│   │   ├── LoginPage.js
│   │   ├── RegisterPage.js
│   │   ├── HomePage.js
│   │   └── DemoPage.js
│   └── services/
│       └── api.js           # API 호출
├── backend/
│   ├── controllers/         # 비즈니스 로직
│   ├── routes/              # API 라우트
│   ├── middleware/          # 미들웨어
│   ├── config/              # 설정
│   └── database/            # 스키마
└── README.md
```

---

## 🚀 로컬 실행 방법

### 프론트엔드
```bash
cd "c:\Users\LG\Desktop\claude simulator"
npm install
npm start
# http://localhost:3001 에서 실행
```

### 백엔드
```bash
cd "c:\Users\LG\Desktop\claude simulator\backend"
npm install
npm start
# http://localhost:3000 에서 실행
```

---

## 📋 커밋 로그

```powershell
git log --oneline
```

현재 커밋:
- `9e239de` 프로젝트 이름 변경: Phoenix Pet -> Walk Simulator
- `b00e7e0` Phoenix Pet: 펫 키우기 게임

---

## ⚠️ 중요 사항

- `node_modules/` 폴더는 업로드되지 않습니다 (.gitignore)
- GitHub에서 클론 후 `npm install` 실행 필요
- 백엔드 실행 시 PostgreSQL 및 환경 변수 설정 필요

---

## 📞 문제 해결

### "그런 저장소를 찾을 수 없습니다" 오류
→ GitHub 저장소를 먼저 생성했는지 확인하세요

### 인증 문제
→ GitHub Personal Access Token을 사용하거나 SSH 키 설정
https://github.com/settings/tokens

---

**Happy Coding! 🚀**

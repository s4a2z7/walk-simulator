# Walk Simulator - 자동 GitHub 업로드 가이드 🚀

## 상황
- ✅ 로컬 Git 저장소 완성
- ✅ 모든 코드 커밋 완료
- 📝 GitHub 사용자명: **s4a2z7**
- ⏳ GitHub에 코드 업로드 필요

---

## 방법 1: Personal Access Token 사용 (권장) ⭐

### Step 1: Personal Access Token 생성

1. https://github.com/settings/tokens 방문
2. **Generate new token** → **Generate new token (classic)** 클릭
3. 다음 설정 입력:
   - **Token name**: `walk-simulator-upload`
   - **Expiration**: 90 days (또는 원하는 기간)
   - **Scopes**: `repo` 체크 ✓
4. **Generate token** 클릭
5. **토큰 값 복사** (다시 볼 수 없으니 안전하게 보관!)

### Step 2: 원격 저장소 추가

PowerShell에서 다음 명령어 실행:

```powershell
cd "c:\Users\LG\Desktop\claude simulator"

# 원격 저장소 추가 (YOUR_TOKEN을 위에서 복사한 토큰으로 변경)
git remote add origin https://YOUR_TOKEN@github.com/s4a2z7/walk-simulator.git

# 푸시
git branch -M main
git push -u origin main
```

### 예시:
토큰이 `ghp_1234567890abcdefghijk`라면:
```powershell
git remote add origin https://ghp_1234567890abcdefghijk@github.com/s4a2z7/walk-simulator.git
git branch -M main
git push -u origin main
```

---

## 방법 2: GitHub CLI (설치 후 재시작 필요)

PowerShell을 **완전히 종료**한 후 새로 열고:

```powershell
cd "c:\Users\LG\Desktop\claude simulator"
gh auth login
# → web을 선택하고 브라우저에서 로그인
# → s4a2z7 사용자명 확인

# 저장소 생성 및 푸시 (한 번에!)
gh repo create walk-simulator --source=. --push --public
```

---

## 방법 3: GitHub 웹사이트에서 수동 생성 후 푸시

1. https://github.com/new 방문
2. Repository name: `walk-simulator`
3. Description: `Walk Simulator - 걸음으로 키우는 불사조 게임`
4. Public 선택
5. Create repository

그 후 PowerShell에서:

```powershell
cd "c:\Users\LG\Desktop\claude simulator"
git remote add origin https://github.com/s4a2z7/walk-simulator.git
git branch -M main
git push -u origin main

# 비밀번호 또는 Personal Access Token 입력
```

---

## 추천 순서
1. **방법 1 (Personal Access Token)** ← 가장 간단! 🌟
2. 방법 2 (GitHub CLI) - PowerShell 재시작 필요
3. 방법 3 (웹사이트 수동) - 단계가 많음

---

## ✅ 완료 확인

업로드 성공하면:
- https://github.com/s4a2z7/walk-simulator 에서 코드 확인 가능
- README.md, 모든 소스 코드 표시

---

## 앞으로 업데이트 푸시하기

```powershell
git add .
git commit -m "설명"
git push origin main
```

---

**도움이 필요하면 위 방법 중 어느 것을 선택했는지 알려주세요!** 😊

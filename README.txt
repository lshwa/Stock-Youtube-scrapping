## YouTube Data API 설정 및 크롤링 방법

이 프로젝트는 **YouTube Data API v3**를 활용하여 주식 관련 유튜브 채널의 영상 정보를 크롤링합니다.  
API 키를 발급받고 크롤러를 실행하는 방법은 다음과 같습니다.

---

###  단계별 설정 방법

1. **Google Cloud Console 접속**  
   → https://console.cloud.google.com/

2. **새 프로젝트 생성**
   - 상단의 **‘프로젝트 선택’** 클릭 후 **‘새 프로젝트’**
   - 예: 프로젝트 이름을 `youtube-stock-crawler`로 설정

3. **YouTube Data API v3 활성화**
   - 왼쪽 메뉴에서 `API 및 서비스 > 라이브러리` 이동
   - `YouTube Data API v3` 검색 후 클릭 → **사용**

4. **API 키 발급**
   - `API 및 서비스 > 사용자 인증 정보` 이동
   - 상단에서 **‘사용자 인증 정보 만들기 > API 키’** 클릭
   - 발급된 API 키 복사하여 보관

5. *(선택 사항)* **API 키 사용 제한**
   - 발급된 API 키 옆 연필 아이콘 클릭
   - "API 제한"에서 **YouTube Data API v3** 선택 후 저장

---

### 환경설정 설치 방법

```bash
# 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# requirements.txt로 라이브러리 설치
pip install -r requirements.txt
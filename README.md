# 고객관리 예시 프로젝트

FastAPI와 SQLite로 만든 교육용 고객 등록/검색/수정/삭제 웹앱입니다. 실제 고객 개인정보 대신 예시 데이터를 사용하세요.

## 실행 방법

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

브라우저에서 `http://서버의-고정-IP:8000`으로 접속합니다. AWS EC2 보안 그룹 인바운드 규칙에서 TCP 8000 포트를 허용해야 합니다. SQLite 데이터는 `customers.db`에 저장되며 Git에는 올리지 않습니다.

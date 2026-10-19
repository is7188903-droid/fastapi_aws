from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

customers = [
    {"name": "홍길동", "phone": "010-1234-5678", "grade": "VIP"},
    {"name": "이순신", "phone": "010-9876-5432", "grade": "GOLD"},
]

@app.get("/", response_class=HTMLResponse)
def home():
    rows = "".join(
        f"<tr><td>{c['name']}</td><td>{c['phone']}</td><td>{c['grade']}</td></tr>"
        for c in customers
    )
    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>AWS EC2 고객관리</title>
      <style>
        body {{ font-family: sans-serif; text-align: center; padding: 30px 16px; }}
        table {{ margin: 20px auto; border-collapse: collapse; }}
        th, td {{ border: 1px solid #999; padding: 6px 40px; }}
        th {{ background: #eee; }}
      </style>
    </head>
    <body>
      <h1>🚀 AWS EC2 고객관리 최종 프로젝트</h1>
      <p>현재 고정 IP(Elastic IP)를 통해 성공적으로 서버에 연결되었습니다.</p>
      <table>
        <tr><th>고객명</th><th>연락처</th><th>등급</th></tr>
        {rows}
      </table>
    </body>
    </html>
    """
  

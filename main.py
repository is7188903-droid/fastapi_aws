from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import sqlite3
import html
from pathlib import Path

app = FastAPI()
DB = Path(__file__).parent / "customers.db"

def connect():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

with connect() as db:
    db.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, phone TEXT, email TEXT, memo TEXT
    )""")

def page(content):
    return HTMLResponse("""<!doctype html><html lang="ko"><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>고객관리</title><style>
    body{font:16px Arial;max-width:900px;margin:30px auto;padding:0 16px;background:#f4f6fa}
    h1{color:#2457a7}form,.box{background:white;padding:14px;margin:12px 0;border-radius:8px}
    input,button{font:inherit;padding:9px;margin:4px;border:1px solid #ccc;border-radius:5px}
    button{background:#2457a7;color:white;cursor:pointer}table{width:100%;background:white;border-collapse:collapse}
    th,td{padding:9px;border-bottom:1px solid #ddd;text-align:left}
    </style><body><h1>고객관리</h1>""" + content + "</body></html>")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    q = request.query_params.get("q", "").strip()
    with connect() as db:
        rows = db.execute(
            "SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ? ORDER BY id DESC" if q else
            "SELECT * FROM customers ORDER BY id DESC",
            (f"%{q}%", f"%{q}%") if q else ()
        ).fetchall()
    items = ""
    for r in rows:
        items += ("<tr><td>" + str(r["id"]) + "</td><td>" + html.escape(r["name"]) +
            "</td><td>" + html.escape(r["phone"] or "") + "</td><td>" +
            html.escape(r["email"] or "") + "</td><td>" + html.escape(r["memo"] or "") +
            f"</td><td><a href='/edit/{r['id']}'>수정</a> " +
            f"<form style='display:inline;padding:0' method='post' action='/delete/{r['id']}'>" +
            "<button>삭제</button></form></td></tr>")
    return page(f"""<form method="post" action="/add"><b>고객 등록</b><br>
    이름* <input name="name" required> 전화번호 <input name="phone">
    이메일 <input name="email"> 메모 <input name="memo"><button>등록</button></form>
    <form method="get">검색 <input name="q" value="{html.escape(q)}" placeholder="이름 또는 전화번호">
    <button>검색</button> <a href="/">전체 보기</a></form><div class="box">고객 {len(rows)}명</div>
    <table><tr><th>번호</th><th>이름</th><th>전화번호</th><th>이메일</th><th>메모</th><th>관리</th></tr>
    {items}</table>""")

@app.post("/add")
async def add(request: Request):
    f = await request.form()
    name = str(f.get("name", "")).strip()
    if name:
        with connect() as db:
            db.execute("INSERT INTO customers(name,phone,email,memo) VALUES(?,?,?,?)",
                       (name, f.get("phone", ""), f.get("email", ""), f.get("memo", "")))
    return RedirectResponse("/", status_code=303)

@app.get("/edit/{cid}", response_class=HTMLResponse)
async def edit_page(cid: int):
    with connect() as db:
        r = db.execute("SELECT * FROM customers WHERE id=?", (cid,)).fetchone()
    if not r: return RedirectResponse("/", status_code=303)
    return page(f"""<form method="post"><h2>고객 정보 수정</h2>
    이름 <input name="name" required value="{html.escape(r['name'])}">
    전화번호 <input name="phone" value="{html.escape(r['phone'] or '')}">
    이메일 <input name="email" value="{html.escape(r['email'] or '')}">
    메모 <input name="memo" value="{html.escape(r['memo'] or '')}">
    <button>저장</button> <a href="/">돌아가기</a></form>""")

@app.post("/edit/{cid}")
async def edit_customer(cid: int, request: Request):
    f = await request.form()
    with connect() as db:
        db.execute("UPDATE customers SET name=?,phone=?,email=?,memo=? WHERE id=?",
                   (f.get("name", ""), f.get("phone", ""), f.get("email", ""), f.get("memo", ""), cid))
    return RedirectResponse("/", status_code=303)

@app.post("/delete/{cid}")
async def delete_customer(cid: int):
    with connect() as db:
        db.execute("DELETE FROM customers WHERE id=?", (cid,))
    return RedirectResponse("/", status_code=303)

"""
Backup toàn bộ Notion workspace sang JSON, commit vào repo này.
Yêu cầu env vars: NOTION_TOKEN
Chạy với: python backup/backup_notion.py
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
OUTPUT_DIR = Path(__file__).parent / "data" / "notion"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def api_get(path: str) -> dict:
    url = f"https://api.notion.com/v1{path}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def api_post(path: str, body: dict) -> dict:
    url = f"https://api.notion.com/v1{path}"
    payload = json.dumps(body).encode()
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def get_all_pages() -> list[dict]:
    """Lấy tất cả pages từ workspace qua Search API."""
    pages, cursor = [], None
    while True:
        body: dict = {"page_size": 100, "filter": {"value": "page", "property": "object"}}
        if cursor:
            body["start_cursor"] = cursor
        result = api_post("/search", body)
        pages.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return pages


def get_page_content(page_id: str) -> list[dict]:
    """Lấy block children của một page."""
    blocks, cursor = [], None
    while True:
        path = f"/blocks/{page_id}/children?page_size=100"
        if cursor:
            path += f"&start_cursor={urllib.parse.quote(cursor)}"
        result = api_get(path)
        blocks.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return blocks


def get_all_databases() -> list[dict]:
    """Lấy tất cả databases."""
    dbs, cursor = [], None
    while True:
        body: dict = {"page_size": 100, "filter": {"value": "database", "property": "object"}}
        if cursor:
            body["start_cursor"] = cursor
        result = api_post("/search", body)
        dbs.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return dbs


def get_database_rows(db_id: str) -> list[dict]:
    """Lấy tất cả rows của một database."""
    rows, cursor = [], None
    while True:
        body: dict = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        result = api_post(f"/databases/{db_id}/query", body)
        rows.extend(result.get("results", []))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
    return rows


def save_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    base = OUTPUT_DIR / timestamp
    print(f"💾 Bắt đầu backup Notion → {base}")

    # Backup pages
    pages = get_all_pages()
    save_json(base / "pages_index.json", pages)
    print(f"  📄 {len(pages)} pages")

    for page in pages:
        pid = page["id"].replace("-", "")
        title_parts = page.get("properties", {}).get("title", {}).get("title", [])
        title = title_parts[0]["plain_text"] if title_parts else pid
        try:
            blocks = get_page_content(page["id"])
            save_json(base / "pages" / f"{pid}.json", {"meta": page, "blocks": blocks})
        except Exception as e:
            print(f"    ⚠️ Bỏ qua page '{title}': {e}")

    # Backup databases
    databases = get_all_databases()
    save_json(base / "databases_index.json", databases)
    print(f"  🗃️  {len(databases)} databases")

    for db in databases:
        did = db["id"].replace("-", "")
        try:
            rows = get_database_rows(db["id"])
            save_json(base / "databases" / f"{did}.json", {"meta": db, "rows": rows})
        except Exception as e:
            print(f"    ⚠️ Bỏ qua DB '{did}': {e}")

    print(f"\n✅ Backup xong: {base}")


if __name__ == "__main__":
    main()

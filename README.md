# GitHub Actions Automation

Hai workflow tự động chạy hoàn toàn miễn phí trên GitHub Actions.

---

## 1. Daily Morning Report (`notifier/`)

Gửi báo cáo sáng qua **Telegram** lúc **9:00 AM GMT+7** mỗi ngày, bao gồm:
- 🌤 Thời tiết (wttr.in — không cần key)
- 💰 Giá vàng XAU/USD + quy đổi VNĐ/chỉ (cần `GOLD_API_KEY` — miễn phí tại goldapi.io)
- 📈 Giá cổ phiếu VN: VNM, FPT, VIC (SSI iBoard — không cần key)

### Cách thiết lập

**Bước 1 — Tạo bot Telegram:**
1. Nhắn `/newbot` cho [@BotFather](https://t.me/BotFather), lấy `BOT_TOKEN`
2. Nhắn bất kỳ gì cho bot vừa tạo, rồi truy cập:
   `https://api.telegram.org/bot<TOKEN>/getUpdates`
   → lấy `chat.id` từ JSON trả về

**Bước 2 — Thêm Secrets vào repo:**

| Secret | Giá trị |
|--------|---------|
| `TELEGRAM_BOT_TOKEN` | Token từ BotFather |
| `TELEGRAM_CHAT_ID` | chat_id của bạn |
| `GOLD_API_KEY` | (tuỳ chọn) key từ goldapi.io |

**Bước 3 — Tuỳ chỉnh (Variables, không phải Secrets):**

| Variable | Default |
|----------|---------|
| `WEATHER_CITY` | `Ho Chi Minh City` |
| `STOCK_SYMBOLS` | `VNM,FPT,VIC` |
| `USD_VND_RATE` | `25000` |

**Settings → Secrets and variables → Actions**

**Bước 4 — Chạy thử ngay:**
Actions tab → *Daily Morning Report* → *Run workflow*

---

## 2. Notion Backup (`backup/`)

Backup toàn bộ workspace Notion (pages + databases) sang JSON, tự động commit về repo lúc **1:00 AM GMT+7** mỗi đêm.

Dữ liệu lưu tại `backup/data/notion/YYYY-MM-DD/` (được `.gitignore` loại trừ khỏi repo chính, chỉ commit khi workflow chạy).

### Cách thiết lập

**Bước 1 — Tạo Notion Integration:**
1. Vào [notion.so/my-integrations](https://www.notion.so/my-integrations) → *New integration*
2. Chọn workspace, lấy **Internal Integration Token**
3. Vào từng page/database → *...* → *Add connections* → chọn integration vừa tạo

**Bước 2 — Thêm Secret:**

| Secret | Giá trị |
|--------|---------|
| `NOTION_TOKEN` | Token từ Notion integration |
| `GH_PAT` | (tuỳ chọn) Personal Access Token nếu repo có branch protection |

**Bước 3 — Chạy thử:**
Actions tab → *Notion Backup* → *Run workflow*

---

## Cấu trúc thư mục

```
.
├── .github/workflows/
│   ├── daily-report.yml      # Workflow gửi báo cáo sáng
│   └── backup-notion.yml     # Workflow backup Notion
├── notifier/
│   └── daily_report.py       # Script cào dữ liệu + gửi Telegram
└── backup/
    ├── backup_notion.py       # Script backup Notion API
    └── data/notion/           # Dữ liệu backup (bị gitignore)
```

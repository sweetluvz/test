"""
Cào dữ liệu thời tiết + giá vàng + chứng khoán VN, gửi Telegram mỗi sáng.
Yêu cầu env vars: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Tuỳ chỉnh
CITY = os.getenv("WEATHER_CITY", "Ho Chi Minh City")
STOCK_SYMBOLS = os.getenv("STOCK_SYMBOLS", "VNM,FPT,VIC").split(",")


def fetch(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def get_weather() -> str:
    encoded = urllib.parse.quote(CITY)
    url = f"https://wttr.in/{encoded}?format=j1"
    try:
        data = fetch(url)
        cur = data["current_condition"][0]
        temp = cur["temp_C"]
        feels = cur["FeelsLikeC"]
        desc = cur["weatherDesc"][0]["value"]
        humidity = cur["humidity"]
        return (
            f"🌤 *Thời tiết {CITY}*\n"
            f"  Nhiệt độ: {temp}°C (cảm giác {feels}°C)\n"
            f"  Trời: {desc}\n"
            f"  Độ ẩm: {humidity}%"
        )
    except Exception as e:
        return f"⚠️ Không lấy được thời tiết: {e}"


def get_gold_price() -> str:
    # Dùng API công khai của GoldAPI (free tier, key lấy tại goldapi.io)
    # Nếu không có key thì hiện giá USD/oz từ metals-api
    api_key = os.getenv("GOLD_API_KEY", "")
    if api_key:
        url = "https://www.goldapi.io/api/XAU/USD"
        try:
            data = fetch(url, headers={"x-access-token": api_key})
            price_usd = data["price"]
            # Quy đổi sang VND xấp xỉ (tỉ giá lấy từ env hoặc mặc định)
            usd_vnd = float(os.getenv("USD_VND_RATE", "25000"))
            price_vnd_per_chi = price_usd / 31.1035 * 3.75 * usd_vnd / 1_000_000
            return (
                f"💰 *Giá vàng*\n"
                f"  XAU/USD: ${price_usd:,.2f}/oz\n"
                f"  ≈ {price_vnd_per_chi:.2f} triệu VNĐ/chỉ (tỉ giá {usd_vnd:,.0f})"
            )
        except Exception as e:
            return f"⚠️ Không lấy được giá vàng: {e}"
    else:
        return "💡 Thêm GOLD_API_KEY vào Secrets để xem giá vàng (miễn phí tại goldapi.io)"


def get_vn_stocks() -> str:
    # SSI data (công khai, không cần key)
    lines = ["📈 *Chứng khoán VN*"]
    url_tpl = "https://iboard-query.ssi.com.vn/v2/stock/ticker/{symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://iboard.ssi.com.vn",
        "Referer": "https://iboard.ssi.com.vn/",
    }
    for symbol in STOCK_SYMBOLS:
        try:
            data = fetch(url_tpl.format(symbol=symbol.strip()), headers=headers)
            item = data.get("data", {})
            price = item.get("lastPrice", "N/A")
            change = item.get("lastVolume", "N/A")
            change_pct = item.get("changePercent", 0)
            arrow = "🟢" if float(change_pct or 0) >= 0 else "🔴"
            lines.append(f"  {arrow} {symbol}: {price:,} ({change_pct:+.2f}%)")
        except Exception:
            lines.append(f"  ⚠️ {symbol}: không lấy được")
    return "\n".join(lines)


def send_telegram(message: str) -> None:
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }).encode()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
    if not result.get("ok"):
        raise RuntimeError(f"Telegram error: {result}")


def main():
    now = datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")
    parts = [
        f"📋 *Báo cáo sáng — {now}*\n",
        get_weather(),
        "",
        get_gold_price(),
        "",
        get_vn_stocks(),
    ]
    message = "\n".join(parts)
    print(message)
    send_telegram(message)
    print("\n✅ Đã gửi Telegram.")


if __name__ == "__main__":
    main()

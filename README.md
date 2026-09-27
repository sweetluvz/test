# Personal Vault — Obsidian + Google Drive

Ghi chú cá nhân đồng bộ miễn phí qua Google Drive, dùng được trên
Windows / macOS / Android / iOS.

---

## Cách hoạt động

```
Obsidian (máy tính / điện thoại)
        ↕  Remotely Save plugin
    Google Drive (15GB miễn phí)
        ↕  tự động
Obsidian (thiết bị khác)
```

Không cần git, không cần terminal. Sync tự động sau mỗi lần lưu file.

---

## Thiết lập lần đầu (15 phút)

### Bước 1 — Tải Obsidian
[obsidian.md/download](https://obsidian.md/download) — có sẵn cho
Windows, macOS, Android, iOS.

### Bước 2 — Mở vault này
- **Máy tính**: mở Obsidian → *Open folder as vault* → chọn thư mục repo này
- **Điện thoại**: mở Obsidian → *Create new vault* (đặt tên bất kỳ) → sau bước 3 sẽ thay bằng dữ liệu thật

### Bước 3 — Cài Remotely Save
1. Obsidian Settings → **Community plugins** → tắt Safe mode
2. Browse → tìm **Remotely Save** → Install → Enable

### Bước 4 — Kết nối Google Drive
1. Settings → Remotely Save → chọn **Google Drive**
2. Nhấn **Auth** → đăng nhập Google → cho phép quyền truy cập
3. Quay lại Obsidian → nhấn **Sync** lần đầu

> Sau bước này mọi thiết bị khác chỉ cần lặp lại Bước 3–4 rồi nhấn Sync
> một lần — toàn bộ notes sẽ tải về tự động.

### Bước 5 — Bật auto-sync (tuỳ chọn)
Settings → Remotely Save:
- **Sync on save**: bật (sync 5 giây sau mỗi lần lưu)
- **Sync on startup**: bật
- **Run once every X minutes**: 10

---

## Cấu trúc thư mục

```
vault/
├── Daily Notes/      ← ghi chú hàng ngày (dùng Calendar plugin)
├── Projects/         ← theo dõi dự án, công việc
├── Resources/        ← tài liệu tham khảo, link, kiến thức
├── Templates/        ← mẫu ghi chú
├── Attachments/      ← ảnh, file đính kèm (tự động)
└── Archive/          ← ghi chú cũ không còn active
```

---

## Plugins đi kèm

| Plugin | Tác dụng |
|--------|----------|
| **Remotely Save** | Sync qua Google Drive |
| **Calendar** | Lịch tháng, tạo Daily Note bằng 1 click |
| **Dataview** | Query ghi chú như database (nâng cao) |
| **Templater** | Tạo note từ template tự động |

Cài tất cả trong: Settings → Community plugins → Browse.

---

## Lưu ý

- **Conflict**: nếu sửa cùng file trên 2 thiết bị lúc offline,
  Remotely Save giữ bản có timestamp mới hơn. Bản cũ lưu vào `.trash/`
  trong 30 ngày.
- **Dung lượng**: Google Drive tính cả ảnh đính kèm. 15GB đủ cho
  hàng chục nghìn trang ghi chú text.
- **Bảo mật**: dữ liệu lưu trên Google Drive của bạn, không qua
  server thứ ba nào.

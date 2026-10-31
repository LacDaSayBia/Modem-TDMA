# M19 — NMS, bảo mật, update và recovery

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Modem cần biết mình chạy phiên bản nào, đang lỗi ở đâu và khôi phục ra sao. NMS hiển thị/quản trị trạng thái; quyền phát RF cuối cùng vẫn nằm ởhardware permit và MAC, time validity.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** vận hành, phát hiện lỗi và phục hồi đúng cấu hình.

**Đầu vào/đầu ra:** counters/config/release/credentials ↔ CLI/SSH/API, alarms, logs, signed update và recovery actions.

**Yêu cầu kỹ thuật:** inventory/version, phân quyền, lưu cấu hình, credential protection, replay defense cho control theo profile, watchdog và rollback. Không ghi correction từng burst xuống flash. Secure boot, firmware authentication và user encryption là phạm vi khác nhau.

**Phương án/chi tiết:** daemon/API/CLI trước UI; counter/gauge schema thống nhất; manifest kiểm board/ABI/FPGA/software trước update; golden recovery image. Dùng thư viện mật mã duy trì, xác định key/nonce lifecycle thay vì tự chế cipher. Tách calibration, provisioning và runtime state; lỗi NMS không được mở TX permit.

**Kiểm chứng/đầu ra bàn giao:** unauthorized action, replay/duplicate, corrupt update/cúp nguồn/rollback, secrets không rò log, watchdog treo userspace; runbook, manifest và recovery test.

**Lộ trình/phụ thuộc:** M5–M10 telemetry; M11–M18 management/security/update; M19–M22 hardening. Embedded/tooling; M03/M16/M17/M20.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M19-REQ-001 | Inventory/version/config | Board/build/ABI/profile/calibration IDs truy vết |
| M19-REQ-002 | Quản trị có phân quyền | Credentials không lọt log, parser/access control có test |
| M19-REQ-003 | Update/recovery an toàn | Manifest/compatibility/verification và rollback có procedure |
| M19-REQ-004 | Telemetry hữu dụng | Counters/gauges, error codes/time frames rõ |
| M19-REQ-005 | Security scope rõ | Control auth, replay, secureboot và payload encryption tách yêu cầu |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Nhận telemetry từ mọi module, xuất CLI/SSH/API và alarms; input config/update bundle đi qua validation. Config schema tách factory calibration/site provisioning/runtime loop state. Kênh NMS không sửa trực tiếp buffer armed hoặc bỏ qua TX inhibit.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Schema và counter policy

Chọn tên units/reset behavior, monotonic timestamps và frame/grant IDs. Queue/FEC/clock/IFL errors có cause thay vì một cờ ERROR chung.

### 5.2. Provisioning/credentials

Network/terminal identity, RF limits, position và secrets có quyền truy cập; không nhúng key thật trong repo/test. Sử dụng thư viện crypto được duy trì, không tự thiết kế mã.

### 5.3. Control security

Quy định message authentication, replay window, nonce/sequence và key lifecycle; tính overhead vào MAC capacity. CRC chỉ kiểm lỗi truyền, không chống giả mạo.

### 5.4. Release/update

Manifest chứa board target, SW/FPGA/ABI, hash/profile/calibration compatibility. Verify trước kích hoạt, để image golden/rollback; mất nguồn không để board vô khả năng recovery.

### 5.5. Watchdog và fault policy

Heartbeat không chỉ tiến timer mà phản ánh health work. Treo app/kernel fault/RF fault không giữ TX enabled; logs được rate-limit và không block đường realtime.

## 6. Ví dụ tính toán hoặc luồng minh họa

Nếu firmware dùng ABI2 nhưng FPGA chỉ ABI1 thì image hợp chữ ký vẫn không tương thích. Phải có compatibility check riêng; version string giống nhau không thay register map/hash. Runtime correction từng burst không ghi xuống flash.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M19-TC-001 | Unauthorized/replay/configbad | Từ chối đúng reason, không lộ secrets |
| M19-TC-002 | Update bị hỏng/cúp nguồn | Golden/rollback recover được, TX mặc định mute |
| M19-TC-003 | Telemetry/fault storm | Counter/log hữu dụng, không làm trễ datapath |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Có AES256chưa chứng minh key/nonce/replay đúng. Web UI không thay authenticated control. Cùng version tên nhưng khác bitstream hash cần phân biệt trong release.

## 10. Bài thực hành nhập môn gắn với mô-đun

Tạo manifest giả gồm board/ABI/profile/hashes không có secrets. Lập3case:hashsai, ABI mismatch, và board target khác; viết policy khi update bị ngắt do mất nguồn.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R18 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Phân biệt bắt buộc/khuyến nghị trong security requirements.
- [R20 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Version public API,không thay hash/buildID/compatibility matrix.
- [R15 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Kernel/driver updates cần version/patch provenance.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

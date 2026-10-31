# M03 — Board SoC/FPGA, nguồn, bộ nhớ và khả năng kiểm tra

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Board không chỉ “nối chip với nhau”. Nó phải cấp nguồn, clock, boot và kiểm tra được ngay cả khi FPGA/software chưa hoạt động đầy đủ. DFT là các đường quan sát/loopback giúp phân biệt lỗi PCB với lỗi logic.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** tạo nền tích hợp có thể bring-up, đo và sửa lỗi.

**Đầu vào/đầu ra:** yêu cầu compute/IO/power/thermal → schematic/layout/BOM, board và manufacturing tests.

**Yêu cầu kỹ thuật:** Ethernet Gigabit, DDR, boot storage, JTAG/console, board ID, power/temperature monitoring; đúng bank voltage/pin/package. Có recovery boot và đường nạp FPGA phụ khi link chưa lên. Mục tiêu nhiệt độ mẫu 0–50 °C và soak 72 giờ cần đo thực tế.

**Phương án/chi tiết:** dùng dev board trước; ưu tiên 7030, xem 7020 theo sizing. Thêm A200T khi M07/M10 có bằng chứng lợi ích. Kiểm rail sequencing, supervisor, decoupling, DDR SI/PI, thermal và clock placement; bố trí testpoint, loopback/PRBS và current measurement. Thực hiện review pin/bank trước layout.

**Kiểm chứng/đầu ra bàn giao:** rail/reset/DDR/Ethernet stress, JTAG recovery, thermal at load; CAD/BOM/Gerber, bring-up guide và DFT checklist. Không phát hành PCB chỉ từ sơ đồ khối.

**Lộ trình/phụ thuộc:** M1–M6 dev board/sizing; M7–M12 PCB vòng 1 sau G1; M15–M18 vòng 2; M19–M21 xác nhận sửa. Hardware; phụ thuộc M01/M05/M07/M10.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M03-REQ-001 | Đúng part/package/pin/bank | Review pin plan, voltage và transceiver accessibility |
| M03-REQ-002 | DDR và boot/recovery ổn định | Memory stress, power cycle và recovery từ image lỗi |
| M03-REQ-003 | Đủ thermal/power ở peak | Đo khi DS10/US3 song công và max decoder iteration |
| M03-REQ-004 | DFT và spare | Console/JTAG/testpoint, PRBS và current measurement có sẵn |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Nhận resource/IO plan từ PHY, FEC, M07 và clock tree. Xuất CAD/BOM/netlist/Gerber, power/reset telemetry, board ID và các interface AD9361/Ethernet/DDR/JTAG. Không tự ghi pad/timing chưa xác nhận thành requirement có bảo đảm.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Bắt đầu bằng dev board

Chạy PoC và đo tài nguyên trước custom PCB; ghi chính xác mã FPGA, package, speed grade, IO banks và tool license.

### 5.2. Lập pin/power matrix

Tách MIO/EMIO/PL, DDR banks, LVDS và reference clock pins. Kiểm điện áp hai đầu, termination và boot straps; sơ đồ khối không thay pin map.

### 5.3. Thiết kế nguồn và reset

Tính từng rail theo load worst case và startup; kiểm sequencing, decoupling, voltage monitor/reset supervisor. Dự phòng điểm đo điện áp/dòng và tách RF noise paths.

### 5.4. Review SI/PI và layout

Kiểm DDR routing, differential skew, return path, clock isolation, thermal copper và connector escape. Dùng review checklist trước release fabrication; không chờ bring-up mới tìm bank conflict.

### 5.5. Bring-up hai vòng

Vòng 1 kiểm nguồn/JTAG/boot/DDR/link rồi RF; ghi rework và errata. Vòng 2 xác nhận fixes, DFT/yield và nhiệt; giữ thời gian cho 72h/field.

## 6. Ví dụ tính toán hoặc luồng minh họa

Nếu raw I/Q hai chiều cần 245,76 MB/s payload, DDR traffic có thể lớn hơn do write/read/trace cạnh tranh. RAM dung lượng 1 GB không tự chứng minh bandwidth đủ. Cần đo traffic thật với DMA và decoder buffers.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M03-TC-001 | Power-cycle nhiều lần | Boot/config/reset nhất quán và default TX mute |
| M03-TC-002 | DDR + Ethernet + PHY load | Không corruption/thermal reset; throughput đạt valid config |
| M03-TC-003 | DFT recovery khi link phụ tắt | Vẫn nạp/quan sát được từng chip |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Lấy tổng DSP để khẳng định fit hoặc quên package không đưa GTX ra chân là lỗi kiến trúc. Thiếu JTAG/console trên board cuối làm debug tốn nhiều tuần. Không gộp dòng BUC vào rail modem khi chưa tính cable/startup.

## 10. Bài thực hành nhập môn gắn với mô-đun

Lập spreadsheet thủ công hoặc bảng Markdown của 10 nhóm tín hiệu: owner, voltage, clock, pin bank và phép thử. Tìm ít nhất một đường phải quan sát được khi Linux chưa boot.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R08 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Tra resource và package tables, không chỉ tên Zynq.
- [R09 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Theo methodology board/clock/constraints và verification.
- [R04 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đối chiếu AD9361 power/interface electrical limits.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

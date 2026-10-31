# M06 — AD9361 interface, điều khiển và luồng sample

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Mô-đun này là cầu nối sample giữa AD9361 và phần PHY tự thiết kế. Nó có thể trao đổi I/Q đúng mà vẫn chưa có DVB-S2/MF-TDMA. Đường SPI điều khiển khác đường sample tốc độ cao.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** trao đổi I/Q liên tục và cấu hình RF tin cậy.

**Đầu vào/đầu ra:** LVDS/CMOS + SPI/control ↔ I/Q stream có sample-valid, status và diagnostic capture.

**Yêu cầu kỹ thuật:** chọn mode FDD và port/rate chain hợp lệ; đúng I/Q order, sign, channel packing và bit width; FIFO/CDC rõ. Không dừng được RF sampling chỉ vì downstream AXI ready hạ. Reset/calibration không được bất ngờ xảy ra trong traffic.

**Phương án/chi tiết:** tái sử dụng ADI `axi_ad9361` và design nền [S4–S5] theo release đã khóa. Bring-up SPI → PN/LVDS → DDS/capture → external loopback → FDD. Giữ stream trong PL cho đường modem, raw I/Q DMA chỉ để debug/capture có arbitration. Lưu config/filter version vì group delay phụ thuộc cấu hình.

**Kiểm chứng/đầu ra bàn giao:** PN/pattern pass, I/Q integrity, không mất sample ở valid rate, reset/recovery được; ILA và captures xác minh interface. Source/config và hướng dẫn bring-up.

**Lộ trình/phụ thuộc:** M1–M4 nền; M5–M8 ổn định; M9–M18 tích hợp board. FPGA/embedded; cần M03/M05/M17.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M06-REQ-001 | Đúng I/Q/sign/packing | Pattern và PN không lỗi tại valid rate |
| M06-REQ-002 | Sample liên tục/FDD | Không mất sample khi AXI consumer stall trong giới hạn FIFO |
| M06-REQ-003 | Calibration/config có version | Không đổi filters/reset giữa burst không kiểm soát |
| M06-REQ-004 | Tách debug raw I/Q khỏi runtime | Có arbitration, overflow counters và capture policy |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Input LVDS/control/SPI và stream TX; output RX I/Q với sample index/config marker, link/PN/overflow status. Interface với M17 cho RF config và DMA debug; với M09/M12/M13 cho stream vận hành. Không mặc định port của IP là AXI-stream nếu release dùng FIFO-style signals.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Khóa release nền

Lấy ADI HDL/Linux hoặc no-OS tương thích board; ghi branch/tag/commit và Vivado version, tránh ghép DT/regmap ngẫu nhiên.

### 5.2. Bring-up có thứ tự

Read SPI ID/settings, clocks, PN/LVDS timing tune, DDS loopback, external RX capture rồi FDD. Lưu captures và error counters mỗi bước.

### 5.3. Chuẩn hóa stream

Chốt signed12-bit từ chip, mở rộng/packing16-bit khi cần; I đi trước Q, chỉ chọn một convention. Tag sample gaps và reset events để receiver biết mất continuity.

### 5.4. Lập buffer/CDC policy

ADC không chờ downstream ready. FIFO theo max stall và speed; overflow làm báo fault/reacquire theo path, không ghi đè âm thầm. TX underflow dẫn mute/abort rõ.

### 5.5. Đo latency/config changes

Kiểm maxrate mới trên board; calibration gắn clock/filter cfg. Config commit chỉ ngoài burst và thay đổi schedule epoch khi cần, re-calibrate latency sau reset.

## 6. Ví dụ tính toán hoặc luồng minh họa

30,72 MS/s × I/Q16 cần122,88 MB/s một chiều. Capture100 ms chiếm 12,288 MB; không stream toàn bộ qua100M Ethernet rồi kết luận DMA yếu. Debug decimation/capture window khác luồng runtime giữ trongPL.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M06-TC-001 | PN và sample-pattern | Không bit/order errors tại clocks được hỗ trợ |
| M06-TC-002 | Backpressure/overflow | Không silent corruption; gap/status đúng |
| M06-TC-003 | Reset/filter change | Latency/config ID thay có kiểm soát, TX default mute |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

TX DDS chạy không chứng minh RX DMA/IRQ đúng. SPI đọc được không chứng minh LVDS capture đúng. IIO read timeout có thể từ IRQ/DT/clock, phải kiểm từng lớp và phối hợp M17.

## 10. Bài thực hành nhập môn gắn với mô-đun

Thu một tone mức an toàn, plot spectrum và kiểm I/Q sign/order bằng model. Đổi cố ý I/Q trong file replay để thấy spectrum bị mirror; không thay hardware tùy tiện khi chưa biết lỗi thuộc lớp nào.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R06 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc port semantics, regmap và configs đúng version.
- [R05 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Dùng reference bring-up, không coi làm sẵn modem.
- [R16 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Phân lập RF init bằng no-OS khi debug Linux bị nhiễu.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

# M05 — Clock vật lý, reference và reset

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Clock vật lý là nhịp lấy mẫu/chạy logic; thời gian mạng là ý nghĩa một counter ở M14. Một clock đúng tần số chưa biết epoch; hai thiết bị có PPS vẫn cần đo delay nội bộ và propagation.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** cung cấp clock ổn định và startup/reset nhất quán.

**Đầu vào/đầu ra:** TCXO/OCXO hoặc reference ngoài → clocks cho AD9361, PL/FPGA và trạng thái reference-valid/reset.

**Yêu cầu kỹ thuật:** frequency stability và phase noise phù hợp; reset release đồng bộ theo domain, phát hiện mất clock. HUB có ngõ reference 10 MHz; VSAT khuyến nghị reference/PPS để thử. Không mặc định cấp trực tiếp 10 MHz vào mọi clock input.

**Phương án/chi tiết:** clock tree dựa [S3–S4]; chọn sample rate dùng chung hợp lệ cho hai chiều, DDC/DUC tạo rate cần thiết. Lập clock-domain map, clock/reset constraints, oscillator drift budget; dùng MMCM/PLL/clock synthesizer đúng dải. Sync mất reference dẫn tới logic holdover của M14, không tự giữ TX permit vô hạn.

**Kiểm chứng/đầu ra bàn giao:** đo frequency/drift/jitter/lock và reset nhiều lần; kiểm valid signals và không có metastability/reset violation chưa xử lý. Clock plan, constraints và báo cáo calibration.

**Lộ trình/phụ thuộc:** M1–M4 plan/PoC; M5–M9 clock độc lập; M10–M18 đo theo nhiệt/config. Hardware/FPGA; liên quan M03/M06/M14.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M05-REQ-001 | Clock tree hợp lệ FDD | RX/TX rate chain và AD9361 FIR/interface được kiểm |
| M05-REQ-002 | CDC/reset an toàn | Không multi-bit sync tùy tiện; report_cdc được review |
| M05-REQ-003 | Reference-valid và holdover interface | Clock loss không giữ TX permission vô hạn |
| M05-REQ-004 | Phase noise/drift budget | Đo tần số/nhiệt/clock source thay vì chỉ resolution |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Input TCXO/OCXO/10MHz/PPS tùy cấu hình; output physical clocks, domain resets, PLL lock/reference-valid và frequency estimate. M14 nhận các trạng thái này nhưng tự giữ network-time validity; không dùng lock của MMCM như bằng chứng đã sync mạng.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Lập clock-domain map

Liệt kê sample, fabric, AXI, DDR, serial và network counter timebase; ghi nguồn/tỷ số/reset/đường crossing. Chọn 30,72 MS/s chỉ sau kiểm filter/rate plan.

### 5.2. Rà soát rate không nguyên

12,5 Msym/s ở 30,72 MS/s là2,4576samples/symbol. Dùng interpolator/resampler và phase accumulator; không divide integer sai để ép rate.

### 5.3. Thiết kế reset

Assertion an toàn theo yêu cầu domain, deassertion đồng bộ; reset consumers sau clock stable. Dữ liệu/descriptor cũ bị invalid khi reset epoch.

### 5.4. Constraints và CDC

Định nghĩa clocks/generated clocks, uncertainties và I/O delays đúng. False path chỉ cho crossing đã có synchronization; dùng async FIFO/handshake/XPM được kiểm, không blanket waiver.

### 5.5. Đo và kiểm mất reference

Sweep nhiệt/nguồn/reference modes; đo drift/phase noise và reset repeatability. Clock fault tới M14/M19 trong thời gian bounded; chọn holdover theo uncertainty thực.

## 6. Ví dụ tính toán hoặc luồng minh họa

1 ppm residual drift trong100 ms gây100 ns lỗi. Upstream5 Msym/s mục tiêu timing50 ns nên drift riêng100 ns đã vượt budget; cần clock discipline tốt hơn hoặc update/holdover ngắn hơn, cùng calibration. Đây là lý do maxrate mới ảnh hưởng M05/M14/M15.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M05-TC-001 | Reset/reference switch | Không glitch gây phát ngoài lịch, epoch/counters xử lý đúng |
| M05-TC-002 | CDC review | Không critical crossing chưa có disposition |
| M05-TC-003 | Clock drift sweep | Có measurement và holdover bound theo maxrate |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Lấy accuracy 10MHz ngoài làm accuracy launch RF là nhầm. Clock chung cho mọi VSAT giúp debug nhưng che lỗi network sync. Dùng false_path để hết timing warning không thay mạch CDC đúng.

## 10. Bài thực hành nhập môn gắn với mô-đun

Vẽ ba miền clock và phân loại một single-bit status, một event pulse và một bus timestamp; chọn crossing mechanism từng loại và giải thích vì sao hai flipflop không đủ cho cả bus.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R09 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc CDC/constraints và review report, không dùng waiver để bỏ lỗi.
- [R04 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc clock/reference limits của chip.
- [R05 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Xem clock tree reference và configurations theo release.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

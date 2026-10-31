# M13 — Bộ thu burst đa carrier tại HUB

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

HUB phải nghe nhiều trạm ở các carrier cùng lúc. Mỗi burst có pha, tần số lệch, timing và mức công suất riêng; receiver liên tục bám một carrier không tự thành burst receiver đa người dùng.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** thu đồng thời burst từ các VSAT có timing, CFO, phase và power khác nhau.

**Đầu vào/đầu ra:** wideband I/Q + schedule hints → payload từng burst và đo arrival/CFO/quality.

**Yêu cầu kỹ thuật:** ít nhất 2 carrier đồng thời, 3 VSAT, detector không nhận nhầm identity; timestamp quy về cùng reference plane; không tái dùng mù phase/AGC của trạm trước. Carrier gain không được làm ADC clipping vì near-far.

**Phương án/chi tiết:** fixed wideband gain hợp lý → bank DDC/decimation → UW correlation → data-aided CFO/timing/phase → matched filter/soft demap → M11 → CRC/reassembly. Dành search window rộng cho logon và hẹp cho traffic; prior estimates theo terminal có expiry. Khi dynamic range không đủ phải điều chỉnh RF/phân receiver.

**Kiểm chứng/đầu ra bàn giao:** simultaneous captures/decoded streams; probability of detection/false alarm, near-far/blocker, back-to-back decoder load, fractional timing bias calibration. Model/RTL/host source và burst reports.

**Lộ trình/phụ thuộc:** M3–M6 một carrier; M7–M12 hai carrier/FEC; M13–M16 near-far/load; M17–M20 hardware final. DSP/FPGA; M02/M06/M11/M14.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M13-REQ-001 | Hai carrier đồng thời | Burst chồng thời gian được giải mã độc lập |
| M13-REQ-002 | Tải peak | Mục tiêu 3 Mbit/s/carrier và 6 Mbit/s tổng |
| M13-REQ-003 | Arrival metadata tin cậy | Reference point/fractional estimator bias và quality được calibration |
| M13-REQ-004 | Near-far và identity | Không gán số đo unknown burst sang nhầm terminal |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Input wideband samples và expected schedule hints. Output payload/CRC/FEC per burst, carrier ID, terminal/grant ID khi xác minh được, arrival timestamp, CFO/phase/quality và overflow status. Cho phép logon chưa biết identity vào path riêng, không dùng để sửa terminal bất kỳ.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Frequency plan và channelization

Với hai carrier dùng bank DDC dễ kiểm hơn PFB lớn; chọn spacing/filters theo occupied bandwidth và transition bands, kiểm DC/alias. Không giả định hai RX AD9361 có LO độc lập.

### 5.2. Gain/dynamic range

Giữ analog gain không chạy theo một burst phá carrier còn lại; digital normalize từng burst. Đo clipping/near-far; nếu không đủ cần phân băng hoặc receiver bổ sung.

### 5.3. Detect và acquisition

Energy gate có thể hỗ trợ nhưng UW correlation xác định burst; window rộng cho logon, hẹp cho traffic. Data-aided CFO/fractional timing/phase từ known symbols và quality score.

### 5.4. Demap/FEC/reassembly

Filter/tracking theo burst, sinh LLR đúng scale; M11 decoder đủ backlog hai carrier. Payload có CRC và fragment handling, bad burst không giao lên IP.

### 5.5. Calibrate metadata

Quy peak correlation về điểm chuẩn RF, trừ filter/channelizer delay. Lưu bias theo profile/rate và threshold; report arrival trước decoder latency biến thiên.

## 6. Ví dụ tính toán hoặc luồng minh họa

Hai burst đến cùng lúc trên hai carrier: channelizer/receiver đều phải hoạt động; tune RX carrier A rồi B sẽ bỏ lỡ một burst. Nếu mỗi carrier 5 Msym/s thì tổng payload ideal 10 Mbit/s trước overhead, mục tiêu IP aggregate6 cần cả PHY/FEC/MAC cùng đủ.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M13-TC-001 | Simultaneous dual-carrier | Hai payload đúng, không dùng tune tuần tự |
| M13-TC-002 | Near-far/blocker sweep | FER/detection/ADC clipping được báo theo mức |
| M13-TC-003 | Known fractional arrival | Bias/error bound xác nhận và giữ đúng ID |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Mang PLL/AGC state trạm A sang B làm acquisition chậm. Lấy completion DMA timestamp làm arrival đo sai theo queue. Unknown/collision burst không được dùng để điều khiển công suất một trạm đã biết.

## 10. Bài thực hành nhập môn gắn với mô-đun

Tạo hai QPSK burst ở hai offset tần số trong cùng IQ stream, cộng chúng và chạy hai DDC. Thay công suất một burst để xem ảnh hưởng clipping; tách lỗi ADC khỏi lỗi decoder.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Return burst và tài nguyên MF-TDMA.
- [R04 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): RF dynamic range/levels theo điều kiện chip.
- [R03 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Tham khảo receiver/system trade-offs; phương án bank DDC là lựa chọn dự án.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

# M14 — Network time, hardware timestamp và timed TX

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Counter phần cứng cho biết một sự kiện xảy ra ở sample nào; network time cho biết sample đó tương ứng mốc mạng nào. Timed TX phải liên kết cả hai và có calibration tới connector RF.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** nối timeline mạng với sự kiện sample/RF một cách xác định.

**Đầu vào/đầu ra:** PHY marker/reference, calibrated delay và descriptor → local network-time estimate, timestamp records, timed launch và TX permit.

**Yêu cầu kỹ thuật:** counter monotonic, integer/fractional precision phù hợp, epoch/wrap-safe, CDC đúng; timestamp trước latency FEC biến thiên; correction không làm phát descriptor hai lần. Linux chỉ nạp sớm; PL tự kiểm deadline và đóng TX.

**Phương án/chi tiết:** HUB đánh số marker và association reference; VSAT lưu sample event theo frame ID trước FEC, sau decode ghép reference để bám offset/rate bằng accumulator/DPLL. State UNLOCKED/ACQUIRE/LOCKED/HOLDOVER/UNSYNC. Double-buffer schedule, atomic commit; launch theo counter sau trừ latency calibration. Mất clock/grant/config/IFL permit dẫn mute.

**Kiểm chứng/đầu ra bàn giao:** test epoch/wrap, late/duplicate, reset, backpressure; đo RF jitter/latency khác với timestamp resolution; drift/holdover sweep. Time ICD, RTL và calibration tables.

**Lộ trình/phụ thuộc:** M2–M5 engine/PoC; M6–M9 clock độc lập; M10–M16 calibration/robustness. FPGA/system; M05/M06/M08/M09/M12/M13.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M14-REQ-001 | Time monotonic và epoch | Không jump ngược gây phát lại grant |
| M14-REQ-002 | Reference association trước FEC | Marker/frame ID ghép đúng giá trị reference giải mã sau |
| M14-REQ-003 | Launch/maxrate accuracy | Mục tiêu arrival50 ns tại 5 Msym/s phải PoC, không suy từ counter resolution |
| M14-REQ-004 | Fail-safe TX permit | Mất clock/grant/RF hoặc config mismatch dẫn mute |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Input physical clock status M05, PHY markers M08/M09, correction/config M15/M16, tx_descriptor M12. Output time_estimate/quality, timestamp records, launch event, inhibit và completions. Counter owner nằm sát RF tại Zynq PL theo phương án cơ sở.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Định nghĩa time ABI

Dùng local 64-bit sample counter cộng fractional position; epoch_id riêng cho timeline. Mapping network_time=a×sample_index+b được cập nhật có giới hạn, không dùng wall clock để launch.

### 5.2. Capture markers

Timestamp reference marker trước FEC; ring giữ frame ID và sample index. Khi control payload giải mã xong ghép đúng entry; unknown/stale markers bỏ có counter, không ghép nearest tùy tiện.

### 5.3. Bám offset/rate

DPLL/estimator tách drift và offset, quality tăng dần sau nhiều reference. HOLDOVER có uncertainty tăng theo drift; quá budget tự UNSYNC/mute.

### 5.4. Execute timed TX

Descriptor accepted→armed→launched→completed; double-buffer schedule commit ở epoch. Compare time wrap-safe trong cửa sổ bounded; late/duplicate/config mismatch reject.

### 5.5. Calibrate RF latency

Đo từ launch API tới RF preamble point theo rate/filter/reset. Nếu timestamp sample 32,55 ns thì accuracy50 ns còn rất ít budget cho estimator/drift; fractional delay và board stability phải chứng minh.

## 6. Ví dụ tính toán hoặc luồng minh họa

Nếu local clock đã biểu diễn network time đúng, launch=A−dR−LTX. Nếu thời gian chỉ đếm từ reference nhận trễ thì wait=A−H0−dF−dR−LTX. Trừ dF hai lần làm phát sớm sai; bỏ dF khi dùng delayed reference làm arrival trễ. ICD phải chọn rõ convention.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M14-TC-001 | Clock độc lập + drift | Reference mapping ổn, holdover uncertainty bounded |
| M14-TC-002 | Epoch/reset/wrap/late | Không phát lại hoặc phát ngoài grant |
| M14-TC-003 | RF timing calibration | Phân biệt resolution, jitter và accuracy; target50 ns có evidence |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Timestamp lúc application nhận gói bao gồm FEC/queue jitter. Counter tick5 ns không có nghĩa RF accuracy5 ns. Tăng/giảm clock estimate giữa burst không kiểm soát có thể làm sai symbol rate.

## 10. Bài thực hành nhập môn gắn với mô-đun

Mô phỏng sample counter, một reference nhận sau240 ms và desired arrival1s. Tính launch ở hai hệ quy chiếu rồi kiểm cho cùng kết quả. Chèn reset epoch và chứng minh descriptor cũ bị reject.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Tham khảo network timing/signalling convention, không thay bằng công thức riêng khi tuyên bố RCS2.
- [R09 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): CDC timestamp/event và reset.
- [R19 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Serial arithmetic cho counter hữu hạn cần cửa sổ dưới nửa miền.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

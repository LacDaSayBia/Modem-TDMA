# M07 — Giao tiếp liên FPGA

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Liên FPGA là đường vận chuyển có lỗi/flow control/reset như một liên kết riêng. Thêm chip tăng tài nguyên nhưng không giúp nếu dữ liệu qua link bị nghẽn hoặc timestamp bị hiểu sai.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** mở rộng FEC/PHY mà không tạo bottleneck hay phá timing.

**Đầu vào/đầu ra:** stream I/Q hoặc LLR/codeblock + metadata ↔ payload/result, credits và link status.

**Yêu cầu kỹ thuật:** throughput đủ worst case, CRC/sequence/config version, backpressure và reset recovery. Có link epoch chống dùng dữ liệu trước reset. Không để arrival của packet trên link biến thiên quyết định mốc RF launch.

**Phương án/chi tiết:** với 7030, khảo sát GTX↔GTP/Aurora hoặc serial protocol có cấu hình tương thích hai đầu; 7020 dùng SelectIO source-synchronous phù hợp [S7]. Thử LLR boundary để giảm traffic so raw I/Q. PRBS/training, frame types, credits, async FIFO và error counters. Không coi GTX maximum là tốc độ hai chip/PCB đã đạt.

**Kiểm chứng/đầu ra bàn giao:** payload bandwidth, max stall/latency, bit/packet errors, reset/retraining ở tải/nhiệt; protocol spec, constraints và loopback fixture. Nếu không cần FPGA phụ, ghi module không áp dụng ở cấu hình đó.

**Lộ trình/phụ thuộc:** M2–M4 PoC và partition gate; M5–M8 tích hợp; M9–M18 board verification. FPGA; cần M01/M03/M10.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M07-REQ-001 | Target/package hỗ trợ link | 7030 GTX khác7020 SelectIO; kiểm hai đầu |
| M07-REQ-002 | Bandwidth/latency worst case | LLR envelope150 Mbit/s downstream hoặc raw IQ theo partition |
| M07-REQ-003 | Integrity và credits | CRC, sequence, frame length, epoch và flow control |
| M07-REQ-004 | Timed TX không phụ thuộc jitter link | Waveform trả đủ sớm; launch ở owner gần RF |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Các frame types: CONFIG/LLR_FRAME/DECODE_RESULT/DIAGNOSTIC/CREDIT; mỗi frame có length, stream/frame ID, config ID, link epoch và CRC. Control/status không bị dữ liệu dài starve. Return payload giữ frame ID để ghép đúng timestamp trước FEC.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. So hai partition

OptionA Zynq synchronizer→LLR→FPGA decoder; optionB rawIQ→PHY FPGA. Tính data rates, buffering/CDC, latency, source reuse và debug mỗi option rồi chọn ADR.

### 5.2. Chọn physical link

7030↔A200T kiểm shared line rate/refclk/IP support GTX/GTP, hoặc SelectIO source-synchronous.7020 không có GTX; không chốt Aurora hard-transceiver kiểu7030 cho 7020.

### 5.3. Định nghĩa transport

Fixed header, max frame, CRC coverage, credits in bytes/frames, sequence reset và resync. Không cho length sai lấy hết DDR/FIFO.

### 5.4. Xây PoC trước PCB

PRBS/raw transport, framed payload, stress full-duplex và reset mỗi đầu. Lưu bit/packet error, max stall và recovery time.

### 5.5. Tích hợp frame semantics

Test LLR frame và decoder completion bị reorder/timeout; config mismatch reject. Link retrain làm invalid descriptors có liên quan, không re-play grant cũ.

## 6. Ví dụ tính toán hoặc luồng minh họa

Một line3,125Gbit/s dùng8b/10b có trần2,5Gbit/s trước headers. Mức rawIQ983 Mbit/s/chiều có thể vừa về average nhưng cần credit/stall margin.150 Mbit/s LLR nhẹ hơn, song memory burstiness/metadata vẫn cần đo.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M07-TC-001 | PRBS + transport CRC | Không unreported error ở test interval, ghi tổng bits/time |
| M07-TC-002 | Stall/full-duplex | Không deadlock, sustained payload đạt budget |
| M07-TC-003 | Reset/retrain | Không frame cũ ghép với epoch mới hoặc duplicate decode |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Chọn bus32bit vì “rộng là nhanh” nhưng quên clock/turnaround là sai. Cặp TX và RX serial riêng mới tạo full-duplex. Nominal GTX rate không phải bandwidth data API đã đạt.

## 10. Bài thực hành nhập môn gắn với mô-đun

Tính bandwidth rawIQ và LLR cho hai partition, rồi thêm20% margin giả định có ghi rõ. Vẽ state machine link DOWN→TRAIN→READY→FAULT và một test reset ở giữa frame.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R08 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Tra transceiver/package đúng part; kiểm IP guide lúc khóa.
- [R09 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): CDC/constraints giữa clock link vàfabric.
- [R06 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Hiểu sample source để chọn partition.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

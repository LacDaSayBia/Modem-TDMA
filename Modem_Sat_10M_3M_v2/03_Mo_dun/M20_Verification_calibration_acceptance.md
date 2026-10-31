# M20 — Tích hợp, calibration và kiểm chứng nghiệm thu

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

M20 là lớp chứng cứ: cho người khác kiểm được thiết bị đạt gì, ở cấu hình nào và còn giới hạn nào. Nó bắt đầu từ test plan tháng1 chứ không đợi cuối dự án kiểm một buổi demo.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** chứng minh toàn bộ chỉ tiêu H/V trên cấu hình bàn giao.

**Đầu vào/đầu ra:** DUT/model/ICD/test cases/lab → calibrated results, incident closure và acceptance package.

**Yêu cầu kỹ thuật:** independent reference, traceable config, PHY/MAC/packet tests tách lớp; đủ 3 VSAT/2 carrier, clock độc lập, GEO delay, FDD/near-far, fault injection và soak. Không dùng một lần live demo để suy availability.

**Phương án/chi tiết:** thiết lập fixture/automation sớm, golden transmit/receive paths; unit→SIL→RTL→IF→impaired IF→GEO→live. Calibration timing/RF theo config và nhiệt/reset; lưu sample/LLR/packet/grant traces. Lab emulator waveform có đủ DDR/bandwidth và đo jitter riêng.

**Kiểm chứng/đầu ra bàn giao:** test plan/pass-fail/raw records, uncertainty/calibration, known limitations, build-from-clean-machine và lặp test bởi người tiếp nhận. Mọi kết quả gắn serial/build/profile/seed.

**Lộ trình/phụ thuộc:** M1 test plan, M4–M12 block/integration, M13–M20 system, M21–M23 live/soak, M24 handover. QA/integration; bao phủ tất cả mô-đun.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M20-REQ-001 | Trace requirements→evidence | MỗiH/V, testID, build/profile và raw result |
| M20-REQ-002 | Independent references | Không chỉ DUT TX↔DUT RX cùng lỗi |
| M20-REQ-003 | Peak/MF/sync/fault coverage | DS10/US3, dual carrier/GEO/clock độc lập/72h |
| M20-REQ-004 | Calibration/uncertainty | Timing/RF/reference plane và validity có procedure |
| M20-REQ-005 | Bàn giao có thể tái lập | Máy sạch build được, lặp được bài thử đại diện |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Nhận SRS/ICD/model/DUT/release, tạo test campaigns, raw captures/results và acceptance matrix. Evidence ID gắn serial, hardware/software/FPGA/profile/calibration hash, procedure version vàUTC cho log người; sample/network time cho sự kiện RF.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. LậpV&Vplan

Chọn review/analysis/simulation/measurement cho từng requirement. Liệt kê lab/fixture/uncertainty/cases/owner, không để các TBD thành PASS.

### 5.2. Tích hợp từng lát cắt

Golden bits→RTL→board PN/DMA→DVB-S2→timed burst→ranging→2 carrier/3 VSAT→IP/QoS. Mỗi bước giữ config/seed để replay và phân lập lỗi.

### 5.3. Thiết kế channel test

Delay/noise/CFO/drift từng chiều/từng trạm, tính DDR/bandwidth nếu trì hoãn raw IQ. Packet delay chỉ kiểm MAC, NCC; waveform timing cần emulator RF/sample có calibration.

### 5.4. Đo cấu hình peak

Đo UDP1500B≥10 phút, song công, aggregate và per terminal; high SNR/loss criterion rõ. FER sweep/timing max error/near-far/spectrum tách bài nhưng cùng support matrix.

### 5.5. Fault/soak/live/transfer

Làm reset/lost grant/reference/IFL/update fault,72hsoak, trình operator và live GEO theo điều kiện. Build máy sạch và lặp tests bởi người nhận; ghi NOT_RUN cho phần chưa thử.

## 6. Ví dụ tính toán hoặc luồng minh họa

Delay300 ms tại 30,72 MS/s, IQ16 cần 36,864 MB mỗi luồng chỉ để lưu mẫu một chiều. Emulator full-duplex đa trạm cần RAM và read/write bandwidth tương ứng; không thể tạo GEO waveform delay bằng vài FIFO BRAM. Số liệu này là sizing, còn jitter fidelity phải đo.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M20-TC-001 | Archive integrity/replay | Checksums/link/module count đúng, seed replay được |
| M20-TC-002 | Acceptance campaign | Peak/MF/timing/QoS/faults có raw data và pass/fail rõ |
| M20-TC-003 | Clean build+handover | Không phụ thuộc máy cá nhân thiếu tài liệu, known limitations rõ |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Không thấy lỗi trong mẫu nhỏ không có nghĩa BER0. Thử thực tế vài giờ không chứng minh 99,9%availability. Common clock trong bài network sync có thể che điểm yếu clock recovery; giữ cho bài debug riêng.

## 10. Bài thực hành nhập môn gắn với mô-đun

Viết testcase cho“VSAT phát đúng khe”:điểm đo, clock độc lập, Ts, error bound, config, thiết bị, rawtrace và failure conditions. Nhờ người khác đọc và lặp lại mà không cần hỏi thêm định dạng.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R01 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Conformancewaveformprofile kiểm độc lập.
- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Timing/resource/burst requirements cần đúng điều kiện chuẩn.
- [R17 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Availability từ model tuyến/dữ liệu phù hợp,không suy từ short test.
- [R14 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Emulation mạng là một cấp test,không thay RF measurement.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

# M02 — Mô hình tham chiếu và test vectors

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Golden model là bộ đối chiếu để biết một chuỗi bits/IQ đúng hay sai. Mô hình floating-point kiểm thuật toán; fixed-point mô tả lượng tử như FPGA; RTL phải cho kết quả tương ứng tại các boundary đã chọn.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** có chuẩn kiểm tra độc lập cho thuật toán, fixed-point và RTL.

**Đầu vào/đầu ra:** payload/config/channel seed → encoded bits, symbols, I/Q, LLR, decoded payload và metadata mong đợi.

**Yêu cầu kỹ thuật:** lặp lại được, có version, vector tại boundary; bao phủ sạch/nhiễu, CFO, fractional delay, clock drift, phase noise và nhiều burst. Model không được dùng cùng một implementation sai ở cả hai đầu rồi coi tự tương thích là đúng.

**Phương án/chi tiết:** Python/C++ và project GNU Radio [S8–S9] cho đối chứng; floating-point trước, fixed-point bit-accurate sau. Lưu scaling, q-format, endian, seed và expected output; tạo scripts FER/EVM/timing. Khi model và RTL khác nhau phải xác định boundary đầu tiên lệch.

**Kiểm chứng/đầu ra bàn giao:** clean-channel bit exact; ít nhất một nguồn encoder/transmitter độc lập; baseline curves có confidence/sample count; bộ vector regression cho CI.

**Lộ trình/phụ thuộc:** M1–M4 nền; M5–M16 thêm impairment/profile và fault tests. DSP + QA; cần M01 profile, hỗ trợ toàn bộ PHY và control.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M02-REQ-001 | Vectors tái lập | Seed/profile/scaling và expected outputs lưu cùng test |
| M02-REQ-002 | Đối chứng độc lập | Có vector hoặc TX khác implementation DUT |
| M02-REQ-003 | Bao phủ impairments | AWGN, CFO, fractional timing, drift và near-far có sweep |
| M02-REQ-004 | Mô hình fixed-point rõ | Mỗi khối có width/fraction/saturation, không cast ngầm |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Input là payload/config và channel impairment. Output lưu `.bin` I/Q hoặc LLR và metadata JSON chứa dtype, endian, signedness, sample rate, frame ID, reference point, seed và checksum. Model không dùng timestamp file hoặc arrival OS làm mốc sample.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Tạo vector sạch

Bắt đầu một frame/burst có payload đếm tăng, qua encode/map/filter. So từng boundary với nguồn độc lập trước khi thêm nhiễu.

### 5.2. Xây mô hình kênh

Tách AWGN, CFO, phase offset, fractional delay và sample drift thành các khối có tham số. Kiểm một impairment một lần rồi tổ hợp; định nghĩa noise power ở bandwidth/reference nào.

### 5.3. Đánh giá acquisition và FEC

Quét SNR/CFO/delay với nhiều seed; ghi số frame, lỗi, thời gian bắt, false locks và confidence. Không suy BER cực thấp từ vài frame.

### 5.4. Lượng tử hóa

Chạy sweep bit widths, rounding và saturation; so degradation và tài nguyên dự kiến. Lưu input gây first divergence để debug RTL.

### 5.5. Đưa vào regression

Phân cấp smoke/per-commit/nightly/full; vector clean và protocol semantics chạy nhanh, FER sweep dài chạy theo milestone. Không cần rerun toàn bộ monte-carlo mỗi sửa văn bản.

## 6. Ví dụ tính toán hoặc luồng minh họa

Với IQ16 little-endian, một complex sample gồm 2 byte I rồi 2 byte Q. 1.000 sample chiếm 4.000 byte. Nếu đo ns từ index, dùng index/fs; một offset 0,5 sample tại 30,72 MS/s tương đương khoảng 16,28 ns, cần fractional delay model để kiểm.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M02-TC-001 | Replay cùng seed/config | Output hash không đổi trong cùng version |
| M02-TC-002 | Clean vector independent TX | Bits/framing trùng và payload đúng |
| M02-TC-003 | Quantization sweep | Có FER/overflow report, không chỉ EVM đồ thị |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Hai đầu dùng chung mapper sai vẫn giải được nhau; cần independent vectors. AWGN tính theo Eb/N0 nhưng plot Es/N0 tạo sai ngưỡng; luôn ghi normalization. Mô hình native float không thay bit-accurate kiểm saturation.

## 10. Bài thực hành nhập môn gắn với mô-đun

Sinh 100 QPSK symbols, thêm CFO có dấu, tự tính góc quay giữa hai symbol. Lưu IQ và JSON, nhờ người khác đọc file không hỏi thêm format. Sau đó chèn lỗi I/Q swap và xác định boundary phát hiện.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R13 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Xem support matrix, flowgraph và các synchronization/FEC blocks; khóa commit khi dùng.
- [R01 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Dùng waveform là oracle normative, không suy từ đồ thị.
- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đối chiếu return burst construction/FEC đúng waveform.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

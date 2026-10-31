# M11 — FEC Turbo upstream

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Turbo ở đây là một waveform return được xác định chính xác, không chỉ một tên họ mã. Remote mã hóa, HUB giải mã; việc HUB thu hai carrier làm tải decoder tăng và có thể đến dồn từng cụm burst.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** bảo vệ burst return với một waveform xác định và decoder HUB đủ backlog.

**Đầu vào/đầu ra:** VSAT packet/codeblock → encoded stream; HUB soft stream → payload và CRC/status.

**Yêu cầu kỹ thuật:** chính xác họ mã, interleaver, puncturing, termination/circulation, block size và mapping. Không dùng core Turbo LTE hoặc Turbo product code rồi mặc định tương thích TC-LM. Rate 1/2 chỉ khóa nếu hợp lệ trong waveform đã chọn.

**Phương án/chi tiết:** encoder ở VSAT PL; decoder HUB software ở PoC thấp tốc, sau đó FPGA hoặc host tối ưu nếu chứng minh đạt. Model kiểm từng permutation/bit order, quantization và iteration. Tính worst-case số burst/giây và max decoder queue cho hai carrier, không dùng benchmark một burst đơn.

**Kiểm chứng/đầu ra bàn giao:** golden vectors, BER/FER, profile sheet, latency/iteration/backlog report. Nếu thay FEC khác phải quản lý thay đổi chỉ tiêu H27–H28/V27–V28 và peer waveform.

**Lộ trình/phụ thuộc:** M2–M4 chọn profile/PoC; M5–M6 vectors; M7–M10 realtime; M11–M14 dual-carrier stress. FEC + HUB implementation; M01/M02/M12/M13.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M11-REQ-001 | Waveform được định danh | Codeblock/interleaver/puncturing/mapping/termination ghi đủ |
| M11-REQ-002 | Peak 3 Mbit/s IP | Profile 5 Msym/s mục tiêu rate 1/2 có overhead đủ margin |
| M11-REQ-003 | HUB dual-carrier load | Mục tiêu ≥6 Mbit/s tổng, max iteration backlog được tính |
| M11-REQ-004 | LLR và trạng thái decoder rõ | Quantization/status/CRC/identity giữ xuyên pipeline |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

VSAT nhận payload đã pack/CRC và waveform ID từ M12/M18, trả coded bits. HUB nhận ordered LLR/codeblock từ M13, trả payload, CRC và iteration/status. Bảng cấu hình có codeblock bits, couple permutation, puncture pattern, transmitted bit count và pilot positions.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Chọn waveform cụ thể

Tra R02 cho TC-LM và reference bursts. Chọn profile hợp lệ theo tốc độ/payload/efficiency; nếu rate 1/2 không hợp với profile đã chọn thì sửa baseline bằng ADR thay tự chế rồi gọi RCS2.

### 5.2. Model encoder độc lập

Kiểm từng permutation, state circulation/termination và puncturing bằng golden vectors. Phân biệt double-binary/convolutional Turbo với product code và các mã LTE.

### 5.3. Model decoder

Khảo sát max-log-MAP/scaling/iteration theo hiệu năng và tài nguyên. Noise/LLR normalization dùng cùng quy ước M02/M13; kiểm tail-biting và boundaries.

### 5.4. Chọn nơi thực thi

HUB software decoder giúp kiểm đúng sớm nhưng cần benchmark trên target thực. Đo nhiều burst back-to-back hai carrier; nếu backlog không bounded chuyển FPGA/parallel engines hoặc mua core.

### 5.5. Tích hợp và kiểm tải

Khóa waveform table/version, test length sai/rate unsupported, lost bursts và queue recovery. VSAT encoder chuẩn bị đủ sớm; không để việc mã hóa trễ làm phát muộn.

## 6. Ví dụ tính toán hoặc luồng minh họa

Upstream QPSK 5 Msym/s, rate 1/2 có ideal 5 Mbit/s. Payload IP 3 Mbit/s cần tổng efficiency ≥60%, gồm preamble, FEC termination, CRC, guards, signalling, padding và lịch. 60% chỉ là điều kiện cần; số symbols thực từ waveform table mới quyết định profile có đủ margin.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M11-TC-001 | Vectors theo waveform | Codewords/decoded bits và status đúng |
| M11-TC-002 | FER/quantization | Có curve và max-iteration performance |
| M11-TC-003 | Hai carrier dồn burst | Decoder queue bounded, không mất identity hoặc completion |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Đặt tên “Turbo” không đủ để hai thiết bị hiểu nhau. Benchmark decoder trên PC mạnh rồi áp cho Cortex-A9 là sai. CRC chỉ được dùng theo định nghĩa profile và không thay xác thực terminal.

## 10. Bài thực hành nhập môn gắn với mô-đun

Lập bảng một burst: information bits, transmitted bits, coded symbols, preamble/tail, guard và IP bytes. Từ bảng tính throughput và tìm hạng mục overhead lớn nhất.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc TC-LM coding/interleaving và burst construction tables.
- [R03 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Tham khảo return-link implementation và hệ thống.
- [R10 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Nếu host decoder dùng DMA buffers, ownership/cache vẫn áp dụng.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

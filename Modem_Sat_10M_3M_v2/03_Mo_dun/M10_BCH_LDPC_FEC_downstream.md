# M10 — FEC BCH/LDPC downstream

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Encoder tạo bit dư để receiver sửa lỗi; decoder dùng nhiều LLR, bộ nhớ và vòng lặp. Decoder thường khó và tốn tài nguyên hơn encoder; mua một core encoder không giải quyết được modem VSAT.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** mã hóa tại HUB và giải mã tại VSAT đúng profile, đủ tốc độ liên tục.

**Đầu vào/đầu ra:** HUB: frame bits → coded bits; VSAT: ordered LLR + config → recovered bits và decode status.

**Yêu cầu kỹ thuật:** đúng normal FECFRAME/rate 1/2; throughput worst case với max iterations; BRAM/message bandwidth đủ; BCH không bị bỏ; status uncorrectable rõ. FPGA resource/Fmax phải có place-and-route evidence, không chỉ số LUT ước tính.

**Phương án/chi tiết:** đánh giá core thương mại và PoC nội bộ; nếu tự làm khảo sát layered normalized/offset min-sum, banking, saturation, early stop. Chọn soft width từ FER/resource trade-off; kiểm parity và permutation độc lập. Giao tiếp frame-ID giữ từ LLR đến output, queue đôi để không tràn.

**Kiểm chứng/đầu ra bàn giao:** vectors độc lập; FER vs reference, max-iteration throughput, timing closure và memory utilization. License/source/binary/constraints theo phương án mua; không hứa làm chủ source phần black box.

**Lộ trình/phụ thuộc:** M1–M4 quyết định buy/build và PoC; M5–M10 tích hợp; M11–M14 worst case. FEC/FPGA; cần M01/M02, phối hợp M07/M09.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M10-REQ-001 | Đúng BCH/LDPC normal-frame profile | Rate1/2bắt buộc, không bỏ BCH |
| M10-REQ-002 | Throughput ở max iterations | TheoDS10/12,5 Msym/s và frame arrivals, không benchmark kênh sạch |
| M10-REQ-003 | Memory bank/scaling | Channel LLR và messages tính riêng, overflow policy rõ |
| M10-REQ-004 | IP/license/resource proof | Timing sau routing/utilization, license/bàn giao source rõ |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

HUB BBbits→BCH→LDPC coded bits. VSAT LLRframe +profile/frameID→LDPC→BCH→recoveredBBbits/status. M07 có thể vận tải LLR; completion giữ frame ID. Config unsupported bị reject, không dùng code rate khác mà vẫn gọi đúng chuẩn.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Chốt profile và golden bits

Tra đúng matrix/parity/BCH parameters, tạo vector encode sạch và error patterns. So độc lập để bắt permutation/endian sai.

### 5.2. Buy/build checkpoint

Yêu cầu vendor target7series, max iterations, quantization, memory, Fmax sau routing, interface và license. Tự làm thìprove một decoder nhỏ/model đúng trước scaling.

### 5.3. Thiết kế decoder

Khảo sát layered normalized/offset min-sum, banking/parallelism, message widths, saturation và early stop. Chọn thuật toán bằng FER và resource, sẽ không được chuẩn chỉ định một architecture.

### 5.4. BCH và status

Giữ outer decoder, correctable/uncorrectable status và BB integrity. Early syndrome success không đủ chứng minh user payload luôn đúng; kiểm full chain.

### 5.5. Load và timing closure

Sweep max iterations, buffer depth và serial LLR backlog. Dùng constraints đúng, timing/CDC report; nếu khôngđạtM4chốt IP/partition/rebaseline, tránh trì hoãn đến cuối.

## 6. Ví dụ tính toán hoặc luồng minh họa

64800codedbits ×6bitLLR=388800 bits=48,6kB channel LLR. Đó chưa là message RAM. Coded-envelope25 Mbit/s cho 385,8frame/s tức2,592 ms/frame; decoder worst case phải theo kịp hoặc engine/buffer được chứng minh đủ, không dùng latency của1iteration.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M10-TC-001 | Independent vectors và error patterns | Encode bits đúng, decoder/status đúng từng profile |
| M10-TC-002 | FER/iteration sweeps | Loss≤mục tiêu, kèm quantization và sample count |
| M10-TC-003 | Continuous frames ở worst case | Không queue overflow; Fmax sau routing/resource có margin |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Bỏ BCH vì LDPC đã sửa được demo là thiếu chuỗi. Chỉ đếm DSP là không đủ vì RAM/routing chi phối. Mua IP không có quyền sử dụng target/bàn giao sẽ khóa sản phẩm về sau.

## 10. Bài thực hành nhập môn gắn với mô-đun

Tự tính RAM cho LLR5/6/8bit, sochi phí. Mô phỏng một block có bit errors và ghi iterations/syndrome. Giải thích vì sao một test kênh sạch không là worst case decoder throughput.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R01 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Tra bảng BCH/LDPC và annex đúng normal frame/rate.
- [R08 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Resourcebydevice/package không là đảm bảo fit.
- [R13 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Decoderreference để đối chiếu; kiểm license/dependencies.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

# M09 — Bộ thu DVB-S2 tại VSAT trước FEC

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Receiver phải tìm “nhịp” và “đầu câu” trong IQ rồi mới đưa quyết định mềm cho decoder. LLR cho biết mức tin cậy bit, không chỉ0/1. Sai timing/pha có thể tạo LLR xấu dù FFT nhìn thấy carrier rõ.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** bắt/bám tín hiệu downstream và sinh soft bits đủ chất lượng.

**Đầu vào/đầu ra:** I/Q samples → LLR, frame/config metadata và timestamp marker trước FEC.

**Yêu cầu kỹ thuật:** hỗ trợ profile HUB; acquisition/tracking symbol, frame, carrier/phase; LLR đúng dấu/thang; có status riêng từng tầng. Miền CFO/drift/SNR và thời gian bắt phải được khóa sau model, không đặt ngẫu nhiên.

**Phương án/chi tiết:** DDC/resampling/RRC; coarse CFO; timing estimator/interpolator; frame/PLS detection; pilot-aided phase/frequency tracking; soft demap. Khảo sát Gardner/Farrow hoặc thuật toán tương đương phù hợp rate và oversampling; tuning acquisition khác tracking. Quantization qua float→fixed sweep, chống false lock/cycle slip.

**Kiểm chứng/đầu ra bàn giao:** acquisition probability/time, miss/false lock, LLR accuracy, FER cùng M10; đối chứng [S8]. Không sửa decoder để che LLR sai. RTL/model và trace tại boundaries.

**Lộ trình/phụ thuộc:** M2–M4 model; M4–M8 QPSK baseline; M9–M14 impairment/tải; M15–M18 mở rộng có gate. DSP/FPGA; M02/M06/M10/M14.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M09-REQ-001 | Bắt/bám profile và rate peak | QPSK tới 12,5 Msym/s; valid profiles rõ |
| M09-REQ-002 | LLR scaling/ordering | Frame length, q-format, sign và noise estimate có test |
| M09-REQ-003 | Marker trước FEC | Lưu frame ID/sample timestamp đểM14ghép reference |
| M09-REQ-004 | Miền bắt/false lock | CFO/SRO/SNR sweeps có ngưỡng khóa ởG1/G2 |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

RX IQ→DDC/resampler/RRC→coarse CFO/timing/frame/carrier recovery→LLR và frame metadata tới M10. Xuất diagnostics lock state, SNR/quality, residual CFO, cycle slips và marker timestamps. Không cắt timestamp tại completion decoder.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Kiểm input và matched filter

Xác minhI/Qsign/DC/clip, chọn RRC cùng roll-off và normalization. Sweep fractional sample offset, không lấy sample index nguyên làm hoàn toàn timing.

### 5.2. Acquisition

So coarse CFO estimator/correlation phù hợp QPSK, phát hiện SOF/PLS và valid frame. Tách state acquisition/tracking, timeout và reacquire; không một ngưỡng energy làm frame lock.

### 5.3. Symbol timing

Chọn timing estimator/interpolator qua mô hình; tại 30,72/12,5=2,4576 sps phải hỗ trợ fractional positions. Tune SRO capture và drift, không trình bày Gardner như lựa chọn bắt buộc chuẩn.

### 5.4. Carrier tracking và LLR

Pilot-aided frequency/phase tracking, kiểm cycle slips. Ước lượng noise variance và soft demap đúng dấu; saturated LLR không được quá tự tin ở SNR thấp.

### 5.5. Fixed-point và stream load

Sweep word length/scales, pipeline cho peak và backpressure trước FEC. Lưu điểm sai khác đầu tiên vector khi RTL/model lệch; pass frame ID/config nguyên vẹn.

## 6. Ví dụ tính toán hoặc luồng minh họa

q=6 bits/LLR và QPSK 12,5 Msym/s cho envelope150 Mbit/s tới FEC. Đây là load thiết kế trước trừ non payload symbols, không 150 Mbit/s IP. Một frame bị lost làm frame ID gap, decoder/timestamper phải nhận ra thay ghép reference sai.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M09-TC-001 | CFO/fractional delay/SRO sweep | ĐoP_acquire, time, false lock và reacquire |
| M09-TC-002 | LLR signs và quantization | BER/FER phù hợp independent model, không reverse bit |
| M09-TC-003 | Backpressure/peak | Không mất frame/metadata hoặc silently stallRF |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Nhầm Rx lock với network operational dẫn phát khi chưa range. Điều chỉnh FEC để che saiLLR làm khó debug. Tính frequency bằng MHz ở một khối và Hz ở khối khác ởkhốikhác có thể làm capture range sai1000lần.

## 10. Bài thực hành nhập môn gắn với mô-đun

Dùng QPSK model thêmphaπ/2 và CFO; xem constellation trước/sau correction. Vẽ histogram LLR cho SNRcao/thấp, kiểm dấu bit và ảnh hưởng saturation. Giải thích vì sao CRC pass không thay phép đo timing.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R01 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): SOF/PLS/pilot/mapping và bit ordering đúng profile.
- [R13 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc implementation synchronization để đối chiếu,không coi Float code là RTL.
- [R09 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): CDC giữa RF clock vàfabric/decoder.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

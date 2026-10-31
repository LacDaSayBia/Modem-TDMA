# M08 — Bộ phát DVB-S2 tại HUB

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

HUB TX tạo carrier liên tục để tất cả VSAT bám được reference và nhận dữ liệu. Packet IP không ánh xạ trực tiếp thành một lần bật/tắt RF; nó đi qua đóng gói, frame, FEC, mapping và lọc.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** phát downstream chuẩn, liên tục, chở IP và control.

**Đầu vào/đầu ra:** encapsulated packets/config/reference association → waveform I/Q và frame marker/ID.

**Yêu cầu kỹ thuật:** profile QPSK, CCM, normal frame/rate 1/2, pilot, roll-off 0,25 và Rs 1/2/5/12,5 Msym/s. Waveform theo [S1]. Reference phải liên kết đúng marker RF, không dùng thời điểm packet vào queue.

**Phương án/chi tiết:** packet framing → M10 encoder → mapping/PL framing → shaping/rate conversion → M06. Chuẩn bị SDR TX tham chiếu độc lập sớm; triển khai TX sản phẩm và đối chiếu. Duy trì waveform khi queue rỗng theo chế độ hợp lệ; kiểm metadata xuyên pipeline.

**Kiểm chứng/đầu ra bàn giao:** bits/symbol/frame markers đúng vector, spectrum/EVM theo test plan, VSAT/reference receiver thu được; continuous TX không mất mẫu. Source, vectors và waveform report.

**Lộ trình/phụ thuộc:** M2–M5 nguồn đối chứng; M5–M10 tích hợp TX; M11–M16 load/config; mode mở rộng sau G3. DSP/FPGA; M02/M06/M10/M18.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M08-REQ-001 | DVB-S2 profile đúng | QPSK CCM normal frame rate1/2, pilots, α0,25 |
| M08-REQ-002 | Maxrate phục vụ DS10 | Hỗ trợ 12,5 Msym/s đề xuất ngoài các bring-up rates |
| M08-REQ-003 | Continuous waveform/reference | Queue rỗng không làm mất mốc mạng |
| M08-REQ-004 | Reference marker association | Timestamp tương ứng mốc PHY, không enqueue time |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Input GSE/encapsulation packets và config; output coded symbols quaM10, shaped IQ tới M06, PHY marker/frame ID tới M14. Control/reference packets có scheduling reservation riêng. Tách byte input frame và bitstream FEC để kiểm bit-order.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Xây chuỗi frame sạch

Từ payload đếm tăng, tạo BBFRAME, gọi BCH/LDPC, mapping/PL header/pilot/scrambling theo profile. So từng boundary với source đối chứng.

### 5.2. Giữ tín hiệu liên tục

Xác định idle/dummy behavior phù hợp profile và protocol. User traffic rỗng vẫn có signalling/time reference; không đóng RF tùy queue.

### 5.3. Shaping và rate conversion

Thiết kế RRC/interpolator và scaleQPSK; rate 12,5 Msym/s có băng~15,625MHz, cần sample/filter plan hợp lệ và tránh overflow.

### 5.4. Gắn time reference

Chọn marker và quy pipeline latency; enqueue payload reference sớm với frame ID tương ứng. Nếu không biết chính xác marker sẽ phát khi nào, đo/crossstamp ởPL thay đoán từ CPU.

### 5.5. Tăng rate và kiểm song công

Chạy1/2/5 rồi 12,5 Msym/s; verify spectrum/payload/reference dưới đầy tải. Đồng thời HUB RX hai carrier, tránh DDR/clock contention.

## 6. Ví dụ tính toán hoặc luồng minh họa

Ideal 12,5 Mbit/s ở QPSK1/2 không phải IP 12,5. Header/pilot/BCH/GSE/control phải để lại≥10 Mbit/s; model lập symbol/byte accounting cụ thể. Dùng10 Msym/s QPSK1/2 không đủ cam kết IP10 vì overhead luôn tồn tại.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M08-TC-001 | Frame/pilot vectors | Trùng chuẩn profile và independent receiver giải được |
| M08-TC-002 | Idle→full load | Không sample gaps/reference discontinuity |
| M08-TC-003 | Peak song công | IPDS≥10 theo điều kiện, không underflow/spectrum violation |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Chạy data mapping đúng nhưng sai PL scrambler hoặc pilot positions sẽ mất interoperability. Dùng đưa payload vào FIFO làm timestamp khiến clock recovery lệch khiqueue thay. Spectrum CW không thay spectrum waveform.

## 10. Bài thực hành nhập môn gắn với mô-đun

Vẽ đường từ gói IP tới IQ và đánh dấu các nơi thêm overhead. Tạo một frame sạch và đối chiếu marker bằng sample index; đổi queue load và giải thích mốc nào vẫn phải ổn định.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R01 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): TraBB/PL framing,mapping và pilot theo bảng profile.
- [R13 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Dùng TX/RX tham chiếu, kiểm support và license.
- [R12 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Khi chọn GSE, đối chiếu header/fragmentation riêng.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

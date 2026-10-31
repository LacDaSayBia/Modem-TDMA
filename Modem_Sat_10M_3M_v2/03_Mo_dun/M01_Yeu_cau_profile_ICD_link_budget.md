# M01 — Phân tích yêu cầu, profile, ICD và quỹ đường truyền

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Mô-đun này giống bản thiết kế giao thông của toàn mạng: xác định ai được phát, phát gì, vào đâu và đánh giá thành công bằng đại lượng nào. Nó không thay việc viết RTL, nhưng ngăn các nhóm tự hiểu khác nhau về “10 Mbps”, “đúng khe” hoặc “hỗ trợ Turbo”.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** tạo cơ sở thống nhất cho mọi nhóm và biến chỉ tiêu thành cấu hình đo được.

**Đầu vào/đầu ra:** đầu vào là bảng H/V, topology, ODU và tài nguyên vệ tinh; đầu ra gồm SRS, profile matrix, ICD, timing/rate/level budgets và verification mapping.

**Yêu cầu kỹ thuật:** phân biệt chuẩn và giao thức riêng, IP/carrier rate, điểm timestamp, đơn vị/dấu, bit order/endian và điều kiện lỗi. Mỗi TBD có owner, thời hạn và dữ liệu cần để chốt. Quỹ đường truyền phải tính riêng hai hướng, không tự gán margin/availability khi thiếu EIRP/G/T và tuyến.

**Phương án/chi tiết:** đọc [S1–S3]; chọn một cấu hình cơ sở; kiểm tổng overhead đạt 10/6 Mbit/s; lập ma trận valid combinations; thống nhất RF reference plane; tính C/N0/EsN0 theo cùng định nghĩa, cộng implementation margin sau khi đo. Chốt encapsulation và waveform upstream bằng decision record.

**Kiểm chứng/đầu ra bàn giao:** review liên ngành; từng chỉ tiêu có phép đo và không có cặp yêu cầu mâu thuẫn. Link budget có input provenance, giả thiết và sensitivity analysis.

**Lộ trình/phụ thuộc:** M1–M2 baseline; M3–M4 đóng các sizing quan trọng; cập nhật tại mỗi gate. System architect chủ trì; là đầu vào của tất cả mô-đun.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M01-REQ-001 | SRS phân biệt peak, aggregate, per-terminal và CIR | REQ-SYS-DS-001/US-001 có điều kiện đo |
| M01-REQ-002 | Có bảng cấu hình PHY hợp lệ và overhead accounting | 12,5 Msym/s downstream; 5 Msym/s return là ứng viên, tính đủ mọi header/guard |
| M01-REQ-003 | Mỗi TBD có owner và hạn | Không cho release acceptance còn TBD ảnh hưởng kết quả |
| M01-REQ-004 | Mỗi yêu cầu có design và test link | Truy vết H/V → mô-đun → test → evidence |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Nhận yêu cầu người dùng và operator, trao đổi ICD với cả 19 mô-đun còn lại. Output machine-readable gồm requirement ID, text, status, origin, owner, test ID và change ID; dữ liệu tuyến gồm tọa độ, EIRP/G/T, frequency, antenna/BUC/LNB, rain availability và input source.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Định nghĩa các ranh giới

Vẽ topology Star GEO và reference planes. Phân biệt HUB modem, host NCC, RF/IFL và ODU. Xác định dữ liệu/clock/control nào qua ranh giới; yêu cầu độc lập PC hay không phải ghi cụ thể.

### 5.2. Khóa thuật ngữ đo

Viết câu nghiệm thu cho 10 Mbit/s IP và 3 Mbit/s IP. Chỉ rõ byte IP, packet size, thời gian quan sát, packet loss và resource allocation. Các proposed aggregate 6 Mbit/s phải được đánh dấu DERIVED, không giả là chỉ thị gốc.

### 5.3. Lập profile sheet

Tra R01/R02 để chọn mode/frame/codeblock chính xác. Tính số symbols, useful bytes, pilot/ramp/guard/control, giữ margin để đạt throughput. Ghi unsupported modes và fallback.

### 5.4. Tính budget và dependency

Liên kết link budget, processing budget và timing budget. Tăng rate có thể giảm Es/N0 và siết arrival accuracy; cập nhật cả ba thay vì riêng throughput.

### 5.5. Review và quản lý thay đổi

Mỗi quyết định có ADR; mỗi sửa requirement có CR, impact matrix và regression. G0 khóa định hướng, G1 khóa sizing, G4 freeze tập cấu hình bàn giao.

## 6. Ví dụ tính toán hoặc luồng minh họa

Downstream QPSK rate 1/2 ở 12,5 Msym/s có ideal 12,5 Mbit/s. Muốn 10 Mbit/s IP thì tổng overhead/loss budget phải dưới 20% với margin. Ở upstream 5 Msym/s, ideal 5 Mbit/s; 3 Mbit/s đòi hiệu suất ít nhất 60%. Hai bài không chứng minh decoder/RF đã đủ; chúng chỉ đặt điều kiện cần cho profile.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M01-TC-001 | Review mục tiêu peak và chia sẻ | Không có câu hứa mọi VSAT đồng thời 3 Mbit/s trên tổng 6 |
| M01-TC-002 | Audit trace | Mỗi H/V có module owner và test; các TBD có deadline |
| M01-TC-003 | Sensitivity link/rate | Thấy rõ thay bandwidth/EsN0/margin khi tăng rate |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Lỗi thường gặp là sao chép trần X5 thành chỉ tiêu board, dùng bit rate PHY thay IP, hoặc bỏ NCC khỏi scope. Cách tránh: một requirement một nghĩa, nguồn rõ và conditions nằm ngay cạnh giá trị. Không lấy model chưa chạy làm evidence MEASURED.

## 10. Bài thực hành nhập môn gắn với mô-đun

Chọn một packet 1.500 byte, lập bảng overhead dự kiến và viết một câu nghiệm thu có đủ đại lượng/đơn vị/điều kiện. Sau đó tìm hai yêu cầu cùng dùng từ “tốc độ” nhưng đo khác nhau và sửa lại cho rõ.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R01 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc system definition và subsystem, lấy bảng đúng profile.
- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc system model, return structure và signalling liên quan.
- [R17 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc phương pháp propagation; nhập tuyến thật thay số mặc định.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

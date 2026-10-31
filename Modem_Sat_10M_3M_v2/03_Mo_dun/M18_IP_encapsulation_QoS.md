# M18 — Encapsulation, IP datapath và QoS

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Lớp này biến packetIP thành các mảnh phù hợp frame/burst và ghép lại ở đầu kia. QoS chọn gói nào đi trước khi vệ tinh không đủ băng thông, không tạo thêm capacity vật lý.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** vận chuyển IP đúng MTU và chuyển yêu cầu dịch vụ thành nhu cầu tài nguyên.

**Đầu vào/đầu ra:** Ethernet/IP packets ↔ GSE hoặc encapsulation profile, upstream payload fragments và queue reports.

**Yêu cầu kỹ thuật:** IPv4/ICMP/UDP/TCP, static route, MTU 1.500, ít nhất 3 queue; fragmentation/reassembly bounded, chống stale fragments. Hạch toán throughput theo IP bytes, không tính padding/FEC.

**Phương án/chi tiết:** ưu tiên GSE downstream khi G0 xác nhận implementation/test [S12]; upstream packing theo burst profile riêng. Classifier theo policy, reservation signalling, priority cho traffic quan trọng và fairness best effort. Giới hạn queue theo latency/memory, report backlog có age; không buffer vô hạn để che thiếu grant. TCP performance đo riêng do RTT/loss.

**Kiểm chứng/đầu ra bàn giao:** packet sizes, fragmentation loss/reorder, checksum/MTU, simultaneous throughput, queue overload/fairness và control reservation. API/spec, source và capacity accounting report.

**Lộ trình/phụ thuộc:** M2–M4 encapsulation decision; M5–M10 IP path; M11–M18 QoS/stress. Embedded/network; M08/M10/M11/M16/M17.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M18-REQ-001 | MTU1500/IPv4 | IP/ICMP/UDP/TCP và static routing |
| M18-REQ-002 | Encapsulation định nghĩa | GSE hoặc TS/private được khóa, không nhập nhằng |
| M18-REQ-003 | Ba lớp QoS | Control reservation, priority và best effort có overload test |
| M18-REQ-004 | Peak accounting đúng | DS≥10/US3; padding/headers không tính thành IP throughput |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Ethernet/IP ingress→classifier/queues→encapsulation/fragmentation→M08/M12; decoder output→reassembly→IP egress. Backlog báo M16 theo useful bytes/queue age; credits/grants đơn vị slot/burst được đổi qua profile capacity table.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Chốt encapsulation

Ưu tiên GSE downstream nếu thư viện/test thích hợp; private/TS cần specification riêng và conformance scope rõ. Upstream packet packing đi theo burst profile nhiệm vụ.

### 5.2. Fragment/reassemble

Giữ packet ID/fragment order/length/timeout, giới hạn RAM và số contexts. Partial/stale/malformed fragments bị drop có counter, không concatenate nhầm packet.

### 5.3. Queue và classification

Ba lớp control/priority/best effort, policies xác định bằng fields/cấu hình. Limit bytes/age; shaping3M nếu yêu cầu trần dịch vụ, không conflating với PHYrate.

### 5.4. Phối hợp NCC

Report backlog có measurement epoch; trừ bytes đã grant/đang in-flight theo policy. Scheduler cấp useful bytes rồi packer chọn packet, tránh systematic padding lớn.

### 5.5. Đo IP/TCP/QoS

UDPpacket1500/high SNR cho peak; small packets/overload choCPU/QoS. TCP đo riêng vì RTT/congestion control; không hứa PEP khi chưa có module.

## 6. Ví dụ tính toán hoặc luồng minh họa

Một gói IP 1500 byte có thể chia thành nhiều burst. Throughput tính1500 byte chỉ khi packet được ghép và giao thành công, không cộng lại mỗi retransmission/fragment. Bộ đếm Ethernet1518 byte sẽ cho kết quả khác nên phải thống nhất.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M18-TC-001 | Fragment loss/reorder/timeout | Không corrupt packet hoặc leak contexts |
| M18-TC-002 | Peak UDP song công | IPbyte accounting và loss đúng baseline |
| M18-TC-003 | QoS overload | Control không starve, latency/drop/fairness được đo |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Tăng queue đến hết RAM làm latency lớn hơn chứ không tăng line capacity. GSElabel/CRC/fragment sai có thể chỉ lộ ởpacket dài. VLAN/MAC overhead không được cộng vào IP rate.

## 10. Bài thực hành nhập môn gắn với mô-đun

Chia packet1500 byte vào payload256 byte/burst giả định, tính số burst/padding và header overhead. Làm thêm packet64 byte để so efficiency, rồi thiết kế reassembly timeout có limits.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R12 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): GSEheader/fragmentation/integrity theo đúng mode.
- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Burstpayload/control structure nếu tham khảo RCS2.
- [R14 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Dùng network emulation để đo traffic/QoS trước RF.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

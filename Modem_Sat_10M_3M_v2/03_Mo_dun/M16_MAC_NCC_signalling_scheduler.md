# M16 — MAC, signalling, logon và NCC scheduler

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

NCC cấp quyền ai phát ở khe nào, carrier nào, tốc độ nào. MAC của VSAT gửi nhu cầu và thực hiện quyền đó. Scheduler đúng cần cả công bằng dịch vụ lẫn bất biến không xung đột và đủ thời gian chuẩn bị.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** quản lý vòng đời terminal và chia tài nguyên đúng nhu cầu/QoS.

**Đầu vào/đầu ra:** terminal state/backlog, resource map/corrections → grants, messages và telemetry.

**Yêu cầu kỹ thuật:** cấp đủ lookahead, không xung đột theo carrier và từng TX chain, control không starve, grant có ID/epoch/expiry. Parser bounded và versioned; logon collision/backoff riêng; ít nhất 16 terminal logic trong simulator.

**Phương án/chi tiết:** static schedule → request/grant → reservation/priority + weighted fairness. Resource ledger tính slots theo payload thực/guard/FEC; schedule double-buffer. VSAT FSM BOOT→RX_ACQUIRE→TIME_LOCK→LOGON→RANGING→OPERATIONAL, có HOLDOVER/TX_MUTED. Chọn message riêng có CRC/auth/replay rules; nếu triển khai RCS2 thay bằng signalling chuẩn phù hợp, không chỉ đổi tên.

**Kiểm chứng/đầu ra bàn giao:** invariant checker không overlap; oversubscription/admission, simultaneous logon, lost/reordered grants và HUB restart. Source, message spec, simulator và replay traces.

**Lộ trình/phụ thuộc:** M2–M5 simulator; M6–M12 static/logon; M13–M18 dynamic/QoS. MAC/network; M01/M14/M15/M18.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M16-REQ-001 | Static rồi dynamic allocation | Request/grant và resource ledger có replay test |
| M16-REQ-002 | Ba VSAT thật,16 logic | RF test và simulator tách kết quả |
| M16-REQ-003 | Peak và control reservation | Hai trạm3M, aggregate6 đề xuất, trạm thứ ba vẫn có signalling |
| M16-REQ-004 | Grant validity/security | ID/epoch/expiry, bounded parser, authentication policy |
| M16-REQ-005 | Không overlap TXchain | Một VSAT không phát hai carrier cùng lúc |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Backlog/terminal state/capabilities→scheduler→future grant tables; burst reports/corrections→state update. Message schema riêng gồm header version/type/length/network/terminal/sequence/epoch, payload và integrity/auth fields. Không giả message riêng là bitfield RCS2.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Thiết kế FSM

BOOT/RX_ACQUIRE/TIME_LOCK/LOGON/RANGING/OPERATIONAL với HOLDOVER/TX_MUTED; mỗi state có allowed messages, timeout và TX permission. Logon/ranging chỉ phát tài nguyên loại đó.

### 5.2. Resource ledger

Lưu timeline theo carrier/slot/profile/guard; tính useful bytes thật. Grant future horizon gồm forward/return và processing; superframe có thể ngắn nhưng cấp trước nhiều frame.

### 5.3. Static schedule proof

Bắt đầu lịch nhỏ để kiểm timing/capacity, invariants checker độc lập kiểm overlap, unsupported rates và late allocation. Network restart đổi epoch làm grants cũ hết hiệu lực.

### 5.4. Dynamic và QoS

Backlog reports có age; reservation control/priority rồi weighted fairness/best effort. Admission khi capacity thiếu, không hứa CIR vượt tổng6 Mbit/s proposed.

### 5.5. Signalling robustness

Bounds checks/CRC/auth/replay, retry/backoff cho contention logon và limits. Giả lập16 terminals với cold-start/loss/outage, lưu trace để replay deterministic.

## 6. Ví dụ tính toán hoặc luồng minh họa

Trên uplink aggregate6 Mbit/s, ba trạm cùng đòi3M tạo9 Mbit/s demand. Scheduler phải admission/share theo policy, không thể cấp đủ bằng cách giảm guard không kiểm. Trong bài peak hai trạm được gần toàn payload capacity và trạm còn lại vẫn giữ control.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M16-TC-001 | Invariant checker | Không overlap hoặc grant quá hạn/unsupported profile |
| M16-TC-002 | 16 terminal overload/cold-start | Control không starve, retry bounded và fairness report |
| M16-TC-003 | Replay/epoch/reset | Không stale grant, không identity mix-up |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Backlog chưa trừ packet đã grant làm cấp thừa. Superframe50 ms không đủ lookahead GEO nếu chỉ báo trước50 ms. UI NMS không nên giữ logic state thời gian thực của scheduler.

## 10. Bài thực hành nhập môn gắn với mô-đun

Vẽ resource map hai carrier, năm khe cho ba trạm. Tạo cố ý một VSAT có hai khe cùng thời gian trên hai carrier; viết checker phát hiện, rồi sửa lịch mà vẫn giữ control slot.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Resource/signalling và MF-TDMA cần đọc theo phiên bản.
- [R14 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Emulator hỗ trợ nghiên cứu traffic/MAC, không RF timing.
- [R18 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Viết requirement levels rõ và phân biệt đề xuất với bắt buộc.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

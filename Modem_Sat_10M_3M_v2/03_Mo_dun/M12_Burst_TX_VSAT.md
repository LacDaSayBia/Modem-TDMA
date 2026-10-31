# M12 — Bộ phát burst upstream tại VSAT

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

VSAT TX chỉ được phát trong khoảng tài nguyên được cấp. Nó vừa tạo nội dung burst vừa phối hợp M14 để sample/RF bắt đầu đúng lúc; đây là hai nhiệm vụ riêng.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** tạo burst đúng dữ liệu, tần số, thời gian và envelope được cấp.

**Đầu vào/đầu ra:** payload/config/grant → prebuilt symbols/waveform → timed I/Q; completion/error record.

**Yêu cầu kỹ thuật:** QPSK 0,25/0,5/1/2/5 Msym/s; preamble/FEC/CRC/tail đúng profile; đầy buffer trước arm, không phát muộn khi thiếu dữ liệu. NCO đổi carrier trong băng hợp lệ; một TX chain không phát hai carrier cùng lúc.

**Phương án/chi tiết:** packet packer → M11 → burst builder → RRC/interpolator → NCO/envelope → timed gate M14 → M06. Tính filter delay/tails; flush có kiểm soát; descriptor giới hạn duration và power. Áp correction theo epoch trước launch, không sửa waveform/config khi đang phát.

**Kiểm chứng/đầu ra bàn giao:** payload/CRC đúng, RF launch và end envelope đúng grant, carrier/ACPR/ramp đo được, duplicate/late descriptor bị từ chối. RTL/vector và RF burst captures.

**Lộ trình/phụ thuộc:** M3–M6 burst debug; M7–M10 FEC/timed; M11–M14 đổi carrier và RF tails. FPGA/DSP; M06/M11/M14/M16.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M12-REQ-001 | QPSK burst tới 5 Msym/s | Đạt chế độ IP3 khi grant đủ và profile hợp lệ |
| M12-REQ-002 | Chỉ phát khi hợp lệ | Clock/grant/epoch/buffer/RF permit đồng thời đúng |
| M12-REQ-003 | Carrier switch bằng số | NCO/DUC trong usable span, một carrier mỗi TX chain |
| M12-REQ-004 | Ramps/tails/duration | Không cắt lọc hoặc phát lấn grant, underflow phải abort/mute |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Nhận payload, waveform/rate/carrier/power IDs và grant; xuất waveform FIFO, arm request tới M14 và completion/error. Descriptor launch định nghĩa tại điểm chuẩn cụ thể; phần delay từ waveform builder tới RF được calibration, không đoán từ số lệnh CPU.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Pack trước deadline

Lấy packet theo QoS, fragment đúng codeblock, tạo CRC và gọi M11. Tính prepare time worst case; không nhận grant đã gần hơn giới hạn chuẩn bị.

### 5.2. Tạo symbols

Chèn UW/preamble/pilot/postamble theo profile, giữ bit mapping/scaling và đầu/đuôi filter rõ. Vector debug không FEC chỉ dùng PoC, không acceptance.

### 5.3. Shaping và đổi carrier

RRC/interpolation và complex NCO với phase policy tại boundary; LO giữ cố định khi span cho phép. Bao gồm group delay và tails trong burst reservation.

### 5.4. Arm có kiểm tra

Validate descriptor/config/epoch và waveform đầy buffer; trả accepted/rejected reason. Không thay buffer đang device-owned; double buffer cho burst tiếp theo.

### 5.5. Launch và kết thúc

M14 mở waveform theo time counter, giới hạn duration, ghi timestamp/completion. Buffer underflow hoặc IFL fault đóng TX theo policy, báo lỗi và không phát bù ngoài grant.

## 6. Ví dụ tính toán hoặc luồng minh họa

Ở 5 Msym/s, một symbol dài 200 ns; mục tiêu arrival 0,25 symbol là 50 ns. Nếu RRC có group delay G symbols thì RF reference phải bù G×200 ns theo quy ước; không mở FIFO đúng giờ rồi bỏ qua filter delay.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M12-TC-001 | Timed waveform sạch | Payload/FEC/CRC và đầu/đuôi đúng vector |
| M12-TC-002 | Late/duplicate/underflow | Reject hoặc mute an toàn, không phát ngoài quyền |
| M12-TC-003 | Đổi hai carrier | Một VSAT đổi theo lịch, spectrum và timing vẫn đạt |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Cắt RRC ngay bit cuối làm tail phổ rộng. Đổi SPI/PLL vào mỗi khe có thể trễ settling. Lấy accepted ACK làm bằng chứng RF đúng giờ sẽ bỏ qua latency của hardware.

## 10. Bài thực hành nhập môn gắn với mô-đun

Viết timeline grant→prepare→arm→launch→tail→complete và đánh dấu mốc RF. Tạo một descriptor quá hạn và kiểm hệ thống ghi REJECT_LATE thay vì phát ngay lập tức.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc burst construction, envelope và timing yêu cầu của waveform tham khảo.
- [R06 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đúng port semantics TX và sample rate.
- [R09 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Clock/reset và crossing của event/descriptor.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

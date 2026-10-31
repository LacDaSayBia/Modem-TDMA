# M17 — Linux/BSP, PS–PL, DMA và packet driver

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Linux quản lý thiết bị và packet; DMA đưa dữ liệu qua PS–PL mà không copy từng sample bằng CPU. CPU virtual address, DMA address và physical address không thể tùy ý thay thế nhau.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** vận chuyển packet/control và cung cấp nền software ổn định.

**Đầu vào/đầu ra:** XSA/bitstream/DT và hardware rings → kernel interfaces, buffers, completion/IRQ và app API.

**Yêu cầu kỹ thuật:** toolchain/release tương thích; regmap/IRQ/clocks/reset đúng; cache ownership và barriers rõ; bounded DMA ring, timeout/recovery. IIO dùng cấu hình/diagnostic, không tự thay timed-burst ABI.

**Phương án/chi tiết:** ADI Linux/no-OS/libiio theo release; PetaLinux tích hợp driver/DT tương thích. Test IRQ IP→GIC→driver, pattern DMA→real I/Q, coherent/streaming mappings theo kernel API. Custom packet/timed control driver với producer/consumer và cancel/reset states; rate-limit IRQ/log. Release bundle gắn driver ABI với FPGA build ID.

**Kiểm chứng/đầu ra bàn giao:** cache stress, ring wrap, MTU/length faults, timeout, reset dưới tải, build từ máy sạch. Source/BSP/DT và report IRQ/DMA/CPU/RAM. Xem [S6, S10–S11].

**Lộ trình/phụ thuộc:** M1–M4 bring-up; M5–M8 packet ABI; M9–M18 hardening; M19–M22 release. Embedded/FPGA; M03/M06/M14.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M17-REQ-001 | Release XSA/DT/driver khớp | Probe kiểm FPGA build/ABI ID, mismatch từ chối |
| M17-REQ-002 | IRQ đến GIC đúng | IP test/real DMA và counters/ack policy |
| M17-REQ-003 | Buffer ownership/cache | DMA API đúng, ring wrap/barrier/status có tests |
| M17-REQ-004 | Peak datapath và recovery | DS10/US3 không drop do software ở valid config, timeout phục hồi |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Register map + descriptor rings + IRQ là boundary kernel/PL; userspace dùng packet/control API bounded. Raw IIO capture là diagnostic path có arbitration. Ring states FREE→CPU_OWNED→DEVICE_OWNED→COMPLETE; reset/cancel có state riêng và không free buffer khi device còn dùng.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Known-good BSP

Khóa Vivado/HDL/kernel/DT/PetaLinux theo compatibility, build từ máy sạch. Kiểm address/phandle/interrupt/clocks/resets thay vì copy DT board khác.

### 5.2. IRQ rồi DMA

Tạo test IRQ IP để tách đường PL→GIC→driver, kiểm trigger/polarity/ack; sau đó DMA thật. Counter pending không đồng nghĩa Linux đã nhận IRQ.

### 5.3. DMA ownership

Dùng coherent hoặc streaming mapping đúng API, direction, sync và barriers. Không cast pointer userspace/stack thành DMA address; kiểm length/alignment và ring wrap.

### 5.4. Packet driver

Bound queue sizes, checksum/MTU, completion batching/IRQ moderation khi cần. Descriptor ABI versioned, validate trước device ownership; PS nạp timed descriptors sớm.

### 5.5. Recovery và load

Timeout reset có thứ tự, invalidate pending grants/buffers, không làm RF phát rác. Stress CPU/cache/DDR và song công, ghi drops/latency/CPU/RAM.

## 6. Ví dụ tính toán hoặc luồng minh họa

10 Mbit/s IP tương đương1,25 MB/s payload, nhỏ hơn raw IQ122,88 MB/s ở 30,72 MS/s. Runtime packet path và diagnostic IQ path có tải rất khác; mất IQ qua100M Ethernet không chứng minh packet modem không đạt10 Mbit/s.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M17-TC-001 | IRQ/pattern/real capture | Xác minh từng lớp, không chỉ một thao tác IIO |
| M17-TC-002 | Ring wrap/cache stress | Không corruption/leak/double completion |
| M17-TC-003 | Reset giữa transfer | Buffers/grants cũ invalid, driver phục hồi bounded |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

SPI tốt và TXDDS tốt chưa chứng minh RXIRQ/DMAC. Tắt cache toàn hệ thống để che ownership lỗi làm mất căn nguyên. Dùng userspace timer launch làm mất deterministic timing.

## 10. Bài thực hành nhập môn gắn với mô-đun

Vẽ một ring4 descriptors và ownership khi CPU ghi/thiết bị đọc/completion. Chèn timeout ở descriptor2, chỉ ra lúc nào được free buffer và lúc nào phải reset/cancel. Liên hệ với IRQ counter và ILA traces.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R07 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc DMAC register/IRQ/transfer semantics đúng corebuild.
- [R10 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): DMA addresses,mapping/cache/ownership và memory barriers.
- [R11 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Kernel code giữ coding style upstream.
- [R15 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): ADI driver nền, cần lock commit và patch set.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

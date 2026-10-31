# 07. Tổ chức nhân lực, WBS và lộ trình 24 tháng

> **Cập nhật CR-002 — 31/10/2026:** HUB downstream IP cực đại hỗ trợ **≥10 Mbit/s**; VSAT upstream IP cực đại **3 Mbit/s** khi được cấp đủ tài nguyên. Phương án sizing: downstream QPSK 12,5 Msym/s, rate 1/2; upstream QPSK tới 5 Msym/s, một Turbo profile mục tiêu rate 1/2. Đề xuất nâng HUB upstream lên **≥6 Mbit/s tổng/2 carrier**; đây là chỉ tiêu suy ra để phê duyệt, không phải yêu cầu người dùng đã chốt. Các rate thấp chỉ phục vụ bring-up. Xem [baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md); ví dụ số ở rate thấp vẫn là ví dụ, không là trần tốc độ sản phẩm. Tại upstream 5 Msym/s, mục tiêu timing 0,25 symbol tương ứng **50 ns**, phải kiểm chứng lại.

Toàn bộ thời gian/người công dưới đây là ước lượng quản lý đề xuất. M1 là tháng đầu kể từ ngày nhiệm vụ được khởi động; không tự gán mốc lịch khi chưa có quyết định triển khai.

## 1. Tổ chức đội ngũ

Đề xuất 8–10 FTE bình quân, khoảng 192–240 người-tháng trong 24 tháng. Có thể bố trí 10–12 người tham gia với tỷ lệ khác nhau để đạt mức FTE đó. Không cộng hai lần một người vừa làm DSP vừa FPGA. Trưởng hệ thống cần có quyền chốt interface/profile và dừng mở rộng khi gate không đạt.

| Vai trò | FTE định hướng | Trách nhiệm chính | Năng lực phải có |
|---|---:|---|---|
| System architect/chủ nhiệm kỹ thuật | 1,0 | Requirements, ICD, timing/link budget, gate | Hiểu waveform–MAC–RF–embedded, điều phối giao diện |
| DSP/PHY algorithm | 1,5 | Float/fixed model, acquisition/tracking, BER | Đồng bộ số, PSK, estimator, mô hình kênh |
| FPGA/SoC RTL | 2,0 | PHY RTL, timed TX, CDC, FEC integration, link | Timing closure, AXI, BRAM/DSP, debug ILA |
| Embedded Linux/BSP | 1,0 | Boot, DT/driver/DMA, network datapath/update | Linux kernel, cache/DMA, PS–PL |
| MAC/NCC/network | 1,0 | Ranging loops, scheduler, signalling, QoS | Distributed state, time-frequency allocation |
| RF/hardware | 1,0 | RF/IFL, clock, SI/PI, PCB và thermal | RF measurement, power/PCB thực tế |
| Verification/integration/QA | 1,0 | Golden vectors, automation, independent tests | DSP/RTL/software test và đo RF |
| NMS/tooling hỗ trợ | 0,5 | Log/monitoring, provisioning, test scripts | Network/API/data analysis |
| Tổng ví dụ | 9,0 | 216 người-tháng | Cần chuyên gia FEC tư vấn nếu đội chưa có |

Nếu tự làm cả LDPC decoder và Turbo decoder từ đầu, cần bổ sung năng lực FEC chuyên sâu hoặc giảm các hạng mục khác. Nhóm nhiều người có kinh nghiệm FPGA không đồng nghĩa có người từng thiết kế burst synchronizer/decoder. Dành 2–3 tuần đánh giá năng lực qua bài PoC thay cho chỉ dựa chức danh.

## 2. Quy tắc trách nhiệm

Mỗi gói có một accountable owner; nhiều người có thể implement/review. QA giữ dữ liệu kiểm thử độc lập, không chỉ dựa testbench của người viết khối. Kiến trúc sư phê duyệt mọi thay đổi điểm timestamp, waveform ID, clock/rate và PS–PL ABI. Chủ nhiệm quản lý nhân lực/kinh phí và scope; không tự thay giới hạn kỹ thuật đã chứng minh.

Sinh hoạt đề xuất: tích hợp hằng tuần; review interface hai tuần một lần; phát hành binary/model/vector hằng tháng. Feature freeze sau M18 ngoại trừ sửa lỗi được đánh giá tác động. Mọi gate có báo cáo đạt/không đạt và quyết định giảm scope/mua IP, không chỉ báo cáo phần trăm hoàn thành.

## 3. Các gói công việc theo form thống nhất

### W01 — Yêu cầu, chuẩn và kiến trúc

- **Mục đích:** biến mục tiêu “giống X5” thành profile đo được.
- **Yêu cầu:** tách chuẩn, tính năng riêng, throughput, topology, môi trường và deliverables.
- **Phương án:** lập support/conformance matrix, ICD và risk register, dùng các nguồn file 09.
- **Chi tiết:** khảo sát hệ thống; chọn Star GEO cố định; chốt A/B MF-TDMA; tính RF/time budget sơ bộ; quy định điểm chuẩn, bit order; định nghĩa G0/G1.
- **Lộ trình:** M1–M2 bản baseline; quản lý thay đổi đến M24.
- **Đầu ra/kiểm chứng:** SRS, architecture, ICD, test mapping; mọi chỉ tiêu có phương pháp đo và owner.
- **Chủ trì/phụ thuộc:** system architect; đầu vào cho tất cả gói.

### W02 — Mô hình tham chiếu và test vectors

- **Mục đích:** có chuẩn đối chiếu độc lập cho thuật toán/RTL.
- **Yêu cầu:** seed/config tái lập, vector tại các boundary và channel impairment.
- **Phương án:** Python/C++/GNU Radio phù hợp; tham khảo gr-dvbs2rx, gr-dvbs2; không giả định hỗ trợ mọi mode.
- **Chi tiết:** encoder/decoder vectors, acquisition sweeps, CFO/drift/phase noise, fractional delay, BER/FER và metadata schema.
- **Lộ trình:** M1–M4 bản đầu; mở rộng M5–M16.
- **Đầu ra/kiểm chứng:** model + test corpus + baseline curves + trace reader.
- **Chủ trì/phụ thuộc:** DSP + QA; W01 profile.

### W03 — Nền tảng AD9361, BSP, DMA và PS–PL

- **Mục đích:** tạo nền phần cứng/phần mềm ổn định trước modem.
- **Yêu cầu:** RX/TX mẫu, IRQ, clock/reset và recovery chạy được trên board.
- **Phương án:** known-good ADI HDL/Linux/no-OS; đóng băng release tương thích.
- **Chi tiết:** build từ đầu; kiểm PN/LVDS; DMA patterns, real capture, interrupt GIC, cache; custom register/descriptor ABI.
- **Lộ trình:** M1–M4; hardening M5–M8.
- **Đầu ra/kiểm chứng:** boot image/source, XSA/DT, I/Q captures, stress log và recovery test.
- **Chủ trì/phụ thuộc:** embedded + FPGA; W01 ICD.

### W04 — FEC PoC và quyết định IP

- **Mục đích:** loại rủi ro decoder làm trễ toàn bộ dự án.
- **Yêu cầu:** support profile, throughput worst case, tài nguyên và license rõ.
- **Phương án:** benchmark mua IP song song PoC nội bộ; chọn một hướng tại G1.
- **Chi tiết:** LDPC/BCH software/fixed/RTL proof; Turbo encoder/decoder profile; BRAM/bandwidth; max iterations; báo giá và quyền bàn giao.
- **Lộ trình:** M1–M4 quyết định; M5–M10 tích hợp; M11–M14 tối ưu nếu cần.
- **Đầu ra/kiểm chứng:** report synthesis/FER/throughput, license matrix, module có vectors.
- **Chủ trì/phụ thuộc:** FEC/FPGA + DSP; W01–W02. Không chờ PCB riêng.

### W05 — Downstream DVB-S2

- **Mục đích:** remote nhận được nguồn chuẩn và signalling liên tục.
- **Yêu cầu:** một MODCOD đúng chuẩn, acquisition/tracking/FEC ở rate baseline.
- **Phương án:** đối chứng SDR TX độc lập, FPGA RX theo từng khối; CCM trước ACM.
- **Chi tiết:** RRC/resampler/CFO/timing/PLS/pilot/LLR/decoder/BBFRAME, load và loss handling.
- **Lộ trình:** M2–M8 baseline; M9–M14 tích hợp; M15–M18 thêm mode có gate.
- **Đầu ra/kiểm chứng:** DVB-S2 chain, profile matrix, waveform/BER và đo chéo.
- **Chủ trì/phụ thuộc:** DSP/FPGA; W02–W04.

### W06 — Burst TX/RX và MF đa carrier

- **Mục đích:** trao đổi burst thực, từ TDMA một carrier đến MF-TDMA.
- **Yêu cầu:** hai carrier HUB thu đồng thời; một remote đổi carrier; burst có FEC/CRC.
- **Phương án:** LO cố định + NCO/DUC; HUB bank DDC, độc lập burst estimator.
- **Chi tiết:** waveform profile, preamble, ramp/tail, per-burst gain/phase/CFO/timing, near-far, decoder backlog.
- **Lộ trình:** M3–M6 burst debug; M7–M12 MF/FEC; M13–M16 load/robustness.
- **Đầu ra/kiểm chứng:** burst chain, two-carrier recordings, detector/FER/ACPR report.
- **Chủ trì/phụ thuộc:** DSP/FPGA; W02/W03/W04; phối hợp W07.

### W07 — Network time, timed TX và ranging

- **Mục đích:** đưa burst từng remote về đúng khe và an toàn khi mất sync.
- **Yêu cầu:** hardware timestamp, epoch, bù thô/tinh, effective correction và error budget.
- **Phương án:** counter PL, reference association, closed-loop HUB correction; hình học hỗ trợ logon.
- **Chi tiết:** công thức/trễ file 05, calibration, oscillator discipline, wrap/holdover, outlier, delayed-loop stability, hardware mute.
- **Lộ trình:** M2–M5 model/timed TX; M6–M9 hai remote lệch delay; M10–M16 tinh chỉnh đa carrier.
- **Đầu ra/kiểm chứng:** sync specification, timestamp/correction trace, arrival error histogram và loss-of-sync test.
- **Chủ trì/phụ thuộc:** system + MAC + FPGA; W03, W06; không đợi DVB-S2 đầy đủ mới mô phỏng.

### W08 — MAC, NCC, QoS và IP

- **Mục đích:** mạng tự gia nhập, cấp phát và chuyển IP theo chính sách.
- **Yêu cầu:** grant không xung đột, cấp sớm, multiuser state, admission/retry.
- **Phương án:** static schedule → request/grant → dynamic/QoS, dùng simulator trước RF.
- **Chi tiết:** message parser, FSM, resource map, backlog, priority/fairness, capacity/admission, CPU profiling.
- **Lộ trình:** M2–M5 simulator; M6–M12 static/integrated; M13–M18 dynamic/QoS.
- **Đầu ra/kiểm chứng:** NCC + remote MAC + replay/invariant checker; mô phỏng ≥16 remote logic.
- **Chủ trì/phụ thuộc:** MAC/network; W01, W07; tích hợp W05/W06.

### W09 — RF/IFL, clock và board sản phẩm mẫu

- **Mục đích:** chuyển dev board thành modem tích hợp có RF/nguồn thực.
- **Yêu cầu:** isolation, level/reference budget, bảo vệ BUC/LNB, thermal và DFT.
- **Phương án:** module RF/IFL trước; PCB tích hợp sau G1/PoC link và decoder.
- **Chi tiết:** chọn chip/package, pin/bank/clock plan, SI/PI, BOM, schematic/layout, manufacturing tests, 2 vòng PCB.
- **Lộ trình:** M1–M6 requirement/module; M7–M12 vòng 1; M15–M18 vòng 2; M19–M21 sửa nhỏ.
- **Đầu ra/kiểm chứng:** CAD/BOM/Gerber, calibration, power/thermal/RF/blocking report.
- **Chủ trì/phụ thuộc:** hardware/RF; W03/W04 kiến trúc chốt. Review độc lập trước fabrication.

### W10 — NMS, bảo mật và cập nhật

- **Mục đích:** vận hành và khôi phục được hệ thống mẫu.
- **Yêu cầu:** telemetry có version, credentials, alarms, signed update/rollback theo scope.
- **Phương án:** daemon/API/CLI trước, UI sau; dùng thư viện mật mã có sẵn.
- **Chi tiết:** inventory, config validation, counters, key provisioning, replay defense, watchdog, recovery release bundle.
- **Lộ trình:** M5–M10 nền log; M11–M18 quản trị/update; M19–M22 hardening.
- **Đầu ra/kiểm chứng:** NMS, runbook, update/recovery/fault tests.
- **Chủ trì/phụ thuộc:** embedded + tooling; W03/W08.

### W11 — Tích hợp, lab và thử vệ tinh

- **Mục đích:** chứng minh mục tiêu end-to-end và tìm lỗi giao diện.
- **Yêu cầu:** source/trace/config truy vết, kênh độc lập, điều kiện thử có calibration.
- **Phương án:** SIL → HDL sim → board loopback → IF impaired → GEO delay → live GEO.
- **Chi tiết:** test matrix file 08, harness, traffic generator, clock độc lập, near-far, faults, soak và live access plan.
- **Lộ trình:** bắt đầu M1 test plan; IF M6–M12; system M13–M20; live/soak M21–M23.
- **Đầu ra/kiểm chứng:** báo cáo pass/fail, raw captures, incident log và closure.
- **Chủ trì/phụ thuộc:** QA/integration; xuyên suốt tất cả gói.

### W12 — Hồ sơ và chuyển giao

- **Mục đích:** người khác build, đo và sửa được sản phẩm.
- **Yêu cầu:** source/model/RTL/BSP/CAD/license/test/report đúng release.
- **Phương án:** documentation-as-code, release manifest và acceptance package.
- **Chi tiết:** hướng dẫn sản xuất/bring-up, user/service manual, calibration procedure, giới hạn profile, training và reproducible build.
- **Lộ trình:** M1 lập khung, cập nhật mỗi gate; M22–M24 chốt.
- **Đầu ra/kiểm chứng:** bên tiếp nhận build từ máy sạch và lặp một bài nghiệm thu.
- **Chủ trì/phụ thuộc:** system/QA + từng owner; hoàn thành trước bàn giao.

## 4. Lịch và các cổng quyết định

| Mốc | Điều kiện phải có | Quyết định nếu chưa đạt |
|---|---|---|
| G0 cuối M2 | Profile, SRS/ICD, nguồn lực/lab, chuẩn A/B, kế hoạch IP | Giảm scope hoặc điều chỉnh tổ chức trước tiếp tục |
| G1 cuối M4 | AD9361/DMA nền ổn, PoC FEC/link, time model, sizing tài nguyên | Mua IP/đổi phân chia/giảm rate; chưa phát hành PCB tích hợp |
| G2 cuối M8 | DVB-S2 baseline ở lab, burst TDMA, timed TX/ranging hai delay | Tạm dừng ACM/mode mới; tập trung lỗi cốt lõi |
| G3 cuối M12 | ≥2 carrier đồng thời, 3 remote, FEC, logon/ranging/static grants, IP | Rebaseline chỉ tiêu trước năm hai; không chuyển sang feature phụ |
| G4 cuối M18 | Dynamic/QoS, PCB vòng 2, RF/clock calibration, fault recovery | Feature freeze, sửa lỗi/hạ subset có công bố |
| G5 cuối M22 | Full lab/GEO delay, soak, điều kiện thử vệ tinh sẵn | Tách nghiệm thu lab và live nếu access chậm, ghi rõ giới hạn |
| G6 cuối M24 | Acceptance profile đạt, hồ sơ/source/test hoàn chỉnh | Không gọi đạt tính năng chưa có dữ liệu kiểm chứng |

## 5. Đường găng và cách bảo vệ tiến độ

Đường găng kỹ thuật: profile → FEC và sync/burst PoC → PHY/timed TX → NCC/đa carrier → tích hợp RF/PCB → kiểm chứng hệ thống. PCB, mua IP và chuẩn bị phép thử vệ tinh có lead time nên chuẩn bị song hành, nhưng không được đóng băng thiết kế trước bằng chứng PoC.

Phân bổ M19–M24 chủ yếu cho tích hợp, sửa lỗi, thử và hồ sơ. Dự phòng thực nằm ở việc cắt tính năng mở rộng và giữ hai vòng PCB, không phải chỉ thêm một dòng “dự phòng” vào tháng cuối. Nếu G1/G2 trễ hơn khoảng một quý, cần quyết định phạm vi chính thức thay vì giữ nguyên mọi cam kết.

## 6. Kế hoạch 8 tuần khởi động

| Tuần | Công việc có giá trị quyết định |
|---|---|
| 1 | Đọc nguồn, lập SRS draft, kiểm kê người/board/lab, chốt thuật ngữ/rate |
| 2 | Chọn profile dự kiến, lập timing/bit-rate/IFL budget, liên hệ IP vendor |
| 3 | Boot/RX/TX DMA known-good; dựng TX/RX tham chiếu trên PC |
| 4 | Vectors một MODCOD và một burst FEC; timed TX counter test |
| 5 | Mô phỏng hai remote khác delay, delayed correction, scheduler invariant |
| 6 | Synthesis FEC/link sơ bộ, đo latency/IRQ/clock, so sánh 7020/7030 |
| 7 | Review ICD, test plan, nhân lực và chi phí theo gói |
| 8 | G0: ký baseline và ghi các việc chưa có bằng chứng; khởi tạo backlog G1 |

## 7. Nội dung đào tạo gắn sản phẩm

Người mới bắt đầu từ I/Q, symbol/sample/bit rate; DVB-S2 framing; AXI/CDC/DMA; hardware time và ranging; burst receiver; FEC soft decision. Mỗi chủ đề có một bài thực hành tạo vector, chạy model và đọc trace. Không giao ngay toàn bộ synchronizer hoặc decoder cho người mới mà thiếu reviewer. Ưu tiên người FPGA giàu kinh nghiệm phụ trách timed TX/CDC, người DSP phụ trách estimator và người Linux giữ BSP/packet path; kiến trúc sư phải hiểu giao điểm của ba nhóm.

# 08. Kiểm chứng, nghiệm thu, rủi ro và khung chi phí

> **Cập nhật CR-002 — 31/10/2026:** HUB downstream IP cực đại hỗ trợ **≥10 Mbit/s**; VSAT upstream IP cực đại **3 Mbit/s** khi được cấp đủ tài nguyên. Phương án sizing: downstream QPSK 12,5 Msym/s, rate 1/2; upstream QPSK tới 5 Msym/s, một Turbo profile mục tiêu rate 1/2. Đề xuất nâng HUB upstream lên **≥6 Mbit/s tổng/2 carrier**; đây là chỉ tiêu suy ra để phê duyệt, không phải yêu cầu người dùng đã chốt. Các rate thấp chỉ phục vụ bring-up. Xem [baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md); ví dụ số ở rate thấp vẫn là ví dụ, không là trần tốc độ sản phẩm. Tại upstream 5 Msym/s, mục tiêu timing 0,25 symbol tương ứng **50 ns**, phải kiểm chứng lại.

## 1. Nguyên tắc nghiệm thu

Các ngưỡng dưới đây là **đề xuất để khóa tại G0/G1**, không phải mức tự động do TCVN hay DVB quy định. Khi công bố tiêu chuẩn, ngưỡng normative đúng phiên bản/profile có ưu tiên; mục tiêu nghiên cứu bổ sung phải ghi riêng. Mỗi kết quả phải kèm cấu hình, số mẫu/thời gian quan sát, uncertainty/calibration và raw data.

Không đánh giá thành công chỉ bằng ping, constellation đẹp hoặc loopback giữa hai DUT giống nhau. Cần kiểm waveform/bit vector độc lập; các chức năng hệ thống như grant, ranging, clock holdover và multi-carrier phải có fault/load tests riêng.

## 2. Ma trận truy vết yêu cầu–kiểm chứng

| ID | Yêu cầu | Phương pháp | Tiêu chí đề xuất / điều phải báo cáo | Gate |
|---|---|---|---|---|
| R01 | DVB-S2 profile | Vector độc lập + nguồn TX đối chứng | Đúng bits/framing/constellation/FEC cho từng mode khai báo | G2 |
| R02 | Hiệu năng downstream | AWGN calibrated sweep | Báo FER vs Es/N0; mục tiêu implementation loss ≤1 dB tại FER 10^-3 so model cùng profile | G3/G4 |
| R03 | Acquisition/tracking | Quét CFO, drift, SNR, phase | Miền bắt, xác suất, p95/max thời gian; ngưỡng khóa sau model G1 | G3 |
| R04 | Upstream FEC | Vectors/FER/decoder load | Không sai bit ở kênh sạch; FER curve và iteration worst case | G3 |
| R05 | MF thực sự | 2 carrier chồng thời gian và 3 remote | HUB giải mã đồng thời; một remote đổi carrier; không lịch chồng TX chain | G3 |
| R06 | Ranging | Kênh delay khác nhau từng remote | Closed-loop arrival residual mục tiêu ≤0,25 symbol ở baseline, có error budget | G3/G4 |
| R07 | Timed launch | Oscilloscope/logic/RF capture | Báo accuracy/jitter RF, không chỉ descriptor ACK | G2/G3 |
| R08 | Mất reference/grant | Drop/reorder/replay/reset | Không phát ngoài quyền; mute trước khi vượt holdover budget | G4 |
| R09 | FEC/link/DDR capacity | Max load, max iterations | Không FIFO overrun/underrun ở valid config; thống kê worst case | G4 |
| R10 | IP throughput | UDP, nhiều packet sizes, hai chiều | Báo per-carrier/per-remote và simultaneous limit; mục tiêu ≥80% capacity model cho packet lớn | G4 |
| R11 | QoS | Mixed traffic quá tải | Traffic ưu tiên giữ SLA đã định, fairness/drop hợp lý; không starve signalling | G4 |
| R12 | RF spectrum | VSA/spectrum đo IF và RF khi có | Mask/ACPR/spur theo profile/operator; ramp/tails nằm trong budget | G4/G5 |
| R13 | FDD/near-far | TX cao khi RX yếu, blocker | Báo desensitization, dynamic range, carrier isolation; giới hạn khóa sau RF PoC | G4 |
| R14 | Update/recovery | Cúp nguồn/update sai/reset PL | Boot recovery được; không firmware/ABI mismatch, không tự TX trái phép | G4 |
| R15 | Stability | Soak 72 h cấu hình công bố | Không treo/reset bất thường, không phát ngoài lịch; counters/leaks và RF lỗi được báo | G5 |
| R16 | GEO thực tế | Delay lab rồi live satellite | Logon/ranging/MF/IP qua kênh; báo conditions/outage, không suy availability dài hạn từ buổi thử | G5/G6 |
| R17 | Bàn giao | Build từ máy sạch, chạy lại tests | Source/CAD/IP/license/version đầy đủ, test lặp được | G6 |

“Không thấy lỗi” không đồng nghĩa BER bằng 0. Ví dụ với N bit độc lập quan sát và không lỗi, upper bound BER một phía xấp xỉ 3/N ở mức tin cậy 95% (xấp xỉ mô hình lỗi hiếm). Với frame errors tương tự dùng số frame và giả thiết phù hợp; lỗi burst/correlated cần phân tích riêng. Không báo BER 10^-9 từ vài MB dữ liệu.

Ngưỡng 1 dB và 80% là mục tiêu nội bộ cần kiểm khả thi ở G1, không có nguồn nào ở đây bảo đảm DUT đạt. Mọi ngưỡng chưa khóa phải được ghi TBD trong acceptance specification chính thức, không để thử cuối dự án mới thương lượng.

## 3. Dựng hệ thống kiểm thử theo cấp

### Cấp 1: Model và RTL

Mục đích kiểm logic trước phần cứng. Dùng encoder/decoder reference, waveform vectors, randomized reset/backpressure, CDC lint và timing constraints. Có independent source vectors để tránh encoder và decoder cùng sai một bit ordering vẫn pass. Với timed TX, kiểm cả epoch wrap, descriptor thiếu, duplicate và negative correction.

### Cấp 2: Board/IF loopback

Dùng attenuator, splitter/combiner, RF shield, power meter và reference để tránh quá mức RF. Kiểm PN/LVDS, SPI, IRQ, DMA, I/Q sign/order, spectrum và deterministic latency. Common clock ở bước debug cho phép tách lỗi frequency khỏi logic; sau đó bắt buộc thử clock độc lập.

### Cấp 3: Kênh có impairment và GEO delay

Đặt riêng delay, attenuation, CFO/drift và noise cho forward/return từng remote. Delay hàng trăm ms nên có buffer lớn; nếu làm trên raw I/Q phải tính `memory = bytes_per_sample × fs × delay × streams`, cùng read/write bandwidth. Không giả định một FIFO BRAM nhỏ tạo được kênh GEO wideband. Có thể dùng emulator chuyên dụng hoặc software/SDR + DDR có timestamp; emulator phải chứng minh không sinh jitter ngoài budget. Thêm delay packet chỉ kiểm MAC/NCC, chưa kiểm waveform timing RF.

### Cấp 4: Live satellite

Chuẩn bị sớm operator approval, frequency/slot/power plan, antenna/BUC/LNB, commissioning và giám sát spectrum theo quy trình nhà khai thác. Chạy profile lab đã ổn, tăng power/tải có kiểm soát. Live test không thay lab fault injection vì khó tái tạo và tốn thời gian tài nguyên.

## 4. Tính capacity và hiệu suất để đặt chỉ tiêu đúng

Với một burst: tổng symbols gồm preamble, payload đã mã hóa, pilots và tails; thời gian thêm ramp/guard/retune nếu không nằm trong symbols. Payload bytes hữu ích trừ headers/CRC/padding. Capacity IP thực của superframe:

`R_IP = 8 × tổng payload_IP_bytes_được_giao_thành_công / T_superframe`.

Để sizing trước lỗi: dùng số byte hữu ích dự kiến và tổng slot, sau đó tính giảm do control/logon, retransmission, grant unused và scheduling fragmentation. Có thể ước lượng lý tưởng `Rs × log2(M) × rate_FEC × efficiency_framing × efficiency_MAC`, nhưng phải khai báo từng efficiency; không chọn một tỷ lệ chung không đo.

Ví dụ riêng để hiểu overhead: Rs=1 Msym/s, QPSK, rate 1/2, combined framing/MAC efficiency giả định 0,8 →0,8 Mbit/s/carrier trước lỗi/retry; hai carrier →1,6 Mbit/s tổng, không phải 1,6 Mbit/s cho từng remote. Giá trị 0,8 là giả thiết tính, không số đo chuẩn.

## 5. Quỹ đường truyền và availability — gói phải bổ sung dữ liệu

Mục đích là chứng minh MODCOD/rate hoạt động trên tuyến vệ tinh thực, gồm mưa. Yêu cầu có vị trí trạm, vệ tinh/transponder, EIRP/G/T, băng thông, antenna/gain/efficiency, BUC/output back-off, LNB/NF, cáp, pointing/polarization loss và interference. Không có các dữ liệu này thì chưa thể đưa dB margin đáng tin.

Phương án: tính riêng HUB→sat→remote và remote→sat→HUB; kết hợp nhiễu uplink/downlink và intermod/interference trong miền tuyến tính thích hợp; quy ra C/N0, Es/N0 hay Eb/N0 thống nhất; so với ngưỡng decoder thực đo cộng implementation/misc margin. P.618 là nguồn phương pháp dự đoán propagation Earth-space [S19], không phải một con số rain attenuation chung cho mọi địa điểm.

Nội dung thực hiện M1–M3 sơ bộ, M9–M12 cập nhật bằng ngưỡng modem và RF thực, M18–M22 chốt tuyến thử. Availability là kết quả mô hình thống kê/điều kiện tuyến và dữ liệu dài hạn; không kết luận “đạt 99,9%” chỉ từ thử vệ tinh vài ngày. Không tăng bitrate khi chưa có margin hỗ trợ.

## 6. Danh mục lab và số lượng prototype

| Nguồn lực | Vai trò | Phương án tối thiểu |
|---|---|---|
| Zynq/AD9361 dev boards | Remote và bring-up song song | Ít nhất 3 remote + 1 spare; HUB SDR/board riêng |
| FPGA board phụ/link fixture | PoC FEC/liên FPGA | 2 bộ đủ thử hai đầu trước PCB |
| PC/server/workstation | Golden model/NCC/build/traffic | Tách máy build và chạy test khi cần |
| Spectrum/VSA + signal generator/SDR đối chứng | Mask, EVM, acquisition, waveform | Đủ bandwidth và sensitivity cấu hình baseline |
| Oscilloscope/logic analyzer/reference counter | Timestamp, clock/IRQ/ramp | Độ phân giải/uncertainty phù hợp error budget |
| Attenuator/coupler/combiner/splitter/filter | Multiuser IF/near-far | Đủ cách ly, power rating và calibration |
| Clock/reference + independent oscillators | Debug và thử drift | Common reference chỉ dùng đúng mục đích bài thử |
| Channel emulator hoặc SDR/DDR impaired loop | Delay GEO/CFO/noise per remote | Chứng minh fidelity và timestamp budget |
| BUC/LNB/antenna/IFL | Kết nối mạng vệ tinh thực | Chọn theo operator và quỹ đường truyền |
| Power/thermal/EMC access | Mẫu tích hợp | Lab nội bộ hoặc thuê đo theo milestone |

Số lượng trên là đề xuất, không phải BOM đã duyệt. Một board vừa develop vừa chạy soak không giúp hai công việc diễn ra ổn định; cần spare và cấu hình test cố định.

## 7. Khung dự toán có thể điền báo giá

Chưa có báo giá hiện hành, địa điểm/chi phí nhân công và lease vệ tinh nên **không đưa tổng tiền giả định**. Công thức lập dự toán:

`C_total = C_labor + C_IP + C_devkits + C_PCB_2spins + C_RF_IFL + C_lab + C_satellite + C_software + C_external_review + C_contingency`.

| Khoản | Cơ sở tính | Phải thu thập |
|---|---|---|
| Nhân công | Tổng FTE-tháng × đơn giá đầy đủ | 192–240 người-tháng định hướng, phân vai cụ thể |
| FEC/protocol IP | License, maintenance, source/target seats | Báo giá, support profile, source escrow/bàn giao |
| Dev kits/chip | Số bộ + spare + freight/tax | Stock/lead time/đúng part-package khi mua |
| PCB/assembly | 2 vòng, fixture, rework, X-ray BGA | Layer count, quantity, test yield |
| RF/IFL/clock | Module và equipment ngoài modem | BUC/LNB level/reference/power spec |
| Lab | Mua/thuê/khấu hao và calibration | Bandwidth, đo phase noise/timing, thermal/EMC |
| Vệ tinh/field | Lease, commissioning, antenna sites | Operator window, rate/power/frequency plan |
| Công cụ | CAD/FPGA/simulation/CI | Seat/target/license duration |
| Chuyên gia | FEC/burst/timing review theo gate | Deliverable và thời điểm hỗ trợ |
| Dự phòng | Theo risk exposure, không chia đều | PCB respin, IP lead time, live access |

Chi phí giảm khi dùng open source nhưng còn công port, verification, license compliance và bảo trì. Cần quyết định buy/build theo thời gian và quyền làm chủ, không chỉ giá license.

## 8. Risk register ban đầu

| ID | Rủi ro / mức ưu tiên | Dấu hiệu sớm | Hành động / owner |
|---|---|---|---|
| K01 | Scope không khóa / rất cao | Đòi thêm mode/mobile/X5 compatibility liên tục | G0 profile + change impact; chủ nhiệm/system |
| K02 | FEC không đạt speed/resource / rất cao | PoC M4 chưa synthesis/FER | IP dự phòng, giảm rate/mode; FEC lead |
| K03 | Timing model sai/delay biến thiên / rất cao | Correction không hội tụ, reset đổi arrival | Hardware timestamp/calibration/delayed-loop model; sync owner |
| K04 | Burst receiver không chịu near-far / cao | Mất burst yếu khi mạnh xuất hiện | Wideband gain plan, filter, split receiver; RF/DSP |
| K05 | MF chỉ là retune tuần tự / cao | HUB không thu đồng thời | Wideband DDC hoặc thêm RX; HUB lead |
| K06 | Liên FPGA bottleneck/CDC / cao | CRC/retraining, FIFO stalls | PRBS/link PoC, margin/credit, simplify partition; FPGA |
| K07 | PS/PL DMA/IRQ chưa ổn / cao | Capture hang, dropped completion | Known-good platform, ILA/IRQ test trước PHY; embedded |
| K08 | RF TX phá RX/IFL faults / cao | Desense, spur, overcurrent | Module shielding/filter/protection; RF |
| K09 | PCB/clock/DDR lỗi / cao | Bring-up lâu, pin/bank conflict | Review/DFT/2 spins; hardware |
| K10 | Nhân lực thiếu chuyên môn / cao | Một người giữ mọi khối khó | Cross review, chuyên gia/IP; chủ nhiệm |
| K11 | Live satellite access chậm / cao | Chưa có operator plan M12 | Book sớm, lab GEO baseline riêng; tích hợp |
| K12 | License/source không bàn giao / cao | IP black box không có điều kiện sử dụng | Legal/IP review tại G1; chủ nhiệm |
| K13 | Test tự tương thích che lỗi / cao | Chỉ DUT TX↔DUT RX | Independent vectors/transmitter; QA |
| K14 | CPU/queue/security update lỗi / trung-cao | Latency tăng, mismatch firmware | Stress, bounded queues, signed bundle/recovery; embedded |
| K15 | Availability bị hứa quá mức / cao | Chưa có link budget vẫn ghi mưa/uptime | Đo và mô hình tuyến; system/RF |

## 9. Bộ sản phẩm nghiệm thu đề xuất

Ba remote mẫu có serial/config/calibration riêng; một HUB/NCC thử nghiệm; source/RTL/models/BSP/CAD; bộ build/release và license manifest; test vectors và scripts; báo cáo RF/PHY/sync/MAC/IP/soak; tài liệu thiết kế–vận hành–sửa chữa; test fixture và calibration procedure. Nếu có IP black box, nêu rõ quyền sửa đổi và phụ thuộc nhà cung cấp, không gọi toàn bộ công nghệ đã tự làm chủ source.

Đối với thương mại hóa tiếp sau, lập giai đoạn riêng cho environmental qualification, EMC/spectrum compliance phù hợp thị trường, manufacturability/yield, supply chain, security maintenance và field support. Chuẩn/phiên bản áp dụng phải được rà soát tại thời điểm phát hành sản phẩm [S20]; hồ sơ này không đưa ra kết luận pháp lý hoặc chứng nhận.

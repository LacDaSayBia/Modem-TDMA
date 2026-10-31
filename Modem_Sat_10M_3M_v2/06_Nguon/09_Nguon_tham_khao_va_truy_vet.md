# 09. Nguồn tham khảo, project và truy vết quyết định

> **Cập nhật CR-002 — 31/10/2026:** HUB downstream IP cực đại hỗ trợ **≥10 Mbit/s**; VSAT upstream IP cực đại **3 Mbit/s** khi được cấp đủ tài nguyên. Phương án sizing: downstream QPSK 12,5 Msym/s, rate 1/2; upstream QPSK tới 5 Msym/s, một Turbo profile mục tiêu rate 1/2. Đề xuất nâng HUB upstream lên **≥6 Mbit/s tổng/2 carrier**; đây là chỉ tiêu suy ra để phê duyệt, không phải yêu cầu người dùng đã chốt. Các rate thấp chỉ phục vụ bring-up. Xem [baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md); ví dụ số ở rate thấp vẫn là ví dụ, không là trần tốc độ sản phẩm. Tại upstream 5 Msym/s, mục tiêu timing 0,25 symbol tương ứng **50 ns**, phải kiểm chứng lại.

Ngày tra cứu: 31/10/2026. Các URL dưới đây là nguồn được tra cứu trực tiếp; tài liệu không khẳng định đã audit toàn bộ source/project hay thực thi một conformance suite. Trong repository phát triển cần lưu chính xác revision, commit SHA và checksum của bản thực sử dụng; hồ sơ hiện tại chưa khóa commit/toolchain của hệ thống tương lai.

## 1. Tiêu chuẩn và tài liệu nền tảng

### [S1] ETSI EN 302 307-1 V1.4.1, 2014-11 — DVB-S2

[PDF chính thức](https://www.etsi.org/deliver/etsi_en/302300_302399/30230701/01.04.01_60/en_30230701v010401p.pdf).

Căn cứ: cấu trúc downstream, BBFRAME/PLFRAME, FEC BCH+LDPC, constellation, frame/pilot và spectral shaping. Mục 5 là điểm bắt đầu tra cứu các subsystem; annex phục vụ mã và mask. Tiêu chuẩn định nghĩa waveform, không cung cấp một decoder FPGA đủ throughput cho board đề tài. Đọc chính xác các bảng tương ứng MODCOD/frame length thay vì triển khai từ bản tóm tắt trong hồ sơ.

### [S2] ETSI EN 301 545-2 V1.5.1, 2026-04 — DVB-RCS2 Lower Layers

[PDF chính thức hiện được đối chiếu](https://www.etsi.org/deliver/etsi_en/301500_301599/30154502/01.05.01_60/en_30154502v010501p.pdf).

Căn cứ: forward signalling, burst waveform/FEC, MF-TDMA resource structure và synchronization. Tra mục 6 signalling; 7.3.5 FEC; 7.3.9 timing; 7.5 MF-TDMA; annex A reference burst constructions. File 05 trích nguyên tắc và một số yêu cầu timing; không thay toàn văn. Phiên bản này đã xuất bản, không dùng draft tháng 1/2026 thay bản final tháng 4/2026.

[Bản V1.4.1, 2024-01 để so sánh khi cần](https://www.etsi.org/deliver/etsi_en/301500_301599/30154502/01.04.01_60/en_30154502v010401p.pdf). Không trộn field/bảng của hai phiên bản mà chưa đánh giá tương thích.

### [S3] ETSI TR 101 545-4 V1.2.1, 2026-01 — Implementation Guidelines

[PDF chính thức](https://www.etsi.org/deliver/etsi_tr/101500_101599/10154504/01.02.01_60/tr_10154504v010201p.pdf).

Dùng để tìm hướng triển khai và mô hình tham chiếu RCS2. Đây là technical report hướng dẫn; các nghĩa vụ tuân thủ phải kiểm lại EN/profile liên quan. Có giá trị để tổ chức nhóm đọc sâu theo miền: synchronization, MAC/control, deployment. Không coi một sơ đồ trong TR là thiết kế HDL hoàn chỉnh.

### [S4] iDirect — Evolution X5 Series Satellite Router, brochure mã 0810

[Bản PDF do nhà sản xuất biên soạn, hiện lưu trên máy chủ bên thứ ba](https://nt-vsat.com/wp-content/uploads/2019/DataSheet/iDirect_Evolution_X5_Brochure.pdf).

Nguồn tác giả là iDirect nhưng nơi lưu không phải domain hãng; đánh dấu rõ giới hạn này. Hai trang brochure hỗ trợ tham chiếu Star, DVB-S2/ACM, MF-TDMA, interface, QoS và các chức năng quản lý cơ bản; bảng có phân biệt chế độ iNFINITI trong ngoặc. Không chứng minh giao thức inbound, thuật toán scheduler hay compatibility. Khi cần đối chiếu hợp đồng phải yêu cầu hãng/đối tác cung cấp tài liệu đúng phiên bản hardware/software; chưa có tài liệu đó ở đây.

### [S5] Analog Devices — AD9361 Datasheet, Rev.G

[PDF hãng](https://www.analog.com/media/en/technical-documentation/data-sheets/AD9361.pdf).

[Trang sản phẩm/tài liệu hãng](https://www.analog.com/en/products/AD9361.html).

Dùng cho RF range, ADC/DAC/interface và bandwidth chip. Cần đọc điều kiện test, mode và giới hạn electrical; không chuyển thông số chip thành thông số modem hoặc board mà chưa đo. Product page có đường vào tài liệu AD9361 mới hơn khi lập thiết kế chi tiết.

### [S6] Analog Devices — AD9361 Reference Manual UG-570

[Bản PDF Rev.0 trên cộng đồng kỹ thuật chính thức ADI](https://ez.analog.com/cfs-file/__key/communityserver-discussions-components-files/323/AD9361_5F00_Reference_5F00_Manual_5F00_UG_2D00_570.pdf).

[Thông báo cập nhật tài liệu trên ADI](https://ez.analog.com/rf/wide-band-rf-transceivers/design-support/a/documents/DO26512/ad936x-documentation-changes).

Dùng để hiểu clock/filter/ENSM/gain/calibration/fastlock và điều khiển RF. PDF Rev.0 là bản tham khảo đã truy cập, không tuyên bố là revision hiện hành; trang sản phẩm nêu User Guide Rev.A. Khi khóa thiết kế phải lấy bản user guide/register map mới nhất được hãng cung cấp và quản lý errata. Không dùng thời gian typical trong user guide như guaranteed settling time của modem.

### [S7] Analog Devices — HDL repository

[Repository gốc](https://github.com/analogdevicesinc/hdl).

Nền tảng interface, clock và hệ thống tham chiếu. Reuse theo release/toolchain được hỗ trợ. Phải đọc license từng phần; không coi mọi file trong repository có cùng điều kiện cấp phép. Không bao gồm sẵn PHY vệ tinh mục tiêu.

### [S8] Analog Devices — AXI AD9361 documentation

[Tài liệu IP](https://analogdevicesinc.github.io/hdl/library/axi_ad9361/index.html).

Dùng cho giao tiếp AD9361–PL và register/data layout, làm cơ sở ICD. Tên `axi_ad9361` là interface IP, không phải DVB decoder. Các port/width/config phải khớp release source thực dùng.

### [S9] Analog Devices — AXI DMAC documentation

[Tài liệu IP](https://analogdevicesinc.github.io/hdl/library/axi_dmac/index.html).

Dùng cho transfer, register và interrupt semantics của DMAC. Cần kiểm đúng mode/build, không chỉ đối chiếu địa chỉ một project khác. DMA engine không cấp quyền phát TDMA và không thay clock/timestamp engine.

### [S10] Analog Devices — FMCOMMS2/3/4 HDL Project

[Reference design](https://analogdevicesinc.github.io/hdl/projects/fmcomms2/index.html).

Căn cứ nền bring-up, cấu hình interface, clock và đường DMA. Tài liệu nêu data rate tới 61,44 MSPS theo cấu hình. Prototype dùng để xác nhận flow trước PCB, không chứng minh mọi carrier/rate cấu hình riêng đều chạy. Phải xác định board hỗ trợ và release; không mặc định tài liệu `main` phù hợp bản Vivado cũ.

### [S11] AMD — Zynq-7000 SoC Data Sheet: Overview DS190 v1.11.1

[Trang tài liệu AMD](https://docs.amd.com/v/u/en-US/ds190-Zynq-7000-Overview).

[PDF từ AMD](https://docs.amd.com/api/khub/documents/juMnxca71Tf2gfjmNyjM8A/content).

Căn cứ bảng tài nguyên 7020/7030 và package/transceiver. Tra Table 1–3; thiết kế chi tiết còn cần technical reference manual, SelectIO, transceiver, memory và board design guides đúng target. DS190 không cho biết thiết kế decoder cụ thể fit hay đạt Fmax.

## 2. Project gốc để đối chiếu và tái sử dụng có giới hạn

| Mã | Project/nguồn gốc | Dùng cho việc gì | Điều không được kết luận |
|---|---|---|---|
| S12 | [igorauad/gr-dvbs2rx](https://github.com/igorauad/gr-dvbs2rx) | GNU Radio TX/RX, synchronization/FEC/BBFRAME đối chứng và test vector | Chưa phải fixed-point FPGA, network MF-TDMA hay bảo đảm realtime trên Cortex-A9 |
| S13 | [drmpeg/gr-dvbs2](https://github.com/drmpeg/gr-dvbs2) | Transmitter DVB-S2/S2X, nguồn test và đọc cách tổ chức framing | Không phải toàn bộ receiver/HUB |
| S14 | [CNES/OpenSAND](https://github.com/CNES/opensand) | Emulation hệ thống vệ tinh để nghiên cứu MAC/traffic/NCC và hành vi mạng | Không đo RF burst timing, không thay FPGA modem |
| S15 | [analogdevicesinc/linux](https://github.com/analogdevicesinc/linux) | Driver/kernel cho ADI, nền Linux/IIO | Không tự khớp XSA/DT của board tùy biến |
| S16 | [analogdevicesinc/no-OS](https://github.com/analogdevicesinc/no-OS) | Bring-up tối giản, phân lập RF driver khỏi Linux | Không có network stack/NCC hoàn chỉnh theo mục tiêu |
| S17 | [ADI libiio documentation](https://analogdevicesinc.github.io/libiio/) | Điều khiển và diagnostic I/Q từ host/app | Không có thời điểm phát TDMA được bảo đảm chỉ từ buffer API |

S12 công bố GPLv3; phải đọc COPYING và dependencies khi tái sử dụng. GPL không tự cấm thương mại, nhưng có nghĩa vụ khi phân phối cần được rà soát theo cách tích hợp. Các project còn lại cũng phải audit license theo component/commit, không suy từ tên tổ chức. Đây là yêu cầu quản lý IP, không phải khẳng định toàn bộ source được phép nhúng nguyên trạng vào sản phẩm đóng.

### [S18] Linux kernel — DMA API

[DMA API](https://www.kernel.org/doc/html/latest/core-api/dma-api.html).

[DMA mapping guide, bản 6.12](https://www.kernel.org/doc/html/v6.12/core-api/dma-api-howto.html).

Căn cứ nguyên tắc mapping, ownership, coherent/streaming DMA và cache synchronization. Kernel dự án có thể khác phiên bản; API chính xác phải theo cây source đã khóa. Không dùng địa chỉ userspace/stack trực tiếp như DMA-safe buffer.

### [S19] ITU-R P.618 — Earth-space propagation

[Trang recommendation chính thức](https://www.itu.int/rec/R-REC-P.618).

[Bản P.618-14, 2023-08](https://www.itu.int/rec/R-REC-P.618-14-202308-I).

Căn cứ phương pháp dự báo suy hao/propagation cho quỹ đường truyền. Dữ liệu vị trí, tần số, khí hậu, góc nâng và availability phải nhập đúng; hồ sơ này chưa thực hiện tính tuyến cụ thể.

### [S20] ETSI — Satellite Earth Stations and Systems

[Nhóm kỹ thuật SES và danh mục liên quan](https://www.etsi.org/technical-groups/ses/).

[Work item EN 301 428, kiểm trạng thái tại thời điểm triển khai](https://portal.etsi.org/webapp/WorkProgram/Report_WorkItem.asp?WKI_ID=74297).

Dùng định hướng xác định tiêu chuẩn spectrum/VSAT theo thị trường và phiên bản. Không coi bản đang approval/draft là đã có hiệu lực áp dụng tự động; phải rà soát quy định sở tại và yêu cầu operator riêng.

### [S21] ETSI TS 102 606-1 V1.3.1, 2025-02 — GSE Protocol

[PDF chính thức](https://www.etsi.org/deliver/etsi_ts/102600_102699/10260601/01.03.01_60/ts_10260601v010301p.pdf).

Căn cứ khi chọn GSE cho IP encapsulation, đặc biệt header, fragmentation/reassembly và integrity. Lựa chọn TS/private trong prototype không được công bố là đã triển khai GSE.

## 3. Bảng truy vết các quyết định quan trọng

| Quyết định/kết luận | Cơ sở bên ngoài | Phần suy luận/đề xuất của hồ sơ |
|---|---|---|
| BCH+LDPC là FEC downstream DVB-S2 | S1 | Sửa cách ghi nhiệm vụ, không dùng Turbo thay thế |
| MF-TDMA cần cấu trúc tài nguyên và điều khiển | S2/S3 | Đưa HUB/NCC vào đầu ra và staffing |
| Không cam kết compatibility X5 | S4 chỉ là brochure | Không có protocol/license thì chỉ benchmark tính năng |
| AD9361 làm RF/IF, ngoài chip vẫn cần modem logic | S5–S10 | Chia PL/FEC/IFL như file 02–04 |
| 7020 khác 7030 về transceiver/tài nguyên | S11 | Chọn serial hoặc SelectIO theo PoC và package |
| Hardware timed TX và latency calibration | S2/S3 + nguyên lý mốc thời gian | API descriptor, vòng điều khiển, error budget file 05 |
| Reference SDR và emulator hỗ trợ kiểm chứng | S12–S14 | Dùng đúng lớp, không coi đó là modem FPGA hoàn chỉnh |
| DMA cần ownership/cache đúng | S9/S18 | Driver/ring/reset tests file 06 |
| Chưa thể hứa availability | S19 cần dữ liệu tuyến | Yêu cầu link-budget work package và live test |
| 24 tháng, 8–10 FTE, các gate | Không có nguồn bảo đảm | Ước lượng kỹ thuật/quản lý của hồ sơ, phải điều chỉnh theo đội thực |
| Ngưỡng 0,25 symbol, ≤1 dB, 80%, soak 72 h | Không phải mặc định chuẩn | Mục tiêu đề xuất có gate, không chứng nhận đã đạt |

## 4. Những thông tin chưa được xác minh và cách đóng

1. Chưa có resource/Fmax/throughput thực của FEC trên 7020/7030/FPGA phụ → W04/G1.
2. Chưa có RF spectrum/sensitivity/clock/settling/calibration thực trên modem → W03/W09/G4.
3. Chưa có protocol nội bộ iDirect, license hay kiểm tương thích HUB → chỉ tham chiếu tính năng.
4. Chưa có băng thông/EIRP/G/T/antenna/BUC/LNB và số liệu tuyến → W01 link budget/G0–G5.
5. Chưa có báo giá và stock hiện hành → mua sắm/IP review trước đặt hàng.
6. Chưa có kết quả chạy các repository trên platform mục tiêu → W02/W03, ghi commit/toolchain và test log.

## 5. Thuật ngữ tối thiểu

| Ký hiệu | Diễn giải |
|---|---|
| Downstream / outbound | HUB → remote |
| Upstream / inbound / return | Remote → HUB |
| MF-TDMA | Multi-Frequency Time Division Multiple Access |
| NCC | Network Control Centre, điều phối mạng |
| PHY / MAC | Lớp vật lý / điều khiển truy nhập môi trường |
| PS / PL | Processing System / Programmable Logic của Zynq |
| FEC | Forward Error Correction |
| LDPC / BCH | Low-Density Parity-Check / Bose–Chaudhuri–Hocquenghem |
| LLR | Log-Likelihood Ratio, thông tin quyết định mềm |
| CCM / ACM | Constant / Adaptive Coding and Modulation |
| CFO | Carrier Frequency Offset |
| NCR | Network Clock Reference |
| BTP / grant | Burst Time Plan / cấp quyền tài nguyên phát |
| Ranging | Đo và hiệu chỉnh delay/thời điểm burst theo mốc mạng |
| IFL / BUC / LNB | Inter-Facility Link / Block Upconverter / Low-Noise Block |
| DDC / DUC / NCO | Hạ tần số số / nâng tần số số / dao động điều khiển số |
| CDC | Clock Domain Crossing |
| DMA / IRQ | Direct Memory Access / Interrupt Request |
| BER / FER / PER | Bit / Frame / Packet Error Rate |
| FTE / WBS / ICD | Full-Time Equivalent / Work Breakdown Structure / Interface Control Document |

## 6. Trình tự đọc nguồn cho đội dự án

Tuần đầu: S1 mô hình hệ thống, S2 mô hình và timing, S5 block diagram, S10 reference design. Sau đó mỗi nhóm đọc sâu phần của mình và lập checklist: DSP/FEC đọc S1/S2/S12/S13; FPGA/embedded đọc S7–S11/S15–S18; MAC/NCC đọc S2/S3/S14; RF/system đọc S5/S6/S19/S20. Mọi ghi chú phải có số mục/bảng hoặc source file/commit để người khác kiểm lại được.

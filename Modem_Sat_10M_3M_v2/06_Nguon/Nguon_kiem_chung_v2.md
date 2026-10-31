# Nguồn kiểm chứng và quy tắc sử dụng — v2

Tra cứu 31/10/2026. Chỉ dùng nguồn tiêu chuẩn, hãng và repository gốc cho các cơ sở kỹ thuật. Các lựa chọn tốc độ, thuật toán, ABI, ngân sách và kế hoạch là đề xuất của dự án; không được diễn đạt như nguồn đã bảo đảm phần cứng đạt. Không đóng gói nguyên bản tiêu chuẩn hoặc source bên thứ ba trong ZIP này.

| Mã | Nguồn trực tiếp | Nội dung tra cứu / giới hạn |
|---|---|---|
| R01 | [ETSI EN 302 307-1 V1.4.1](https://www.etsi.org/deliver/etsi_en/302300_302399/30230701/01.04.01_60/en_30230701v010401p.pdf) | DVB-S2 waveform, BCH/LDPC, framing; mục 5 và các bảng/annex theo profile. Không chỉ định kiến trúc decoder |
| R02 | [ETSI EN 301 545-2 V1.5.1](https://www.etsi.org/deliver/etsi_en/301500_301599/30154502/01.05.01_60/en_30154502v010501p.pdf) | Return waveform/signalling, mục 7.3.5 FEC, 7.3.9 timing, 7.5 MF-TDMA; phải chọn đúng tables/waveform |
| R03 | [ETSI TR 101 545-4 V1.2.1](https://www.etsi.org/deliver/etsi_tr/101500_101599/10154504/01.02.01_60/tr_10154504v010201p.pdf) | Hướng dẫn triển khai RCS2; không thay normative EN |
| R04 | [AD9361 Datasheet Rev.G](https://www.analog.com/media/en/technical-documentation/data-sheets/AD9361.pdf) | RF/clock/interface/electrical limits; cần đúng conditions |
| R05 | [ADI FMCOMMS2/3/4](https://analogdevicesinc.github.io/hdl/projects/fmcomms2/index.html) | Reference design/clock/data path; không mặc định mọi release đều hỗ trợ board |
| R06 | [ADI AXI AD9361](https://analogdevicesinc.github.io/hdl/library/axi_ad9361/index.html) | IP interface/regmap/sample order |
| R07 | [ADI AXI DMAC](https://analogdevicesinc.github.io/hdl/library/axi_dmac/index.html) | DMA, IRQ/register/flow control theo cấu hình core |
| R08 | [AMD DS190](https://docs.amd.com/v/u/en-US/ds190-Zynq-7000-Overview) | Zynq resources/package; không chứng minh fit/routed throughput |
| R09 | [AMD UG949 CDC, 2024.2](https://docs.amd.com/r/2024.2-English/ug949-vivado-design-methodology/Clock-Domain-Crossing) | CDC/methodology; phiên bản tham khảo, không ép dự án dùng Vivado 2024.2 |
| R10 | [Linux DMA API HOWTO](https://docs.kernel.org/core-api/dma-api-howto.html) | DMA ownership/mapping/cache; API theo kernel khóa |
| R11 | [Linux kernel coding style](https://docs.kernel.org/process/coding-style.html) | Chỉ áp coding style cho kernel; code vendor giữ style gốc |
| R12 | [ETSI TS 102 606-1 V1.3.1](https://www.etsi.org/deliver/etsi_ts/102600_102699/10260601/01.03.01_60/ts_10260601v010301p.pdf) | GSE protocol/fragmentation; chọn ở G0 |
| R13 | [igorauad/gr-dvbs2rx](https://github.com/igorauad/gr-dvbs2rx) | Đối chứng SDR TX/RX; không phải RTL. Kiểm COPYING/dependencies và support matrix |
| R14 | [CNES OpenSAND](https://github.com/CNES/opensand) | Emulation mạng/traffic, không chứng minh RF timing |
| R15 | [ADI Linux](https://github.com/analogdevicesinc/linux) | Kernel/driver nền; không đảm bảo khớp DT tùy biến |
| R16 | [ADI no-OS](https://github.com/analogdevicesinc/no-OS) | RF bring-up phân lập khỏi Linux; không cung cấp toàn NCC |
| R17 | [ITU-R P.618](https://www.itu.int/rec/R-REC-P.618) | Propagation Earth-space; phiên bản hiện tra cứu P.618-14; cần dữ liệu tuyến |
| R18 | [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.txt) và [RFC 8174](https://www.rfc-editor.org/info/rfc8174/) | Ý nghĩa mức yêu cầu khi dùng uppercase keywords |
| R19 | [RFC 1982](https://www.rfc-editor.org/info/rfc1982/) | Tham khảo serial arithmetic; áp project cần giới hạn cửa sổ nhỏ hơn nửa miền |
| R20 | [Semantic Versioning 2.0.0](https://semver.org/) | Tham khảo version public API; không thay build ID/ABI compatibility rules |

## Phương pháp dẫn nguồn

Mỗi mô-đun có mục “Nguồn và cách đọc” nêu mã Rxx và phần nội dung liên quan. Người triển khai phải ghi số mục/bảng hoặc source file/commit khi tạo ICD/code, không dùng một URL trang chủ làm bằng chứng cho tất cả yêu cầu. Các bản HTML động không chứa đầy đủ tables thì mở PDF chuẩn; lỗi truy cập phải ghi chưa xác minh thay vì tự suy diễn.

Đối với repository đang phát triển, bản tài liệu này chỉ ghi URL origin, chưa chọn commit phần mềm tương lai. Tại G1 ghi SHA, toolchain, license và patch set vào lockfile; source/software-only model hỗ trợ kiểm đúng chứ không chứng minh timing closure FPGA. Với R01/R02, mọi phép diễn giải tóm tắt trong bộ hồ sơ đều phải kiểm lại toàn văn trước tuyên bố conformance.

## Phân loại bằng chứng

NORM: nội dung normative đã chỉ đúng điều/mục; VENDOR: đặc tính theo điều kiện hãng; MODEL: kết quả mô hình có seed/config; MEASURED: số đo có procedure/calibration; PROPOSED: lựa chọn dự án; TBD: chưa đủ dữ liệu. Không nâng MODEL thành MEASURED hoặc PROPOSED thành NORM. Các file trong gói này là phân tích/thiết kế, chưa có số đo phần cứng mới.

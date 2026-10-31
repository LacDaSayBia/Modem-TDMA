# Bộ phương án nghiên cứu chế tạo modem vệ tinh Star — 24 tháng

> **Cập nhật CR-002 — 31/10/2026:** HUB downstream IP cực đại hỗ trợ **≥10 Mbit/s**; VSAT upstream IP cực đại **3 Mbit/s** khi được cấp đủ tài nguyên. Phương án sizing: downstream QPSK 12,5 Msym/s, rate 1/2; upstream QPSK tới 5 Msym/s, một Turbo profile mục tiêu rate 1/2. Đề xuất nâng HUB upstream lên **≥6 Mbit/s tổng/2 carrier**; đây là chỉ tiêu suy ra để phê duyệt, không phải yêu cầu người dùng đã chốt. Các rate thấp chỉ phục vụ bring-up. Xem [baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md); ví dụ số ở rate thấp vẫn là ví dụ, không là trần tốc độ sản phẩm. Tại upstream 5 Msym/s, mục tiêu timing 0,25 symbol tương ứng **50 ns**, phải kiểm chứng lại.

Ngày lập: 31/10/2026. Phiên bản: 1.0 — cơ sở lập nhiệm vụ và thiết kế sơ bộ, chưa phải thiết kế đã được đo kiểm.

## Kết luận điều hành

**Khả thi có điều kiện trong 24 tháng ở mức hệ thống mẫu nghiên cứu gồm HUB thử nghiệm + ít nhất 3 modem remote, DVB-S2 downstream và MF-TDMA upstream.** Không có cơ sở để cam kết trong cùng thời gian một sản phẩm tương đương toàn bộ iDirect X5, tương thích HUB iDirect, đủ mọi MODCOD và đã hoàn tất thương mại hóa. Đây là đánh giá kỹ thuật của bộ tài liệu, không phải kết luận được một nhà sản xuất bảo đảm.

Ba điều kiện bắt buộc: khóa phạm vi ngay hai tháng đầu; bố trí đội chuyên trách đủ năng lực PHY/FPGA, MAC/NCC, Linux và RF; có kinh phí IP FEC hoặc thời gian dự phòng cho tự phát triển, cùng hệ thống đo kiểm độc lập. Không thể chỉ giao một người viết FPGA và một người Linux rồi coi các phần còn lại là tích hợp thông thường.

**Cần sửa cách ghi FEC:** downstream DVB-S2 sử dụng BCH ngoài + LDPC trong [S1]. Turbo chỉ được lựa chọn cho upstream hoặc waveform riêng. Không ghi “DVB-S2 dùng Turbo hoặc LDPC/BCH” như hai phương án tương đương chuẩn.

**MF-TDMA là phương thức truy nhập, chưa xác định một waveform hoàn chỉnh.** Phải chọn: (A) MF-TDMA riêng có tham khảo DVB-RCS2; hoặc (B) triển khai một profile DVB-RCS2 có ma trận tuân thủ. Bộ tài liệu khuyến nghị A cho đầu ra 24 tháng, tổ chức kiến trúc để có thể nâng cấp B. Nếu hồ sơ nhiệm vụ bắt buộc B, phải đánh giá lại nhân lực, IP và tiến độ trước khi nhận nhiệm vụ.

## Danh mục và thứ tự đọc

| File | Nội dung | Người đọc chính |
|---|---|---|
| [01_Pham_vi_va_kha_thi.md](../01_Yeu_cau/01_Pham_vi_va_kha_thi.md) | Mục tiêu, giới hạn, chỉ tiêu sơ bộ, đối chiếu X5, khó khăn và điều kiện thành công | Chủ nhiệm, hội đồng, trưởng nhóm |
| [02_Kien_truc_he_thong_va_giao_thuc.md](../02_Kien_truc/02_Kien_truc_he_thong_va_giao_thuc.md) | HUB, remote, NCC, lớp giao thức, phân chia PS/PL/FPGA, hợp đồng giao tiếp | Kiến trúc sư, MAC, embedded |
| [03_Phan_cung_RF_clock_va_lien_FPGA.md](../02_Kien_truc/03_Phan_cung_RF_clock_va_lien_FPGA.md) | Zynq/FPGA/AD9361, RF/IFL, clock, băng thông, liên FPGA, PCB | FPGA, hardware, RF |
| [04_PHY_DVB_S2_MF_TDMA_va_FEC.md](../02_Kien_truc/04_PHY_DVB_S2_MF_TDMA_va_FEC.md) | Chuỗi tín hiệu, đồng bộ thu, burst receiver, mã sửa lỗi và fixed-point | DSP, FPGA, verification |
| [05_Dong_bo_thoi_gian_va_ranging.md](../02_Kien_truc/05_Dong_bo_thoi_gian_va_ranging.md) | Mô hình trễ, ví dụ số, timestamp, ranging, timing advance, sai số, vòng điều khiển | Tất cả nhóm kỹ thuật |
| [06_Phan_mem_nhung_MAC_NCC_va_NMS.md](../02_Kien_truc/06_Phan_mem_nhung_MAC_NCC_va_NMS.md) | Linux/IIO/DMA, driver, FSM, scheduler, QoS, bảo mật, quản trị | Embedded, network, MAC |
| [07_WBS_nhan_luc_va_lo_trinh_24_thang.md](../05_Ke_hoach_va_Kiem_thu/07_WBS_nhan_luc_va_lo_trinh_24_thang.md) | Gói công việc, đầu ra, người phụ trách, phụ thuộc, mốc quyết định | Chủ nhiệm và trưởng nhóm |
| [08_Kiem_thu_nghiem_thu_rui_ro_va_chi_phi.md](../05_Ke_hoach_va_Kiem_thu/08_Kiem_thu_nghiem_thu_rui_ro_va_chi_phi.md) | Ma trận kiểm chứng, nguồn lực lab, tiêu chí chấp nhận, rủi ro và khung dự toán | QA, tích hợp, hội đồng |
| [09_Nguon_tham_khao_va_truy_vet.md](../06_Nguon/09_Nguon_tham_khao_va_truy_vet.md) | Nguồn chính thức/project gốc, cách dùng, giới hạn bằng chứng | Người rà soát kỹ thuật |

## Cách đọc và sử dụng

- [Sx] là mã nguồn, tra đường dẫn trong file 09. Các tài liệu liên quan dùng đường dẫn tương đối để giữ nguyên khi giải nén hoặc đưa vào Git.
- **Cơ sở nguồn:** các đặc tính tiêu chuẩn/chip/project có trích dẫn. **Đề xuất thiết kế:** lựa chọn kiến trúc, nhân lực, chỉ tiêu, mốc và thuật toán triển khai do phân tích kỹ thuật trong bộ hồ sơ này đề xuất. **Ví dụ tính:** minh họa với giả thiết công khai, không phải số đo.
- Tất cả thông lượng, số trạm, ngân sách thời gian, số người và ngưỡng nghiệm thu đề xuất cần được phê duyệt tại G0. Không biến số minh họa thành yêu cầu hợp đồng khi chưa tính quỹ đường truyền và đo prototype.
- Chưa có: mã HDL hoàn chỉnh, schematic/layout, license IP, kết quả synthesis, báo giá, quỹ đường truyền cho một transponder cụ thể, chứng nhận tương thích hay kết quả thử vệ tinh. Bộ hồ sơ chỉ rõ công việc cần làm để tạo ra các sản phẩm đó.

## Năm quyết định cần khóa ở G0

1. GEO cố định, Ku qua BUC/LNB và IF L-band hay một cấu hình khác; HUB và remote có đồng vị trí feeder hay không.
2. MF-TDMA riêng hay profile DVB-RCS2; phạm vi tương thích chỉ PHY DVB-S2 hay cả signalling/network.
3. Symbol rate downstream, tổng số carrier upstream đồng thời, mức tốc độ từng remote, số remote vật lý và mô phỏng.
4. Mua hay tự làm LDPC decoder/Turbo decoder; điều kiện bàn giao source và quyền sử dụng.
5. Đầu ra nghiên cứu và mức sẵn sàng công nghệ; phần thương mại hóa/EMC/môi trường nào nằm trong 24 tháng.

Khuyến nghị triển khai một lát cắt xuyên suốt rất sớm: Ethernet → burst có timestamp → HUB thu → phản hồi timing → remote sửa → Ethernet. Nó phơi bày rủi ro hệ thống sớm hơn việc hoàn thiện riêng từng khối rồi mới nối vào cuối dự án.

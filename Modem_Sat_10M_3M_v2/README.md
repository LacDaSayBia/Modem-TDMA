# Hồ sơ modem vệ tinh HUB–VSAT — v2, baseline 10M/3M

Ngày 31/10/2026. Bộ hồ sơ nghiên cứu/thiết kế 24 tháng; chưa có firmware/RTL sản phẩm mới hay số đo chứng minh các chỉ tiêu. Đọc file này trước khi dùng bảng chỉ tiêu hoặc giao công việc.

## Thay đổi chính theo yêu cầu

- **HUB downstream IP peak ≥10 Mbit/s.** VSAT RX phải xử lý tương ứng khi được cấp dữ liệu.
- **VSAT upstream IP peak 3 Mbit/s**, khi được cấp đủ tài nguyên. Có thể shaper 3M nếu cần trần dịch vụ.
- Đề xuất sizing: QPSK downstream12,5 Msym/s và upstream5 Msym/s, mục tiêu FEC rate1/2. Upstream profile Turbo cuối phải được chọn đúng waveform và kiểm overhead.
- **HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra**, chưa là chỉ thị gốc đã phê duyệt. Không hứa ba VSAT cùng3M trên tổng6M.
- Mục tiêu timing0,25symbol tại upstream5Msym/s còn50ns, cần PoC lại clock/fractional timestamp/calibration.

Chi tiết quyết định và điều kiện đo tại [CR002](01_Yeu_cau/CR002_Baseline_10M_3M.md). Các tài liệu cũ được cập nhật v2; số ở rate thấp chỉ là ví dụ/bring-up, không phải peak sản phẩm.

## Cây thư mục và thứ tự đọc

- **00_Quan_ly/** — chỉ dẫn đọc, glossary, lịch sử thay đổi, chỉ mục máy đọc.
- **01_Yeu_cau/** — bảng chỉ tiêu HUB/VSAT, khả thi và baselineCR002.
- **02_Kien_truc/** — phân tích tổng thể, phần cứng/PHY/time/software và phân chia20mô-đun.
- **03_Mo_dun/** — đúng20file M01–M20; mỗi file có nhập môn, yêu cầu, interfaces, thực hiện, ví dụ, tests, lịch và nguồn.
- **04_Quy_uoc/** — bộ quy ước nội bộ: repo/ID/Git,RTL/CDC,DSP,time,ABI/DMA,verification,release/security và hardware/RF.
- **05_Ke_hoach_va_Kiem_thu/** — WBS24tháng, ma trận acceptance và kết quả kiểm tra hồ sơ.
- **06_Nguon/** — danh mục nguồn gốc/tiêu chuẩn/hãng/project, giới hạn bằng chứng.
- **07_Bieu_mau/** — mẫu requirement,ICD,ADR/CR,test và calibration, chưa phải record đã chạy.
- **08_Cau_hinh/** — baselineJSON và mẫu lockfile/config cho quá trình triển khai.

[FILE_INDEX.md](FILE_INDEX.md) liệt kê đầy đủ cây file với liên kết tương đối; giải nén giữ nguyên thư mục để links hoạt động. [SHA256SUMS.txt](SHA256SUMS.txt) kiểm integrity nội dung ZIP, không phải chữ ký tác giả.

## Lộ trình đọc theo người dùng

Chủ nhiệm/hội đồng: CR002 → bảng chỉ tiêu → khả thi → WBS/gates → risk/acceptance. Người mới: glossary → kiến trúc chung → M02/M06 → M08/M09/M10 → M12/M13 → M14/M15/M16. Nhóm triển khai: requirements và quy ước trước, module của mình sau, rồi đọc hai module đầu nối và ICD liên quan. QA đọc baseline→trace→tests→calibration, không chỉ xem checklistPASS.

## Cách dùng tài liệu mô-đun

Các mô-đun chia theo trách nhiệm kỹ thuật, không phải20chip hoặc20tiến trình OS. Chủ sở hữu có thể cùng người nhưng FTE không cộng hai lần. Tháng viết M1–M24 trong lịch có nghĩa projectmonth; module luôn có ID M01–M20 và tên đầy đủ để tránh nhầm.

Mỗi file dùng các nhãn PROPOSED/MODEL/MEASURED/NORM ở nơi cần; chưa có số đo mới trong bộ hồ sơ. Các chương tự thiết kế không chứng minh tuân thủ đầy đủ DVB-RCS2 hoặc tương thích iDirect. Không có báo giá/IP license/resource fit được nhà cung cấp xác nhận trong gói này.

## Điểm bắt đầu thực hiện

Trong bốn tháng đầu phải có profile/overhead accounting, BSP/IRQ/DMA ổn, FEC PoC ở tải mới, clock/sample plan cho12,5/5Msym/s, hardware-time proof và quyết định partition/link. Sau đó mới chốt PCB tích hợp. Giữ sáu tháng cuối chủ yếu cho tích hợp/đo/sửa lỗi, hạn chế mở rộng ACM/8PSK trước khi baseline10M/3M vững.

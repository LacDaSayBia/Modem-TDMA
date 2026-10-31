# Bộ quy ước chuẩn nội bộ project modem vệ tinh — v2

Trạng thái: đề xuất baseline nội bộ để đội dự án review/áp dụng; không phải tiêu chuẩn quốc gia hay chứng nhận tuân thủ DVB. Ngày 31/10/2026. Owner đề xuất: system architect; thay đổi được quản lý theo CR/ADR. Quyền quyết định yêu cầu sản phẩm thuộc chủ nhiệm kỹ thuật theo tổ chức dự án.

## 1. Mục đích và mức yêu cầu

Mục tiêu là các nhóm hardware, DSP, FPGA, Linux, MAC và QA dùng cùng đơn vị, mốc thời gian và giao diện. Quy ước có tính bắt buộc sau khi được đội dự án baseline; không tự biến lựa chọn nội bộ thành yêu cầu của ETSI/ADI.

Dùng MUST/MUST NOT/SHOULD/MAY theo ý nghĩa mức yêu cầu của RFC2119/8174 [R18](../06_Nguon/Nguon_kiem_chung_v2.md); chỉ uppercase có ý nghĩa quy phạm. Trong tiếng Việt: PHẢI, KHÔNG ĐƯỢC, NÊN, CÓ THỂ là bản diễn đạt tương ứng trong tài liệu nội bộ, scope nêu ở đầu file. SHOULD có ngoại lệ khi có lý do và đánh giá tác động; không cần lập một vòng xin phép người dùng cho mọi lựa chọn implementation.

## 2. Thứ tự ưu tiên và nguồn chân lý

Yêu cầu người dùng/hợp đồng hiện hành → requirement baseline và CR đã chốt → ICD/profile được review → design module → code/config → ví dụ/bài học. Với tuyên bố conformance, yêu cầu normative của chuẩn đúng version được ưu tiên trong phạm vi đã chọn; sai khác phải công bố. Không chọn code hiện chạy làm tiêu chuẩn để đổi yêu cầu đo.

[Baseline CR002](../01_Yeu_cau/CR002_Baseline_10M_3M.md) và [JSON baseline](../08_Cau_hinh/baseline_v2.json) là dữ liệu tốc độ hiện hành. Tài liệu tổng hợp trước được cập nhật v2, các ví dụ tốc độ thấp là bài minh họa. Sửa thông số ở một file mà không cập nhật source-of-truth và impact list là lỗi quy trình.

## 3. Danh mục quy ước

| File | Nội dung | Nhóm áp dụng |
|---|---|---|
| [01](01_Repo_ID_Git_va_tai_lieu.md) | Cây repo, tên file, ID, trace, Git và tài liệu | Tất cả |
| [02](02_RTL_clock_reset_CDC_constraints.md) | RTL, clock/reset/CDC, AXI/constraints và lint | FPGA/hardware |
| [03](03_DSP_don_vi_fixedpoint_IQ.md) | Đơn vị, IQ, fixed-point, LLR và binary vectors | DSP/FPGA/QA |
| [04](04_Time_epoch_timing_sign.md) | Timeline, timestamp, correction sign, epochs và timed TX | System/PHY/MAC |
| [05](05_Interface_ABI_wire_DMA.md) | Binary wire/control proposal, PS–PL ABI, DMA ownership | Embedded/FPGA/MAC |
| [06](06_Verification_trace_va_calibration.md) | Test IDs, evidence, calibration, pass/fail và CI | QA/tất cả |
| [07](07_Build_release_security_license.md) | Build/version/update/security/license/recovery | Embedded/release |
| [08](08_HW_RF_calibration_va_bien_ban.md) | Hardware/RF/IFL, datasheet limits, DFT và review | Hardware/RF/system |

## 4. Quy tắc chung bắt buộc

1. Mọi đại lượng có đơn vị/reference point; IP bytes khác coded bits, dB khác dBm, sample khác symbol.
2. Mọi module boundary có version, owner và golden transaction; struct native không phải wire ABI.
3. Clock/reset/CDC và buffer ownership được viết trước tích hợp; không giấu overflow/underflow bằng retry vô hạn.
4. TX permit cuối ở hardware: clock, grant, epoch, buffer và RF safety đều hợp lệ.
5. Mọi source/vendor IP có origin/revision/license; không ghi credentials/key thật trong source hoặc sample configs.
6. Mọi kết quả có build/config/profile/calibration IDs; NOT_RUN/TBD không được ghi PASS.
7. Không có con số “mặc định sai số đo” cho mọi tham số; uncertainty và decision rule theo test.

## 5. Cách đưa quy ước vào vận hành

M1: review các conventions và owner; M2: lint/checklist/template áp cho code mới; M4: ICD/ABI/profile version1 và CI smoke; M8: regression tích hợp/time/RF; M18: freeze interfaces bàn giao. Code vendor giữ format/license gốc, bao bằng adapter; không đổi style toàn bộ vendor để giống project rồi mất khả năng cập nhật.

Ngoại lệ có record EXC-ID: rule, lý do, scope/version, risk, mitigation, test và thời hạn review. Trưởng miền cùng system architect quyết định theo phân quyền sẵn có; lỗi unsafe TX hoặc thiếu integrity không được waiver chỉ để hoàn thành gate. Bộ quy ước không tự khẳng định được thực thi bởi tooling; quy tắc nào đã check tự động được ghi trong validation report.

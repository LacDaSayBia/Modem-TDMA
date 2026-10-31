# Lịch sử thay đổi CR002

## 2.0 — 31/10/2026

Yêu cầu người dùng: nâng HUB downstream max lên≥10Mbps và VSAT upstream max3Mbps; tạo20file mô-đun, xây quy ước và ZIP cây thư mục logic.

Thay baselineIP4/0,7 bằng10/3; đề xuất nâng aggregateHUB1,4 lên6Mbit/s/2carrier. Thêm downstream12,5 và upstream5Msym/s vào tập cấu hình; giữ các rate thấp cho bring-up. DownstreamQPSK1/2 ideal10Msym/s không đủ10IP nên không dùng10Msym/s làm cấu hình chứng minhpeak.

Cập nhật12tài liệu đã tạo, gồm10tài liệu bộ trước và2file chỉ tiêu/phân tích. Bổ sung20module chi tiết giữ nguyên mã M01–M20;9file quy ước, baselineJSON/CR, tài liệu nguồn và biểu mẫu. Không đưa bản thông số cũ thành active trongZIP; các numericalexamples rate thấp có nhãn giải thích.

Tác động chính: decoder/LLRload, sample/resampler ratios, RFspan/channelization, return symbol timing từ250ns ở1Msym/s thành50ns ở5Msym/s, capacity/control/QoS và acceptance load. Nhân lực/tiến độ24tháng giữ định hướng nhưng G1 phải đánh giá lại risk; không có cam kết phần cứng đạt trước PoC.

## Quy tắc thay đổi tiếp theo

CR tiếp theo phải có requirementID, origin, old/new value, impactmodules/interfaces/test/clock/RF/IP/license, owner và gate. Không sửa chỉ một bảng rồi bỏ các testconditions cũ. Ghi rõ DERIVED/PROPOSED nếu chỉ tiêu được suy ra để đáp ứng mục tiêu gốc.

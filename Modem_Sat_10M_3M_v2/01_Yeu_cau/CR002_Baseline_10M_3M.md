# CR-002 — Baseline thông lượng HUB 10 Mbit/s và VSAT 3 Mbit/s

Phiên bản 2.0; 31/10/2026. Trạng thái: yêu cầu tốc độ theo người dùng; phương án PHY và chỉ tiêu suy ra là đề xuất kỹ thuật cần kiểm chứng. Mọi tài liệu trong gói áp dụng baseline này.

## 1. Yêu cầu và cách diễn giải

| Mã yêu cầu | Nội dung | Trạng thái |
|---|---|---|
| REQ-SYS-DS-001 | Tốc độ IP cực đại hỗ trợ của HUB downstream không nhỏ hơn 10.000.000 bit/s | Người dùng yêu cầu |
| REQ-SYS-US-001 | VSAT hỗ trợ upstream IP 3.000.000 bit/s khi được cấp tài nguyên tương ứng | Người dùng yêu cầu |
| REQ-DER-RX-001 | VSAT RX xử lý được downstream IP ≥10 Mbit/s khi dữ liệu được cấp cho trạm đó | Suy ra bắt buộc để sử dụng downstream |
| REQ-DER-HUBUS-001 | Đề xuất HUB RX xử lý ≥3 Mbit/s mỗi carrier, ≥6 Mbit/s tổng hai carrier đồng thời | Đề xuất kiến trúc, cần phê duyệt |
| REQ-SYS-NET-001 | Ít nhất 3 VSAT vật lý gia nhập; HUB thu đồng thời ≥2 carrier | Giữ từ baseline trước |
| REQ-DER-DUPLEX-001 | Kiểm downstream ≥10 và upstream tổng ≥6 Mbit/s đồng thời | Mục tiêu kiểm chứng suy ra theo kiến trúc đề xuất |

“Max 3 Mbps” được diễn giải là chế độ hỗ trợ tốc độ IP 3 Mbit/s, không bắt buộc hardware có giới hạn vật lý đúng bằng 3. Nếu cần trần dịch vụ 3 Mbit/s, dùng shaper/token bucket. Không có yêu cầu ba VSAT đều 3 Mbit/s đồng thời trên tổng uplink 6 Mbit/s. Trong bài peak, hai trạm phát tốc độ cao, trạm còn lại vẫn có tài nguyên signalling/keepalive. Downstream 10 Mbit/s là tổng carrier, không phải băng thông riêng bảo đảm cho từng trạm.

## 2. Cấu hình PHY để sizing

| Tham số | Downstream | Upstream |
|---|---|---|
| Carrier | 1 carrier liên tục | 2 carrier thu đồng thời tại HUB |
| Điều chế cơ sở | QPSK | QPSK burst |
| FEC | BCH + LDPC, normal frame, rate 1/2 | Một profile Turbo TC-LM mục tiêu rate 1/2; phải chọn đúng waveform hợp lệ |
| Symbol rate mục tiêu peak | 12,5 Msym/s | 5 Msym/s mỗi carrier |
| Rate thấp phục vụ bring-up | 1/2/5 Msym/s | 0,25/0,5/1/2 Msym/s |
| Roll-off dùng sizing | 0,25 | 0,25 là ứng viên, chốt theo profile |
| Băng thông xấp xỉ Rs(1+α) | 15,625 MHz | 6,25 MHz/carrier |
| Dung lượng lý tưởng Rs×2×1/2 | 12,5 Mbit/s | 5 Mbit/s/carrier |
| Tổng hiệu suất tối thiểu cần để đạt IP | 80% | 60% để đạt 3 Mbit/s/carrier |

Hiệu suất ở đây đã bao gồm mọi overhead so với ideal rate: framing, BCH outer overhead, pilots, GSE/headers, control, guard/ramp, padding, unused grants và lỗi. Hai tỷ lệ 80%/60% là **điều kiện cần**, không là kết quả đã đo. Thiết kế phải có margin thay vì vừa chạm giới hạn. Cần bảng accounting byte/symbol theo profile cuối và quỹ đường truyền hỗ trợ MODCOD.

QPSK rate 1/2 ở 10 Msym/s có ideal 10 Mbit/s trước overhead nên không thể dùng để cam kết 10 Mbit/s IP thực. Có thể chọn 10 Msym/s rate cao hơn thay phương án 12,5 Msym/s, nhưng cần thêm mode/FER/link margin; chỉ thay qua ADR/CR. Tương tự không giữ upstream 1 Msym/s rồi chỉ sửa yêu cầu IP thành 3 Mbit/s.

## 3. Clock, FEC và timing chịu tác động

Sample rate 30,72 MS/s là ứng viên cho nghiên cứu, không phải cấu hình AD9361 đã xác nhận trên board. Downstream 12,5 Msym/s tương ứng 2,4576 samples/symbol, cần resampling/timing interpolation phù hợp; không giả định hệ số 2 nguyên. Upstream 5 Msym/s cũng cần clock-enable/rational interpolation. Rate chain FDD, FIR, interface và filter bandwidth phải kiểm tại G1.

LLR QPSK 12,5 Msym/s với 6 bit/LLR có envelope 150 Mbit/s trước trừ pilot/header. Decoder phải sizing theo coded arrivals và max iterations. Với n=64.800, envelope coded 25 Mbit/s tương ứng ~385,8 frame/s, ngân sách ~2,592 ms/frame; framing thực thay đổi nhịp nên cần tính đúng và đo worst case.

Ở 5 Msym/s, Ts=200 ns; 0,25Ts=50 ns. Bảng budget 250 ns tại 1 Msym/s trong tài liệu cũ chỉ là ví dụ rate thấp. Tại max rate cần fractional estimator, launch/calibration tốt hơn; bước sample ở 30,72 MS/s là ~32,55 ns. Độ phân giải counter không thay accuracy RF. Nếu PoC không đạt 50 ns, phải review timing/guard và chỉ tiêu bằng CR, không tự bỏ ngưỡng.

## 4. Điều kiện đo peak

UDP gói IP 1.500 byte; đếm toàn bộ byte gói IP thành công, không đếm Ethernet/FEC/guard. Đề xuất phép đo ≥10 phút sau ổn định; packet loss mục tiêu ≤10^-5 ở high-SNR có calibration, không duplicate/corrupt packet, đồng thời báo offered load và queue overflow. Đây là tiêu chí đề xuất mới để kết quả thông lượng có ý nghĩa.

Trình tự: chứng minh riêng từng hướng → song công theo valid config → multiuser có signalling đầy đủ → thêm GEO delay/drift → quét SNR và QoS overload. Chỉ kết luận peak trong cấu hình cấp tài nguyên đã ghi; CIR/SLA dưới tải nhiều trạm phải xác định riêng. Các tham số packet loss/high-SNR được khóa tại G1 trước nghiệm thu.

## 5. Phê duyệt và đóng thay đổi

M1–M2 cập nhật SRS/trace; M4 có capacity model, FEC synthesis, sample/clock plan và timing PoC mới; M8 chạy profile thấp rồi tăng rate; M12 đạt peak lab nếu các gate trước đạt; M18 freeze cấu hình cuối; M22–M24 nghiệm thu. Tăng yêu cầu tốc độ làm giảm dự phòng tiến độ; IP decoder và chuyên môn timing/burst cần ưu tiên sớm. Không kéo các tính năng mở rộng ACM/8PSK vào đường găng khi baseline peak chưa ổn.

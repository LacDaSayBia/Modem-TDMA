# Thuật ngữ và lộ trình nhập môn

| Thuật ngữ | Giải thích trong project |
|---|---|
| HUB / VSAT | Trạm trung tâm / trạm đầu cuối |
| NCC | Bộ điều phối: cấp tài nguyên và quản lý trạng thái terminal |
| Downstream / upstream | HUB→VSAT / VSAT→HUB |
| Carrier / burst / slot | Sóng mang / đợt phát ngắn / khoảng tài nguyên thời gian |
| MF-TDMA | Chia tài nguyên cả tần số lẫn thời gian, HUB có thể nhận nhiều carrier cùng lúc |
| PHY / MAC | Xử lý tín hiệu vật lý / quy tắc truy nhập và cấp phát |
| Symbol / sample / bit | Phần tử điều chế / mẫu IQ / đơn vị nhị phân; ba tốc độ khác nhau |
| FEC / LDPC / BCH / Turbo | Mã sửa lỗi; từng họ mã phải có profile và bit order cụ thể |
| LLR | Độ tin cậy mềm của bit để decoder khai thác |
| Acquisition / tracking | Bắt ban đầu / bám trạng thái sau khi bắt |
| CFO / SRO | Lệch tần số carrier / lệch tốc độ lấy mẫu |
| DDC / DUC / NCO | Dịch xuống / lên tần số số và dao động điều khiển số |
| RRC / UW | Lọc tạo dạng phối hợp / chuỗi symbol biết trước để bắt burst |
| Ranging / timing advance | Đo sai lệch arrival / điều chỉnh phát sớm để đến đúng khe |
| Epoch / grant | Phiên timeline / quyền phát được cấp |
| Clock / timestamp | Nhịp vật lý / bản ghi mốc một sự kiện |
| PS / PL / CDC | CPU Zynq / logic lập trình / qua miền clock |
| DMA / IRQ / ABI | Truyền bộ nhớ trực tiếp / ngắt / giao diện nhị phân |
| IFL / ODU / BUC / LNB | Cáp-giao tiếp tới thiết bị ngoài trời / thiết bị ngoài / nâng tần công suất / hạ tần nhiễu thấp |
| Golden vector / bit-accurate | Dữ liệu chuẩn đối chiếu / model mô tả đúng lượng tử và bit operations |
| Synthesis / place-and-route | Tổng hợp logic / bố trí định tuyến thực để biết fit và timing |
| Peak / CIR / aggregate | Cực đại khi đủ tài nguyên / tốc độ dịch vụ bảo đảm / tổng nhiều luồng |
| TBD / PoC / gate / FTE | Chưa chốt / bằng chứng khả thi / mốc quyết định / nhân lực toàn thời gian tương đương |

## Bài đọc theo thứ tự

1. Hiểu IQ và quan hệ sample-symbol-bit ở M02, M06 và quy ước DSP.
2. Đọc HUBTX→VSATRX→FEC ở M08–M10, tự tạo một vector sạch trước khi thêm nhiễu.
3. Đọc upstreamTX/RX/FEC ở M11–M13 để hiểu vì sao burst khó hơn carrier liên tục.
4. Đọc M14–M16 và ví dụ hai remote khác delay; phân biệt clock, epoch và bù propagation.
5. Đọc M17/M18 về packet/DMA/QoS, sau đó M19/M20 về vận hành và chứng cứ nghiệm thu.

Một bài học phải kết thúc bằng input/output có đơn vị, ví dụ đúng/lỗi và phép quan sát. Không bắt đầu bằng viết toàn bộ modem hoặc sao chép Tcl/DT mà không hiểu reference design đang làm gì.

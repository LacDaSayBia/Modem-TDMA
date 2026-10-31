# 01. Phạm vi nhiệm vụ và đánh giá khả thi

> **Cập nhật CR-002 — 31/10/2026:** HUB downstream IP cực đại hỗ trợ **≥10 Mbit/s**; VSAT upstream IP cực đại **3 Mbit/s** khi được cấp đủ tài nguyên. Phương án sizing: downstream QPSK 12,5 Msym/s, rate 1/2; upstream QPSK tới 5 Msym/s, một Turbo profile mục tiêu rate 1/2. Đề xuất nâng HUB upstream lên **≥6 Mbit/s tổng/2 carrier**; đây là chỉ tiêu suy ra để phê duyệt, không phải yêu cầu người dùng đã chốt. Các rate thấp chỉ phục vụ bring-up. Xem [baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md); ví dụ số ở rate thấp vẫn là ví dụ, không là trần tốc độ sản phẩm. Tại upstream 5 Msym/s, mục tiêu timing 0,25 symbol tương ứng **50 ns**, phải kiểm chứng lại.

## 1. Định nghĩa đúng đối tượng cần chế tạo

Modem remote thực hiện thu downstream và phát upstream. Nhưng để chứng minh remote hoạt động MF-TDMA, dự án còn phải tạo HUB thử nghiệm có bộ phát downstream, thu burst đa tần và NCC (Network Control Centre). NCC cấp tài nguyên, điều khiển gia nhập mạng và gửi lệnh hiệu chỉnh. Chỉ có một cặp thiết bị truyền được I/Q hoặc ping qua cáp chưa chứng minh được mạng Star MF-TDMA.

Giả thiết cơ sở của phương án: vệ tinh GEO transparent/bent-pipe; HUB phát một sóng mang downstream liên tục; nhiều remote chia sẻ tối thiểu hai sóng mang upstream; remote cố định trong giai đoạn nghiệm thu chính. Vệ tinh không xử lý MAC. Liên lạc remote–remote, nếu có, đi qua HUB và thường trải qua hai chặng vệ tinh. Mạng chuyển động, beam handover, LEO và trải phổ là phạm vi mở rộng, không mặc nhiên bao gồm.

## 2. Phân biệt bốn lớp tương thích

| Lớp | Ý nghĩa | Điều không được suy ra |
|---|---|---|
| DVB-S2 PHY | Tín hiệu downstream đúng framing, mapping, FEC và profile được công bố | Chưa chứng minh truyền IP hoặc gia nhập mạng |
| Đóng gói dữ liệu | TS/private encapsulation hoặc GSE phù hợp hai đầu | Chưa tương thích signalling HUB khác |
| MF-TDMA | Tài nguyên chia theo tần số và thời gian | Chưa phải DVB-RCS2 |
| Hệ thống thương mại | Waveform, signalling, authentication, NMS, cấp phép và vận hành cụ thể | Không thể suy ra từ việc đọc datasheet X5 |

DVB-S2 và DVB-RCS2 là hai tập tiêu chuẩn khác nhau [S1–S3]. Nếu chọn burst/FEC/signalling riêng, chỉ được công bố “DVB-S2 downstream; MF-TDMA upstream theo giao thức của đề tài”. Không công bố tuân thủ đầy đủ DVB-RCS2 từ một số chức năng tham khảo.

## 3. Đối chiếu iDirect X5 có kiểm soát phạm vi

Nguồn [S4] là brochure do iDirect biên soạn, lưu trên máy chủ đơn vị khác, mã 0810. Nó mô tả cấu hình lịch sử; không dùng làm khẳng định tính năng của mọi phiên bản X5 hay tình trạng hỗ trợ hiện tại. Không tìm thấy tài liệu giao thức nội bộ hoặc source iDirect để làm cơ sở tương thích HUB.

| Hạng mục tham chiếu từ brochure | Ý nghĩa cho nhiệm vụ | Khuyến nghị 24 tháng |
|---|---|---|
| Star, DVB-S2/ACM outbound, MF-TDMA inbound | Cần hệ thống hai chiều có điều phối | Bắt buộc Star; CCM trước, ACM sau |
| Các chế độ outbound DVB-S2 và iNFINITI | Turbo ở chế độ khác không phải FEC DVB-S2 | Chỉ làm DVB-S2 BCH/LDPC downstream |
| QoS, timing/frequency/power control | Chức năng hệ thống quan trọng ngoài PHY | Làm mức tối thiểu đo kiểm được |
| NMS, authentication | Modem là thiết bị mạng được quản lý | Có provisioning, log, thống kê, cập nhật |
| Cấp nguồn và reference cho BUC/LNB | AD9361 không thay mạch IFL | Làm module RF/IFL riêng |
| 45 Msym/s downstream, 7,5 Msym/s upstream trong bản brochure | Là trần cấu hình tham chiếu, không phải cam kết của phần cứng đề tài | Không lấy đồng loạt làm chỉ tiêu ban đầu |

Không dùng chung “bit rate”: coded bit rate, information bit rate, carrier IP rate và lưu lượng IP từng remote là những đại lượng khác nhau. So sánh thiết bị phải dùng cùng packet size, MODCOD, cấu hình song công, QoS và điều kiện RF.

## 4. Chỉ tiêu sơ bộ đề xuất để lập kế hoạch

Các số dưới đây là **mục tiêu thiết kế đề xuất**, chưa phải khả năng đã được xác nhận. G0 có thể điều chỉnh; G1 phải kiểm tra bằng mô hình và synthesis. Chọn mục tiêu vừa sức để ưu tiên làm chủ hệ thống.

| Tham số | Mức cơ sở phải đạt | Mức mở rộng sau G3 |
|---|---|---|
| Downstream | DVB-S2 QPSK, CCM, pilot; 1–12,5 Msym/s | 8PSK và ACM; tốc độ ngoài tập cơ sở sau sizing cho tập MODCOD đã kiểm chứng |
| FEC downstream | BCH + LDPC; bắt đầu một MODCOD 1/2 và một kích thước FECFRAME được khai báo | Thêm rate/frame length theo nguồn lực |
| Upstream | QPSK burst; 0,25–5 Msym/s mỗi carrier; ≥2 carrier HUB thu đồng thời | 4 carrier; rate cao hơn nếu tài nguyên cho phép |
| FEC upstream | Chọn chính xác một profile Turbo TC-LM tham khảo RCS2, hoặc một mã riêng được ghi rõ | Thêm rate; không phát triển nhiều họ mã đồng thời |
| Số remote | 3 remote vật lý; thêm tải mô phỏng để đánh giá scheduler ≥16 remote logic | 8 remote vật lý nếu kinh phí |
| Đổi carrier | Một remote được cấp khe trên ít nhất hai carrier; lịch không xung đột | Cấp phát động nhiều carrier hơn |
| Gia nhập | Logon → ranging → được cấp khe → hoạt động → mất đồng bộ tự khóa TX | Tự khôi phục và kiểm thử tải logon lớn |
| Dịch vụ | IPv4 unicast, 2–3 hàng đợi QoS, static route; Ethernet | VLAN, thêm policy, tối ưu TCP riêng |
| Kênh thử | IF có trễ GEO mô phỏng + thử vệ tinh khi có điều kiện | Môi trường/rain fade nâng cao |
| Độ bền | Bài soak 72 giờ có log và điều kiện công khai | Thử môi trường theo hồ sơ sản phẩm |

Không cộng các giá trị cực đại riêng lẻ để cam kết tất cả đồng thời. Phải có bảng cấu hình hợp lệ: Rs, MODCOD, carrier count, số decoder, thông lượng, công suất và nhiệt. Chế độ chính xác cho normal/short FECFRAME được quyết định sau PoC LDPC, không giả định short frame luôn được mọi bộ phát tham chiếu hỗ trợ.

## 5. Đánh giá toàn diện theo miền kỹ thuật

| Miền | Phải làm chủ | Điểm khó thật sự | Đánh giá và cách giảm rủi ro |
|---|---|---|---|
| Kiến trúc hệ thống | Profile, interface, thời gian, chuẩn, quỹ đường truyền | Các nhóm dùng khác mốc thời gian/đơn vị/dấu | Rủi ro cao; kiến trúc sư giữ ICD và kiểm thử xuyên suốt |
| DVB-S2 RX | Acquisition, tracking, soft LLR, FEC, BBFRAME | Giải mã đạt tốc độ ở SNR thấp và frequency offset thực tế | Khả thi với subset; PoC decoder và receiver đầu kỳ |
| Upstream PHY | Burst generation/receiver, AGC, estimator | Mỗi burst có pha, CFO, công suất, timing khác nhau | Khó hơn demo sóng mang liên tục; có bộ test near-far |
| MF-TDMA | Time-frequency map, grant, request, collision/logon | HUB nhận đồng thời nhiều carrier, scheduler không trễ | Khả thi khi hạn chế carrier/rate, cần NCC riêng |
| Đồng bộ | Frequency discipline, timestamp, ranging, timing correction | Trễ truyền khác nhau, latency pipeline, drift, vòng phản hồi GEO | Rủi ro hệ thống cao nhất; PL thực thi timed TX |
| FEC | LDPC/BCH decoder; Turbo nếu chọn | BRAM, routing, số vòng lặp, throughput worst case | Rủi ro cao; mua IP hoặc chuyên gia riêng |
| RF/IFL | FDD, blocking, reference, DC/10 MHz, bảo vệ | Rò TX vào RX, reference spur, gain/transient BUC | Cần RF engineer; thử block-level trước PCB tích hợp |
| PS–PL | DMA, IRQ, FIFO, cache, timestamp | Demo DMA chạy chưa bảo đảm deadline burst | Tách I/Q debug khỏi đường packet hoạt động |
| Liên FPGA | CDC, framing, link budget số, reset | Hai FPGA tăng điểm lỗi và latency | Chỉ dùng khi PoC chứng minh lợi ích |
| Linux/network | Boot, driver, queues, QoS, update | Linux không bảo đảm mốc phát từng mẫu | Linux điều khiển; PL quyết định đúng thời điểm |
| HUB/NMS | Multiuser state, scheduling, quản trị | Một lỗi grant ảnh hưởng cả mạng | Cần test mô phỏng nhiều remote và fault injection |
| Sản xuất | PCB, SI/PI, DFT, thermal, BOM | Nhiều vòng PCB trong 24 tháng | Dev board năm đầu; bố trí 2 vòng PCB |
| Đo kiểm | Reference độc lập, BER/PER, timing/phổ | Hai thiết bị cùng lỗi vẫn tự tương thích | Đo chéo và golden vectors độc lập |

## 6. Giới hạn phần cứng dự kiến

Zynq-7020/7030 có thể làm nền tảng, nhưng không có bằng chứng đủ tài nguyên cho toàn bộ cấu hình trước synthesis/place-and-route. Số DSP không quyết định riêng khả năng LDPC: BRAM, băng thông message passing, LUT và routing thường quan trọng. Thêm FPGA không tự động làm decoder nhanh hơn nếu giao tiếp phải chuyển lượng LLR quá lớn hoặc latency không kiểm soát.

AD9361 phù hợp tầng RF/IF của SDR [S5–S6]; nó không tích hợp modem DVB-S2, MF-TDMA, bộ giải mã LDPC hay NCC. BUC/LNB chuyển đổi Ku và công suất phát vẫn là phần ngoài. Xem tính toán băng thông và hai phương án liên FPGA ở file 03.

## 7. Điều kiện nguồn lực và mức khả thi

| Kịch bản tổ chức | Đánh giá trong 24 tháng |
|---|---|
| 8–10 FTE bình quân, có chuyên gia FEC/burst PHY, IP có thể mua, lab đủ | Hệ thống mẫu giới hạn profile khả thi có điều kiện |
| 4–5 người làm kiêm nhiệm, cùng học Linux/FPGA/FEC từ đầu | Rủi ro cao; nên giảm thành PoC một carrier TDMA rồi MF-TDMA lab |
| Tự làm mọi FEC, nhiều MODCOD, HUB thương mại, mobility, tương thích X5 | Không có cơ sở cam kết 24 tháng |
| Phải tương thích HUB iDirect nhưng không có SDK/protocol/license/đối tác | Không thể lập kế hoạch kỹ thuật đáng tin chỉ từ brochure |

FTE là nhân lực làm việc toàn thời gian tương đương. Các con số là ước lượng lập kế hoạch, không phải định mức ngành. Cần phỏng vấn/đánh giá thực lực từng người và tính phần thời gian cho nghiên cứu học tập.

## 8. Những vấn đề phải giải quyết trước khi phê duyệt chính thức

Chưa có băng thông thuê vệ tinh, EIRP/G/T, antenna/BUC/LNB, mức C/N mục tiêu và availability nên chưa thể kết luận đường truyền đủ dự trữ, nhất là mưa Ku. Chưa có license và synthesis nên chưa thể chốt 7020 hay 7030 và FPGA phụ. Chưa có yêu cầu môi trường nên chưa thể tính toàn bộ chi phí sản phẩm.

Đề nghị nghiệm thu theo profile công bố, bộ đo có truy vết và cấu hình cụ thể. Mục tiêu làm chủ công nghệ nên thể hiện bằng source, model, tài liệu thiết kế, test vector, khả năng thay đổi cấu hình và phân tích lỗi; không chỉ bằng một buổi demo truyền file.

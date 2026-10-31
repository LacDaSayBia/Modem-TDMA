# BẢNG TỔNG HỢP CHỈ TIÊU KỸ THUẬT VÀ TÍNH NĂNG MODEM HUB, MODEM VSAT

> **Cập nhật CR-002 — 31/10/2026:** HUB downstream IP cực đại hỗ trợ **≥10 Mbit/s**; VSAT upstream IP cực đại **3 Mbit/s** khi được cấp đủ tài nguyên. Phương án sizing: downstream QPSK 12,5 Msym/s, rate 1/2; upstream QPSK tới 5 Msym/s, một Turbo profile mục tiêu rate 1/2. Đề xuất nâng HUB upstream lên **≥6 Mbit/s tổng/2 carrier**; đây là chỉ tiêu suy ra để phê duyệt, không phải yêu cầu người dùng đã chốt. Các rate thấp chỉ phục vụ bring-up. Xem [baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md); ví dụ số ở rate thấp vẫn là ví dụ, không là trần tốc độ sản phẩm. Tại upstream 5 Msym/s, mục tiêu timing 0,25 symbol tương ứng **50 ns**, phải kiểm chứng lại.

**Nhiệm vụ:** Nghiên cứu, thiết kế, chế tạo modem vệ tinh mạng hình sao.

**Thời gian thực hiện:** 24 tháng. **Ngày tổng hợp:** 31/10/2026.

**Nền tảng dự kiến:** Zynq-7030/7020, FPGA bổ trợ theo nhu cầu tài nguyên, AD9361 và khối RF/IFL ngoài.

## 1. Phạm vi và quy ước

Tài liệu tổng hợp các chỉ tiêu đã đề xuất thành hai bộ riêng cho modem HUB và modem VSAT. Đây là **mục tiêu thiết kế cho hệ thống mẫu nghiên cứu**, chưa phải thông số thiết bị đã đo kiểm. Các chỉ tiêu cần hoàn thiện được đánh dấu rõ, phải khóa trước khi phát hành yêu cầu nghiệm thu chính thức.

- Downstream: HUB → VSAT; upstream: VSAT → HUB.
- Mạng cơ sở: Star, vệ tinh GEO transparent, các VSAT cố định.
- HUB gồm bộ phát downstream và bộ thu upstream đa carrier. NCC là chức năng điều phối mạng; trong mẫu nghiên cứu có thể chạy trên máy tính đi kèm HUB. Những hàng ghi “HUB/NCC” thuộc đầu ra hệ thống HUB, không mặc nhiên bắt buộc nằm trong một vỏ modem.
- Chỉ tiêu “cơ sở” thuộc phạm vi đề xuất nghiệm thu; “mở rộng” chỉ triển khai khi đủ nguồn lực và vượt mốc kiểm chứng.
- MF-TDMA upstream theo profile nhiệm vụ có tham khảo DVB-RCS2. Không mặc nhiên công bố tuân thủ đầy đủ DVB-RCS2 hoặc tương thích HUB/modem iDirect.
- Dải RF/IF và các đại lượng mức tín hiệu được xác định tại connector modem; công suất cấp BUC/LNB được tách khỏi công suất tiêu thụ phần modem.

## 2. Chỉ tiêu kỹ thuật và tính năng riêng cho modem HUB

### 2.1. Kiến trúc, dung lượng và giao thức

| STT | Tham số/chức năng | Mức cơ sở đề xuất | Điều kiện/ghi chú |
|---|---|---|---|
| H01 | Vai trò hệ thống | Trạm trung tâm mạng Star | Kết nối mạng IP trung tâm với các VSAT |
| H02 | Chế độ hoạt động | Phát downstream và thu upstream đồng thời | FDD; kiểm chứng song công |
| H03 | Downstream | Phát DVB-S2 | Tập cấu hình hỗ trợ được công bố |
| H04 | Upstream | Thu MF-TDMA | Burst profile xác định trước nghiệm thu |
| H05 | Số carrier downstream | 01 carrier liên tục | Duy trì reference và signalling khi không có user traffic |
| H06 | Số carrier upstream | Thu đồng thời ít nhất 02 carrier | Có burst chồng thời gian trên hai carrier |
| H07 | Số VSAT kiểm chứng vật lý | Ít nhất 03 VSAT hoạt động trong cùng mạng | Không thay bằng các luồng dữ liệu giả lập |
| H08 | Quy mô điều phối mô phỏng | Ít nhất 16 VSAT logic | Chỉ chứng minh MAC/NCC, chưa phải 16 thiết bị RF |
| H09 | Thông lượng IP downstream toàn mạng | Tốc độ IP cực đại hỗ trợ không nhỏ hơn 10 Mbit/s | Cấu hình đo tại mục 5 |
| H10 | Thông lượng IP upstream mỗi carrier | Tốc độ IP cực đại hỗ trợ đạt 3 Mbit/s | Cấu hình đo tại mục 5 |
| H11 | Tổng thông lượng IP upstream | Đề xuất không nhỏ hơn 6 Mbit/s tổng trên 02 carrier | Kiểm đồng thời với downstream |
| H12 | Cấp phát tài nguyên HUB/NCC | Hỗ trợ cấp phát tĩnh và động theo nhu cầu lưu lượng | Phân bổ cả khe thời gian và carrier |
| H13 | Ethernet dữ liệu | Ít nhất 01 cổng 10/100/1000BASE-T | Tốc độ cổng không đồng nghĩa tốc độ qua vệ tinh |
| H14 | Giao thức dữ liệu | IPv4, ICMP, UDP, TCP | Đo throughput bằng UDP; đo TCP riêng |
| H15 | Định tuyến | Static routing | Cấu hình được từ giao diện quản trị |
| H16 | MTU IP | Hỗ trợ 1.500 byte | Phân mảnh/đóng gói nội bộ không làm mất khả năng vận chuyển gói |
| H17 | QoS HUB/NCC | Ít nhất 03 lớp: điều khiển, ưu tiên, best effort | Bảo đảm tài nguyên cho signalling khi quá tải |

### 2.2. Phát downstream và thu upstream

| STT | Tham số/chức năng | Mức cơ sở đề xuất | Điều kiện/ghi chú |
|---|---|---|---|
| H18 | Điều chế phát downstream | QPSK | 8PSK là mở rộng |
| H19 | FEC phát downstream | BCH ngoài + LDPC trong | Theo DVB-S2; Turbo không thay thế FEC này |
| H20 | Tỷ lệ mã downstream | 1/2 | 2/3 là bổ sung ưu tiên |
| H21 | FECFRAME downstream | Normal frame, 64.800 bit | Đúng bảng tham số của rate được chọn |
| H22 | Tốc độ symbol downstream | 1; 2; 5; 12,5 Msym/s | Các cấu hình rời rạc được kiểm chứng |
| H23 | Chế độ coding/modulation | CCM | ACM là mở rộng |
| H24 | Pilot downstream | Có hỗ trợ chèn pilot | Theo cấu hình DVB-S2 |
| H25 | Roll-off downstream | 0,25 | Các giá trị khác là bổ sung |
| H26 | Điều chế thu upstream | QPSK burst | Thu độc lập phase, CFO, timing của từng burst |
| H27 | FEC thu upstream | Một profile Turbo TC-LM xác định | Khóa waveform ID, codeblock, interleaver, puncturing và mapping |
| H28 | Tỷ lệ mã upstream | Ưu tiên 1/2 nếu có trong waveform được chọn | Phải ghi rate chính xác trước nghiệm thu |
| H29 | Tốc độ symbol upstream mỗi carrier | 0,25; 0,5; 1; 2; 5 Msym/s | Khai báo các tổ hợp chạy đồng thời được hỗ trợ |
| H30 | Xử lý cấu trúc burst | Preamble/UW, payload, FEC, CRC và phần kết thúc theo profile | Kiểm cả burst có lỗi và không nhận dạng được |
| H31 | Thu đa carrier | Tách và giải mã ít nhất 02 carrier đồng thời | Wideband RX + DDC/channelizer hoặc các receiver song song |
| H32 | Đo chất lượng upstream | Arrival timestamp, CFO, mức tín hiệu/chất lượng và trạng thái FEC/CRC | Có định nghĩa đơn vị và điểm chuẩn |
| H33 | Hiệu năng giải mã | Đo FER theo Es/N0 cho từng cấu hình | Mục tiêu implementation loss ≤1 dB tại FER 10^-3 so mô hình cùng profile; xác nhận sau PoC |

### 2.3. Đồng bộ, điều phối, RF và vận hành

| STT | Tham số/chức năng | Mức cơ sở đề xuất | Điều kiện/ghi chú |
|---|---|---|---|
| H34 | Reference mạng HUB/NCC | Tạo và phát reference gắn với mốc PHY xác định | Không lấy thời điểm userspace gửi gói làm mốc RF |
| H35 | Timestamp thu | Timestamp phần cứng trong PL | Quy đổi về điểm chuẩn arrival HUB |
| H36 | Logon/ranging HUB/NCC | Tiếp nhận VSAT, cấp ranging resource, tính và gửi correction | Có timeout, retry và kiểm định danh |
| H37 | Timing correction HUB/NCC | Hiệu chỉnh riêng từng VSAT | Có đơn vị, dấu, sequence và epoch hiệu lực |
| H38 | Sai lệch arrival sau ranging | Mục tiêu trị tuyệt đối không lớn hơn 0,25 chu kỳ symbol upstream | Closed-loop; điều kiện kênh và phương pháp đo công bố |
| H39 | Frequency/power control HUB/NCC | Đo và phát lệnh hiệu chỉnh | Có giới hạn, quality và thời điểm hiệu lực |
| H40 | Kiểm soát lịch HUB/NCC | Không cấp khe xung đột hoặc vượt khả năng TX của VSAT | Grant có ID, epoch và thời hạn |
| H41 | Thu hồi tài nguyên HUB/NCC | Có khi VSAT mất hoạt động hoặc mất đồng bộ | Lịch cũ không tiếp tục có hiệu lực sau network restart |
| H42 | Hoạt động với trễ GEO mô phỏng | Thử 200–300 ms mỗi chiều | Khoảng trễ propagation cấu hình, chưa gồm xử lý |
| H43 | Dải tần thu IF | Đề xuất 950–2.150 MHz | Chốt theo LNB và frequency plan |
| H44 | Dải tần phát IF | Đề xuất 950–1.700 MHz | Chốt theo BUC và frequency plan |
| H45 | Cổng RF | RX/TX riêng; prototype ưu tiên 50 Ω | Đầu nối và trở kháng chính thức khóa trong ICD |
| H46 | Miền mức thu, mức phát và bước điều chỉnh | Chốt sau level budget và PoC RF | Phải quy định cả công suất từng carrier và composite power |
| H47 | Hoạt động FDD RF | Đo chất lượng RX khi TX đang hoạt động | Giới hạn desensitization chốt sau PoC |
| H48 | Reference ngoài | Có đầu vào 10 MHz; khuyến nghị PPS | Qua mạch clock phù hợp; không mặc định nối trực tiếp AD9361 |
| H49 | IFL/ODU | Module ngoài hoặc tích hợp theo cấu hình BUC/LNB | Reference 10 MHz, nguồn và bảo vệ theo ODU thực chọn |
| H50 | Quản trị | CLI/SSH hoặc API, phân quyền và lưu cấu hình | Có version phần mềm/FPGA và kiểm tra tương thích |
| H51 | Giám sát HUB/NCC | Theo VSAT, carrier, chất lượng burst, grant, queue và lỗi phần cứng | Xuất được log và thống kê |
| H52 | Cập nhật và recovery | Có kiểm tra tương thích và khôi phục khi lỗi | Không duy trì lịch cũ khi firmware/config đổi epoch |
| H53 | Watchdog | Có | Phát hiện treo và phục hồi có kiểm soát |
| H54 | Hoạt động liên tục | Ít nhất 72 giờ | Không treo/reset bất thường; thống kê đầy đủ lỗi RF và hệ thống |
| H55 | Nhiệt độ hoạt động mẫu | Đề xuất 0 đến +50 °C | Phải kiểm chứng trên mẫu tích hợp |
| H56 | Nguồn vào, công suất và kích thước | Chốt sau thiết kế phần cứng sơ bộ | Tách công suất modem và công suất ODU |

## 3. Chỉ tiêu kỹ thuật và tính năng riêng cho modem VSAT

### 3.1. Kiến trúc, dung lượng và giao thức

| STT | Tham số/chức năng | Mức cơ sở đề xuất | Điều kiện/ghi chú |
|---|---|---|---|
| V01 | Vai trò hệ thống | Trạm đầu cuối mạng Star | Được HUB/NCC quản lý và cấp phát tài nguyên |
| V02 | Chế độ hoạt động | Thu downstream và phát upstream đồng thời | FDD; kiểm chứng song công |
| V03 | Downstream | Thu DVB-S2 | Tập cấu hình đồng nhất với HUB |
| V04 | Upstream | Phát MF-TDMA burst | Chỉ phát theo quyền truy nhập hợp lệ |
| V05 | Số carrier downstream | Thu 01 carrier | Liên tục trong khi upstream phát burst |
| V06 | Số carrier upstream tại một thời điểm | Phát 01 carrier | Không yêu cầu VSAT phát hai carrier đồng thời |
| V07 | Chuyển carrier | Chuyển giữa ít nhất 02 carrier theo lịch | Kiểm trên cùng một VSAT |
| V08 | Mạng kiểm chứng | Hoạt động cùng ít nhất 02 VSAT khác | Tổng mạng ít nhất 03 VSAT vật lý |
| V09 | Thông lượng IP downstream | Tốc độ IP cực đại hỗ trợ không nhỏ hơn 10 Mbit/s khi được cấp toàn bộ tài nguyên dữ liệu thử | Đây là năng lực xử lý, không là tốc độ bảo đảm cho mọi trạm đồng thời |
| V10 | Thông lượng IP upstream | Tốc độ IP cực đại hỗ trợ đạt 3 Mbit/s khi được cấp tài nguyên thử tương ứng | Cấu hình đo tại mục 5 |
| V11 | Cấp phát tài nguyên | Thực hiện lịch tĩnh và grant động | Có khả năng gửi yêu cầu theo backlog |
| V12 | Ethernet dữ liệu | Ít nhất 01 cổng 10/100/1000BASE-T | Không đồng nghĩa tốc độ qua vệ tinh |
| V13 | Giao thức dữ liệu | IPv4, ICMP, UDP, TCP | Đo UDP và TCP riêng |
| V14 | Định tuyến | Static routing | Cấu hình được từ giao diện quản trị |
| V15 | MTU IP | Hỗ trợ 1.500 byte | Fragmentation/reassembly nội bộ được kiểm chứng |
| V16 | QoS | Ít nhất 03 lớp: điều khiển, ưu tiên, best effort | Queue và request phù hợp policy HUB/NCC |

### 3.2. Thu downstream và phát upstream

| STT | Tham số/chức năng | Mức cơ sở đề xuất | Điều kiện/ghi chú |
|---|---|---|---|
| V17 | Điều chế thu downstream | QPSK | 8PSK là mở rộng |
| V18 | FEC thu downstream | Giải mã LDPC + BCH | Theo DVB-S2 |
| V19 | Tỷ lệ mã downstream | 1/2 | 2/3 là bổ sung ưu tiên |
| V20 | FECFRAME downstream | Normal frame, 64.800 bit | Đúng cấu hình rate hỗ trợ |
| V21 | Tốc độ symbol downstream | 1; 2; 5; 12,5 Msym/s | Tự bắt và bám trong miền thử đã công bố |
| V22 | Chế độ coding/modulation | CCM | ACM là mở rộng |
| V23 | Pilot downstream | Có hỗ trợ | Khai thác để đồng bộ theo cấu hình receiver |
| V24 | Roll-off downstream | 0,25 | Các giá trị khác là bổ sung |
| V25 | Đồng bộ thu | Symbol timing, frame timing, carrier frequency và phase | Báo riêng lock PHY, FEC và network state |
| V26 | Điều chế phát upstream | QPSK burst | Tương thích profile thu của HUB |
| V27 | FEC phát upstream | Một profile Turbo TC-LM xác định | Khóa waveform ID, codeblock, interleaver, puncturing và mapping |
| V28 | Tỷ lệ mã upstream | Ưu tiên 1/2 nếu có trong waveform được chọn | Phải ghi rate chính xác trước nghiệm thu |
| V29 | Tốc độ symbol upstream | 0,25; 0,5; 1; 2; 5 Msym/s | Theo grant/config hợp lệ |
| V30 | Tạo burst | Preamble/UW, payload, FEC, CRC và phần kết thúc theo profile | Bao gồm ramp/filter tail trong duration budget |
| V31 | Chuyển tần số số | Ưu tiên NCO/DUC với LO cố định trong cùng băng tức thời | Không mặc nhiên retune PLL mỗi khe |
| V32 | Hiệu năng thu | Đo FER theo Es/N0 cho từng cấu hình | Mục tiêu implementation loss ≤1 dB tại FER 10^-3 so mô hình cùng profile; xác nhận sau PoC |

### 3.3. Đồng bộ, RF và vận hành

| STT | Tham số/chức năng | Mức cơ sở đề xuất | Điều kiện/ghi chú |
|---|---|---|---|
| V33 | Phục hồi thời gian mạng | Thu reference, bám clock và timeline mạng | Reference gắn mốc PHY; không dùng timer Linux phát burst |
| V34 | Timed TX | Thực thi thời điểm phát bằng PL | Timestamp được quy về mốc RF đã hiệu chuẩn |
| V35 | Gia nhập mạng | Tự động logon, ranging và vào trạng thái hoạt động | Timeout/retry có giới hạn |
| V36 | Bù trễ thô | Hỗ trợ vị trí trạm/vệ tinh qua provisioning hoặc GNSS | Không bắt buộc tích hợp GNSS trong mức cơ sở |
| V37 | Hiệu chỉnh timing | Nhận và áp dụng correction riêng của trạm | Đúng dấu, đơn vị, sequence và effective epoch |
| V38 | Độ chính xác sau ranging | Cùng HUB đạt mục tiêu arrival error không lớn hơn 0,25 symbol | Đây là chỉ tiêu closed-loop tại HUB, không chỉ jitter logic launch |
| V39 | Hiệu chỉnh tần số | Có, theo lệnh HUB/NCC | Giới hạn và thời điểm hiệu lực xác định |
| V40 | Điều chỉnh công suất | Có, theo lệnh và trần cấu hình | Không tăng công suất vô hạn khi mất feedback |
| V41 | Kiểm tra quyền phát | Chỉ phát với grant, clock, config và buffer hợp lệ | Loại grant cũ, trùng, quá hạn hoặc sai network epoch |
| V42 | Mất đồng bộ | Tự động khóa phát | Holdover có giới hạn theo drift budget |
| V43 | Lỗi phần mềm/phần cứng | Watchdog và hardware TX inhibit | Linux treo không được làm phát ngoài lịch |
| V44 | Hoạt động với trễ GEO mô phỏng | Thử 200–300 ms mỗi chiều | Bao gồm logon/ranging và vận hành ổn định |
| V45 | Dải tần thu IF | Đề xuất 950–2.150 MHz | Chốt theo LNB và frequency plan |
| V46 | Dải tần phát IF | Đề xuất 950–1.700 MHz | Chốt theo BUC và frequency plan |
| V47 | Cổng RF | RX/TX riêng; prototype ưu tiên 50 Ω | Nếu dùng Type-F 75 Ω phải có matching/chuyển tiếp phù hợp |
| V48 | Miền mức thu, mức phát và bước điều chỉnh | Chốt sau level budget và PoC RF | Đo tại connector modem |
| V49 | Hoạt động FDD RF | Đo RX trong khi TX hoạt động | Kiểm sensitivity/desensitization và spur |
| V50 | Reference ngoài | Khuyến nghị ngõ 10 MHz và PPS | Phục vụ reference/đo; không thay ranging |
| V51 | IFL/ODU | Module ngoài hoặc tích hợp theo BUC/LNB thực chọn | Có lọc, cách ly, bảo vệ quá dòng/ngắn mạch và báo lỗi |
| V52 | Quản trị | CLI/SSH hoặc API, phân quyền và lưu cấu hình | Có version firmware/FPGA/config |
| V53 | Giám sát | RF, lock, timing, CFO, FEC, grant, queue, nguồn và nhiệt | Xuất log có frame/grant ID và nguyên nhân lỗi |
| V54 | Cập nhật và recovery | Có kiểm tra tương thích và khôi phục | Không tự phát lại theo lịch cũ sau reset |
| V55 | Hoạt động liên tục | Ít nhất 72 giờ | Không treo/reset bất thường hoặc phát ngoài lịch |
| V56 | Nhiệt độ hoạt động mẫu | Đề xuất 0 đến +50 °C | Phải kiểm chứng trên mẫu tích hợp |
| V57 | Nguồn vào, công suất và kích thước | Chốt sau thiết kế phần cứng sơ bộ | Tách công suất modem và công suất cấp ODU |

## 4. Mức mở rộng, tách khỏi nghiệm thu cơ sở

| Hạng mục | Modem HUB | Modem VSAT |
|---|---|---|
| Tốc độ downstream | Các tốc độ ngoài tập cơ sở sau sizing | Tương ứng HUB |
| Điều chế downstream | Thêm 8PSK | Thêm 8PSK |
| ACM | NCC chọn MODCOD, HUB phát theo lịch | Thu thay đổi mode trong tập hỗ trợ, gửi feedback chất lượng |
| FEC downstream | Thêm rate và short FECFRAME | Giải mã tương ứng |
| Upstream đa carrier | Thu đồng thời ít nhất 04 carrier | Phát theo lịch trên nhóm carrier mở rộng |
| Điều chế upstream | Thêm thu 8PSK burst | Thêm phát 8PSK burst |
| Quy mô mạng | Tăng VSAT vật lý theo nguồn lực đo kiểm | Tương thích mạng mở rộng |
| Dịch vụ | VLAN, multicast, QoS nâng cao | Các chức năng tương ứng |
| Bảo mật dữ liệu | Phương án mã hóa và quản lý khóa xác định | Thực hiện tương thích HUB |
| Chuẩn return | Mở rộng theo ma trận tuân thủ DVB-RCS2 được phê duyệt | Tương ứng profile HUB |

Không tự gán thông lượng mới từ symbol rate mở rộng; phải tính lại MODCOD, overhead, khả năng decoder, CPU và song công.

## 5. Điều kiện kiểm tra và nghiệm thu dùng chung

| Nội dung | Điều kiện/mức đề xuất |
|---|---|
| Downstream chuẩn đo thông lượng | 12,5 Msym/s, QPSK, rate 1/2, normal FECFRAME, pilot bật, roll-off 0,25 |
| Upstream chuẩn đo thông lượng | 02 carrier đồng thời, mỗi carrier 5 Msym/s, QPSK, profile burst/FEC đã khóa |
| Lưu lượng | UDP, gói IP dài 1.500 byte; thông lượng tính trên byte gói IP, loại Ethernet và overhead vệ tinh |
| Thời gian đo tốc độ | Đề xuất ít nhất 10 phút sau khi ổn định; ghi offered load, loss và số byte thực nhận |
| RF cho bài đo tốc độ | Mức tín hiệu trong miền bảo đảm, Es/N0 đủ cao; ngưỡng cụ thể chốt sau PoC |
| Song công | Chứng minh downstream ≥10 Mbit/s đồng thời tổng upstream ≥6 Mbit/s |
| Phân bổ downstream | Mức ít nhất 10 Mbit/s là tổng carrier; bài kiểm từng VSAT cho phép cấp toàn bộ tài nguyên dữ liệu thử cho trạm đó |
| Phân bổ upstream | Mức 3 Mbit/s/VSAT chỉ áp dụng khi được cấp tài nguyên tương ứng; tổng lưu lượng mạng bị giới hạn bởi 02 carrier |
| Chứng minh MF-TDMA | Hai carrier có burst chồng thời gian; ba VSAT tham gia; ít nhất một VSAT đổi carrier theo grant |
| Timing | Clock VSAT độc lập; đo arrival tại điểm chuẩn HUB; ghi sai số cực đại và phân bố sai số |
| Ngưỡng timing | 0,25 symbol là mục tiêu nội bộ, không tự coi là chứng nhận RCS2; với 5 Msym/s tương ứng 50 ns (1 Msym/s tương ứng 250 ns) |
| Chất lượng PHY | Quét Es/N0 để lấy FER curve; nêu profile, số frame, lỗi, calibration và điều kiện channel |
| Implementation loss | So DUT với mô hình cùng waveform/channel tại FER 10^-3; mục tiêu ≤1 dB được xác nhận sau PoC |
| Trễ GEO | Kiểm forward/return delay và chênh delay giữa các VSAT; delay packet chỉ kiểm MAC, chưa thay bài timing waveform |
| Bài thử lỗi | Mất reference, grant/correction trùng hoặc quá hạn, reset HUB/VSAT, DMA/FIFO lỗi, mất nguồn IFL |
| Hoạt động 72 giờ | Lưu cấu hình, raw counters, log lỗi/reset và trạng thái RF; không yêu cầu không có lỗi RF dưới mọi điều kiện kênh |
| Thử vệ tinh thực | Theo tuyến, tài nguyên và điều kiện nhà khai thác; không suy availability dài hạn từ một buổi thử |

Về dung lượng: QPSK rate 1/2 tại 12,5 Msym/s có xấp xỉ 12,5 Mbit/s trước overhead; upstream 5 Msym/s có xấp xỉ 5 Mbit/s trước overhead. Downstream IP ≥10 Mbit/s cần tổng hiệu suất trên 80%; upstream 3 Mbit/s cần trên 60%. Phải tính chính xác frame/burst/control và đo thực tế. Tổng HUB upstream ≥6 Mbit/s là đề xuất nâng đồng bộ, kiểm với hai VSAT tốc độ cao và trạm thứ ba vẫn gia nhập mạng.

## 6. Các giá trị phải khóa trước nghiệm thu

1. Profile upstream chính xác: waveform, tỷ lệ mã, codeblock, burst length, preamble/pilot, ramp/tail và guard.
2. Miền bắt CFO/sample-rate offset, thời gian acquisition/logon/reacquisition và điều kiện SNR tương ứng.
3. Miền công suất thu từng carrier/composite; mức phát, bước/sai số điều chỉnh; sensitivity, spur, spectrum mask và FDD desensitization.
4. Điểm timestamp, calibration latency, ngưỡng mất sync và thời gian holdover theo từng rate.
5. Thời lượng superframe, lookahead grant, capacity control và SLA QoS dưới tải.
6. Đầu nối/trở kháng RF, voltage/current IFL, nguồn vào, công suất tiêu thụ và kích thước.
7. Đóng gói IP/signalling: TS/private hoặc GSE; phạm vi tương thích được công bố.

Các mục này cần có kết quả model/PoC hoặc yêu cầu ODU/operator để định lượng. Tài liệu hiện tại là cơ sở thống nhất phạm vi, chưa phải bản yêu cầu nghiệm thu hoàn toàn đóng băng.

## 7. Tài liệu căn cứ

- [ETSI EN 302 307-1 V1.4.1 — DVB-S2](https://www.etsi.org/deliver/etsi_en/302300_302399/30230701/01.04.01_60/en_30230701v010401p.pdf): căn cứ waveform downstream; các giá trị tốc độ/throughput của nhiệm vụ là đề xuất riêng.
- [ETSI EN 301 545-2 V1.5.1 — DVB-RCS2 Lower Layers](https://www.etsi.org/deliver/etsi_en/301500_301599/30154502/01.05.01_60/en_30154502v010501p.pdf): căn cứ tham khảo burst, MF-TDMA, signalling và timing; không suy ra tuân thủ đầy đủ từ một tập tính năng.
- [Analog Devices AD9361 Datasheet Rev.G](https://www.analog.com/media/en/technical-documentation/data-sheets/AD9361.pdf): căn cứ khả năng chip RF; thông số modem tích hợp phải đo riêng.

Các ngưỡng thông lượng, số trạm, số carrier, 0,25 symbol, implementation loss, nhiệt độ và thời gian thử trong bảng là **mục tiêu đề xuất của nhiệm vụ**, không phải yêu cầu mặc định của các tài liệu viện dẫn.

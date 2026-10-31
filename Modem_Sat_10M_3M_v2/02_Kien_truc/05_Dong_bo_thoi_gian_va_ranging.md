# 05. Đồng bộ thời gian, ranging và điều khiển thời điểm burst

> **Cập nhật CR-002 — 31/10/2026:** HUB downstream IP cực đại hỗ trợ **≥10 Mbit/s**; VSAT upstream IP cực đại **3 Mbit/s** khi được cấp đủ tài nguyên. Phương án sizing: downstream QPSK 12,5 Msym/s, rate 1/2; upstream QPSK tới 5 Msym/s, một Turbo profile mục tiêu rate 1/2. Đề xuất nâng HUB upstream lên **≥6 Mbit/s tổng/2 carrier**; đây là chỉ tiêu suy ra để phê duyệt, không phải yêu cầu người dùng đã chốt. Các rate thấp chỉ phục vụ bring-up. Xem [baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md); ví dụ số ở rate thấp vẫn là ví dụ, không là trần tốc độ sản phẩm. Tại upstream 5 Msym/s, mục tiêu timing 0,25 symbol tương ứng **50 ns**, phải kiểm chứng lại.

## 1. Mục tiêu thực sự của đồng bộ TDMA

Các remote không nhận tín hiệu HUB đồng thời. Chúng cũng không cần phát đồng thời. Điều cần đạt là burst của từng remote đến **điểm tham chiếu của mạng** đúng khe đã cấp. Với một vệ tinh transparent chung và HUB thu chung, có thể thiết kế theo timeline arrival tại HUB; có thể chọn timeline tại vệ tinh nếu mọi độ lệch được chuyển đổi nhất quán. Trong toàn bộ ví dụ sau, chọn điểm chuẩn là đầu vào thu HUB sau khi đã hiệu chuẩn delay thiết bị.

Không đồng nhất ba việc: đồng bộ tần số clock để không trôi; đồng bộ epoch/frame để biết lịch; bù propagation/pipeline để RF burst đến đúng nơi. GNSS/PPS có thể hỗ trợ clock/position nhưng không tự đo delay AD9361, filter, BUC và cáp.

Phần 2–10 là mô hình/thuật toán đề xuất cho profile riêng. Phần 11 đối chiếu nguyên tắc DVB-RCS2 [S2–S3]; không dùng công thức minh họa thay thế toàn bộ quy tắc normative của tiêu chuẩn.

## 2. Mô hình trễ rõ điểm đầu/cuối

Gọi:

- `H0`: thời điểm một sự kiện tham chiếu rời HUB TX, theo network time.
- `dF_i`: trễ từ sự kiện HUB TX đến điểm timestamp RX đã chọn ở remote i, gồm đường HUB→vệ tinh→remote và các delay tương ứng.
- `dR_i`: trễ từ điểm RF TX chuẩn của remote i đến điểm chuẩn HUB RX, gồm remote→vệ tinh→HUB.
- `LTX_i`: trễ từ sự kiện launch trong PL đến điểm RF TX chuẩn của remote.
- `A_i`: thời điểm muốn đầu burst đến HUB.
- `W_i`: thời gian chờ tính từ sự kiện reference nhận tại remote đến launch PL.

Khi clock rate đã bám và các đơn vị đã quy đổi:

`arrival_i = H0 + dF_i + W_i + LTX_i + dR_i`

Do đó:

`W_i = A_i − H0 − dF_i − dR_i − LTX_i`.

Đây là giải thích quan trọng: nếu remote khởi đầu lịch từ một mốc **đã nhận trễ**, cần xử lý cả độ trễ forward lẫn return trong hệ quy chiếu này. Chỉ bù một chiều mà không xét ý nghĩa local clock là sai. Nếu đã có clock remote biểu diễn đúng network time tại thời điểm hiện tại, công thức launch lại là `Tlaunch_i = A_i − dR_i − LTX_i`; không trừ `dF_i` lần nữa. Hai công thức tương thích khi định nghĩa clock nhất quán.

Các delay có thể gom vào hằng calibration, nhưng phải ghi rõ cái nào đã nằm trong hằng đó để tránh bù hai lần. Đường forward và return khác tần số vẫn phải định nghĩa riêng; không tự giả định hai đường/thiết bị có cùng delay.

## 3. Ví dụ số hai remote ở vị trí khác nhau

Giả thiết minh họa, không phải số đo mạng: reference rời HUB ở H0=0; A nhận sau 240 ms và return mất 240 ms; B nhận sau 245 ms và return mất 245 ms; bỏ qua LTX trong ví dụ. HUB muốn A đến ở 1000 ms, B đến ở 1002 ms.

| Đại lượng | Remote A | Remote B |
|---|---:|---:|
| Reference nhận tại remote | 240 ms | 245 ms |
| Arrival được cấp tại HUB | 1000 ms | 1002 ms |
| Chờ sau reference: A−dF−dR | 520 ms | 512 ms |
| Thời điểm phát thực trong timeline HUB | 760 ms | 757 ms |
| Kiểm tra cộng return delay | 760+240=1000 ms | 757+245=1002 ms |

B nhận reference muộn hơn nhưng phát sớm hơn A để đến khe muộn hơn 2 ms tại HUB. Điều này hoàn toàn bình thường. Nếu cả hai đều chờ 520 ms sau khi nhận, B sẽ đến 1010 ms, trễ 8 ms so với khe 1002 ms. Chênh lệch arrival khi cùng chờ là 10 ms do có cả khác biệt forward và return.

Nếu `W_i<0`, grant đã quá gần: không thể quay về quá khứ. NCC phải cấp tài nguyên cho một epoch tương lai đủ xa. Các giá trị ở đây nhằm minh họa phép tính; không xác lập superframe 1 giây cho mọi hệ thống.

## 4. Remote lấy đâu ra delay ban đầu?

### 4.1 Bù thô bằng hình học

**Mục đích:** đưa logon burst vào cửa sổ HUB có thể tìm, tránh quét không giới hạn. **Yêu cầu:** biết vị trí remote và vị trí/ephemeris vệ tinh; có mức sai số được giới hạn.

**Phương án:** đổi tọa độ trạm và vệ tinh sang cùng hệ ECEF, tính range `rho=||r_sat−r_station||`; propagation delay `tau=rho/c`. Cộng các đoạn đường liên quan theo đúng topology và delay thiết bị. Một sai số range 300 m tương ứng khoảng 1 µs một đoạn đường; ở mô hình reference-trễ, sai số có thể góp ở cả forward và return. Không dùng độ cao GEO 35.786 km thay slant range cho mọi trạm.

**Nội dung:** kiểm vị trí nhập sai, đơn vị độ/radian, cao độ, thời điểm ephemeris và footprint; cho phép provisioning thay GNSS với trạm cố định. **Lộ trình:** model tháng 2–3, kiểm ngoài lab tháng 8–10. Hình học không thay được ranging tinh và calibration.

### 4.2 Cửa sổ acquisition riêng

Khi delay chưa đủ chính xác, chỉ cấp logon/ranging slot có guard rộng, power hạn chế, không cho phát payload bình thường. Có thể bắt đầu một remote trong lab rồi thêm contention/backoff. HUB tìm burst trong cửa sổ dự kiến, xác minh identity và CRC trước khi gán số đo. Một burst không nhận dạng được không dùng để điều chỉnh terminal đang chạy khác.

## 5. Ranging vòng kín

Định nghĩa timing error: `e_k = measured_arrival_k − assigned_arrival_k`. `e>0` nghĩa là burst đến muộn. Nếu có biến `advance` mà tăng lên làm phát sớm, dùng luật minh họa:

`advance_(k+1) = advance_k + K × e_k`.

Nếu phần mềm lưu biến delay/chờ thay vì advance, dấu cập nhật ngược lại. Unit test phải chứng minh lỗi muộn làm phát sớm hơn; không dựa vào tên biến.

Quy trình đề xuất:

1. HUB cấp ranging grant, ghi expected arrival và điểm chuẩn waveform (ví dụ đầu symbol preamble theo quy ước).
2. Remote chuẩn bị burst, áp dụng bù thô, phát bằng timed TX.
3. HUB correlation + fractional timing estimator, quy timestamp detection về điểm chuẩn; đánh giá chất lượng số đo.
4. NCC tính error, loại outlier/false detection, tạo correction có sequence và effective epoch.
5. Remote nhận correction sớm, áp dụng một lần tại epoch; ACK/report version nếu profile yêu cầu.
6. Lặp tới khi residual nằm trong miền chấp nhận; sau đó cấp traffic, vẫn theo dõi drift.

Không gửi “trừ trễ đi 2 µs” mà không có đơn vị, dấu, epoch và tham chiếu. Không áp dụng correction lặp do retransmission của cùng message. Không thay đổi clock nhảy bậc giữa một burst đang phát.

## 6. Vòng điều khiển chậm do GEO

Một bản tin correction đi HUB→vệ tinh→remote đã mất một khoảng trễ đáng kể; số đo burst quay về HUB còn thêm return. Hệ điều khiển phải xét feedback age. Không đưa gain lớn để “sửa nhanh” khi nhiều lệnh cũ đang trên đường.

Đề xuất giai đoạn đầu chỉ có một correction chưa xác nhận cho mỗi remote, dùng gain thấp/giới hạn bước; sau đó nâng cấp estimator trạng thái gồm offset và frequency drift, hiệu chỉnh dự đoán tại effective epoch. Lưu `measurement_epoch`, `command_epoch`, `applied_epoch` để ghép số đo với đúng cấu hình. Mô phỏng stability với max RTT, jitter, mất/reorder message và clock drift trước chọn K/PI. Không cung cấp một hệ số gain cố định chung cho mọi mạng.

Nếu biết slope drift, dự báo `offset(t+Δ)=offset(t)+drift×Δ`. Phải phân biệt drift oscillator với thay đổi đường truyền hoặc nhảy pipeline. Correction quá lớn hoặc quality thấp dẫn về ranging, không tùy tiện tiếp tục traffic.

## 7. Timestamp và clock recovery ở PL

**Mục đích:** loại jitter do OS và FEC queue khỏi mốc thời gian. **Yêu cầu:** mọi timestamp gắn với sample/symbol event, có integer/fractional part và calibration latency.

Phương án `TIME_REF` của profile riêng: HUB liên kết một reference value với một PHY marker định danh rõ (frame counter/marker). Remote timestamp marker tại tầng PL trước delay biến thiên FEC, lưu theo frame ID; khi payload reference được giải mã sau đó, ghép đúng record. Nếu reference được chèn trước FEC/queue tại HUB, phải tính/đo chính xác pipeline hoặc dùng cơ chế association đã định nghĩa. Timestamp thời điểm ứng dụng nhận packet không đạt yêu cầu.

PL dùng local counter monotonic, accumulator/NCO điều chỉnh tốc độ ước lượng network time. State: UNLOCKED → ACQUIRING → LOCKED → HOLDOVER → UNSYNC. Filter phase/rate dựa trên reference; không cho counter đảo chiều gây descriptor chạy hai lần. Lịch dùng epoch và so sánh wrap-safe; 64 bit được khuyến nghị cho internal representation, không thay độ rộng field của chuẩn khi interoperable.

Sample clock, symbol clock, network clock và CPU clock khác nhau. Cần mapping/tỷ số giữa chúng; mọi fractional correction được thực hiện bằng sample scheduling/interpolator/NCO đã mô hình hóa, không chỉ làm tròn microsecond.

## 8. Delay xác định trong TX/RX pipeline

Timed TX phải quy định mốc: bắt đầu đọc waveform FIFO hay sample đầu ở interface AD9361 hay preamble RF ra connector. Chọn một mốc làm API và đo conversion sang mốc RF. Delay gồm filter group delay, CDC buffering, serializer, AD9361 filters và RF group delay; có thể đổi theo sample rate/filter config.

Lập bảng calibration theo cấu hình được hỗ trợ, đo qua loopback với thiết bị đo độc lập. Nếu reset/link retraining thay đổi latency, phải re-calibrate hoặc thiết kế deterministic buffering trước arm. Không giả định độ trễ luôn giống nhau chỉ vì HDL không thay.

HUB timestamp detection phải trừ group delay filter/channelizer và độ lệch estimator; interpolation fractional cần calibrate với vector có offset đã biết. Phát hiện “peak correlation” thường không trùng trực tiếp sample đầu RF nếu chưa quy ước.

## 9. Ngân sách sai số và guard

Ở Rs=1 Msym/s, một symbol là 1 µs; ở 5 Msym/s là 200 ns. Ví dụ mục tiêu residual arrival |e|≤0,25 symbol là 250 ns và 50 ns tương ứng. Đây là **mục tiêu nội bộ đề xuất cho closed-loop**, không phải chứng nhận đạt chuẩn hoặc có thể đạt ngay với mọi cấu hình AD9361.

Ví dụ ngân sách worst-case cho mục tiêu 250 ns ở 1 Msym/s, cần thay bằng số đo:

| Thành phần | Phần ngân sách ví dụ |
|---|---:|
| HUB detection/estimation | 60 ns |
| Network time estimation và reference association | 50 ns |
| Launch quantization/fractional scheduling | 20 ns |
| TX/RX calibration residual | 50 ns |
| Drift giữa hai lần cập nhật | 50 ns |
| Dự phòng | 20 ns |
| Tổng bound tuyến tính | 250 ns |

Không cộng RSS nếu các đại lượng chưa được chứng minh độc lập/ngẫu nhiên. Sai số resolution 10 ns không có nghĩa accuracy 10 ns.

Sai số rate `ε ppm` sau T giây sinh drift xấp xỉ `ε×10^-6×T`. Ví dụ 1 ppm trong 100 ms →100 ns, trong 1 s →1 µs. Nếu phần drift được phép 50 ns trong 100 ms thì cần residual rate khoảng 0,5 ppm hoặc tốt hơn; phải bám clock thường xuyên hoặc giảm khoảng cập nhật. Thực tế cần cộng jitter/path drift.

Guard giữa hai burst trên cùng carrier phải bao phủ sai số burst trước và sau, duration error, ramp/filter tails, channel transient và margin. Nếu mỗi đầu có bound E, riêng sai số tương đối có thể tới 2E. Không đặt guard bằng một residual đơn lẻ. Ranging guard lớn hơn traffic guard. Các carrier khác nhau còn chịu filter leakage và near-far chứ không chỉ guard thời gian.

## 10. Cấp lịch đủ sớm và xử lý mất đồng bộ

Tại lúc NCC gửi grant, điểm arrival được cấp ở HUB phải ở tương lai ít nhất:

`Hlookahead ≥ dF_max + processing_remote_max + dR_max + LTX_max + margin`,

nếu `dF` được tính từ thời điểm grant/reference thực rời HUB và output được quy về launch như trên. Phải cộng thêm downstream queue/FEC/transport còn nằm ngoài định nghĩa dF. Superframe có thể ngắn nhưng grant được gửi trước nhiều superframe. Không nhầm superframe duration với tổng lookahead.

Remote chỉ được phát khi clock valid, grant hợp lệ, payload/waveform ready, config đúng epoch và hardware permit. Mất reference dùng holdover giới hạn theo drift budget, sau đó tự mute. Không để remote phát mãi theo lịch cũ khi HUB restart hoặc network epoch đổi. Watchdog phần cứng phải đóng TX dù Linux treo.

## 11. Đối chiếu DVB-RCS2 và giới hạn tuyên bố

EN 301 545-2 V1.5.1 (2026-04), mục 7.3.9 mô tả NCR, thông tin vị trí vệ tinh, lịch burst và correction. NCR tham chiếu 27 MHz; mục 7.3.9.1 yêu cầu độ chính xác khởi đầu burst traffic trong 50% chu kỳ symbol so với lịch danh định và xử lý correction nhận đủ sớm theo quy định. Logon có giới hạn riêng theo bảng 7-30; không áp cùng ngưỡng traffic cho logon. Mục 7.5 tổ chức tài nguyên MF-TDMA. [S2]

Nếu chọn tuân thủ RCS2 phải áp đúng signalling, đơn vị/scale, điểm tham chiếu và toàn bộ điều kiện liên quan, cùng các bắt buộc của profile; không lấy mỗi ngưỡng 0,5 symbol làm chứng nhận. Các message riêng và arrival-at-HUB convention của hồ sơ này chỉ giải thích/đề xuất kiến trúc. TR 101 545-4 là hướng dẫn triển khai, không thay normative EN [S3].

## 12. Phép thử chứng minh đã làm chủ

1. Hai remote có dF/dR khác nhau, cả hai đến đúng lịch HUB; kiểm lại công thức với dấu và unit.
2. Một remote tăng delay, một remote giữ nguyên; correction chỉ ảnh hưởng đúng terminal/epoch.
3. Quét fractional delay, oscillator ppm, SNR, temperature/config; đo residual không chỉ bằng log software.
4. Mất/reorder/duplicate reference/correction/grant; không phát ngoài grant hoặc áp correction hai lần.
5. Reset một FPGA hoặc AD9361; latency thay đổi phải được phát hiện trước khi traffic hoạt động lại.
6. Đổi carrier trong từng remote; timeline RF vẫn đúng và upstream không làm mất downstream lock.
7. Ranging và traffic đồng thời; logon không gây collision vào khe user đã cấp.
8. Bài GEO-delay ở lab trước live satellite; trace đồng bộ tại HUB và remote dùng chung frame/grant ID.

Các thí nghiệm phải giữ clock remote độc lập trong bài nghiệm thu network synchronization. Dùng chung 10 MHz trong giai đoạn debug là hữu ích nhưng chưa chứng minh khả năng tự đồng bộ qua mạng.

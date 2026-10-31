# M04 — RF/IFL và tích hợp BUC/LNB

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

RF/IFL chuyển mức và bảo vệ giữa chip RF với cáp vệ tinh. L-band là miền nối BUC/LNB; AD9361 không phát trực tiếp Ku công suất lớn. DC feed và 10 MHz trên cáp cần bias tee/cách ly đúng, không nối thẳng vào RF pin.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** nối AD9361 với miền IF vệ tinh an toàn, đúng level và chất lượng RF.

**Đầu vào/đầu ra:** RF port AD9361, ODU/reference/power → IF RX/TX, DC/reference feed và telemetry fault.

**Yêu cầu kỹ thuật:** định hướng RX 950–2.150 MHz, TX 950–1.700 MHz theo ODU; RX/TX riêng; prototype ưu tiên 50 Ω. Quy định input composite, output range, spur/mask, matching, FDD desense và bảo vệ DC. Đầu nối/trở kháng final phải khóa trong ICD.

**Phương án/chi tiết:** matching/balun/filter, gain/attenuator, shielding và layout cách ly; bias tee/10 MHz injection riêng. Chọn eFuse/current limit và surge/ESD theo điện áp/dòng BUC/LNB; đo cable loss, startup current, thermal. Không để nguồn ODU đi vào port AD9361; kiểm BUC back-off và transient bằng waveform burst.

**Kiểm chứng/đầu ra bàn giao:** level calibration, return loss, spectrum, blocking, RX trong lúc TX; trip/fault/recovery của IFL. Báo cáo RF theo reference plane và procedure calibration.

**Lộ trình/phụ thuộc:** M1–M3 level plan; M4–M8 module thử; M9–M18 tích hợp PCB; M19–M22 xác nhận. RF/hardware; cần ODU plan, M03/M05/M12/M13.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M04-REQ-001 | Frequency/level budget có reference plane | RX950–2150/TX950–1700 MHz là đề xuất theo ODU |
| M04-REQ-002 | Bảo vệ DC và fault | Overcurrent/short dẫn ngắt an toàn và log |
| M04-REQ-003 | FDD và blockers | Đo RX khi TX cao, nhiều carrier composite |
| M04-REQ-004 | Spectrum/ramp/back-off | Mask và giới hạn power khóa theo operator/profile |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Ports gồm RF RX/TX, reference/DC ODU, enable/inhibit, fault/current/temperature và config attenuator. Level table phải có desired single-carrier, composite max, cable loss và gain theo frequency. Dữ liệu calibration trả cho M15 để power command có ý nghĩa dB.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Chọn ODU và dải mức

Thu thập BUC input/output/back-off, LNB gain/NF/reference và impedance. Tính gain/attenuation sao cho receiver không clip và transmitter không overdrive BUC.

### 5.2. Thiết kế RF conditioning

Matching/balun/filter, attenuation/gain và switch/test coupler nếu cần. Khi prototype50Ω nối75Ω phải phân tích mismatch thay vì đổi connector hình thức.

### 5.3. Thiết kế IFL power/reference

Bias tee, DC block,10MHz injection, eFuse/current sense và discharge/reset; kiểm power rating và fault propagation về hardware mute.

### 5.4. Kiểm layout/FDD

Đánh giá rò TX qua connector, ground, nguồn và không gian; dùng shield/filter phù hợp. Đo sensitivity/desense trong song công ở peak traffic.

### 5.5. Calibration và qualification

Sweep frequency/level/temp, đo spur/harmonics/envelope cả IF và sau BUC khi có lab. Duy trì calibration ID và uncertainty; chỉ mở phát trong mức cho phép.

## 6. Ví dụ tính toán hoặc luồng minh họa

Một carrier return 5 Msym/s, α=0,25 có băng danh định ~6,25MHz. Hai carrier không nhất thiết chỉ cần 12,5MHz: phải cộng khoảng cách trung tâm, passband/transition margins và tránh DC/alias. Chọn frequency plan trước filter và clock plan.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M04-TC-001 | Short/overcurrent test | Không hỏng RF chip; inhibit/fault đúng |
| M04-TC-002 | Strong TX + weak RX | Đo desense và so giới hạn đã khóa |
| M04-TC-003 | Burst spectrum | Ramps/tails/ACPR nằm trong budget, không chỉ CW đẹp |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Chỉ đo một carrier yếu khi TX tắt sẽ bỏ qua desense. “AD9361 56MHz” không bằng usable span của board. Nguồn DC lọt vào input RF có thể phá chip; đo biastee bằng dummy load trước nối modem.

## 10. Bài thực hành nhập môn gắn với mô-đun

Vẽ level budget từ AD9361 tới BUC bằng dBm/dB, thêm cable loss và attenuator. Sau đó vẽ đường DC/reference và chỉ ra linh kiện ngăn DC vào chip. Không thực hiện thử công suất khi chưa có fixture bảo vệ phù hợp.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R04 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Đọc RF ports/electrical limits và conditions.
- [R17 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Dùng link budget/propagation để chọn gain/power, không hứa rain margin từ peak modem.
- [R03 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Tham khảo deployment/system engineering; operator limits riêng.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

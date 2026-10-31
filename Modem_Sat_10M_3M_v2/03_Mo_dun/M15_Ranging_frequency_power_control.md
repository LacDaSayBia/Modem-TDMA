# M15 — Ranging và vòng điều khiển timing/frequency/power

Phiên bản 2.0; 31/10/2026. Trạng thái: phương án triển khai đề xuất, chưa phải kết quả phần cứng đã kiểm chứng.

[Mục lục toàn bộ](../README.md) · [Baseline tốc độ](../01_Yeu_cau/CR002_Baseline_10M_3M.md) · [Quy ước dự án](../04_Quy_uoc/00_Bo_quy_uoc_project.md)

## 1. Giải thích cho người mới và vai trò

Ranging là HUB đo burst đến sớm/muộn rồi hướng dẫn VSAT sửa lần phát sau. Hình học cho giá trị khởi đầu; vòng kín sửa phần sai còn lại. Với GEO, lệnh sửa luôn đến trễ nên control cần xử lý tuổi số đo.

Đọc lần đầu theo thứ tự: phần 1 → ví dụ phần 6 → các bước phần 5 → yêu cầu và phép thử. Từ ngữ chưa rõ tra [bảng thuật ngữ](../00_Quan_ly/Thuat_ngu_va_lo_trinh_doc.md). Nguồn kỹ thuật ở phần 11; lựa chọn implementation ở đây là đề xuất dự án.

## 2. Mục đích, phạm vi, đầu vào và đầu ra

**Mục đích:** khép vòng để burst từng VSAT đến đúng khe và chất lượng đủ tốt.

**Đầu vào/đầu ra:** expected/actual arrival, CFO, quality, identity và location → correction có epoch; residual/health report.

**Yêu cầu kỹ thuật:** lỗi/dấu/unit rõ, correction chỉ áp một lần, đo thuộc đúng grant/config, có outlier/age checks và giới hạn bước. Control stability phải xét feedback GEO; bù hình học chỉ thô.

**Phương án/chi tiết:** logon có cửa sổ riêng; range theo ECEF khi có vị trí; đo burst data-aided; `e=arrival_measured−arrival_target`, e dương nghĩa muộn, tăng advance để phát sớm. Ban đầu một correction chưa xác nhận mỗi terminal; sau nâng estimator offset/drift và prediction tới effective epoch. Frequency/power có limits và anti-windup/clamp, không tăng power vô hạn khi mất feedback.

**Kiểm chứng/đầu ra bàn giao:** hai remote khác delay hội tụ đúng, drift và delayed feedback không dao động, reject wrong-ID/stale reports; residual target ≤0,25 symbol theo điều kiện. Model/loop parameters, trace và failure policy.

**Lộ trình/phụ thuộc:** M2–M5 model; M6–M9 ranging hai trạm; M10–M16 multiuser/control; M17–M20 RF thực. MAC/system/DSP; M13/M14/M16.

## 3. Yêu cầu kỹ thuật mô-đun

| Mã yêu cầu | Nội dung phải thực hiện | Tiêu chí/điều kiện kiểm |
|---|---|---|
| M15-REQ-001 | Measurement/command epochs | Gắn đúng grant/config và áp correction một lần |
| M15-REQ-002 | Closed-loop arrival | Target≤0,25Ts tương ứng50 ns ở 5 Msym/s |
| M15-REQ-003 | Bù thô có giới hạn | Vị trí/ephemeris và calibration, acquisition window riêng |
| M15-REQ-004 | Frequency/power limits | Quality/outlier/clamp và fail policy; không tăng vô hạn |

Mục tiêu hệ thống liên quan: HUB downstream IP peak ≥10 Mbit/s; VSAT upstream IP peak 3 Mbit/s; HUB upstream aggregate ≥6 Mbit/s/2 carrier là đề xuất suy ra. Tải nào không đi qua mô-đun này chỉ dùng để xác định interface/load, không được cộng thành throughput riêng. Peak đo theo grant/resource allocation, không là CIR đồng thời cho mọi trạm.

## 4. Giao tiếp và dữ liệu trao đổi

Nhận expected/actual arrival và quality M13, time state M14, terminal/capability M16; trả timing advance, CFO/power deltas, effective epoch và residual health. Lưu applied correction history để ghép số đo với đúng trạng thái trước đó.

Mọi boundary phải ghi clock/reset, đơn vị/scaling, byte/bit order, config/epoch ID, backpressure, error và hành vi reset. Các chi tiết wire/ABI cuối phải có golden transaction trong ICD. Không truyền một pointer C hoặc struct có padding native lên wire mà không serialization.

## 5. Phương án thực hiện chi tiết

### 5.1. Khởi tạo range thô

ECEF trạm/vệ tinh cùng datum và thời điểm, range/c cho từng đoạn; cộng device delay theo reference convention. Vị trí sai hoặc thiếu dẫn logon/ranging window bảo thủ.

### 5.2. Đo và xác minh

Chỉ dùng burst có terminal/grant match, timestamp quality và config hợp lệ. Loại false detect, collision, outlier và measurement age quá lớn.

### 5.3. Đóng timing loop

Định nghĩa e=measured−target; e>0 nghĩa muộn. Tăng advance để phát sớm, hoặc giảm wait. Gain/step limit chọn từ mô phỏng delayed feedback; bắt đầu một correction chưa xác nhận mỗi trạm.

### 5.4. Ước lượng drift

Khi có nhiều số đo, fit offset và slope/drift, dự báo tại effective epoch. Không sửa liên tục theo noise; lost/reordered/duplicate commands phải idempotent.

### 5.5. Frequency/power loops

Phân common-mode CFO khi có căn cứ, dùng NCO cho correction nhỏ; power step clamp bởi ODU/linear range. Nếu control không hội tụ thì về ranging/mute thay tiếp tục traffic.

## 6. Ví dụ tính toán hoặc luồng minh họa

e=+100 ns nghĩa burst trễ100 ns. Với K=0,5 minh họa, advance tăng50 ns cho command mới; nhưng chưa được dùng K này cho thật nếu chưa xét RTT và lệnh cũ đang bay. Frequency1 ppm trong100 ms thêm100 ns, vượt timing50 ns maxrate nếu không discipline.

Ví dụ dùng để giải thích/sizing, không phải số đo hay cam kết fit/FER/timing. Lưu giả thiết và thay bằng kết quả PoC trước chốt cấu hình.

## 7. Nội dung kiểm thử và tiêu chí hoàn thành

| Mã test | Phép thử | Kết quả cần có |
|---|---|---|
| M15-TC-001 | Hai delay khác nhau | Hai remote cùng về đúng khe, không cùng một correction |
| M15-TC-002 | Delay feedback/lost/reorder | Loop không dao động, không áp correction hai lần |
| M15-TC-003 | Power/CFO saturation | Limits và failure policy đúng, không unsafe TX |

Mỗi test lưu build/profile/config hash, seed hoặc raw input, expected/actual và lỗi mở. Test không được chạy không ghi PASS; trạng thái NOT_RUN/TBD phải được giữ. [Quy ước verification](../04_Quy_uoc/06_Verification_trace_va_calibration.md) áp dụng chung.

## 8. Lộ trình và sản phẩm bàn giao

Các mốc ở phần 2 là lịch chủ trì. Ba bước kiểm soát của mô-đun: (a) model/ICD draft trước khi tích hợp; (b) PoC ở tốc độ thấp nhưng đúng semantics; (c) stress ở cấu hình peak và error cases trước G4/M18. Phụ thuộc thiếu phải báo blocker cụ thể, không đánh dấu hoàn tất theo phần trăm mã nguồn.

Bàn giao tối thiểu: đặc tả interface, source/model hoặc IP package đúng quyền sử dụng, test vectors/procedure, build recipe, báo cáo performance/resource/latency liên quan và known limitations. M20 nhận evidence; M01 nhận tác động requirement/TBD; M19 nhận counters/fault codes. Thuật toán mua ngoài phải có license manifest và phạm vi không có source.

## 9. Lỗi thường gặp và cách tránh

Lệnh “trừ2µs” không có điểm chuẩn/dấu/epoch dễ làm ngược. Dùng GNSS để bỏ ranging bỏ sót pipeline delay. Sửa timing quá mạnh theo một số đo nhiễu qua GEO dễ tạo dao động.

## 10. Bài thực hành nhập môn gắn với mô-đun

Viết mô phỏng arrival offset+drift, feedback delay500 ms và correction sequence. So hai gain, plot residual và nêu khi nào hệ mất ổn định. Sau đó thêm duplicate command và kiểm không sửa hai lần.

Người thực hiện viết một trang giải thích đầu vào/đầu ra, một case đúng, một case lỗi và cách quan sát. Reviewer kiểm người học hiểu mốc thời gian/đơn vị, không chỉ chạy lại lệnh mẫu.

## 11. Nguồn và cách đọc

- [R02 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Timing adjustment và return synchronization trong profile.
- [R03 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Hướng dẫn triển khai synchronization/control.
- [R17 — danh mục nguồn](../06_Nguon/Nguon_kiem_chung_v2.md): Range/propagation dùng dữ liệu tuyến thật; không cấp một delay chung mọi trạm.

Khi chi tiết hóa, ghi điều/bảng hoặc source path/commit cạnh quyết định. Các source locator Rxx dùng trong phần này đã được tổng hợp riêng; không suy conformance đầy đủ từ một implementation mẫu hoặc một phép loopback.

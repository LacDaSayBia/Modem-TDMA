# Quy ước verification, trace, calibration và nghiệm thu

## 1. Test record bắt buộc

TestID, requirementIDs, objective, method(analysis/review/model/RTL/lab/field), preconditions, equipment/calibration validity, exact procedure, stimuli/seed, expected/unit/tolerance, actual, evidence paths/hashes, build/config/profile/serial và status. Status: PASS/FAIL/BLOCKED/NOT_RUN/INCONCLUSIVE, không dùng “gần đạt” thay actual.

Unit tests cho semantics/parser/algorithm; RTL sim cho handshake/time/reset; lab cho hardware/RF/latency; field cho tuyến thật. Cùng một testID không dùng kết quả model để đánh dấu measurementPASS. Golden vector độc lập tối thiểu cho framing/FEC/IQ/timing signs.

## 2. Thông lượng và QoS

Baseline DS≥10Mbit/s IP, VSAT US3Mbit/s IP khi đủ tài nguyên, proposed HUB aggregate≥6Mbit/s/2carrier. UDPIP1500byte đo≥10phút sau ổn định, đếm bytes successfully delivered, không Ethernet/FEC/padding/retransmit. Mục tiêu loss≤10^-5 ở highSNR là proposed acceptance criterion cần khóa. Report offered load, lost/duplicate/corrupt/queue drops, elapsed time theo monotonic clock.

Kiểm song công, hai burst carrier chồng thời gian, ba trạm joined và một trạm đổi carrier. Bài peak hai VSAT3M không đồng nghĩa ba trạm đều3M; QoS overload báo fairness/latency/queue age và control reservation. TCP ghi RTT, congestion control và packet loss riêng, không thay UDP capacity.

## 3. PHY/timing statistics

FER/BER phải kèm tổng frame/bit và errors, max iteration, SNR calibration và confidence thích hợp. Zero errors không bằng BER0; với independent rare events có thể dùng xấp xỉ upper95%≈3/N nhưng phải ghi assumptions. Time measurement báo reference plane, sample/fractional calibration, max|e| và distribution/quantiles; không chỉ average nhỏ.

0,25Ts tại5Msym/s là50ns, tại1Msym/s250ns. Hiện chỉ là mục tiêu; threshold/GEO delays/clock source độc lập phải nằm trong campaign. Common-reference debug không chứng minh network synchronization. RF launch accuracy, estimator resolution và jitter report riêng.

## 4. Calibration và uncertainty

Calibration ID gắn serial, firmware/filter/clock config, ngày/nhiệt/reference plane, phương pháp, instrument ID/validity và uncertainty. Đổi filter/rate/reset/linktraining có thể làm invalid delay table; phải kiểm hoặc re-calibrate trước traffic.

Không mặc định uncertainty là10% hay1/3 cho mọi phép đo. Khi dùng expanded uncertaintyU và upper limitL, decision rule bảo thủ có thể chọn measured+U≤L; lower limit dùng measured−U≥L. Đây là decision rule dự án cần thỏa thuận và áp đúng measurand, không phải mặc định TCVN. RF/time uncertainty budget phải được reviewer đo lường kiểm tra.

## 5. CI và definition of done

Per-commit: syntax/lint/schema/link checks, keyscan, unit semantics, tiny golden vectors. Nightly/định kỳ: RTL randomized resets/backpressure, integration replay, fixed-point sweeps. Milestone: routed timing/CDC, lab RF/FER/time/load/fault, soak/live. Không rerun tất cả chỉ vì sửa typo; impact analysis chọn tests, mọi required check vẫn phải pass.

Done module khi requirements/interfaces/source hoặc IP package/build/tests/evidence/limitations được review, counters tích hợpM19 và issue blockers đóng hoặc scope rõ. Done release khi support matrix/ABI/config/license/update/recovery và system campaign đủ. Mẫu hồ sơ trong07_Bieu_mau chưa là kết quả thử thật.

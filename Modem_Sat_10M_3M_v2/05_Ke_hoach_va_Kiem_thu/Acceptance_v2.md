# Ma trận acceptance baseline v2

Các mức peak theo người dùng; aggregate6 và losscriterion là proposed derived requirements phải khóa. Các testcases dưới đây là kế hoạch, chưa có PASS phần cứng.

| TestID | Mục tiêu/cấu hình | Tiêu chí dự kiến | Owner |
|---|---|---|---|
| SYS-TC-001 | HUBDS→VSATRX, QPSK1/2 NF/pilot,12,5Msym/s | IP≥10Mbit/s theo packet/loss conditions | M08–M10/M18/M20 |
| SYS-TC-002 | Một VSAT→HUB, QPSK5Msym/s, profileTurbo chính xác | IP3Mbit/s khi cấp đủ tài nguyên | M11–M13/M16/M18 |
| SYS-TC-003 | HaiVSAT peak,2carrier cùng thời gian, third joined | HUBaggregate≥6Mbit/s đề xuất; signalling trạm3 còn hoạt động | M13/M16/M20 |
| SYS-TC-004 | Song công SYS001+003 | DS≥10/USaggregate≥6 đồng thời, validconfig/nooverflow | M03/M06/M07/M17/M20 |
| SYS-TC-005 | Một VSAT đổi carrier theogrant | RF/bursttiming đúng, payload không nhầm carrier | M12/M13/M16 |
| SYS-TC-006 | Ranging: trạm khác delay, independentclocks,GEO200–300ms/chiều | Residual≤0,25Ts; maxrate5Msym/s là50ns, cần uncertainty | M05/M14/M15 |
| SYS-TC-007 | Mất reference/grant, duplicate/reorder/epochreset | Không phát TX không an toàn;mute/reacquire/correctionidempotent | M14–M17/M19 |
| SYS-TC-008 | FER/SNR và fixed point | Mục tiêu loss≤1dB tại FER10^-3 so cùng reference/profile | M02/M09–M11/M13 |
| SYS-TC-009 | Nearfar/blocker và TX cao/RX yếu | TheoRFlevels/mask/desense đã khóa, báo ADC clip | M04/M06/M13 |
| SYS-TC-010 | QoSoverload +16logicterminal | Control không starve,fairness/admission theo policy | M16/M18 |
| SYS-TC-011 | Update/powerloss/ABImismatch | Khôi phục được,defaultmute,không stale grants | M17/M19 |
| SYS-TC-012 | 72hsoak và0–50°C trong cấu hình chốt | Không treo/reset bất thường, errors/recovery được log | M03/M04/M19/M20 |
| SYS-TC-013 | Live GEO + build máy sạch | Trace tuyến/thông số/operator, chạy lại test đại diện | M01/M20 |

Report peak: UDP gói IP1500byte, ≥10phút, đếm IP bytes thành công; loss mục tiêu≤10^-5 ởhighSNR, không duplicate/corrupt. Báo offered load,RTT/queueages vàdrops. Không thay12,5Msym/s bằng10Msym/s QPSK1/2 rồi đo PHY bits gọi IP10M.

Mỗi test có preconditions,equipment/uncertainty,expected,actual và evidence; dùng mẫu07_Bieu_mau. Timing250ns ở1Msym/s không thay50ns tại maxrate. Đồng hồ chung chỉ bài DEBUG,không thaynetworkacceptance. Bất kỳ test chưa chạy giữ NOT_RUN.

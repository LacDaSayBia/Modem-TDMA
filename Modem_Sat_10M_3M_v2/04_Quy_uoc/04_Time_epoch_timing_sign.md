# Quy ước time, epoch, correction sign và timed TX

## 1. Ba loại thời gian

| Loại | Dùng cho | Không dùng thay |
|---|---|---|
| UTC wall clock | Log con người, thời điểm campaign | Deadline RF khi đồng hồ hệ điều hành nhảy |
| Local monotonic sample time | Sample ordering, PHY timestamp | Epoch mạng khi chưa lock/reference association |
| Network time + epoch | Grants, reference, ranging, correction hiệu lực | OS packet-arrival time |

Representation nội bộ đề xuất: `epoch_id:u64`, `sample_index:u64`, `sample_fraction:u32` theo unsigned Q0.32 của **một sample**. Network scheduling serialization dùng `network_time_ns:u64` + `sub_ns_q32:u32` khi ICD chọn mapping đó; không tráo sample fraction thành ns fraction. Counter/sample frequency hoặc conversion coefficients phải đi cùng config version. Đây là representation nội bộ, không thay field/đơn vị NCR của chuẩn nếu triển khai RCS2.

Local sample counter không lùi. Mapping network_time=a×sample_index+b điều chỉnh có chất lượng/uncertainty; nhảy epoch làm hủy lịch cũ. Không nhận grant từ timeline khác chỉ vì số timestamp có vẻ trong tương lai. Mỗi ID64 có thể không wrap trong tuổi thọ nhưng code không dựa vào signed casts sai.

## 2. Điểm chuẩn và công thức

RF TX reference: thời điểm symbol đầu preamble tại connector modem TX theo định nghĩa waveform, sau quy đổi group delay. HUB RX reference: thời điểm symbol đó đến connector RX, ước lượng từ sample/correlation đã calibration. Điểm antenna/satellite chỉ dùng khi có conversion được ghi trong ICD.

`e_time = measured_arrival − assigned_arrival`; e>0 là đến muộn. `advance` tăng làm launch sớm; cập nhật advance+=K×e. Nếu dùng wait/delay thì chiều sửa ngược. `cfo_hz = measured−nominal`; NCO correction lấy dấu phù hợp convention IQ và đã kiểm known tone. Power delta dB dương yêu cầu tăng trong giới hạn, không có nghĩa gain absolute dBm.

Nếu reference nhận trễ: `W=A−H0−dF−dR−LTX`. Nếu VSAT đã giữ đúng network time hiện tại: `launch=A−dR−LTX`. Không trừ dF thêm lần nữa ở trường hợp sau. Mỗi delay có endpoint/bandwidth/config/temp dependence và chỉ được tính một lần.

## 3. Epoch, sequence và hiệu lực

`epoch_id` thay khi HUB restart timeline hoặc thay reference convention; terminal phải relock/rejoin. `config_id` thay rate/filter/waveform, `calibration_id` thay delay/gain tables, `link_epoch` thay liên FPGA reset. Các ID có mục đích khác nhau, không gộp thành một “version”.

Correction record gồm measurement_epoch/time, terminal/grant ID, correction_seq, applied/config epoch, delta/unit, effective_time và validity. Duplicate seq không áp hai lần; old/out-of-order theo rule idempotency. Grants và correction không được sửa một burst đã launched. Schedule/config dùng shadow bank và commit atomically; kết quả apply có ACK/reason.

Với sequence n-bit, so sánh modulo chỉ trong cửa sổ <2^(n−1); khoảng cách đúng nửa miền là ambiguous và reject/resync. [R19](../06_Nguon/Nguon_kiem_chung_v2.md) cung cấp nguyên lý serial arithmetic; không dùng `a>b` thông thường qua wrap.

## 4. Holdover và an toàn

Time states UNLOCKED/ACQUIRING/LOCKED/HOLDOVER/UNSYNC có ngưỡng quality và uncertainty. Holdover bound dựa residual ppm, tuổi reference và pipeline calibration; không định thời tùy ý “giữ30giây” khi chưa có budget. 5Msym/s yêu cầu mục tiêu50ns cho0,25Ts; 1ppm/100ms đã100ns nên chế độ cũ250ns không còn đủ.

`tx_permit=clock_valid && network_state_allows_tx && grant_valid && epoch_match && waveform_ready && rf_permit && !fault`. Ranging/logon chỉ được permit trong slot tương ứng. Hardware watchdog đóng TX khi software treo. Bài thử clock chung được ghi DEBUG_COMMON_REF, không tính acceptance network synchronization.

## 5. Golden timing tests

Hai remote dF/dR=240/240ms và245/245ms, arrival1s/1,002s phải launch760/757ms nếu bỏ LTX; test e=+100ns làm phát sớm hơn, negative correction ngược lại; reject duplicates/stale epoch; reset/link retraining thay latency phải mute/recalibrate; maxrate fractional delay/temperature cần có error distribution lẫn max bound.

Nguồn: [R02/R03/R09/R19](../06_Nguon/Nguon_kiem_chung_v2.md). Công thức/control/representation trên là thiết kế nội bộ, không tự chứng minh conformance ETSI.

# Quy ước RTL, clock/reset, CDC và constraints

## 1. Coding và cấu trúc

New RTL có thể dùng VHDL-2008 làm ngôn ngữ chính theo năng lực nhóm; vendor/ADI Verilog/SystemVerilog giữ nguyên và mixed-language qua wrapper. Đây là lựa chọn đề xuất, khóa tại G0 theo simulator/tool license. Không dịch lại IP vendor chỉ để thống nhất ngôn ngữ.

Mỗi entity/module có clock/reset/handshake rõ, parameter/generic constraints, width/signedness explicit. Tách combinational và sequential logic; không inferred latch ngoài chủ ý review. Dùng `numeric_std` với VHDL và conversion rõ; SystemVerilog dùng typed logic/always_ff/always_comb phù hợp tool. Testbench không đi vào synthesis file set.

Port mới dùng `_i`, `_o` nếu style nội bộ; suffix unit/type khi giúp tránh nhầm: `arrival_sample_i`, `cfo_hz_i`, `payload_len_bytes_i`. Legacy vendor ports giữ tên. Clock `clk_sample`, `clk_axi`, `clk_link`; reset `rst_*_n` chỉ khi active-low. Constant có đơn vị và range, không magic number không giải thích.

## 2. Clock và reset

Clock từ clock resources chính thức; không tạo clock bằng combinational AND một enable. Dùng clock enable hoặc dedicated clock gating đúng guide. Reset policy theo domain: assertion an toàn theo nguồn reset, deassertion đồng bộ sau clock ổn; nếu IP yêu cầu khác thì wrapper ghi rõ.

Reset local module phải làm output-valid=0, không giữ stale frame/grant, TX inhibit=1; memory không cần reset toàn bộ nếu validity tags xóa đúng. Reset runtime có handshake stop/drain/cancel và epoch bump; không deassert reset để interface coi buffer cũ hợp lệ.

## 3. CDC theo loại dữ liệu

| Dữ liệu crossing | Phương án | Điều phải kiểm |
|---|---|---|
| Status đơn bit, thay chậm | Synchronizer chain đúng cell/attributes | Pulse width, MTBF assumption |
| Event pulse | Toggle/handshake hoặc event FIFO | Không mất hoặc đếm hai lần |
| Multi-bit config | Shadow registers + request/ack commit | Nhận atomic toàn config |
| Stream IQ/LLR/packet | Async FIFO có record/metadata chung | Full/empty/reset và overflow |
| Counter/timestamp | Snapshot handshake/FIFO, hoặc Gray cho mục đích phù hợp | Không đồng bộ từng bit nhị phân rời |

`report_cdc` phải được review, không chỉ chạy. False-path/asynchronous clock groups không thay synchronization circuitry. Mỗi waiver có EXC owner, mạch và test; không blanket waive critical crossings. Tham khảo [R09](../06_Nguon/Nguon_kiem_chung_v2.md).

## 4. Streaming semantics

Tại boundary AXI-stream thật, transfer chỉ khi valid&&ready. Producer giữ data/metadata ổn khi valid=1,ready=0; không đọc `ready` để tạo combinational loop qua nhiều modules. Các port ADI FIFO-style không tự có semantics AXI; adapter ghi conversion và buffering.

Tkeep/tlast/tuser có định nghĩa byte/frame/metadata trong ICD; không dùng tlast lúc là packet lúc là codeblock mà không type. RX ADC sampling không thể bị downstream stall tùy ý; overflow phải được detect và xử lý. TX đã launch cần continuous feed hoặc safe abort/mute, không pause RF giữa burst vì ready=0.

## 5. Constraints và sign-off

XDC/Tcl version-controlled, đúng target/pin/IOSTANDARD/termination/clock/generated clock và I/O delays; mọi clock có period/uncertainty từ clock plan. Không sửa constraints để làm report “xanh” khi interface vật lý không đạt.

Sign-off gồm post-route setup/hold theo corners/tool target, unconstrained-path review, CDC/reset review, utilization và max load sim/hardware. Frequency goal ví dụ100MHz không phải achieved Fmax. Báo số latency min/max, cycles/sample/frame, queue depths và valid configurations. Regression bắt reset/full/empty/overflow/late descriptors, không chỉ nominal payload.

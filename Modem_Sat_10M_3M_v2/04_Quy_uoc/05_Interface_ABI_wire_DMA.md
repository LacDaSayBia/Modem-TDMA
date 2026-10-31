# Quy ước giao tiếp, ABI, wire/control và DMA

Trạng thái: schema/wire proposal cho giao thức riêng, cần peer review và golden packets trước implementation. Không phải bitfield DVB-RCS2. RF burst framing/FEC/CRC normative khi chọn chuẩn giữ theo profile, không thay bằng CRC transport nội bộ.

## 1. Ba loại serialization

Wire/network control: big-endian multi-byte integers, fixed offsets, signed two's-complement khi ghi signed. MMIO/PS–PL: words theo driver/IP thực, baseline custom registers little-endian32bit aligned; dùng accessor kernel phù hợp, không cast pointer wire. Vector IQ: int16 little-endian I,Q như quy ước DSP. Không dùng host-native `struct` trực tiếp cho cả ba.

## 2. Header control riêng đề xuất, v1

Header40byte, payload_len chỉ payload, CRC4byte, authentication trailer nếu policy layer dùng có schema riêng được khóa trước phát thật. Max control payload4096byte, chưa gồm header/CRC/auth; burst payload nhỏ hơn phải fragment theo profile. Unknown major/version/flags/length bị reject. Reserved phải bằng0 khi gửi và xử lý theo version policy khi nhận.

| Offset byte | Size | Field | Ý nghĩa |
|---:|---:|---|---|
| 0 | 4 | magic | ASCII `SM01` |
| 4 | 1 | major | 1 |
| 5 | 1 | minor | 0 |
| 6 | 2 | message_type | Registry trong ICD06 |
| 8 | 4 | payload_len_bytes | 0..4096 theo type/range |
| 12 | 4 | network_id | Namespace mạng |
| 16 | 4 | terminal_id | 0 dành HUB, nonzero assigned terminals; broadcast value khóa ICD |
| 20 | 4 | sequence | Per-source/per-session counter |
| 24 | 8 | epoch_id | Timeline/session epoch |
| 32 | 4 | config_id | Profile/config revision |
| 36 | 4 | flags_reserved | 0 trong bản header proposal này; mở rộng qua minor/major review |

Message types draft:0x0001 NETWORK_ANNOUNCE,0x0002 TIME_REF,0x0010 LOGON_REQ,0x0011 LOGON_RESP,0x0020 RANGING_GRANT,0x0021 BURST_REPORT,0x0022 CORRECTION,0x0030 RESOURCE_REQUEST,0x0031 BURST_GRANT,0x0040 KEEPALIVE,0x0041 TX_INHIBIT. Mỗi payload có schema type/length/units và golden vector riêng; registry trên chưa là payload specification hoàn chỉnh.

Transport CRC proposal: CRC-32C, polynomial normal0x1EDC6F41/reflected0x82F63B78, init0xFFFFFFFF, refin/refout=true, xorout0xFFFFFFFF; tính trên header+payload không padding. Giá trị32bit serialize big-endian theo project. `123456789` check=0xE3069283. Đây là quy ước serialization riêng; không sao chép trực tiếp byte mapping iSCSI hay CRC waveform. Tham khảo thuật toán CRC32C tại [RFC3720 Appendix B](https://www.rfc-editor.org/info/rfc3720/) (RFC đã được thay thế cho toàn giao thức iSCSI, chỉ tham khảo phần CRC).

CRC không xác thực command. Management dùng SSH/TLS phù hợp implementation; on-air grant/correction/authentication phải có thiết kế key/session/replay được review ở M19/ICD06. Header40byte trên chỉ là inner record, có thể được bọc authenticated envelope. Không dùng proposal chưa có envelope/keys hợp lệ để gọi sản phẩm secure. Logon bootstrap/ranging cũng phải có giới hạn quyền phát.

## 3. PS–PL custom register/descriptor ABI

Register map có identity/magic, ABI major/minor, build ID, capability bits, control/status, IRQ enable/status/ack và counters. W1C/read-to-clear phải ghi từng trường; không giả mọi IP cùng ack. Không tự cấp địa chỉ base tuyệt đối trước address map/XSA/DT review.

Descriptor logical fields: grant_id,epoch_id,config_id,launch_time representation,carrier/rate/waveform IDs,buffer_id,len_bytes,duration_samples,power_profile,flags,status. Bản đồ offsets/width/alignment của descriptor final được khóa trong ICD03 sau target/DMA evaluation. Không đoán offset từ thứ tự C fields.

Producer writes buffer+descriptor→memory barrier/cache sync→publish tail/doorbell. Consumer validates→device ownership→completion→CPU sync/acquire→read. MMIO writes dùng accessors/barriers, không `volatile` đơn thuần thay synchronization. Ownership FREE/CPU_OWNED/DEVICE_OWNED/COMPLETE/ABORTED rõ; không free/reuse khi device đang giữ buffer.

## 4. Errors, reset và flow control

Common reason names: REJECT_VERSION,LENGTH,PROFILE,EPOCH,LATE,DUPLICATE,BUFFER; FAULT_UNDERFLOW,OVERFLOW,CLOCK,RF,LINK. Numeric enum và severity registry versioned, unknown status không coi success. Reset bump epochs, cancel/stop trước release memory, default TX mute. Timeout có bound và reason; retry không làm phát lại cùng grant.

Credit units explicit bytes/frames, high/low watermark; traffic control không bị bulkdata starve. Link CRC/sequence không thay application frame/grant IDs. Test malformed length, endian, wrap, memory ownership, reset giữaDMA và congestion là bắt buộc. Nguồn: [R06/R07/R10/R18/R19](../06_Nguon/Nguon_kiem_chung_v2.md).

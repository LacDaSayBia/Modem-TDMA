# Quy ước DSP, đơn vị, I/Q, LLR và fixed-point

## 1. Đơn vị và quy ước phức

Đơn vị nội bộ mặc định: Hz, samples/s, symbols/s, seconds hoặc integer ns/sample counts đã chỉ rõ. Tốc độ mạng dùng bit/s decimal; Mbit/s=10^6bit/s, MB=10^6byte, MiB=2^20byte. Không trộn byte/s và bit/s; packet length ghi `*_bytes`, LLR count ghi bits/symbols phù hợp.

Complex baseband x=I+jQ. NCO positive offset dùng nhân exp(+j2π f n/fs); spectrum và downconversion sign phải kiểm bằng tone known-frequency. CFO báo `f_measured−f_nominal`; để sửa residual dương, NCO correction âm tại boundary đã quy định. Nếu mixer convention khác ở IP vendor, adapter đổi dấu và test rõ.

Amplitude dB=20log10(A/Aref), power dB=10log10(P/Pref); dBm là absolute power ref1mW. Es/N0 và Eb/N0 không thay nhau; conversion cần bits/symbol, effective code rate và định nghĩa energy tính pilot/overhead hay không. SNR sample bandwidth khác Es/N0.

## 2. I/Q file và sample format đề xuất

Diagnostic IQ format chuẩn: signed two's-complement int16 little-endian, interleaved `I0,Q0,I1,Q1,...`. Một complex sample 4byte. AD9361 native12bit khi đưa int16 nội bộ **sign-extend, không tự left-shift**; metadata ghi `effective_bits=12`, `fraction_bits=11` nếu dùng normalization x=raw/2048. Nếu capture khác source scale, ghi fraction/fullscale riêng, không mặc định int16 luôn Q1.15.

Wire/control endian độc lập fileIQ và MMIO. Raw vector có JSON metadata: dtype,endian,complex_order,effective_bits,fraction_bits,fs_hz,channel,profile_id,config_hash,first_sample_index,reference_plane,calibration_id,gaps và SHA256. File dài không ngầm chứa headers. Khi có sample gaps, sidecar mô tả các đoạn; không nối rồi giả continuous.

## 3. Fixed-point rõ W/F

Dùng notation `S(W,F)` signed two's-complement total W bit, F fractional bits; value=integer×2^-F. Ví dụ S(16,15) có range[-1,1−2^-15], S(16,11) có range[-16,16−2^-11]. Không dùng chỉ “Q15” hoặc “Q1.15” nếu nhóm hiểu integer-bit count khác nhau.

Mỗi khối có input/output/accumulator W,F, coefficients, expected peak, rounding và overflow. Baseline rounding đề xuất nearest, ties-to-even khi khả thi; saturation thay wrap cho signal arithmetic trừ chỗ modulo có chủ đích (phase accumulator). Actual IP dùng rounding khác phải ghi và model bit-accurate tương ứng. Integer divisions/truncations không để implicit cast quyết định.

Gain/filter normalization: định nghĩa average QPSK symbol power=1 trước TX scaling; RRC coefficients và interpolation gain kiểm bằng impulse/tone/average power. Filter state/tail/reset length có units và group-delay record; không tự bỏ samples mà vẫn giữ timestamp cũ.

## 4. LLR

Convention dự án: L=log(P(bit=0|y)/P(bit=1|y)); L>0 thiên bit0. Quantized LLR signed q-bit two's-complement, scale `llr_units_per_nat` hoặc hệ số tương đương explicit; q=6 là ứng viên, không khóa decoder chưa benchmark. Ghi clipping range và noise normalization. Một vendor core dùng sign ngược thì adapter/testvector đổi rõ.

Bit ordering theo codeword index n=0..N−1, symbol bit order theo waveform chuẩn. Frame metadata có profile/MODCOD/frame length/valid bit count và frameID. Không thêm paddingLLR mà không báo count; codeword swap/endian có independent golden test.

## 5. Phép thử tối thiểu và ví dụ

Impulse, DC, positive/negative tone, fullscale/clip, random seeded, I/Q swap, sign inversion, fractional delay và codeword known bits. Ví dụ int12 raw=-2048 sign-extend ra int16=-2048; x=-1 với F=11, không phải -0,0625 của F=15. Một decoder sign test phải cho zero-noise all-zero codeword ra đúng bits.

Nguồn: [R01/R02](../06_Nguon/Nguon_kiem_chung_v2.md) cho mapping/coding; [R04/R06] trong danh mục nguồn cho native chip/IP. Normalization/WF/LLR conventions là lựa chọn nội bộ, cần adapters và không sửa waveform normative.

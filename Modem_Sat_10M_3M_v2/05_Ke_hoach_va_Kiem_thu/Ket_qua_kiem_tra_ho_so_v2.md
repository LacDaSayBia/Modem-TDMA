# Kết quả kiểm tra hồ sơ v2

**Trạng thái kiểm tra cấu trúc hồ sơ:** PASS

Số file mô-đun: 20; số file Markdown: 54.

Đã kiểm: đủ 20 mô-đun, mỗi file 11 phần; liên kết tương đối; JSON; các giá trị baseline 10M/3M và proposed aggregate6M; timing50ns; ví dụ băng thôngIQ; header40byte và CRC32C golden check.

**Chưa kiểm chứng phần cứng modem:** resource/Fmax/FER/RF/latency/throughput thực và conformance. PASS ở đây không phải sản phẩm đạt chỉ tiêu. Các test nghiệm thu hệ thống vẫn NOT_RUN cho đến khi có thiết bị và evidence.

Lặp lại: `python3 09_Tools/validate_docs.py --report` sau khi giải nén. Công cụ dùng thư viện chuẩn Python3.

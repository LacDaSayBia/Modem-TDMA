# Quy ước repo, định danh, Git và tài liệu

## 1. Cây repo triển khai đề xuất

ZIP hiện tại là hồ sơ thiết kế, không chứa source modem đã hoạt động. Khi bắt đầu code, dùng cây repo sau; mỗi vùng có README mô tả build/test/owner. Không tạo giả RTL để làm đầy cấu trúc.

| Đường dẫn | Nội dung |
|---|---|
| docs/requirements, architecture, modules, icd, adr, tests | Hồ sơ hiện hành và trace |
| hw/schematic, pcb, bom, test_fixture | CAD nguồn và fixture; generated Gerber trong release |
| fpga/common, zynq, accelerator, sim, constraints, scripts | RTL/BD/Tcl/XDC/Testbench có thể tái tạo |
| sw/kernel, bsp, userspace, ncc, nms | Patch và source theo component |
| models/float, fixed, channel | Thuật toán và emulation |
| config/profiles, boards, calibration | Config có version, calibration theo serial |
| tests/unit, rtl, integration, system, vectors | Tests và vector index; raw lớn tách retention |
| tools, ci, third_party | Tooling/lint, pipeline definitions, origin/license |
| out, build, captures | Sinh tự động; không commit raw secrets hoặc output tùy máy |
| releases | Manifest/index các release; binary lưu theo quy trình artifact |

## 2. Quy tắc đặt tên

File/path mới dùng ASCII snake_case, không dấu/khoảng trắng; tài liệu Markdown nội dung tiếng Việt UTF-8 LF. ID mô-đun giữ M01–M20; không dùng M01 đồng thời làm tháng, tháng viết “tháng 1” hoặc schedule_month=1. MATLAB/Python/C/HDL có extension đúng loại; không đổi tên target/vendor IP bắt buộc.

| Loại | Mẫu | Ví dụ |
|---|---|---|
| Requirement | REQ-domain-topic-NNN | REQ-SYS-DS-001 |
| Module requirement | Mxx-REQ-NNN | M14-REQ-003 |
| Interface | ICD-NN | ICD-02 |
| Decision/change | ADR-NNN / CR-NNN | ADR-004 / CR-002 |
| Test/evidence | Mxx-TC-NNN / EVD-release-run | M14-TC-003 |
| Exception/bug | EXC-NNN / BUG-NNN | EXC-005 |
| Profile | lowercase semantic ID + immutable revision | ds_qpsk_r12_nf_12m5_v1 |

ID không tái sử dụng khi xóa yêu cầu. H/V cũ giữ là legacy IDs; bảng trace nối tới REQ và module IDs. Dùng một document index; filename đổi phải sửa relative links và review references.

## 3. Git và thay đổi

Main luôn có build/test smoke đạt theo scope. Nhánh ngắn `feat/m14-timed_tx`, `fix/m17-irq_ack`, `docs/cr002-rate`; commit một thay đổi logic, message nêu problem/behavior/module. Không ép một tiêu chuẩn commit bên ngoài khi project chưa áp; đây là convention nội bộ.

Pull request phải có requirement/bug/ADR links, thay đổi behavior/interface, test evidence và risk/rollback. Thay ABI/time/bit order cần peer review hai phía; sửa typos chỉ cần link/lint. Không commit generated Vivado cache/DDR captures khổng lồ; commit Tcl/BD sources/constraints và lockfile đủ tái tạo. Binary cần phục vụ nghiệm thu được quản lý qua release manifest/hash.

## 4. Tài liệu và trace

Mỗi module có mục đích, scope, input/output, requirements, detailed steps, tests, schedule, owner và source locator. Mỗi requirement phải cụ thể: đối tượng + hành vi + giá trị/condition + test. Từ “hỗ trợ”, “ổn định”, “đồng bộ chính xác” đứng một mình chưa đủ.

Evidence labels: NORM/VENDOR/MODEL/MEASURED/PROPOSED/TBD. Bảng kết quả giữ expected/actual/unit/build/profile/decision. Nội dung kế hoạch không được ghi như đã hoàn thành. Mẫu ở thư mục `07_Bieu_mau` dùng để tạo record, không phải evidence thực.

## 5. Kiểm tra tự động và review

CI kiểm links, unique IDs, schema/config ranges, UTF-8, không chứa keys và source lockfile. Reviewer kiểm ý nghĩa requirement và nguồn, vì linter không hiểu một con số sai vật lý. Chưa có repo Git external được tạo trong yêu cầu này; cây trên là đề xuất để triển khai.

Nguồn tham khảo phương pháp: [R18, R20](../06_Nguon/Nguon_kiem_chung_v2.md). Các tên/path/branch và ID là quyết định nội bộ, không phải yêu cầu ETSI.

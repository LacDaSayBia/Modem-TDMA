# Quy ước build, version, release, security và license

## 1. Lockfile và build tái lập

Record target part/package/speedgrade, boardrev, Vivado/Vitis/PetaLinux/kernel/compiler/simulator versions, HDL/source commit vàpatch hashes, IP revisions/licenses, profile/ABI/config/calibration compatibility. Không tự gán commit chưa kiểm; template khóa ban đầu dùng null/TBD và block production release nếu còn thiếu.

Build từ scripts/Tcl/Make/config sources, không cần state GUI trên máy cá nhân. Generated bitstream/DTB/rootfs/kernel/modules thuộc cùng release bundle; không trộn kernel cũ với DT/FPGA mới rồi coi boot thành công là tương thích. Ghi build timestamp/host ảnh hưởng binary; không hứa bit-identical khi vendor tool chưa bảo đảm, nhưng phải tái tạo functionality/provenance và report differences.

## 2. Version và identity

Theo tư tưởng SemVer [R20], public interface breaking change tăng major, additive compatible tăng minor, bugfix compatible tăng patch. Whole release version không thay ABI version, profile revision, hardware boardrev hoặc actual buildhash. Ví dụ release2.0.0 có thể dùng control-ABI1.0; đó không là mâu thuẫn.

FPGA expose identity/capability và ABI; driver probe kiểm major/features; NMS lưu serial/boardrev/build IDs. Calibration table chỉ hợp config đã định; không chọn “mới nhất” tự động khi không match.

## 3. Release package

Manifest gồm files/size/SHA256, versions/targets/compatibility, profile support, tests/evidence, known issues, license inventory, provisioning/recovery instructions và rollback constraints. Hash phát hiện thay đổi, không thay signature/authentication. Ký firmware bundle bằng phương án đã chọn và bảo vệ key ngoài repo; test wrongtarget/corrupt/signaturebad/powerloss.

Release tags immutable; fix tạo version mới và CR/bug trace. Không ghi đè binary đã gắn acceptance evidence. Source blackbox/IP obligations rõ: target/số seat/quyền phân phối/bảo trì/source access. Không đưa source PDF tiêu chuẩn hoặc vendorIP vàoZIP khi chưa có quyền.

## 4. Security design scope

Threat model tối thiểu: giả mạo grant/correction/terminal, replay, malformed length, management intrusion, firmware tamper, credential leak, denial of service. Baseline MUST có safeTX limits/parser bounds/management access control và signed-or-authenticated update theo scope khóa; onair control authentication thiết kế cụ thể ởICD06/M19 trước thử vận hành.

Dùng crypto library được duy trì, định nghĩa key provisioning/rotation/revocation và replay session policy. Không tự chế cipher/hash hoặc dùng CRC làm auth. Sample configs tuyệt đối không chứa productionkeys; logs không dump credentials/tokens/raw privileged packets. Nếu debug auth-off, gắn LAB_ONLY, cấm claim secure và chỉ chạy môi trường test được kiểm soát theo quy trình dự án.

## 5. Recovery và maintenance

Golden boot/recovery path không phụ thuộc linkFPGA đang hỏng; watchdog/fault đưa TXmute. Update atomic/banked hoặc procedure tương đương có powerloss proof; board/ABI mismatch reject trước arm. Có service runbook, lifetime component/tool risk và vulnerability patch policy. Mọi ngoại lệ cần risk/test, không dùng thuật ngữ AES256 thay mô tả bảo mật hệ thống.

Nguồn: [R11/R15/R18/R20](../06_Nguon/Nguon_kiem_chung_v2.md). Các yêu cầu security trên là baseline dự án đề xuất, chưa phải kết quả audit/chứng nhận.

# Quy ước phần cứng, RF/IFL, calibration và review

## 1. Nguồn đặc tính và BOM

Mỗi chip có exactpart/package/temp/speedgrade, datasheet revision, power/IO limits và lifecycle/leadtime được xác minh lúc mua. Typical performance không chuyển thành guaranteed bound; absolute maximum không là operating point. 7030 và7020 có IO/transceiver khác, pin-compatible chỉ khi hãng xác nhận đúng pair/package.

BOM ghi MPN/mfg/value/tolerance/rating/package/quantity/approvedalternatives; thay thế clock/filter/power parts có impact review RF/time/thermal. Quotes/stock trước đây không thay kiểm procurement hiện hành. BUC/LNB spec và cable plan gắn đúng số serial/model dùng thử.

## 2. Schematic/layout sign-off

Power tree/reset/rail sequencing, voltage banks/termination, DDR/QSPI/bootstraps, clocks/refclk pins, LVDS/GT constraints, RFmatching/filter/isolation, connector impedance, grounding/shield, thermal và mechanical đều có reviewowner. Không phát Gerber khi pinmap/chiptarget còn TBD quan trọng.

DFT gồm JTAG mỗi chip, console/recoveryboot, testpoint rails/clocks, PRBS/loopback, current/temperature sensing và fixture RF an toàn. Board phải kiểm được khi app/NCC chưa hoạt động; test fixture tách fault PCB với software.

## 3. RF reference planes và level budget

Chỉ rõ connector/antenna/AD9361pin plane cho mỗi dBm/gain/delay. Composite power là tổng các carrier/noise/blocker trong băng, không giống single-carrier desired. 50Ω và75Ω chuyển tiếp có matching/mismatch loss và calibration; không đổi connector rồi coi impedance đúng.

Mỗi frequency profile có TXlevel range/step/accuracy, RXoperating range/composite max, spectrum/mask/spurs, FDDdesense và filter response theo điều kiện đã khóa. Không lấy AD9361EVMchip làm EVMmodem sau BUC. Ramps/tails và PA back-off theo waveform/burst công suất thực.

## 4. IFL safety và calibration

DCblock/biastee/referenceinjection có ratings phù hợp; eFuse/limit/protection được thử bằng dummyload trước nối RF chip. Fault state và reset/retry không gây oscillationpower hoặc tự mở TX khi chưa được grant. Tách modem power và ODU power cả dự toán/thermal/báo cáo.

Calibration record gắn hardware/config/temperature/rate/reset state; gồm gain/attenuation, frequency/clock, TX/RXgroupdelay và uncertainty. Mỗi table có checksum/calibrationID và valid range, không nội suy ra vùng chưa đo mà không model/review. Đổi filter/rate/clock hoặc rework RF phải đánh giá validtable.

## 5. Mẫu review gate

Đầu vào: schematic/BOM/layout version, pin/clock/level budgets và open issues. Checklist owner từng miền ký accept/rework/defer có reason. Output: release package, fabrication files hash, assembly/bring-up và acceptance plan. Defer chỉ cho phần không chặn chức năng/safety; mục unsafeTX/overvoltage không waiver để kịp deadline.

Nguồn hãng/chỉ dẫn: [R04/R05/R08/R09](../06_Nguon/Nguon_kiem_chung_v2.md); RFmask/operatingconditions theo profile/operator cụ thể cònphải khóa. Đây là quy ước nội bộ, không tựchứngnhận EMC/spectrum compliance.

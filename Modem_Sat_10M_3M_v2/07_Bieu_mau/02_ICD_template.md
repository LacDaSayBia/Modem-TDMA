# Mẫu ICD — chưa là interface đã đóng băng

ID/version/owner hai phía/status. Scope: signal/wire/register/file format; không trộn endian ba miền.

## Interface table

| Field/port | Width/type | Offset/units/reference | Producer/consumer | Reset/valid/flow control |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

## Semantics

Clock/reset/CDC; ownership; atomiccommit; range/endianness/signedness; scaling/bitorder; frame/epoch/sequence; maxlatency/stall; errors/timeouts/recovery; security/integrity.

## Golden transactions

Một case nominal, một boundary, một malformed/resetcase có byte/sample vector và expected. Không dùng native sizeof(struct) làm offset source. Compatibility/migration và req ui re dt es ts khi version đổi.

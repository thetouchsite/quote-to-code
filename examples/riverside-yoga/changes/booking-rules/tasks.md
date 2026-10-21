# Tasks · booking-rules

## 1 · Data

- [x] 1.1 Migration: `bookings`, `studio_settings`, RLS policies
- [x] 1.2 `book_session` with row lock, capacity, credit and window checks
- [x] 1.3 `cancel_booking` with the 12-hour rule and refund entry
- [ ] 1.4 Job after class: bookings without check-in become `no_show`

## 2 · Interface

- [ ] 2.1 «Book» and «Cancel» on the schedule and in the member area, with the reason when refused
- [ ] 2.2 Policy text shown before confirming a booking inside 12 hours

## 3 · Verification

- [ ] 3.1 A test for every scenario in `specs/bookings.md`, including two members on the last spot at once
- [ ] 3.2 `python tools/changes.py check booking-rules` with no problems

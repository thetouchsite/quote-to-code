# Tasks · weekly-schedule

## 1 · Data

- [x] 1.1 Migration: `rooms`, `instructors`, `class_types`, `class_series`, `sessions`
- [x] 1.2 Nightly job generating sessions eight weeks ahead from series
- [x] 1.3 View `session_availability` with spots left, readable by anyone

## 2 · Interface

- [x] 2.1 Schedule page, week by week, grouped by day, mobile first
- [x] 2.2 Filters by type, level, instructor, saved on the device
- [x] 2.3 «Cancelled» and «full» states

## 3 · Verification

- [x] 3.1 A test for every scenario in `specs/schedule.md`
- [x] 3.2 `python tools/changes.py check weekly-schedule` with no problems

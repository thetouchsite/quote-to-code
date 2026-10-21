## Added requirements

### Requirement: Weekly timetable
The system SHALL show the sessions of the current and the next week, grouped
by day, with class type, level, instructor, room and start time.

#### Scenario: Browsing the week
- **WHEN** a visitor opens the schedule on Monday morning
- **THEN** they see every session from Monday to Sunday
- **AND** they can move to the following week

#### Scenario: Cancelled session
- **WHEN** the front desk cancels Tuesday's 18:30 Vinyasa
- **THEN** the session stays in the timetable marked «cancelled»
- **AND** it cannot be booked

### Requirement: Spots left
The system SHALL show how many spots are left in each session, and «full» when
none are left.

#### Scenario: Last spot
- **WHEN** a session in a 14-person room has 13 active bookings
- **THEN** it shows «1 spot left»

#### Scenario: Full class
- **WHEN** a session has as many active bookings as its capacity
- **THEN** it shows «full»

### Requirement: Filters
The system SHALL let visitors filter the timetable by class type, level and
instructor, and remember the filters on the same device.

#### Scenario: Beginners only
- **WHEN** a visitor selects the level «beginner»
- **THEN** only beginner sessions are shown
- **AND** the filter is still applied when they come back the next day

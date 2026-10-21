## Added requirements

### Requirement: Booking a session
The system SHALL let a signed-in member book a session that has free spots,
is open for booking and is not cancelled, spending one valid credit.

#### Scenario: Booking with credits
- **WHEN** a member with 3 credits books Thursday's 07:00 Hatha
- **THEN** the booking is confirmed
- **AND** the member has 2 credits left

#### Scenario: Last spot taken at the same time
- **WHEN** two members book the last spot of a session in the same second
- **THEN** exactly one booking is confirmed
- **AND** the other member is told the class is full

#### Scenario: No credits
- **WHEN** a member with no valid credits tries to book
- **THEN** the booking is refused
- **AND** the member is offered to buy a drop-in or a pack

### Requirement: Cancellation window
The system SHALL refund the credit when a member cancels more than 12 hours
before the start, and SHALL NOT refund it when they cancel later.

#### Scenario: Early cancellation
- **WHEN** a member cancels 20 hours before the start
- **THEN** the booking is cancelled
- **AND** the credit is back in the member's balance

#### Scenario: Late cancellation
- **WHEN** a member cancels 3 hours before the start
- **THEN** the booking is cancelled as «late»
- **AND** no credit is refunded

### Requirement: No-shows
The system SHALL mark as «no-show» every booking without check-in once the
session has ended.

#### Scenario: Member does not come
- **WHEN** a session ends and a booked member was not checked in
- **THEN** the booking becomes «no-show»
- **AND** the credit stays spent

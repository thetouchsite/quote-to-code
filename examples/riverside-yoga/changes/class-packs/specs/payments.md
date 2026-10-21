## Added requirements

### Requirement: Buying a pack
The system SHALL let a signed-in member buy a drop-in, a pack of 5 or a pack
of 10 by card, and add the credits only once the payment is confirmed.

#### Scenario: Pack of 10
- **WHEN** a member pays for a pack of 10 and Stripe confirms the payment
- **THEN** 10 credits are added to the member's balance
- **AND** they expire 4 months after the purchase

#### Scenario: Confirmation received twice
- **WHEN** Stripe sends the same payment confirmation twice
- **THEN** the credits are added only once

### Requirement: Credit expiry
The system SHALL spend the credits that expire first, and SHALL remove unused
credits when their pack expires.

#### Scenario: Two packs
- **WHEN** a member with a pack expiring in March and one expiring in May books a class
- **THEN** the credit is taken from the March pack

### Requirement: Adjustments by the front desk
The system MUST record who made every manual credit adjustment or refund, and why.

#### Scenario: Goodwill credit
- **WHEN** the front desk adds one credit to a member with the reason «class cancelled by the studio»
- **THEN** the member's balance grows by one
- **AND** the admin log shows who did it, when and why

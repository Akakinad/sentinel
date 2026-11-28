
# Northfield Bank - Card Fraud Policy Manual (fictional)

## POL-001 Automatic block

Transactions with a fraud score at or above the automatic block threshold are declined and the card is blocked immediately.
The customer is notified through their registered channel, and an analyst reviews every automatic block within 24 hours.

## POL-002 Investigation band

Transactions scored between the investigation and block thresholds are sent for investigation.
An automated investigator prepares a recommendation, but a human analyst makes the final decision.

## POL-003 Unusual amount for the customer

A purchase of 5 times or more the customer's average transaction amount over the previous 30 days requires review.
Recommended action: HOLD until the customer confirms the purchase.

## POL-004 High-value online purchase

A single online purchase above 1,000 USD, with no purchase of similar size in the previous 30 days, requires review.
Recommended action: HOLD pending customer verification.

## POL-005 Rapid repeated activity

Three or more transactions on the same card within one hour may indicate card testing or account takeover.
Recommended action: HOLD and contact the customer.

## POL-006 Small test charge followed by large purchase

A very small charge (under 5 USD) followed within 24 hours by a large purchase is a known card-testing pattern.
Recommended action: BLOCK the card and contact the customer.

## POL-007 Night-time high-value online spending

Online purchases above 200 USD made between 22:00 and 04:00 carry elevated risk and require review.
Night-time alone is not grounds for blocking; it must be combined with other risk indicators.

## POL-008 High-risk categories

The categories shopping_net, misc_net and grocery_pos show above-average fraud rates.
A high-risk category increases scrutiny but is never, on its own, a reason to block.

## POL-009 No recent history

If a card has no transactions in the previous 30 days, the customer's normal behaviour is unknown.
Verify with the customer before any block; lack of history alone must not lead to a BLOCK, to protect new customers.

## POL-010 Protected attributes

Decisions must never be based on gender, age, ethnicity, name, home address or occupation.
Only transaction behaviour, amounts, timing, categories and merchant information may be used as evidence.

## POL-011 Customer contact on hold

When a transaction is held, the customer is contacted through their registered channel within one hour.
If the customer confirms the purchase, it is released; if they deny it, the card is blocked and a new card is issued.

## POL-012 Evidence and audit trail

Every recommendation must cite the policy IDs it relies on and the transaction evidence behind it.
Recommendations must not speculate beyond the available data; if evidence is insufficient, recommend HOLD and state what is missing.

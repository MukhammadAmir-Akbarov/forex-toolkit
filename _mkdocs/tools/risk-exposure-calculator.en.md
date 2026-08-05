# Aggregate Risk Calculator

One position may look safe while several trades repeat the same currency bet.
This calculator allocates one total limit, sizes each position and estimates
their combined risk.

!!! warning "Not live correlation"
    The correlation table is static and intended for stress-testing a plan.
    Check current market conditions and news separately.

<div id="risk-exposure-widget" class="fx-tool"></div>

## Reading the result

- **Nominal risk** is the sum of all stop risks.
- **Correlation estimate** is a covariance-style estimate including long/short direction.
- **Exposure** reveals currencies repeated across the portfolio.
- Lot size uses your stop and pip value; verify the contract specification with the broker.

[Pre-trade desk →](trade-desk.md)

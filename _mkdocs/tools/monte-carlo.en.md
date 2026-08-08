---
widgets: [monte-carlo]
---

# Monte Carlo in the Browser

Even a positive-expectancy strategy can produce a painful streak. The simulator
shows outcome ranges, drawdowns, losing streaks and the risk of losing half the capital.

<div id="monte-carlo-widget" class="fx-tool"></div>

## How to use it

1. Use Win Rate and average R:R from at least 50-100 journal trades.
2. Run several risk scenarios: 0.5%, 1% and 2%.
3. Choose a risk where the worst 5% of outcomes remain financially and emotionally tolerable.

In the web journal, **Simulate my results** automatically fills Win Rate, average
R:R, and sample size. With fewer than 30 trades, the simulator clearly warns
that the estimate is not stable yet.

The same `seed` reproduces the same experiment. Calculation stays local and no
parameters are sent over the network.

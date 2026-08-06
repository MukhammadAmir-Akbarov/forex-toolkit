---
widgets: [broker-check]
verified: 2026-08-06
---

# Broker check

!!! abstract "What this tool does"
    It builds direct links to the official registries of five regulators, shows
    historical licence data from the project reference, and helps you tick off
    red flags. You make the decision — the site approves nothing.

!!! danger "A beginner's most expensive mistake is not a bad trade"
    A bad trade costs one risk unit. A firm you cannot withdraw from costs the
    whole deposit. Verify the licence **before** your first deposit, not after
    your first withdrawal problem.

<div id="broker-check-widget"></div>

## Why one licence is not enough

Large brokers usually operate several legal entities:

| Entity | For whom | Protection |
|---|---|---|
| EU / UK | clients in the EU and UK | strict: compensation funds, leverage caps |
| Offshore | often clients from our region | weak: disputes go under offshore law |

The broker's website may talk about the FCA while your account is opened with
the offshore company. So the real question is not "is there a licence at all"
but **"which legal entity holds my account"**.

## How to check a registry

1. Open the regulator link from the widget above.
2. Find the company by name — it must match the name in your contract, not the
   brand on the website.
3. Check the status: is the licence active or withdrawn?
4. Compare the address and licence number with the ones in the site footer.

If the company is not in the registry while the broker claims to be regulated,
that is your complete answer.

## Further reading

- [Scam protection](../uz/scam-protection.md) — how the schemes work and what to
  do if withdrawals have already stopped.
- [Brokers for Uzbekistan](../uz/brokers-uz.md) — what to weigh when choosing.
- [Withdrawing money](../uz/withdrawal-guide.md) — routes and fees.

The same tool is available in the terminal: `forex-broker-check "IC Markets"` or
`python tools/broker_check.py "IC Markets"`.

!!! warning "Not financial advice and not a broker rating"
    The project does not recommend particular brokers and receives no payment
    from them. Licence data are historical reference points and go out of date;
    the only source of truth is the regulator's official registry.

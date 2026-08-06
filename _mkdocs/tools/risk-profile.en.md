---
widgets: [risk-profile]
---

# Trading readiness test

!!! abstract "What this test does"
    30 questions about money, time, psychology and health. At the end you get a
    score from 0 to 100% and a list of weak areas. This is the one tool in the
    project that can honestly tell you: **do not trade yet**.

!!! danger "Answer honestly"
    Only you see the result. It stays in your browser and is never sent anywhere.
    Fooling the test is easy — but you would pay for it with your money, not points.

The [roadmap](../roadmap.md) puts this test in week one. A result below 50% is
not a ban: it is a reason to close the weak areas first — a six-month cushion,
stable income, and your relationship with losses.

<div id="risk-profile-widget"></div>

<script type="application/json" id="risk-profile-questions">
[
  {
    "q": "1. How much money do you plan to put into trading?",
    "category": "finance",
    "options": [
      {
        "label": "Up to 2% of spare money (not living costs)",
        "points": 10
      },
      {
        "label": "5-10% of spare money",
        "points": 5
      },
      {
        "label": "All of my savings",
        "points": -10
      },
      {
        "label": "Credit / borrowed money",
        "points": -20
      }
    ]
  },
  {
    "q": "2. Do you have a safety cushion covering 6 months of living?",
    "category": "finance",
    "options": [
      {
        "label": "Yes, at least 6 months of expenses set aside",
        "points": 10
      },
      {
        "label": "3-5 months",
        "points": 5
      },
      {
        "label": "1-2 months",
        "points": 0
      },
      {
        "label": "No",
        "points": -10
      }
    ]
  },
  {
    "q": "3. Do you have a stable main income?",
    "category": "finance",
    "options": [
      {
        "label": "Yes, permanent job / business",
        "points": 10
      },
      {
        "label": "Freelance / unstable but sufficient",
        "points": 5
      },
      {
        "label": "Occasional side jobs",
        "points": -5
      },
      {
        "label": "No income right now",
        "points": -15
      }
    ]
  },
  {
    "q": "4. If you lost the whole amount, how would it affect your life?",
    "category": "finance",
    "options": [
      {
        "label": "Not at all, I am ready to lose it",
        "points": 10
      },
      {
        "label": "Unpleasant, but I would cope",
        "points": 0
      },
      {
        "label": "Badly, I would have to cut back",
        "points": -10
      },
      {
        "label": "Catastrophically — loans, real trouble",
        "points": -25
      }
    ]
  },
  {
    "q": "5. How many hours a week can you devote to trading?",
    "category": "time",
    "options": [
      {
        "label": "10-20 hours (right for learning)",
        "points": 10
      },
      {
        "label": "5-10 hours",
        "points": 5
      },
      {
        "label": "1-5 hours",
        "points": 0
      },
      {
        "label": "Less than 1 hour",
        "points": -5
      }
    ]
  },
  {
    "q": "6. Are you ready to study for 1-3 years before steady profit?",
    "category": "time",
    "options": [
      {
        "label": "Yes, I understand it is long-term",
        "points": 10
      },
      {
        "label": "I will try for 6-12 months",
        "points": 0
      },
      {
        "label": "I want profit within 3-6 months",
        "points": -10
      },
      {
        "label": "I want profit immediately",
        "points": -25
      }
    ]
  },
  {
    "q": "7. Are you ready to journal every trade?",
    "category": "time",
    "options": [
      {
        "label": "Yes, I understand why it matters",
        "points": 10
      },
      {
        "label": "I will try, but I am not sure",
        "points": 0
      },
      {
        "label": "I see no point in it",
        "points": -10
      }
    ]
  },
  {
    "q": "8. How do you usually react to a financial loss?",
    "category": "psychology",
    "options": [
      {
        "label": "I analyse it and draw conclusions",
        "points": 10
      },
      {
        "label": "I get upset but recover",
        "points": 5
      },
      {
        "label": "I dwell on it for a long time and sleep badly",
        "points": -10
      },
      {
        "label": "I get angry and want to win it back immediately",
        "points": -20
      }
    ]
  },
  {
    "q": "9. What do you do when the plan is not working?",
    "category": "psychology",
    "options": [
      {
        "label": "I follow the plan and review it afterwards",
        "points": 10
      },
      {
        "label": "I sometimes deviate, then come back",
        "points": 0
      },
      {
        "label": "I improvise as I go",
        "points": -10
      },
      {
        "label": "I change the plan straight away",
        "points": -15
      }
    ]
  },
  {
    "q": "10. Can you say no to temptations (food, gambling, shopping)?",
    "category": "psychology",
    "options": [
      {
        "label": "Yes, my self-control is strong",
        "points": 10
      },
      {
        "label": "In most cases",
        "points": 5
      },
      {
        "label": "I slip sometimes",
        "points": 0
      },
      {
        "label": "I slip often",
        "points": -15
      }
    ]
  },
  {
    "q": "11. Have you gambled (casino, betting, poker for money)?",
    "category": "psychology",
    "options": [
      {
        "label": "No / only rarely for fun",
        "points": 10
      },
      {
        "label": "Sometimes, without problems",
        "points": 0
      },
      {
        "label": "I gamble regularly",
        "points": -10
      },
      {
        "label": "I have had problems with addiction",
        "points": -25
      }
    ]
  },
  {
    "q": "12. How do you cope with stress?",
    "category": "psychology",
    "options": [
      {
        "label": "Sport, meditation, talking to people close to me",
        "points": 10
      },
      {
        "label": "Hobbies, I distract myself",
        "points": 5
      },
      {
        "label": "I eat, I watch TV",
        "points": 0
      },
      {
        "label": "Alcohol / smoking / other addictions",
        "points": -15
      }
    ]
  },
  {
    "q": "13. Can you sit through boring periods without acting?",
    "category": "psychology",
    "options": [
      {
        "label": "Yes, not every day is a day for a trade",
        "points": 10
      },
      {
        "label": "Broadly yes",
        "points": 5
      },
      {
        "label": "It is hard, I want to do something",
        "points": -10
      },
      {
        "label": "I cannot sit without acting",
        "points": -15
      }
    ]
  },
  {
    "q": "14. Are you a systematic or an intuitive person?",
    "category": "character",
    "options": [
      {
        "label": "Systematic, I like rules and processes",
        "points": 10
      },
      {
        "label": "Rather systematic",
        "points": 5
      },
      {
        "label": "Rather intuitive",
        "points": -5
      },
      {
        "label": "Entirely on intuition",
        "points": -15
      }
    ]
  },
  {
    "q": "15. Do you take responsibility for your mistakes?",
    "category": "character",
    "options": [
      {
        "label": "Yes, I always look for the cause in myself",
        "points": 10
      },
      {
        "label": "In most cases",
        "points": 5
      },
      {
        "label": "I often blame circumstances",
        "points": -10
      },
      {
        "label": "I blame others / the market / the government",
        "points": -15
      }
    ]
  },
  {
    "q": "16. Are you ready to follow a 10+ item checklist before every trade?",
    "category": "character",
    "options": [
      {
        "label": "Yes, discipline is needed",
        "points": 10
      },
      {
        "label": "I will try, but it is boring",
        "points": 0
      },
      {
        "label": "Too tedious",
        "points": -10
      },
      {
        "label": "Checklists are for the weak",
        "points": -25
      }
    ]
  },
  {
    "q": "17. Do you compare yourself with others?",
    "category": "character",
    "options": [
      {
        "label": "Rarely, I focus on my own progress",
        "points": 10
      },
      {
        "label": "Sometimes",
        "points": 0
      },
      {
        "label": "Often, especially on social media",
        "points": -10
      },
      {
        "label": "Constantly, I need to be the best",
        "points": -15
      }
    ]
  },
  {
    "q": "18. What is your experience with finance?",
    "category": "experience",
    "options": [
      {
        "label": "I budget and invest in ETFs / stocks",
        "points": 10
      },
      {
        "label": "I know the basics, I invest sometimes",
        "points": 5
      },
      {
        "label": "Basic knowledge (banks, loans)",
        "points": 0
      },
      {
        "label": "Minimal",
        "points": -5
      }
    ]
  },
  {
    "q": "19. Have you studied anything about forex / trading?",
    "category": "experience",
    "options": [
      {
        "label": "I have read several books and taken courses",
        "points": 10
      },
      {
        "label": "I have watched YouTube and articles",
        "points": 5
      },
      {
        "label": "I have read nothing, I am starting",
        "points": 0
      },
      {
        "label": "I believed adverts about easy money",
        "points": -20
      }
    ]
  },
  {
    "q": "20. Are you familiar with programming / mathematics?",
    "category": "experience",
    "options": [
      {
        "label": "Yes, I can write a script",
        "points": 10
      },
      {
        "label": "I understand the basic logic",
        "points": 5
      },
      {
        "label": "Not really",
        "points": 0
      },
      {
        "label": "Not at all",
        "points": -5
      }
    ]
  },
  {
    "q": "21. How many hours do you sleep on average?",
    "category": "health",
    "options": [
      {
        "label": "7-9 hours consistently",
        "points": 10
      },
      {
        "label": "6-7 hours",
        "points": 0
      },
      {
        "label": "5-6 hours",
        "points": -10
      },
      {
        "label": "Less than 5 hours",
        "points": -20
      }
    ]
  },
  {
    "q": "22. Do you exercise?",
    "category": "health",
    "options": [
      {
        "label": "3+ times a week",
        "points": 10
      },
      {
        "label": "1-2 times a week",
        "points": 5
      },
      {
        "label": "Rarely",
        "points": 0
      },
      {
        "label": "Never",
        "points": -5
      }
    ]
  },
  {
    "q": "23. Do you drink alcohol regularly?",
    "category": "health",
    "options": [
      {
        "label": "No / very rarely",
        "points": 10
      },
      {
        "label": "At weekends",
        "points": 0
      },
      {
        "label": "2-3 times a week",
        "points": -10
      },
      {
        "label": "Daily",
        "points": -20
      }
    ]
  },
  {
    "q": "24. Do the people close to you know you are going to trade?",
    "category": "relationships",
    "options": [
      {
        "label": "Yes, and they support me / are neutral",
        "points": 10
      },
      {
        "label": "They know, but they are against it",
        "points": 0
      },
      {
        "label": "I hide it",
        "points": -10
      },
      {
        "label": "I hide it and I use their money",
        "points": -25
      }
    ]
  },
  {
    "q": "25. Are your relationships / family stable?",
    "category": "relationships",
    "options": [
      {
        "label": "Yes, all is well",
        "points": 10
      },
      {
        "label": "Broadly stable",
        "points": 5
      },
      {
        "label": "There are problems",
        "points": -5
      },
      {
        "label": "In crisis / separating",
        "points": -10
      }
    ]
  },
  {
    "q": "26. Why do you want to trade forex?",
    "category": "motivation",
    "options": [
      {
        "label": "It interests me as a profession, I am ready to learn",
        "points": 10
      },
      {
        "label": "Extra income plus interest",
        "points": 5
      },
      {
        "label": "I need money, I hope to earn quickly",
        "points": -10
      },
      {
        "label": "Everyone around is earning, I want it too",
        "points": -20
      }
    ]
  },
  {
    "q": "27. What does success in trading after 1 year mean to you?",
    "category": "motivation",
    "options": [
      {
        "label": "Not blowing the account and understanding the market",
        "points": 10
      },
      {
        "label": "A steady 1-3% a month",
        "points": 5
      },
      {
        "label": "10-20% a month",
        "points": -10
      },
      {
        "label": "Quitting my job / buying a car",
        "points": -20
      }
    ]
  },
  {
    "q": "28. If you lost the whole deposit, what would you do?",
    "category": "warnings",
    "options": [
      {
        "label": "Pause, analyse, possibly never come back",
        "points": 10
      },
      {
        "label": "Take a 1-3 month break, then think",
        "points": 5
      },
      {
        "label": "Top it up straight away",
        "points": -15
      },
      {
        "label": "Take a loan and try again",
        "points": -30
      }
    ]
  },
  {
    "q": "29. Have you bought signals on Telegram / from a guru?",
    "category": "warnings",
    "options": [
      {
        "label": "No / I would not",
        "points": 10
      },
      {
        "label": "I considered it but decided against it",
        "points": 5
      },
      {
        "label": "I bought some, but not any more",
        "points": -5
      },
      {
        "label": "I buy them regularly",
        "points": -15
      }
    ]
  },
  {
    "q": "30. Are you ready to trade only on demo for the first 3-6 months?",
    "category": "warnings",
    "options": [
      {
        "label": "Yes, I understand why it matters",
        "points": 10
      },
      {
        "label": "A month or two",
        "points": 0
      },
      {
        "label": "I want to go live straight away",
        "points": -15
      },
      {
        "label": "I have already opened live and started trading",
        "points": -25
      }
    ]
  }
]
</script>

## How to read the result

| Result | What it means |
|---|---|
| 80% and above | Excellent profile: cushion in place, expectations realistic |
| 60-80% | Good profile, but close the weak spots before real money |
| 40-60% | Borderline: at least six months of preparation |
| 20-40% | High risk: do not start yet |
| below 20% | Critical risk: long-term investing is safer |

Percentages are measured against a maximum of 300 points. Poor answers subtract
points, so the result can be negative — that is normal and means exactly what
the verdict says.

## What to do about weak areas

- **Finance** — a six-month cushion and stable income come first. Trading on
  borrowed money has no good outcome.
- **Psychology** — wanting to win it back immediately after a loss is the most
  expensive habit in trading. [Emotion breakdown in the journal](../journal/web-journal.md).
- **Time** — under an hour a week is not even enough to review your own trades.
- **Red flags** — if there is a tendency to gambling or addiction, talk to a
  specialist before opening an account.

The same test is available in the terminal: `forex-risk-profile` or
`python tools/risk_profile.py`. The web version and the CLI score identically —
that is covered by tests.

!!! warning "Not financial advice"
    This is an educational self-check, not an assessment from a financial
    adviser and not a guarantee of any outcome.

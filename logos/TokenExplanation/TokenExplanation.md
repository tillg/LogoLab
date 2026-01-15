# Token explanation

I would like to have a nice image that explains how tokens add up and are checked against limits. This is the basic content:

```text
┌─────────────────────────────────────────────┐
│           CONTEXT WINDOW (e.g. 16K)         │
├─────────────────────────────────────────────┤
│  INPUT                    │  OUTPUT         │
│  • System prompt          │  • LLM response │
│  • Page content           │  • Tool calls   │
│  • Chat history           │                 │
│  • Tool definitions       │                 │
├─────────────────────────────────────────────┤
│  INPUT + OUTPUT must fit within CONTEXT     │
└─────────────────────────────────────────────┘
```

Pls make me an SVG that represents this.
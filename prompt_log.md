# Prompt Log

AI tool used: Claude, used throughout for API research, planning, and code generation/debugging.

Key prompts that shaped the build:

- Asked Claude to identify real, verified public APIs relevant to stats/econ/traffic, including checking that endpoints actually existed rather than trusting a plausible-looking guess.
- Asked Claude to assess feasibility honestly for a traffic-scenario prediction game and identify what real data could and couldn't support before committing to a design.
- Asked for the exact Socrata `$where` query syntax to filter Chicago's traffic dataset by region and date range, and to explain the response fields before building anything on top of it.
- Asked how to join per-hour weather data against traffic readings that update more often than hourly, since multiple readings land in the same hour.
- Asked for help designing the Flask session-based round/score state across multiple page loads, and later to diagnose a bug where refreshing the browser silently advanced the round counter past the max.
- Asked Claude to review the actual project folder directly and find/fix real bugs (a template variable that was computed but never passed to the page, an unwired weighting feature, and a malformed template tag) rather than guessing blind from conversation.

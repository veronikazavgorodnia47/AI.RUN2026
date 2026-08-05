# By-hand vs Agent — K 7.W.7

## What the agent built
Full bronze → silver → gold → DQ → charts pipeline for the online course completions dataset in one pass:
- 500-row generator with seed, mixed date formats, nulls, duplicates
- Bronze landing → silver cleaning (nulls removed, dedup, 3 date formats standardised)
- Two gold tables: daily_completions_by_category + dropout_rate
- 6 DQ checks, all passing
- Two plotly charts (completion % by category, dropout rate over time)

## One time-saving
The agent rebuilt the entire 5-layer pipeline pattern on a new dataset in a single cell — work equivalent to katas K 7.W.1 through K 7.W.6 (~90 min by hand). The boilerplate (generator structure, COPY syntax, ROW_NUMBER dedup, regexp date parsing, DQ check loop) transferred without any re-prompting.

## One thing a human must verify
The `avg_completion_pct` metric averages `completion_pct` across **all** enrollment statuses — including students who dropped at 10% and those still in progress. Whether dropped and in-progress students should be included in the average is a business rule the agent cannot decide from the spec alone. A product manager must confirm: does "avg completion %" mean "among all who started" or "among those who finished"? The SQL is technically correct either way — only the business definition determines which is right.

## Conclusion
The agent is AI-assisted, not AI-autonomous. It saves time on pattern transfer and boilerplate. It cannot substitute for the human who owns the metric definition.

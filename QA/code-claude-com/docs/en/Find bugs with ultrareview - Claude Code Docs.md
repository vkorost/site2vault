---
title: Find bugs with ultrareview - Claude Code Docs
source_url: https://code.claude.com/docs/en/ultrareview
description: Run a deep, multi-agent code review in the cloud with /ultrareview to
  find and verify bugs before you merge.
---

Ultrareview is a research preview feature available in Claude Code v2.1.86 and later. The feature, pricing, and availability may change based on feedback.

```
/ultrareview
```

, Claude Code launches a fleet of reviewer agents in a remote sandbox to find bugs in your branch or pull request.
Compared to a local

```
/review
```

, ultrareview offers:

- Higher signal: every reported finding is independently reproduced and verified, so the results focus on real bugs rather than style suggestions
- Broader coverage: many reviewer agents explore the change in parallel, which surfaces issues that a single-pass review can miss
- No local resource use: the review runs entirely in a remote sandbox, so your terminal stays free for other work while it runs

```
/login
```

and authenticate with Claude.ai first. Ultrareview is not available when using Claude Code with Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry, and it is not available to organizations that have enabled Zero Data Retention.

## Run ultrareview from the CLI

Start a review from any git repository in the Claude Code CLI.

```
github.com
```

remote on the repository.
Before launching, Claude Code shows a confirmation dialog with the review scope (including the file and line count when reviewing a branch), your remaining free runs, and the estimated cost. After you confirm, the review continues in the background and you can keep using your session. The command runs only when you invoke it with

```
/ultrareview
```

; Claude does not start an ultrareview on its own.

## Pricing and free runs

Ultrareview is a premium feature that bills against extra usage rather than your plan’s included usage.

PlanIncluded free runsAfter free runsPro3 free runs through May 5, 2026billed as

[extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)[extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)

```
/extra-usage
```

to check or change your current setting.

## Track a running review

A review typically takes 5 to 10 minutes. The review runs as a background task, so you can keep working in your session, start other commands, or close the terminal entirely. Use

```
/tasks
```

to see running and completed reviews, open the detail view for a review, or stop a review that is in progress. Stopping a review archives the cloud session, and partial findings are not returned. When the review finishes, the verified findings appear as a notification in your session. Each finding includes the file location and an explanation of the issue so you can ask Claude to fix it directly.

## How ultrareview compares to /review

Both commands review code, but they target different stages of your workflow.

```
/review
```

```
/ultrareview
```

Runslocally in your sessionremotely in a cloud sandboxDepthsingle-pass reviewmulti-agent fleet with independent verificationDurationseconds to a few minutesroughly 5 to 10 minutesCostcounts toward normal usagefree runs, then roughly $5 to $20 per review as extra usageBest forquick feedback while iteratingpre-merge confidence on substantial changes

```
/review
```

for fast feedback as you work. Use

```
/ultrareview
```

before merging a substantial change when you want a deeper pass that catches issues a single review might miss.

## Related resources

- [[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]: learn how remote sessions and cloud sandboxes work
- [[Plan in the cloud with ultraplan - Claude Code Docs|Plan complex changes with ultraplan]]: the planning counterpart to ultrareview for upfront design work
- [[Manage costs effectively - Claude Code Docs|Manage costs effectively]]: track usage and set spending limits

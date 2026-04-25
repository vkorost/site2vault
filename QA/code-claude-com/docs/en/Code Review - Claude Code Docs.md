---
title: Code Review - Claude Code Docs
source_url: https://code.claude.com/docs/en/code-review
description: Set up automated PR reviews that catch logic errors, security vulnerabilities,
  and regressions using multi-agent analysis of your full codebase
---

Code Review is in research preview, available for

[Team and Enterprise](https://claude.ai/admin-settings/claude-code)subscriptions. It is not available for organizations with[[Zero data retention - Claude Code Docs|Zero Data Retention]]enabled.

```
CLAUDE.md
```

or

```
REVIEW.md
```

file to your repository.
To run Claude in your own CI infrastructure instead of this managed service, see

[[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]or

[[Claude Code GitLab CICD - Claude Code Docs|GitLab CI/CD]]. For repositories on a self-hosted GitHub instance, see

[[Claude Code with GitHub Enterprise Server - Claude Code Docs|GitHub Enterprise Server]]. This page covers:

- [[Code Review - Claude Code Docs#How reviews work|How reviews work]]
- [[Code Review - Claude Code Docs#Set up Code Review|Setup]]
- [[Code Review - Claude Code Docs#Manually trigger reviews|Triggering reviews manually]]with

  ```
  @claude review
  ```

  and

  ```
  @claude review once
  ```
- [[Code Review - Claude Code Docs#Customize reviews|Customizing reviews]]with

  ```
  CLAUDE.md
  ```

  and

  ```
  REVIEW.md
  ```
- [[Code Review - Claude Code Docs#Pricing|Pricing]]
- [[Code Review - Claude Code Docs#Troubleshooting|Troubleshooting]]failed runs and missing comments

## How reviews work

Once an admin

[[Code Review - Claude Code Docs#Set up Code Review|enables Code Review]]for your organization, reviews trigger when a PR opens, on every push, or when manually requested, depending on the repository’s configured behavior. Commenting

```
@claude review
```

[[Code Review - Claude Code Docs#Manually trigger reviews|starts reviews on a PR]]in any mode. When a review runs, multiple agents analyze the diff and surrounding code in parallel on Anthropic infrastructure. Each agent looks for a different class of issue, then a verification step checks candidates against actual code behavior to filter out false positives. The results are deduplicated, ranked by severity, and posted as inline comments on the specific lines where issues were found, with a summary in the review body. If no issues are found, Claude posts a short confirmation comment on the PR. Reviews scale in cost with PR size and complexity, completing in 20 minutes on average. Admins can monitor review activity and spend via the

[[Code Review - Claude Code Docs#View usage|analytics dashboard]].

### Severity levels

Each finding is tagged with a severity level:

MarkerSeverityMeaning🔴ImportantA bug that should be fixed before merging🟡NitA minor issue, worth fixing but not blocking🟣Pre-existingA bug that exists in the codebase but was not introduced by this PR

### Rate and reply to findings

Each review comment from Claude arrives with 👍 and 👎 already attached so both buttons appear in the GitHub UI for one-click rating. Click 👍 if the finding was useful or 👎 if it was wrong or noisy. Anthropic collects reaction counts after the PR merges and uses them to tune the reviewer. Reactions do not trigger a re-review or change anything on the PR. Replying to an inline comment does not prompt Claude to respond or update the PR. To act on a finding, fix the code and push. If the PR is subscribed to push-triggered reviews, the next run resolves the thread when the issue is fixed. To request a fresh review without pushing, comment

```
@claude review once
```

as a

[[Code Review - Claude Code Docs#Manually trigger reviews|top-level PR comment]].

### Check run output

Beyond the inline review comments, each review populates the Claude Code Review check run that appears alongside your CI checks. Expand its Details link to see a summary of every finding in one place, sorted by severity:

SeverityFile:LineIssue🔴 Important

```
src/auth/session.ts:142
```

Token refresh races with logout, leaving stale sessions active🟡 Nit

```
src/auth/session.ts:88
```

```
parseExpiry
```

silently returns 0 on malformed input

```
gh
```

and jq:

```
{"normal": 2, "nit": 1, "pre_existing": 0}
```

. The

```
normal
```

key holds the count of Important findings; a non-zero value means Claude found at least one bug worth fixing before merge.

### What Code Review checks

By default, Code Review focuses on correctness: bugs that would break production, not formatting preferences or missing test coverage. You can expand what it checks by

[[Code Review - Claude Code Docs#Customize reviews|adding guidance files]]to your repository.

## Set up Code Review

An admin enables Code Review once for the organization and selects which repositories to include.

Open Claude Code admin settings

Go to

[claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)and find the Code Review section. You need admin access to your Claude organization and permission to install GitHub Apps in your GitHub organization.

Install the Claude GitHub App

Follow the prompts to install the Claude GitHub App to your GitHub organization. The app requests these repository permissions:

- Contents: read and write
- Issues: read and write
- Pull requests: read and write

[[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]if you enable that later.

Select repositories

Choose which repositories to enable for Code Review. If you don’t see a repository, make sure you gave the Claude GitHub App access to it during installation. You can add more repositories later.

Set review triggers per repo

After setup completes, the Code Review section shows your repositories in a table. For each repository, use the Review Behavior dropdown to choose when reviews run:

- Once after PR creation: review runs once when a PR is opened or marked ready for review
- After every push: review runs on every push to the PR branch, catching new issues as the PR evolves and auto-resolving threads when you fix flagged issues
- Manual: reviews start only when someone [[Code Review - Claude Code Docs#Manually trigger reviews|comments]];

  ```
  @claude review
  ```

  or

  ```
  @claude review once
  ```

  on a PR

  ```
  @claude review
  ```

  also subscribes the PR to reviews on subsequent pushes

```
@claude review
```

on the PR to start the first review. If no check run appears, confirm the repository is listed in your admin settings and the Claude GitHub App has access to it.

## Manually trigger reviews

Two comment commands start a review on demand. Both work regardless of the repository’s configured trigger, so you can use them to opt specific PRs into review in Manual mode or to get an immediate re-review in other modes.

CommandWhat it does

```
@claude review
```

Starts a review and subscribes the PR to push-triggered reviews going forward

```
@claude review once
```

Starts a single review without subscribing the PR to future pushes

```
@claude review once
```

when you want feedback on the current state of a PR but don’t want every subsequent push to incur a review. This is useful for long-running PRs with frequent pushes, or when you want a one-off second opinion without changing the PR’s review behavior.
For either command to trigger a review:

- Post it as a top-level PR comment, not an inline comment on a diff line
- Put the command at the start of the comment, with

  ```
  once
  ```

  on the same line if you’re using the one-shot form
- You must have owner, member, or collaborator access to the repository
- The PR must be open

## Customize reviews

Code Review reads two files from your repository to guide what it flags. They differ in how strongly they influence the review:

- ```
  CLAUDE.md
  ```

  : shared project instructions that Claude Code uses for all tasks, not just reviews. Code Review reads it as project context and flags newly introduced violations as nits.
- ```
  REVIEW.md
  ```

  : review-only instructions, injected directly into every agent in the review pipeline as highest priority. Use it to change what gets flagged, at what severity, and how findings are reported.

### CLAUDE.md

Code Review reads your repository’s

```
CLAUDE.md
```

files and treats newly introduced violations as

[[Code Review - Claude Code Docs#Severity levels|nit-level]]findings. This works bidirectionally: if your PR changes code in a way that makes a

```
CLAUDE.md
```

statement outdated, Claude flags that the docs need updating too.
Claude reads

```
CLAUDE.md
```

files at every level of your directory hierarchy, so rules in a subdirectory’s

```
CLAUDE.md
```

apply only to files under that path. See the

[[How Claude remembers your project - Claude Code Docs|memory documentation]]for more on how

```
CLAUDE.md
```

works.
For review-specific guidance that you don’t want applied to general Claude Code sessions, use

[[Code Review - Claude Code Docs|instead.]]

```
REVIEW.md
```

### REVIEW.md

```
REVIEW.md
```

is a file at your repository root that overrides how Code Review behaves on your repo. Its contents are injected into the system prompt of every agent in the review pipeline as the highest-priority instruction block, taking precedence over the default review guidance.
Because it’s pasted verbatim,

```
REVIEW.md
```

is plain instructions:

[[How Claude remembers your project - Claude Code Docs#Import additional files|is not expanded, and referenced files are not read into the prompt. Put the rules you want enforced directly in the file.]]

```
@
```

import syntax

#### What you can tune

```
REVIEW.md
```

is freeform markdown, so anything you can express as a review instruction is in scope. The patterns below have the most impact in practice.
Severity: redefine what 🔴 Important means for your repo. The default calibration targets production code; a docs repo, a config repo, or a prototype might want a much narrower definition. State explicitly which classes of finding are Important and which are Nit at most. You can also escalate in the other direction, for example treating any

```
CLAUDE.md
```

violation as Important rather than the default nit.
Nit volume: cap how many 🟡 Nit comments a single review posts. Prose and config files can be polished forever. A cap like “report at most five nits, mention the rest as a count in the summary” keeps reviews actionable.
Skip rules: list paths, branch patterns, and finding categories where Claude should post no findings. Common candidates are generated code, lockfiles, vendored dependencies, and machine-authored branches, along with anything your CI already enforces like linting or spellcheck. For paths that warrant some review but not full scrutiny, set a higher bar instead of skipping entirely: “in

```
scripts/
```

, only report if near-certain and severe.”
Repo-specific checks: add rules you want flagged on every PR, like “new API routes must have an integration test.” Because

```
REVIEW.md
```

is injected as highest priority, these land more reliably than the same rules in a long

```
CLAUDE.md
```

.
Verification bar: require evidence before a class of finding is posted. For example, “behavior claims need a

```
file:line
```

citation in the source, not an inference from naming” cuts false positives that would otherwise cost the author a round trip.
Re-review convergence: tell Claude how to behave when a PR has already been reviewed. A rule like “after the first review, suppress new nits and post Important findings only” stops a one-line fix from reaching round seven on style alone.
Summary shape: ask for the review body to open with a one-line tally such as

```
2 factual, 4 style
```

, and to lead with “no factual issues” when that’s the case. The author wants to know the shape of the work before the details.

#### Example

This

```
REVIEW.md
```

recalibrates severity for a backend service, caps nits, skips generated files, and adds repo-specific checks.

#### Keep it focused

Length has a cost: a long

```
REVIEW.md
```

dilutes the rules that matter most. Keep it to instructions that change review behavior, and leave general project context in

```
CLAUDE.md
```

.

## View usage

Go to

[claude.ai/analytics/code-review](https://claude.ai/analytics/code-review)to see Code Review activity across your organization. The dashboard shows:

SectionWhat it showsPRs reviewedDaily count of pull requests reviewed over the selected time rangeCost weeklyWeekly spend on Code ReviewFeedbackCount of review comments that were auto-resolved because a developer addressed the issueRepository breakdownPer-repo counts of PRs reviewed and comments resolved

## Pricing

Code Review is billed based on token usage. Each review averages $15-25 in cost, scaling with PR size, codebase complexity, and how many issues require verification. Code Review usage is billed separately through

[extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)and does not count against your plan’s included usage. The review trigger you choose affects total cost:

- Once after PR creation: runs once per PR
- After every push: runs on each push, multiplying cost by the number of pushes
- Manual: no reviews until someone comments

  ```
  @claude review
  ```

  on a PR

```
@claude review
```

[[Code Review - Claude Code Docs#Manually trigger reviews|opts the PR into push-triggered reviews]], so additional cost accrues per push after that comment. To run a single review without subscribing to future pushes, comment

```
@claude review once
```

instead.
Costs appear on your Anthropic bill regardless of whether your organization uses AWS Bedrock or Google Vertex AI for other Claude Code features. To set a monthly spend cap for Code Review, go to

[claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage)and configure the limit for the Claude Code Review service. Monitor spend via the weekly cost chart in

[[Code Review - Claude Code Docs#View usage|analytics]]or the per-repo average cost column in admin settings.

## Troubleshooting

Review runs are best-effort. A failed run never blocks your PR, but it also doesn’t retry on its own. This section covers how to recover from a failed run and where to look when the check run reports issues you can’t find.

### Retrigger a failed or timed-out review

When the review infrastructure hits an internal error or exceeds its time limit, the check run completes with a title of Code review encountered an error or Code review timed out. The conclusion is still neutral, so nothing blocks your merge, but no findings are posted. To run the review again, comment

```
@claude review once
```

on the PR. This starts a fresh review without subscribing the PR to future pushes. If the PR is already subscribed to push-triggered reviews, pushing a new commit also starts a new review.
The Re-run button in GitHub’s Checks tab does not retrigger Code Review. Use the comment command or a new push instead.

### Review didn’t run and the PR shows a spend-cap message

When your organization’s monthly spend cap is reached, Code Review posts a single comment on the PR explaining that the review was skipped. Reviews resume automatically at the start of the next billing period, or immediately when an admin raises the cap at

[claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage).

### Find issues that aren’t showing as inline comments

If the check run title says issues were found but you don’t see inline review comments on the diff, look in these other locations where findings are surfaced:

- Check run Details: click Details next to the Claude Code Review check in the Checks tab. The severity table lists every finding with its file, line, and summary regardless of whether the inline comment was accepted.
- Files changed annotations: open the Files changed tab on the PR. Findings render as annotations attached directly to the diff lines, separate from review comments.
- Review body: if you pushed to the PR while a review was running, some findings may reference lines that no longer exist in the current diff. Those appear under an Additional findings heading in the review body text rather than as inline comments.

## Related resources

Code Review is designed to work alongside the rest of Claude Code. If you want to run reviews locally before opening a PR, need a self-hosted setup, or want to go deeper on how

```
CLAUDE.md
```

shapes Claude’s behavior across tools, these pages are good next stops:

- [[Discover and install prebuilt plugins through marketplaces - Claude Code Docs|Plugins]]: browse the plugin marketplace, including a

  ```
  code-review
  ```

  plugin for running on-demand reviews locally before pushing
- [[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]: run Claude in your own GitHub Actions workflows for custom automation beyond code review
- [[Claude Code GitLab CICD - Claude Code Docs|GitLab CI/CD]]: self-hosted Claude integration for GitLab pipelines
- [[How Claude remembers your project - Claude Code Docs|Memory]]: how

  ```
  CLAUDE.md
  ```

  files work across Claude Code
- [[Track team usage with analytics - Claude Code Docs|Analytics]]: track Claude Code usage beyond code review

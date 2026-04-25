---
title: Run prompts on a schedule - Claude Code Docs
source_url: https://code.claude.com/docs/en/scheduled-tasks
description: Use /loop and the cron scheduling tools to run prompts repeatedly, poll
  for status, or set one-time reminders within a Claude Code session.
---

Scheduled tasks require Claude Code v2.1.72 or later. Check your version with

```
claude --version
```

.

[[Push events into a running session with channels - Claude Code Docs|Channels]]: your CI can push the failure into the session directly. Tasks are session-scoped: they live in the current conversation and stop when you start a new one. Resuming with

```
--resume
```

or

```
--continue
```

brings back any task that hasn’t

[[Run prompts on a schedule - Claude Code Docs#Seven-day expiry|expired]]: a recurring task created within the last 7 days, or a one-shot whose scheduled time hasn’t passed yet. For scheduling that survives independently of any session, use

[[Automate work with routines - Claude Code Docs|Routines]],

[[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|Desktop scheduled tasks]], or

[[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]].

## Compare scheduling options

Claude Code offers three ways to schedule recurring or one-off work:

[[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|Desktop]]

```
/loop
```

```
--resume
```

if unexpired[[Connect Claude Code to tools via MCP - Claude Code Docs|Config files]]and connectors

```
/schedule
```

in the CLI

## Run a prompt repeatedly with /loop

The

```
/loop
```

[[Commands - Claude Code Docs|bundled skill]]is the quickest way to run a prompt on repeat while the session stays open. Both the interval and the prompt are optional, and what you provide determines how the loop behaves.

What you provideExampleWhat happensInterval and prompt

```
/loop 5m check the deploy
```

Your prompt runs on a

```
/loop check the deploy
```

[[Run prompts on a schedule - Claude Code Docs#Let Claude choose the interval|interval Claude chooses]]each iteration

```
/loop
```

[[Run prompts on a schedule - Claude Code Docs#Run the built-in maintenance prompt|built-in maintenance prompt]]runs, or your

```
loop.md
```

if one exists

```
/loop 20m /review-pr 1234
```

, to re-run a packaged workflow each iteration.

### Run on a fixed interval

When you supply an interval, Claude converts it to a cron expression, schedules the job, and confirms the cadence and job ID.

```
30m
```

, or trail it as a clause like

```
every 2 hours
```

. Supported units are

```
s
```

for seconds,

```
m
```

for minutes,

```
h
```

for hours, and

```
d
```

for days.
Seconds are rounded up to the nearest minute since cron has one-minute granularity. Intervals that don’t map to a clean cron step, such as

```
7m
```

or

```
90m
```

, are rounded to the nearest interval that does and Claude tells you what it picked.

### Let Claude choose the interval

When you omit the interval, Claude chooses one dynamically instead of running on a fixed cron schedule. After each iteration it picks a delay between one minute and one hour based on what it observed: short waits while a build is finishing or a PR is active, longer waits when nothing is pending. The chosen delay and the reason for it are printed at the end of each iteration. The example below checks CI and review comments, with Claude waiting longer between iterations once the PR goes quiet:

```
/loop
```

schedule, Claude may use the

[[Tools reference - Claude Code Docs#Monitor tool|Monitor tool]]directly. Monitor runs a background script and streams each output line back, which avoids polling altogether and is often more token-efficient and responsive than re-running a prompt on an interval. A dynamically scheduled loop appears in your

[[Run prompts on a schedule - Claude Code Docs#Manage scheduled tasks|scheduled task list]]like any other task, so you can list or cancel it the same way. The

[[Run prompts on a schedule - Claude Code Docs#Jitter|jitter rules]]don’t apply to it, but the

[[Run prompts on a schedule - Claude Code Docs#Seven-day expiry|seven-day expiry]]does: the loop ends automatically seven days after you start it.

On Bedrock, Vertex AI, and Microsoft Foundry, a prompt with no interval runs on a fixed 10-minute schedule instead.

### Run the built-in maintenance prompt

When you omit the prompt, Claude uses a built-in maintenance prompt instead of one you supply. On each iteration it works through the following, in order:

- continue any unfinished work from the conversation
- tend to the current branch’s pull request: review comments, failed CI runs, merge conflicts
- run cleanup passes such as bug hunts or simplification when nothing else is pending

```
/loop
```

runs this prompt at a

[[Run prompts on a schedule - Claude Code Docs#Let Claude choose the interval|dynamically chosen interval]]. Add an interval, for example

```
/loop 15m
```

, to run it on a fixed schedule instead. To replace the built-in prompt with your own default, see

[[Run prompts on a schedule - Claude Code Docs|Customize the default prompt with loop.md]].

On Bedrock, Vertex AI, and Microsoft Foundry,

```
/loop
```

with no prompt prints the usage message instead of starting the maintenance loop.

### Customize the default prompt with loop.md

A

```
loop.md
```

file replaces the built-in maintenance prompt with your own instructions. It defines a single default prompt for bare

```
/loop
```

, not a list of separate scheduled tasks, and is ignored whenever you supply a prompt on the command line. To schedule additional prompts alongside it, use

```
/loop <prompt>
```

or

[[Run prompts on a schedule - Claude Code Docs#Manage scheduled tasks|ask Claude directly]]. Claude looks for the file in two locations and uses the first one it finds.

PathScope

```
.claude/loop.md
```

Project-level. Takes precedence when both files exist.

```
~/.claude/loop.md
```

User-level. Applies in any project that does not define its own.

```
/loop
```

prompt directly. The following example keeps a release branch healthy:

.claude/loop.md

```
loop.md
```

take effect on the next iteration, so you can refine the instructions while a loop is running. When no

```
loop.md
```

exists in either location, the loop falls back to the built-in maintenance prompt. Keep the file concise: content beyond 25,000 bytes is truncated.

### Stop a loop

To stop a

```
/loop
```

while it is waiting for the next iteration, press

```
Esc
```

. This clears the pending wakeup so the loop does not fire again. Tasks you scheduled by

[[Run prompts on a schedule - Claude Code Docs#Manage scheduled tasks|asking Claude directly]]are not affected by

```
Esc
```

and stay in place until you delete them.

## Set a one-time reminder

For one-shot reminders, describe what you want in natural language instead of using

```
/loop
```

. Claude schedules a single-fire task that deletes itself after running.

## Manage scheduled tasks

Ask Claude in natural language to list or cancel tasks, or reference the underlying tools directly.

ToolPurpose

```
CronCreate
```

Schedule a new task. Accepts a 5-field cron expression, the prompt to run, and whether it recurs or fires once.

```
CronList
```

List all scheduled tasks with their IDs, schedules, and prompts.

```
CronDelete
```

Cancel a task by ID.

```
CronDelete
```

. A session can hold up to 50 scheduled tasks at once.

## How scheduled tasks run

The scheduler checks every second for due tasks and enqueues them at low priority. A scheduled prompt fires between your turns, not while Claude is mid-response. If Claude is busy when a task comes due, the prompt waits until the current turn ends. All times are interpreted in your local timezone. A cron expression like

```
0 9 * * *
```

means 9am wherever you’re running Claude Code, not UTC.

### Jitter

To avoid every session hitting the API at the same wall-clock moment, the scheduler adds a small deterministic offset to fire times:

- Recurring tasks fire up to 10% of their period late, capped at 15 minutes. An hourly job might fire anywhere from

  ```
  :00
  ```

  to

  ```
  :06
  ```

  .
- One-shot tasks scheduled for the top or bottom of the hour fire up to 90 seconds early.

```
:00
```

or

```
:30
```

, for example

```
3 9 * * *
```

instead of

```
0 9 * * *
```

, and the one-shot jitter will not apply.

### Seven-day expiry

Recurring tasks automatically expire 7 days after creation. The task fires one final time, then deletes itself. This bounds how long a forgotten loop can run. If you need a recurring task to last longer, cancel and recreate it before it expires, or use

[[Automate work with routines - Claude Code Docs|Routines]]or

[[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|Desktop scheduled tasks]]for durable scheduling.

## Cron expression reference

```
CronCreate
```

accepts standard 5-field cron expressions:

```
minute hour day-of-month month day-of-week
```

. All fields support wildcards (

```
*
```

), single values (

```
5
```

), steps (

```
*/15
```

), ranges (

```
1-5
```

), and comma-separated lists (

```
1,15,30
```

).

ExampleMeaning

```
*/5 * * * *
```

Every 5 minutes

```
0 * * * *
```

Every hour on the hour

```
7 * * * *
```

Every hour at 7 minutes past

```
0 9 * * *
```

Every day at 9am local

```
0 9 * * 1-5
```

Weekdays at 9am local

```
30 14 15 3 *
```

March 15 at 2:30pm local

```
0
```

or

```
7
```

for Sunday through

```
6
```

for Saturday. Extended syntax like

```
L
```

,

```
W
```

,

```
?
```

, and name aliases such as

```
MON
```

or

```
JAN
```

is not supported.
When both day-of-month and day-of-week are constrained, a date matches if either field matches. This follows standard vixie-cron semantics.

## Disable scheduled tasks

Set

```
CLAUDE_CODE_DISABLE_CRON=1
```

in your environment to disable the scheduler entirely. The cron tools and

```
/loop
```

become unavailable, and any already-scheduled tasks stop firing. See

[[Environment variables - Claude Code Docs|Environment variables]]for the full list of disable flags.

## Limitations

Session-scoped scheduling has inherent constraints:

- Tasks only fire while Claude Code is running and idle. Closing the terminal or letting the session exit stops them firing.
- No catch-up for missed fires. If a task’s scheduled time passes while Claude is busy on a long-running request, it fires once when Claude becomes idle, not once per missed interval.
- Starting a fresh conversation clears all session-scoped tasks. Resuming with

  ```
  claude --resume
  ```

  or

  ```
  claude --continue
  ```

  restores tasks that have not expired: recurring tasks within seven days of creation, and one-shot tasks whose scheduled time has not yet passed. Background Bash and monitor tasks are never restored on resume.

- [[Automate work with routines - Claude Code Docs|Routines]]: run on Anthropic-managed infrastructure on a schedule, via API call, or on GitHub events
- [[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]: use a

  ```
  schedule
  ```

  trigger in CI
- [[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|Desktop scheduled tasks]]: run locally on your machine

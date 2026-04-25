---
title: Schedule recurring tasks in Claude Code Desktop - Claude Code Docs
source_url: https://code.claude.com/docs/en/desktop-scheduled-tasks
description: Set up scheduled tasks in Claude Code Desktop to run Claude automatically
  on a recurring basis for daily code reviews, dependency audits, or morning briefings.
---

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

- Local tasks: run on your machine. They have direct access to your local files and tools, but the desktop app must be open and your computer awake for them to run.
- Remote tasks: run on Anthropic-managed cloud infrastructure. They keep running even when your computer is off, but work against a fresh clone of your repository rather than your local checkout.

[[Automate work with routines - Claude Code Docs|Routines]]. See

[[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs#How scheduled tasks run|How scheduled tasks run]]for details on missed runs and catch-up behavior for local tasks.

By default, local scheduled tasks run against whatever state your working directory is in, including uncommitted changes. Enable the worktree toggle in the prompt input to give each run its own isolated Git worktree, the same way

[[Use Claude Code Desktop - Claude Code Docs#Work in parallel with sessions|parallel sessions]]work.

## Create a scheduled task

To create a local scheduled task, click Schedule in the sidebar, click New task, and choose New local task. Configure these fields:

FieldDescriptionNameIdentifier for the task. Converted to lowercase kebab-case and used as the folder name on disk. Must be unique across your tasks.DescriptionShort summary shown in the task list.PromptThe instructions sent to Claude when the task runs. Write this the same way you’d write any message in the prompt box. The prompt input also includes controls for model, permission mode, working folder, and worktree.FrequencyHow often the task runs. See

## Frequency options

Pick a preset from the frequency dropdown, or ask Claude for anything the picker doesn’t cover:

- Manual: no schedule, only runs when you click Run now. Useful for saving a prompt you trigger on demand
- Hourly: runs every hour. Each task gets a fixed offset of up to 10 minutes from the top of the hour to stagger API traffic
- Daily: shows a time picker, defaults to 9:00 AM local time
- Weekdays: same as Daily but skips Saturday and Sunday
- Weekly: shows a time picker and a day picker

## How scheduled tasks run

Local scheduled tasks run on your machine. Desktop checks the schedule every minute while the app is open and starts a fresh session when a task is due, independent of any manual sessions you have open. Each task gets a fixed delay of up to 10 minutes after the scheduled time to stagger API traffic. The delay is deterministic: the same task always starts at the same offset. When a task fires, you get a desktop notification and a new session appears under a Scheduled section in the sidebar. Open it to see what Claude did, review changes, or respond to permission prompts. The session works like any other: Claude can edit files, run commands, create commits, and open pull requests. Tasks only run while the desktop app is running and your computer is awake. If your computer sleeps through a scheduled time, the run is skipped. To prevent idle-sleep, enable Keep computer awake in Settings under Desktop app → General. Closing the laptop lid still puts it to sleep. For tasks that need to run even when your computer is off, or that should trigger automatically on an API call or GitHub event, use a

[[Automate work with routines - Claude Code Docs|routine]]instead.

## Missed runs

When the app starts or your computer wakes, Desktop checks whether each task missed any runs in the last seven days. If it did, Desktop starts exactly one catch-up run for the most recently missed time and discards anything older. A daily task that missed six days runs once on wake. Desktop shows a notification when a catch-up run starts. Keep this in mind when writing prompts. A task scheduled for 9am might run at 11pm if your computer was asleep all day. If timing matters, add guardrails to the prompt itself, for example: “Only review today’s commits. If it’s after 5pm, skip the review and just post a summary of what was missed.”

## Permissions for scheduled tasks

Each task has its own permission mode, which you set when creating or editing the task. Allow rules from

```
~/.claude/settings.json
```

also apply to scheduled task sessions. If a task runs in Ask mode and needs to run a tool it doesn’t have permission for, the run stalls until you approve it. The session stays open in the sidebar so you can answer later.
To avoid stalls, click Run now after creating a task, watch for permission prompts, and select “always allow” for each one. Future runs of that task auto-approve the same tools without prompting. You can review and revoke these approvals from the task’s detail page.

## Manage scheduled tasks

Click a task in the Schedule list to open its detail page. From here you can:

- Run now: start the task immediately without waiting for the next scheduled time
- Toggle repeats: pause or resume scheduled runs without deleting the task
- Edit: change the prompt, frequency, folder, or other settings
- Review history: see every past run, including ones that were skipped because your computer was asleep
- Review allowed permissions: see and revoke saved tool approvals for this task from the Always allowed panel
- Delete: remove the task and archive all sessions it created

```
~/.claude/scheduled-tasks/<task-name>/SKILL.md
```

(or under

[[Environment variables - Claude Code Docs|if set). The file uses YAML frontmatter for]]

```
CLAUDE_CONFIG_DIR
```

```
name
```

and

```
description
```

, with the prompt as the body. Changes take effect on the next run. Schedule, folder, model, and enabled state are not in this file: change them through the Edit form or ask Claude.

## Related resources

- [[Automate work with routines - Claude Code Docs|Routines]]: run tasks on Anthropic-managed infrastructure on a schedule, via API call, or in response to GitHub events, even when your computer is off
- [[Run prompts on a schedule - Claude Code Docs|Run prompts on a schedule]]: session-scoped scheduling with

  ```
  /loop
  ```

  in the CLI
- [[Claude Code GitHub Actions - Claude Code Docs|Claude Code GitHub Actions]]: run Claude on a schedule in CI instead of on your machine
- [[Use Claude Code Desktop - Claude Code Docs|Use Claude Code Desktop]]: the full Desktop app guide

---
title: Orchestrate teams of Claude Code sessions - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-teams
description: Coordinate multiple Claude Code instances working together as a team,
  with shared tasks, inter-agent messaging, and centralized management.
---

[[Create custom subagents - Claude Code Docs|subagents]], which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead.

Agent teams require Claude Code v2.1.32 or later. Check your version with

```
claude --version
```

.

- [[Orchestrate teams of Claude Code sessions - Claude Code Docs#When to use agent teams|When to use agent teams]], including best use cases and how they compare with subagents
- [[Orchestrate teams of Claude Code sessions - Claude Code Docs#Start your first agent team|Starting a team]]
- [[Orchestrate teams of Claude Code sessions - Claude Code Docs#Control your agent team|Controlling teammates]], including display modes, task assignment, and delegation
- [[Orchestrate teams of Claude Code sessions - Claude Code Docs#Best practices|Best practices for parallel work]]

## When to use agent teams

Agent teams are most effective for tasks where parallel exploration adds real value. See

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Use case examples|use case examples]]for full scenarios. The strongest use cases are:

- Research and review: multiple teammates can investigate different aspects of a problem simultaneously, then share and challenge each other’s findings
- New modules or features: teammates can each own a separate piece without stepping on each other
- Debugging with competing hypotheses: teammates test different theories in parallel and converge on the answer faster
- Cross-layer coordination: changes that span frontend, backend, and tests, each owned by a different teammate

[[Create custom subagents - Claude Code Docs|subagents]]are more effective.

### Compare with subagents

Both agent teams and

[[Create custom subagents - Claude Code Docs|subagents]]let you parallelize work, but they operate differently. Choose based on whether your workers need to communicate with each other:

SubagentsAgent teamsContextOwn context window; results return to the callerOwn context window; fully independentCommunicationReport results back to the main agent onlyTeammates message each other directlyCoordinationMain agent manages all workShared task list with self-coordinationBest forFocused tasks where only the result mattersComplex work requiring discussion and collaborationToken costLower: results summarized back to main contextHigher: each teammate is a separate Claude instance

## Enable agent teams

Agent teams are disabled by default. Enable them by setting the

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
```

environment variable to

```
1
```

, either in your shell environment or through

[[Claude Code settings - Claude Code Docs|settings.json]]:

settings.json

## Start your first agent team

After enabling agent teams, tell Claude to create an agent team and describe the task and the team structure you want in natural language. Claude creates the team, spawns teammates, and coordinates work based on your prompt. This example works well because the three roles are independent and can explore the problem without waiting on each other:

[[Interactive mode - Claude Code Docs#Task list|shared task list]], spawns teammates for each perspective, has them explore the problem, synthesizes findings, and attempts to

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Clean up the team|clean up the team]]when finished. The lead’s terminal lists all teammates and what they’re working on. Use Shift+Down to cycle through teammates and message them directly. After the last teammate, Shift+Down wraps back to the lead. If you want each teammate in its own split pane, see

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Choose a display mode|Choose a display mode]].

## Control your agent team

Tell the lead what you want in natural language. It handles team coordination, task assignment, and delegation based on your instructions.

### Choose a display mode

Agent teams support two display modes:

- In-process: all teammates run inside your main terminal. Use Shift+Down to cycle through teammates and type to message them directly. Works in any terminal, no extra setup required.
- Split panes: each teammate gets its own pane. You can see everyone’s output at once and click into a pane to interact directly. Requires tmux, or iTerm2.

```
tmux
```

has known limitations on certain operating systems and traditionally works best on macOS. Using

```
tmux -CC
```

in iTerm2 is the suggested entrypoint into

```
tmux
```

.

```
"auto"
```

, which uses split panes if you’re already running inside a tmux session, and in-process otherwise. The

```
"tmux"
```

setting enables split-pane mode and auto-detects whether to use tmux or iTerm2 based on your terminal. To override, set

[[Claude Code settings - Claude Code Docs#Available settings|in]]

```
teammateMode
```

```
~/.claude/settings.json
```

:

[tmux](https://github.com/tmux/tmux/wiki)or iTerm2 with the

[. To install manually:](https://github.com/mkusaka/it2)

```
it2
```

CLI

- tmux: install through your system’s package manager. See the [tmux wiki](https://github.com/tmux/tmux/wiki/Installing)for platform-specific instructions.
- iTerm2: install the , then enable the Python API in iTerm2 → Settings → General → Magic → Enable Python API.

  ```
  it2
  ```

  CLI

### Specify teammates and models

Claude decides the number of teammates to spawn based on your task, or you can specify exactly what you want:

### Require plan approval for teammates

For complex or risky tasks, you can require teammates to plan before implementing. The teammate works in read-only plan mode until the lead approves their approach:

### Talk to teammates directly

Each teammate is a full, independent Claude Code session. You can message any teammate directly to give additional instructions, ask follow-up questions, or redirect their approach.

- In-process mode: use Shift+Down to cycle through teammates, then type to send them a message. Press Enter to view a teammate’s session, then Escape to interrupt their current turn. Press Ctrl+T to toggle the task list.
- Split-pane mode: click into a teammate’s pane to interact with their session directly. Each teammate has a full view of their own terminal.

### Assign and claim tasks

The shared task list coordinates work across the team. The lead creates tasks and teammates work through them. Tasks have three states: pending, in progress, and completed. Tasks can also depend on other tasks: a pending task with unresolved dependencies cannot be claimed until those dependencies are completed. The lead can assign tasks explicitly, or teammates can self-claim:

- Lead assigns: tell the lead which task to give to which teammate
- Self-claim: after finishing a task, a teammate picks up the next unassigned, unblocked task on its own

### Shut down teammates

To gracefully end a teammate’s session:

### Clean up the team

When you’re done, ask the lead to clean up:

### Enforce quality gates with hooks

Use

[[Hooks reference - Claude Code Docs|hooks]]to enforce rules when teammates finish work or tasks are created or completed:

- : runs when a teammate is about to go idle. Exit with code 2 to send feedback and keep the teammate working.

  ```
  TeammateIdle
  ```
- : runs when a task is being created. Exit with code 2 to prevent creation and send feedback.

  ```
  TaskCreated
  ```
- : runs when a task is being marked complete. Exit with code 2 to prevent completion and send feedback.

  ```
  TaskCompleted
  ```

## How agent teams work

This section covers the architecture and mechanics behind agent teams. If you want to start using them, see

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Control your agent team|Control your agent team]]above.

### How Claude starts agent teams

There are two ways agent teams get started:

- You request a team: give Claude a task that benefits from parallel work and explicitly ask for an agent team. Claude creates one based on your instructions.
- Claude proposes a team: if Claude determines your task would benefit from parallel work, it may suggest creating a team. You confirm before it proceeds.

### Architecture

An agent team consists of:

ComponentRoleTeam leadThe main Claude Code session that creates the team, spawns teammates, and coordinates workTeammatesSeparate Claude Code instances that each work on assigned tasksTask listShared list of work items that teammates claim and completeMailboxMessaging system for communication between agents

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Choose a display mode|Choose a display mode]]for display configuration options. Teammate messages arrive at the lead automatically. The system manages task dependencies automatically. When a teammate completes a task that other tasks depend on, blocked tasks unblock without manual intervention. Teams and tasks are stored locally:

- Team config:

  ```
  ~/.claude/teams/{team-name}/config.json
  ```
- Task list:

  ```
  ~/.claude/tasks/{team-name}/
  ```

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Use subagent definitions for teammates|subagent definitions]]instead. The team config contains a

```
members
```

array with each teammate’s name, agent ID, and agent type. Teammates can read this file to discover other team members.
There is no project-level equivalent of the team config. A file like

```
.claude/teams/teams.json
```

in your project directory is not recognized as configuration; Claude treats it as an ordinary file.

### Use subagent definitions for teammates

When spawning a teammate, you can reference a

[[Create custom subagents - Claude Code Docs|subagent]]type from any

[[Create custom subagents - Claude Code Docs#Choose the subagent scope|subagent scope]]: project, user, plugin, or CLI-defined. This lets you define a role once, such as a security-reviewer or test-runner, and reuse it both as a delegated subagent and as an agent team teammate. To use a subagent definition, mention it by name when asking Claude to spawn the teammate:

```
tools
```

allowlist and

```
model
```

, and the definition’s body is appended to the teammate’s system prompt as additional instructions rather than replacing it. Team coordination tools such as

```
SendMessage
```

and the task management tools are always available to a teammate even when

```
tools
```

restricts other tools.

The

```
skills
```

and

```
mcpServers
```

frontmatter fields in a subagent definition are not applied when that definition runs as a teammate. Teammates load skills and MCP servers from your project and user settings, the same as a regular session.

### Permissions

Teammates start with the lead’s permission settings. If the lead runs with

```
--dangerously-skip-permissions
```

, all teammates do too. After spawning, you can change individual teammate modes, but you can’t set per-teammate modes at spawn time.

### Context and communication

Each teammate has its own context window. When spawned, a teammate loads the same project context as a regular session: CLAUDE.md, MCP servers, and skills. It also receives the spawn prompt from the lead. The lead’s conversation history does not carry over. How teammates share information:

- Automatic message delivery: when teammates send messages, they’re delivered automatically to recipients. The lead doesn’t need to poll for updates.
- Idle notifications: when a teammate finishes and stops, they automatically notify the lead.
- Shared task list: all agents can see task status and claim available work.
- Teammate messaging: send a message to one specific teammate by name. To reach everyone, send one message per recipient.

### Token usage

Agent teams use significantly more tokens than a single session. Each teammate has its own context window, and token usage scales with the number of active teammates. For research, review, and new feature work, the extra tokens are usually worthwhile. For routine tasks, a single session is more cost-effective. See

[[Manage costs effectively - Claude Code Docs#Agent team token costs|agent team token costs]]for usage guidance.

## Use case examples

These examples show how agent teams handle tasks where parallel exploration adds value.

### Run a parallel code review

A single reviewer tends to gravitate toward one type of issue at a time. Splitting review criteria into independent domains means security, performance, and test coverage all get thorough attention simultaneously. The prompt assigns each teammate a distinct lens so they don’t overlap:

### Investigate with competing hypotheses

When the root cause is unclear, a single agent tends to find one plausible explanation and stop looking. The prompt fights this by making teammates explicitly adversarial: each one’s job is not only to investigate its own theory but to challenge the others’.

## Best practices

### Give teammates enough context

Teammates load project context automatically, including CLAUDE.md, MCP servers, and skills, but they don’t inherit the lead’s conversation history. See

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Context and communication|Context and communication]]for details. Include task-specific details in the spawn prompt:

### Choose an appropriate team size

There’s no hard limit on the number of teammates, but practical constraints apply:

- Token costs scale linearly: each teammate has its own context window and consumes tokens independently. See [[Manage costs effectively - Claude Code Docs#Agent team token costs|agent team token costs]]for details.
- Coordination overhead increases: more teammates means more communication, task coordination, and potential for conflicts
- Diminishing returns: beyond a certain point, additional teammates don’t speed up work proportionally

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Architecture|tasks]]per teammate keeps everyone productive without excessive context switching. If you have 15 independent tasks, 3 teammates is a good starting point. Scale up only when the work genuinely benefits from having teammates work simultaneously. Three focused teammates often outperform five scattered ones.

### Size tasks appropriately

- Too small: coordination overhead exceeds the benefit
- Too large: teammates work too long without check-ins, increasing risk of wasted effort
- Just right: self-contained units that produce a clear deliverable, such as a function, a test file, or a review

### Wait for teammates to finish

Sometimes the lead starts implementing tasks itself instead of waiting for teammates. If you notice this:

### Start with research and review

If you’re new to agent teams, start with tasks that have clear boundaries and don’t require writing code: reviewing a PR, researching a library, or investigating a bug. These tasks show the value of parallel exploration without the coordination challenges that come with parallel implementation.

### Avoid file conflicts

Two teammates editing the same file leads to overwrites. Break the work so each teammate owns a different set of files.

### Monitor and steer

Check in on teammates’ progress, redirect approaches that aren’t working, and synthesize findings as they come in. Letting a team run unattended for too long increases the risk of wasted effort.

## Troubleshooting

### Teammates not appearing

If teammates aren’t appearing after you ask Claude to create a team:

- In in-process mode, teammates may already be running but not visible. Press Shift+Down to cycle through active teammates.
- Check that the task you gave Claude was complex enough to warrant a team. Claude decides whether to spawn teammates based on the task.
- If you explicitly requested split panes, ensure tmux is installed and available in your PATH:
- For iTerm2, verify the

  ```
  it2
  ```

  CLI is installed and the Python API is enabled in iTerm2 preferences.

### Too many permission prompts

Teammate permission requests bubble up to the lead, which can create friction. Pre-approve common operations in your

[[Configure permissions - Claude Code Docs|permission settings]]before spawning teammates to reduce interruptions.

### Teammates stopping on errors

Teammates may stop after encountering errors instead of recovering. Check their output using Shift+Down in in-process mode or by clicking the pane in split mode, then either:

- Give them additional instructions directly
- Spawn a replacement teammate to continue the work

### Lead shuts down before work is done

The lead may decide the team is finished before all tasks are actually complete. If this happens, tell it to keep going. You can also tell the lead to wait for teammates to finish before proceeding if it starts doing work instead of delegating.

### Orphaned tmux sessions

If a tmux session persists after the team ends, it may not have been fully cleaned up. List sessions and kill the one created by the team:

## Limitations

Agent teams are experimental. Current limitations to be aware of:

- No session resumption with in-process teammates:

  ```
  /resume
  ```

  and

  ```
  /rewind
  ```

  do not restore in-process teammates. After resuming a session, the lead may attempt to message teammates that no longer exist. If this happens, tell the lead to spawn new teammates.
- Task status can lag: teammates sometimes fail to mark tasks as completed, which blocks dependent tasks. If a task appears stuck, check whether the work is actually done and update the task status manually or tell the lead to nudge the teammate.
- Shutdown can be slow: teammates finish their current request or tool call before shutting down, which can take time.
- One team per session: a lead can only manage one team at a time. Clean up the current team before starting a new one.
- No nested teams: teammates cannot spawn their own teams or teammates. Only the lead can manage the team.
- Lead is fixed: the session that creates the team is the lead for its lifetime. You can’t promote a teammate to lead or transfer leadership.
- Permissions set at spawn: all teammates start with the lead’s permission mode. You can change individual teammate modes after spawning, but you can’t set per-teammate modes at spawn time.
- Split panes require tmux or iTerm2: the default in-process mode works in any terminal. Split-pane mode isn’t supported in VS Code’s integrated terminal, Windows Terminal, or Ghostty.

## Next steps

Explore related approaches for parallel work and delegation:

- Lightweight delegation: [[Create custom subagents - Claude Code Docs|subagents]]spawn helper agents for research or verification within your session, better for tasks that don’t need inter-agent coordination
- Manual parallel sessions: [[Common workflows - Claude Code Docs#Run parallel Claude Code sessions with Git worktrees|Git worktrees]]let you run multiple Claude Code sessions yourself without automated team coordination
- Compare approaches: see the [[Extend Claude Code - Claude Code Docs#Compare similar features|subagent vs agent team]]comparison for a side-by-side breakdown

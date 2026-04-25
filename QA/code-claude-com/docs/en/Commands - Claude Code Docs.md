---
title: Commands - Claude Code Docs
source_url: https://code.claude.com/docs/en/commands
description: Complete reference for commands available in Claude Code, including built-in
  commands and bundled skills.
---

```
/
```

to see every command available to you, or type

```
/
```

followed by letters to filter.
The table below lists all the commands included in Claude Code. Entries marked

[[Extend Claude with skills - Claude Code Docs#Bundled skills|Skill]]are bundled skills. They use the same mechanism as skills you write yourself: a prompt handed to Claude, which Claude can also invoke automatically when relevant. Everything else is a built-in command whose behavior is coded into the CLI. To add your own commands, see

[[Extend Claude with skills - Claude Code Docs|skills]]. Not every command appears for every user. Availability depends on your platform, plan, and environment. For example,

```
/desktop
```

only shows on macOS and Windows, and

```
/upgrade
```

only shows on Pro and Max plans.
In the table below,

```
<arg>
```

indicates a required argument and

```
[arg]
```

indicates an optional one.

CommandPurpose

```
/add-dir <path>
```

Add a working directory for file access during the current session. Most

```
.claude/
```

configuration is

```
--continue
```

or

```
--resume
```

```
/agents
```

Manage

```
/autofix-pr [prompt]
```

[[Use Claude Code on the web - Claude Code Docs#Auto-fix pull requests|Claude Code on the web]]session that watches the current branch’s PR and pushes fixes when CI fails or reviewers leave comments. Detects the open PR from your checked-out branch with

```
gh pr view
```

; to watch a different PR, check out its branch first. By default the remote session is told to fix every CI failure and review comment; pass a prompt to give it different instructions, for example

```
/autofix-pr only fix lint and type errors
```

. Requires the

```
gh
```

CLI and access to [[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]

```
/batch <instruction>
```

[[Extend Claude with skills - Claude Code Docs#Bundled skills|Skill]]. Orchestrate large-scale changes across a codebase in parallel. Researches the codebase, decomposes the work into 5 to 30 independent units, and presents a plan. Once approved, spawns one background agent per unit in an isolated[[Common workflows - Claude Code Docs#Run parallel Claude Code sessions with Git worktrees|git worktree]]. Each agent implements its unit, runs tests, and opens a pull request. Requires a git repository. Example:

```
/batch migrate src/ from Solid to React
```

```
/branch [name]
```

```
/resume
```

. Alias:

```
/fork
```

. When [[Environment variables - Claude Code Docs|is set,]]

```
CLAUDE_CODE_FORK_SUBAGENT
```

```
/fork
```

instead spawns a [[Create custom subagents - Claude Code Docs#Fork the current conversation|forked subagent]]and is no longer an alias for this command

```
/btw <question>
```

[[Interactive mode - Claude Code Docs|side question]]without adding to the conversation

```
/chrome
```

[[Use Claude Code with Chrome (beta) - Claude Code Docs|Claude in Chrome]]settings

```
/claude-api
```

[[Extend Claude with skills - Claude Code Docs#Bundled skills|Skill]]. Load Claude API reference material for your project’s language (Python, TypeScript, Java, Go, Ruby, C#, PHP, or cURL) and Managed Agents reference. Covers tool use, streaming, batches, structured outputs, and common pitfalls. Also activates automatically when your code imports

```
anthropic
```

or

```
@anthropic-ai/sdk
```

```
/clear
```

```
/resume
```

. To free up context while continuing the same conversation, use

```
/compact
```

instead. Aliases:

```
/reset
```

,

```
/new
```

```
/color [color|default]
```

```
red
```

,

```
blue
```

,

```
green
```

,

```
yellow
```

,

```
purple
```

,

```
orange
```

,

```
pink
```

,

```
cyan
```

. Use

```
default
```

to reset. When [[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]is connected, the color syncs to claude.ai/code

```
/compact [instructions]
```

[[Explore the context window - Claude Code Docs#What survives compaction|how compaction handles rules, skills, and memory files]]

```
/config
```

[[Claude Code settings - Claude Code Docs|Settings]]interface to adjust theme, model,[[Output styles - Claude Code Docs|output style]], and other preferences. Alias:

```
/settings
```

```
/context
```

```
/copy [N]
```

```
N
```

to copy the Nth-latest response:

```
/copy 2
```

copies the second-to-last. When code blocks are present, shows an interactive picker to select individual blocks or the full response. Press

```
w
```

in the picker to write the selection to a file instead of the clipboard, which is useful over SSH

```
/cost
```

```
/usage
```

```
/debug [description]
```

[[Extend Claude with skills - Claude Code Docs#Bundled skills|Skill]]. Enable debug logging for the current session and troubleshoot issues by reading the session debug log. Debug logging is off by default unless you started with

```
claude --debug
```

, so running

```
/debug
```

mid-session starts capturing logs from that point forward. Optionally describe the issue to focus the analysis

```
/desktop
```

```
/app
```

```
/diff
```

```
/doctor
```

```
f
```

to have Claude fix any reported issues

```
/effort [level|auto]
```

[[Model configuration - Claude Code Docs#Adjust effort level|effort level]]. Accepts

```
low
```

,

```
medium
```

,

```
high
```

,

```
xhigh
```

, or

```
max
```

; available levels depend on the model and

```
max
```

is session-only.

```
auto
```

resets to the model default. Without an argument, opens an interactive slider; use left and right arrows to pick a level and

```
Enter
```

to apply. Takes effect immediately without waiting for the current response to finish

```
/exit
```

```
/quit
```

```
/export [filename]
```

```
/extra-usage
```

```
/fast [on|off]
```

[[Speed up responses with fast mode - Claude Code Docs|fast mode]]on or off

```
/feedback [report]
```

```
/bug
```

```
/fewer-permission-prompts
```

[[Extend Claude with skills - Claude Code Docs#Bundled skills|Skill]]. Scan your transcripts for common read-only Bash and MCP tool calls, then add a prioritized allowlist to project

```
.claude/settings.json
```

to reduce permission prompts

```
/focus
```

[[Fullscreen rendering - Claude Code Docs|fullscreen rendering]]

```
/heapdump
```

```
~/Desktop
```

for diagnosing high memory usage. See [[Troubleshooting - Claude Code Docs#High CPU or memory usage|troubleshooting]]

```
/help
```

```
/hooks
```

[[Hooks reference - Claude Code Docs|hook]]configurations for tool events

```
/ide
```

```
/init
```

```
CLAUDE.md
```

guide. Set

```
CLAUDE_CODE_NEW_INIT=1
```

for an interactive flow that also walks through skills, hooks, and personal memory files

```
/insights
```

```
/install-github-app
```

[[Claude Code GitHub Actions - Claude Code Docs|Claude GitHub Actions]]app for a repository. Walks you through selecting a repo and configuring the integration

```
/install-slack-app
```

```
/keybindings
```

```
/login
```

```
/logout
```

```
/loop [interval] [prompt]
```

[[Extend Claude with skills - Claude Code Docs#Bundled skills|Skill]]. Run a prompt repeatedly while the session stays open. Omit the interval and Claude self-paces between iterations. Omit the prompt and Claude runs an autonomous maintenance check, or the prompt in

```
.claude/loop.md
```

if present. Example:

```
/loop 5m check if the deploy finished
```

. See [[Run prompts on a schedule - Claude Code Docs|Run prompts on a schedule]]. Alias:

```
/proactive
```

```
/mcp
```

```
/memory
```

```
CLAUDE.md
```

memory files, enable or disable [[How Claude remembers your project - Claude Code Docs#Auto memory|auto-memory]], and view auto-memory entries

```
/mobile
```

```
/ios
```

,

```
/android
```

```
/model [model]
```

[[Model configuration - Claude Code Docs#Adjust effort level|adjust effort level]]. With no argument, opens a picker that asks for confirmation when the conversation has prior output, since the next response re-reads the full history without cached context. Once confirmed, the change applies without waiting for the current response to finish

```
/passes
```

```
/permissions
```

[[Configure auto mode - Claude Code Docs#Review denials|recent auto mode denials]]. Alias:

```
/allowed-tools
```

```
/plan [description]
```

```
/plan fix the auth bug
```

```
/plugin
```

[[Create plugins - Claude Code Docs|plugins]]

```
/powerup
```

```
/pr-comments [PR]
```

```
gh
```

CLI

```
/privacy-settings
```

```
/recap
```

[[Interactive mode - Claude Code Docs#Session recap|Session recap]]for the automatic recap that appears after you’ve been away

```
/release-notes
```

```
/reload-plugins
```

[[Create plugins - Claude Code Docs|plugins]]to apply pending changes without restarting. Reports counts for each reloaded component and flags any load errors

```
/remote-control
```

[[Continue local sessions from any device with Remote Control - Claude Code Docs|remote control]]from claude.ai. Alias:

```
/rc
```

```
/remote-env
```

[[Use Claude Code on the web - Claude Code Docs#Configure your environment|web sessions started with]]

```
--remote
```

```
/rename [name]
```

```
/resume [session]
```

```
/continue
```

```
/review [PR]
```

```
/ultrareview
```

```
/rewind
```

[[Checkpointing - Claude Code Docs|checkpointing]]. Aliases:

```
/checkpoint
```

,

```
/undo
```

```
/sandbox
```

[[Sandboxing - Claude Code Docs|sandbox mode]]. Available on supported platforms only

```
/schedule [description]
```

[[Automate work with routines - Claude Code Docs|routines]]. Claude walks you through the setup conversationally. Alias:

```
/routines
```

```
/security-review
```

```
/setup-bedrock
```

[[Claude Code on Amazon Bedrock - Claude Code Docs|Amazon Bedrock]]authentication, region, and model pins through an interactive wizard. Only visible when

```
CLAUDE_CODE_USE_BEDROCK=1
```

is set. First-time Bedrock users can also access this wizard from the login screen

```
/setup-vertex
```

[[Claude Code on Google Vertex AI - Claude Code Docs|Google Vertex AI]]authentication, project, region, and model pins through an interactive wizard. Only visible when

```
CLAUDE_CODE_USE_VERTEX=1
```

is set. First-time Vertex AI users can also access this wizard from the login screen

```
/simplify [focus]
```

[[Extend Claude with skills - Claude Code Docs#Bundled skills|Skill]]. Review your recently changed files for code reuse, quality, and efficiency issues, then fix them. Spawns three review agents in parallel, aggregates their findings, and applies fixes. Pass text to focus on specific concerns:

```
/simplify focus on memory efficiency
```

```
/skills
```

[[Extend Claude with skills - Claude Code Docs|skills]]. Press

```
t
```

to sort by token count

```
/stats
```

```
/usage
```

. Opens on the Stats tab

```
/status
```

```
/statusline
```

[[Customize your status line - Claude Code Docs|status line]]. Describe what you want, or run without arguments to auto-configure from your shell prompt

```
/stickers
```

```
/tasks
```

```
/bashes
```

```
/team-onboarding
```

```
/teleport
```

[[Use Claude Code on the web - Claude Code Docs#From web to terminal|Claude Code on the web]]session into this terminal: opens a picker, then fetches the branch and conversation. Also available as

```
/tp
```

. Requires a claude.ai subscription

```
/terminal-setup
```

```
/theme
```

```
auto
```

option that matches your terminal’s light or dark background, light and dark variants, colorblind-accessible (daltonized) themes, ANSI themes that use your terminal’s color palette, and any [[Configure your terminal for Claude Code - Claude Code Docs#Create a custom theme|custom themes]]from

```
~/.claude/themes/
```

or plugins. Select New custom theme… to create one

```
/tui [default|fullscreen]
```

```
fullscreen
```

enables the [[Fullscreen rendering - Claude Code Docs|flicker-free alt-screen renderer]]. With no argument, prints the active renderer

```
/ultraplan <prompt>
```

[[Plan in the cloud with ultraplan - Claude Code Docs|ultraplan]]session, review it in your browser, then execute remotely or send it back to your terminal

```
/ultrareview [PR]
```

[[Find bugs with ultrareview - Claude Code Docs|ultrareview]]. Includes 3 free runs on Pro and Max through May 5, 2026, then requires[extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)

```
/upgrade
```

```
/usage
```

[[Manage costs effectively - Claude Code Docs|cost tracking guide]]for subscription-specific details.

```
/cost
```

and

```
/stats
```

are aliases

```
/vim
```

```
/config
```

→ Editor mode

```
/voice [hold|tap|off]
```

[[Voice dictation - Claude Code Docs|voice dictation]], or enable it in a specific mode. Requires a Claude.ai account

```
/web-setup
```

[[Get started with Claude Code on the web - Claude Code Docs#Connect from your terminal|Claude Code on the web]]using your local

```
gh
```

CLI credentials.

```
/schedule
```

prompts for this automatically if GitHub isn’t connected

## MCP prompts

MCP servers can expose prompts that appear as commands. These use the format

```
/mcp__<server>__<prompt>
```

and are dynamically discovered from connected servers. See

[[Connect Claude Code to tools via MCP - Claude Code Docs#Use MCP prompts as commands|MCP prompts]]for details.

## See also

- [[Extend Claude with skills - Claude Code Docs|Skills]]: create your own commands
- [[Interactive mode - Claude Code Docs|Interactive mode]]: keyboard shortcuts, Vim mode, and command history
- [[CLI reference - Claude Code Docs|CLI reference]]: launch-time flags

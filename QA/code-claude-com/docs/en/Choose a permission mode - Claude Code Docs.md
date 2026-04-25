---
title: Choose a permission mode - Claude Code Docs
source_url: https://code.claude.com/docs/en/permission-modes
description: Control whether Claude asks before editing files or running commands.
  Cycle modes with Shift+Tab in the CLI or use the mode selector in VS Code, Desktop,
  and cl
---

## Available modes

Each mode makes a different tradeoff between convenience and oversight. The table below shows what Claude can do without a permission prompt in each mode.

ModeWhat runs without askingBest for

```
default
```

Reads onlyGetting started, sensitive work

```
acceptEdits
```

```
mkdir
```

,

```
touch
```

,

```
mv
```

,

```
cp
```

, etc.)

```
plan
```

```
auto
```

```
dontAsk
```

```
bypassPermissions
```

[[Choose a permission mode - Claude Code Docs#Protected paths|protected paths]]are never auto-approved, guarding repository state and Claude’s own configuration against accidental corruption. Modes set the baseline. Layer

[[Configure permissions - Claude Code Docs#Manage permissions|permission rules]]on top to pre-approve or block specific tools in any mode except

```
bypassPermissions
```

, which skips the permission layer entirely.

## Switch permission modes

You can switch modes mid-session, at startup, or as a persistent default. The mode is set through these controls, not by asking Claude in chat. Select your interface below to see how to change it.

- CLI
- VS Code
- JetBrains
- Desktop
- Web and mobile

During a session: press As a default: set The same

```
Shift+Tab
```

to cycle

```
default
```

→

```
acceptEdits
```

→

```
plan
```

. The current mode appears in the status bar. Not every mode is in the default cycle:

- ```
  auto
  ```

  : appears when your account meets the[[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|auto mode requirements]]; cycling to auto shows an opt-in prompt until you accept it, or select No, don’t ask again to remove auto from the cycle
- ```
  bypassPermissions
  ```

  : appears after you start with

  ```
  --permission-mode bypassPermissions
  ```

  ,

  ```
  --dangerously-skip-permissions
  ```

  , or

  ```
  --allow-dangerously-skip-permissions
  ```

  ; the

  ```
  --allow-
  ```

  variant adds the mode to the cycle without activating it
- ```
  dontAsk
  ```

  : never appears in the cycle; set it with

  ```
  --permission-mode dontAsk
  ```

```
plan
```

, with

```
bypassPermissions
```

first and

```
auto
```

last. If you have both enabled, you will cycle through

```
bypassPermissions
```

on the way to

```
auto
```

.At startup: pass the mode as a flag.

```
defaultMode
```

in [[Claude Code settings - Claude Code Docs#Settings files|settings]].

```
--permission-mode
```

flag works with

```
-p
```

for [[Run Claude Code programmatically - Claude Code Docs|non-interactive runs]].

## Auto-approve file edits with acceptEdits mode

```
acceptEdits
```

mode lets Claude create and edit files in your working directory without prompting. The status bar shows

```
⏵⏵ accept edits on
```

while this mode is active.
In addition to file edits,

```
acceptEdits
```

mode auto-approves common filesystem Bash commands:

```
mkdir
```

,

```
touch
```

,

```
rm
```

,

```
rmdir
```

,

```
mv
```

,

```
cp
```

, and

```
sed
```

. These commands are also auto-approved when prefixed with safe environment variables such as

```
LANG=C
```

or

```
NO_COLOR=1
```

, or process wrappers such as

```
timeout
```

,

```
nice
```

, or

```
nohup
```

. Like file edits, auto-approval applies only to paths inside your working directory or

```
additionalDirectories
```

. Paths outside that scope, writes to

[[Choose a permission mode - Claude Code Docs#Protected paths|protected paths]], and all other Bash commands still prompt. Use

```
acceptEdits
```

when you want to review changes in your editor or via

```
git diff
```

after the fact rather than approving each edit inline. Press

```
Shift+Tab
```

once from default mode to enter it, or start with it directly:

## Analyze before you edit with plan mode

Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source. Permission prompts still apply the same as default mode. Enter plan mode by pressing

```
Shift+Tab
```

or prefixing a single prompt with

```
/plan
```

. You can also start in plan mode from the CLI:

```
Shift+Tab
```

again to leave plan mode without approving a plan.
When the plan is ready, Claude presents it and asks how to proceed. From that prompt you can:

- Approve and start in auto mode
- Approve and accept edits
- Approve and review each edit manually
- Keep planning with feedback
- Refine with [[Plan in the cloud with ultraplan - Claude Code Docs|Ultraplan]]for browser-based review

## Eliminate prompts with auto mode

Auto mode requires Claude Code v2.1.83 or later.

- Plan: Max, Team, Enterprise, or API. Not available on Pro.
- Admin: on Team and Enterprise, an admin must enable it in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code)before users can turn it on. Admins can also lock it off by setting

  ```
  permissions.disableAutoMode
  ```

  to

  ```
  "disable"
  ```

  in[[Configure permissions - Claude Code Docs#Managed settings|managed settings]].
- Model: Claude Sonnet 4.6, Opus 4.6, or Opus 4.7 on Team, Enterprise, and API plans; Claude Opus 4.7 only on Max plans. Other models, including Haiku and claude-3 models, are not supported.
- Provider: Anthropic API only. Not available on Bedrock, Vertex, or Foundry.

[[Error reference - Claude Code Docs#Auto mode cannot determine the safety of an action|error reference]].

### What the classifier blocks by default

The classifier trusts your working directory and your repo’s configured remotes. Everything else is treated as external until you

[[Configure auto mode - Claude Code Docs|configure trusted infrastructure]]. Blocked by default:

- Downloading and executing code, like

  ```
  curl | bash
  ```
- Sending sensitive data to external endpoints
- Production deploys and migrations
- Mass deletion on cloud storage
- Granting IAM or repo permissions
- Modifying shared infrastructure
- Irreversibly destroying files that existed before the session
- Force push, or pushing directly to

  ```
  main
  ```

- Local file operations in your working directory
- Installing dependencies declared in your lock files or manifests
- Reading

  ```
  .env
  ```

  and sending credentials to their matching API
- Read-only HTTP requests
- Pushing to the branch you started on or one Claude created

```
claude auto-mode defaults
```

to see the full rule lists. If routine actions get blocked, an administrator can add trusted repos, buckets, and services via the

```
autoMode.environment
```

setting: see

[[Configure auto mode - Claude Code Docs|Configure auto mode]].

### Boundaries you state in conversation

The classifier treats boundaries you state in the conversation as a block signal. If you tell Claude “don’t push” or “wait until I review before deploying”, the classifier blocks matching actions even when the default rules would allow them. A boundary stays in force until you lift it in a later message. Claude’s own judgment that a condition was met does not lift it. Boundaries are not stored as rules. The classifier re-reads them from the transcript on each check, so a boundary can be lost if

[[Manage costs effectively - Claude Code Docs#Reduce token usage|context compaction]]removes the message that stated it. For a hard guarantee, add a

[[Configure permissions - Claude Code Docs#Permission rule syntax|deny rule]]instead.

### When auto mode falls back

Each denied action shows a notification and appears in

```
/permissions
```

under the Recently denied tab, where you can press

```
r
```

to retry it with a manual approval.
If the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses and Claude Code resumes prompting. Approving the prompted action resumes auto mode. These thresholds are not configurable. Any allowed action resets the consecutive counter, while the total counter persists for the session and resets only when its own limit triggers a fallback.
In

[[Run Claude Code programmatically - Claude Code Docs|non-interactive mode]]with the

```
-p
```

flag, repeated blocks abort the session since there is no user to prompt.
Repeated blocks usually mean the classifier is missing context about your infrastructure. Use

```
/feedback
```

to report false positives, or have an administrator

[[Configure auto mode - Claude Code Docs|configure trusted infrastructure]].

###

How the classifier evaluates actions

How the classifier evaluates actions

Each action goes through a fixed decision order. The first matching step wins:

- Actions matching your [[Configure permissions - Claude Code Docs#Manage permissions|allow or deny rules]]resolve immediately
- Read-only actions and file edits in your working directory are auto-approved, except writes to [[Choose a permission mode - Claude Code Docs#Protected paths|protected paths]]
- Everything else goes to the classifier
- If the classifier blocks, Claude receives the reason and tries an alternative

- Blanket

  ```
  Bash(*)
  ```

  or

  ```
  PowerShell(*)
  ```
- Wildcarded interpreters like

  ```
  Bash(python*)
  ```
- Package-manager run commands
- ```
  Agent
  ```

  allow rules

```
Bash(npm test)
```

carry over. Dropped rules are restored when you leave auto mode.The classifier sees user messages, tool calls, and your CLAUDE.md content. Tool results are stripped, so hostile content in a file or web page cannot manipulate it directly. A separate server-side probe scans incoming tool results and flags suspicious content before Claude reads it. For more on how these layers work together, see the [auto mode announcement](https://claude.com/blog/auto-mode)and the[engineering deep dive](https://www.anthropic.com/engineering/claude-code-auto-mode).

###

How auto mode handles subagents

How auto mode handles subagents

The classifier checks

[[Create custom subagents - Claude Code Docs|subagent]]work at three points:

- Before a subagent starts, the delegated task description is evaluated, so a dangerous-looking task is blocked at spawn time.
- While the subagent runs, each of its actions goes through the classifier with the same rules as the parent session, and any

  ```
  permissionMode
  ```

  in the subagent’s frontmatter is ignored.
- When the subagent finishes, the classifier reviews its full action history; if that return check flags a concern, a security warning is prepended to the subagent’s results.

###

Cost and latency

Cost and latency

The classifier runs on a server-configured model that is independent of your

```
/model
```

selection, so switching models does not change classifier availability. Classifier calls count toward your token usage. Each check sends a portion of the transcript plus the pending action, adding a round-trip before execution. Reads and working-directory edits outside protected paths skip the classifier, so the overhead comes mainly from shell commands and network operations.

## Allow only pre-approved tools with dontAsk mode

```
dontAsk
```

mode auto-denies every tool call that would otherwise prompt. Only actions matching your

```
permissions.allow
```

rules and

[[Configure permissions - Claude Code Docs#Read-only commands|read-only Bash commands]]can execute; explicit

```
ask
```

rules are denied rather than prompting. This makes the mode fully non-interactive for CI pipelines or restricted environments where you pre-define exactly what Claude may do.
Set it at startup with the flag:

## Skip all checks with bypassPermissions mode

```
bypassPermissions
```

mode disables permission prompts and safety checks so tool calls execute immediately. Writes to

[[Choose a permission mode - Claude Code Docs#Protected paths|protected paths]]are the only actions that still prompt. Only use this mode in isolated environments like containers, VMs, or devcontainers without internet access, where Claude Code cannot damage your host system. You cannot enter

```
bypassPermissions
```

from a session that was started without one of the enabling flags; restart with one to enable it:

```
--dangerously-skip-permissions
```

flag is equivalent.

## Protected paths

Writes to a small set of paths are never auto-approved, in every mode. This prevents accidental corruption of repository state and Claude’s own configuration. In

```
default
```

,

```
acceptEdits
```

,

```
plan
```

, and

```
bypassPermissions
```

these writes prompt; in

```
auto
```

they route to the classifier; in

```
dontAsk
```

they are denied.
Protected directories:

- ```
  .git
  ```
- ```
  .vscode
  ```
- ```
  .idea
  ```
- ```
  .husky
  ```
- ```
  .claude
  ```

  , except for

  ```
  .claude/commands
  ```

  ,

  ```
  .claude/agents
  ```

  ,

  ```
  .claude/skills
  ```

  , and

  ```
  .claude/worktrees
  ```

  where Claude routinely creates content

- ```
  .gitconfig
  ```

  ,

  ```
  .gitmodules
  ```
- ```
  .bashrc
  ```

  ,

  ```
  .bash_profile
  ```

  ,

  ```
  .zshrc
  ```

  ,

  ```
  .zprofile
  ```

  ,

  ```
  .profile
  ```
- ```
  .ripgreprc
  ```
- ```
  .mcp.json
  ```

  ,

  ```
  .claude.json
  ```

## See also

- [[Configure permissions - Claude Code Docs|Permissions]]: allow, ask, and deny rules; managed policies
- [[Configure auto mode - Claude Code Docs|Configure auto mode]]: tell the classifier which infrastructure your organization trusts
- [[Hooks reference - Claude Code Docs|Hooks]]: custom permission logic via

  ```
  PreToolUse
  ```

  and

  ```
  PermissionRequest
  ```

  hooks
- [[Plan in the cloud with ultraplan - Claude Code Docs|Ultraplan]]: run plan mode in a Claude Code on the web session with browser-based review
- [[Security - Claude Code Docs|Security]]: safeguards and best practices
- [[Sandboxing - Claude Code Docs|Sandboxing]]: filesystem and network isolation for Bash commands
- [[Run Claude Code programmatically - Claude Code Docs|Non-interactive mode]]: run Claude Code with the

  ```
  -p
  ```

  flag

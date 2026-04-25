---
title: Automate workflows with hooks - Claude Code Docs
source_url: https://code.claude.com/docs/en/hooks-guide
description: Run shell commands automatically when Claude Code edits files, finishes
  tasks, or needs input. Format code, send notifications, validate commands, and enforce
  p
---

[[Automate workflows with hooks - Claude Code Docs#Prompt-based hooks|prompt-based hooks]]or

[[Automate workflows with hooks - Claude Code Docs#Agent-based hooks|agent-based hooks]]that use a Claude model to evaluate conditions. For other ways to extend Claude Code, see

[[Extend Claude with skills - Claude Code Docs|skills]]for giving Claude additional instructions and executable commands,

[[Create custom subagents - Claude Code Docs|subagents]]for running tasks in isolated contexts, and

[[Create plugins - Claude Code Docs|plugins]]for packaging extensions to share across projects.

## Set up your first hook

To create a hook, add a

```
hooks
```

block to a

[[Automate workflows with hooks - Claude Code Docs#Configure hook location|settings file]]. This walkthrough creates a desktop notification hook, so you get alerted whenever Claude is waiting for your input instead of watching the terminal.

Add the hook to your settings

Open If your settings file already has a You can also ask Claude to write the hook for you by describing what you want in the CLI.

```
~/.claude/settings.json
```

and add a

```
Notification
```

hook. The example below uses

```
osascript
```

for macOS; see [[Automate workflows with hooks - Claude Code Docs#Get notified when Claude needs input|Get notified when Claude needs input]]for Linux and Windows commands.

```
hooks
```

key, add

```
Notification
```

as a sibling of the existing event keys rather than replacing the whole object. Each event name is a key inside the single

```
hooks
```

object:

Verify the configuration

Type

```
/hooks
```

to open the hooks browser. You’ll see a list of all available hook events, with a count next to each event that has hooks configured. Select

```
Notification
```

to confirm your new hook appears in the list. Selecting the hook shows its details: the event, matcher, type, source file, and command.

## What you can automate

Hooks let you run code at key points in Claude Code’s lifecycle: format files after edits, block commands before they execute, send notifications when Claude needs input, inject context at session start, and more. For the full list of hook events, see the

[[Hooks reference - Claude Code Docs#Hook lifecycle|Hooks reference]]. Each example includes a ready-to-use configuration block that you add to a

[[Automate workflows with hooks - Claude Code Docs#Configure hook location|settings file]]. The most common patterns:

- [[Automate workflows with hooks - Claude Code Docs#Get notified when Claude needs input|Get notified when Claude needs input]]
- [[Automate workflows with hooks - Claude Code Docs#Auto-format code after edits|Auto-format code after edits]]
- [[Automate workflows with hooks - Claude Code Docs#Block edits to protected files|Block edits to protected files]]
- [[Automate workflows with hooks - Claude Code Docs#Re-inject context after compaction|Re-inject context after compaction]]
- [[Automate workflows with hooks - Claude Code Docs#Audit configuration changes|Audit configuration changes]]
- [[Automate workflows with hooks - Claude Code Docs#Reload environment when directory or files change|Reload environment when directory or files change]]
- [[Automate workflows with hooks - Claude Code Docs#Auto-approve specific permission prompts|Auto-approve specific permission prompts]]

### Get notified when Claude needs input

Get a desktop notification whenever Claude finishes working and needs your input, so you can switch to other tasks without checking the terminal. This hook uses the

```
Notification
```

event, which fires when Claude is waiting for input or permission. Each tab below uses the platform’s native notification command. Add this to

```
~/.claude/settings.json
```

:

- macOS
- Linux
- Windows (PowerShell)

###

If no notification appears

If no notification appears

```
osascript
```

routes notifications through the built-in Script Editor app. If Script Editor doesn’t have notification permission, the command fails silently, and macOS won’t prompt you to grant it. Run this in Terminal once to make Script Editor appear in your notification settings:

### Auto-format code after edits

Automatically run

[Prettier](https://prettier.io/)on every file Claude edits, so formatting stays consistent without manual intervention. This hook uses the

```
PostToolUse
```

event with an

```
Edit|Write
```

matcher, so it runs only after file-editing tools. The command extracts the edited file path with

[and passes it to Prettier. Add this to](https://jqlang.github.io/jq/)

```
jq
```

```
.claude/settings.json
```

in your project root:

The Bash examples on this page use

```
jq
```

for JSON parsing. Install it with

```
brew install jq
```

(macOS),

```
apt-get install jq
```

(Debian/Ubuntu), or see [.](https://jqlang.github.io/jq/download/)

```
jq
```

downloads

### Block edits to protected files

Prevent Claude from modifying sensitive files like

```
.env
```

,

```
package-lock.json
```

, or anything in

```
.git/
```

. Claude receives feedback explaining why the edit was blocked, so it can adjust its approach.
This example uses a separate script file that the hook calls. The script checks the target file path against a list of protected patterns and exits with code 2 to block the edit.

Make the script executable (macOS/Linux)

Hook scripts must be executable for Claude Code to run them:

### Re-inject context after compaction

When Claude’s context window fills up, compaction summarizes the conversation to free space. This can lose important details. Use a

```
SessionStart
```

hook with a

```
compact
```

matcher to re-inject critical context after every compaction.
Any text your command writes to stdout is added to Claude’s context. This example reminds Claude of project conventions and recent work. Add this to

```
.claude/settings.json
```

in your project root:

```
echo
```

with any command that produces dynamic output, like

```
git log --oneline -5
```

to show recent commits. For injecting context on every session start, consider using

[[How Claude remembers your project - Claude Code Docs|CLAUDE.md]]instead. For environment variables, see

[[Hooks reference - Claude Code Docs#Persist environment variables|in the reference.]]

```
CLAUDE_ENV_FILE
```

### Audit configuration changes

Track when settings or skills files change during a session. The

```
ConfigChange
```

event fires when an external process or editor modifies a configuration file, so you can log changes for compliance or block unauthorized modifications.
This example appends each change to an audit log. Add this to

```
~/.claude/settings.json
```

:

```
user_settings
```

,

```
project_settings
```

,

```
local_settings
```

,

```
policy_settings
```

, or

```
skills
```

. To block a change from taking effect, exit with code 2 or return

```
{"decision": "block"}
```

. See the

[[Hooks reference - Claude Code Docs#ConfigChange|ConfigChange reference]]for the full input schema.

### Reload environment when directory or files change

Some projects set different environment variables depending on which directory you are in. Tools like

[direnv](https://direnv.net/)do this automatically in your shell, but Claude’s Bash tool does not pick up those changes on its own. Pairing a

```
SessionStart
```

hook with a

```
CwdChanged
```

hook fixes this.

```
SessionStart
```

loads the variables for the directory you launch in, and

```
CwdChanged
```

reloads them each time Claude changes directory. Both write to

```
CLAUDE_ENV_FILE
```

, which Claude Code runs as a script preamble before each Bash command. Add this to

```
~/.claude/settings.json
```

:

```
direnv allow
```

once in each directory that has an

```
.envrc
```

so direnv is permitted to load it. If you use devbox or nix instead of direnv, the same pattern works with

```
devbox shellenv
```

or

```
devbox global shellenv
```

in place of

```
direnv export bash
```

.
To react to specific files instead of every directory change, use

```
FileChanged
```

with a

```
matcher
```

listing the filenames to watch, separated by

```
|
```

. To build the watch list, this value is split into literal filenames rather than evaluated as a regex. See

[[Hooks reference - Claude Code Docs#FileChanged|FileChanged]]for how the same value also filters which hook groups run when a file changes. This example watches

```
.envrc
```

and

```
.env
```

in the working directory:

[[Hooks reference - Claude Code Docs#CwdChanged|CwdChanged]]and

[[Hooks reference - Claude Code Docs#FileChanged|FileChanged]]reference entries for input schemas,

```
watchPaths
```

output, and

```
CLAUDE_ENV_FILE
```

details.

### Auto-approve specific permission prompts

Skip the approval dialog for tool calls you always allow. This example auto-approves

```
ExitPlanMode
```

, the tool Claude calls when it finishes presenting a plan and asks to proceed, so you aren’t prompted every time a plan is ready.
Unlike the exit-code examples above, auto-approval requires your hook to write a JSON decision to stdout. A

```
PermissionRequest
```

hook fires when Claude Code is about to show a permission dialog, and returning

```
"behavior": "allow"
```

answers it on your behalf.
The matcher scopes the hook to

```
ExitPlanMode
```

only, so no other prompts are affected. Add this to

```
~/.claude/settings.json
```

:

```
updatedPermissions
```

array with a

```
setMode
```

entry. The

```
mode
```

value is any permission mode like

```
default
```

,

```
acceptEdits
```

, or

```
bypassPermissions
```

, and

```
destination: "session"
```

applies it for the current session only.

```
bypassPermissions
```

only applies if the session was launched with bypass mode already available:

```
--dangerously-skip-permissions
```

,

```
--permission-mode bypassPermissions
```

,

```
--allow-dangerously-skip-permissions
```

, or

```
permissions.defaultMode: "bypassPermissions"
```

in settings, and not disabled by

[[Configure permissions - Claude Code Docs#Managed settings|. It is never persisted as]]

```
permissions.disableBypassPermissionsMode
```

```
defaultMode
```

.

```
acceptEdits
```

, your hook writes this JSON to stdout:

```
.*
```

or leaving the matcher empty would auto-approve every permission prompt, including file writes and shell commands. See the

[[Hooks reference - Claude Code Docs#PermissionRequest decision control|PermissionRequest reference]]for the full set of decision fields.

## How hooks work

Hook events fire at specific lifecycle points in Claude Code. When an event fires, all matching hooks run in parallel, and identical hook commands are automatically deduplicated. The table below shows each event and when it triggers:

EventWhen it fires

```
SessionStart
```

When a session begins or resumes

```
UserPromptSubmit
```

When you submit a prompt, before Claude processes it

```
UserPromptExpansion
```

When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion

```
PreToolUse
```

Before a tool call executes. Can block it

```
PermissionRequest
```

When a permission dialog appears

```
PermissionDenied
```

When a tool call is denied by the auto mode classifier. Return

```
{retry: true}
```

to tell the model it may retry the denied tool call

```
PostToolUse
```

After a tool call succeeds

```
PostToolUseFailure
```

After a tool call fails

```
PostToolBatch
```

After a full batch of parallel tool calls resolves, before the next model call

```
Notification
```

When Claude Code sends a notification

```
SubagentStart
```

When a subagent is spawned

```
SubagentStop
```

When a subagent finishes

```
TaskCreated
```

When a task is being created via

```
TaskCreate
```

```
TaskCompleted
```

When a task is being marked as completed

```
Stop
```

When Claude finishes responding

```
StopFailure
```

When the turn ends due to an API error. Output and exit code are ignored

```
TeammateIdle
```

When an

```
InstructionsLoaded
```

```
.claude/rules/*.md
```

file is loaded into context. Fires at session start and when files are lazily loaded during a session

```
ConfigChange
```

```
CwdChanged
```

```
cd
```

command. Useful for reactive environment management with tools like direnv

```
FileChanged
```

```
matcher
```

field specifies which filenames to watch

```
WorktreeCreate
```

```
--worktree
```

or

```
isolation: "worktree"
```

. Replaces default git behavior

```
WorktreeRemove
```

```
PreCompact
```

```
PostCompact
```

```
Elicitation
```

```
ElicitationResult
```

```
SessionEnd
```

```
PreToolUse
```

hook returning

```
deny
```

cancels the tool call no matter what the others return. One hook returning

```
ask
```

forces the permission prompt even if the rest return

```
allow
```

. Text from

```
additionalContext
```

is kept from every hook and passed to Claude together.
Each hook has a

```
type
```

that determines how it runs. Most hooks use

```
"type": "command"
```

, which runs a shell command. Four other types are available:

- ```
  "type": "http"
  ```

  : POST event data to a URL. See[[Automate workflows with hooks - Claude Code Docs#HTTP hooks|HTTP hooks]].
- ```
  "type": "mcp_tool"
  ```

  : call a tool on an already-connected MCP server. See[[Hooks reference - Claude Code Docs#MCP tool hook fields|MCP tool hooks]].
- ```
  "type": "prompt"
  ```

  : single-turn LLM evaluation. See[[Automate workflows with hooks - Claude Code Docs#Prompt-based hooks|Prompt-based hooks]].
- ```
  "type": "agent"
  ```

  : multi-turn verification with tool access. Agent hooks are experimental and may change. See[[Automate workflows with hooks - Claude Code Docs#Agent-based hooks|Agent-based hooks]].

### Read input and return output

Hooks communicate with Claude Code through stdin, stdout, stderr, and exit codes. When an event fires, Claude Code passes event-specific data as JSON to your script’s stdin. Your script reads that data, does its work, and tells Claude Code what to do next via the exit code.

#### Hook input

Every event includes common fields like

```
session_id
```

and

```
cwd
```

, but each event type adds different data. For example, when Claude runs a Bash command, a

```
PreToolUse
```

hook receives something like this on stdin:

```
UserPromptSubmit
```

hooks get the

```
prompt
```

text instead,

```
SessionStart
```

hooks get the

```
source
```

(startup, resume, clear, compact), and so on. See

[[Hooks reference - Claude Code Docs#Common input fields|Common input fields]]in the reference for shared fields, and each event’s section for event-specific schemas.

#### Hook output

Your script tells Claude Code what to do next by writing to stdout or stderr and exiting with a specific code. For example, a

```
PreToolUse
```

hook that wants to block a command:

- Exit 0: the action proceeds. For

  ```
  UserPromptSubmit
  ```

  ,

  ```
  UserPromptExpansion
  ```

  , and

  ```
  SessionStart
  ```

  hooks, anything you write to stdout is added to Claude’s context.
- Exit 2: the action is blocked. Write a reason to stderr, and Claude receives it as feedback so it can adjust.
- Any other exit code: the action proceeds. The transcript shows a

  ```
  <hook name> hook error
  ```

  notice followed by the first line of stderr; the full stderr goes to the[[Hooks reference - Claude Code Docs#Debug hooks|debug log]].

#### Structured JSON output

Exit codes give you two options: allow or block. For more control, exit 0 and print a JSON object to stdout instead.

Use exit 2 to block with a stderr message, or exit 0 with JSON for structured control. Don’t mix them: Claude Code ignores JSON when you exit 2.

```
PreToolUse
```

hook can deny a tool call and tell Claude why, or escalate it to the user for approval:

```
"deny"
```

, Claude Code cancels the tool call and feeds

```
permissionDecisionReason
```

back to Claude. These

```
permissionDecision
```

values are specific to

```
PreToolUse
```

:

- ```
  "allow"
  ```

  : skip the interactive permission prompt. Deny and ask rules, including enterprise managed deny lists, still apply
- ```
  "deny"
  ```

  : cancel the tool call and send the reason to Claude
- ```
  "ask"
  ```

  : show the permission prompt to the user as normal

```
"defer"
```

, is available in

[[Run Claude Code programmatically - Claude Code Docs|non-interactive mode]]with the

```
-p
```

flag. It exits the process with the tool call preserved so an Agent SDK wrapper can collect input and resume. See

[[Hooks reference - Claude Code Docs#Defer a tool call for later|Defer a tool call for later]]in the reference. Returning

```
"allow"
```

skips the interactive prompt but does not override

[[Configure permissions - Claude Code Docs#Manage permissions|permission rules]]. If a deny rule matches the tool call, the call is blocked even when your hook returns

```
"allow"
```

. If an ask rule matches, the user is still prompted. This means deny rules from any settings scope, including

[[Claude Code settings - Claude Code Docs#Settings files|managed settings]], always take precedence over hook approvals. Other events use different decision patterns. For example,

```
PostToolUse
```

and

```
Stop
```

hooks use a top-level

```
decision: "block"
```

field, while

```
PermissionRequest
```

uses

```
hookSpecificOutput.decision.behavior
```

. See the

[[Hooks reference - Claude Code Docs#Decision control|summary table]]in the reference for a full breakdown by event. For

```
UserPromptSubmit
```

hooks, use

```
additionalContext
```

instead to inject text into Claude’s context. Prompt-based hooks (

```
type: "prompt"
```

) handle output differently: see

[[Automate workflows with hooks - Claude Code Docs#Prompt-based hooks|Prompt-based hooks]].

### Filter hooks with matchers

Without a matcher, a hook fires on every occurrence of its event. Matchers let you narrow that down. For example, if you want to run a formatter only after file edits (not after every tool call), add a matcher to your

```
PostToolUse
```

hook:

```
"Edit|Write"
```

matcher fires only when Claude uses the

```
Edit
```

or

```
Write
```

tool, not when it uses

```
Bash
```

,

```
Read
```

, or any other tool. See

[[Hooks reference - Claude Code Docs#Matcher patterns|Matcher patterns]]for how plain names and regular expressions are evaluated. Each event type matches on a specific field:

EventWhat the matcher filtersExample matcher values

```
PreToolUse
```

,

```
PostToolUse
```

,

```
PostToolUseFailure
```

,

```
PermissionRequest
```

,

```
PermissionDenied
```

tool name

```
Bash
```

,

```
Edit|Write
```

,

```
mcp__.*
```

```
SessionStart
```

how the session started

```
startup
```

,

```
resume
```

,

```
clear
```

,

```
compact
```

```
SessionEnd
```

why the session ended

```
clear
```

,

```
resume
```

,

```
logout
```

,

```
prompt_input_exit
```

,

```
bypass_permissions_disabled
```

,

```
other
```

```
Notification
```

notification type

```
permission_prompt
```

,

```
idle_prompt
```

,

```
auth_success
```

,

```
elicitation_dialog
```

```
SubagentStart
```

agent type

```
Bash
```

,

```
Explore
```

,

```
Plan
```

, or custom agent names

```
PreCompact
```

,

```
PostCompact
```

what triggered compaction

```
manual
```

,

```
auto
```

```
SubagentStop
```

agent typesame values as

```
SubagentStart
```

```
ConfigChange
```

configuration source

```
user_settings
```

,

```
project_settings
```

,

```
local_settings
```

,

```
policy_settings
```

,

```
skills
```

```
StopFailure
```

error type

```
rate_limit
```

,

```
authentication_failed
```

,

```
billing_error
```

,

```
invalid_request
```

,

```
server_error
```

,

```
max_output_tokens
```

,

```
unknown
```

```
InstructionsLoaded
```

load reason

```
session_start
```

,

```
nested_traversal
```

,

```
path_glob_match
```

,

```
include
```

,

```
compact
```

```
Elicitation
```

MCP server nameyour configured MCP server names

```
ElicitationResult
```

MCP server namesame values as

```
Elicitation
```

```
FileChanged
```

literal filenames to watch (see

```
.envrc|.env
```

```
UserPromptExpansion
```

```
UserPromptSubmit
```

,

```
PostToolBatch
```

,

```
Stop
```

,

```
TeammateIdle
```

,

```
TaskCreated
```

,

```
TaskCompleted
```

,

```
WorktreeCreate
```

,

```
WorktreeRemove
```

,

```
CwdChanged
```

- Log every Bash command
- Match MCP tools
- Clean up on session end

Match only

```
Bash
```

tool calls and log each command to a file. The

```
PostToolUse
```

event fires after the command completes, so

```
tool_input.command
```

contains what ran. The hook receives the event data as JSON on stdin, and

```
jq -r '.tool_input.command'
```

extracts just the command string, which

```
>>
```

appends to the log file:

[[Hooks reference - Claude Code Docs#Configuration|Hooks reference]].

#### Filter by tool name and arguments with the ``` if ``` field

The

```
if
```

field requires Claude Code v2.1.85 or later. Earlier versions ignore it and run the hook on every matched call.

```
if
```

field uses

[[Configure permissions - Claude Code Docs|permission rule syntax]]to filter hooks by tool name and arguments together, so the hook process only spawns when the tool call matches, or when a Bash command is too complex to parse. This goes beyond

```
matcher
```

, which filters at the group level by tool name only.
For example, to run a hook only when Claude uses

```
git
```

commands rather than all Bash commands:

```
git *
```

, or when the command is too complex to parse into subcommands. For compound commands like

```
npm test && git push
```

, Claude Code evaluates each subcommand and fires the hook because

```
git push
```

matches. The

```
if
```

field accepts the same patterns as permission rules:

```
"Bash(git *)"
```

,

```
"Edit(*.ts)"
```

, and so on. To match multiple tool names, use separate handlers each with its own

```
if
```

value, or match at the

```
matcher
```

level where pipe alternation is supported.

```
if
```

only works on tool events:

```
PreToolUse
```

,

```
PostToolUse
```

,

```
PostToolUseFailure
```

,

```
PermissionRequest
```

, and

```
PermissionDenied
```

. Adding it to any other event prevents the hook from running.

### Configure hook location

Where you add a hook determines its scope:

LocationScopeShareable

```
~/.claude/settings.json
```

All your projectsNo, local to your machine

```
.claude/settings.json
```

Single projectYes, can be committed to the repo

```
.claude/settings.local.json
```

Single projectNo, gitignoredManaged policy settingsOrganization-wideYes, admin-controlled

```
hooks/hooks.json
```

[[Extend Claude with skills - Claude Code Docs|Skill]]or[[Create custom subagents - Claude Code Docs|agent]]frontmatter

[[Hooks reference - Claude Code Docs|in Claude Code to browse all configured hooks grouped by event. To disable all hooks at once, set]]

```
/hooks
```

```
"disableAllHooks": true
```

in your settings file.
If you edit settings files directly while Claude Code is running, the file watcher normally picks up hook changes automatically.

## Prompt-based hooks

For decisions that require judgment rather than deterministic rules, use

```
type: "prompt"
```

hooks. Instead of running a shell command, Claude Code sends your prompt and the hook’s input data to a Claude model (Haiku by default) to make the decision. You can specify a different model with the

```
model
```

field if you need more capability.
The model’s only job is to return a yes/no decision as JSON:

- ```
  "ok": true
  ```

  : the action proceeds
- ```
  "ok": false
  ```

  : the action is blocked. The model’s

  ```
  "reason"
  ```

  is fed back to Claude so it can adjust.

```
Stop
```

hook to ask the model whether all requested tasks are complete. If the model returns

```
"ok": false
```

, Claude keeps working and uses the

```
reason
```

as its next instruction:

[[Hooks reference - Claude Code Docs#Prompt-based hooks|Prompt-based hooks]]in the reference.

## Agent-based hooks

When verification requires inspecting files or running commands, use

```
type: "agent"
```

hooks. Unlike prompt hooks which make a single LLM call, agent hooks spawn a subagent that can read files, search code, and use other tools to verify conditions before returning a decision.
Agent hooks use the same

```
"ok"
```

/

```
"reason"
```

response format as prompt hooks, but with a longer default timeout of 60 seconds and up to 50 tool-use turns.
This example verifies that tests pass before allowing Claude to stop:

[[Hooks reference - Claude Code Docs#Agent-based hooks|Agent-based hooks]]in the reference.

## HTTP hooks

Use

```
type: "http"
```

hooks to POST event data to an HTTP endpoint instead of running a shell command. The endpoint receives the same JSON that a command hook would receive on stdin, and returns results through the HTTP response body using the same JSON format.
HTTP hooks are useful when you want a web server, cloud function, or external service to handle hook logic: for example, a shared audit service that logs tool use events across a team.
This example posts every tool use to a local logging service:

[[Hooks reference - Claude Code Docs#JSON output|output format]]as command hooks. To block a tool call, return a 2xx response with the appropriate

```
hookSpecificOutput
```

fields. HTTP status codes alone cannot block actions.
Header values support environment variable interpolation using

```
$VAR_NAME
```

or

```
${VAR_NAME}
```

syntax. Only variables listed in the

```
allowedEnvVars
```

array are resolved; all other

```
$VAR
```

references remain empty.
For full configuration options and response handling, see

[[Hooks reference - Claude Code Docs#HTTP hook fields|HTTP hooks]]in the reference.

## Limitations and troubleshooting

### Limitations

- Command hooks communicate through stdout, stderr, and exit codes only. They cannot trigger

  ```
  /
  ```

  commands or tool calls. Text returned via

  ```
  additionalContext
  ```

  is injected as a system reminder that Claude reads as plain text. HTTP hooks communicate through the response body instead.
- Hook timeout is 10 minutes by default, configurable per hook with the

  ```
  timeout
  ```

  field (in seconds).
- ```
  PostToolUse
  ```

  hooks cannot undo actions since the tool has already executed.
- ```
  PermissionRequest
  ```

  hooks do not fire in[[Run Claude Code programmatically - Claude Code Docs|non-interactive mode]](

  ```
  -p
  ```

  ). Use

  ```
  PreToolUse
  ```

  hooks for automated permission decisions.
- ```
  Stop
  ```

  hooks fire whenever Claude finishes responding, not only at task completion. They do not fire on user interrupts. API errors fire[[Hooks reference - Claude Code Docs#StopFailure|StopFailure]]instead.
- When multiple PreToolUse hooks return to rewrite a tool’s arguments, the last one to finish wins. Since hooks run in parallel, the order is non-deterministic. Avoid having more than one hook modify the same tool’s input.

  ```
  updatedInput
  ```

### Hooks and permission modes

PreToolUse hooks fire before any permission-mode check. A hook that returns

```
permissionDecision: "deny"
```

blocks the tool even in

```
bypassPermissions
```

mode or with

```
--dangerously-skip-permissions
```

. This lets you enforce policy that users cannot bypass by changing their permission mode.
The reverse is not true: a hook returning

```
"allow"
```

does not bypass deny rules from settings. Hooks can tighten restrictions but not loosen them past what permission rules allow.

### Hook not firing

The hook is configured but never executes.

- Run

  ```
  /hooks
  ```

  and confirm the hook appears under the correct event
- Check that the matcher pattern matches the tool name exactly (matchers are case-sensitive)
- Verify you’re triggering the right event type (e.g.,

  ```
  PreToolUse
  ```

  fires before tool execution,

  ```
  PostToolUse
  ```

  fires after)
- If using

  ```
  PermissionRequest
  ```

  hooks in non-interactive mode (

  ```
  -p
  ```

  ), switch to

  ```
  PreToolUse
  ```

  instead

### Hook error in output

You see a message like “PreToolUse hook error: …” in the transcript.

- Your script exited with a non-zero code unexpectedly. Test it manually by piping sample JSON:
- If you see “command not found”, use absolute paths or

  ```
  $CLAUDE_PROJECT_DIR
  ```

  to reference scripts
- If you see “jq: command not found”, install

  ```
  jq
  ```

  or use Python/Node.js for JSON parsing
- If the script isn’t running at all, make it executable:

  ```
  chmod +x ./my-hook.sh
  ```

### ``` /hooks ``` shows no hooks configured

You edited a settings file but the hooks don’t appear in the menu.

- File edits are normally picked up automatically. If they haven’t appeared after a few seconds, the file watcher may have missed the change: restart your session to force a reload.
- Verify your JSON is valid (trailing commas and comments are not allowed)
- Confirm the settings file is in the correct location:

  ```
  .claude/settings.json
  ```

  for project hooks,

  ```
  ~/.claude/settings.json
  ```

  for global hooks

### Stop hook runs forever

Claude keeps working in an infinite loop instead of stopping. Your Stop hook script needs to check whether it already triggered a continuation. Parse the

```
stop_hook_active
```

field from the JSON input and exit early if it’s

```
true
```

:

### JSON validation failed

Claude Code shows a JSON parsing error even though your hook script outputs valid JSON. When Claude Code runs a hook, it spawns a shell that sources your profile (

```
~/.zshrc
```

or

```
~/.bashrc
```

). If your profile contains unconditional

```
echo
```

statements, that output gets prepended to your hook’s JSON:

```
$-
```

variable contains shell flags, and

```
i
```

means interactive. Hooks run in non-interactive shells, so the echo is skipped.

### Debug techniques

The transcript view, toggled with

```
Ctrl+O
```

, shows a one-line summary for each hook that fired: success is silent, blocking errors show stderr, and non-blocking errors show a

```
<hook name> hook error
```

notice followed by the first line of stderr.
For full execution details including which hooks matched, their exit codes, stdout, and stderr, read the debug log. Start Claude Code with

```
claude --debug-file /tmp/claude.log
```

to write to a known path, then

```
tail -f /tmp/claude.log
```

in another terminal. If you started without that flag, run

```
/debug
```

mid-session to enable logging and find the log path.

## Learn more

- [[Hooks reference - Claude Code Docs|Hooks reference]]: full event schemas, JSON output format, async hooks, and MCP tool hooks
- [[Hooks reference - Claude Code Docs#Security considerations|Security considerations]]: review before deploying hooks in shared or production environments
- [Bash command validator example](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): complete reference implementation

---
title: Customize your status line - Claude Code Docs
source_url: https://code.claude.com/docs/en/statusline
description: Configure a custom status bar to monitor context window usage, costs,
  and git status in Claude Code
---

- Want to monitor context window usage as you work
- Need to track session costs
- Work across multiple sessions and need to distinguish them
- Want git branch and status always visible

[[Customize your status line - Claude Code Docs#Display multiple lines|multi-line status line]]that displays git info on the first line and a color-coded context bar on the second.

[[Customize your status line - Claude Code Docs#Set up a status line|setting up a basic status line]], explains

[[Customize your status line - Claude Code Docs#How status lines work|how the data flows]]from Claude Code to your script, lists

[[Customize your status line - Claude Code Docs#Available data|all the fields you can display]], and provides

[[Customize your status line - Claude Code Docs#Examples|ready-to-use examples]]for common patterns like git status, cost tracking, and progress bars.

## Set up a status line

Use the

[[Customize your status line - Claude Code Docs|to have Claude Code generate a script for you, or]]

```
/statusline
```

command

[[Customize your status line - Claude Code Docs#Manually configure a status line|manually create a script]]and add it to your settings.

### Use the /statusline command

The

```
/statusline
```

command accepts natural language instructions describing what you want displayed. Claude Code generates a script file in

```
~/.claude/
```

and updates your settings automatically:

### Manually configure a status line

Add a

```
statusLine
```

field to your user settings (

```
~/.claude/settings.json
```

, where

```
~
```

is your home directory) or

[[Claude Code settings - Claude Code Docs#Settings files|project settings]]. Set

```
type
```

to

```
"command"
```

and point

```
command
```

to a script path or an inline shell command. For a full walkthrough of creating a script, see

[[Customize your status line - Claude Code Docs#Build a status line step by step|Build a status line step by step]].

```
command
```

field runs in a shell, so you can also use inline commands instead of a script file. This example uses

```
jq
```

to parse the JSON input and display the model name and context percentage:

```
padding
```

field adds extra horizontal spacing (in characters) to the status line content. Defaults to

```
0
```

. This padding is in addition to the interface’s built-in spacing, so it controls relative indentation rather than absolute distance from the terminal edge.
The optional

```
refreshInterval
```

field re-runs your command every N seconds in addition to the

[[Customize your status line - Claude Code Docs#How status lines work|event-driven updates]]. The minimum is

```
1
```

. Set this when your status line shows time-based data such as a clock, or when background subagents change git state while the main session is idle. Leave it unset to run only on events.

### Disable the status line

Run

```
/statusline
```

and ask it to remove or clear your status line (e.g.,

```
/statusline delete
```

,

```
/statusline clear
```

,

```
/statusline remove it
```

). You can also manually delete the

```
statusLine
```

field from your settings.json.

## Build a status line step by step

This walkthrough shows what’s happening under the hood by manually creating a status line that displays the current model, working directory, and context window usage percentage.

Running

[[Customize your status line - Claude Code Docs|with a description of what you want configures all of this for you automatically.]]

```
/statusline
```

[[Customize your status line - Claude Code Docs#Windows configuration|Windows configuration]]for PowerShell and Git Bash examples.

Create a script that reads JSON and prints output

Claude Code sends JSON data to your script via stdin. This script uses

[, a command-line JSON parser you may need to install, to extract the model name, directory, and context percentage, then prints a formatted line.Save this to](https://jqlang.github.io/jq/)

```
jq
```

```
~/.claude/statusline.sh
```

(where

```
~
```

is your home directory, such as

```
/Users/username
```

on macOS or

```
/home/username
```

on Linux):

Add to settings

Tell Claude Code to run your script as the status line. Add this configuration to Your status line appears at the bottom of the interface. Settings reload automatically, but changes won’t appear until your next interaction with Claude Code.

```
~/.claude/settings.json
```

, which sets

```
type
```

to

```
"command"
```

(meaning “run this shell command”) and points

```
command
```

to your script:

## How status lines work

Claude Code runs your script and pipes

[[Customize your status line - Claude Code Docs#Available data|JSON session data]]to it via stdin. Your script reads the JSON, extracts what it needs, and prints text to stdout. Claude Code displays whatever your script prints. When it updates Your script runs after each new assistant message, when the permission mode changes, or when vim mode toggles. Updates are debounced at 300ms, meaning rapid changes batch together and your script runs once things settle. If a new update triggers while your script is still running, the in-flight execution is cancelled. If you edit your script, the changes won’t appear until your next interaction with Claude Code triggers an update. These triggers can go quiet when the main session is idle, for example while a coordinator waits on background subagents. To keep time-based or externally-sourced segments current during idle periods, set

[[Customize your status line - Claude Code Docs#Manually configure a status line|to also re-run the command on a fixed timer. What your script can output]]

```
refreshInterval
```

- Multiple lines: each

  ```
  echo
  ```

  or

  ```
  print
  ```

  statement displays as a separate row. See the[[Customize your status line - Claude Code Docs#Display multiple lines|multi-line example]].
- Colors: use [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)like

  ```
  \033[[Customize your status line - Claude Code Docs#Git status with colors|32m
  ```

  for green (terminal must support them). See the[git status example]].
- Links: use [OSC 8 escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code#OSC)to make text clickable (Cmd+click on macOS, Ctrl+click on Windows/Linux). Requires a terminal that supports hyperlinks like iTerm2, Kitty, or WezTerm. See the[[Customize your status line - Claude Code Docs#Clickable links|clickable links example]].

The status line runs locally and does not consume API tokens. It temporarily hides during certain UI interactions, including autocomplete suggestions, the help menu, and permission prompts.

## Available data

Claude Code sends the following JSON fields to your script via stdin:

FieldDescription

```
model.id
```

,

```
model.display_name
```

Current model identifier and display name

```
cwd
```

,

```
workspace.current_dir
```

Current working directory. Both fields contain the same value;

```
workspace.current_dir
```

is preferred for consistency with

```
workspace.project_dir
```

.

```
workspace.project_dir
```

Directory where Claude Code was launched, which may differ from

```
cwd
```

if the working directory changes during a session

```
workspace.added_dirs
```

Additional directories added via

```
/add-dir
```

or

```
--add-dir
```

. Empty array if none have been added

```
workspace.git_worktree
```

Git worktree name when the current directory is inside a linked worktree created with

```
git worktree add
```

. Absent in the main working tree. Populated for any git worktree, unlike

```
worktree.*
```

which applies only to

```
--worktree
```

sessions

```
cost.total_cost_usd
```

Estimated session cost in USD, computed client-side. May differ from your actual bill

```
cost.total_duration_ms
```

Total wall-clock time since the session started, in milliseconds

```
cost.total_api_duration_ms
```

Total time spent waiting for API responses in milliseconds

```
cost.total_lines_added
```

,

```
cost.total_lines_removed
```

Lines of code changed

```
context_window.total_input_tokens
```

,

```
context_window.total_output_tokens
```

Cumulative token counts across the session

```
context_window.context_window_size
```

Maximum context window size in tokens. 200000 by default, or 1000000 for models with extended context.

```
context_window.used_percentage
```

Pre-calculated percentage of context window used

```
context_window.remaining_percentage
```

Pre-calculated percentage of context window remaining

```
context_window.current_usage
```

Token counts from the last API call, described in

```
exceeds_200k_tokens
```

```
effort.level
```

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

). Reflects the live session value, including mid-session

```
/effort
```

changes. Absent when the current model does not support the effort parameter

```
thinking.enabled
```

```
rate_limits.five_hour.used_percentage
```

,

```
rate_limits.seven_day.used_percentage
```

```
rate_limits.five_hour.resets_at
```

,

```
rate_limits.seven_day.resets_at
```

```
session_id
```

```
session_name
```

```
--name
```

flag or

```
/rename
```

. Absent if no custom name has been set

```
transcript_path
```

```
version
```

```
output_style.name
```

```
vim.mode
```

```
NORMAL
```

,

```
INSERT
```

,

```
VISUAL
```

, or

```
VISUAL LINE
```

) when [[Interactive mode - Claude Code Docs#Vim editor mode|vim mode]]is enabled

```
agent.name
```

```
--agent
```

flag or agent settings configured

```
worktree.name
```

```
--worktree
```

sessions

```
worktree.path
```

```
worktree.branch
```

```
"worktree-my-feature"
```

). Absent for hook-based worktrees

```
worktree.original_cwd
```

```
worktree.original_branch
```

###

Full JSON schema

Full JSON schema

Your status line command receives this JSON structure via stdin:Fields that may be absent (not present in JSON):

- ```
  session_name
  ```

  : appears only when a custom name has been set with

  ```
  --name
  ```

  or

  ```
  /rename
  ```
- ```
  workspace.git_worktree
  ```

  : appears only when the current directory is inside a linked git worktree
- ```
  effort
  ```

  : appears only when the current model supports the reasoning effort parameter
- ```
  vim
  ```

  : appears only when vim mode is enabled
- ```
  agent
  ```

  : appears only when running with the

  ```
  --agent
  ```

  flag or agent settings configured
- ```
  worktree
  ```

  : appears only during

  ```
  --worktree
  ```

  sessions. When present,

  ```
  branch
  ```

  and

  ```
  original_branch
  ```

  may also be absent for hook-based worktrees
- ```
  rate_limits
  ```

  : appears only for Claude.ai subscribers (Pro/Max) after the first API response in the session. Each window (

  ```
  five_hour
  ```

  ,

  ```
  seven_day
  ```

  ) may be independently absent. Use

  ```
  jq -r '.rate_limits.five_hour.used_percentage // empty'
  ```

  to handle absence gracefully.

```
null
```

:

- ```
  context_window.current_usage
  ```

  :

  ```
  null
  ```

  before the first API call in a session
- ```
  context_window.used_percentage
  ```

  ,

  ```
  context_window.remaining_percentage
  ```

  : may be

  ```
  null
  ```

  early in the session

### Context window fields

The

```
context_window
```

object provides two ways to track context usage:

- Cumulative totals (

  ```
  total_input_tokens
  ```

  ,

  ```
  total_output_tokens
  ```

  ): sum of all tokens across the entire session, useful for tracking total consumption
- Current usage (

  ```
  current_usage
  ```

  ): token counts from the most recent API call, use this for accurate context percentage since it reflects the actual context state

```
current_usage
```

object contains:

- ```
  input_tokens
  ```

  : input tokens in current context
- ```
  output_tokens
  ```

  : output tokens generated
- ```
  cache_creation_input_tokens
  ```

  : tokens written to cache
- ```
  cache_read_input_tokens
  ```

  : tokens read from cache

```
used_percentage
```

field is calculated from input tokens only:

```
input_tokens + cache_creation_input_tokens + cache_read_input_tokens
```

. It does not include

```
output_tokens
```

.
If you calculate context percentage manually from

```
current_usage
```

, use the same input-only formula to match

```
used_percentage
```

.
The

```
current_usage
```

object is

```
null
```

before the first API call in a session.

## Examples

These examples show common status line patterns. To use any example:

- Save the script to a file like

  ```
  ~/.claude/statusline.sh
  ```

  (or

  ```
  .py
  ```

  /

  ```
  .js
  ```

  )
- Make it executable:

  ```
  chmod +x ~/.claude/statusline.sh
  ```
- Add the path to your [[Customize your status line - Claude Code Docs#Manually configure a status line|settings]]

[to parse JSON. Python and Node.js have built-in JSON parsing.](https://jqlang.github.io/jq/)

```
jq
```

### Context window usage

Display the current model and context window usage with a visual progress bar. Each script reads JSON from stdin, extracts the

```
used_percentage
```

field, and builds a 10-character bar where filled blocks (▓) represent usage:

### Git status with colors

Show git branch with color-coded indicators for staged and modified files. This script uses

[ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)for terminal colors:

```
\033[[Create custom subagents - Claude Code Docs|32m
```

is green,

```
\033[33m
```

is yellow, and

```
\033[0m
```

resets to default.

### Cost and duration tracking

Track your session’s API costs and elapsed time. The

```
cost.total_cost_usd
```

field accumulates the estimated cost of all API calls in the current session. The

```
cost.total_duration_ms
```

field measures total elapsed time since the session started, while

```
cost.total_api_duration_ms
```

tracks only the time spent waiting for API responses.
Each script formats cost as currency and converts milliseconds to minutes and seconds:

### Display multiple lines

Your script can output multiple lines to create a richer display. Each

```
echo
```

statement produces a separate row in the status area.

```
print
```

or

```
echo
```

statement creates a separate row:

### Clickable links

This example creates a clickable link to your GitHub repository. It reads the git remote URL, converts SSH format to HTTPS with

```
sed
```

, and wraps the repo name in OSC 8 escape codes. Hold Cmd (macOS) or Ctrl (Windows/Linux) and click to open the link in your browser.

```
printf '%b'
```

which interprets backslash escapes more reliably than

```
echo -e
```

across different shells:

### Rate limit usage

Display Claude.ai subscription rate limit usage in the status line. The

```
rate_limits
```

object contains

```
five_hour
```

(5-hour rolling window) and

```
seven_day
```

(weekly) windows. Each window provides

```
used_percentage
```

(0-100) and

```
resets_at
```

(Unix epoch seconds when the window resets).
This field is only present for Claude.ai subscribers (Pro/Max) after the first API response. Each script handles the absent field gracefully:

### Cache expensive operations

Your status line script runs frequently during active sessions. Commands like

```
git status
```

or

```
git diff
```

can be slow, especially in large repositories. This example caches git information to a temp file and only refreshes it every 5 seconds.
The cache filename needs to be stable across status line invocations within a session, but unique across sessions so concurrent sessions in different repositories don’t read each other’s cached git state. Process-based identifiers like

```
$$
```

,

```
os.getpid()
```

, or

```
process.pid
```

change on every invocation and defeat the cache. Use the

```
session_id
```

from the JSON input instead: it’s stable for the lifetime of a session and unique per session.
Each script checks if the cache file is missing or older than 5 seconds before running git commands:

### Windows configuration

On Windows, Claude Code runs status line commands through Git Bash. You can invoke PowerShell from that shell:

## Subagent status lines

The

```
subagentStatusLine
```

setting renders a custom row body for each

[subagent]]shown in the agent panel below the prompt. Use it to replace the default

```
name · description · token count
```

row with your own formatting.

[[Hooks reference - Claude Code Docs#Common input fields|base hook fields]]plus

```
columns
```

(the usable row width) and a

```
tasks
```

array, where each task has

```
id
```

,

```
name
```

,

```
type
```

,

```
status
```

,

```
description
```

,

```
label
```

,

```
startTime
```

,

```
tokenCount
```

,

```
tokenSamples
```

, and

```
cwd
```

.
Write one JSON line to stdout per row you want to override, in the form

```
{"id": "<task id>", "content": "<row body>"}
```

. The

```
content
```

string is rendered as-is, including ANSI colors and OSC 8 hyperlinks. Omit a task’s

```
id
```

to keep the default rendering for that row; emit an empty

```
content
```

string to hide it.
The same trust and

```
disableAllHooks
```

gates that apply to

```
statusLine
```

apply here. Plugins can ship a default

```
subagentStatusLine
```

in their

[[Plugins reference - Claude Code Docs#Standard plugin layout|.]]

```
settings.json
```

## Tips

- Test with mock input:

  ```
  echo '{"model":{"display_name":"Opus"},"workspace":{"current_dir":"/home/user/project"},"context_window":{"used_percentage":25},"session_id":"test-session-abc"}' | ./statusline.sh
  ```
- Keep output short: the status bar has limited width, so long output may get truncated or wrap awkwardly
- Cache slow operations: your script runs frequently during active sessions, so commands like

  ```
  git status
  ```

  can cause lag. See the[[Customize your status line - Claude Code Docs#Cache expensive operations|caching example]]for how to handle this.

[ccstatusline](https://github.com/sirmalloc/ccstatusline)and

[starship-claude](https://github.com/martinemde/starship-claude)provide pre-built configurations with themes and additional features.

## Troubleshooting

Status line not appearing

- Verify your script is executable:

  ```
  chmod +x ~/.claude/statusline.sh
  ```
- Check that your script outputs to stdout, not stderr
- Run your script manually to verify it produces output
- If

  ```
  disableAllHooks
  ```

  is set to

  ```
  true
  ```

  in your settings, the status line is also disabled. Remove this setting or set it to

  ```
  false
  ```

  to re-enable.
- Run

  ```
  claude --debug
  ```

  to log the exit code and stderr from the first status line invocation in a session
- Ask Claude to read your settings file and execute the

  ```
  statusLine
  ```

  command directly to surface errors

```
--
```

or empty values

- Fields may be

  ```
  null
  ```

  before the first API response completes
- Handle null values in your script with fallbacks such as

  ```
  // 0
  ```

  in jq
- Restart Claude Code if values remain empty after multiple messages

- Use

  ```
  used_percentage
  ```

  for accurate context state rather than cumulative totals
- The

  ```
  total_input_tokens
  ```

  and

  ```
  total_output_tokens
  ```

  are cumulative across the session and may exceed the context window size
- Context percentage may differ from

  ```
  /context
  ```

  output due to when each is calculated

- Verify your terminal supports OSC 8 hyperlinks (iTerm2, Kitty, WezTerm)
- Terminal.app does not support clickable links
- If link text appears but isn’t clickable, Claude Code may not have detected hyperlink support in your terminal. This commonly affects Windows Terminal and other emulators not in the auto-detection list. Set the

  ```
  FORCE_HYPERLINK
  ```

  environment variable to override detection before launching Claude Code:In PowerShell, set the variable in the current session first:
- SSH and tmux sessions may strip OSC sequences depending on configuration
- If escape sequences appear as literal text like

  ```
  \e]8;;
  ```

  , use

  ```
  printf '%b'
  ```

  instead of

  ```
  echo -e
  ```

  for more reliable escape handling

- Complex escape sequences (ANSI colors, OSC 8 links) can occasionally cause garbled output if they overlap with other UI updates
- If you see corrupted text, try simplifying your script to plain text output
- Multi-line status lines with escape codes are more prone to rendering issues than single-line plain text

- The status line command only runs if you’ve accepted the workspace trust dialog for the current directory. Because

  ```
  statusLine
  ```

  executes a shell command, it requires the same trust acceptance as hooks and other shell-executing settings.
- If trust isn’t accepted, you’ll see the notification

  ```
  statusline skipped · restart to fix
  ```

  instead of your status line output. Restart Claude Code and accept the trust prompt to enable it.

- Scripts that exit with non-zero codes or produce no output cause the status line to go blank
- Slow scripts block the status line from updating until they complete. Keep scripts fast to avoid stale output.
- If a new update triggers while a slow script is running, the in-flight script is cancelled
- Test your script independently with mock input before configuring it

- System notifications like MCP server errors and auto-updates display on the right side of the same row as your status line. Transient notifications such as the context-low warning also cycle through this area.
- Enabling verbose mode adds a token counter to this area
- On narrow terminals, these notifications may truncate your status line output

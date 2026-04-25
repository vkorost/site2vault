---
title: Tools reference - Claude Code Docs
source_url: https://code.claude.com/docs/en/tools-reference
description: Complete reference for the tools Claude Code can use, including permission
  requirements.
---

[[Configure permissions - Claude Code Docs#Tool-specific permission rules|permission rules]],

[[Create custom subagents - Claude Code Docs|subagent tool lists]], and

[[Hooks reference - Claude Code Docs|hook matchers]]. To disable a tool entirely, add its name to the

```
deny
```

array in your

[[Configure permissions - Claude Code Docs#Tool-specific permission rules|permission settings]]. To add custom tools, connect an

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP server]]. To extend Claude with reusable prompt-based workflows, write a

[[Extend Claude with skills - Claude Code Docs|skill]], which runs through the existing

```
Skill
```

tool rather than adding a new tool entry.

ToolDescriptionPermission Required

```
Agent
```

Spawns a

```
AskUserQuestion
```

```
Bash
```

[[Tools reference - Claude Code Docs#Bash tool behavior|Bash tool behavior]]

```
CronCreate
```

```
--resume
```

or

```
--continue
```

if unexpired. See [[Run prompts on a schedule - Claude Code Docs|scheduled tasks]]

```
CronDelete
```

```
CronList
```

```
Edit
```

```
EnterPlanMode
```

```
EnterWorktree
```

[[Common workflows - Claude Code Docs#Run parallel Claude Code sessions with Git worktrees|git worktree]]and switches into it. Pass a

```
path
```

to switch into an existing worktree of the current repository instead of creating a new one. Not available to subagents

```
ExitPlanMode
```

```
ExitWorktree
```

```
Glob
```

```
Grep
```

```
ListMcpResourcesTool
```

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP servers]]

```
LSP
```

[[Tools reference - Claude Code Docs#LSP tool behavior|LSP tool behavior]]

```
Monitor
```

[[Tools reference - Claude Code Docs#Monitor tool|Monitor tool]]

```
NotebookEdit
```

```
PowerShell
```

[[Tools reference - Claude Code Docs#PowerShell tool|PowerShell tool]]for availability

```
Read
```

```
ReadMcpResourceTool
```

```
SendMessage
```

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|agent team]]teammate, or[[Create custom subagents - Claude Code Docs#Resume subagents|resumes a subagent]]by its agent ID. Stopped subagents auto-resume in the background. Only available when

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

is set

```
Skill
```

[[Extend Claude with skills - Claude Code Docs#Control who invokes a skill|skill]]within the main conversation

```
TaskCreate
```

```
TaskGet
```

```
TaskList
```

```
TaskOutput
```

```
Read
```

on the task’s output file path

```
TaskStop
```

```
TaskUpdate
```

```
TeamCreate
```

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|agent team]]with multiple teammates. Only available when

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

is set

```
TeamDelete
```

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

is set

```
TodoWrite
```

[[Run Claude Code programmatically - Claude Code Docs|Agent SDK]]; interactive sessions use TaskCreate, TaskGet, TaskList, and TaskUpdate instead

```
ToolSearch
```

[[Connect Claude Code to tools via MCP - Claude Code Docs#Scale with MCP Tool Search|tool search]]is enabled

```
WebFetch
```

```
WebSearch
```

```
Write
```

```
/permissions
```

or in

[[Claude Code settings - Claude Code Docs#Available settings|permission settings]]. Also see

[[Configure permissions - Claude Code Docs#Tool-specific permission rules|Tool-specific permission rules]].

## Bash tool behavior

The Bash tool runs each command in a separate process with the following persistence behavior:

- When Claude runs

  ```
  cd
  ```

  in the main session, the new working directory carries over to later Bash commands as long as it stays inside the project directory or an[[Configure permissions - Claude Code Docs#Working directories|additional working directory]]you added with

  ```
  --add-dir
  ```

  ,

  ```
  /add-dir
  ```

  , or

  ```
  additionalDirectories
  ```

  in settings. Subagent sessions never carry over working directory changes.
  - If

    ```
    cd
    ```

    lands outside those directories, Claude Code resets to the project directory and appends

    ```
    Shell cwd was reset to <dir>
    ```

    to the tool result.
  - To disable this carry-over so every Bash command starts in the project directory, set

    ```
    CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1
    ```

    .
- If
- Environment variables do not persist. An

  ```
  export
  ```

  in one command will not be available in the next.

[[Environment variables - Claude Code Docs|to a shell script before launching Claude Code, or use a]]

```
CLAUDE_ENV_FILE
```

[[Hooks reference - Claude Code Docs#Persist environment variables|SessionStart hook]]to populate it dynamically.

## LSP tool behavior

The LSP tool gives Claude code intelligence from a running language server. After each file edit, it automatically reports type errors and warnings so Claude can fix issues without a separate build step. Claude can also call it directly to navigate code:

- Jump to a symbol’s definition
- Find all references to a symbol
- Get type information at a position
- List symbols in a file or workspace
- Find implementations of an interface
- Trace call hierarchies

[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs#Code intelligence|code intelligence plugin]]for your language. The plugin bundles the language server configuration, and you install the server binary separately.

## Monitor tool

The Monitor tool requires Claude Code v2.1.98 or later.

- Tail a log file and flag errors as they appear
- Poll a PR or CI job and report when its status changes
- Watch a directory for file changes
- Track output from any long-running script you point it at

[[Configure permissions - Claude Code Docs#Tool-specific permission rules|permission rules as Bash]], so

```
allow
```

and

```
deny
```

patterns you have set for Bash apply here too. It is not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry. It is also not available when

```
DISABLE_TELEMETRY
```

or

```
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC
```

is set.
Plugins can declare monitors that start automatically when the plugin is active, instead of asking Claude to start them. See

[[Plugins reference - Claude Code Docs#Monitors|plugin monitors]].

## PowerShell tool

The PowerShell tool lets Claude run PowerShell commands natively. On Windows, this means commands run in PowerShell instead of routing through Git Bash. The tool is rolling out progressively on Windows and is opt-in on Linux, macOS, and WSL.

### Enable the PowerShell tool

Set

```
CLAUDE_CODE_USE_POWERSHELL_TOOL=1
```

in your environment or in

```
settings.json
```

:

```
0
```

to opt out of the rollout. On Linux, macOS, and WSL, the tool requires PowerShell 7 or later: install

```
pwsh
```

and ensure it is on your

```
PATH
```

.
On Windows, Claude Code auto-detects

```
pwsh.exe
```

for PowerShell 7+ with a fallback to

```
powershell.exe
```

for PowerShell 5.1. The Bash tool remains registered alongside the PowerShell tool, so you may need to ask Claude to use PowerShell.

### Shell selection in settings, hooks, and skills

Three additional settings control where PowerShell is used:

- ```
  "defaultShell": "powershell"
  ```

  in: routes interactive

  ```
  settings.json
  ```

  ```
  !
  ```

  commands through PowerShell. Requires the PowerShell tool to be enabled.
- ```
  "shell": "powershell"
  ```

  on individual[[Hooks reference - Claude Code Docs#Command hook fields|command hooks]]: runs that hook in PowerShell. Hooks spawn PowerShell directly, so this works regardless of

  ```
  CLAUDE_CODE_USE_POWERSHELL_TOOL
  ```

  .
- ```
  shell: powershell
  ```

  in[[Extend Claude with skills - Claude Code Docs#Frontmatter reference|skill frontmatter]]: runs

  ```
  !`command`
  ```

  blocks in PowerShell. Requires the PowerShell tool to be enabled.

```
CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR
```

environment variable.

### Preview limitations

The PowerShell tool has the following known limitations during the preview:

- PowerShell profiles are not loaded
- On Windows, sandboxing is not supported
- On Windows, Git Bash is still required to start Claude Code

## Check which tools are available

Your exact tool set depends on your provider, platform, and settings. To check what’s loaded in a running session, ask Claude directly:

```
/mcp
```

.

## See also

- [[Connect Claude Code to tools via MCP - Claude Code Docs|MCP servers]]: add custom tools by connecting external servers
- [[Configure permissions - Claude Code Docs|Permissions]]: permission system, rule syntax, and tool-specific patterns
- [[Create custom subagents - Claude Code Docs|Subagents]]: configure tool access for subagents
- [[Automate workflows with hooks - Claude Code Docs|Hooks]]: run custom commands before or after tool execution

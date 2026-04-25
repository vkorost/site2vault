---
title: Configure permissions - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/permissions
description: Control how your agent uses tools with permission modes, hooks, and declarative
  allow/deny rules.
---

[[Handle approvals and user input - Claude Code Docs|to handle everything else at runtime.]]

```
canUseTool
```

callback

This page covers permission modes and rules. To build interactive approval flows where users approve or deny tool requests at runtime, see

[[Handle approvals and user input - Claude Code Docs|Handle approvals and user input]].

## How permissions are evaluated

When Claude requests a tool, the SDK checks permissions in this order:

Hooks

Run

[[Intercept and control agent behavior with hooks - Claude Code Docs|hooks]]first, which can allow, deny, or continue to the next step

Deny rules

Check

```
deny
```

rules (from

```
disallowed_tools
```

and [[Claude Code settings - Claude Code Docs#Permission settings|settings.json]]). If a deny rule matches, the tool is blocked, even in

```
bypassPermissions
```

mode.

Permission mode

Apply the active

[[Configure permissions - Claude Code Docs-dbd6de#Permission modes|permission mode]].

```
bypassPermissions
```

approves everything that reaches this step.

```
acceptEdits
```

approves file operations. Other modes fall through.

Allow rules

Check

```
allow
```

rules (from

```
allowed_tools
```

and settings.json). If a rule matches, the tool is approved.

canUseTool callback

If not resolved by any of the above, call your

[[Handle approvals and user input - Claude Code Docs|for a decision. In]]

```
canUseTool
```

callback

```
dontAsk
```

mode, this step is skipped and the tool is denied.

- Hooks: run custom code to allow, deny, or modify tool requests. See [[Intercept and control agent behavior with hooks - Claude Code Docs|Control execution with hooks]].
- canUseTool callback: prompt users for approval at runtime. See [[Handle approvals and user input - Claude Code Docs|Handle approvals and user input]].

## Allow and deny rules

```
allowed_tools
```

and

```
disallowed_tools
```

(TypeScript:

```
allowedTools
```

/

```
disallowedTools
```

) add entries to the allow and deny rule lists in the evaluation flow above. They control whether a tool call is approved, not whether the tool is available to Claude.

OptionEffect

```
allowed_tools=["Read", "Grep"]
```

```
Read
```

and

```
Grep
```

are auto-approved. Tools not listed here still exist and fall through to the permission mode and

```
canUseTool
```

.

```
disallowed_tools=["Bash"]
```

```
Bash
```

is always denied. Deny rules are checked first and hold in every permission mode, including

```
bypassPermissions
```

.

```
allowedTools
```

with

```
permissionMode: "dontAsk"
```

. Listed tools are approved; anything else is denied outright instead of prompting:

```
.claude/settings.json
```

. These rules are read when the

```
project
```

setting source is enabled, which it is for default

```
query()
```

options. If you set

```
setting_sources
```

(TypeScript:

```
settingSources
```

) explicitly, include

```
"project"
```

for them to apply. See

[[Claude Code settings - Claude Code Docs#Permission settings|Permission settings]]for the rule syntax.

## Permission modes

Permission modes provide global control over how Claude uses tools. You can set the permission mode when calling

```
query()
```

or change it dynamically during streaming sessions.

### Available modes

The SDK supports these permission modes:

ModeDescriptionTool behavior

```
default
```

Standard permission behaviorNo auto-approvals; unmatched tools trigger your

```
canUseTool
```

callback

```
dontAsk
```

Deny instead of promptingAnything not pre-approved by

```
allowed_tools
```

or rules is denied;

```
canUseTool
```

is never called

```
acceptEdits
```

Auto-accept file editsFile edits and

```
mkdir
```

,

```
rm
```

,

```
mv
```

, etc.) are automatically approved

```
bypassPermissions
```

```
plan
```

```
auto
```

(TypeScript only)[[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|Auto mode]]for availability

### Set permission mode

You can set the permission mode once when starting a query, or change it dynamically while the session is active.

- At query time
- During streaming

Pass

```
permission_mode
```

(Python) or

```
permissionMode
```

(TypeScript) when creating a query. This mode applies for the entire session unless changed dynamically.

### Mode details

#### Accept edits mode ( ``` acceptEdits ``` )

Auto-approves file operations so Claude can edit code without prompting. Other tools (like Bash commands that aren’t filesystem operations) still require normal permissions.
Auto-approved operations:

- File edits (Edit, Write tools)
- Filesystem commands:

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

  ,

  ```
  sed
  ```

```
additionalDirectories
```

. Paths outside that scope and writes to protected paths still prompt.
Use when: you trust Claude’s edits and want faster iteration, such as during prototyping or when working in an isolated directory.

#### Don’t ask mode ( ``` dontAsk ``` )

Converts any permission prompt into a denial. Tools pre-approved by

```
allowed_tools
```

,

```
settings.json
```

allow rules, or a hook run as normal. Everything else is denied without calling

```
canUseTool
```

.
Use when: you want a fixed, explicit tool surface for a headless agent and prefer a hard deny over silent reliance on

```
canUseTool
```

being absent.

#### Bypass permissions mode ( ``` bypassPermissions ``` )

Auto-approves all tool uses without prompts. Hooks still execute and can block operations if needed.

#### Plan mode ( ``` plan ``` )

Prevents tool execution entirely. Claude can analyze code and create plans but cannot make changes. Claude may use

```
AskUserQuestion
```

to clarify requirements before finalizing the plan. See

[[Handle approvals and user input - Claude Code Docs#Handle clarifying questions|Handle approvals and user input]]for handling these prompts. Use when: you want Claude to propose changes without executing them, such as during code review or when you need to approve changes before they’re made.

## Related resources

For the other steps in the permission evaluation flow:

- [[Handle approvals and user input - Claude Code Docs|Handle approvals and user input]]: interactive approval prompts and clarifying questions
- [[Intercept and control agent behavior with hooks - Claude Code Docs|Hooks guide]]: run custom code at key points in the agent lifecycle
- [[Claude Code settings - Claude Code Docs#Permission settings|Permission rules]]: declarative allow/deny rules in

  ```
  settings.json
  ```

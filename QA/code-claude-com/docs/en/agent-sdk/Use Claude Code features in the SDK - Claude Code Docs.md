---
title: Use Claude Code features in the SDK - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/claude-code-features
description: Load project instructions, skills, hooks, and other Claude Code features
  into your SDK agents.
---

```
CLAUDE.md
```

and rules), skills, hooks, and more.
When you omit

```
settingSources
```

,

```
query()
```

reads the same filesystem settings as the Claude Code CLI: user, project, and local settings, CLAUDE.md files, and

```
.claude/
```

skills, agents, and commands. To run without these, pass

```
settingSources: []
```

, which limits the agent to what you configure programmatically. Managed policy settings and the global

```
~/.claude.json
```

config are read regardless of this option. See

[[Use Claude Code features in the SDK - Claude Code Docs#What settingSources does not control|What settingSources does not control]]. For a conceptual overview of what each feature does and when to use it, see

[[Extend Claude Code - Claude Code Docs|Extend Claude Code]].

## Control filesystem settings with settingSources

The setting sources option (

[[Agent SDK reference - Python - Claude Code Docs|in Python,]]

```
setting_sources
```

[[Agent SDK reference - TypeScript - Claude Code Docs|in TypeScript) controls which filesystem-based settings the SDK loads. Pass an explicit list to opt in to specific sources, or pass an empty array to disable user, project, and local settings. This example loads both user-level and project-level settings by setting]]

```
settingSources
```

```
settingSources
```

to

```
["user", "project"]
```

:

```
<cwd>
```

is the working directory you pass via the

```
cwd
```

option (or the process’s current directory if unset). For the full type definition, see

[[Agent SDK reference - TypeScript - Claude Code Docs|(TypeScript) or]]

```
SettingSource
```

[[Agent SDK reference - Python - Claude Code Docs|(Python).]]

```
SettingSource
```

SourceWhat it loadsLocation

```
"project"
```

Project CLAUDE.md,

```
.claude/rules/*.md
```

, project skills, project hooks, project

```
settings.json
```

```
<cwd>/.claude/
```

and each parent directory up to the filesystem root (stopping when a

```
.claude/
```

is found or no more parents exist)

```
"user"
```

User CLAUDE.md,

```
~/.claude/rules/*.md
```

, user skills, user settings

```
~/.claude/
```

```
"local"
```

CLAUDE.local.md (gitignored),

```
.claude/settings.local.json
```

```
<cwd>/
```

```
settingSources
```

is equivalent to

```
["user", "project", "local"]
```

.
The

```
cwd
```

option determines where the SDK looks for project settings. If neither

```
cwd
```

nor any of its parent directories contains a

```
.claude/
```

folder, project-level features won’t load.

### What settingSources does not control

```
settingSources
```

covers user, project, and local settings. A few inputs are read regardless of its value:

InputBehaviorTo disableManaged policy settingsAlways loaded when present on the hostRemove the managed settings file

```
~/.claude.json
```

global configAlways readRelocate with

```
CLAUDE_CONFIG_DIR
```

in

```
env
```

Auto memory at

```
~/.claude/projects/<project>/memory/
```

Loaded by default into the system promptSet

```
autoMemoryEnabled: false
```

in settings, or

```
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

in

```
env
```

## Project instructions (CLAUDE.md and rules)

```
CLAUDE.md
```

files and

```
.claude/rules/*.md
```

files give your agent persistent context about your project: coding conventions, build commands, architecture decisions, and instructions. When

```
settingSources
```

includes

```
"project"
```

(as in the example above), the SDK loads these files into context at session start. The agent then follows your project conventions without you repeating them in every prompt.

### CLAUDE.md load locations

LevelLocationWhen loadedProject (root)

```
<cwd>/CLAUDE.md
```

or

```
<cwd>/.claude/CLAUDE.md
```

```
settingSources
```

includes

```
"project"
```

Project rules

```
<cwd>/.claude/rules/*.md
```

```
settingSources
```

includes

```
"project"
```

Project (parent dirs)

```
CLAUDE.md
```

files in directories above

```
cwd
```

```
settingSources
```

includes

```
"project"
```

, loaded at session startProject (child dirs)

```
CLAUDE.md
```

files in subdirectories of

```
cwd
```

```
settingSources
```

includes

```
"project"
```

, loaded on demand when the agent reads a file in that subtreeLocal (gitignored)

```
<cwd>/CLAUDE.local.md
```

```
settingSources
```

includes

```
"local"
```

User

```
~/.claude/CLAUDE.md
```

```
settingSources
```

includes

```
"user"
```

User rules

```
~/.claude/rules/*.md
```

```
settingSources
```

includes

```
"user"
```

[[How Claude remembers your project - Claude Code Docs|Manage Claude’s memory]].

## Skills

Skills are markdown files that give your agent specialized knowledge and invocable workflows. Unlike

```
CLAUDE.md
```

(which loads every session), skills load on demand. The agent receives skill descriptions at startup and loads the full content when relevant.
Skills are discovered from the filesystem through

```
settingSources
```

. With default options, user and project skills load automatically. The

```
Skill
```

tool is enabled by default when you don’t specify

```
allowedTools
```

. If you are using an

```
allowedTools
```

allowlist, include

```
"Skill"
```

explicitly.

Skills must be created as filesystem artifacts (

```
.claude/skills/<name>/SKILL.md
```

). The SDK does not have a programmatic API for registering skills. See [[Agent Skills in the SDK - Claude Code Docs|Agent Skills in the SDK]]for full details.

[[Agent Skills in the SDK - Claude Code Docs|Agent Skills in the SDK]].

## Hooks

The SDK supports two ways to define hooks, and they run side by side:

- Filesystem hooks: shell commands defined in

  ```
  settings.json
  ```

  , loaded when

  ```
  settingSources
  ```

  includes the relevant source. These are the same hooks you’d configure for[[Automate workflows with hooks - Claude Code Docs|interactive Claude Code sessions]].
- Programmatic hooks: callback functions passed directly to

  ```
  query()
  ```

  . These run in your application process and can return structured decisions. See[[Intercept and control agent behavior with hooks - Claude Code Docs|Control execution with hooks]].

```
.claude/settings.json
```

and you set

```
settingSources: ["project"]
```

, those hooks run automatically in the SDK with no extra configuration.
Hook callbacks receive the tool input and return a decision dict. Returning

```
{}
```

(an empty dict) means allow the tool to proceed. Returning

```
{"decision": "block", "reason": "..."}
```

prevents execution and the reason is sent to Claude as the tool result. See the

[[Intercept and control agent behavior with hooks - Claude Code Docs|hooks guide]]for the full callback signature and return types.

### When to use which hook type

Hook typeBest forFilesystem (

```
settings.json
```

)Sharing hooks between CLI and SDK sessions. Supports

```
"command"
```

(shell scripts),

```
"http"
```

(POST to an endpoint),

```
"mcp_tool"
```

(call a connected MCP server’s tool),

```
"prompt"
```

(LLM evaluates a prompt), and

```
"agent"
```

(spawns a verifier agent). These fire in the main agent and any subagents it spawns.Programmatic (callbacks in

```
query()
```

)Application-specific logic; returning structured decisions; in-process integration. Scoped to the main session only.

The TypeScript SDK supports additional hook events beyond Python, including

```
SessionStart
```

,

```
SessionEnd
```

,

```
TeammateIdle
```

, and

```
TaskCompleted
```

. See the [[Intercept and control agent behavior with hooks - Claude Code Docs|hooks guide]]for the full event compatibility table.

[[Intercept and control agent behavior with hooks - Claude Code Docs|Control execution with hooks]]. For filesystem hook syntax, see

[[Hooks reference - Claude Code Docs|Hooks]].

## Choose the right feature

The Agent SDK gives you access to several ways to extend your agent’s behavior. If you’re unsure which to use, this table maps common goals to the right approach.

You want to…UseSDK surfaceSet project conventions your agent always follows

```
settingSources: ["project"]
```

loads it automatically[[Agent Skills in the SDK - Claude Code Docs|Skills]]

```
settingSources
```

+

```
allowedTools: ["Skill"]
```

[[Agent Skills in the SDK - Claude Code Docs|User-invocable skills]]

```
settingSources
```

+

```
allowedTools: ["Skill"]
```

[[Subagents in the SDK - Claude Code Docs|Subagents]]

```
agents
```

parameter +

```
allowedTools: ["Agent"]
```

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|Agent teams]][[Intercept and control agent behavior with hooks - Claude Code Docs|Hooks]]

```
hooks
```

parameter with callbacks, or shell scripts loaded via

```
settingSources
```

[[Connect to external tools with MCP - Claude Code Docs|MCP]]

```
mcpServers
```

parameter

[[Extend Claude Code - Claude Code Docs#Understand context costs|Extend Claude Code]].

## Related resources

- [[Extend Claude Code - Claude Code Docs|Extend Claude Code]]: Conceptual overview of all extension features, with comparison tables and context cost analysis
- [[Agent Skills in the SDK - Claude Code Docs|Skills in the SDK]]: Full guide to using skills programmatically
- [[Subagents in the SDK - Claude Code Docs|Subagents]]: Define and invoke subagents for isolated subtasks
- [[Intercept and control agent behavior with hooks - Claude Code Docs|Hooks]]: Intercept and control agent behavior at key execution points
- [[Configure permissions - Claude Code Docs-dbd6de|Permissions]]: Control tool access with modes, rules, and callbacks
- [[Modifying system prompts - Claude Code Docs|System prompts]]: Inject context without CLAUDE.md files

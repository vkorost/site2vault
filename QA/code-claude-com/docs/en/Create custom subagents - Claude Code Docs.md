---
title: Create custom subagents - Claude Code Docs
source_url: https://code.claude.com/docs/en/sub-agents
description: Create and use specialized AI subagents in Claude Code for task-specific
  workflows and improved context management.
---

[[Explore the context window - Claude Code Docs|context window visualization]]walks through a session where a subagent handles research in its own separate window.

If you need multiple agents working in parallel and communicating with each other, see

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|agent teams]]instead. Subagents work within a single session; agent teams coordinate across separate sessions.

- Preserve context by keeping exploration and implementation out of your main conversation
- Enforce constraints by limiting which tools a subagent can use
- Reuse configurations across projects with user-level subagents
- Specialize behavior with focused system prompts for specific domains
- Control costs by routing tasks to faster, cheaper models like Haiku

- [[Create custom subagents - Claude Code Docs#Built-in subagents|Built-in subagents]]
- [[Create custom subagents - Claude Code Docs#Quickstart: create your first subagent|How to create your own]]
- [[Create custom subagents - Claude Code Docs#Configure subagents|Full configuration options]]
- [[Create custom subagents - Claude Code Docs#Work with subagents|Patterns for working with subagents]]
- [[Create custom subagents - Claude Code Docs#Fork the current conversation|Forked subagents]]
- [[Create custom subagents - Claude Code Docs#Example subagents|Example subagents]]

## Built-in subagents

Claude Code includes built-in subagents that Claude automatically uses when appropriate. Each inherits the parent conversation’s permissions with additional tool restrictions.

- Explore
- Plan
- General-purpose
- Other

A fast, read-only agent optimized for searching and analyzing codebases.

- Model: Haiku (fast, low-latency)
- Tools: Read-only tools (denied access to Write and Edit tools)
- Purpose: File discovery, code search, codebase exploration

## Quickstart: create your first subagent

Subagents are defined in Markdown files with YAML frontmatter. You can

[[Create custom subagents - Claude Code Docs#Write subagent files|create them manually]]or use the

```
/agents
```

command.
This walkthrough guides you through creating a user-level subagent with the

```
/agents
```

command. The subagent reviews code and suggests improvements for the codebase.

Choose a location

Switch to the Library tab, select Create new agent, then choose Personal. This saves the subagent to

```
~/.claude/agents/
```

so it’s available in all your projects.

Generate with Claude

Select Generate with Claude. When prompted, describe the subagent:Claude generates the identifier, description, and system prompt for you.

Select tools

For a read-only reviewer, deselect everything except Read-only tools. If you keep all tools selected, the subagent inherits all tools available to the main conversation.

Select model

Choose which model the subagent uses. For this example agent, select Sonnet, which balances capability and speed for analyzing code patterns.

Choose a color

Pick a background color for the subagent. This helps you identify which subagent is running in the UI.

Configure memory

Select User scope to give the subagent a

[[Create custom subagents - Claude Code Docs#Enable persistent memory|persistent memory directory]]at

```
~/.claude/agent-memory/
```

. The subagent uses this to accumulate insights across conversations, such as codebase patterns and recurring issues. Select None if you don’t want the subagent to persist learnings.

## Configure subagents

### Use the /agents command

The

```
/agents
```

command opens a tabbed interface for managing subagents. The Running tab shows live subagents and lets you open or stop them. The Library tab lets you:

- View all available subagents (built-in, user, project, and plugin)
- Create new subagents with guided setup or Claude generation
- Edit existing subagent configuration and tool access
- Delete custom subagents
- See which subagents are active when duplicates exist

```
claude agents
```

. This shows agents grouped by source and indicates which are overridden by higher-priority definitions.

### Choose the subagent scope

Subagents are Markdown files with YAML frontmatter. Store them in different locations depending on scope. When multiple subagents share the same name, the higher-priority location wins.

LocationScopePriorityHow to createManaged settingsOrganization-wide1 (highest)Deployed via

```
--agents
```

CLI flag

```
.claude/agents/
```

```
~/.claude/agents/
```

```
agents/
```

directory[[Create plugins - Claude Code Docs|plugins]]

```
.claude/agents/
```

) are ideal for subagents specific to a codebase. Check them into version control so your team can use and improve them collaboratively.
Project subagents are discovered by walking up from the current working directory. Directories added with

```
--add-dir
```

[[Configure permissions - Claude Code Docs#Additional directories grant file access, not configuration|grant file access only]]and are not scanned for subagents. To share subagents across projects, use

```
~/.claude/agents/
```

or a

[[Create plugins - Claude Code Docs|plugin]]. User subagents (

```
~/.claude/agents/
```

) are personal subagents available in all your projects.
CLI-defined subagents are passed as JSON when launching Claude Code. They exist only for that session and aren’t saved to disk, making them useful for quick testing or automation scripts. You can define multiple subagents in a single

```
--agents
```

call:

```
--agents
```

flag accepts JSON with the same

[[Create custom subagents - Claude Code Docs#Supported frontmatter fields|frontmatter]]fields as file-based subagents:

```
description
```

,

```
prompt
```

,

```
tools
```

,

```
disallowedTools
```

,

```
model
```

,

```
permissionMode
```

,

```
mcpServers
```

,

```
hooks
```

,

```
maxTurns
```

,

```
skills
```

,

```
initialPrompt
```

,

```
memory
```

,

```
effort
```

,

```
background
```

,

```
isolation
```

, and

```
color
```

. Use

```
prompt
```

for the system prompt, equivalent to the markdown body in file-based subagents.
Managed subagents are deployed by organization administrators. Place markdown files in

```
.claude/agents/
```

inside the

[[Claude Code settings - Claude Code Docs#Settings files|managed settings directory]], using the same frontmatter format as project and user subagents. Managed definitions take precedence over project and user subagents with the same name. Plugin subagents come from

[[Create plugins - Claude Code Docs|plugins]]you’ve installed. They appear in

```
/agents
```

alongside your custom subagents. See the

[[Plugins reference - Claude Code Docs#Agents|plugin components reference]]for details on creating plugin subagents.

For security reasons, plugin subagents do not support the

```
hooks
```

,

```
mcpServers
```

, or

```
permissionMode
```

frontmatter fields. These fields are ignored when loading agents from a plugin. If you need them, copy the agent file into

```
.claude/agents/
```

or

```
~/.claude/agents/
```

. You can also add rules to [[Claude Code settings - Claude Code Docs#Permission settings|in]]

```
permissions.allow
```

```
settings.json
```

or

```
settings.local.json
```

, but these rules apply to the entire session, not just the plugin subagent.

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Use subagent definitions for teammates|agent teams]]: when spawning a teammate, you can reference a subagent type and the teammate uses its

```
tools
```

and

```
model
```

, with the definition’s body appended to the teammate’s system prompt as additional instructions. See

[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Use subagent definitions for teammates|agent teams]]for which frontmatter fields apply on that path.

### Write subagent files

Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown:

Subagents are loaded at session start. If you create a subagent by manually adding a file, restart your session or use

```
/agents
```

to load it immediately.

```
cd
```

commands do not persist between Bash or PowerShell tool calls and do not affect the main conversation’s working directory. To give the subagent an isolated copy of the repository instead, set

[[Create custom subagents - Claude Code Docs#Supported frontmatter fields|.]]

```
isolation: worktree
```

#### Supported frontmatter fields

The following fields can be used in the YAML frontmatter. Only

```
name
```

and

```
description
```

are required.

FieldRequiredDescription

```
name
```

YesUnique identifier using lowercase letters and hyphens

```
description
```

YesWhen Claude should delegate to this subagent

```
tools
```

No

```
disallowedTools
```

```
model
```

[[Create custom subagents - Claude Code Docs#Choose a model|Model]]to use:

```
sonnet
```

,

```
opus
```

,

```
haiku
```

, a full model ID (for example,

```
claude-opus-4-7
```

), or

```
inherit
```

. Defaults to

```
inherit
```

```
permissionMode
```

[[Create custom subagents - Claude Code Docs#Permission modes|Permission mode]]:

```
default
```

,

```
acceptEdits
```

,

```
auto
```

,

```
dontAsk
```

,

```
bypassPermissions
```

, or

```
plan
```

```
maxTurns
```

```
skills
```

[[Extend Claude with skills - Claude Code Docs|Skills]]to load into the subagent’s context at startup. The full skill content is injected, not just made available for invocation. Subagents don’t inherit skills from the parent conversation

```
mcpServers
```

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP servers]]available to this subagent. Each entry is either a server name referencing an already-configured server (e.g.,

```
"slack"
```

) or an inline definition with the server name as key and a full [[Connect Claude Code to tools via MCP - Claude Code Docs#Installing MCP servers|MCP server config]]as value

```
hooks
```

[[Create custom subagents - Claude Code Docs#Define hooks for subagents|Lifecycle hooks]]scoped to this subagent

```
memory
```

[[Create custom subagents - Claude Code Docs#Enable persistent memory|Persistent memory scope]]:

```
user
```

,

```
project
```

, or

```
local
```

. Enables cross-session learning

```
background
```

```
true
```

to always run this subagent as a [[Create custom subagents - Claude Code Docs#Run subagents in foreground or background|background task]]. Default:

```
false
```

```
effort
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

,

```
max
```

; available levels depend on the model

```
isolation
```

```
worktree
```

to run the subagent in a temporary [[Common workflows - Claude Code Docs#Run parallel Claude Code sessions with Git worktrees|git worktree]], giving it an isolated copy of the repository. The worktree is automatically cleaned up if the subagent makes no changes

```
color
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

, or

```
cyan
```

```
initialPrompt
```

```
--agent
```

or the

```
agent
```

setting). [[Commands - Claude Code Docs|Commands]]and[[Extend Claude with skills - Claude Code Docs|skills]]are processed. Prepended to any user-provided prompt

### Choose a model

The

```
model
```

field controls which

[[Model configuration - Claude Code Docs|AI model]]the subagent uses:

- Model alias: Use one of the available aliases:

  ```
  sonnet
  ```

  ,

  ```
  opus
  ```

  , or

  ```
  haiku
  ```
- Full model ID: Use a full model ID such as

  ```
  claude-opus-4-7
  ```

  or

  ```
  claude-sonnet-4-6
  ```

  . Accepts the same values as the

  ```
  --model
  ```

  flag
- inherit: Use the same model as the main conversation
- Omitted: If not specified, defaults to

  ```
  inherit
  ```

  (uses the same model as the main conversation)

```
model
```

parameter for that specific invocation. Claude Code resolves the subagent’s model in this order:

- The environment variable, if set

  ```
  CLAUDE_CODE_SUBAGENT_MODEL
  ```
- The per-invocation

  ```
  model
  ```

  parameter
- The subagent definition’s

  ```
  model
  ```

  frontmatter
- The main conversation’s model

### Control subagent capabilities

You can control what subagents can do through tool access, permission modes, and conditional rules.

#### Available tools

Subagents can use any of Claude Code’s

[[Tools reference - Claude Code Docs|internal tools]]. By default, subagents inherit all tools from the main conversation, including MCP tools. To restrict tools, use either the

```
tools
```

field (allowlist) or the

```
disallowedTools
```

field (denylist). This example uses

```
tools
```

to exclusively allow Read, Grep, Glob, and Bash. The subagent can’t edit files, write files, or use any MCP tools:

```
disallowedTools
```

to inherit every tool from the main conversation except Write and Edit. The subagent keeps Bash, MCP tools, and everything else:

```
disallowedTools
```

is applied first, then

```
tools
```

is resolved against the remaining pool. A tool listed in both is removed.

#### Restrict which subagents can be spawned

When an agent runs as the main thread with

```
claude --agent
```

, it can spawn subagents using the Agent tool. To restrict which subagent types it can spawn, use

```
Agent(agent_type)
```

syntax in the

```
tools
```

field.

In version 2.1.63, the Task tool was renamed to Agent. Existing

```
Task(...)
```

references in settings and agent definitions still work as aliases.

```
worker
```

and

```
researcher
```

subagents can be spawned. If the agent tries to spawn any other type, the request fails and the agent sees only the allowed types in its prompt. To block specific agents while allowing all others, use

[[Create custom subagents - Claude Code Docs#Disable specific subagents|instead. To allow spawning any subagent without restrictions, use]]

```
permissions.deny
```

```
Agent
```

without parentheses:

```
Agent
```

is omitted from the

```
tools
```

list entirely, the agent cannot spawn any subagents. This restriction only applies to agents running as the main thread with

```
claude --agent
```

. Subagents cannot spawn other subagents, so

```
Agent(agent_type)
```

has no effect in subagent definitions.

#### Scope MCP servers to a subagent

Use the

```
mcpServers
```

field to give a subagent access to

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP]]servers that aren’t available in the main conversation. Inline servers defined here are connected when the subagent starts and disconnected when it finishes. String references share the parent session’s connection.

The

```
mcpServers
```

field applies in both contexts where an agent file can run:

- As a subagent, spawned through the Agent tool or an @-mention
- As the main session, launched with or the

  ```
  --agent
  ```

  ```
  agent
  ```

  setting

[[Connect Claude Code to tools via MCP - Claude Code Docs|and settings files.]]

```
.mcp.json
```

```
.mcp.json
```

server entries (

```
stdio
```

,

```
http
```

,

```
sse
```

,

```
ws
```

), keyed by the server name.
To keep an MCP server out of the main conversation entirely and avoid its tool descriptions consuming context there, define it inline here rather than in

```
.mcp.json
```

. The subagent gets the tools; the parent conversation does not.

#### Permission modes

The

```
permissionMode
```

field controls how the subagent handles permission prompts. Subagents inherit the permission context from the main conversation and can override the mode, except when the parent mode takes precedence as described below.

ModeBehavior

```
default
```

Standard permission checking with prompts

```
acceptEdits
```

Auto-accept file edits and common filesystem commands for paths in the working directory or

```
additionalDirectories
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

```
plan
```

```
bypassPermissions
```

or

```
acceptEdits
```

, this takes precedence and cannot be overridden. If the parent uses

[[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|auto mode]], the subagent inherits auto mode and any

```
permissionMode
```

in its frontmatter is ignored: the classifier evaluates the subagent’s tool calls with the same block and allow rules as the parent session.

#### Preload skills into subagents

Use the

```
skills
```

field to inject skill content into a subagent’s context at startup. This gives the subagent domain knowledge without requiring it to discover and load skills during execution.

[[Extend Claude with skills - Claude Code Docs#Control who invokes a skill|, since preloading draws from the same set of skills Claude can invoke. If a listed skill is missing or disabled, Claude Code skips it and logs a warning to the debug log.]]

```
disable-model-invocation: true
```

This is the inverse of

[[Extend Claude with skills - Claude Code Docs#Run skills in a subagent|running a skill in a subagent]]. With

```
skills
```

in a subagent, the subagent controls the system prompt and loads skill content. With

```
context: fork
```

in a skill, the skill content is injected into the agent you specify. Both use the same underlying system.

#### Enable persistent memory

The

```
memory
```

field gives the subagent a persistent directory that survives across conversations. The subagent uses this directory to build up knowledge over time, such as codebase patterns, debugging insights, and architectural decisions.

ScopeLocationUse when

```
user
```

```
~/.claude/agent-memory/<name-of-agent>/
```

the subagent should remember learnings across all projects

```
project
```

```
.claude/agent-memory/<name-of-agent>/
```

the subagent’s knowledge is project-specific and shareable via version control

```
local
```

```
.claude/agent-memory-local/<name-of-agent>/
```

the subagent’s knowledge is project-specific but should not be checked into version control

- The subagent’s system prompt includes instructions for reading and writing to the memory directory.
- The subagent’s system prompt also includes the first 200 lines or 25KB of

  ```
  MEMORY.md
  ```

  in the memory directory, whichever comes first, with instructions to curate

  ```
  MEMORY.md
  ```

  if it exceeds that limit.
- Read, Write, and Edit tools are automatically enabled so the subagent can manage its memory files.

##### Persistent memory tips

- ```
  project
  ```

  is the recommended default scope. It makes subagent knowledge shareable via version control. Use

  ```
  user
  ```

  when the subagent’s knowledge is broadly applicable across projects, or

  ```
  local
  ```

  when the knowledge should not be checked into version control.
- Ask the subagent to consult its memory before starting work: “Review this PR, and check your memory for patterns you’ve seen before.”
- Ask the subagent to update its memory after completing a task: “Now that you’re done, save what you learned to your memory.” Over time, this builds a knowledge base that makes the subagent more effective.
- Include memory instructions directly in the subagent’s markdown file so it proactively maintains its own knowledge base:

#### Conditional rules with hooks

For more dynamic control over tool usage, use

```
PreToolUse
```

hooks to validate operations before they execute. This is useful when you need to allow some operations of a tool while blocking others.
This example creates a subagent that only allows read-only database queries. The

```
PreToolUse
```

hook runs the script specified in

```
command
```

before each Bash command executes:

[[Hooks reference - Claude Code Docs#PreToolUse input|passes hook input as JSON]]via stdin to hook commands. The validation script reads this JSON, extracts the Bash command, and

[[Hooks reference - Claude Code Docs#Exit code 2 behavior per event|exits with code 2]]to block write operations:

[[Hooks reference - Claude Code Docs#PreToolUse input|Hook input]]for the complete input schema and

[[Hooks reference - Claude Code Docs#Exit code output|exit codes]]for how exit codes affect behavior.

#### Disable specific subagents

You can prevent Claude from using specific subagents by adding them to the

```
deny
```

array in your

[[Claude Code settings - Claude Code Docs#Permission settings|settings]]. Use the format

```
Agent(subagent-name)
```

where

```
subagent-name
```

matches the subagent’s name field.

```
--disallowedTools
```

CLI flag:

[[Configure permissions - Claude Code Docs#Tool-specific permission rules|Permissions documentation]]for more details on permission rules.

### Define hooks for subagents

Subagents can define

[[Hooks reference - Claude Code Docs|hooks]]that run during the subagent’s lifecycle. There are two ways to configure hooks:

- In the subagent’s frontmatter: Define hooks that run only while that subagent is active
- In

  ```
  settings.json
  ```

  : Define hooks that run in the main session when subagents start or stop

#### Hooks in subagent frontmatter

Define hooks directly in the subagent’s markdown file. These hooks only run while that specific subagent is active and are cleaned up when it finishes.

Frontmatter hooks fire when the agent is spawned as a subagent through the Agent tool or an @-mention, and when the agent runs as the main session via

[[Create custom subagents - Claude Code Docs#Invoke subagents explicitly|or the]]

```
--agent
```

```
agent
```

setting. In the main-session case they run alongside any hooks defined in [[Hooks reference - Claude Code Docs|.]]

```
settings.json
```

[[Hooks reference - Claude Code Docs#Hook events|hook events]]are supported. The most common events for subagents are:

EventMatcher inputWhen it fires

```
PreToolUse
```

Tool nameBefore the subagent uses a tool

```
PostToolUse
```

Tool nameAfter the subagent uses a tool

```
Stop
```

(none)When the subagent finishes (converted to

```
SubagentStop
```

at runtime)

```
PreToolUse
```

hook and runs a linter after file edits with

```
PostToolUse
```

:

```
Stop
```

hooks in frontmatter are automatically converted to

```
SubagentStop
```

events.

#### Project-level hooks for subagent events

Configure hooks in

```
settings.json
```

that respond to subagent lifecycle events in the main session.

EventMatcher inputWhen it fires

```
SubagentStart
```

Agent type nameWhen a subagent begins execution

```
SubagentStop
```

Agent type nameWhen a subagent completes

```
db-agent
```

subagent starts, and a cleanup script when any subagent stops:

[[Hooks reference - Claude Code Docs|Hooks]]for the complete hook configuration format.

## Work with subagents

### Understand automatic delegation

Claude automatically delegates tasks based on the task description in your request, the

```
description
```

field in subagent configurations, and current context. To encourage proactive delegation, include phrases like “use proactively” in your subagent’s description field.

### Invoke subagents explicitly

When automatic delegation isn’t enough, you can request a subagent yourself. Three patterns escalate from a one-off suggestion to a session-wide default:

- Natural language: name the subagent in your prompt; Claude decides whether to delegate
- @-mention: guarantees the subagent runs for one task
- Session-wide: the whole session uses that subagent’s system prompt, tool restrictions, and model via the

  ```
  --agent
  ```

  flag or the

  ```
  agent
  ```

  setting

```
@
```

and pick the subagent from the typeahead, the same way you @-mention files. This ensures that specific subagent runs rather than leaving the choice to Claude:

[[Create plugins - Claude Code Docs|plugin]]appear in the typeahead as

```
<plugin-name>:<agent-name>
```

. Named background subagents currently running in the session also appear in the typeahead, showing their status next to the name. You can also type the mention manually without using the picker:

```
@agent-<name>
```

for local subagents, or

```
@agent-<plugin-name>:<agent-name>
```

for plugin subagents.
Run the whole session as a subagent. Pass

[[CLI reference - Claude Code Docs|to start a session where the main thread itself takes on that subagent’s system prompt, tool restrictions, and model:]]

```
--agent <name>
```

[[CLI reference - Claude Code Docs|does.]]

```
--system-prompt
```

```
CLAUDE.md
```

files and project memory still load through the normal message flow. The agent name appears as

```
@<name>
```

in the startup header so you can confirm it’s active.
This works with built-in and custom subagents, and the choice persists when you resume the session.
For a plugin-provided subagent, pass the scoped name:

```
claude --agent <plugin-name>:<agent-name>
```

.
To make it the default for every session in a project, set

```
agent
```

in

```
.claude/settings.json
```

:

### Run subagents in foreground or background

Subagents can run in the foreground (blocking) or background (concurrent):

- Foreground subagents block the main conversation until complete. Permission prompts and clarifying questions (like ) are passed through to you.

  ```
  AskUserQuestion
  ```
- Background subagents run concurrently while you continue working. Before launching, Claude Code prompts for any tool permissions the subagent will need, ensuring it has the necessary approvals upfront. Once running, the subagent inherits these permissions and auto-denies anything not pre-approved. If a background subagent needs to ask clarifying questions, that tool call fails but the subagent continues.

- Ask Claude to “run this in the background”
- Press Ctrl+B to background a running task

```
CLAUDE_CODE_DISABLE_BACKGROUND_TASKS
```

environment variable to

```
1
```

. See

[[Environment variables - Claude Code Docs|Environment variables]]. When

[[Create custom subagents - Claude Code Docs#Fork the current conversation|fork mode]]is enabled, every subagent spawn runs in the background regardless of the

```
background
```

field. Forks still surface permission prompts in your terminal as they occur instead of pre-approving; named subagents follow the pre-approval flow above.

### Common patterns

#### Isolate high-volume operations

One of the most effective uses for subagents is isolating operations that produce large amounts of output. Running tests, fetching documentation, or processing log files can consume significant context. By delegating these to a subagent, the verbose output stays in the subagent’s context while only the relevant summary returns to your main conversation.

#### Run parallel research

For independent investigations, spawn multiple subagents to work simultaneously:

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|agent teams]]give each worker its own independent context.

#### Chain subagents

For multi-step workflows, ask Claude to use subagents in sequence. Each subagent completes its task and returns results to Claude, which then passes relevant context to the next subagent.

### Choose between subagents and main conversation

Use the main conversation when:

- The task needs frequent back-and-forth or iterative refinement
- Multiple phases share significant context (planning → implementation → testing)
- You’re making a quick, targeted change
- Latency matters. Subagents start fresh and may need time to gather context

- The task produces verbose output you don’t need in your main context
- You want to enforce specific tool restrictions or permissions
- The work is self-contained and can return a summary

[[Extend Claude with skills - Claude Code Docs|Skills]]instead when you want reusable prompts or workflows that run in the main conversation context rather than isolated subagent context. For a quick question about something already in your conversation, use

[[Interactive mode - Claude Code Docs|instead of a subagent. It sees your full context but has no tool access, and the answer is discarded rather than added to history.]]

```
/btw
```

Subagents cannot spawn other subagents. If your workflow requires nested delegation, use

[[Extend Claude with skills - Claude Code Docs|Skills]]or[[Create custom subagents - Claude Code Docs#Chain subagents|chain subagents]]from the main conversation.

### Manage subagent context

#### Resume subagents

Each subagent invocation creates a new instance with fresh context. To continue an existing subagent’s work instead of starting over, ask Claude to resume it. Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh. When a subagent completes, Claude receives its agent ID. Claude uses the

```
SendMessage
```

tool with the agent’s ID as the

```
to
```

field to resume it. The

```
SendMessage
```

tool is only available when

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|agent teams]]are enabled via

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

.
To resume a subagent, ask Claude to continue the previous work:

```
SendMessage
```

, it auto-resumes in the background without requiring a new

```
Agent
```

invocation.
You can also ask Claude for the agent ID if you want to reference it explicitly, or find IDs in the transcript files at

```
~/.claude/projects/{project}/{sessionId}/subagents/
```

. Each transcript is stored as

```
agent-{agentId}.jsonl
```

.
Subagent transcripts persist independently of the main conversation:

- Main conversation compaction: When the main conversation compacts, subagent transcripts are unaffected. They’re stored in separate files.
- Session persistence: Subagent transcripts persist within their session. You can [[Create custom subagents - Claude Code Docs#Resume subagents|resume a subagent]]after restarting Claude Code by resuming the same session.
- Automatic cleanup: Transcripts are cleaned up based on the

  ```
  cleanupPeriodDays
  ```

  setting (default: 30 days).

#### Auto-compaction

Subagents support automatic compaction using the same logic as the main conversation. By default, auto-compaction triggers at approximately 95% capacity. To trigger compaction earlier, set

```
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE
```

to a lower percentage (for example,

```
50
```

). See

[[Environment variables - Claude Code Docs|environment variables]]for details. Compaction events are logged in subagent transcript files:

```
preTokens
```

value shows how many tokens were used before compaction occurred.

## Fork the current conversation

Forked subagents are experimental and require Claude Code v2.1.117 or later. Behavior and configuration may change in future releases. Enable them by setting the

[[Environment variables - Claude Code Docs|environment variable to]]

```
CLAUDE_CODE_FORK_SUBAGENT
```

```
1
```

.

- Claude spawns a fork whenever it would otherwise use the [[Create custom subagents - Claude Code Docs#Built-in subagents|general-purpose]]subagent. Named subagents such as Explore still spawn as before.
- Every subagent spawn runs in the [[Create custom subagents - Claude Code Docs#Run subagents in foreground or background|background]], whether it is a fork or a named subagent. Set

  ```
  CLAUDE_CODE_DISABLE_BACKGROUND_TASKS
  ```

  to

  ```
  1
  ```

  to keep spawns synchronous.
- The

  ```
  /fork
  ```

  command spawns a fork instead of acting as an alias for.

  ```
  /branch
  ```

```
/fork
```

followed by a directive. Claude Code names the fork from the first words of the directive. The following example forks the conversation to draft test cases while you continue with the implementation in the main session:

### Observe and steer running forks

Running forks appear in a panel below the prompt input, with one row for the main session and one for each fork. Use these keys to interact with the panel:

KeyAction

```
↑
```

/

```
↓
```

Move between rows

```
Enter
```

Open the selected fork’s transcript and send it follow-up messages

```
x
```

Dismiss a finished fork or stop a running one

```
Esc
```

Return focus to the prompt input

### How forks differ from named subagents

A fork inherits everything the main session has at the moment it spawns. A named subagent starts from its own definition.

ForkNamed subagentContextFull conversation historyFresh context with the prompt you passSystem prompt and toolsSame as main sessionFrom the subagent’s

```
model
```

field[[Create custom subagents - Claude Code Docs#Run subagents in foreground or background|Pre-approved]]before launch, then auto-denied

```
isolation: "worktree"
```

so the fork’s file edits are written to a separate git worktree instead of your checkout.

### Limitations

Fork mode works only in interactive sessions. It is disabled in

[[Run Claude Code programmatically - Claude Code Docs|non-interactive mode]], which includes the Agent SDK. A fork cannot spawn further forks.

## Example subagents

These examples demonstrate effective patterns for building subagents. Use them as starting points, or generate a customized version with Claude.

### Code reviewer

A read-only subagent that reviews code without modifying it. This example shows how to design a focused subagent with limited tool access (no Edit or Write) and a detailed prompt that specifies exactly what to look for and how to format output.

### Debugger

A subagent that can both analyze and fix issues. Unlike the code reviewer, this one includes Edit because fixing bugs requires modifying code. The prompt provides a clear workflow from diagnosis to verification.

### Data scientist

A domain-specific subagent for data analysis work. This example shows how to create subagents for specialized workflows outside of typical coding tasks. It explicitly sets

```
model: sonnet
```

for more capable analysis.

### Database query validator

A subagent that allows Bash access but validates commands to permit only read-only SQL queries. This example shows how to use

```
PreToolUse
```

hooks for conditional validation when you need finer control than the

```
tools
```

field provides.

[[Hooks reference - Claude Code Docs#PreToolUse input|passes hook input as JSON]]via stdin to hook commands. The validation script reads this JSON, extracts the command being executed, and checks it against a list of SQL write operations. If a write operation is detected, the script

[[Hooks reference - Claude Code Docs#Exit code 2 behavior per event|exits with code 2]]to block execution and returns an error message to Claude via stderr. Create the validation script anywhere in your project. The path must match the

```
command
```

field in your hook configuration:

```
tool_input.command
```

. Exit code 2 blocks the operation and feeds the error message back to Claude. See

[[Hooks reference - Claude Code Docs#Exit code output|Hooks]]for details on exit codes and

[[Hooks reference - Claude Code Docs#PreToolUse input|Hook input]]for the complete input schema.

## Next steps

Now that you understand subagents, explore these related features:

- [[Create plugins - Claude Code Docs|Distribute subagents with plugins]]to share subagents across teams or projects
- [[Run Claude Code programmatically - Claude Code Docs|Run Claude Code programmatically]]with the Agent SDK for CI/CD and automation
- [[Connect Claude Code to tools via MCP - Claude Code Docs|Use MCP servers]]to give subagents access to external tools and data

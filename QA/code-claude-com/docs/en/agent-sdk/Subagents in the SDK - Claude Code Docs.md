---
title: Subagents in the SDK - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/subagents
description: Define and invoke subagents to isolate context, run tasks in parallel,
  and apply specialized instructions in your Claude Agent SDK applications.
---

```
agents
```

parameter.

## Overview

You can create subagents in three ways:

- Programmatically: use the

  ```
  agents
  ```

  parameter in your

  ```
  query()
  ```

  options ([[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript]],[[Agent SDK reference - Python - Claude Code Docs|Python]])
- Filesystem-based: define agents as markdown files in

  ```
  .claude/agents/
  ```

  directories (see[[Create custom subagents - Claude Code Docs|defining subagents as files]])
- Built-in general-purpose: Claude can invoke the built-in

  ```
  general-purpose
  ```

  subagent at any time via the Agent tool without you defining anything

```
description
```

field. Write clear descriptions that explain when the subagent should be used, and Claude will automatically delegate appropriate tasks. You can also explicitly request a subagent by name in your prompt (for example, “Use the code-reviewer agent to…”).

## Benefits of using subagents

### Context isolation

Each subagent runs in its own fresh conversation. Intermediate tool calls and results stay inside the subagent; only its final message returns to the parent. See

[[Subagents in the SDK - Claude Code Docs#What subagents inherit|What subagents inherit]]for exactly what’s in the subagent’s context. Example: a

```
research-assistant
```

subagent can explore dozens of files without any of that content accumulating in the main conversation. The parent receives a concise summary, not every file the subagent read.

### Parallelization

Multiple subagents can run concurrently, dramatically speeding up complex workflows. Example: during a code review, you can run

```
style-checker
```

,

```
security-scanner
```

, and

```
test-coverage
```

subagents simultaneously, reducing review time from minutes to seconds.

### Specialized instructions and knowledge

Each subagent can have tailored system prompts with specific expertise, best practices, and constraints. Example: a

```
database-migration
```

subagent can have detailed knowledge about SQL best practices, rollback strategies, and data integrity checks that would be unnecessary noise in the main agent’s instructions.

### Tool restrictions

Subagents can be limited to specific tools, reducing the risk of unintended actions. Example: a

```
doc-reviewer
```

subagent might only have access to Read and Grep tools, ensuring it can analyze but never accidentally modify your documentation files.

## Creating subagents

### Programmatic definition (recommended)

Define subagents directly in your code using the

```
agents
```

parameter. This example creates two subagents: a code reviewer with read-only access and a test runner that can execute commands. The

```
Agent
```

tool must be included in

```
allowedTools
```

since Claude invokes subagents through the Agent tool.

### AgentDefinition configuration

FieldTypeRequiredDescription

```
description
```

```
string
```

YesNatural language description of when to use this agent

```
prompt
```

```
string
```

YesThe agent’s system prompt defining its role and behavior

```
tools
```

```
string[]
```

NoArray of allowed tool names. If omitted, inherits all tools

```
disallowedTools
```

```
string[]
```

NoArray of tool names to remove from the agent’s tool set

```
model
```

```
string
```

NoModel override for this agent. Accepts an alias such as

```
'sonnet'
```

,

```
'opus'
```

,

```
'haiku'
```

,

```
'inherit'
```

, or a full model ID. Defaults to main model if omitted

```
skills
```

```
string[]
```

NoList of skill names available to this agent

```
memory
```

```
'user' | 'project' | 'local'
```

NoMemory source for this agent

```
mcpServers
```

```
(string | object)[]
```

NoMCP servers available to this agent, by name or inline config

```
maxTurns
```

```
number
```

NoMaximum number of agentic turns before the agent stops

```
background
```

```
boolean
```

NoRun this agent as a non-blocking background task when invoked

```
effort
```

```
'low' | 'medium' | 'high' | 'xhigh' | 'max' | number
```

NoReasoning effort level for this agent

```
permissionMode
```

```
PermissionMode
```

NoPermission mode for tool execution within this agent

[[Agent SDK reference - Python - Claude Code Docs|for details.]]

```
AgentDefinition
```

reference

Subagents cannot spawn their own subagents. Don’t include

```
Agent
```

in a subagent’s

```
tools
```

array.

### Filesystem-based definition (alternative)

You can also define subagents as markdown files in

```
.claude/agents/
```

directories. See the

[[Create custom subagents - Claude Code Docs|Claude Code subagents documentation]]for details on this approach. Programmatically defined agents take precedence over filesystem-based agents with the same name.

Even without defining custom subagents, Claude can spawn the built-in

```
general-purpose
```

subagent when

```
Agent
```

is in your

```
allowedTools
```

. This is useful for delegating research or exploration tasks without creating specialized agents.

## What subagents inherit

A subagent’s context window starts fresh (no parent conversation) but isn’t empty. The only channel from parent to subagent is the Agent tool’s prompt string, so include any file paths, error messages, or decisions the subagent needs directly in that prompt.

The subagent receivesThe subagent does not receiveIts own system prompt (

```
AgentDefinition.prompt
```

) and the Agent tool’s promptThe parent’s conversation history or tool resultsProject CLAUDE.md (loaded via

```
settingSources
```

)Skills (unless listed in

```
AgentDefinition.skills
```

)Tool definitions (inherited from parent, or the subset in

```
tools
```

)The parent’s system prompt

The parent receives the subagent’s final message verbatim as the Agent tool result, but may summarize it in its own response. To preserve subagent output verbatim in the user-facing response, include an instruction to do so in the prompt or

```
systemPrompt
```

option you pass to the main

```
query()
```

call.

## Invoking subagents

### Automatic invocation

Claude automatically decides when to invoke subagents based on the task and each subagent’s

```
description
```

. For example, if you define a

```
performance-optimizer
```

subagent with the description “Performance optimization specialist for query tuning”, Claude will invoke it when your prompt mentions optimizing queries.
Write clear, specific descriptions so Claude can match tasks to the right subagent.

### Explicit invocation

To guarantee Claude uses a specific subagent, mention it by name in your prompt:

### Dynamic agent configuration

You can create agent definitions dynamically based on runtime conditions. This example creates a security reviewer with different strictness levels, using a more powerful model for strict reviews.

## Detecting subagent invocation

Subagents are invoked via the Agent tool. To detect when a subagent is invoked, check for

```
tool_use
```

blocks where

```
name
```

is

```
"Agent"
```

. Messages from within a subagent’s context include a

```
parent_tool_use_id
```

field.

The tool name was renamed from

```
"Task"
```

to

```
"Agent"
```

in Claude Code v2.1.63. Current SDK releases emit

```
"Agent"
```

in

```
tool_use
```

blocks but still use

```
"Task"
```

in the

```
system:init
```

tools list and in

```
result.permission_denials[].tool_name
```

. Checking both values in

```
block.name
```

ensures compatibility across SDK versions.

The message structure differs between SDKs. In Python, content blocks are accessed directly via

```
message.content
```

. In TypeScript,

```
SDKAssistantMessage
```

wraps the Claude API message, so content is accessed via

```
message.message.content
```

.

## Resuming subagents

Subagents can be resumed to continue where they left off. Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh. When a subagent completes, Claude receives its agent ID in the Agent tool result. To resume a subagent programmatically:

- Capture the session ID: Extract

  ```
  session_id
  ```

  from messages during the first query
- Extract the agent ID: Parse

  ```
  agentId
  ```

  from the message content
- Resume the session: Pass

  ```
  resume: sessionId
  ```

  in the second query’s options, and include the agent ID in your prompt

You must resume the same session to access the subagent’s transcript. Each

```
query()
```

call starts a new session by default, so pass

```
resume: sessionId
```

to continue in the same session.If you’re using a custom agent (not a built-in one), you also need to pass the same agent definition in the

```
agents
```

parameter for both queries.

- Main conversation compaction: When the main conversation compacts, subagent transcripts are unaffected. They’re stored in separate files.
- Session persistence: Subagent transcripts persist within their session. You can resume a subagent after restarting Claude Code by resuming the same session.
- Automatic cleanup: Transcripts are cleaned up based on the

  ```
  cleanupPeriodDays
  ```

  setting (default: 30 days).

## Tool restrictions

Subagents can have restricted tool access via the

```
tools
```

field:

- Omit the field: agent inherits all available tools (default)
- Specify tools: agent can only use listed tools

### Common tool combinations

Use caseToolsDescriptionRead-only analysis

```
Read
```

,

```
Grep
```

,

```
Glob
```

Can examine code but not modify or executeTest execution

```
Bash
```

,

```
Read
```

,

```
Grep
```

Can run commands and analyze outputCode modification

```
Read
```

,

```
Edit
```

,

```
Write
```

,

```
Grep
```

,

```
Glob
```

Full read/write access without command executionFull accessAll toolsInherits all tools from parent (omit

```
tools
```

field)

## Troubleshooting

### Claude not delegating to subagents

If Claude completes tasks directly instead of delegating to your subagent:

- Include the Agent tool: subagents are invoked via the Agent tool, so it must be in

  ```
  allowedTools
  ```
- Use explicit prompting: mention the subagent by name in your prompt (for example, “Use the code-reviewer agent to…”)
- Write a clear description: explain exactly when the subagent should be used so Claude can match tasks appropriately

### Filesystem-based agents not loading

Agents defined in

```
.claude/agents/
```

are loaded at startup only. If you create a new agent file while Claude Code is running, restart the session to load it.

### Windows: long prompt failures

On Windows, subagents with very long prompts may fail due to command line length limits (8191 chars). Keep prompts concise or use filesystem-based agents for complex instructions.

## Related documentation

- [[Create custom subagents - Claude Code Docs|Claude Code subagents]]: comprehensive subagent documentation including filesystem-based definitions
- [[Agent SDK overview - Claude Code Docs|SDK overview]]: getting started with the Claude Agent SDK

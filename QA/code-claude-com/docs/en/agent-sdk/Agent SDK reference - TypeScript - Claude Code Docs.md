---
title: Agent SDK reference - TypeScript - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/typescript
description: Complete API reference for the TypeScript Agent SDK, including all functions,
  types, and interfaces.
---

Try the new V2 interface (preview): A simplified interface with

```
send()
```

and

```
stream()
```

patterns is now available, making multi-turn conversations easier. [Learn more about the TypeScript V2 preview](https://code.claude.com/docs/en/agent-sdk/typescript-v2-preview)

## Installation

The SDK bundles a native Claude Code binary for your platform as an optional dependency such as

```
@anthropic-ai/claude-agent-sdk-darwin-arm64
```

. You don’t need to install Claude Code separately. If your package manager skips optional dependencies, the SDK throws

```
Native CLI binary for <platform> not found
```

; set [[Agent SDK reference - TypeScript - Claude Code Docs#Options|to a separately installed]]

```
pathToClaudeCodeExecutable
```

```
claude
```

binary instead.

## Functions

### ``` query() ```

The primary function for interacting with Claude Code. Creates an async generator that streams messages as they arrive.

#### Parameters

ParameterTypeDescription

```
prompt
```

```
string | AsyncIterable<
```

```
SDKUserMessage
```

The input prompt as a string or async iterable for streaming mode

```
options
```

```
Options
```

#### Returns

Returns a

[[Agent SDK reference - TypeScript - Claude Code Docs|object that extends]]

```
Query
```

```
AsyncGenerator<
```

```
SDKMessage
```

```
, void>
```

with additional methods.

### ``` startup() ```

Pre-warms the CLI subprocess by spawning it and completing the initialize handshake before a prompt is available. The returned

[[Agent SDK reference - TypeScript - Claude Code Docs|handle accepts a prompt later and writes it to an already-ready process, so the first]]

```
WarmQuery
```

```
query()
```

call resolves without paying subprocess spawn and initialization cost inline.

#### Parameters

ParameterTypeDescription

```
options
```

```
Options
```

```
options
```

parameter to

```
query()
```

```
initializeTimeoutMs
```

```
number
```

```
60000
```

. If initialization does not complete in time, the promise rejects with a timeout error

#### Returns

Returns a

```
Promise<
```

```
WarmQuery
```

```
>
```

that resolves once the subprocess has spawned and completed its initialize handshake.

#### Example

Call

```
startup()
```

early, for example on application boot, then call

```
.query()
```

on the returned handle once a prompt is ready. This moves subprocess spawn and initialization out of the critical path.

### ``` tool() ```

Creates a type-safe MCP tool definition for use with SDK MCP servers.

#### Parameters

ParameterTypeDescription

```
name
```

```
string
```

The name of the tool

```
description
```

```
string
```

A description of what the tool does

```
inputSchema
```

```
Schema extends AnyZodRawShape
```

Zod schema defining the tool’s input parameters (supports both Zod 3 and Zod 4)

```
handler
```

```
(args, extra) => Promise<
```

```
CallToolResult
```

Async function that executes the tool logic

```
extras
```

```
{ annotations?:
```

```
ToolAnnotations
```

Optional MCP tool annotations providing behavioral hints to clients

#### ``` ToolAnnotations ```

Re-exported from

```
@modelcontextprotocol/sdk/types.js
```

. All fields are optional hints; clients should not rely on them for security decisions.

FieldTypeDefaultDescription

```
title
```

```
string
```

```
undefined
```

Human-readable title for the tool

```
readOnlyHint
```

```
boolean
```

```
false
```

If

```
true
```

, the tool does not modify its environment

```
destructiveHint
```

```
boolean
```

```
true
```

If

```
true
```

, the tool may perform destructive updates (only meaningful when

```
readOnlyHint
```

is

```
false
```

)

```
idempotentHint
```

```
boolean
```

```
false
```

If

```
true
```

, repeated calls with the same arguments have no additional effect (only meaningful when

```
readOnlyHint
```

is

```
false
```

)

```
openWorldHint
```

```
boolean
```

```
true
```

If

```
true
```

, the tool interacts with external entities (for example, web search). If

```
false
```

, the tool’s domain is closed (for example, a memory tool)

### ``` createSdkMcpServer() ```

Creates an MCP server instance that runs in the same process as your application.

#### Parameters

ParameterTypeDescription

```
options.name
```

```
string
```

The name of the MCP server

```
options.version
```

```
string
```

Optional version string

```
options.tools
```

```
Array<SdkMcpToolDefinition>
```

Array of tool definitions created with

```
tool()
```

### ``` listSessions() ```

Discovers and lists past sessions with light metadata. Filter by project directory or list sessions across all projects.

#### Parameters

ParameterTypeDefaultDescription

```
options.dir
```

```
string
```

```
undefined
```

Directory to list sessions for. When omitted, returns sessions across all projects

```
options.limit
```

```
number
```

```
undefined
```

Maximum number of sessions to return

```
options.includeWorktrees
```

```
boolean
```

```
true
```

When

```
dir
```

is inside a git repository, include sessions from all worktree paths

#### Return type: ``` SDKSessionInfo ```

PropertyTypeDescription

```
sessionId
```

```
string
```

Unique session identifier (UUID)

```
summary
```

```
string
```

Display title: custom title, auto-generated summary, or first prompt

```
lastModified
```

```
number
```

Last modified time in milliseconds since epoch

```
fileSize
```

```
number | undefined
```

Session file size in bytes. Only populated for local JSONL storage

```
customTitle
```

```
string | undefined
```

User-set session title (via

```
/rename
```

)

```
firstPrompt
```

```
string | undefined
```

First meaningful user prompt in the session

```
gitBranch
```

```
string | undefined
```

Git branch at the end of the session

```
cwd
```

```
string | undefined
```

Working directory for the session

```
tag
```

```
string | undefined
```

User-set session tag (see

```
tagSession()
```

```
createdAt
```

```
number | undefined
```

#### Example

Print the 10 most recent sessions for a project. Results are sorted by

```
lastModified
```

descending, so the first item is the newest. Omit

```
dir
```

to search across all projects.

### ``` getSessionMessages() ```

Reads user and assistant messages from a past session transcript.

#### Parameters

ParameterTypeDefaultDescription

```
sessionId
```

```
string
```

requiredSession UUID to read (see

```
listSessions()
```

)

```
options.dir
```

```
string
```

```
undefined
```

Project directory to find the session in. When omitted, searches all projects

```
options.limit
```

```
number
```

```
undefined
```

Maximum number of messages to return

```
options.offset
```

```
number
```

```
undefined
```

Number of messages to skip from the start

#### Return type: ``` SessionMessage ```

PropertyTypeDescription

```
type
```

```
"user" | "assistant"
```

Message role

```
uuid
```

```
string
```

Unique message identifier

```
session_id
```

```
string
```

Session this message belongs to

```
message
```

```
unknown
```

Raw message payload from the transcript

```
parent_tool_use_id
```

```
null
```

Reserved

#### Example

### ``` getSessionInfo() ```

Reads metadata for a single session by ID without scanning the full project directory.

#### Parameters

ParameterTypeDefaultDescription

```
sessionId
```

```
string
```

requiredUUID of the session to look up

```
options.dir
```

```
string
```

```
undefined
```

Project directory path. When omitted, searches all project directories

[[Agent SDK reference - TypeScript - Claude Code Docs|, or]]

```
SDKSessionInfo
```

```
undefined
```

if the session is not found.

### ``` renameSession() ```

Renames a session by appending a custom-title entry. Repeated calls are safe; the most recent title wins.

#### Parameters

ParameterTypeDefaultDescription

```
sessionId
```

```
string
```

requiredUUID of the session to rename

```
title
```

```
string
```

requiredNew title. Must be non-empty after trimming whitespace

```
options.dir
```

```
string
```

```
undefined
```

Project directory path. When omitted, searches all project directories

### ``` tagSession() ```

Tags a session. Pass

```
null
```

to clear the tag. Repeated calls are safe; the most recent tag wins.

#### Parameters

ParameterTypeDefaultDescription

```
sessionId
```

```
string
```

requiredUUID of the session to tag

```
tag
```

```
string | null
```

requiredTag string, or

```
null
```

to clear

```
options.dir
```

```
string
```

```
undefined
```

Project directory path. When omitted, searches all project directories

## Types

### ``` Options ```

Configuration object for the

```
query()
```

function.

PropertyTypeDefaultDescription

```
abortController
```

```
AbortController
```

```
new AbortController()
```

Controller for cancelling operations

```
additionalDirectories
```

```
string[]
```

```
[]
```

Additional directories Claude can access

```
agent
```

```
string
```

```
undefined
```

Agent name for the main thread. The agent must be defined in the

```
agents
```

option or in settings

```
agents
```

```
Record<string, [
```

AgentDefinition

```
](#agent-definition)>
```

```
undefined
```

Programmatically define subagents

```
allowDangerouslySkipPermissions
```

```
boolean
```

```
false
```

Enable bypassing permissions. Required when using

```
permissionMode: 'bypassPermissions'
```

```
allowedTools
```

```
string[]
```

```
[]
```

Tools to auto-approve without prompting. This does not restrict Claude to only these tools; unlisted tools fall through to

```
permissionMode
```

and

```
canUseTool
```

. Use

```
disallowedTools
```

to block tools. See

```
betas
```

```
SdkBeta
```

```
[]
```

```
[]
```

```
canUseTool
```

```
CanUseTool
```

```
undefined
```

```
continue
```

```
boolean
```

```
false
```

```
cwd
```

```
string
```

```
process.cwd()
```

```
debug
```

```
boolean
```

```
false
```

```
debugFile
```

```
string
```

```
undefined
```

```
disallowedTools
```

```
string[]
```

```
[]
```

```
allowedTools
```

and

```
permissionMode
```

(including

```
bypassPermissions
```

)

```
effort
```

```
'low' | 'medium' | 'high' | 'xhigh' | 'max'
```

```
'high'
```

```
enableFileCheckpointing
```

```
boolean
```

```
false
```

[File checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing)

```
env
```

```
Record<string, string | undefined>
```

```
process.env
```

[[Environment variables - Claude Code Docs|Environment variables]]for variables the underlying CLI reads. Set

```
CLAUDE_AGENT_SDK_CLIENT_APP
```

to identify your app in the User-Agent header

```
executable
```

```
'bun' | 'deno' | 'node'
```

```
executableArgs
```

```
string[]
```

```
[]
```

```
extraArgs
```

```
Record<string, string | null>
```

```
{}
```

```
fallbackModel
```

```
string
```

```
undefined
```

```
forkSession
```

```
boolean
```

```
false
```

```
resume
```

, fork to a new session ID instead of continuing the original session

```
hooks
```

```
Partial<Record<
```

```
HookEvent
```

```
,
```

```
HookCallbackMatcher
```

```
[]>>
```

```
{}
```

```
includePartialMessages
```

```
boolean
```

```
false
```

```
maxBudgetUsd
```

```
number
```

```
undefined
```

```
total_cost_usd
```

; see [Track cost and usage](https://code.claude.com/docs/en/agent-sdk/cost-tracking)for accuracy caveats

```
maxThinkingTokens
```

```
number
```

```
undefined
```

```
thinking
```

instead. Maximum tokens for thinking process

```
maxTurns
```

```
number
```

```
undefined
```

```
mcpServers
```

```
Record<string, [
```

McpServerConfig

```
](#mcp-server-config)>
```

```
{}
```

```
model
```

```
string
```

```
outputFormat
```

```
{ type: 'json_schema', schema: JSONSchema }
```

```
undefined
```

[[Get structured output from agents - Claude Code Docs|Structured outputs]]for details

```
pathToClaudeCodeExecutable
```

```
string
```

```
permissionMode
```

```
PermissionMode
```

```
'default'
```

```
permissionPromptToolName
```

```
string
```

```
undefined
```

```
persistSession
```

```
boolean
```

```
true
```

```
false
```

, disables session persistence to disk. Sessions cannot be resumed later

```
plugins
```

```
SdkPluginConfig
```

```
[]
```

```
[]
```

[[Plugins in the SDK - Claude Code Docs|Plugins]]for details

```
promptSuggestions
```

```
boolean
```

```
false
```

```
prompt_suggestion
```

message after each turn with a predicted next user prompt

```
resume
```

```
string
```

```
undefined
```

```
resumeSessionAt
```

```
string
```

```
undefined
```

```
sandbox
```

```
SandboxSettings
```

```
undefined
```

[[Agent SDK reference - TypeScript - Claude Code Docs|Sandbox settings]]for details

```
sessionId
```

```
string
```

```
sessionStore
```

```
SessionStore
```

```
undefined
```

[Persist sessions to external storage](https://code.claude.com/docs/en/agent-sdk/session-storage)

```
settingSources
```

```
SettingSource
```

```
[]
```

```
[]
```

to disable user, project, and local settings. Managed policy settings load regardless. See [[Use Claude Code features in the SDK - Claude Code Docs#What settingSources does not control|Use Claude Code features]]

```
spawnClaudeCodeProcess
```

```
(options: SpawnOptions) => SpawnedProcess
```

```
undefined
```

```
stderr
```

```
(data: string) => void
```

```
undefined
```

```
strictMcpConfig
```

```
boolean
```

```
false
```

```
systemPrompt
```

```
string | { type: 'preset'; preset: 'claude_code'; append?: string; excludeDynamicSections?: boolean }
```

```
undefined
```

(minimal prompt)

```
{ type: 'preset', preset: 'claude_code' }
```

to use Claude Code’s system prompt. When using the preset object form, add

```
append
```

to extend it with additional instructions, and set

```
excludeDynamicSections: true
```

to move per-session context into the first user message for [[Modifying system prompts - Claude Code Docs#Improve prompt caching across users and machines|better prompt-cache reuse across machines]]

```
thinking
```

```
ThinkingConfig
```

```
{ type: 'adaptive' }
```

for supported models[[Agent SDK reference - TypeScript - Claude Code Docs|for options]]

```
ThinkingConfig
```

```
toolConfig
```

```
ToolConfig
```

```
undefined
```

[[Agent SDK reference - TypeScript - Claude Code Docs|for details]]

```
ToolConfig
```

```
tools
```

```
string[] | { type: 'preset'; preset: 'claude_code' }
```

```
undefined
```

### ``` Query ``` object

Interface returned by the

```
query()
```

function.

#### Methods

MethodDescription

```
interrupt()
```

Interrupts the query (only available in streaming input mode)

```
rewindFiles(userMessageId, options?)
```

Restores files to their state at the specified user message. Pass

```
{ dryRun: true }
```

to preview changes. Requires

```
enableFileCheckpointing: true
```

. See

```
setPermissionMode()
```

Changes the permission mode (only available in streaming input mode)

```
setModel()
```

Changes the model (only available in streaming input mode)

```
setMaxThinkingTokens()
```

Deprecated: Use the

```
thinking
```

option instead. Changes the maximum thinking tokens

```
initializationResult()
```

Returns the full initialization result including supported commands, models, account info, and output style configuration

```
supportedCommands()
```

Returns available slash commands

```
supportedModels()
```

Returns available models with display info

```
supportedAgents()
```

Returns available subagents as

```
AgentInfo
```

```
[]
```

```
mcpServerStatus()
```

```
accountInfo()
```

```
reconnectMcpServer(serverName)
```

```
toggleMcpServer(serverName, enabled)
```

```
setMcpServers(servers)
```

```
streamInput(stream)
```

```
stopTask(taskId)
```

```
close()
```

### ``` WarmQuery ```

Handle returned by

[[Agent SDK reference - TypeScript - Claude Code Docs#startup()|. The subprocess is already spawned and initialized, so calling]]

```
startup()
```

```
query()
```

on this handle writes the prompt directly to a ready process with no startup latency.

#### Methods

MethodDescription

```
query(prompt)
```

Send a prompt to the pre-warmed subprocess and return a

```
Query
```

```
WarmQuery
```

```
close()
```

```
WarmQuery
```

implements

```
AsyncDisposable
```

, so it can be used with

```
await using
```

for automatic cleanup.

### ``` SDKControlInitializeResponse ```

Return type of

```
initializationResult()
```

. Contains session initialization data.

### ``` AgentDefinition ```

Configuration for a subagent defined programmatically.

FieldRequiredDescription

```
description
```

YesNatural language description of when to use this agent

```
tools
```

NoArray of allowed tool names. If omitted, inherits all tools from parent

```
disallowedTools
```

NoArray of tool names to explicitly disallow for this agent

```
prompt
```

YesThe agent’s system prompt

```
model
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

, or a full model ID. If omitted or

```
'inherit'
```

, uses the main model

```
mcpServers
```

NoMCP server specifications for this agent

```
skills
```

NoArray of skill names to preload into the agent context

```
initialPrompt
```

NoAuto-submitted as the first user turn when this agent runs as the main thread agent

```
maxTurns
```

NoMaximum number of agentic turns (API round-trips) before stopping

```
background
```

NoRun this agent as a non-blocking background task when invoked

```
memory
```

NoMemory source for this agent:

```
'user'
```

,

```
'project'
```

, or

```
'local'
```

```
effort
```

NoReasoning effort level for this agent. Accepts a named level or an integer

```
permissionMode
```

NoPermission mode for tool execution within this agent. See

```
PermissionMode
```

```
criticalSystemReminder_EXPERIMENTAL
```

### ``` AgentMcpServerSpec ```

Specifies MCP servers available to a subagent. Can be a server name (string referencing a server from the parent’s

```
mcpServers
```

config) or an inline server configuration record mapping server names to configs.

```
McpServerConfigForProcessTransport
```

is

```
McpStdioServerConfig | McpSSEServerConfig | McpHttpServerConfig | McpSdkServerConfig
```

.

### ``` SettingSource ```

Controls which filesystem-based configuration sources the SDK loads settings from.

ValueDescriptionLocation

```
'user'
```

Global user settings

```
~/.claude/settings.json
```

```
'project'
```

Shared project settings (version controlled)

```
.claude/settings.json
```

```
'local'
```

Local project settings (gitignored)

```
.claude/settings.local.json
```

#### Default behavior

When

```
settingSources
```

is omitted or

```
undefined
```

,

```
query()
```

loads the same filesystem settings as the Claude Code CLI: user, project, and local. Managed policy settings are loaded in all cases. See

[[Use Claude Code features in the SDK - Claude Code Docs#What settingSources does not control|What settingSources does not control]]for inputs that are read regardless of this option, and how to disable them.

#### Why use settingSources

Disable filesystem settings:

#### Settings precedence

When multiple sources are loaded, settings are merged with this precedence (highest to lowest):

- Local settings (

  ```
  .claude/settings.local.json
  ```

  )
- Project settings (

  ```
  .claude/settings.json
  ```

  )
- User settings (

  ```
  ~/.claude/settings.json
  ```

  )

```
agents
```

and

```
allowedTools
```

override user, project, and local filesystem settings. Managed policy settings take precedence over programmatic options.

### ``` PermissionMode ```

### ``` CanUseTool ```

Custom permission function type for controlling tool usage.

OptionTypeDescription

```
signal
```

```
AbortSignal
```

Signaled if the operation should be aborted

```
suggestions
```

```
PermissionUpdate
```

```
[]
```

```
blockedPath
```

```
string
```

```
decisionReason
```

```
string
```

```
toolUseID
```

```
string
```

```
agentID
```

```
string
```

### ``` PermissionResult ```

Result of a permission check.

### ``` ToolConfig ```

Configuration for built-in tool behavior.

FieldTypeDescription

```
askUserQuestion.previewFormat
```

```
'markdown' | 'html'
```

Opts into the

```
preview
```

field on

```
AskUserQuestion
```

### ``` McpServerConfig ```

Configuration for MCP servers.

#### ``` McpStdioServerConfig ```

#### ``` McpSSEServerConfig ```

#### ``` McpHttpServerConfig ```

#### ``` McpSdkServerConfigWithInstance ```

#### ``` McpClaudeAIProxyServerConfig ```

### ``` SdkPluginConfig ```

Configuration for loading plugins in the SDK.

FieldTypeDescription

```
type
```

```
'local'
```

Must be

```
'local'
```

(only local plugins currently supported)

```
path
```

```
string
```

Absolute or relative path to the plugin directory

[[Plugins in the SDK - Claude Code Docs|Plugins]].

## Message Types

### ``` SDKMessage ```

Union type of all possible messages returned by the query.

### ``` SDKAssistantMessage ```

Assistant response message.

```
message
```

field is a

[from the Anthropic SDK. It includes fields like](https://platform.claude.com/docs/en/api/messages/create)

```
BetaMessage
```

```
id
```

,

```
content
```

,

```
model
```

,

```
stop_reason
```

, and

```
usage
```

.

```
SDKAssistantMessageError
```

is one of:

```
'authentication_failed'
```

,

```
'billing_error'
```

,

```
'rate_limit'
```

,

```
'invalid_request'
```

,

```
'server_error'
```

,

```
'max_output_tokens'
```

, or

```
'unknown'
```

.

### ``` SDKUserMessage ```

User input message.

```
shouldQuery
```

to

```
false
```

to append the message to the transcript without triggering an assistant turn. The message is held and merged into the next user message that does trigger a turn. Use this to inject context, such as the output of a command you ran out of band, without spending a model call on it.

### ``` SDKUserMessageReplay ```

Replayed user message with required UUID.

### ``` SDKResultMessage ```

Final result message.

```
PreToolUse
```

hook returns

```
permissionDecision: "defer"
```

, the result has

```
stop_reason: "tool_deferred"
```

and

```
deferred_tool_use
```

carries the pending tool’s

```
id
```

,

```
name
```

, and

```
input
```

. Read this field to surface the request in your own UI, then resume with the same

```
session_id
```

to continue. See

[[Hooks reference - Claude Code Docs#Defer a tool call for later|Defer a tool call for later]]for the full round trip.

### ``` SDKSystemMessage ```

System initialization message.

### ``` SDKPartialAssistantMessage ```

Streaming partial message (only when

```
includePartialMessages
```

is true).

### ``` SDKCompactBoundaryMessage ```

Message indicating a conversation compaction boundary.

### ``` SDKPluginInstallMessage ```

Plugin installation progress event. Emitted when

[[Environment variables - Claude Code Docs|is set, so your Agent SDK application can track marketplace plugin installation before the first turn. The]]

```
CLAUDE_CODE_SYNC_PLUGIN_INSTALL
```

```
started
```

and

```
completed
```

statuses bracket the overall install. The

```
installed
```

and

```
failed
```

statuses report individual marketplaces and include

```
name
```

.

### ``` SDKPermissionDenial ```

Information about a denied tool use.

## Hook Types

For a comprehensive guide on using hooks with examples and common patterns, see the

[[Intercept and control agent behavior with hooks - Claude Code Docs|Hooks guide]].

### ``` HookEvent ```

Available hook events.

### ``` HookCallback ```

Hook callback function type.

### ``` HookCallbackMatcher ```

Hook configuration with optional matcher.

### ``` HookInput ```

Union type of all hook input types.

### ``` BaseHookInput ```

Base interface that all hook input types extend.

#### ``` PreToolUseHookInput ```

#### ``` PostToolUseHookInput ```

#### ``` PostToolUseFailureHookInput ```

#### ``` PostToolBatchHookInput ```

Fires once after every tool call in a batch has resolved, before the next model request.

```
tool_response
```

carries the serialized

```
tool_result
```

content the model sees; the shape differs from

```
PostToolUseHookInput
```

’s structured

```
Output
```

object.

#### ``` NotificationHookInput ```

#### ``` UserPromptSubmitHookInput ```

#### ``` SessionStartHookInput ```

#### ``` SessionEndHookInput ```

#### ``` StopHookInput ```

#### ``` SubagentStartHookInput ```

#### ``` SubagentStopHookInput ```

#### ``` PreCompactHookInput ```

#### ``` PermissionRequestHookInput ```

#### ``` SetupHookInput ```

#### ``` TeammateIdleHookInput ```

#### ``` TaskCompletedHookInput ```

#### ``` ConfigChangeHookInput ```

#### ``` WorktreeCreateHookInput ```

#### ``` WorktreeRemoveHookInput ```

### ``` HookJSONOutput ```

Hook return value.

#### ``` AsyncHookJSONOutput ```

#### ``` SyncHookJSONOutput ```

## Tool Input Types

Documentation of input schemas for all built-in Claude Code tools. These types are exported from

```
@anthropic-ai/claude-agent-sdk
```

and can be used for type-safe tool interactions.

### ``` ToolInputSchemas ```

Union of all tool input types, exported from

```
@anthropic-ai/claude-agent-sdk
```

.

### Agent

Tool name:

```
Agent
```

(previously

```
Task
```

, which is still accepted as an alias)

### AskUserQuestion

Tool name:

```
AskUserQuestion
```

[[Handle approvals and user input - Claude Code Docs#Handle clarifying questions|Handle approvals and user input]]for usage details.

### Bash

Tool name:

```
Bash
```

### Monitor

Tool name:

```
Monitor
```

```
persistent: true
```

for session-length watches such as log tails. Monitor follows the same permission rules as Bash. See the

[[Tools reference - Claude Code Docs#Monitor tool|Monitor tool reference]]for behavior and provider availability.

### TaskOutput

Tool name:

```
TaskOutput
```

### Edit

Tool name:

```
Edit
```

### Read

Tool name:

```
Read
```

```
pages
```

for PDF page ranges (for example,

```
"1-5"
```

).

### Write

Tool name:

```
Write
```

### Glob

Tool name:

```
Glob
```

### Grep

Tool name:

```
Grep
```

### TaskStop

Tool name:

```
TaskStop
```

### NotebookEdit

Tool name:

```
NotebookEdit
```

### WebFetch

Tool name:

```
WebFetch
```

### WebSearch

Tool name:

```
WebSearch
```

### TodoWrite

Tool name:

```
TodoWrite
```

### ExitPlanMode

Tool name:

```
ExitPlanMode
```

### ListMcpResources

Tool name:

```
ListMcpResources
```

### ReadMcpResource

Tool name:

```
ReadMcpResource
```

### EnterWorktree

Tool name:

```
EnterWorktree
```

```
path
```

to switch into an existing worktree of the current repository instead of creating a new one.

```
name
```

and

```
path
```

are mutually exclusive.

## Tool Output Types

Documentation of output schemas for all built-in Claude Code tools. These types are exported from

```
@anthropic-ai/claude-agent-sdk
```

and represent the actual response data returned by each tool.

### ``` ToolOutputSchemas ```

Union of all tool output types.

### Agent

Tool name:

```
Agent
```

(previously

```
Task
```

, which is still accepted as an alias)

```
status
```

field:

```
"completed"
```

for finished tasks,

```
"async_launched"
```

for background tasks, and

```
"sub_agent_entered"
```

for interactive subagents.

### AskUserQuestion

Tool name:

```
AskUserQuestion
```

### Bash

Tool name:

```
Bash
```

```
backgroundTaskId
```

.

### Monitor

Tool name:

```
Monitor
```

```
TaskStop
```

to cancel the watch early.

### Edit

Tool name:

```
Edit
```

### Read

Tool name:

```
Read
```

```
type
```

field.

### Write

Tool name:

```
Write
```

### Glob

Tool name:

```
Glob
```

### Grep

Tool name:

```
Grep
```

```
mode
```

: file list, content with matches, or match counts.

### TaskStop

Tool name:

```
TaskStop
```

### NotebookEdit

Tool name:

```
NotebookEdit
```

### WebFetch

Tool name:

```
WebFetch
```

### WebSearch

Tool name:

```
WebSearch
```

### TodoWrite

Tool name:

```
TodoWrite
```

### ExitPlanMode

Tool name:

```
ExitPlanMode
```

### ListMcpResources

Tool name:

```
ListMcpResources
```

### ReadMcpResource

Tool name:

```
ReadMcpResource
```

### EnterWorktree

Tool name:

```
EnterWorktree
```

## Permission Types

### ``` PermissionUpdate ```

Operations for updating permissions.

### ``` PermissionBehavior ```

### ``` PermissionUpdateDestination ```

### ``` PermissionRuleValue ```

## Other Types

### ``` ApiKeySource ```

### ``` SdkBeta ```

Available beta features that can be enabled via the

```
betas
```

option. See

[Beta headers](https://platform.claude.com/docs/en/api/beta-headers)for more information.

### ``` SlashCommand ```

Information about an available slash command.

### ``` ModelInfo ```

Information about an available model.

### ``` AgentInfo ```

Information about an available subagent that can be invoked via the Agent tool.

FieldTypeDescription

```
name
```

```
string
```

Agent type identifier (e.g.,

```
"Explore"
```

,

```
"general-purpose"
```

)

```
description
```

```
string
```

Description of when to use this agent

```
model
```

```
string | undefined
```

Model alias this agent uses. If omitted, inherits the parent’s model

### ``` McpServerStatus ```

Status of a connected MCP server.

### ``` McpServerStatusConfig ```

The configuration of an MCP server as reported by

```
mcpServerStatus()
```

. This is the union of all MCP server transport types.

[[Agent SDK reference - TypeScript - Claude Code Docs|for details on each transport type.]]

```
McpServerConfig
```

### ``` AccountInfo ```

Account information for the authenticated user.

### ``` ModelUsage ```

Per-model usage statistics returned in result messages. The

```
costUSD
```

value is a client-side estimate. See

[Track cost and usage](https://code.claude.com/docs/en/agent-sdk/cost-tracking)for billing caveats.

### ``` ConfigScope ```

### ``` NonNullableUsage ```

A version of

[[Agent SDK reference - TypeScript - Claude Code Docs#Usage|with all nullable fields made non-nullable.]]

```
Usage
```

### ``` Usage ```

Token usage statistics (from

```
@anthropic-ai/sdk
```

).

### ``` CallToolResult ```

MCP tool result type (from

```
@modelcontextprotocol/sdk/types.js
```

).

### ``` ThinkingConfig ```

Controls Claude’s thinking/reasoning behavior. Takes precedence over the deprecated

```
maxThinkingTokens
```

.

### ``` SpawnedProcess ```

Interface for custom process spawning (used with

```
spawnClaudeCodeProcess
```

option).

```
ChildProcess
```

already satisfies this interface.

### ``` SpawnOptions ```

Options passed to the custom spawn function.

### ``` McpSetServersResult ```

Result of a

```
setMcpServers()
```

operation.

### ``` RewindFilesResult ```

Result of a

```
rewindFiles()
```

operation.

### ``` SDKStatusMessage ```

Status update message (e.g., compacting).

### ``` SDKTaskNotificationMessage ```

Notification when a background task completes, fails, or is stopped. Background tasks include

```
run_in_background
```

Bash commands,

[[Agent SDK reference - TypeScript - Claude Code Docs#Monitor|Monitor]]watches, and background subagents.

### ``` SDKToolUseSummaryMessage ```

Summary of tool usage in a conversation.

### ``` SDKHookStartedMessage ```

Emitted when a hook begins executing.

### ``` SDKHookProgressMessage ```

Emitted while a hook is running, with stdout/stderr output.

### ``` SDKHookResponseMessage ```

Emitted when a hook finishes executing.

### ``` SDKToolProgressMessage ```

Emitted periodically while a tool is executing to indicate progress.

### ``` SDKAuthStatusMessage ```

Emitted during authentication flows.

### ``` SDKTaskStartedMessage ```

Emitted when a background task begins. The

```
task_type
```

field is

```
"local_bash"
```

for background Bash commands and

[[Agent SDK reference - TypeScript - Claude Code Docs#Monitor|Monitor]]watches,

```
"local_agent"
```

for subagents, or

```
"remote_agent"
```

.

### ``` SDKTaskProgressMessage ```

Emitted periodically while a background task is running.

### ``` SDKTaskUpdatedMessage ```

Emitted when a background task’s state changes, such as when it transitions from

```
running
```

to

```
completed
```

. Merge

```
patch
```

into your local task map keyed by

```
task_id
```

. The

```
end_time
```

field is a Unix epoch timestamp in milliseconds, comparable with

```
Date.now()
```

.

### ``` SDKFilesPersistedEvent ```

Emitted when file checkpoints are persisted to disk.

### ``` SDKRateLimitEvent ```

Emitted when the session encounters a rate limit.

### ``` SDKLocalCommandOutputMessage ```

Output from a local slash command (for example,

```
/voice
```

or

```
/usage
```

). Displayed as assistant-style text in the transcript.

### ``` SDKPromptSuggestionMessage ```

Emitted after each turn when

```
promptSuggestions
```

is enabled. Contains a predicted next user prompt.

### ``` AbortError ```

Custom error class for abort operations.

## Sandbox Configuration

### ``` SandboxSettings ```

Configuration for sandbox behavior. Use this to enable command sandboxing and configure network restrictions programmatically.

PropertyTypeDefaultDescription

```
enabled
```

```
boolean
```

```
false
```

Enable sandbox mode for command execution

```
autoAllowBashIfSandboxed
```

```
boolean
```

```
true
```

Auto-approve bash commands when sandbox is enabled

```
excludedCommands
```

```
string[]
```

```
[]
```

Commands that always bypass sandbox restrictions (e.g.,

```
['docker']
```

). These run unsandboxed automatically without model involvement

```
allowUnsandboxedCommands
```

```
boolean
```

```
true
```

Allow the model to request running commands outside the sandbox. When

```
true
```

, the model can set

```
dangerouslyDisableSandbox
```

in tool input, which falls back to the

```
network
```

```
SandboxNetworkConfig
```

```
undefined
```

```
filesystem
```

```
SandboxFilesystemConfig
```

```
undefined
```

```
ignoreViolations
```

```
Record<string, string[]>
```

```
undefined
```

```
{ file: ['/tmp/*'], network: ['localhost'] }
```

)

```
enableWeakerNestedSandbox
```

```
boolean
```

```
false
```

```
ripgrep
```

```
{ command: string; args?: string[] }
```

```
undefined
```

#### Example usage

### ``` SandboxNetworkConfig ```

Network-specific configuration for sandbox mode.

PropertyTypeDefaultDescription

```
allowedDomains
```

```
string[]
```

```
[]
```

Domain names that sandboxed processes can access

```
deniedDomains
```

```
string[]
```

```
[]
```

Domain names that sandboxed processes cannot access. Takes precedence over

```
allowedDomains
```

```
allowManagedDomainsOnly
```

```
boolean
```

```
false
```

Restrict network access to only the domains in

```
allowedDomains
```

```
allowLocalBinding
```

```
boolean
```

```
false
```

Allow processes to bind to local ports (e.g., for dev servers)

```
allowUnixSockets
```

```
string[]
```

```
[]
```

Unix socket paths that processes can access (e.g., Docker socket)

```
allowAllUnixSockets
```

```
boolean
```

```
false
```

Allow access to all Unix sockets

```
httpProxyPort
```

```
number
```

```
undefined
```

HTTP proxy port for network requests

```
socksProxyPort
```

```
number
```

```
undefined
```

SOCKS proxy port for network requests

### ``` SandboxFilesystemConfig ```

Filesystem-specific configuration for sandbox mode.

PropertyTypeDefaultDescription

```
allowWrite
```

```
string[]
```

```
[]
```

File path patterns to allow write access to

```
denyWrite
```

```
string[]
```

```
[]
```

File path patterns to deny write access to

```
denyRead
```

```
string[]
```

```
[]
```

File path patterns to deny read access to

### Permissions Fallback for Unsandboxed Commands

When

```
allowUnsandboxedCommands
```

is enabled, the model can request to run commands outside the sandbox by setting

```
dangerouslyDisableSandbox: true
```

in the tool input. These requests fall back to the existing permissions system, meaning your

```
canUseTool
```

handler is invoked, allowing you to implement custom authorization logic.

```
excludedCommands
```

vs

```
allowUnsandboxedCommands
```

:

- ```
  excludedCommands
  ```

  : A static list of commands that always bypass the sandbox automatically (e.g.,

  ```
  ['docker']
  ```

  ). The model has no control over this.
- ```
  allowUnsandboxedCommands
  ```

  : Lets the model decide at runtime whether to request unsandboxed execution by setting

  ```
  dangerouslyDisableSandbox: true
  ```

  in the tool input.

- Audit model requests: Log when the model requests unsandboxed execution
- Implement allowlists: Only permit specific commands to run unsandboxed
- Add approval workflows: Require explicit authorization for privileged operations

## See also

- [[Agent SDK overview - Claude Code Docs|SDK overview]]- General SDK concepts
- [[Agent SDK reference - Python - Claude Code Docs|Python SDK reference]]- Python SDK documentation
- [[CLI reference - Claude Code Docs|CLI reference]]- Command-line interface
- [[Common workflows - Claude Code Docs|Common workflows]]- Step-by-step guides

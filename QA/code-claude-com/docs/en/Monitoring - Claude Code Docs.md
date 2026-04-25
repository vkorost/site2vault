---
title: Monitoring - Claude Code Docs
source_url: https://code.claude.com/docs/en/monitoring-usage
description: Learn how to enable and configure OpenTelemetry for Claude Code.
---

[[Monitoring - Claude Code Docs#Traces (beta)|traces protocol]]. Configure your metrics, logs, and traces backends to match your monitoring requirements.

## Quick start

Configure OpenTelemetry using environment variables:

The default export intervals are 60 seconds for metrics and 5 seconds for logs. During setup, you may want to use shorter intervals for debugging purposes. Remember to reset these for production use.

[OpenTelemetry specification](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Administrator configuration

Administrators can configure OpenTelemetry settings for all users through the

[[Claude Code settings - Claude Code Docs#Settings files|managed settings file]]. This allows for centralized control of telemetry settings across an organization. See the

[[Claude Code settings - Claude Code Docs#Settings precedence|settings precedence]]for more information about how settings are applied. Example managed settings configuration:

Managed settings can be distributed via MDM (Mobile Device Management) or other device management solutions. Environment variables defined in the managed settings file have high precedence and cannot be overridden by users.

## Configuration details

### Common configuration variables

Environment VariableDescriptionExample Values

```
CLAUDE_CODE_ENABLE_TELEMETRY
```

Enables telemetry collection (required)

```
1
```

```
OTEL_METRICS_EXPORTER
```

Metrics exporter types, comma-separated. Use

```
none
```

to disable

```
console
```

,

```
otlp
```

,

```
prometheus
```

,

```
none
```

```
OTEL_LOGS_EXPORTER
```

Logs/events exporter types, comma-separated. Use

```
none
```

to disable

```
console
```

,

```
otlp
```

,

```
none
```

```
OTEL_EXPORTER_OTLP_PROTOCOL
```

Protocol for OTLP exporter, applies to all signals

```
grpc
```

,

```
http/json
```

,

```
http/protobuf
```

```
OTEL_EXPORTER_OTLP_ENDPOINT
```

OTLP collector endpoint for all signals

```
http://localhost:4317
```

```
OTEL_EXPORTER_OTLP_METRICS_PROTOCOL
```

Protocol for metrics, overrides general setting

```
grpc
```

,

```
http/json
```

,

```
http/protobuf
```

```
OTEL_EXPORTER_OTLP_METRICS_ENDPOINT
```

OTLP metrics endpoint, overrides general setting

```
http://localhost:4318/v1/metrics
```

```
OTEL_EXPORTER_OTLP_LOGS_PROTOCOL
```

Protocol for logs, overrides general setting

```
grpc
```

,

```
http/json
```

,

```
http/protobuf
```

```
OTEL_EXPORTER_OTLP_LOGS_ENDPOINT
```

OTLP logs endpoint, overrides general setting

```
http://localhost:4318/v1/logs
```

```
OTEL_EXPORTER_OTLP_HEADERS
```

Authentication headers for OTLP

```
Authorization=Bearer token
```

```
OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY
```

Client key for mTLS authenticationPath to client key file

```
OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE
```

Client certificate for mTLS authenticationPath to client cert file

```
OTEL_METRIC_EXPORT_INTERVAL
```

Export interval in milliseconds (default: 60000)

```
5000
```

,

```
60000
```

```
OTEL_LOGS_EXPORT_INTERVAL
```

Logs export interval in milliseconds (default: 5000)

```
1000
```

,

```
10000
```

```
OTEL_LOG_USER_PROMPTS
```

Enable logging of user prompt content (default: disabled)

```
1
```

to enable

```
OTEL_LOG_TOOL_DETAILS
```

Enable logging of tool parameters and input arguments in tool events and trace span attributes: Bash commands, MCP server and tool names, skill names, and tool input. Also enables custom, plugin, and MCP command names on

```
user_prompt
```

events (default: disabled)

```
1
```

to enable

```
OTEL_LOG_TOOL_CONTENT
```

Enable logging of tool input and output content in span events (default: disabled). Requires

```
1
```

to enable

```
OTEL_LOG_RAW_API_BODIES
```

```
api_request_body
```

/

```
api_response_body
```

log events (default: disabled). Bodies include the entire conversation history. Enabling this implies consent to everything

```
OTEL_LOG_USER_PROMPTS
```

,

```
OTEL_LOG_TOOL_DETAILS
```

, and

```
OTEL_LOG_TOOL_CONTENT
```

would reveal

```
1
```

for inline bodies truncated at 60 KB, or

```
file:<dir>
```

for untruncated bodies on disk with a

```
body_ref
```

pointer in the event

```
OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
```

```
delta
```

). Set to

```
cumulative
```

if your backend expects cumulative temporality

```
delta
```

,

```
cumulative
```

```
CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS
```

```
900000
```

### Metrics cardinality control

The following environment variables control which attributes are included in metrics to manage cardinality:

Environment VariableDescriptionDefault ValueExample to Disable

```
OTEL_METRICS_INCLUDE_SESSION_ID
```

Include session.id attribute in metrics

```
true
```

```
false
```

```
OTEL_METRICS_INCLUDE_VERSION
```

Include app.version attribute in metrics

```
false
```

```
true
```

```
OTEL_METRICS_INCLUDE_ACCOUNT_UUID
```

Include user.account\_uuid and user.account\_id attributes in metrics

```
true
```

```
false
```

### Traces (beta)

Distributed tracing exports spans that link each user prompt to the API requests and tool executions it triggers, so you can view a full request as a single trace in your tracing backend. Tracing is off by default. To enable it, set both

```
CLAUDE_CODE_ENABLE_TELEMETRY=1
```

and

```
CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1
```

, then set

```
OTEL_TRACES_EXPORTER
```

to choose where spans are sent. Traces reuse the

[[Monitoring - Claude Code Docs#Common configuration variables|common OTLP configuration]]for endpoint, protocol, and headers.

Environment VariableDescriptionExample Values

```
CLAUDE_CODE_ENHANCED_TELEMETRY_BETA
```

Enable span tracing (required).

```
ENABLE_ENHANCED_TELEMETRY_BETA
```

is also accepted

```
1
```

```
OTEL_TRACES_EXPORTER
```

Traces exporter types, comma-separated. Use

```
none
```

to disable

```
console
```

,

```
otlp
```

,

```
none
```

```
OTEL_EXPORTER_OTLP_TRACES_PROTOCOL
```

Protocol for traces, overrides

```
OTEL_EXPORTER_OTLP_PROTOCOL
```

```
grpc
```

,

```
http/json
```

,

```
http/protobuf
```

```
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT
```

OTLP traces endpoint, overrides

```
OTEL_EXPORTER_OTLP_ENDPOINT
```

```
http://localhost:4318/v1/traces
```

```
OTEL_TRACES_EXPORT_INTERVAL
```

Span batch export interval in milliseconds (default: 5000)

```
1000
```

,

```
10000
```

```
OTEL_LOG_USER_PROMPTS=1
```

,

```
OTEL_LOG_TOOL_DETAILS=1
```

, and

```
OTEL_LOG_TOOL_CONTENT=1
```

to include them.
When tracing is active, Bash and PowerShell subprocesses automatically inherit a

```
TRACEPARENT
```

environment variable containing the W3C trace context of the active tool execution span. This lets any subprocess that reads

```
TRACEPARENT
```

parent its own spans under the same trace, enabling end-to-end distributed tracing through scripts and commands that Claude runs.
In Agent SDK and non-interactive sessions started with

```
-p
```

, Claude Code also reads

```
TRACEPARENT
```

and

```
TRACESTATE
```

from its own environment when starting each interaction span. This lets an embedding process pass its active W3C trace context into the subprocess so Claude Code’s spans appear as children of the caller’s distributed trace. Interactive sessions ignore inbound

```
TRACEPARENT
```

to avoid accidentally inheriting ambient values from CI or container environments.

#### Span hierarchy

Each user prompt starts a

```
claude_code.interaction
```

root span. API calls, tool calls, and hook executions are recorded as its children. Tool spans have two child spans of their own: one for the time spent waiting on a permission decision and one for the execution itself. When the Task tool spawns a subagent, the subagent’s API and tool spans nest under the parent’s

```
claude_code.tool
```

span.

```
claude -p
```

sessions,

```
claude_code.interaction
```

itself becomes a child of the caller’s span when

```
TRACEPARENT
```

is set in the environment.

#### Span attributes

Every span carries the

[[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]plus a

```
span.type
```

attribute matching its name. The tables below list the additional attributes set on each span. The

```
llm_request
```

,

```
tool.execution
```

, and

```
hook
```

spans set OpenTelemetry status

```
ERROR
```

when they record a failure; the other spans always end with status

```
UNSET
```

.

```
claude_code.interaction
```

AttributeDescriptionGated by

```
user_prompt
```

Prompt text. Value is

```
<REDACTED>
```

unless the gate is set

```
OTEL_LOG_USER_PROMPTS
```

```
user_prompt_length
```

Prompt length in characters

```
interaction.sequence
```

1-based counter of interactions in this session

```
interaction.duration_ms
```

Wall-clock duration of the turn

```
claude_code.llm_request
```

AttributeDescriptionGated by

```
model
```

Model identifier

```
gen_ai.system
```

Always

```
anthropic
```

. OpenTelemetry GenAI semantic convention

```
gen_ai.request.model
```

Same value as

```
model
```

. OpenTelemetry GenAI semantic convention

```
query_source
```

Subsystem that issued the request, such as

```
repl_main_thread
```

or a subagent name

```
speed
```

```
fast
```

or

```
normal
```

```
llm_request.context
```

```
interaction
```

,

```
tool
```

, or

```
standalone
```

depending on the parent span

```
duration_ms
```

Wall-clock duration including retries

```
ttft_ms
```

Time to first token in milliseconds

```
input_tokens
```

Input token count from the API usage block

```
output_tokens
```

Output token count

```
cache_read_tokens
```

Tokens read from prompt cache

```
cache_creation_tokens
```

Tokens written to prompt cache

```
request_id
```

Anthropic API request ID from the

```
request-id
```

response header

```
gen_ai.response.id
```

Same value as

```
request_id
```

. OpenTelemetry GenAI semantic convention

```
client_request_id
```

Client-generated

```
x-client-request-id
```

of the final attempt

```
attempt
```

Total attempts made for this request

```
success
```

```
true
```

or

```
false
```

```
status_code
```

HTTP status code when the request failed

```
error
```

Error message when the request failed

```
response.has_tool_call
```

```
true
```

when the response contained tool-use blocks

```
gen_ai.request.attempt
```

span event with

```
attempt
```

and

```
client_request_id
```

attributes.

```
claude_code.tool
```

AttributeDescriptionGated by

```
tool_name
```

Tool name

```
duration_ms
```

Wall-clock duration including permission wait and execution

```
result_tokens
```

Approximate token size of the tool result

```
file_path
```

Target file path for Read, Edit, and Write tools

```
OTEL_LOG_TOOL_DETAILS
```

```
full_command
```

Command string for the Bash tool

```
OTEL_LOG_TOOL_DETAILS
```

```
skill_name
```

Skill name for the Skill tool

```
OTEL_LOG_TOOL_DETAILS
```

```
subagent_type
```

Subagent type for the Task tool

```
OTEL_LOG_TOOL_DETAILS
```

```
OTEL_LOG_TOOL_CONTENT=1
```

, this span also records a

```
tool.output
```

span event whose attributes contain the tool’s input and output bodies, truncated at 60 KB per attribute.

```
claude_code.tool.blocked_on_user
```

AttributeDescriptionGated by

```
duration_ms
```

Time spent waiting for the permission decision

```
decision
```

```
accept
```

or

```
reject
```

```
source
```

Decision source, matching the

```
tool_decision
```

event

```
claude_code.tool.execution
```

AttributeDescriptionGated by

```
duration_ms
```

Time spent running the tool body

```
success
```

```
true
```

or

```
false
```

```
error
```

Error category string when execution failed, such as

```
Error:ENOENT
```

or

```
ShellError
```

. Contains the full error message instead when the gate is set

```
OTEL_LOG_TOOL_DETAILS
```

```
claude_code.hook
```

This span is emitted only when detailed beta tracing is active, which requires

```
ENABLE_BETA_TRACING_DETAILED=1
```

and

```
BETA_TRACING_ENDPOINT
```

in addition to the trace exporter configuration above. In interactive CLI sessions, this also requires your organization to be allowlisted for the feature. Agent SDK and non-interactive

```
-p
```

sessions are not gated. It is not emitted when only

```
CLAUDE_CODE_ENHANCED_TELEMETRY_BETA
```

is set.

AttributeDescriptionGated by

```
hook_event
```

Hook event type, such as

```
PreToolUse
```

```
hook_name
```

Full hook name, such as

```
PreToolUse:Write
```

```
num_hooks
```

Number of matching hook commands executed

```
hook_definitions
```

JSON-serialized hook configuration

```
OTEL_LOG_TOOL_DETAILS
```

```
duration_ms
```

Wall-clock duration of all matching hooks

```
num_success
```

Count of hooks that completed successfully

```
num_blocking
```

Count of hooks that returned a blocking decision

```
num_non_blocking_error
```

Count of hooks that failed without blocking

```
num_cancelled
```

Count of hooks cancelled before completion

Additional content-bearing attributes such as

```
new_context
```

,

```
system_prompt_preview
```

,

```
tool_input
```

, and

```
response.model_output
```

are emitted only when detailed beta tracing is active. They are not part of the stable span schema.

### Dynamic headers

For enterprise environments that require dynamic authentication, you can configure a script to generate headers dynamically:

#### Settings configuration

Add to your

```
.claude/settings.json
```

:

#### Script requirements

The script must output valid JSON with string key-value pairs representing HTTP headers:

#### Refresh behavior

The headers helper script runs at startup and periodically thereafter to support token refresh. By default, the script runs every 29 minutes. Customize the interval with the

```
CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS
```

environment variable.

### Multi-team organization support

Organizations with multiple teams or departments can add custom attributes to distinguish between different groups using the

```
OTEL_RESOURCE_ATTRIBUTES
```

environment variable:

- Filter metrics by team or department
- Track costs per cost center
- Create team-specific dashboards
- Set up alerts for specific teams

### Example configurations

Set these environment variables before running

```
claude
```

. Each block shows a complete configuration for a different exporter or deployment scenario:

## Available metrics and events

### Standard attributes

All metrics and events share these standard attributes:

AttributeDescriptionControlled By

```
session.id
```

Unique session identifier

```
OTEL_METRICS_INCLUDE_SESSION_ID
```

(default: true)

```
app.version
```

Current Claude Code version

```
OTEL_METRICS_INCLUDE_VERSION
```

(default: false)

```
organization.id
```

Organization UUID (when authenticated)Always included when available

```
user.account_uuid
```

Account UUID (when authenticated)

```
OTEL_METRICS_INCLUDE_ACCOUNT_UUID
```

(default: true)

```
user.account_id
```

Account ID in tagged format matching Anthropic admin APIs (when authenticated), such as

```
user_01BWBeN28...
```

```
OTEL_METRICS_INCLUDE_ACCOUNT_UUID
```

(default: true)

```
user.id
```

Anonymous device/installation identifier, generated per Claude Code installationAlways included

```
user.email
```

User email address (when authenticated via OAuth)Always included when available

```
terminal.type
```

Terminal type, such as

```
iTerm.app
```

,

```
vscode
```

,

```
cursor
```

, or

```
tmux
```

Always included when detected

- ```
  prompt.id
  ```

  : UUID correlating a user prompt with all subsequent events until the next prompt. See[[Monitoring - Claude Code Docs#Event correlation attributes|Event correlation attributes]].
- ```
  workspace.host_paths
  ```

  : host workspace directories selected in the desktop app, as a string array

### Metrics

Claude Code exports the following metrics:

Metric NameDescriptionUnit

```
claude_code.session.count
```

Count of CLI sessions startedcount

```
claude_code.lines_of_code.count
```

Count of lines of code modifiedcount

```
claude_code.pull_request.count
```

Number of pull requests createdcount

```
claude_code.commit.count
```

Number of git commits createdcount

```
claude_code.cost.usage
```

Cost of the Claude Code sessionUSD

```
claude_code.token.usage
```

Number of tokens usedtokens

```
claude_code.code_edit_tool.decision
```

Count of code editing tool permission decisionscount

```
claude_code.active_time.total
```

Total active time in secondss

### Metric details

Each metric includes the standard attributes listed above. Metrics with additional context-specific attributes are noted below.

#### Session counter

Incremented at the start of each session. Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  start_type
  ```

  : How the session was started. One of

  ```
  "fresh"
  ```

  ,

  ```
  "resume"
  ```

  , or

  ```
  "continue"
  ```

#### Lines of code counter

Incremented when code is added or removed. Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  type
  ```

  : (

  ```
  "added"
  ```

  ,

  ```
  "removed"
  ```

  )

#### Pull request counter

Incremented when creating pull requests via Claude Code. Attributes:

#### Commit counter

Incremented when creating git commits via Claude Code. Attributes:

#### Cost counter

Incremented after each API request. Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  model
  ```

  : Model identifier (for example, “claude-sonnet-4-6”)
- ```
  query_source
  ```

  : Category of the subsystem that issued the request. One of

  ```
  "main"
  ```

  ,

  ```
  "subagent"
  ```

  , or

  ```
  "auxiliary"
  ```
- ```
  speed
  ```

  :

  ```
  "fast"
  ```

  when the request used fast mode. Absent otherwise
- ```
  effort
  ```

  :[[Model configuration - Claude Code Docs#Adjust effort level|Effort level]]applied to the request:

  ```
  "low"
  ```

  ,

  ```
  "medium"
  ```

  ,

  ```
  "high"
  ```

  ,

  ```
  "xhigh"
  ```

  , or

  ```
  "max"
  ```

  . Absent when the model does not support effort.

#### Token counter

Incremented after each API request. Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  type
  ```

  : (

  ```
  "input"
  ```

  ,

  ```
  "output"
  ```

  ,

  ```
  "cacheRead"
  ```

  ,

  ```
  "cacheCreation"
  ```

  )
- ```
  model
  ```

  : Model identifier (for example, “claude-sonnet-4-6”)
- ```
  query_source
  ```

  : Category of the subsystem that issued the request. One of

  ```
  "main"
  ```

  ,

  ```
  "subagent"
  ```

  , or

  ```
  "auxiliary"
  ```
- ```
  speed
  ```

  :

  ```
  "fast"
  ```

  when the request used fast mode. Absent otherwise
- ```
  effort
  ```

  :[[Model configuration - Claude Code Docs#Adjust effort level|Effort level]]applied to the request. See[[Monitoring - Claude Code Docs#Cost counter|Cost counter]]for details.

#### Code edit tool decision counter

Incremented when user accepts or rejects Edit, Write, or NotebookEdit tool usage. Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  tool_name
  ```

  : Tool name (

  ```
  "Edit"
  ```

  ,

  ```
  "Write"
  ```

  ,

  ```
  "NotebookEdit"
  ```

  )
- ```
  decision
  ```

  : User decision (

  ```
  "accept"
  ```

  ,

  ```
  "reject"
  ```

  )
- ```
  source
  ```

  : Decision source -

  ```
  "config"
  ```

  ,

  ```
  "hook"
  ```

  ,

  ```
  "user_permanent"
  ```

  ,

  ```
  "user_temporary"
  ```

  ,

  ```
  "user_abort"
  ```

  , or

  ```
  "user_reject"
  ```
- ```
  language
  ```

  : Programming language of the edited file, such as

  ```
  "TypeScript"
  ```

  ,

  ```
  "Python"
  ```

  ,

  ```
  "JavaScript"
  ```

  , or

  ```
  "Markdown"
  ```

  . Returns

  ```
  "unknown"
  ```

  for unrecognized file extensions.

#### Active time counter

Tracks actual time spent actively using Claude Code, excluding idle time. This metric is incremented during user interactions (typing, reading responses) and during CLI processing (tool execution, AI response generation). Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  type
  ```

  :

  ```
  "user"
  ```

  for keyboard interactions,

  ```
  "cli"
  ```

  for tool execution and AI responses

### Events

Claude Code exports the following events via OpenTelemetry logs/events (when

```
OTEL_LOGS_EXPORTER
```

is configured):

#### Event correlation attributes

When a user submits a prompt, Claude Code may make multiple API calls and run several tools. The

```
prompt.id
```

attribute lets you tie all of those events back to the single prompt that triggered them.

AttributeDescription

```
prompt.id
```

UUID v4 identifier linking all events produced while processing a single user prompt

```
prompt.id
```

value. This returns the user\_prompt event, any api\_request events, and any tool\_result events that occurred while processing that prompt.

```
prompt.id
```

is intentionally excluded from metrics because each prompt generates a unique ID, which would create an ever-growing number of time series. Use it for event-level analysis and audit trails only.

#### User prompt event

Logged when a user submits a prompt. Event Name:

```
claude_code.user_prompt
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "user_prompt"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  prompt_length
  ```

  : Length of the prompt
- ```
  prompt
  ```

  : Prompt content (redacted by default, enable with

  ```
  OTEL_LOG_USER_PROMPTS=1
  ```

  )
- ```
  command_name
  ```

  : Command name when the prompt invokes one. Built-in and bundled command names such as

  ```
  compact
  ```

  or

  ```
  debug
  ```

  are emitted as-is; aliases such as

  ```
  reset
  ```

  emit as typed rather than the canonical name. Custom, plugin, and MCP command names collapse to

  ```
  custom
  ```

  or

  ```
  mcp
  ```

  unless

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  is set
- ```
  command_source
  ```

  : Origin of the command when present:

  ```
  builtin
  ```

  ,

  ```
  custom
  ```

  , or

  ```
  mcp
  ```

  . Plugin-provided commands report as

  ```
  custom
  ```

#### Tool result event

Logged when a tool completes execution. Event Name:

```
claude_code.tool_result
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "tool_result"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  tool_name
  ```

  : Name of the tool
- ```
  tool_use_id
  ```

  : Unique identifier for this tool invocation. Matches the

  ```
  tool_use_id
  ```

  passed to hooks, allowing correlation between OTel events and hook-captured data.
- ```
  success
  ```

  :

  ```
  "true"
  ```

  or

  ```
  "false"
  ```
- ```
  duration_ms
  ```

  : Execution time in milliseconds
- ```
  error_type
  ```

  : Error category string when the tool failed, such as

  ```
  "Error:ENOENT"
  ```

  or

  ```
  "ShellError"
  ```
- ```
  error
  ```

  (when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  ): Full error message when the tool failed
- ```
  decision_type
  ```

  : Either

  ```
  "accept"
  ```

  or

  ```
  "reject"
  ```
- ```
  decision_source
  ```

  : Decision source -

  ```
  "config"
  ```

  ,

  ```
  "hook"
  ```

  ,

  ```
  "user_permanent"
  ```

  ,

  ```
  "user_temporary"
  ```

  ,

  ```
  "user_abort"
  ```

  , or

  ```
  "user_reject"
  ```
- ```
  tool_input_size_bytes
  ```

  : Size of the JSON-serialized tool input in bytes
- ```
  tool_result_size_bytes
  ```

  : Size of the tool result in bytes
- ```
  mcp_server_scope
  ```

  : MCP server scope identifier (for MCP tools)
- ```
  tool_parameters
  ```

  (when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  ): JSON string containing tool-specific parameters:
  - For Bash tool: includes

    ```
    bash_command
    ```

    ,

    ```
    full_command
    ```

    ,

    ```
    timeout
    ```

    ,

    ```
    description
    ```

    ,

    ```
    dangerouslyDisableSandbox
    ```

    , and

    ```
    git_commit_id
    ```

    (the commit SHA, when a

    ```
    git commit
    ```

    command succeeds)
  - For MCP tools: includes

    ```
    mcp_server_name
    ```

    ,

    ```
    mcp_tool_name
    ```
  - For Skill tool: includes

    ```
    skill_name
    ```
  - For Task tool: includes

    ```
    subagent_type
    ```
- For Bash tool: includes
- ```
  tool_input
  ```

  (when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  ): JSON-serialized tool arguments. Individual values over 512 characters are truncated, and the full payload is bounded to ~4 K characters. Applies to all tools including MCP tools.

#### API request event

Logged for each API request to Claude. Event Name:

```
claude_code.api_request
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "api_request"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  model
  ```

  : Model used (for example, “claude-sonnet-4-6”)
- ```
  cost_usd
  ```

  : Estimated cost in USD
- ```
  duration_ms
  ```

  : Request duration in milliseconds
- ```
  input_tokens
  ```

  : Number of input tokens
- ```
  output_tokens
  ```

  : Number of output tokens
- ```
  cache_read_tokens
  ```

  : Number of tokens read from cache
- ```
  cache_creation_tokens
  ```

  : Number of tokens used for cache creation
- ```
  request_id
  ```

  : Anthropic API request ID from the response’s

  ```
  request-id
  ```

  header, such as

  ```
  "req_011..."
  ```

  . Present only when the API returns one.
- ```
  speed
  ```

  :

  ```
  "fast"
  ```

  or

  ```
  "normal"
  ```

  , indicating whether fast mode was active
- ```
  query_source
  ```

  : Subsystem that issued the request, such as

  ```
  "repl_main_thread"
  ```

  ,

  ```
  "compact"
  ```

  , or a subagent name
- ```
  effort
  ```

  :[[Model configuration - Claude Code Docs#Adjust effort level|Effort level]]applied to the request:

  ```
  "low"
  ```

  ,

  ```
  "medium"
  ```

  ,

  ```
  "high"
  ```

  ,

  ```
  "xhigh"
  ```

  , or

  ```
  "max"
  ```

  . Absent when the model does not support effort.

#### API error event

Logged when an API request to Claude fails. Event Name:

```
claude_code.api_error
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "api_error"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  model
  ```

  : Model used (for example, “claude-sonnet-4-6”)
- ```
  error
  ```

  : Error message
- ```
  status_code
  ```

  : HTTP status code as a string, or

  ```
  "undefined"
  ```

  for non-HTTP errors
- ```
  duration_ms
  ```

  : Request duration in milliseconds
- ```
  attempt
  ```

  : Total number of attempts made, including the initial request (

  ```
  1
  ```

  means no retries occurred)
- ```
  request_id
  ```

  : Anthropic API request ID from the response’s

  ```
  request-id
  ```

  header, such as

  ```
  "req_011..."
  ```

  . Present only when the API returns one.
- ```
  speed
  ```

  :

  ```
  "fast"
  ```

  or

  ```
  "normal"
  ```

  , indicating whether fast mode was active
- ```
  query_source
  ```

  : Subsystem that issued the request, such as

  ```
  "repl_main_thread"
  ```

  ,

  ```
  "compact"
  ```

  , or a subagent name
- ```
  effort
  ```

  :[[Model configuration - Claude Code Docs#Adjust effort level|Effort level]]applied to the request. Absent when the model does not support effort.

#### API request body event

Logged for each API request attempt when

```
OTEL_LOG_RAW_API_BODIES
```

is set. One event is emitted per attempt, so retries with adjusted parameters each produce their own event.
Event Name:

```
claude_code.api_request_body
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "api_request_body"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  body
  ```

  : JSON-serialized Messages API request parameters (system prompt, messages, tools, etc.), truncated at 60 KB. Extended-thinking content in prior assistant turns is redacted. Emitted only in inline mode (

  ```
  OTEL_LOG_RAW_API_BODIES=1
  ```

  ).
- ```
  body_ref
  ```

  : Absolute path to a

  ```
  <dir>/<uuid>.request.json
  ```

  file containing the untruncated body. Emitted only in file mode (

  ```
  OTEL_LOG_RAW_API_BODIES=file:<dir>
  ```

  ).
- ```
  body_length
  ```

  : Untruncated body length. UTF-8 bytes when

  ```
  OTEL_LOG_RAW_API_BODIES=file:<dir>
  ```

  , or UTF-16 code units when

  ```
  =1
  ```
- ```
  body_truncated
  ```

  :

  ```
  "true"
  ```

  when inline truncation occurred. Absent in file mode and when no truncation occurred.
- ```
  model
  ```

  : Model identifier from the request parameters
- ```
  query_source
  ```

  : Subsystem that issued the request (for example,

  ```
  "compact"
  ```

  )

#### API response body event

Logged for each successful API response when

```
OTEL_LOG_RAW_API_BODIES
```

is set.
Event Name:

```
claude_code.api_response_body
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "api_response_body"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  body
  ```

  : JSON-serialized Messages API response (id, content blocks, usage, stop reason), truncated at 60 KB. Extended-thinking content is redacted. Emitted only in inline mode (

  ```
  OTEL_LOG_RAW_API_BODIES=1
  ```

  ).
- ```
  body_ref
  ```

  : Absolute path to a

  ```
  <dir>/<request_id>.response.json
  ```

  file containing the untruncated body. Emitted only in file mode (

  ```
  OTEL_LOG_RAW_API_BODIES=file:<dir>
  ```

  ).
- ```
  body_length
  ```

  : Untruncated body length. UTF-8 bytes when

  ```
  OTEL_LOG_RAW_API_BODIES=file:<dir>
  ```

  , or UTF-16 code units when

  ```
  =1
  ```
- ```
  body_truncated
  ```

  :

  ```
  "true"
  ```

  when inline truncation occurred. Absent in file mode and when no truncation occurred.
- ```
  model
  ```

  : Model identifier
- ```
  query_source
  ```

  : Subsystem that issued the request
- ```
  request_id
  ```

  : Anthropic API request ID from the response’s

  ```
  request-id
  ```

  header, such as

  ```
  "req_011..."
  ```

  . Present only when the API returns one.

#### Tool decision event

Logged when a tool permission decision is made (accept/reject). Event Name:

```
claude_code.tool_decision
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "tool_decision"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  tool_name
  ```

  : Name of the tool (for example, “Read”, “Edit”, “Write”, “NotebookEdit”)
- ```
  tool_use_id
  ```

  : Unique identifier for this tool invocation. Matches the

  ```
  tool_use_id
  ```

  passed to hooks, allowing correlation between OTel events and hook-captured data.
- ```
  decision
  ```

  : Either

  ```
  "accept"
  ```

  or

  ```
  "reject"
  ```
- ```
  source
  ```

  : Decision source -

  ```
  "config"
  ```

  ,

  ```
  "hook"
  ```

  ,

  ```
  "user_permanent"
  ```

  ,

  ```
  "user_temporary"
  ```

  ,

  ```
  "user_abort"
  ```

  , or

  ```
  "user_reject"
  ```

#### Permission mode changed event

Logged when the permission mode changes, for example from

```
Shift+Tab
```

cycling, exiting plan mode, or an auto mode gate check.
Event Name:

```
claude_code.permission_mode_changed
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "permission_mode_changed"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  from_mode
  ```

  : The previous permission mode, for example

  ```
  "default"
  ```

  ,

  ```
  "plan"
  ```

  ,

  ```
  "acceptEdits"
  ```

  ,

  ```
  "auto"
  ```

  , or

  ```
  "bypassPermissions"
  ```
- ```
  to_mode
  ```

  : The new permission mode
- ```
  trigger
  ```

  : What caused the change. One of

  ```
  "shift_tab"
  ```

  ,

  ```
  "exit_plan_mode"
  ```

  ,

  ```
  "auto_gate_denied"
  ```

  , or

  ```
  "auto_opt_in"
  ```

  . Absent when the transition originates from the SDK or bridge

#### Auth event

Logged when

```
/login
```

or

```
/logout
```

completes.
Event Name:

```
claude_code.auth
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "auth"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  action
  ```

  :

  ```
  "login"
  ```

  or

  ```
  "logout"
  ```
- ```
  success
  ```

  :

  ```
  "true"
  ```

  or

  ```
  "false"
  ```
- ```
  auth_method
  ```

  : Authentication method, such as

  ```
  "oauth"
  ```
- ```
  error_category
  ```

  : Categorical error kind when the action failed. The raw error message is never included
- ```
  status_code
  ```

  : HTTP status code as a string when the action failed with an HTTP error

#### MCP server connection event

Logged when an MCP server connects, disconnects, or fails to connect. Event Name:

```
claude_code.mcp_server_connection
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "mcp_server_connection"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  status
  ```

  :

  ```
  "connected"
  ```

  ,

  ```
  "failed"
  ```

  , or

  ```
  "disconnected"
  ```
- ```
  transport_type
  ```

  : Server transport, such as

  ```
  "stdio"
  ```

  ,

  ```
  "sse"
  ```

  , or

  ```
  "http"
  ```
- ```
  server_scope
  ```

  : Scope the server is configured at, such as

  ```
  "user"
  ```

  ,

  ```
  "project"
  ```

  , or

  ```
  "local"
  ```
- ```
  duration_ms
  ```

  : Connection attempt duration in milliseconds
- ```
  error_code
  ```

  : Error code when the connection failed
- ```
  server_name
  ```

  (when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  ): Configured server name
- ```
  error
  ```

  (when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  ): Full error message when the connection failed

#### Internal error event

Logged when Claude Code catches an unexpected internal error. Only the error class name and an errno-style code are recorded. The error message and stack trace are never included. This event is not emitted when running against Bedrock, Vertex, or Foundry, or when

```
DISABLE_ERROR_REPORTING
```

is set.
Event Name:

```
claude_code.internal_error
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "internal_error"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  error_name
  ```

  : Error class name, such as

  ```
  "TypeError"
  ```

  or

  ```
  "SyntaxError"
  ```
- ```
  error_code
  ```

  : Node.js errno code such as

  ```
  "ENOENT"
  ```

  when present on the error

#### Plugin installed event

Logged when a plugin finishes installing, from both the

```
claude plugin install
```

CLI command and the interactive

```
/plugin
```

UI.
Event Name:

```
claude_code.plugin_installed
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "plugin_installed"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  marketplace.is_official
  ```

  :

  ```
  "true"
  ```

  if the marketplace is an official Anthropic marketplace,

  ```
  "false"
  ```

  otherwise
- ```
  install.trigger
  ```

  :

  ```
  "cli"
  ```

  or

  ```
  "ui"
  ```
- ```
  plugin.name
  ```

  : Name of the installed plugin. For third-party marketplaces this is included only when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```
- ```
  plugin.version
  ```

  : Plugin version when declared in the marketplace entry. For third-party marketplaces this is included only when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```
- ```
  marketplace.name
  ```

  : Marketplace the plugin was installed from. For third-party marketplaces this is included only when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

#### Skill activated event

Logged when a skill is invoked. Event Name:

```
claude_code.skill_activated
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "skill_activated"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  skill.name
  ```

  : Name of the skill. For user-defined and third-party plugin skills the value is the placeholder

  ```
  "custom_skill"
  ```

  unless

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```
- ```
  skill.source
  ```

  : Where the skill was loaded from (for example,

  ```
  "bundled"
  ```

  ,

  ```
  "userSettings"
  ```

  ,

  ```
  "projectSettings"
  ```

  ,

  ```
  "plugin"
  ```

  )
- ```
  plugin.name
  ```

  (when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  or the plugin is from an official marketplace): Name of the owning plugin when the skill is provided by a plugin
- ```
  marketplace.name
  ```

  (when

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  or the plugin is from an official marketplace): Marketplace the owning plugin was installed from, when the skill is provided by a plugin

#### API retries exhausted event

Logged once when an API request fails after more than one attempt. Emitted alongside the final

```
api_error
```

event.
Event Name:

```
claude_code.api_retries_exhausted
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "api_retries_exhausted"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  model
  ```

  : Model used
- ```
  error
  ```

  : Final error message
- ```
  status_code
  ```

  : HTTP status code as a string
- ```
  total_attempts
  ```

  : Total number of attempts made
- ```
  total_retry_duration_ms
  ```

  : Total wall-clock time across all attempts
- ```
  speed
  ```

  :

  ```
  "fast"
  ```

  or

  ```
  "normal"
  ```

#### Hook execution start event

Logged when one or more hooks begin executing for a hook event. Event Name:

```
claude_code.hook_execution_start
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "hook_execution_start"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  hook_event
  ```

  : Hook event type, such as

  ```
  "PreToolUse"
  ```

  or

  ```
  "PostToolUse"
  ```
- ```
  hook_name
  ```

  : Full hook name including matcher, such as

  ```
  "PreToolUse:Write"
  ```
- ```
  num_hooks
  ```

  : Number of matching hook commands
- ```
  managed_only
  ```

  :

  ```
  "true"
  ```

  when only managed-policy hooks are permitted
- ```
  hook_source
  ```

  :

  ```
  "policySettings"
  ```

  or

  ```
  "merged"
  ```
- ```
  hook_definitions
  ```

  : JSON-serialized hook configuration. Included only when both detailed beta tracing and

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  are enabled

#### Hook execution complete event

Logged when all hooks for a hook event have finished. Event Name:

```
claude_code.hook_execution_complete
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "hook_execution_complete"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  hook_event
  ```

  : Hook event type
- ```
  hook_name
  ```

  : Full hook name including matcher
- ```
  num_hooks
  ```

  : Number of matching hook commands
- ```
  num_success
  ```

  : Count that completed successfully
- ```
  num_blocking
  ```

  : Count that returned a blocking decision
- ```
  num_non_blocking_error
  ```

  : Count that failed without blocking
- ```
  num_cancelled
  ```

  : Count cancelled before completion
- ```
  total_duration_ms
  ```

  : Wall-clock duration of all matching hooks
- ```
  managed_only
  ```

  :

  ```
  "true"
  ```

  when only managed-policy hooks are permitted
- ```
  hook_source
  ```

  :

  ```
  "policySettings"
  ```

  or

  ```
  "merged"
  ```
- ```
  hook_definitions
  ```

  : JSON-serialized hook configuration. Included only when both detailed beta tracing and

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  are enabled

#### Compaction event

Logged when conversation compaction completes. Event Name:

```
claude_code.compaction
```

Attributes:

- All [[Monitoring - Claude Code Docs#Standard attributes|standard attributes]]
- ```
  event.name
  ```

  :

  ```
  "compaction"
  ```
- ```
  event.timestamp
  ```

  : ISO 8601 timestamp
- ```
  event.sequence
  ```

  : monotonically increasing counter for ordering events within a session
- ```
  trigger
  ```

  :

  ```
  "auto"
  ```

  or

  ```
  "manual"
  ```
- ```
  success
  ```

  :

  ```
  "true"
  ```

  or

  ```
  "false"
  ```
- ```
  duration_ms
  ```

  : Compaction duration
- ```
  pre_tokens
  ```

  : Approximate token count before compaction
- ```
  post_tokens
  ```

  : Approximate token count after compaction
- ```
  error
  ```

  : Error message when compaction failed

## Interpret metrics and events data

The exported metrics and events support a range of analyses:

### Usage monitoring

MetricAnalysis Opportunity

```
claude_code.token.usage
```

Break down by

```
type
```

(input/output), user, team, or model

```
claude_code.session.count
```

Track adoption and engagement over time

```
claude_code.lines_of_code.count
```

Measure productivity by tracking code additions/removals

```
claude_code.commit.count
```

&

```
claude_code.pull_request.count
```

Understand impact on development workflows

### Cost monitoring

The

```
claude_code.cost.usage
```

metric helps with:

- Tracking usage trends across teams or individuals
- Identifying high-usage sessions for optimization

Cost metrics are approximations. For official billing data, refer to your API provider (Claude Console, AWS Bedrock, or Google Cloud Vertex).

### Alerting and segmentation

Common alerts to consider:

- Cost spikes
- Unusual token consumption
- High session volume from specific users

```
user.account_uuid
```

,

```
user.account_id
```

,

```
organization.id
```

,

```
session.id
```

,

```
model
```

, and

```
app.version
```

.

### Detect retry exhaustion

Claude Code retries failed API requests internally and emits a single

```
claude_code.api_error
```

event only after it gives up, so the event itself is the terminal signal for that request. Intermediate retry attempts are not logged as separate events.
The

```
attempt
```

attribute on the event records how many attempts were made in total. A value greater than

```
CLAUDE_CODE_MAX_RETRIES
```

(default

```
10
```

) indicates the request exhausted all retries on a transient error. A lower value indicates a non-retryable error such as a

```
400
```

response.
To distinguish a session that recovered from one that stalled, group events by

```
session.id
```

and check whether a later

```
api_request
```

event exists after the error.

### Event analysis

The event data provides detailed insights into Claude Code interactions: Tool Usage Patterns: analyze tool result events to identify:

- Most frequently used tools
- Tool success rates
- Average tool execution times
- Error patterns by tool type

## Backend considerations

Your choice of metrics, logs, and traces backends determines the types of analyses you can perform:

### For metrics

- Time series databases (for example, Prometheus): Rate calculations, aggregated metrics
- Columnar stores (for example, ClickHouse): Complex queries, unique user analysis
- Full-featured observability platforms (for example, Honeycomb, Datadog): Advanced querying, visualization, alerting

### For events/logs

- Log aggregation systems (for example, Elasticsearch, Loki): Full-text search, log analysis
- Columnar stores (for example, ClickHouse): Structured event analysis
- Full-featured observability platforms (for example, Honeycomb, Datadog): Correlation between metrics and events

### For traces

Choose a backend that supports distributed trace storage and span correlation:

- Distributed tracing systems (for example, Jaeger, Zipkin, Grafana Tempo): Span visualization, request waterfalls, latency analysis
- Full-featured observability platforms (for example, Honeycomb, Datadog): Trace search and correlation with metrics and logs

## Service information

All metrics and events are exported with the following resource attributes:

- ```
  service.name
  ```

  :

  ```
  claude-code
  ```
- ```
  service.version
  ```

  : Current Claude Code version
- ```
  os.type
  ```

  : Operating system type (for example,

  ```
  linux
  ```

  ,

  ```
  darwin
  ```

  ,

  ```
  windows
  ```

  )
- ```
  os.version
  ```

  : Operating system version string
- ```
  host.arch
  ```

  : Host architecture (for example,

  ```
  amd64
  ```

  ,

  ```
  arm64
  ```

  )
- ```
  wsl.version
  ```

  : WSL version number (only present when running on Windows Subsystem for Linux)
- Meter Name:

  ```
  com.anthropic.claude_code
  ```

## ROI measurement resources

For a comprehensive guide on measuring return on investment for Claude Code, including telemetry setup, cost analysis, productivity metrics, and automated reporting, see the

[Claude Code ROI Measurement Guide](https://github.com/anthropics/claude-code-monitoring-guide). This repository provides ready-to-use Docker Compose configurations, Prometheus and OpenTelemetry setups, and templates for generating productivity reports integrated with tools like Linear.

## Security and privacy

- Telemetry is opt-in and requires explicit configuration
- Raw file contents and code snippets are not included in metrics or events. Trace spans are a separate data path: see the

  ```
  OTEL_LOG_TOOL_CONTENT
  ```

  bullet below
- When authenticated via OAuth,

  ```
  user.email
  ```

  is included in telemetry attributes. If this is a concern for your organization, work with your telemetry backend to filter or redact this field
- User prompt content is not collected by default. Only prompt length is recorded. To include prompt content, set

  ```
  OTEL_LOG_USER_PROMPTS=1
  ```
- Tool input arguments and parameters are not logged by default. To include them, set

  ```
  OTEL_LOG_TOOL_DETAILS=1
  ```

  . When enabled,

  ```
  tool_result
  ```

  events include a

  ```
  tool_parameters
  ```

  attribute with Bash commands, MCP server and tool names, and skill names, plus a

  ```
  tool_input
  ```

  attribute with file paths, URLs, search patterns, and other arguments.

  ```
  user_prompt
  ```

  events include the verbatim

  ```
  command_name
  ```

  for custom, plugin, and MCP commands. Trace spans include the same

  ```
  tool_input
  ```

  attribute and input-derived attributes such as

  ```
  file_path
  ```

  . Individual values over 512 characters are truncated and the total is bounded to ~4 K characters, but the arguments may still contain sensitive values. Configure your telemetry backend to filter or redact these attributes as needed
- Tool input and output content is not logged in trace spans by default. To include it, set

  ```
  OTEL_LOG_TOOL_CONTENT=1
  ```

  . When enabled, span events include full tool input and output content truncated at 60 KB per span. This can include raw file contents from Read tool results and Bash command output. Configure your telemetry backend to filter or redact these attributes as needed
- Raw Anthropic Messages API request and response bodies are not logged by default. To include them, set

  ```
  OTEL_LOG_RAW_API_BODIES
  ```

  . With

  ```
  =1
  ```

  , each API call emits

  ```
  api_request_body
  ```

  and

  ```
  api_response_body
  ```

  log events whose

  ```
  body
  ```

  attribute is the JSON-serialized payload, truncated at 60 KB. With

  ```
  =file:<dir>
  ```

  , untruncated bodies are written to

  ```
  .request.json
  ```

  and

  ```
  .response.json
  ```

  files under that directory and the events carry a

  ```
  body_ref
  ```

  path instead of the inline body. Ship the directory with a log collector or sidecar rather than through the telemetry stream. In both modes, bodies contain the full conversation history (system prompt, every prior user and assistant turn, tool results), so enabling this implies consent to everything the other

  ```
  OTEL_LOG_*
  ```

  content flags would reveal. Claude’s extended-thinking content is always redacted from these bodies regardless of other settings

## Monitor Claude Code on Amazon Bedrock

For detailed Claude Code usage monitoring guidance for Amazon Bedrock, see

[Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).

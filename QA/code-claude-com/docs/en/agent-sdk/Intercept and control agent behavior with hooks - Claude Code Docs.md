---
title: Intercept and control agent behavior with hooks - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/hooks
description: Intercept and customize agent behavior at key execution points with hooks
---

- Block dangerous operations before they execute, like destructive shell commands or unauthorized file access
- Log and audit every tool call for compliance, debugging, or analytics
- Transform inputs and outputs to sanitize data, inject credentials, or redirect file paths
- Require human approval for sensitive actions like database writes or API calls
- Track session lifecycle to manage state, clean up resources, or send notifications

## How hooks work

An event fires

Something happens during agent execution and the SDK fires an event: a tool is about to be called (

```
PreToolUse
```

), a tool returned a result (

```
PostToolUse
```

), a subagent started or stopped, the agent is idle, or execution finished. See the [[Intercept and control agent behavior with hooks - Claude Code Docs#Available hooks|full list of events]].

The SDK collects registered hooks

The SDK checks for hooks registered for that event type. This includes callback hooks you pass in

```
options.hooks
```

and shell command hooks from settings files when the corresponding [[Agent SDK reference - TypeScript - Claude Code Docs|or]]

```
settingSources
```

[[Agent SDK reference - Python - Claude Code Docs|entry is enabled, which it is for default]]

```
setting_sources
```

```
query()
```

options.

Matchers filter which hooks run

If a hook has a

[[Intercept and control agent behavior with hooks - Claude Code Docs#Matchers|pattern (like]]

```
matcher
```

```
"Write|Edit"
```

), the SDK tests it against the event’s target (for example, the tool name). Hooks without a matcher run for every event of that type.

Callback functions execute

Each matching hook’s

[[Intercept and control agent behavior with hooks - Claude Code Docs#Callback functions|callback function]]receives input about what’s happening: the tool name, its arguments, the session ID, and other event-specific details.

Your callback returns a decision

After performing any operations (logging, API calls, validation), your callback returns an

[[Intercept and control agent behavior with hooks - Claude Code Docs#Outputs|output object]]that tells the agent what to do: allow the operation, block it, modify the input, or inject context into the conversation.

```
PreToolUse
```

hook (step 1) with a

```
"Write|Edit"
```

matcher (step 3) so the callback only fires for file-writing tools. When triggered, the callback receives the tool’s input (step 4), checks if the file path targets a

```
.env
```

file, and returns

```
permissionDecision: "deny"
```

to block the operation (step 5):

## Available hooks

The SDK provides hooks for different stages of agent execution. Some hooks are available in both SDKs, while others are TypeScript-only.

Hook EventPython SDKTypeScript SDKWhat triggers itExample use case

```
PreToolUse
```

YesYesTool call request (can block or modify)Block dangerous shell commands

```
PostToolUse
```

YesYesTool execution resultLog all file changes to audit trail

```
PostToolUseFailure
```

YesYesTool execution failureHandle or log tool errors

```
PostToolBatch
```

NoYesA full batch of tool calls resolves, once per batch before the next model callInject conventions once for the whole batch

```
UserPromptSubmit
```

YesYesUser prompt submissionInject additional context into prompts

```
Stop
```

YesYesAgent execution stopSave session state before exit

```
SubagentStart
```

YesYesSubagent initializationTrack parallel task spawning

```
SubagentStop
```

YesYesSubagent completionAggregate results from parallel tasks

```
PreCompact
```

YesYesConversation compaction requestArchive full transcript before summarizing

```
PermissionRequest
```

YesYesPermission dialog would be displayedCustom permission handling

```
SessionStart
```

NoYesSession initializationInitialize logging and telemetry

```
SessionEnd
```

NoYesSession terminationClean up temporary resources

```
Notification
```

YesYesAgent status messagesSend agent status updates to Slack or PagerDuty

```
Setup
```

NoYesSession setup/maintenanceRun initialization tasks

```
TeammateIdle
```

NoYesTeammate becomes idleReassign work or notify

```
TaskCompleted
```

NoYesBackground task completesAggregate results from parallel tasks

```
ConfigChange
```

NoYesConfiguration file changesReload settings dynamically

```
WorktreeCreate
```

NoYesGit worktree createdTrack isolated workspaces

```
WorktreeRemove
```

NoYesGit worktree removedClean up workspace resources

## Configure hooks

To configure a hook, pass it in the

```
hooks
```

field of your agent options (

```
ClaudeAgentOptions
```

in Python, the

```
options
```

object in TypeScript):

```
hooks
```

option is a dictionary (Python) or object (TypeScript) where:

- Keys are [[Intercept and control agent behavior with hooks - Claude Code Docs#Available hooks|hook event names]](e.g.,

  ```
  'PreToolUse'
  ```

  ,

  ```
  'PostToolUse'
  ```

  ,

  ```
  'Stop'
  ```

  )
- Values are arrays of [[Intercept and control agent behavior with hooks - Claude Code Docs#Matchers|matchers]], each containing an optional filter pattern and your[[Intercept and control agent behavior with hooks - Claude Code Docs#Callback functions|callback functions]]

### Matchers

Use matchers to filter when your callbacks fire. The

```
matcher
```

field is a regex string that matches against a different value depending on the hook event type. For example, tool-based hooks match against the tool name, while

```
Notification
```

hooks match against the notification type. See the

[[Hooks reference - Claude Code Docs#Matcher patterns|Claude Code hooks reference]]for the full list of matcher values for each event type.

OptionTypeDefaultDescription

```
matcher
```

```
string
```

```
undefined
```

Regex pattern matched against the event’s filter field. For tool hooks, this is the tool name. Built-in tools include

```
Bash
```

,

```
Read
```

,

```
Write
```

,

```
Edit
```

,

```
Glob
```

,

```
Grep
```

,

```
WebFetch
```

,

```
Agent
```

, and others (see

```
mcp__<server>__<action>
```

.

```
hooks
```

```
HookCallback[]
```

-Required. Array of callback functions to execute when the pattern matches

```
timeout
```

```
number
```

```
60
```

Timeout in seconds

```
matcher
```

pattern to target specific tools whenever possible. A matcher with

```
'Bash'
```

only runs for Bash commands, while omitting the pattern runs your callbacks for every occurrence of the event. Note that for tool-based hooks, matchers only filter by tool name, not by file paths or other arguments. To filter by file path, check

```
tool_input.file_path
```

inside your callback.

### Callback functions

#### Inputs

Every hook callback receives three arguments:

- Input data: a typed object containing event details. Each hook type has its own input shape (for example,

  ```
  PreToolUseHookInput
  ```

  includes

  ```
  tool_name
  ```

  and

  ```
  tool_input
  ```

  , while

  ```
  NotificationHookInput
  ```

  includes

  ```
  message
  ```

  ). See the full type definitions in the[[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript]]and[[Agent SDK reference - Python - Claude Code Docs|Python]]SDK references.
  - All hook inputs share

    ```
    session_id
    ```

    ,

    ```
    cwd
    ```

    , and

    ```
    hook_event_name
    ```

    .
  - ```
    agent_id
    ```

    and

    ```
    agent_type
    ```

    are populated when the hook fires inside a subagent. In TypeScript, these are on the base hook input and available to all hook types. In Python, they are on

    ```
    PreToolUse
    ```

    ,

    ```
    PostToolUse
    ```

    , and

    ```
    PostToolUseFailure
    ```

    only.
- All hook inputs share
- Tool use ID (

  ```
  str | None
  ```

  /

  ```
  string | undefined
  ```

  ): correlates

  ```
  PreToolUse
  ```

  and

  ```
  PostToolUse
  ```

  events for the same tool call.
- Context: in TypeScript, contains a

  ```
  signal
  ```

  property (

  ```
  AbortSignal
  ```

  ) for cancellation. In Python, this argument is reserved for future use.

#### Outputs

Your callback returns an object with two categories of fields:

- Top-level fields control the conversation:

  ```
  systemMessage
  ```

  injects a message into the conversation visible to the model, and

  ```
  continue
  ```

  (

  ```
  continue_
  ```

  in Python) determines whether the agent keeps running after this hook.
- ```
  hookSpecificOutput
  ```

  controls the current operation. The fields inside depend on the hook event type. For

  ```
  PreToolUse
  ```

  hooks, this is where you set

  ```
  permissionDecision
  ```

  (

  ```
  "allow"
  ```

  ,

  ```
  "deny"
  ```

  , or

  ```
  "ask"
  ```

  ),

  ```
  permissionDecisionReason
  ```

  , and

  ```
  updatedInput
  ```

  . In the TypeScript SDK,

  ```
  permissionDecision
  ```

  also accepts

  ```
  "defer"
  ```

  to end the query and[[Hooks reference - Claude Code Docs#Defer a tool call for later|resume later]]; this value is not available in the Python SDK. For

  ```
  PostToolUse
  ```

  hooks, you can set

  ```
  additionalContext
  ```

  to append information to the tool result.

```
{}
```

to allow the operation without changes. SDK callback hooks use the same JSON output format as

[[Hooks reference - Claude Code Docs#JSON output|Claude Code shell command hooks]], which documents every field and event-specific option. For the SDK type definitions, see the

[[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript]]and

[[Agent SDK reference - Python - Claude Code Docs|Python]]SDK references.

When multiple hooks or permission rules apply, deny takes priority over defer, which takes priority over ask, which takes priority over allow. If any hook returns

```
deny
```

, the operation is blocked regardless of other hooks.

#### Asynchronous output

By default, the agent waits for your hook to return before proceeding. If your hook performs a side effect (logging, sending a webhook) and doesn’t need to influence the agent’s behavior, you can return an async output instead. This tells the agent to continue immediately without waiting for the hook to finish:

FieldTypeDescription

```
async
```

```
true
```

Signals async mode. The agent proceeds without waiting. In Python, use

```
async_
```

to avoid the reserved keyword.

```
asyncTimeout
```

```
number
```

Optional timeout in milliseconds for the background operation

Async outputs cannot block, modify, or inject context into the operation since the agent has already moved on. Use them only for side effects like logging, metrics, or notifications.

## Examples

### Modify tool input

This example intercepts Write tool calls and rewrites the

```
file_path
```

argument to prepend

```
/sandbox
```

, redirecting all file writes to a sandboxed directory. The callback returns

```
updatedInput
```

with the modified path and

```
permissionDecision: 'allow'
```

to auto-approve the rewritten operation:

When using

```
updatedInput
```

, you must also include

```
permissionDecision: 'allow'
```

. Always return a new object rather than mutating the original

```
tool_input
```

.

### Add context and block a tool

This example blocks any attempt to write to the

```
/etc
```

directory and uses two output fields together:

```
permissionDecision: 'deny'
```

stops the tool call, while

```
systemMessage
```

injects a reminder into the conversation so the agent receives context about why the operation was blocked and avoids retrying it:

### Auto-approve specific tools

By default, the agent may prompt for permission before using certain tools. This example auto-approves read-only filesystem tools (Read, Glob, Grep) by returning

```
permissionDecision: 'allow'
```

, letting them run without user confirmation while leaving all other tools subject to normal permission checks:

### Chain multiple hooks

Hooks execute in the order they appear in the array. Keep each hook focused on a single responsibility and chain multiple hooks for complex logic:

### Filter with regex matchers

Use regex patterns to match multiple tools. This example registers three matchers with different scopes: the first triggers

```
file_security_hook
```

only for file modification tools, the second triggers

```
mcp_audit_hook
```

for any MCP tool (tools whose names start with

```
mcp__
```

), and the third triggers

```
global_logger
```

for every tool call regardless of name:

### Track subagent activity

Use

```
SubagentStop
```

hooks to monitor when subagents finish their work. See the full input type in the

[[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript]]and

[[Agent SDK reference - Python - Claude Code Docs|Python]]SDK references. This example logs a summary each time a subagent completes:

### Make HTTP requests from hooks

Hooks can perform asynchronous operations like HTTP requests. Catch errors inside your hook instead of letting them propagate, since an unhandled exception can interrupt the agent. This example sends a webhook after each tool completes, logging which tool ran and when. The hook catches errors so a failed webhook doesn’t interrupt the agent:

### Forward notifications to Slack

Use

```
Notification
```

hooks to receive system notifications from the agent and forward them to external services. Notifications fire for specific event types:

```
permission_prompt
```

(Claude needs permission),

```
idle_prompt
```

(Claude is waiting for input),

```
auth_success
```

(authentication completed), and

```
elicitation_dialog
```

(Claude is prompting the user). Each notification includes a

```
message
```

field with a human-readable description and optionally a

```
title
```

.
This example forwards every notification to a Slack channel. It requires a

[Slack incoming webhook URL](https://api.slack.com/messaging/webhooks), which you create by adding an app to your Slack workspace and enabling incoming webhooks:

## Fix common issues

### Hook not firing

- Verify the hook event name is correct and case-sensitive (

  ```
  PreToolUse
  ```

  , not

  ```
  preToolUse
  ```

  )
- Check that your matcher pattern matches the tool name exactly
- Ensure the hook is under the correct event type in

  ```
  options.hooks
  ```
- For non-tool hooks like

  ```
  Stop
  ```

  and

  ```
  SubagentStop
  ```

  , matchers match against different fields (see[[Hooks reference - Claude Code Docs#Matcher patterns|matcher patterns]])
- Hooks may not fire when the agent hits the limit because the session ends before hooks can execute

  ```
  max_turns
  ```

### Matcher not filtering as expected

Matchers only match tool names, not file paths or other arguments. To filter by file path, check

```
tool_input.file_path
```

inside your hook:

### Hook timeout

- Increase the

  ```
  timeout
  ```

  value in the

  ```
  HookMatcher
  ```

  configuration
- Use the

  ```
  AbortSignal
  ```

  from the third callback argument to handle cancellation gracefully in TypeScript

### Tool blocked unexpectedly

- Check all

  ```
  PreToolUse
  ```

  hooks for

  ```
  permissionDecision: 'deny'
  ```

  returns
- Add logging to your hooks to see what

  ```
  permissionDecisionReason
  ```

  they’re returning
- Verify matcher patterns aren’t too broad (an empty matcher matches all tools)

### Modified input not applied

- Ensure

  ```
  updatedInput
  ```

  is inside

  ```
  hookSpecificOutput
  ```

  , not at the top level:
- You must also return

  ```
  permissionDecision: 'allow'
  ```

  for the input modification to take effect
- Include

  ```
  hookEventName
  ```

  in

  ```
  hookSpecificOutput
  ```

  to identify which hook type the output is for

### Session hooks not available in Python

```
SessionStart
```

and

```
SessionEnd
```

can be registered as SDK callback hooks in TypeScript, but are not available in the Python SDK (

```
HookEvent
```

omits them). In Python, they are only available as

[[Hooks reference - Claude Code Docs#Hook events|shell command hooks]]defined in settings files (for example,

```
.claude/settings.json
```

). To load shell command hooks from your SDK application, include the appropriate setting source with

[[Agent SDK reference - Python - Claude Code Docs|or]]

```
setting_sources
```

[[Agent SDK reference - TypeScript - Claude Code Docs|:]]

```
settingSources
```

```
client.receive_response()
```

as your trigger.

### Subagent permission prompts multiplying

When spawning multiple subagents, each one may request permissions separately. Subagents do not automatically inherit parent agent permissions. To avoid repeated prompts, use

```
PreToolUse
```

hooks to auto-approve specific tools, or configure permission rules that apply to subagent sessions.

### Recursive hook loops with subagents

A

```
UserPromptSubmit
```

hook that spawns subagents can create infinite loops if those subagents trigger the same hook. To prevent this:

- Check for a subagent indicator in the hook input before spawning
- Use a shared variable or session state to track whether you’re already inside a subagent
- Scope hooks to only run for the top-level agent session

### systemMessage not appearing in output

The

```
systemMessage
```

field adds context to the conversation that the model sees, but it may not appear in all SDK output modes. If you need to surface hook decisions to your application, log them separately or use a dedicated output channel.

## Related resources

- [[Hooks reference - Claude Code Docs|Claude Code hooks reference]]: full JSON input/output schemas, event documentation, and matcher patterns
- [[Automate workflows with hooks - Claude Code Docs|Claude Code hooks guide]]: shell command hook examples and walkthroughs
- [[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript SDK reference]]: hook types, input/output definitions, and configuration options
- [[Agent SDK reference - Python - Claude Code Docs|Python SDK reference]]: hook types, input/output definitions, and configuration options
- [[Configure permissions - Claude Code Docs-dbd6de|Permissions]]: control what your agent can do
- [[Give Claude custom tools - Claude Code Docs|Custom tools]]: build tools to extend agent capabilities

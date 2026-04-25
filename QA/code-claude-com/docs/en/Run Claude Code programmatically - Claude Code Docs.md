---
title: Run Claude Code programmatically - Claude Code Docs
source_url: https://code.claude.com/docs/en/headless
description: Use the Agent SDK to run Claude Code programmatically from the CLI, Python,
  or TypeScript.
---

[[Agent SDK overview - Claude Code Docs|Agent SDK]]gives you the same tools, agent loop, and context management that power Claude Code. It’s available as a CLI for scripts and CI/CD, or as

[[Agent SDK reference - Python - Claude Code Docs|Python]]and

[[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript]]packages for full programmatic control.

The CLI was previously called “headless mode.” The

```
-p
```

flag and all CLI options work the same way.

```
-p
```

with your prompt and any

[[CLI reference - Claude Code Docs|CLI options]]:

```
claude -p
```

). For the Python and TypeScript SDK packages with structured outputs, tool approval callbacks, and native message objects, see the

[[Agent SDK overview - Claude Code Docs|full Agent SDK documentation]].

## Basic usage

Add the

```
-p
```

(or

```
--print
```

) flag to any

```
claude
```

command to run it non-interactively. All

[[CLI reference - Claude Code Docs|CLI options]]work with

```
-p
```

, including:

- ```
  --continue
  ```

  for[[Run Claude Code programmatically - Claude Code Docs#Continue conversations|continuing conversations]]
- ```
  --allowedTools
  ```

  for[[Run Claude Code programmatically - Claude Code Docs#Auto-approve tools|auto-approving tools]]
- ```
  --output-format
  ```

  for[[Run Claude Code programmatically - Claude Code Docs#Get structured output|structured output]]

### Start faster with bare mode

Add

```
--bare
```

to reduce startup time by skipping auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md. Without it,

```
claude -p
```

loads the same

[[How Claude Code works - Claude Code Docs#The context window|context]]an interactive session would, including anything configured in the working directory or

```
~/.claude
```

.
Bare mode is useful for CI and scripts where you need the same result on every machine. A hook in a teammate’s

```
~/.claude
```

or an MCP server in the project’s

```
.mcp.json
```

won’t run, because bare mode never reads them. Only flags you pass explicitly take effect.
This example runs a one-off summarize task in bare mode and pre-approves the Read tool so the call completes without a permission prompt:

To loadUseSystem prompt additions

```
--append-system-prompt
```

,

```
--append-system-prompt-file
```

Settings

```
--settings <file-or-json>
```

MCP servers

```
--mcp-config <file-or-json>
```

Custom agents

```
--agents <json>
```

A plugin directory

```
--plugin-dir <path>
```

```
ANTHROPIC_API_KEY
```

or an

```
apiKeyHelper
```

in the JSON passed to

```
--settings
```

. Bedrock, Vertex, and Foundry use their usual provider credentials.

```
--bare
```

is the recommended mode for scripted and SDK calls, and will become the default for

```
-p
```

in a future release.

## Examples

These examples highlight common CLI patterns. For CI and other scripted calls, add

[[Run Claude Code programmatically - Claude Code Docs#Start faster with bare mode|so they don’t pick up whatever happens to be configured locally.]]

```
--bare
```

### Get structured output

Use

```
--output-format
```

to control how responses are returned:

- ```
  text
  ```

  (default): plain text output
- ```
  json
  ```

  : structured JSON with result, session ID, and metadata
- ```
  stream-json
  ```

  : newline-delimited JSON for real-time streaming

```
result
```

field:

```
--output-format json
```

with

```
--json-schema
```

and a

[JSON Schema](https://json-schema.org/)definition. The response includes metadata about the request (session ID, usage, etc.) with the structured output in the

```
structured_output
```

field.
This example extracts function names and returns them as an array of strings:

### Stream responses

Use

```
--output-format stream-json
```

with

```
--verbose
```

and

```
--include-partial-messages
```

to receive tokens as they’re generated. Each line is a JSON object representing an event:

[jq](https://jqlang.github.io/jq/)to filter for text deltas and display just the streaming text. The

```
-r
```

flag outputs raw strings (no quotes) and

```
-j
```

joins without newlines so tokens stream continuously:

```
system/api_retry
```

event before retrying. You can use this to surface retry progress or implement custom backoff logic.

FieldTypeDescription

```
type
```

```
"system"
```

message type

```
subtype
```

```
"api_retry"
```

identifies this as a retry event

```
attempt
```

integercurrent attempt number, starting at 1

```
max_retries
```

integertotal retries permitted

```
retry_delay_ms
```

integermilliseconds until the next attempt

```
error_status
```

integer or nullHTTP status code, or

```
null
```

for connection errors with no HTTP response

```
error
```

stringerror category:

```
authentication_failed
```

,

```
billing_error
```

,

```
rate_limit
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

, or

```
unknown
```

```
uuid
```

stringunique event identifier

```
session_id
```

stringsession the event belongs to

```
system/init
```

event reports session metadata including the model, tools, MCP servers, and loaded plugins. It is the first event in the stream unless

[[Environment variables - Claude Code Docs|is set, in which case]]

```
CLAUDE_CODE_SYNC_PLUGIN_INSTALL
```

```
plugin_install
```

events precede it. Use the plugin fields to fail CI when a plugin did not load:

FieldTypeDescription

```
plugins
```

arrayplugins that loaded successfully, each with

```
name
```

and

```
path
```

```
plugin_errors
```

arrayplugin load-time errors such as an unsatisfied dependency version, each with

```
plugin
```

,

```
type
```

, and

```
message
```

. Affected plugins are demoted and absent from

```
plugins
```

. The key is omitted when there are no errors

[[Environment variables - Claude Code Docs|is set, Claude Code emits]]

```
CLAUDE_CODE_SYNC_PLUGIN_INSTALL
```

```
system/plugin_install
```

events while marketplace plugins install before the first turn. Use these to surface install progress in your own UI.

FieldTypeDescription

```
type
```

```
"system"
```

message type

```
subtype
```

```
"plugin_install"
```

identifies this as a plugin install event

```
status
```

```
"started"
```

,

```
"installed"
```

,

```
"failed"
```

, or

```
"completed"
```

```
started
```

and

```
completed
```

bracket the overall install;

```
installed
```

and

```
failed
```

report individual marketplaces

```
name
```

string, optionalmarketplace name, present on

```
installed
```

and

```
failed
```

```
error
```

string, optionalfailure message, present on

```
failed
```

```
uuid
```

stringunique event identifier

```
session_id
```

stringsession the event belongs to

[[Stream responses in real-time - Claude Code Docs|Stream responses in real-time]]in the Agent SDK documentation.

### Auto-approve tools

Use

```
--allowedTools
```

to let Claude use certain tools without prompting. This example runs a test suite and fixes failures, allowing Claude to execute Bash commands and read/edit files without asking for permission:

[[Choose a permission mode - Claude Code Docs|permission mode]].

```
dontAsk
```

denies anything not in your

```
permissions.allow
```

rules or the

[[Configure permissions - Claude Code Docs#Read-only commands|read-only command set]], which is useful for locked-down CI runs.

```
acceptEdits
```

lets Claude write files without prompting and also auto-approves common filesystem commands such as

```
mkdir
```

,

```
touch
```

,

```
mv
```

, and

```
cp
```

. Other shell commands and network requests still need an

```
--allowedTools
```

entry or a

```
permissions.allow
```

rule, otherwise the run aborts when one is attempted:

### Create a commit

This example reviews staged changes and creates a commit with an appropriate message:

```
--allowedTools
```

flag uses

[[Claude Code settings - Claude Code Docs#Permission rule syntax|permission rule syntax]]. The trailing

```
 *
```

enables prefix matching, so

```
Bash(git diff *)
```

allows any command starting with

```
git diff
```

. The space before

```
*
```

is important: without it,

```
Bash(git diff*)
```

would also match

```
git diff-index
```

.

User-invoked

[[Extend Claude with skills - Claude Code Docs|skills]]like

```
/commit
```

and [[Commands - Claude Code Docs|built-in commands]]are only available in interactive mode. In

```
-p
```

mode, describe the task you want to accomplish instead.

### Customize the system prompt

Use

```
--append-system-prompt
```

to add instructions while keeping Claude Code’s default behavior. This example pipes a PR diff to Claude and instructs it to review for security vulnerabilities:

[[CLI reference - Claude Code Docs|system prompt flags]]for more options including

```
--system-prompt
```

to fully replace the default prompt.

### Continue conversations

Use

```
--continue
```

to continue the most recent conversation, or

```
--resume
```

with a session ID to continue a specific conversation. This example runs a review, then sends follow-up prompts:

## Next steps

- [[Quickstart - Claude Code Docs-1f2ec9|Agent SDK quickstart]]: build your first agent with Python or TypeScript
- [[CLI reference - Claude Code Docs|CLI reference]]: all CLI flags and options
- [[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]: use the Agent SDK in GitHub workflows
- [[Claude Code GitLab CICD - Claude Code Docs|GitLab CI/CD]]: use the Agent SDK in GitLab pipelines

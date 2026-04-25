---
title: Give Claude custom tools - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/custom-tools
description: Define custom tools with the Claude Agent SDK's in-process MCP server
  so Claude can call your functions, hit your APIs, and perform domain-specific operations.
---

```
query
```

, and control which tools Claude can access. It also covers error handling, tool annotations, and returning non-text content like images.

## Quick reference

If you want to…Do thisDefine a toolUse

```
@tool
```

[[Agent SDK reference - TypeScript - Claude Code Docs#tool()|(TypeScript) with a name, description, schema, and handler. See]]

```
tool()
```

[[Give Claude custom tools - Claude Code Docs#Create a custom tool|Create a custom tool]].

```
create_sdk_mcp_server
```

/

```
createSdkMcpServer
```

and pass to

```
mcpServers
```

in

```
query()
```

. See [[Give Claude custom tools - Claude Code Docs#Call a custom tool|Call a custom tool]].[[Give Claude custom tools - Claude Code Docs#Configure allowed tools|Configure allowed tools]].

```
tools
```

array listing only the built-ins you want. See [[Give Claude custom tools - Claude Code Docs#Configure allowed tools|Configure allowed tools]].

```
readOnlyHint: true
```

on tools with no side effects. See [[Give Claude custom tools - Claude Code Docs#Add tool annotations|Add tool annotations]].

```
isError: true
```

instead of throwing. See [[Give Claude custom tools - Claude Code Docs#Handle errors|Handle errors]].

```
image
```

or

```
resource
```

blocks in the content array. See [[Give Claude custom tools - Claude Code Docs#Return images and resources|Return images and resources]].[tool search](https://code.claude.com/docs/en/agent-sdk/tool-search)to load tools on demand.

## Create a custom tool

A tool is defined by four parts, passed as arguments to the

[[Agent SDK reference - TypeScript - Claude Code Docs#tool()|helper in TypeScript or the]]

```
tool()
```

[[Agent SDK reference - Python - Claude Code Docs|decorator in Python:]]

```
@tool
```

- Name: a unique identifier Claude uses to call the tool.
- Description: what the tool does. Claude reads this to decide when to call it.
- Input schema: the arguments Claude must provide. In TypeScript this is always a [Zod schema](https://zod.dev/), and the handler’s

  ```
  args
  ```

  are typed from it automatically. In Python this is a dict mapping names to types, like

  ```
  {"latitude": float}
  ```

  , which the SDK converts to JSON Schema for you. The Python decorator also accepts a full[JSON Schema](https://json-schema.org/understanding-json-schema/about)dict directly when you need enums, ranges, optional fields, or nested objects.
- Handler: the async function that runs when Claude calls the tool. It receives the validated arguments and must return an object with:
  - ```
    content
    ```

    (required): an array of result blocks, each with a

    ```
    type
    ```

    of

    ```
    "text"
    ```

    ,

    ```
    "image"
    ```

    , or

    ```
    "resource"
    ```

    . See[[Give Claude custom tools - Claude Code Docs#Return images and resources|Return images and resources]]for non-text blocks.
  - ```
    isError
    ```

    (optional): set to

    ```
    true
    ```

    to signal a tool failure so Claude can react to it. See[[Give Claude custom tools - Claude Code Docs#Handle errors|Handle errors]].

[[Agent SDK reference - TypeScript - Claude Code Docs|(TypeScript) or]]

```
createSdkMcpServer
```

[[Agent SDK reference - Python - Claude Code Docs|(Python). The server runs in-process inside your application, not as a separate process.]]

```
create_sdk_mcp_server
```

### Weather tool example

This example defines a

```
get_temperature
```

tool and wraps it in an MCP server. It only sets up the tool; to pass it to

```
query
```

and run it, see

[[Give Claude custom tools - Claude Code Docs#Call a custom tool|Call a custom tool]]below.

[[Agent SDK reference - TypeScript - Claude Code Docs#tool()|TypeScript reference or the]]

```
tool()
```

[[Agent SDK reference - Python - Claude Code Docs|Python reference for full parameter details, including JSON Schema input formats and return value structure.]]

```
@tool
```

### Call a custom tool

Pass the MCP server you created to

```
query
```

via the

```
mcpServers
```

option. The key in

```
mcpServers
```

becomes the

```
{server_name}
```

segment in each tool’s fully qualified name:

```
mcp__{server_name}__{tool_name}
```

. List that name in

```
allowedTools
```

so the tool runs without a permission prompt.
These snippets reuse the

```
weatherServer
```

from the

[[Give Claude custom tools - Claude Code Docs#Weather tool example|example above]]to ask Claude what the weather is in a specific location.

### Add more tools

A server holds as many tools as you list in its

```
tools
```

array. With more than one tool on a server, you can list each one in

```
allowedTools
```

individually or use the wildcard

```
mcp__weather__*
```

to cover every tool the server exposes.
The example below adds a second tool,

```
get_precipitation_chance
```

, to the

```
weatherServer
```

from the

[[Give Claude custom tools - Claude Code Docs#Weather tool example|weather tool example]]and rebuilds it with both tools in the array.

[tool search](https://code.claude.com/docs/en/agent-sdk/tool-search)to load them on demand instead.

### Add tool annotations

[Tool annotations](https://modelcontextprotocol.io/docs/concepts/tools#tool-annotations)are optional metadata describing how a tool behaves. Pass them as the fifth argument to

```
tool()
```

helper in TypeScript or via the

```
annotations
```

keyword argument for the

```
@tool
```

decorator in Python. All hint fields are Booleans.

FieldDefaultMeaning

```
readOnlyHint
```

```
false
```

Tool does not modify its environment. Controls whether the tool can be called in parallel with other read-only tools.

```
destructiveHint
```

```
true
```

Tool may perform destructive updates. Informational only.

```
idempotentHint
```

```
false
```

Repeated calls with the same arguments have no additional effect. Informational only.

```
openWorldHint
```

```
true
```

Tool reaches systems outside your process. Informational only.

```
readOnlyHint: true
```

can still write to disk if that’s what the handler does. Keep the annotation accurate to the handler.
This example adds

```
readOnlyHint
```

to the

```
get_temperature
```

tool from the

[[Give Claude custom tools - Claude Code Docs#Weather tool example|weather tool example]].

```
ToolAnnotations
```

in the

[[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript]]or

[[Agent SDK reference - Python - Claude Code Docs|Python]]reference.

## Control tool access

The

[[Give Claude custom tools - Claude Code Docs#Weather tool example|weather tool example]]registered a server and listed tools in

```
allowedTools
```

. This section covers how tool names are constructed and how to scope access when you have multiple tools or want to restrict built-ins.

### Tool name format

When MCP tools are exposed to Claude, their names follow a specific format:

- Pattern:

  ```
  mcp__{server_name}__{tool_name}
  ```
- Example: A tool named

  ```
  get_temperature
  ```

  in server

  ```
  weather
  ```

  becomes

  ```
  mcp__weather__get_temperature
  ```

### Configure allowed tools

The

```
tools
```

option and the allowed/disallowed lists operate on separate layers.

```
tools
```

controls which built-in tools appear in Claude’s context. Allowed and disallowed tool lists control whether calls are approved or denied once Claude attempts them.

OptionLayerEffect

```
tools: ["Read", "Grep"]
```

AvailabilityOnly the listed built-ins are in Claude’s context. Unlisted built-ins are removed. MCP tools are unaffected.

```
tools: []
```

AvailabilityAll built-ins are removed. Claude can only use your MCP tools.allowed toolsPermissionListed tools run without a permission prompt. Unlisted tools remain available; calls go through the

```
tools
```

over disallowed tools. Omitting a tool from

```
tools
```

removes it from context so Claude never attempts it; listing it in

```
disallowedTools
```

(Python:

```
disallowed_tools
```

) blocks the call but leaves the tool visible, so Claude may waste a turn trying it. See

[[Configure permissions - Claude Code Docs-dbd6de|Configure permissions]]for the full evaluation order.

## Handle errors

How your handler reports errors determines whether the agent loop continues or stops:

What happensResultHandler throws an uncaught exceptionAgent loop stops. Claude never sees the error, and the

```
query
```

call fails.Handler catches the error and returns

```
isError: true
```

(TS) /

```
"is_error": True
```

(Python)Agent loop continues. Claude sees the error as data and can retry, try a different tool, or explain the failure.

```
try/except
```

(Python) or

```
try/catch
```

(TypeScript) and also returned as an error result. In both cases the handler returns normally and the agent loop continues.

## Return images and resources

The

```
content
```

array in a tool result accepts

```
text
```

,

```
image
```

, and

```
resource
```

blocks. You can mix them in the same response.

### Images

An image block carries the image bytes inline, encoded as base64. There is no URL field. To return an image that lives at a URL, fetch it in the handler, read the response bytes, and base64-encode them before returning. The result is processed as visual input.

FieldTypeNotes

```
type
```

```
"image"
```

```
data
```

```
string
```

Base64-encoded bytes. Raw base64 only, no

```
data:image/...;base64,
```

prefix

```
mimeType
```

```
string
```

Required. For example

```
image/png
```

,

```
image/jpeg
```

,

```
image/webp
```

,

```
image/gif
```

### Resources

A resource block embeds a piece of content identified by a URI. The URI is a label for Claude to reference; the actual content rides in the block’s

```
text
```

or

```
blob
```

field. Use this when your tool produces something that makes sense to address by name later, such as a generated file or a record from an external system.

FieldTypeNotes

```
type
```

```
"resource"
```

```
resource.uri
```

```
string
```

Identifier for the content. Any URI scheme

```
resource.text
```

```
string
```

The content, if it’s text. Provide this or

```
blob
```

, not both

```
resource.blob
```

```
string
```

The content base64-encoded, if it’s binary

```
resource.mimeType
```

```
string
```

Optional

```
file:///tmp/report.md
```

is a label that Claude can reference later; the SDK does not read from that path.

```
CallToolResult
```

type. See the

[MCP specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#tool-result)for the full definition.

## Example: unit converter

This tool converts values between units of length, temperature, and weight. A user can ask “convert 100 kilometers to miles” or “what is 72°F in Celsius,” and Claude picks the right unit type and units from the request. It demonstrates two patterns:

- Enum schemas:

  ```
  unit_type
  ```

  is constrained to a fixed set of values. In TypeScript, use

  ```
  z.enum()
  ```

  . In Python, the dict schema doesn’t support enums, so the full JSON Schema dict is required.
- Unsupported input handling: when a conversion pair isn’t found, the handler returns

  ```
  isError: true
  ```

  so Claude can tell the user what went wrong rather than treating a failure as a normal result.

```
query
```

the same way as the weather example. This example sends three different prompts in a loop to show the same tool handling different unit types. For each response, it inspects

```
AssistantMessage
```

objects (which contain the tool calls Claude made during that turn) and prints each

```
ToolUseBlock
```

before printing the final

```
ResultMessage
```

text. This lets you see when Claude is using the tool versus answering from its own knowledge.

## Next steps

Custom tools wrap async functions in a standard interface. You can mix the patterns on this page in the same server: a single server can hold a database tool, an API gateway tool, and an image renderer alongside each other. From here:

- If your server grows to dozens of tools, see [tool search](https://code.claude.com/docs/en/agent-sdk/tool-search)to defer loading them until Claude needs them.
- To connect to external MCP servers (filesystem, GitHub, Slack) instead of building your own, see [[Connect to external tools with MCP - Claude Code Docs|Connect MCP servers]].
- To control which tools run automatically versus requiring approval, see [[Configure permissions - Claude Code Docs-dbd6de|Configure permissions]].

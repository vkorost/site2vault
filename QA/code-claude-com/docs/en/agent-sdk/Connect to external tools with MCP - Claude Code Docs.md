---
title: Connect to external tools with MCP - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/mcp
description: Configure MCP servers to extend your agent with external tools. Covers
  transport types, tool search for large tool sets, authentication, and error handling.
---

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro)is an open standard for connecting AI agents to external tools and data sources. With MCP, your agent can query databases, integrate with APIs like Slack and GitHub, and connect to other services without writing custom tool implementations. MCP servers can run as local processes, connect over HTTP, or execute directly within your SDK application.

## Quickstart

This example connects to the

[Claude Code documentation](https://code.claude.com/docs)MCP server using

[[Connect to external tools with MCP - Claude Code Docs#HTTP/SSE servers|HTTP transport]]and uses

[[Connect to external tools with MCP - Claude Code Docs#Allow MCP tools|with a wildcard to permit all tools from the server.]]

```
allowedTools
```

## Add an MCP server

You can configure MCP servers in code when calling

```
query()
```

, or in a

```
.mcp.json
```

file loaded via

[[Connect to external tools with MCP - Claude Code Docs#From a config file|.]]

```
settingSources
```

### In code

Pass MCP servers directly in the

```
mcpServers
```

option:

### From a config file

Create a

```
.mcp.json
```

file at your project root. The file is picked up when the

```
project
```

setting source is enabled, which it is for default

```
query()
```

options. If you set

```
settingSources
```

explicitly, include

```
"project"
```

for this file to load:

## Allow MCP tools

MCP tools require explicit permission before Claude can use them. Without permission, Claude will see that tools are available but won’t be able to call them.

### Tool naming convention

MCP tools follow the naming pattern

```
mcp__<server-name>__<tool-name>
```

. For example, a GitHub server named

```
"github"
```

with a

```
list_issues
```

tool becomes

```
mcp__github__list_issues
```

.

### Grant access with allowedTools

Use

```
allowedTools
```

to specify which MCP tools Claude can use:

```
*
```

) let you allow all tools from a server without listing each one individually.

Prefer

```
allowedTools
```

over permission modes for MCP access.

```
permissionMode: "acceptEdits"
```

does not auto-approve MCP tools (only file edits and filesystem Bash commands).

```
permissionMode: "bypassPermissions"
```

does auto-approve MCP tools but also disables all other safety prompts, which is broader than necessary. A wildcard in

```
allowedTools
```

grants exactly the MCP server you want and nothing more. See [[Configure permissions - Claude Code Docs-dbd6de#Permission modes|Permission modes]]for a full comparison.

### Discover available tools

To see what tools an MCP server provides, check the server’s documentation or connect to the server and inspect the

```
system
```

init message:

## Transport types

MCP servers communicate with your agent using different transport protocols. Check the server’s documentation to see which transport it supports:

- If the docs give you a command to run (like

  ```
  npx @modelcontextprotocol/server-github
  ```

  ), use stdio
- If the docs give you a URL, use HTTP or SSE
- If you’re building your own tools in code, use an SDK MCP server

### stdio servers

Local processes that communicate via stdin/stdout. Use this for MCP servers you run on the same machine:

- In code
- .mcp.json

### HTTP/SSE servers

Use HTTP or SSE for cloud-hosted MCP servers and remote APIs:

- In code
- .mcp.json

```
"type": "http"
```

instead.

### SDK MCP servers

Define custom tools directly in your application code instead of running a separate server process. See the

[[Give Claude custom tools - Claude Code Docs|custom tools guide]]for implementation details.

## MCP tool search

When you have many MCP tools configured, tool definitions can consume a significant portion of your context window. Tool search solves this by withholding tool definitions from context and loading only the ones Claude needs for each turn. Tool search is enabled by default. See

[Tool search](https://code.claude.com/docs/en/agent-sdk/tool-search)for configuration options and details. For more detail, including best practices and using tool search with custom SDK tools, see the

[tool search guide](https://code.claude.com/docs/en/agent-sdk/tool-search).

## Authentication

Most MCP servers require authentication to access external services. Pass credentials through environment variables in the server configuration.

### Pass credentials via environment variables

Use the

```
env
```

field to pass API keys, tokens, and other credentials to the MCP server:

- In code
- .mcp.json

[[Connect to external tools with MCP - Claude Code Docs#List issues from a repository|List issues from a repository]]for a complete working example with debug logging.

### HTTP headers for remote servers

For HTTP and SSE servers, pass authentication headers directly in the server configuration:

- In code
- .mcp.json

### OAuth2 authentication

The

[MCP specification supports OAuth 2.1](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization)for authorization. The SDK doesn’t handle OAuth flows automatically, but you can pass access tokens via headers after completing the OAuth flow in your application:

## Examples

### List issues from a repository

This example connects to the

[GitHub MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/github)to list recent issues. The example includes debug logging to verify the MCP connection and tool calls. Before running, create a

[GitHub personal access token](https://github.com/settings/tokens)with

```
repo
```

scope and set it as an environment variable:

### Query a database

This example uses the

[Postgres MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres)to query a database. The connection string is passed as an argument to the server. The agent automatically discovers the database schema, writes the SQL query, and returns the results:

## Error handling

MCP servers can fail to connect for various reasons: the server process might not be installed, credentials might be invalid, or a remote server might be unreachable. The SDK emits a

```
system
```

message with subtype

```
init
```

at the start of each query. This message includes the connection status for each MCP server. Check the

```
status
```

field to detect connection failures before the agent starts working:

## Troubleshooting

### Server shows “failed” status

Check the

```
init
```

message to see which servers failed to connect:

- Missing environment variables: Ensure required tokens and credentials are set. For stdio servers, check the

  ```
  env
  ```

  field matches what the server expects.
- Server not installed: For

  ```
  npx
  ```

  commands, verify the package exists and Node.js is in your PATH.
- Invalid connection string: For database servers, verify the connection string format and that the database is accessible.
- Network issues: For remote HTTP/SSE servers, check the URL is reachable and any firewalls allow the connection.

### Tools not being called

If Claude sees tools but doesn’t use them, check that you’ve granted permission with

```
allowedTools
```

:

### Connection timeouts

The MCP SDK has a default timeout of 60 seconds for server connections. If your server takes longer to start, the connection will fail. For servers that need more startup time, consider:

- Using a lighter-weight server if available
- Pre-warming the server before starting your agent
- Checking server logs for slow initialization causes

## Related resources

- [[Give Claude custom tools - Claude Code Docs|Custom tools guide]]: Build your own MCP server that runs in-process with your SDK application
- [[Configure permissions - Claude Code Docs-dbd6de|Permissions]]: Control which MCP tools your agent can use with

  ```
  allowedTools
  ```

  and

  ```
  disallowedTools
  ```
- [[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript SDK reference]]: Full API reference including MCP configuration options
- [[Agent SDK reference - Python - Claude Code Docs|Python SDK reference]]: Full API reference including MCP configuration options
- [MCP server directory](https://github.com/modelcontextprotocol/servers): Browse available MCP servers for databases, APIs, and more

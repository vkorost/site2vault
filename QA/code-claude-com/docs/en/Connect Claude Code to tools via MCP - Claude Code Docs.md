---
title: Connect Claude Code to tools via MCP - Claude Code Docs
source_url: https://code.claude.com/docs/en/mcp
description: Learn how to connect Claude Code to your tools with the Model Context
  Protocol.
---

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), an open source standard for AI-tool integrations. MCP servers give Claude Code access to your tools, databases, and APIs. Connect a server when you find yourself copying data into chat from another tool, like an issue tracker or a monitoring dashboard. Once connected, Claude can read and act on that system directly instead of working from what you paste.

## What you can do with MCP

With MCP servers connected, you can ask Claude Code to:

- Implement features from issue trackers: “Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub.”
- Analyze monitoring data: “Check Sentry and Statsig to check the usage of the feature described in ENG-4521.”
- Query databases: “Find emails of 10 random users who used feature ENG-4521, based on our PostgreSQL database.”
- Integrate designs: “Update our standard email template based on the new Figma designs that were posted in Slack”
- Automate workflows: “Create Gmail drafts inviting these 10 users to a feedback session about the new feature.”
- React to external events: An MCP server can also act as a [[Push events into a running session with channels - Claude Code Docs|channel]]that pushes messages into your session, so Claude reacts to Telegram messages, Discord chats, or webhook events while you’re away.

## Popular MCP servers

Here are some commonly used MCP servers you can connect to Claude Code:

Need a specific integration?

[Find hundreds more MCP servers on GitHub](https://github.com/modelcontextprotocol/servers), or build your own using the[MCP SDK](https://modelcontextprotocol.io/quickstart/server).

## Installing MCP servers

MCP servers can be configured in three different ways depending on your needs:

### Option 1: Add a remote HTTP server

HTTP servers are the recommended option for connecting to remote MCP servers. This is the most widely supported transport for cloud-based services.

### Option 2: Add a remote SSE server

### Option 3: Add a local stdio server

Stdio servers run as local processes on your machine. They’re ideal for tools that need direct system access or custom scripts.

Important: Option orderingAll options (

```
--transport
```

,

```
--env
```

,

```
--scope
```

,

```
--header
```

) must come before the server name. The

```
--
```

(double dash) then separates the server name from the command and arguments that get passed to the MCP server.For example:

- ```
  claude mcp add --transport stdio myserver -- npx server
  ```

  → runs

  ```
  npx server
  ```
- ```
  claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080
  ```

  → runs

  ```
  python server.py --port 8080
  ```

  with

  ```
  KEY=value
  ```

  in environment

### Managing your servers

Once configured, you can manage your MCP servers with these commands:

### Dynamic tool updates

Claude Code supports MCP

```
list_changed
```

notifications, allowing MCP servers to dynamically update their available tools, prompts, and resources without requiring you to disconnect and reconnect. When an MCP server sends a

```
list_changed
```

notification, Claude Code automatically refreshes the available capabilities from that server.

### Automatic reconnection

If an HTTP or SSE server disconnects mid-session, Claude Code automatically reconnects with exponential backoff: up to five attempts, starting at a one-second delay and doubling each time. The server appears as pending in

```
/mcp
```

while reconnection is in progress. After five failed attempts the server is marked as failed and you can retry manually from

```
/mcp
```

. Stdio servers are local processes and are not reconnected automatically.

### Push messages with channels

An MCP server can also push messages directly into your session so Claude can react to external events like CI results, monitoring alerts, or chat messages. To enable this, your server declares the

```
claude/channel
```

capability and you opt it in with the

```
--channels
```

flag at startup. See

[[Push events into a running session with channels - Claude Code Docs|Channels]]to use an officially supported channel, or

[[Channels reference - Claude Code Docs|Channels reference]]to build your own.

### Plugin-provided MCP servers

[[Create plugins - Claude Code Docs|Plugins]]can bundle MCP servers, automatically providing tools and integrations when the plugin is enabled. Plugin MCP servers work identically to user-configured servers. How plugin MCP servers work:

- Plugins define MCP servers in

  ```
  .mcp.json
  ```

  at the plugin root or inline in

  ```
  plugin.json
  ```
- When a plugin is enabled, its MCP servers start automatically
- Plugin MCP tools appear alongside manually configured MCP tools
- Plugin servers are managed through plugin installation (not

  ```
  /mcp
  ```

  commands)

```
.mcp.json
```

at plugin root:

```
plugin.json
```

:

- Automatic lifecycle: At session startup, servers for enabled plugins connect automatically. If you enable or disable a plugin during a session, run

  ```
  /reload-plugins
  ```

  to connect or disconnect its MCP servers
- Environment variables: use

  ```
  ${CLAUDE_PLUGIN_ROOT}
  ```

  for bundled plugin files and

  ```
  ${CLAUDE_PLUGIN_DATA}
  ```

  for[[Plugins reference - Claude Code Docs#Persistent data directory|persistent state]]that survives plugin updates
- User environment access: Access to same environment variables as manually configured servers
- Multiple transport types: Support stdio, SSE, and HTTP transports (transport support may vary by server)

- Bundled distribution: Tools and servers packaged together
- Automatic setup: No manual MCP configuration needed
- Team consistency: Everyone gets the same tools when plugin is installed

[[Plugins reference - Claude Code Docs#MCP servers|plugin components reference]]for details on bundling MCP servers with plugins.

## MCP installation scopes

MCP servers can be configured at three scopes. The scope you choose controls which projects the server loads in and whether the configuration is shared with your team.

### Local scope

Local scope is the default. A local-scoped server loads only in the project where you added it and stays private to you. Claude Code stores it in

```
~/.claude.json
```

under that project’s path, so the same server won’t appear in your other projects. Use local scope for personal development servers, experimental configurations, or servers with credentials you don’t want in version control.

The term “local scope” for MCP servers differs from general local settings. MCP local-scoped servers are stored in

```
~/.claude.json
```

(your home directory), while general local settings use

```
.claude/settings.local.json
```

(in the project directory). See [[Claude Code settings - Claude Code Docs#Settings files|Settings]]for details on settings file locations.

```
~/.claude.json
```

. The example below shows the result when you run it from

```
/path/to/your/project
```

:

### Project scope

Project-scoped servers enable team collaboration by storing configurations in a

```
.mcp.json
```

file at your project’s root directory. This file is designed to be checked into version control, ensuring all team members have access to the same MCP tools and services. When you add a project-scoped server, Claude Code automatically creates or updates this file with the appropriate configuration structure.

```
.mcp.json
```

file follows a standardized format:

```
.mcp.json
```

files. If you need to reset these approval choices, use the

```
claude mcp reset-project-choices
```

command.

### User scope

User-scoped servers are stored in

```
~/.claude.json
```

and provide cross-project accessibility, making them available across all projects on your machine while remaining private to your user account. This scope works well for personal utility servers, development tools, or services you frequently use across different projects.

### Scope hierarchy and precedence

When the same server is defined in more than one place, Claude Code connects to it once, using the definition from the highest-precedence source:

- Local scope
- Project scope
- User scope
- [[Create plugins - Claude Code Docs|Plugin-provided servers]]
- [[Connect Claude Code to tools via MCP - Claude Code Docs|claude.ai connectors]]

### Environment variable expansion in ``` .mcp.json ```

Claude Code supports environment variable expansion in

```
.mcp.json
```

files, allowing teams to share configurations while maintaining flexibility for machine-specific paths and sensitive values like API keys.
Supported syntax:

- ```
  ${VAR}
  ```

  - Expands to the value of environment variable

  ```
  VAR
  ```
- ```
  ${VAR:-default}
  ```

  - Expands to

  ```
  VAR
  ```

  if set, otherwise uses

  ```
  default
  ```

- ```
  command
  ```

  - The server executable path
- ```
  args
  ```

  - Command-line arguments
- ```
  env
  ```

  - Environment variables passed to the server
- ```
  url
  ```

  - For HTTP server types
- ```
  headers
  ```

  - For HTTP server authentication

## Practical examples

### Example: Monitor errors with Sentry

### Example: Connect to GitHub for code reviews

GitHub’s remote MCP server authenticates with a GitHub personal access token passed as a header. To get one, open your

[GitHub token settings](https://github.com/settings/personal-access-tokens), generate a new fine-grained token with access to the repositories you want Claude to work with, then add the server:

### Example: Query your PostgreSQL database

## Authenticate with remote MCP servers

Many cloud-based MCP servers require authentication. Claude Code supports OAuth 2.0 for secure connections.

### Use a fixed OAuth callback port

Some MCP servers require a specific redirect URI registered in advance. By default, Claude Code picks a random available port for the OAuth callback. Use

```
--callback-port
```

to fix the port so it matches a pre-registered redirect URI of the form

```
http://localhost:PORT/callback
```

.
You can use

```
--callback-port
```

on its own (with dynamic client registration) or together with

```
--client-id
```

(with pre-configured credentials).

### Use pre-configured OAuth credentials

Some MCP servers don’t support automatic OAuth setup via Dynamic Client Registration. If you see an error like “Incompatible auth server: does not support dynamic client registration,” the server requires pre-configured credentials. Claude Code also supports servers that use a Client ID Metadata Document (CIMD) instead of Dynamic Client Registration, and discovers these automatically. If automatic discovery fails, register an OAuth app through the server’s developer portal first, then provide the credentials when adding the server.

Register an OAuth app with the server

Create an app through the server’s developer portal and note your client ID and client secret.Many servers also require a redirect URI. If so, choose a port and register a redirect URI in the format

```
http://localhost:PORT/callback
```

. Use that same port with

```
--callback-port
```

in the next step.

Add the server with your credentials

Choose one of the following methods. The port used for

```
--callback-port
```

can be any available port. It just needs to match the redirect URI you registered in the previous step.

- claude mcp add
- claude mcp add-json
- claude mcp add-json (callback port only)
- CI / env var

Use

```
--client-id
```

to pass your app’s client ID. The

```
--client-secret
```

flag prompts for the secret with masked input:

### Override OAuth metadata discovery

Point Claude Code at a specific OAuth authorization server metadata URL to bypass the default discovery chain. Set

```
authServerMetadataUrl
```

when the MCP server’s standard endpoints error, or when you want to route discovery through an internal proxy. By default, Claude Code first checks RFC 9728 Protected Resource Metadata at

```
/.well-known/oauth-protected-resource
```

, then falls back to RFC 8414 authorization server metadata at

```
/.well-known/oauth-authorization-server
```

.
Set

```
authServerMetadataUrl
```

in the

```
oauth
```

object of your server’s config in

```
.mcp.json
```

:

```
https://
```

.

```
authServerMetadataUrl
```

requires Claude Code v2.1.64 or later. The metadata URL’s

```
scopes_supported
```

overrides the scopes the upstream server advertises.

### Restrict OAuth scopes

Set

```
oauth.scopes
```

to pin the scopes Claude Code requests during the authorization flow. This is the supported way to restrict an MCP server to a security-team-approved subset when the upstream authorization server advertises more scopes than you want to grant. The value is a single space-separated string, matching the

```
scope
```

parameter format in RFC 6749 §3.3.

```
oauth.scopes
```

takes precedence over both

```
authServerMetadataUrl
```

and the scopes the server discovers at

```
/.well-known
```

. Leave it unset to let the MCP server determine the requested scope set.
If the authorization server advertises

```
offline_access
```

in

```
scopes_supported
```

, Claude Code appends it to the pinned scopes so the access token can be refreshed without a new browser sign-in.
If the server later returns a 403

```
insufficient_scope
```

for a tool call, Claude Code re-authenticates with the same pinned scopes. Widen

```
oauth.scopes
```

when a tool you need requires a scope outside the pin.

### Use dynamic headers for custom authentication

If your MCP server uses an authentication scheme other than OAuth (such as Kerberos, short-lived tokens, or an internal SSO), use

```
headersHelper
```

to generate request headers at connection time. Claude Code runs the command and merges its output into the connection headers.

- The command must write a JSON object of string key-value pairs to stdout
- The command runs in a shell with a 10-second timeout
- Dynamic headers override any static

  ```
  headers
  ```

  with the same name

VariableValue

```
CLAUDE_CODE_MCP_SERVER_NAME
```

the name of the MCP server

```
CLAUDE_CODE_MCP_SERVER_URL
```

the URL of the MCP server

```
headersHelper
```

executes arbitrary shell commands. When defined at project or local scope, it only runs after you accept the workspace trust dialog.

## Add MCP servers from JSON configuration

If you have a JSON configuration for an MCP server, you can add it directly:

## Import MCP servers from Claude Desktop

If you’ve already configured MCP servers in Claude Desktop, you can import them:

Select which servers to import

After running the command, you’ll see an interactive dialog that allows you to select which servers you want to import.

## Use MCP servers from Claude.ai

If you’ve logged into Claude Code with a

[Claude.ai](https://claude.ai)account, MCP servers you’ve added in Claude.ai are automatically available in Claude Code:

Configure MCP servers in Claude.ai

Add servers at

[claude.ai/customize/connectors](https://claude.ai/customize/connectors). On Team and Enterprise plans, only admins can add servers.

```
ENABLE_CLAUDEAI_MCP_SERVERS
```

environment variable to

```
false
```

:

## Use Claude Code as an MCP server

You can use Claude Code itself as an MCP server that other applications can connect to:

## MCP output limits and warnings

When MCP tools produce large outputs, Claude Code helps manage the token usage to prevent overwhelming your conversation context:

- Output warning threshold: Claude Code displays a warning when any MCP tool output exceeds 10,000 tokens
- Configurable limit: you can adjust the maximum allowed MCP output tokens using the

  ```
  MAX_MCP_OUTPUT_TOKENS
  ```

  environment variable
- Default limit: the default maximum is 25,000 tokens
- Scope: the environment variable applies to tools that don’t declare their own limit. Tools that set use that value instead for text content, regardless of what

  ```
  anthropic/maxResultSizeChars
  ```

  ```
  MAX_MCP_OUTPUT_TOKENS
  ```

  is set to. Tools that return image data are still subject to

  ```
  MAX_MCP_OUTPUT_TOKENS
  ```

- Query large datasets or databases
- Generate detailed reports or documentation
- Process extensive log files or debugging information

### Raise the limit for a specific tool

If you’re building an MCP server, you can allow individual tools to return results larger than the default persist-to-disk threshold by setting

```
_meta["anthropic/maxResultSizeChars"]
```

in the tool’s

```
tools/list
```

response entry. Claude Code raises that tool’s threshold to the annotated value, up to a hard ceiling of 500,000 characters.
This is useful for tools that return inherently large but necessary outputs, such as database schemas or full file trees. Without the annotation, results that exceed the default threshold are persisted to disk and replaced with a file reference in the conversation.

```
MAX_MCP_OUTPUT_TOKENS
```

for text content, so users don’t need to raise the environment variable for tools that declare it. Tools that return image data are still subject to the token limit.

## Respond to MCP elicitation requests

MCP servers can request structured input from you mid-task using elicitation. When a server needs information it can’t get on its own, Claude Code displays an interactive dialog and passes your response back to the server. No configuration is required on your side: elicitation dialogs appear automatically when a server requests them. Servers can request input in two ways:

- Form mode: Claude Code shows a dialog with form fields defined by the server (for example, a username and password prompt). Fill in the fields and submit.
- URL mode: Claude Code opens a browser URL for authentication or approval. Complete the flow in the browser, then confirm in the CLI.

[[Hooks reference - Claude Code Docs#Elicitation|. If you’re building an MCP server that uses elicitation, see the]]

```
Elicitation
```

hook

[MCP elicitation specification](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation)for protocol details and schema examples.

## Use MCP resources

MCP servers can expose resources that you can reference using @ mentions, similar to how you reference files.

### Reference MCP resources

List available resources

Type

```
@
```

in your prompt to see available resources from all connected MCP servers. Resources appear alongside files in the autocomplete menu.

Reference a specific resource

Use the format

```
@server:protocol://resource/path
```

to reference a resource:

## Scale with MCP Tool Search

Tool search keeps MCP context usage low by deferring tool definitions until Claude needs them. Only tool names load at session start, so adding more MCP servers has minimal impact on your context window.

### How it works

Tool search is enabled by default. MCP tools are deferred rather than loaded into context upfront, and Claude uses a search tool to discover relevant ones when a task needs them. Only the tools Claude actually uses enter context. From your perspective, MCP tools work exactly as before. If you prefer threshold-based loading, set

```
ENABLE_TOOL_SEARCH=auto
```

to load schemas upfront when they fit within 10% of the context window and defer only the overflow. See

[[Connect Claude Code to tools via MCP - Claude Code Docs#Configure tool search|Configure tool search]]for all options.

### For MCP server authors

If you’re building an MCP server, the server instructions field becomes more useful with Tool Search enabled. Server instructions help Claude understand when to search for your tools, similar to how

[[Extend Claude with skills - Claude Code Docs|skills]]work. Add clear, descriptive server instructions that explain:

- What category of tasks your tools handle
- When Claude should search for your tools
- Key capabilities your server provides

### Configure tool search

Tool search is enabled by default: MCP tools are deferred and discovered on demand. It is disabled by default on Vertex AI, which does not accept the tool search beta header, and when

```
ANTHROPIC_BASE_URL
```

points to a non-first-party host, since most proxies do not forward

```
tool_reference
```

blocks. Set

```
ENABLE_TOOL_SEARCH
```

explicitly to opt in. This feature requires models that support

```
tool_reference
```

blocks: Sonnet 4 and later, or Opus 4 and later. Haiku models do not support tool search.
Control tool search behavior with the

```
ENABLE_TOOL_SEARCH
```

environment variable:

ValueBehavior(unset)All MCP tools deferred and loaded on demand. Falls back to loading upfront on Vertex AI or when

```
ANTHROPIC_BASE_URL
```

is a non-first-party host

```
true
```

All MCP tools deferred, including on Vertex AI and for non-first-party

```
ANTHROPIC_BASE_URL
```

```
auto
```

Threshold mode: tools load upfront if they fit within 10% of the context window, deferred otherwise

```
auto:<N>
```

Threshold mode with a custom percentage, where

```
<N>
```

is 0-100 (e.g.,

```
auto:5
```

for 5%)

```
false
```

All MCP tools loaded upfront, no deferral

[[Claude Code settings - Claude Code Docs#Available settings|settings.json]]. You can also disable the

```
env
```

field

```
ToolSearch
```

tool specifically:

## Use MCP prompts as commands

MCP servers can expose prompts that become available as commands in Claude Code.

### Execute MCP prompts

Discover available prompts

Type

```
/
```

to see all available commands, including those from MCP servers. MCP prompts appear with the format

```
/mcp__servername__promptname
```

.

## Managed MCP configuration

For organizations that need centralized control over MCP servers, Claude Code supports two configuration options:

- Exclusive control with

  ```
  managed-mcp.json
  ```

  : Deploy a fixed set of MCP servers that users cannot modify or extend
- Policy-based control with allowlists/denylists: Allow users to add their own servers, but restrict which ones are permitted

- Control which MCP servers employees can access: Deploy a standardized set of approved MCP servers across the organization
- Prevent unauthorized MCP servers: Restrict users from adding unapproved MCP servers
- Disable MCP entirely: Remove MCP functionality completely if needed

### Option 1: Exclusive control with managed-mcp.json

When you deploy a

```
managed-mcp.json
```

file, it takes exclusive control over all MCP servers. Users cannot add, modify, or use any MCP servers other than those defined in this file. This is the simplest approach for organizations that want complete control.
System administrators deploy the configuration file to a system-wide directory:

- macOS:

  ```
  /Library/Application Support/ClaudeCode/managed-mcp.json
  ```
- Linux and WSL:

  ```
  /etc/claude-code/managed-mcp.json
  ```
- Windows:

  ```
  C:\Program Files\ClaudeCode\managed-mcp.json
  ```

These are system-wide paths (not user home directories like

```
~/Library/...
```

) that require administrator privileges. They are designed to be deployed by IT administrators.

```
managed-mcp.json
```

file uses the same format as a standard

```
.mcp.json
```

file:

### Option 2: Policy-based control with allowlists and denylists

Instead of taking exclusive control, administrators can allow users to configure their own MCP servers while enforcing restrictions on which servers are permitted. This approach uses

```
allowedMcpServers
```

and

```
deniedMcpServers
```

in the

[[Claude Code settings - Claude Code Docs#Settings files|managed settings file]].

Choosing between options: Use Option 1 (

```
managed-mcp.json
```

) when you want to deploy a fixed set of servers with no user customization. Use Option 2 (allowlists/denylists) when you want to allow users to add their own servers within policy constraints.

#### Restriction options

Each entry in the allowlist or denylist can restrict servers in three ways:

- By server name (

  ```
  serverName
  ```

  ): Matches the configured name of the server
- By command (

  ```
  serverCommand
  ```

  ): Matches the exact command and arguments used to start stdio servers
- By URL pattern (

  ```
  serverUrl
  ```

  ): Matches remote server URLs with wildcard support

```
serverName
```

,

```
serverCommand
```

, or

```
serverUrl
```

.

#### Example configuration

#### How command-based restrictions work

Exact matching:

- Command arrays must match exactly - both the command and all arguments in the correct order
- Example:

  ```
  ["npx", "-y", "server"]
  ```

  will NOT match

  ```
  ["npx", "server"]
  ```

  or

  ```
  ["npx", "-y", "server", "--flag"]
  ```

- When the allowlist contains any

  ```
  serverCommand
  ```

  entries, stdio servers must match one of those commands
- Stdio servers cannot pass by name alone when command restrictions are present
- This ensures administrators can enforce which commands are allowed to run

- Remote servers (HTTP, SSE, WebSocket) use URL-based matching when

  ```
  serverUrl
  ```

  entries exist in the allowlist
- If no URL entries exist, remote servers fall back to name-based matching
- Command restrictions do not apply to remote servers

#### How URL-based restrictions work

URL patterns support wildcards using

```
*
```

to match any sequence of characters. This is useful for allowing entire domains or subdomains.
Wildcard examples:

- ```
  https://mcp.company.com/*
  ```

  - Allow all paths on a specific domain
- ```
  https://*.example.com/*
  ```

  - Allow any subdomain of example.com
- ```
  http://localhost:*/*
  ```

  - Allow any port on localhost

- When the allowlist contains any

  ```
  serverUrl
  ```

  entries, remote servers must match one of those URL patterns
- Remote servers cannot pass by name alone when URL restrictions are present
- This ensures administrators can enforce which remote endpoints are allowed

###

Example: URL-only allowlist

Example: URL-only allowlist

- HTTP server at

  ```
  https://mcp.company.com/api
  ```

  : ✅ Allowed (matches URL pattern)
- HTTP server at

  ```
  https://api.internal.corp/mcp
  ```

  : ✅ Allowed (matches wildcard subdomain)
- HTTP server at

  ```
  https://external.com/mcp
  ```

  : ❌ Blocked (doesn’t match any URL pattern)
- Stdio server with any command: ❌ Blocked (no name or command entries to match)

###

Example: Command-only allowlist

Example: Command-only allowlist

- Stdio server with

  ```
  ["npx", "-y", "approved-package"]
  ```

  : ✅ Allowed (matches command)
- Stdio server with

  ```
  ["node", "server.js"]
  ```

  : ❌ Blocked (doesn’t match command)
- HTTP server named “my-api”: ❌ Blocked (no name entries to match)

###

Example: Mixed name and command allowlist

Example: Mixed name and command allowlist

- Stdio server named “local-tool” with

  ```
  ["npx", "-y", "approved-package"]
  ```

  : ✅ Allowed (matches command)
- Stdio server named “local-tool” with

  ```
  ["node", "server.js"]
  ```

  : ❌ Blocked (command entries exist but doesn’t match)
- Stdio server named “github” with

  ```
  ["node", "server.js"]
  ```

  : ❌ Blocked (stdio servers must match commands when command entries exist)
- HTTP server named “github”: ✅ Allowed (matches name)
- HTTP server named “other-api”: ❌ Blocked (name doesn’t match)

###

Example: Name-only allowlist

Example: Name-only allowlist

- Stdio server named “github” with any command: ✅ Allowed (no command restrictions)
- Stdio server named “internal-tool” with any command: ✅ Allowed (no command restrictions)
- HTTP server named “github”: ✅ Allowed (matches name)
- Any server named “other”: ❌ Blocked (name doesn’t match)

#### Allowlist behavior ( ``` allowedMcpServers ``` )

- ```
  undefined
  ```

  (default): No restrictions - users can configure any MCP server
- Empty array

  ```
  []
  ```

  : Complete lockdown - users cannot configure any MCP servers
- List of entries: Users can only configure servers that match by name, command, or URL pattern

#### Denylist behavior ( ``` deniedMcpServers ``` )

- ```
  undefined
  ```

  (default): No servers are blocked
- Empty array

  ```
  []
  ```

  : No servers are blocked
- List of entries: Specified servers are explicitly blocked across all scopes

#### Important notes

- Option 1 and Option 2 can be combined: If

  ```
  managed-mcp.json
  ```

  exists, it has exclusive control and users cannot add servers. Allowlists/denylists still apply to the managed servers themselves.
- Denylist takes absolute precedence: If a server matches a denylist entry (by name, command, or URL), it will be blocked even if it’s on the allowlist
- Name-based, command-based, and URL-based restrictions work together: a server passes if it matches either a name entry, a command entry, or a URL pattern (unless blocked by denylist)

When using

```
managed-mcp.json
```

: Users cannot add MCP servers through

```
claude mcp add
```

or configuration files. The

```
allowedMcpServers
```

and

```
deniedMcpServers
```

settings still apply to filter which managed servers are actually loaded.

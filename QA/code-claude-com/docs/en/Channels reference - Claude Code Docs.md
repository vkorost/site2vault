---
title: Channels reference - Claude Code Docs
source_url: https://code.claude.com/docs/en/channels-reference
description: 'Build an MCP server that pushes webhooks, alerts, and chat messages
  into a Claude Code session. Reference for the channel contract: capability declaration,
  noti'
---

Channels are in

[[Push events into a running session with channels - Claude Code Docs#Research preview|research preview]]and require Claude Code v2.1.80 or later. They require claude.ai login. Console and API key authentication is not supported. Team and Enterprise organizations must[[Push events into a running session with channels - Claude Code Docs#Enterprise controls|explicitly enable them]].

[[Channels reference - Claude Code Docs#Expose a reply tool|expose a reply tool]]so Claude can send messages back. A channel with a trusted sender path can also opt in to

[[Channels reference - Claude Code Docs#Relay permission prompts|relay permission prompts]]so you can approve or deny tool use remotely. This page covers:

- [[Channels reference - Claude Code Docs#Overview|Overview]]: how channels work
- [[Channels reference - Claude Code Docs#What you need|What you need]]: requirements and general steps
- [[Channels reference - Claude Code Docs#Example: build a webhook receiver|Example: build a webhook receiver]]: a minimal one-way walkthrough
- [[Channels reference - Claude Code Docs#Server options|Server options]]: the constructor fields
- [[Channels reference - Claude Code Docs#Notification format|Notification format]]: the event payload
- [[Channels reference - Claude Code Docs#Expose a reply tool|Expose a reply tool]]: let Claude send messages back
- [[Channels reference - Claude Code Docs#Gate inbound messages|Gate inbound messages]]: sender checks to prevent prompt injection
- [[Channels reference - Claude Code Docs#Relay permission prompts|Relay permission prompts]]: forward tool approval prompts to remote channels

[[Push events into a running session with channels - Claude Code Docs|Channels]]. Telegram, Discord, iMessage, and fakechat are included in the research preview.

## Overview

A channel is an

[MCP](https://modelcontextprotocol.io)server that runs on the same machine as Claude Code. Claude Code spawns it as a subprocess and communicates over stdio. Your channel server is the bridge between external systems and the Claude Code session:

- Chat platforms (Telegram, Discord): your plugin runs locally and polls the platform’s API for new messages. When someone DMs your bot, the plugin receives the message and forwards it to Claude. No URL to expose.
- Webhooks (CI, monitoring): your server listens on a local HTTP port. External systems POST to that port, and your server pushes the payload to Claude.

## What you need

The only hard requirement is the

[package and a Node.js-compatible runtime.](https://www.npmjs.com/package/@modelcontextprotocol/sdk)

```
@modelcontextprotocol/sdk
```

[Bun](https://bun.sh),

[Node](https://nodejs.org), and

[Deno](https://deno.com)all work. The pre-built plugins in the research preview use Bun, but your channel doesn’t have to. Your server needs to:

- Declare the

  ```
  claude/channel
  ```

  capability so Claude Code registers a notification listener
- Emit

  ```
  notifications/claude/channel
  ```

  events when something happens
- Connect over [stdio transport](https://modelcontextprotocol.io/docs/concepts/transports#standard-io)(Claude Code spawns your server as a subprocess)

[[Channels reference - Claude Code Docs#Server options|Server options]]and

[[Channels reference - Claude Code Docs#Notification format|Notification format]]sections cover each of these in detail. See

[[Channels reference - Claude Code Docs#Example: build a webhook receiver|Example: build a webhook receiver]]for a full walkthrough. During the research preview, custom channels aren’t on the

[[Push events into a running session with channels - Claude Code Docs#Supported channels|approved allowlist]]. Use

```
--dangerously-load-development-channels
```

to test locally. See

[[Channels reference - Claude Code Docs#Test during the research preview|Test during the research preview]]for details.

## Example: build a webhook receiver

This walkthrough builds a single-file server that listens for HTTP requests and forwards them into your Claude Code session. By the end, anything that can send an HTTP POST, like a CI pipeline, a monitoring alert, or a

```
curl
```

command, can push events to Claude.
This example uses

[Bun](https://bun.sh)as the runtime for its built-in HTTP server and TypeScript support. You can use

[Node](https://nodejs.org)or

[Deno](https://deno.com)instead; the only requirement is the

[MCP SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk).

Write the channel server

Create a file called The file does three things in order:

```
webhook.ts
```

. This is your entire channel server: it connects to Claude Code over stdio, and it listens for HTTP POSTs on port 8788. When a request arrives, it pushes the body to Claude as a channel event.

webhook.ts

- Server configuration: creates the MCP server with

  ```
  claude/channel
  ```

  in its capabilities, which is what tells Claude Code this is a channel. Thestring goes into Claude’s system prompt: tell Claude what events to expect, whether to reply, and how to route replies if it should.

  ```
  instructions
  ```
- Stdio connection: connects to Claude Code over stdin/stdout. This is standard for any [MCP server](https://modelcontextprotocol.io/docs/concepts/transports#standard-io): Claude Code spawns it as a subprocess.
- HTTP listener: starts a local web server on port 8788. Every POST body gets forwarded to Claude as a channel event via

  ```
  mcp.notification()
  ```

  . The

  ```
  content
  ```

  becomes the event body, and each

  ```
  meta
  ```

  entry becomes an attribute on the

  ```
  <channel>
  ```

  tag. The listener needs access to the

  ```
  mcp
  ```

  instance, so it runs in the same process. You could split it into separate modules for a larger project.

Register your server with Claude Code

Add the server to your MCP config so Claude Code knows how to start it. For a project-level Claude Code reads your MCP config at startup and spawns each server as a subprocess.

```
.mcp.json
```

in the same directory, use a relative path. For user-level config in

```
~/.claude.json
```

, use the full absolute path so the server can be found from any project:

.mcp.json

Test it

During the research preview, custom channels aren’t on the allowlist, so start Claude Code with the development flag:When Claude Code starts, it reads your MCP config, spawns your The payload arrives in your Claude Code session as a In your Claude Code terminal, you’ll see Claude receive the message and start responding: reading files, running commands, or whatever the message calls for. This is a one-way channel, so Claude acts in your session but doesn’t send anything back through the webhook. To add replies, see

```
webhook.ts
```

as a subprocess, and the HTTP listener starts automatically on the port you configured (8788 in this example). You don’t need to run the server yourself.If you see “blocked by org policy,” your Team or Enterprise admin needs to [[Push events into a running session with channels - Claude Code Docs#Enterprise controls|enable channels]]first.In a separate terminal, simulate a webhook by sending an HTTP POST with a message to your server. This example sends a CI failure alert to port 8788 (or whichever port you configured):

```
<channel>
```

tag:[[Channels reference - Claude Code Docs#Expose a reply tool|Expose a reply tool]].If the event doesn’t arrive, the diagnosis depends on what

```
curl
```

returned:

- ```
  curl
  ```

  succeeds but nothing reaches Claude: run

  ```
  /mcp
  ```

  in your session to check the server’s status. “Failed to connect” usually means a dependency or import error in your server file; check the debug log at

  ```
  ~/.claude/debug/<session-id>.txt
  ```

  for the stderr trace.
- ```
  curl
  ```

  fails with “connection refused”: the port is either not bound yet or a stale process from an earlier run is holding it.

  ```
  lsof -i :<port>
  ```

  shows what’s listening;

  ```
  kill
  ```

  the stale process before restarting your session.

[fakechat server](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/fakechat)extends this pattern with a web UI, file attachments, and a reply tool for two-way chat.

## Test during the research preview

During the research preview, every channel must be on the

[[Push events into a running session with channels - Claude Code Docs#Research preview|approved allowlist]]to register. The development flag bypasses the allowlist for specific entries after a confirmation prompt. This example shows both entry types:

```
--channels
```

doesn’t extend the bypass to the

```
--channels
```

entries. During the research preview, the approved allowlist is Anthropic-curated, so your channel stays on the development flag while you build and test.

This flag skips the allowlist only. The

```
channelsEnabled
```

organization policy still applies. Don’t use it to run channels from untrusted sources.

## Server options

A channel sets these options in the

[constructor. The](https://modelcontextprotocol.io/docs/concepts/servers)

```
Server
```

```
instructions
```

and

```
capabilities.tools
```

fields are

[standard MCP](https://modelcontextprotocol.io/docs/concepts/servers);

```
capabilities.experimental['claude/channel']
```

and

```
capabilities.experimental['claude/channel/permission']
```

are the channel-specific additions:

FieldTypeDescription

```
capabilities.experimental['claude/channel']
```

```
object
```

Required. Always

```
{}
```

. Presence registers the notification listener.

```
capabilities.experimental['claude/channel/permission']
```

```
object
```

Optional. Always

```
{}
```

. Declares that this channel can receive permission relay requests. When declared, Claude Code forwards tool approval prompts to your channel so you can approve or deny them remotely. See

```
capabilities.tools
```

```
object
```

Two-way only. Always

```
{}
```

. Standard MCP tool capability. See

```
instructions
```

```
string
```

Recommended. Added to Claude’s system prompt. Tell Claude what events to expect, what the

```
<channel>
```

tag attributes mean, whether to reply, and if so which tool to use and which attribute to pass back (like

```
chat_id
```

).

```
capabilities.tools
```

. This example shows a two-way setup with the channel capability, tools, and instructions set:

```
mcp.notification()
```

with method

```
notifications/claude/channel
```

. The params are in the next section.

## Notification format

Your server emits

```
notifications/claude/channel
```

with two params:

FieldTypeDescription

```
content
```

```
string
```

The event body. Delivered as the body of the

```
<channel>
```

tag.

```
meta
```

```
Record<string, string>
```

Optional. Each entry becomes an attribute on the

```
<channel>
```

tag for routing context like chat ID, sender name, or alert severity. Keys must be identifiers: letters, digits, and underscores only. Keys containing hyphens or other characters are silently dropped.

```
mcp.notification()
```

on the

```
Server
```

instance. This example pushes a CI failure alert with two meta keys:

```
<channel>
```

tag. The

```
source
```

attribute is set automatically from your server’s configured name:

## Expose a reply tool

If your channel is two-way, like a chat bridge rather than an alert forwarder, expose a standard

[MCP tool](https://modelcontextprotocol.io/docs/concepts/tools)that Claude can call to send messages back. Nothing about the tool registration is channel-specific. A reply tool has three components:

- A

  ```
  tools: {}
  ```

  entry in your

  ```
  Server
  ```

  constructor capabilities so Claude Code discovers the tool
- Tool handlers that define the tool’s schema and implement the send logic
- An

  ```
  instructions
  ```

  string in your

  ```
  Server
  ```

  constructor that tells Claude when and how to call the tool

[[Channels reference - Claude Code Docs#Example: build a webhook receiver|webhook receiver above]]:

Enable tool discovery

In your

```
Server
```

constructor in

```
webhook.ts
```

, add

```
tools: {}
```

to the capabilities so Claude Code knows your server offers tools:

Register the reply tool

Add the following to

```
webhook.ts
```

. The

```
import
```

goes at the top of the file with your other imports; the two handlers go between the

```
Server
```

constructor and

```
mcp.connect()
```

. This registers a

```
reply
```

tool that Claude can call with a

```
chat_id
```

and

```
text
```

:

```
webhook.ts
```

with two-way support. Outbound replies stream over

```
GET /events
```

using

[Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)(SSE), so

```
curl -N localhost:8788/events
```

can watch them live; inbound chat arrives on

```
POST /
```

:

Full webhook.ts with reply tool

[fakechat server](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/fakechat)shows a more complete example with file attachments and message editing.

## Gate inbound messages

An ungated channel is a prompt injection vector. Anyone who can reach your endpoint can put text in front of Claude. A channel listening to a chat platform or a public endpoint needs a real sender check before it emits anything. Check the sender against an allowlist before calling

```
mcp.notification()
```

. This example drops any message from a sender not in the set:

```
message.from.id
```

in the example, not

```
message.chat.id
```

. In group chats, these differ, and gating on the room would let anyone in an allowlisted group inject messages into the session.
The

[Telegram](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/telegram)and

[Discord](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord)channels gate on a sender allowlist the same way. They bootstrap the list by pairing: the user DMs the bot, the bot replies with a pairing code, the user approves it in their Claude Code session, and their platform ID is added. See either implementation for the full pairing flow. The

[iMessage](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/imessage)channel takes a different approach: it detects the user’s own addresses from the Messages database at startup and lets them through automatically, with other senders added by handle.

## Relay permission prompts

Permission relay requires Claude Code v2.1.81 or later. Earlier versions ignore the

```
claude/channel/permission
```

capability.

```
Bash
```

,

```
Write
```

, and

```
Edit
```

. Project trust and MCP server consent dialogs don’t relay; those only appear in the local terminal.

### How relay works

When a permission prompt opens, the relay loop has four steps:

- Claude Code generates a short request ID and notifies your server
- Your server forwards the prompt and ID to your chat app
- The remote user replies with a yes or no and that ID
- Your inbound handler parses the reply into a verdict, and Claude Code applies it only if the ID matches an open request

### Permission request fields

The outbound notification from Claude Code is

```
notifications/claude/channel/permission_request
```

. Like the

[[Channels reference - Claude Code Docs#Notification format|channel notification]], the transport is standard MCP but the method and schema are Claude Code extensions. The

```
params
```

object has four string fields your server formats into the outgoing prompt:

FieldDescription

```
request_id
```

Five lowercase letters drawn from

```
a
```

-

```
z
```

without

```
l
```

, so it never reads as a

```
1
```

or

```
I
```

when typed on a phone. Include it in your outgoing prompt so it can be echoed in the reply. Claude Code only accepts a verdict that carries an ID it issued. The local terminal dialog doesn’t display this ID, so your outbound handler is the only way to learn it.

```
tool_name
```

Name of the tool Claude wants to use, for example

```
Bash
```

or

```
Write
```

.

```
description
```

Human-readable summary of what this specific tool call does, the same text the local terminal dialog shows. For a Bash call this is Claude’s description of the command, or the command itself if none was given.

```
input_preview
```

The tool’s arguments as a JSON string, truncated to 200 characters. For Bash this is the command; for Write it’s the file path and a prefix of the content. Omit it from your prompt if you only have room for a one-line message. Your server decides what to show.

```
notifications/claude/channel/permission
```

with two fields:

```
request_id
```

echoing the ID above, and

```
behavior
```

set to

```
'allow'
```

or

```
'deny'
```

. Allow lets the tool call proceed; deny rejects it, the same as answering No in the local dialog. Neither verdict affects future calls.

### Add relay to a chat bridge

Adding permission relay to a two-way channel takes three components:

- A

  ```
  claude/channel/permission: {}
  ```

  entry under

  ```
  experimental
  ```

  capabilities in your

  ```
  Server
  ```

  constructor so Claude Code knows to forward prompts
- A notification handler for

  ```
  notifications/claude/channel/permission_request
  ```

  that formats the prompt and sends it out through your platform API
- A check in your inbound message handler that recognizes

  ```
  yes <id>
  ```

  or

  ```
  no <id>
  ```

  and emits a

  ```
  notifications/claude/channel/permission
  ```

  verdict instead of forwarding the text to Claude

[[Channels reference - Claude Code Docs#Gate inbound messages|authenticates the sender]], because anyone who can reply through your channel can approve or deny tool use in your session. To add these to a two-way chat bridge like the one assembled in

[[Channels reference - Claude Code Docs#Expose a reply tool|Expose a reply tool]]:

Declare the permission capability

In your

```
Server
```

constructor, add

```
claude/channel/permission: {}
```

alongside

```
claude/channel
```

under

```
experimental
```

:

Handle the incoming request

Register a notification handler between your

```
Server
```

constructor and

```
mcp.connect()
```

. Claude Code calls it with the [[Channels reference - Claude Code Docs#Permission request fields|four request fields]]when a permission dialog opens. Your handler formats the prompt for your platform and includes instructions for replying with the ID:

Intercept the verdict in your inbound handler

Your inbound handler is the loop or callback that receives messages from your platform: the same place you

[[Channels reference - Claude Code Docs#Gate inbound messages|gate on sender]]and emit

```
notifications/claude/channel
```

to forward chat to Claude. Add a check before the chat-forwarding call that recognizes the verdict format and emits the permission notification instead.The regex matches the ID format Claude Code generates: five letters, never

```
l
```

. The

```
/i
```

flag tolerates phone autocorrect capitalizing the reply; lowercase the captured ID before sending it back.

- Different format: your inbound handler’s regex fails to match, so text like

  ```
  approve it
  ```

  or

  ```
  yes
  ```

  without an ID falls through as a normal message to Claude.
- Right format, wrong ID: your server emits a verdict, but Claude Code finds no open request with that ID and drops it silently.

### Full example

The assembled

```
webhook.ts
```

below combines all three extensions from this page: the reply tool, sender gating, and permission relay. If you’re starting here, you’ll also need the

[[Channels reference - Claude Code Docs#Example: build a webhook receiver|project setup and]]from the initial walkthrough. To make both directions testable from curl, the HTTP listener serves two paths:

```
.mcp.json
```

entry

- ```
  GET /events
  ```

  : holds an SSE stream open and pushes each outbound message as a

  ```
  data:
  ```

  line, so

  ```
  curl -N
  ```

  can watch Claude’s replies and permission prompts arrive live.
- ```
  POST /
  ```

  : the inbound side, the same handler as earlier, now with the verdict-format check inserted before the chat-forward branch.

Full webhook.ts with permission relay

[[Channels reference - Claude Code Docs#Test during the research preview|development flag]]so it spawns

```
webhook.ts
```

:

```
/events
```

stream, including the five-letter ID. Approve it from the remote side:

```
reply
```

tool and lands in the stream too.
The three channel-specific pieces in this file:

- Capabilities in the

  ```
  Server
  ```

  constructor:

  ```
  claude/channel
  ```

  registers the notification listener,

  ```
  claude/channel/permission
  ```

  opts in to permission relay,

  ```
  tools
  ```

  lets Claude discover the reply tool.
- Outbound paths: the

  ```
  reply
  ```

  tool handler is what Claude calls for conversational responses; the

  ```
  PermissionRequestSchema
  ```

  notification handler is what Claude Code calls when a permission dialog opens. Both call

  ```
  send()
  ```

  to broadcast over

  ```
  /events
  ```

  , but they’re triggered by different parts of the system.
- HTTP handler:

  ```
  GET /events
  ```

  holds an SSE stream open so curl can watch outbound live;

  ```
  POST
  ```

  is inbound, gated on the

  ```
  X-Sender
  ```

  header. A

  ```
  yes <id>
  ```

  or

  ```
  no <id>
  ```

  body goes to Claude Code as a verdict notification and never reaches Claude; anything else is forwarded to Claude as a channel event.

## Package as a plugin

To make your channel installable and shareable, wrap it in a

[[Create plugins - Claude Code Docs|plugin]]and publish it to a

[[Create and distribute a plugin marketplace - Claude Code Docs|marketplace]]. Users install it with

```
/plugin install
```

, then enable it per session with

```
--channels plugin:<name>@<marketplace>
```

.
A channel published to your own marketplace still needs

```
--dangerously-load-development-channels
```

to run, since it isn’t on the

[[Push events into a running session with channels - Claude Code Docs#Supported channels|approved allowlist]]. To get it added,

[[Create plugins - Claude Code Docs#Submit your plugin to the official marketplace|submit it to the official marketplace]]. Channel plugins go through security review before being approved. On Team and Enterprise plans, an admin can instead include your plugin in the organization’s own

[[Push events into a running session with channels - Claude Code Docs#Restrict which channel plugins can run|list, which replaces the default Anthropic allowlist.]]

```
allowedChannelPlugins
```

## See also

- [[Push events into a running session with channels - Claude Code Docs|Channels]]to install and use Telegram, Discord, iMessage, or the fakechat demo, and to enable channels for a Team or Enterprise org
- [Working channel implementations](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins)for complete server code with pairing flows, reply tools, and file attachments
- [[Connect Claude Code to tools via MCP - Claude Code Docs|MCP]]for the underlying protocol that channel servers implement
- [[Create plugins - Claude Code Docs|Plugins]]to package your channel so users can install it with

  ```
  /plugin install
  ```

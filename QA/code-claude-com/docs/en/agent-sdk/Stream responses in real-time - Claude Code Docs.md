---
title: Stream responses in real-time - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/streaming-output
description: Get real-time responses from the Agent SDK as text and tool calls stream
  in
---

```
AssistantMessage
```

objects after Claude finishes generating each response. To receive incremental updates as text and tool calls are generated, enable partial message streaming by setting

```
include_partial_messages
```

(Python) or

```
includePartialMessages
```

(TypeScript) to

```
true
```

in your options.

## Enable streaming output

To enable streaming, set

```
include_partial_messages
```

(Python) or

```
includePartialMessages
```

(TypeScript) to

```
true
```

in your options. This causes the SDK to yield

```
StreamEvent
```

messages containing raw API events as they arrive, in addition to the usual

```
AssistantMessage
```

and

```
ResultMessage
```

.
Your code then needs to:

- Check each message’s type to distinguish

  ```
  StreamEvent
  ```

  from other message types
- For

  ```
  StreamEvent
  ```

  , extract the

  ```
  event
  ```

  field and check its

  ```
  type
  ```
- Look for

  ```
  content_block_delta
  ```

  events where

  ```
  delta.type
  ```

  is

  ```
  text_delta
  ```

  , which contain the actual text chunks

```
StreamEvent
```

, then for

```
content_block_delta
```

, then for

```
text_delta
```

:

## StreamEvent reference

When partial messages are enabled, you receive raw Claude API streaming events wrapped in an object. The type has different names in each SDK:

- Python:

  ```
  StreamEvent
  ```

  (import from

  ```
  claude_agent_sdk.types
  ```

  )
- TypeScript:

  ```
  SDKPartialAssistantMessage
  ```

  with

  ```
  type: 'stream_event'
  ```

```
event
```

field contains the raw streaming event from the

[Claude API](https://platform.claude.com/docs/en/build-with-claude/streaming#event-types). Common event types include:

Event TypeDescription

```
message_start
```

Start of a new message

```
content_block_start
```

Start of a new content block (text or tool use)

```
content_block_delta
```

Incremental update to content

```
content_block_stop
```

End of a content block

```
message_delta
```

Message-level updates (stop reason, usage)

```
message_stop
```

End of the message

## Message flow

With partial messages enabled, you receive messages in this order:

```
include_partial_messages
```

in Python,

```
includePartialMessages
```

in TypeScript), you receive all message types except

```
StreamEvent
```

. Common types include

```
SystemMessage
```

(session initialization),

```
AssistantMessage
```

(complete responses),

```
ResultMessage
```

(final result), and a compact boundary message indicating when conversation history was compacted (

```
SDKCompactBoundaryMessage
```

in TypeScript;

```
SystemMessage
```

with subtype

```
"compact_boundary"
```

in Python).

## Stream text responses

To display text as it’s generated, look for

```
content_block_delta
```

events where

```
delta.type
```

is

```
text_delta
```

. These contain the incremental text chunks. The example below prints each chunk as it arrives:

## Stream tool calls

Tool calls also stream incrementally. You can track when tools start, receive their input as it’s generated, and see when they complete. The example below tracks the current tool being called and accumulates the JSON input as it streams in. It uses three event types:

- ```
  content_block_start
  ```

  : tool begins
- ```
  content_block_delta
  ```

  with

  ```
  input_json_delta
  ```

  : input chunks arrive
- ```
  content_block_stop
  ```

  : tool call complete

## Build a streaming UI

This example combines text and tool streaming into a cohesive UI. It tracks whether the agent is currently executing a tool (using an

```
in_tool
```

flag) to show status indicators like

```
[Using Read...]
```

while tools run. Text streams normally when not in a tool, and tool completion triggers a “done” message. This pattern is useful for chat interfaces that need to show progress during multi-step agent tasks.

## Known limitations

Some SDK features are incompatible with streaming:

- Extended thinking: when you explicitly set

  ```
  max_thinking_tokens
  ```

  (Python) or

  ```
  maxThinkingTokens
  ```

  (TypeScript),

  ```
  StreamEvent
  ```

  messages are not emitted. You’ll only receive complete messages after each turn. Note that thinking is disabled by default in the SDK, so streaming works unless you enable it.
- Structured output: the JSON result appears only in the final

  ```
  ResultMessage.structured_output
  ```

  , not as streaming deltas. See[[Get structured output from agents - Claude Code Docs|structured outputs]]for details.

## Next steps

Now that you can stream text and tool calls in real-time, explore these related topics:

- [[Streaming Input - Claude Code Docs|Interactive vs one-shot queries]]: choose between input modes for your use case
- [[Get structured output from agents - Claude Code Docs|Structured outputs]]: get typed JSON responses from the agent
- [[Configure permissions - Claude Code Docs-dbd6de|Permissions]]: control which tools the agent can use

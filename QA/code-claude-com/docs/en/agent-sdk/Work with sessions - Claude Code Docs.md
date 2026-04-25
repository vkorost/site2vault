---
title: Work with sessions - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/sessions
description: How sessions persist agent conversation history, and when to use continue,
  resume, and fork to return to a prior run.
---

Sessions persist the conversation, not the filesystem. To snapshot and revert file changes the agent made, use

[file checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing).

```
resume
```

and

```
fork
```

manually, and what to know about resuming sessions across hosts.

## Choose an approach

How much session handling you need depends on your application’s shape. Session management comes into play when you send multiple prompts that should share context. Within a single

```
query()
```

call, the agent already takes as many turns as it needs, and permission prompts and

```
AskUserQuestion
```

are

[[Handle approvals and user input - Claude Code Docs|handled in-loop]](they don’t end the call).

What you’re buildingWhat to useOne-shot task: single prompt, no follow-upNothing extra. One

```
query()
```

call handles it.Multi-turn chat in one process

```
ClaudeSDKClient
```

(Python) or

```
continue: true
```

(TypeScript)

```
continue_conversation=True
```

(Python) /

```
continue: true
```

(TypeScript). Resumes the most recent session in the directory, no ID needed.

```
resume
```

.[[Agent SDK reference - TypeScript - Claude Code Docs#Options|. The session exists only in memory for the duration of the call. Python always persists to disk.]]

```
persistSession: false
```

### Continue, resume, and fork

Continue, resume, and fork are option fields you set on

```
query()
```

(

[[Agent SDK reference - Python - Claude Code Docs|in Python,]]

```
ClaudeAgentOptions
```

[[Agent SDK reference - TypeScript - Claude Code Docs#Options|in TypeScript). Continue and resume both pick up an existing session and add to it. The difference is how they find that session:]]

```
Options
```

- Continue finds the most recent session in the current directory. You don’t track anything. Works well when your app runs one conversation at a time.
- Resume takes a specific session ID. You track the ID. Required when you have multiple sessions (for example, one per user in a multi-user app) or want to return to one that isn’t the most recent.

## Automatic session management

Both SDKs offer an interface that tracks session state for you across calls, so you don’t pass IDs around manually. Use these for multi-turn conversations within a single process.

### Python: ``` ClaudeSDKClient ```

[[Agent SDK reference - Python - Claude Code Docs|handles session IDs internally. Each call to]]

```
ClaudeSDKClient
```

```
client.query()
```

automatically continues the same session. Call

[[Agent SDK reference - Python - Claude Code Docs|to iterate over the messages for the current query. The client must be used as an async context manager. This example runs two queries against the same]]

```
client.receive_response()
```

```
client
```

. The first asks the agent to analyze a module; the second asks it to refactor that module. Because both calls go through the same client instance, the second query has full context from the first without any explicit

```
resume
```

or session ID:

Python

[[Agent SDK reference - Python - Claude Code Docs|Python SDK reference]]for details on when to use

```
ClaudeSDKClient
```

vs the standalone

```
query()
```

function.

### TypeScript: ``` continue: true ```

The stable TypeScript SDK (the

```
query()
```

function used throughout these docs, sometimes called V1) doesn’t have a session-holding client object like Python’s

```
ClaudeSDKClient
```

. Instead, pass

```
continue: true
```

on each subsequent

```
query()
```

call and the SDK picks up the most recent session in the current directory. No ID tracking required.
This example makes two separate

```
query()
```

calls. The first creates a fresh session; the second sets

```
continue: true
```

, which tells the SDK to find and resume the most recent session on disk. The agent has full context from the first call:

TypeScript

There’s also a

[V2 preview](https://code.claude.com/docs/en/agent-sdk/typescript-v2-preview)of the TypeScript SDK that provides

```
createSession()
```

with a

```
send
```

/

```
stream
```

pattern, closer to Python’s

```
ClaudeSDKClient
```

in feel. V2 is unstable and its APIs may change; the rest of this documentation uses the stable V1

```
query()
```

function.

## Use session options with ``` query() ```

### Capture the session ID

Resume and fork require a session ID. Read it from the

```
session_id
```

field on the result message (

[[Agent SDK reference - Python - Claude Code Docs|in Python,]]

```
ResultMessage
```

[[Agent SDK reference - TypeScript - Claude Code Docs|in TypeScript), which is present on every result regardless of success or error. In TypeScript the ID is also available earlier as a direct field on the init]]

```
SDKResultMessage
```

```
SystemMessage
```

; in Python it’s nested inside

```
SystemMessage.data
```

.

### Resume by ID

Pass a session ID to

```
resume
```

to return to that specific session. The agent picks up with full context from wherever the session left off. Common reasons to resume:

- Follow up on a completed task. The agent already analyzed something; now you want it to act on that analysis without re-reading files.
- Recover from a limit. The first run ended with

  ```
  error_max_turns
  ```

  or

  ```
  error_max_budget_usd
  ```

  (see[Handle the result](https://code.claude.com/docs/en/agent-sdk/agent-loop#handle-the-result)); resume with a higher limit.
- Restart your process. You captured the ID before shutdown and want to restore the conversation.

[[Work with sessions - Claude Code Docs#Capture the session ID|Capture the session ID]]with a follow-up prompt. Because you’re resuming, the agent already has the prior analysis in context:

[.](https://code.claude.com/docs/en/agent-sdk/session-storage)

```
SessionStore
```

adapter

### Fork to explore alternatives

Forking creates a new session that starts with a copy of the original’s history but diverges from that point. The fork gets its own session ID; the original’s ID and history stay unchanged. You end up with two independent sessions you can resume separately.

Forking branches the conversation history, not the filesystem. If a forked agent edits files, those changes are real and visible to any session working in the same directory. To branch and revert file changes, use

[file checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing).

[[Work with sessions - Claude Code Docs#Capture the session ID|Capture the session ID]]: you’ve already analyzed an auth module in

```
session_id
```

and want to explore OAuth2 without losing the JWT-focused thread. The first block forks the session and captures the fork’s ID (

```
forked_id
```

); the second block resumes the original

```
session_id
```

to continue down the JWT path. You now have two session IDs pointing at two separate histories:

## Resume across hosts

Session files are local to the machine that created them. To resume a session on a different host (CI workers, ephemeral containers, serverless), you have two options:

- Move the session file. Persist

  ```
  ~/.claude/projects/<encoded-cwd>/<session-id>.jsonl
  ```

  from the first run and restore it to the same path on the new host before calling

  ```
  resume
  ```

  . The

  ```
  cwd
  ```

  must match.
- Don’t rely on session resume. Capture the results you need (analysis output, decisions, file diffs) as application state and pass them into a fresh session’s prompt. This is often more robust than shipping transcript files around.

[[Agent SDK reference - TypeScript - Claude Code Docs|and]]

```
listSessions()
```

[[Agent SDK reference - TypeScript - Claude Code Docs|in TypeScript,]]

```
getSessionMessages()
```

[[Agent SDK reference - Python - Claude Code Docs|and]]

```
list_sessions()
```

[[Agent SDK reference - Python - Claude Code Docs|in Python. Use them to build custom session pickers, cleanup logic, or transcript viewers. Both SDKs also expose functions for looking up and mutating individual sessions:]]

```
get_session_messages()
```

[[Agent SDK reference - Python - Claude Code Docs|,]]

```
get_session_info()
```

[[Agent SDK reference - Python - Claude Code Docs|, and]]

```
rename_session()
```

[[Agent SDK reference - Python - Claude Code Docs|in Python, and]]

```
tag_session()
```

[[Agent SDK reference - TypeScript - Claude Code Docs|,]]

```
getSessionInfo()
```

[[Agent SDK reference - TypeScript - Claude Code Docs|, and]]

```
renameSession()
```

[[Agent SDK reference - TypeScript - Claude Code Docs|in TypeScript. Use them to organize sessions by tag or give them human-readable titles.]]

```
tagSession()
```

## Related resources

- [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop): Understand turns, messages, and context accumulation within a session
- [File checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing): Track and revert file changes across sessions
- [[Agent SDK reference - Python - Claude Code Docs|Python]]: Full session option reference for Python

  ```
  ClaudeAgentOptions
  ```
- [[Agent SDK reference - TypeScript - Claude Code Docs#Options|TypeScript]]: Full session option reference for TypeScript

  ```
  Options
  ```

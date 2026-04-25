---
title: Quickstart - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/quickstart
description: Get started with the Python or TypeScript Agent SDK to build AI agents
  that work autonomously
---

- Set up a project with the Agent SDK
- Create a file with some buggy code
- Run an agent that finds and fixes the bugs automatically

## Prerequisites

- Node.js 18+ or Python 3.10+
- An Anthropic account ([sign up here](https://platform.claude.com/))

## Setup

Create a project folder

Create a new directory for this quickstart:For your own projects, you can run the SDK from any folder; it will have access to files in that directory and its subdirectories by default.

Install the SDK

Install the Agent SDK package for your language:

- TypeScript
- Python (uv)
- Python (pip)

The TypeScript SDK bundles a native Claude Code binary for your platform as an optional dependency, so you don’t need to install Claude Code separately.

Set your API key

Get an API key from the The SDK also supports authentication via third-party API providers:

[Claude Console](https://platform.claude.com/), then create a

```
.env
```

file in your project directory:

- Amazon Bedrock: set

  ```
  CLAUDE_CODE_USE_BEDROCK=1
  ```

  environment variable and configure AWS credentials
- Google Vertex AI: set

  ```
  CLAUDE_CODE_USE_VERTEX=1
  ```

  environment variable and configure Google Cloud credentials
- Microsoft Azure: set

  ```
  CLAUDE_CODE_USE_FOUNDRY=1
  ```

  environment variable and configure Azure credentials

[[Claude Code on Amazon Bedrock - Claude Code Docs|Bedrock]],[[Claude Code on Google Vertex AI - Claude Code Docs|Vertex AI]], or[[Claude Code on Microsoft Foundry - Claude Code Docs|Azure AI Foundry]]for details.

Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Please use the API key authentication methods described in this document instead.

## Create a buggy file

This quickstart walks you through building an agent that can find and fix bugs in code. First, you need a file with some intentional bugs for the agent to fix. Create

```
utils.py
```

in the

```
my-agent
```

directory and paste the following code:

- ```
  calculate_average([])
  ```

  crashes with division by zero
- ```
  get_user_name(None)
  ```

  crashes with a TypeError

## Build an agent that finds and fixes bugs

Create

```
agent.py
```

if you’re using the Python SDK, or

```
agent.ts
```

for TypeScript:

- ```
  query
  ```

  : the main entry point that creates the agentic loop. It returns an async iterator, so you use

  ```
  async for
  ```

  to stream messages as Claude works. See the full API in the[[Agent SDK reference - Python - Claude Code Docs#query()|Python]]or[[Agent SDK reference - TypeScript - Claude Code Docs#query()|TypeScript]]SDK reference.
- ```
  prompt
  ```

  : what you want Claude to do. Claude figures out which tools to use based on the task.
- ```
  options
  ```

  : configuration for the agent. This example uses

  ```
  allowedTools
  ```

  to pre-approve

  ```
  Read
  ```

  ,

  ```
  Edit
  ```

  , and

  ```
  Glob
  ```

  , and

  ```
  permissionMode: "acceptEdits"
  ```

  to auto-approve file changes. Other options include

  ```
  systemPrompt
  ```

  ,

  ```
  mcpServers
  ```

  , and more. See all options for[[Agent SDK reference - Python - Claude Code Docs|Python]]or[[Agent SDK reference - TypeScript - Claude Code Docs#Options|TypeScript]].

```
async for
```

loop keeps running as Claude thinks, calls tools, observes results, and decides what to do next. Each iteration yields a message: Claude’s reasoning, a tool call, a tool result, or the final outcome. The SDK handles the orchestration (tool execution, context management, retries) so you just consume the stream. The loop ends when Claude finishes the task or hits an error.
The message handling inside the loop filters for human-readable output. Without filtering, you’d see raw message objects including system initialization and internal state, which is useful for debugging but noisy otherwise.

This example uses streaming to show progress in real-time. If you don’t need live output (e.g., for background jobs or CI pipelines), you can collect all messages at once. See

[[Streaming Input - Claude Code Docs|Streaming vs. single-turn mode]]for details.

### Run your agent

Your agent is ready. Run it with the following command:

- Python
- TypeScript

```
utils.py
```

. You’ll see defensive code handling empty lists and null users. Your agent autonomously:

- Read

  ```
  utils.py
  ```

  to understand the code
- Analyzed the logic and identified edge cases that would crash
- Edited the file to add proper error handling

If you see “API key not found”, make sure you’ve set the

```
ANTHROPIC_API_KEY
```

environment variable in your

```
.env
```

file or shell environment. See the [[Troubleshooting - Claude Code Docs|full troubleshooting guide]]for more help.

### Try other prompts

Now that your agent is set up, try some different prompts:

- ```
  "Add docstrings to all functions in utils.py"
  ```
- ```
  "Add type hints to all functions in utils.py"
  ```
- ```
  "Create a README.md documenting the functions in utils.py"
  ```

### Customize your agent

You can modify your agent’s behavior by changing the options. Here are a few examples: Add web search capability:

```
Bash
```

enabled, try:

```
"Write unit tests for utils.py, run them, and fix any failures"
```

## Key concepts

Tools control what your agent can do:

ToolsWhat the agent can do

```
Read
```

,

```
Glob
```

,

```
Grep
```

Read-only analysis

```
Read
```

,

```
Edit
```

,

```
Glob
```

Analyze and modify code

```
Read
```

,

```
Edit
```

,

```
Bash
```

,

```
Glob
```

,

```
Grep
```

Full automation

ModeBehaviorUse case

```
acceptEdits
```

Auto-approves file edits and common filesystem commands, asks for other actionsTrusted development workflows

```
dontAsk
```

Denies anything not in

```
allowedTools
```

Locked-down headless agents

```
auto
```

(TypeScript only)A model classifier approves or denies each tool callAutonomous agents with safety guardrails

```
bypassPermissions
```

Runs every tool without promptsSandboxed CI, fully trusted environments

```
default
```

Requires a

```
canUseTool
```

callback to handle approvalCustom approval flows

```
acceptEdits
```

mode, which auto-approves file operations so the agent can run without interactive prompts. If you want to prompt users for approval, use

```
default
```

mode and provide a

[[Handle approvals and user input - Claude Code Docs|that collects user input. For more control, see]]

```
canUseTool
```

callback

[[Configure permissions - Claude Code Docs-dbd6de|Permissions]].

## Troubleshooting

### API error ``` thinking.type.enabled ``` is not supported for this model

Claude Opus 4.7 replaces

```
thinking.type.enabled
```

with

```
thinking.type.adaptive
```

. Older Agent SDK versions fail with the following API error when you select

```
claude-opus-4-7
```

:

## Next steps

Now that you’ve created your first agent, learn how to extend its capabilities and tailor it to your use case:

- [[Configure permissions - Claude Code Docs-dbd6de|Permissions]]: control what your agent can do and when it needs approval
- [[Intercept and control agent behavior with hooks - Claude Code Docs|Hooks]]: run custom code before or after tool calls
- [[Work with sessions - Claude Code Docs|Sessions]]: build multi-turn agents that maintain context
- [[Connect to external tools with MCP - Claude Code Docs|MCP servers]]: connect to databases, browsers, APIs, and other external systems
- [[Hosting the Agent SDK - Claude Code Docs|Hosting]]: deploy agents to Docker, cloud, and CI/CD
- [Example agents](https://github.com/anthropics/claude-agent-sdk-demos): see complete examples: email assistant, research agent, and more

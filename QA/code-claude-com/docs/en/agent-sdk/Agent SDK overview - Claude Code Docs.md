---
title: Agent SDK overview - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/overview
description: Build production AI agents with Claude Code as a library
---

The Claude Code SDK has been renamed to the Claude Agent SDK. If you’re migrating from the old SDK, see the

[[Migrate to Claude Agent SDK - Claude Code Docs|Migration Guide]].

Opus 4.7 (

```
claude-opus-4-7
```

) requires Agent SDK v0.2.111 or later. If you see a

```
thinking.type.enabled
```

API error, see [[Quickstart - Claude Code Docs-1f2ec9#Troubleshooting|Troubleshooting]].

## Quickstart

Build a bug-fixing agent in minutes

## Example agents

Email assistant, research agent, and more

## Get started

Install the SDK

- TypeScript
- Python

The TypeScript SDK bundles a native Claude Code binary for your platform as an optional dependency, so you don’t need to install Claude Code separately.

Set your API key

Get an API key from the The SDK also supports authentication via third-party API providers:

[Console](https://platform.claude.com/), then set it as an environment variable:

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

[[Quickstart - Claude Code Docs-1f2ec9|Quickstart]]to create an agent that finds and fixes bugs in minutes.

## Capabilities

Everything that makes Claude Code powerful is available in the SDK:

- Built-in tools
- Hooks
- Subagents
- MCP
- Permissions
- Sessions

Your agent can read files, run commands, and search codebases out of the box. Key tools include:

This example creates an agent that searches your codebase for TODO comments:

ToolWhat it doesReadRead any file in the working directoryWriteCreate new filesEditMake precise edits to existing filesBashRun terminal commands, scripts, git operationsMonitorWatch a background script and react to each output line as an eventGlobFind files by pattern (

```
**/*.ts
```

,

```
src/**/*.py
```

)GrepSearch file contents with regexWebSearchSearch the web for current informationWebFetchFetch and parse web page content

### Claude Code features

The SDK also supports Claude Code’s filesystem-based configuration. With default options the SDK loads these from

```
.claude/
```

in your working directory and

```
~/.claude/
```

. To restrict which sources load, set

```
setting_sources
```

(Python) or

```
settingSources
```

(TypeScript) in your options.

FeatureDescriptionLocation

```
.claude/skills/*/SKILL.md
```

[[Slash Commands in the SDK - Claude Code Docs|Slash commands]]

```
.claude/commands/*.md
```

[[Modifying system prompts - Claude Code Docs|Memory]]

```
CLAUDE.md
```

or

```
.claude/CLAUDE.md
```

[[Plugins in the SDK - Claude Code Docs|Plugins]]

```
plugins
```

option

## Compare the Agent SDK to other Claude tools

The Claude Platform offers multiple ways to build with Claude. Here’s how the Agent SDK fits in:

- Agent SDK vs Client SDK
- Agent SDK vs Claude Code CLI

The

[Anthropic Client SDK](https://platform.claude.com/docs/en/api/client-sdks)gives you direct API access: you send prompts and implement tool execution yourself. The Agent SDK gives you Claude with built-in tool execution.With the Client SDK, you implement a tool loop. With the Agent SDK, Claude handles it:

## Changelog

View the full changelog for SDK updates, bug fixes, and new features:

- TypeScript SDK: [view CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md)
- Python SDK: [view CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md)

## Reporting bugs

If you encounter bugs or issues with the Agent SDK:

- TypeScript SDK: [report issues on GitHub](https://github.com/anthropics/claude-agent-sdk-typescript/issues)
- Python SDK: [report issues on GitHub](https://github.com/anthropics/claude-agent-sdk-python/issues)

## Branding guidelines

For partners integrating the Claude Agent SDK, use of Claude branding is optional. When referencing Claude in your product: Allowed:

- “Claude Agent” (preferred for dropdown menus)
- “Claude” (when within a menu already labeled “Agents”)
- ” Powered by Claude” (if you have an existing agent name)

- “Claude Code” or “Claude Code Agent”
- Claude Code-branded ASCII art or visual elements that mimic Claude Code

[sales team](https://www.anthropic.com/contact-sales).

## License and terms

Use of the Claude Agent SDK is governed by

[Anthropic’s Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms), including when you use it to power products and services that you make available to your own customers and end users, except to the extent a specific component or dependency is covered by a different license as indicated in that component’s LICENSE file.

## Next steps

## Quickstart

Build an agent that finds and fixes bugs in minutes

## Example agents

Email assistant, research agent, and more

## TypeScript SDK

Full TypeScript API reference and examples

## Python SDK

Full Python API reference and examples

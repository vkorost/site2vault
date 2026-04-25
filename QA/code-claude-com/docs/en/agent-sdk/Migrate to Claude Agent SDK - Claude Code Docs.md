---
title: Migrate to Claude Agent SDK - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/migration-guide
description: Guide for migrating the Claude Code TypeScript and Python SDKs to the
  Claude Agent SDK
---

## Overview

The Claude Code SDK has been renamed to the Claude Agent SDK and its documentation has been reorganized. This change reflects the SDK’s broader capabilities for building AI agents beyond just coding tasks.

## What’s Changed

AspectOldNewPackage Name (TS/JS)

```
@anthropic-ai/claude-code
```

```
@anthropic-ai/claude-agent-sdk
```

Python Package

```
claude-code-sdk
```

```
claude-agent-sdk
```

Documentation LocationClaude Code docsAPI Guide → Agent SDK section

Documentation Changes: The Agent SDK documentation has moved from the Claude Code docs to the API Guide under a dedicated [[Agent SDK overview - Claude Code Docs|Agent SDK]] section. The Claude Code docs now focus on the CLI tool and automation features.

## Migration Steps

### For TypeScript/JavaScript Projects

1. Uninstall the old package:

> ```
> npm uninstall @anthropic-ai/claude-code
> ```

2. Install the new package:

> ```
> npm install @anthropic-ai/claude-agent-sdk
> ```

3. Update your imports:
Change all imports from

```
@anthropic-ai/claude-code
```

to

```
@anthropic-ai/claude-agent-sdk
```

:

> ```
> // Before
> import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-code";
>
> // After
> import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
> ```

4. Update package.json dependencies:
If you have the package listed in your

```
package.json
```

, update it:
Before:

> ```
> {
>   "dependencies": {
>     "@anthropic-ai/claude-code": "^0.0.42"
>   }
> }
> ```

After:

> ```
> {
>   "dependencies": {
>     "@anthropic-ai/claude-agent-sdk": "^0.2.0"
>   }
> }
> ```

That’s it! No other code changes are required.

### For Python Projects

1. Uninstall the old package:

> ```
> pip uninstall claude-code-sdk
> ```

2. Install the new package:

> ```
> pip install claude-agent-sdk
> ```

3. Update your imports:
Change all imports from

```
claude_code_sdk
```

to

```
claude_agent_sdk
```

:

> ```
> # Before
> from claude_code_sdk import query, ClaudeCodeOptions
>
> # After
> from claude_agent_sdk import query, ClaudeAgentOptions
> ```

4. Update type names:
Change

```
ClaudeCodeOptions
```

to

```
ClaudeAgentOptions
```

:

> ```
> # Before
> from claude_code_sdk import query, ClaudeCodeOptions
>
> options = ClaudeCodeOptions(model="claude-opus-4-7")
>
> # After
> from claude_agent_sdk import query, ClaudeAgentOptions
>
> options = ClaudeAgentOptions(model="claude-opus-4-7")
> ```

5. Review [[Migrate to Claude Agent SDK - Claude Code Docs#Breaking changes|breaking changes]]
Make any code changes needed to complete the migration.

## Breaking changes

To improve isolation and explicit configuration, Claude Agent SDK v0.1.0 introduces breaking changes for users migrating from Claude Code SDK. Review this section carefully before migrating.

### Python: ClaudeCodeOptions renamed to ClaudeAgentOptions

What changed: The Python SDK type

```
ClaudeCodeOptions
```

has been renamed to

```
ClaudeAgentOptions
```

.
Migration:

> ```
> # BEFORE (claude-code-sdk)
> from claude_code_sdk import query, ClaudeCodeOptions
>
> options = ClaudeCodeOptions(model="claude-opus-4-7", permission_mode="acceptEdits")
>
> # AFTER (claude-agent-sdk)
> from claude_agent_sdk import query, ClaudeAgentOptions
>
> options = ClaudeAgentOptions(model="claude-opus-4-7", permission_mode="acceptEdits")
> ```

Why this changed: The type name now matches the “Claude Agent SDK” branding and provides consistency across the SDK’s naming conventions.

### System prompt no longer default

What changed: The SDK no longer uses Claude Code’s system prompt by default.
Migration:

> ```
> // BEFORE (v0.0.x) - Used Claude Code's system prompt by default
> const result = query({ prompt: "Hello" });
>
> // AFTER (v0.1.0) - Uses minimal system prompt by default
> // To get the old behavior, explicitly request Claude Code's preset:
> const result = query({
>   prompt: "Hello",
>   options: {
>     systemPrompt: { type: "preset", preset: "claude_code" }
>   }
> });
>
> // Or use a custom system prompt:
> const result = query({
>   prompt: "Hello",
>   options: {
>     systemPrompt: "You are a helpful coding assistant"
>   }
> });
> ```

Why this changed: Provides better control and isolation for SDK applications. You can now build agents with custom behavior without inheriting Claude Code’s CLI-focused instructions.

### Settings Sources No Longer Loaded by Default

What changed: The SDK no longer reads from filesystem settings (CLAUDE.md, settings.json, slash commands, etc.) by default.
Migration:

> ```
> // BEFORE (v0.0.x) - Loaded all settings automatically
> const result = query({ prompt: "Hello" });
> // Would read from:
> // - ~/.claude/settings.json (user)
> // - .claude/settings.json (project)
> // - .claude/settings.local.json (local)
> // - CLAUDE.md files
> // - Custom slash commands
>
> // AFTER (v0.1.0) - No settings loaded by default
> // To get the old behavior:
> const result = query({
>   prompt: "Hello",
>   options: {
>     settingSources: ["user", "project", "local"]
>   }
> });
>
> // Or load only specific sources:
> const result = query({
>   prompt: "Hello",
>   options: {
>     settingSources: ["project"] // Only project settings
>   }
> });
> ```

Why this changed: Ensures SDK applications have predictable behavior independent of local filesystem configurations. This is especially important for:

- CI/CD environments - Consistent behavior without local customizations
- Deployed applications - No dependency on filesystem settings
- Testing - Isolated test environments
- Multi-tenant systems - Prevent settings leakage between users

Current SDK releases have reverted this default for

```
query()
```

: omitting the option once again loads user, project, and local settings, matching the CLI. Pass

```
settingSources: []
```

in TypeScript or

```
setting_sources=[]
```

in Python if your application depends on the isolated behavior described above. Python SDK 0.1.59 and earlier treated an empty list the same as omitting the option, so upgrade before relying on

```
setting_sources=[]
```

. See [[Use Claude Code features in the SDK - Claude Code Docs#What settingSources does not control|What settingSources does not control]] for inputs that are read even when

```
settingSources
```

is

```
[]
```

.

## Why the Rename?

The Claude Code SDK was originally designed for coding tasks, but it has evolved into a powerful framework for building all types of AI agents. The new name “Claude Agent SDK” better reflects its capabilities:

- Building business agents (legal assistants, finance advisors, customer support)
- Creating specialized coding agents (SRE bots, security reviewers, code review agents)
- Developing custom agents for any domain with tool use, MCP integration, and more

## Getting Help

If you encounter any issues during migration:
For TypeScript/JavaScript:

- Check that all imports are updated to use

  ```
  @anthropic-ai/claude-agent-sdk
  ```
- Verify your package.json has the new package name
- Run

  ```
  npm install
  ```

  to ensure dependencies are updated

For Python:

- Check that all imports are updated to use

  ```
  claude_agent_sdk
  ```
- Verify your requirements.txt or pyproject.toml has the new package name
- Run

  ```
  pip install claude-agent-sdk
  ```

  to ensure the package is installed

## Next Steps

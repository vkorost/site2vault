---
title: Slash Commands in the SDK - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/slash-commands
description: Learn how to use slash commands to control Claude Code sessions through
  the SDK
---

```
/
```

. These commands can be sent through the SDK to perform actions like compacting context, listing context usage, or invoking custom commands. Only commands that work without an interactive terminal are dispatchable through the SDK; the

```
system/init
```

message lists the ones available in your session.

## Discovering Available Slash Commands

The Claude Agent SDK provides information about available slash commands in the system initialization message. Access this information when your session starts:

## Sending Slash Commands

Send slash commands by including them in your prompt string, just like regular text:

## Common Slash Commands

### ``` /compact ``` - Compact Conversation History

The

```
/compact
```

command reduces the size of your conversation history by summarizing older messages while preserving important context:

### Clearing the conversation

The interactive

```
/clear
```

command is not available in the SDK. Each

```
query()
```

call already starts a fresh conversation, so to clear context, end the current

```
query()
```

and start a new one. The previous conversation stays on disk and can be returned to by passing its session ID to the

[[Work with sessions - Claude Code Docs#Resume by ID|.]]

```
resume
```

option

## Creating Custom Slash Commands

In addition to using built-in slash commands, you can create your own custom commands that are available through the SDK. Custom commands are defined as markdown files in specific directories, similar to how subagents are configured.

The

```
.claude/commands/
```

directory is the legacy format. The recommended format is

```
.claude/skills/<name>/SKILL.md
```

, which supports the same slash-command invocation (

```
/name
```

) plus autonomous invocation by Claude. See [[Agent Skills in the SDK - Claude Code Docs|Skills]]for the current format. The CLI continues to support both formats, and the examples below remain accurate for

```
.claude/commands/
```

.

### File Locations

Custom slash commands are stored in designated directories based on their scope:

- Project commands:

  ```
  .claude/commands/
  ```

  - Available only in the current project (legacy; prefer

  ```
  .claude/skills/
  ```

  )
- Personal commands:

  ```
  ~/.claude/commands/
  ```

  - Available across all your projects (legacy; prefer

  ```
  ~/.claude/skills/
  ```

  )

### File Format

Each custom command is a markdown file where:

- The filename (without

  ```
  .md
  ```

  extension) becomes the command name
- The file content defines what the command does
- Optional YAML frontmatter provides configuration

#### Basic Example

Create

```
.claude/commands/refactor.md
```

:

```
/refactor
```

command that you can use through the SDK.

#### With Frontmatter

Create

```
.claude/commands/security-check.md
```

:

### Using Custom Commands in the SDK

Once defined in the filesystem, custom commands are automatically available through the SDK:

### Advanced Features

#### Arguments and Placeholders

Custom commands support dynamic arguments using placeholders: Create

```
.claude/commands/fix-issue.md
```

:

#### Bash Command Execution

Custom commands can execute bash commands and include their output: Create

```
.claude/commands/git-commit.md
```

:

#### File References

Include file contents using the

```
@
```

prefix:
Create

```
.claude/commands/review-config.md
```

:

### Organization with Namespacing

Organize commands in subdirectories for better structure:

### Practical Examples

#### Code Review Command

Create

```
.claude/commands/code-review.md
```

:

#### Test Runner Command

Create

```
.claude/commands/test.md
```

:

## See Also

- [[Extend Claude with skills - Claude Code Docs|Slash Commands]]- Complete slash command documentation
- [[Subagents in the SDK - Claude Code Docs|Subagents in the SDK]]- Similar filesystem-based configuration for subagents
- [[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript SDK reference]]- Complete API documentation
- [[Agent SDK overview - Claude Code Docs|SDK overview]]- General SDK concepts
- [[CLI reference - Claude Code Docs|CLI reference]]- Command-line interface

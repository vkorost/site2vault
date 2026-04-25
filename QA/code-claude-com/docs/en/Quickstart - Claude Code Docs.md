---
title: Quickstart - Claude Code Docs
source_url: https://code.claude.com/docs/en/quickstart
description: Welcome to Claude Code!
---

## Before you begin

Make sure you have:

- A terminal or command prompt open
  - If you’ve never used the terminal before, check out the [[Terminal guide for new users - Claude Code Docs|terminal guide]]
- If you’ve never used the terminal before, check out the
- A code project to work with
- A [Claude subscription](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=quickstart_prereq)(Pro, Max, Team, or Enterprise),[Claude Console](https://console.anthropic.com/)account, or access through a[[Enterprise deployment overview - Claude Code Docs|supported cloud provider]]

This guide covers the terminal CLI. Claude Code is also available on the

[web](https://claude.ai/code), as a[[Use Claude Code Desktop - Claude Code Docs|desktop app]], in[[Use Claude Code in VS Code - Claude Code Docs|VS Code]]and[[JetBrains IDEs - Claude Code Docs|JetBrains IDEs]], in[[Claude Code in Slack - Claude Code Docs|Slack]], and in CI/CD with[[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]and[[Claude Code GitLab CICD - Claude Code Docs|GitLab]]. See[all interfaces](https://code.claude.com/docs/en/overview#use-claude-code-everywhere).

## Step 1: Install Claude Code

To install Claude Code, use one of the following methods:

- Native Install (Recommended)
- Homebrew
- WinGet

macOS, Linux, WSL:Windows PowerShell:Windows CMD:If you see

```
The token '&&' is not a valid statement separator
```

, you’re in PowerShell, not CMD. If you see

```
'irm' is not recognized as an internal or external command
```

, you’re in CMD, not PowerShell. Your prompt shows

```
PS C:\
```

when you’re in PowerShell and

```
C:\
```

without the

```
PS
```

when you’re in CMD.Native Windows setups require [Git for Windows](https://git-scm.com/downloads/win). Install it first if you don’t have it. WSL setups do not need it.

Native installations automatically update in the background to keep you on the latest version.

[[Advanced setup - Claude Code Docs#Install with Linux package managers|apt, dnf, or apk]]on Debian, Fedora, RHEL, and Alpine.

## Step 2: Log in to your account

Claude Code requires an account to use. When you start an interactive session with the

```
claude
```

command, you’ll need to log in:

- [Claude Pro, Max, Team, or Enterprise](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=quickstart_login)(recommended)
- [Claude Console](https://console.anthropic.com/)(API access with pre-paid credits). On first login, a “Claude Code” workspace is automatically created in the Console for centralized cost tracking.
- [[Enterprise deployment overview - Claude Code Docs|Amazon Bedrock, Google Vertex AI, or Microsoft Foundry]](enterprise cloud providers)

```
/login
```

command.

## Step 3: Start your first session

Open your terminal in any project directory and start Claude Code:

```
/help
```

for available commands or

```
/resume
```

to continue a previous conversation.

## Step 4: Ask your first question

Let’s start with understanding your codebase. Try one of these commands:

Claude Code reads your project files as needed. You don’t have to manually add context.

## Step 5: Make your first code change

Now let’s make Claude Code do some actual coding. Try a simple task:

- Find the appropriate file
- Show you the proposed changes
- Ask for your approval
- Make the edit

Claude Code always asks for permission before modifying files. You can approve individual changes or enable “Accept all” mode for a session.

## Step 6: Use Git with Claude Code

Claude Code makes Git operations conversational:

## Step 7: Fix a bug or add a feature

Claude is proficient at debugging and feature implementation. Describe what you want in natural language:

- Locate the relevant code
- Understand the context
- Implement a solution
- Run tests if available

## Step 8: Test out other common workflows

There are a number of ways to work with Claude: Refactor code

## Essential commands

Here are the most important commands for daily use:

CommandWhat it doesExample

```
claude
```

Start interactive mode

```
claude
```

```
claude "task"
```

Run a one-time task

```
claude "fix the build error"
```

```
claude -p "query"
```

Run one-off query, then exit

```
claude -p "explain this function"
```

```
claude -c
```

Continue most recent conversation in current directory

```
claude -c
```

```
claude -r
```

Resume a previous conversation

```
claude -r
```

```
/clear
```

Clear conversation history

```
/clear
```

```
/help
```

Show available commands

```
/help
```

```
exit
```

or Ctrl+DExit Claude Code

```
exit
```

[[CLI reference - Claude Code Docs|CLI reference]]for a complete list of commands.

## Pro tips for beginners

For more, see

[[Best Practices for Claude Code - Claude Code Docs|best practices]]and

[[Common workflows - Claude Code Docs|common workflows]].

###

Be specific with your requests

Be specific with your requests

Instead of: “fix the bug”Try: “fix the login bug where users see a blank screen after entering wrong credentials”

###

Use step-by-step instructions

Use step-by-step instructions

Break complex tasks into steps:

###

Let Claude explore first

Let Claude explore first

Before making changes, let Claude understand your code:

###

Save time with shortcuts

Save time with shortcuts

- Press

  ```
  ?
  ```

  to see all available keyboard shortcuts
- Use Tab for command completion
- Press ↑ for command history
- Type

  ```
  /
  ```

  to see all commands and skills

## What’s next?

Now that you’ve learned the basics, explore more advanced features:

## How Claude Code works

Understand the agentic loop, built-in tools, and how Claude Code interacts with your project

## Best practices

Get better results with effective prompting and project setup

## Common workflows

Step-by-step guides for common tasks

## Extend Claude Code

Customize with CLAUDE.md, skills, hooks, MCP, and more

## Getting help

- In Claude Code: Type

  ```
  /help
  ```

  or ask “how do I…”
- Documentation: You’re here! Browse other guides
- Community: Join our [Discord](https://www.anthropic.com/discord)for tips and support

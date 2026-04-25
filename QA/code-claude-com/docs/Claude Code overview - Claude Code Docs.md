---
title: Claude Code overview - Claude Code Docs
source_url: https://code.claude.com/docs/en
description: Claude Code is an agentic coding tool that reads your codebase, edits
  files, runs commands, and integrates with your development tools. Available in your
  termin
---

## Get started

Choose your environment to get started. Most surfaces require a

[Claude subscription](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=overview_pricing)or

[Anthropic Console](https://console.anthropic.com/)account. The Terminal CLI and VS Code also support

[[Enterprise deployment overview - Claude Code Docs|third-party providers]].

- Terminal
- VS Code
- Desktop app
- Web
- JetBrains

The full-featured CLI for working with Claude Code directly in your terminal. Edit files, run commands, and manage your entire project from the command line.To install Claude Code, use one of the following methods:You can also install with You’ll be prompted to log in on first use. That’s it!

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

[[Advanced setup - Claude Code Docs#Install with Linux package managers|apt, dnf, or apk]]on Debian, Fedora, RHEL, and Alpine.Then start Claude Code in any project:[[Quickstart - Claude Code Docs|Continue with the Quickstart →]]

## What you can do

Here are some of the ways you can use Claude Code:

###

Automate the work you keep putting off

Automate the work you keep putting off

Claude Code handles the tedious tasks that eat up your day: writing tests for untested code, fixing lint errors across a project, resolving merge conflicts, updating dependencies, and writing release notes.

###

Build features and fix bugs

Build features and fix bugs

Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works.For bugs, paste an error message or describe the symptom. Claude Code traces the issue through your codebase, identifies the root cause, and implements a fix. See

[[Common workflows - Claude Code Docs|common workflows]]for more examples.

###

Create commits and pull requests

Create commits and pull requests

Claude Code works directly with git. It stages changes, writes commit messages, creates branches, and opens pull requests.In CI, you can automate code review and issue triage with

[[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]or[[Claude Code GitLab CICD - Claude Code Docs|GitLab CI/CD]].

###

Connect your tools with MCP

Connect your tools with MCP

The

[[Connect Claude Code to tools via MCP - Claude Code Docs|Model Context Protocol (MCP)]]is an open standard for connecting AI tools to external data sources. With MCP, Claude Code can read your design docs in Google Drive, update tickets in Jira, pull data from Slack, or use your own custom tooling.

###

Customize with instructions, skills, and hooks

Customize with instructions, skills, and hooks

[[How Claude remembers your project - Claude Code Docs|is a markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards, architecture decisions, preferred libraries, and review checklists. Claude also builds]]

```
CLAUDE.md
```

[[How Claude remembers your project - Claude Code Docs#Auto memory|auto memory]]as it works, saving learnings like build commands and debugging insights across sessions without you writing anything.Create

[[Extend Claude with skills - Claude Code Docs|custom commands]]to package repeatable workflows your team can share, like

```
/review-pr
```

or

```
/deploy-staging
```

.

[[Hooks reference - Claude Code Docs|Hooks]]let you run shell commands before or after Claude Code actions, like auto-formatting after every file edit or running lint before a commit.

###

Run agent teams and build custom agents

Run agent teams and build custom agents

Spawn

[[Create custom subagents - Claude Code Docs|multiple Claude Code agents]]that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results.For fully custom workflows, the[[Agent SDK overview - Claude Code Docs|Agent SDK]]lets you build your own agents powered by Claude Code’s tools and capabilities, with full control over orchestration, tool access, and permissions.

###

Pipe, script, and automate with the CLI

Pipe, script, and automate with the CLI

Claude Code is composable and follows the Unix philosophy. Pipe logs into it, run it in CI, or chain it with other tools:See the

[[CLI reference - Claude Code Docs|CLI reference]]for the full set of commands and flags.

###

Schedule recurring tasks

Schedule recurring tasks

Run Claude on a schedule to automate work that repeats: morning PR reviews, overnight CI failure analysis, weekly dependency audits, or syncing docs after PRs merge.

- [[Automate work with routines - Claude Code Docs|Routines]]run on Anthropic-managed infrastructure, so they keep running even when your computer is off. They can also trigger on API calls or GitHub events. Create them from the web, the Desktop app, or by running

  ```
  /schedule
  ```

  in the CLI.
- [[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|Desktop scheduled tasks]]run on your machine, with direct access to your local files and tools
- repeats a prompt within a CLI session for quick polling

  ```
  /loop
  ```

###

Work from anywhere

Work from anywhere

Sessions aren’t tied to a single surface. Move work between environments as your context changes:

- Step away from your desk and keep working from your phone or any browser with [[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]
- Message [[Use Claude Code Desktop - Claude Code Docs#Sessions from Dispatch|Dispatch]]a task from your phone and open the Desktop session it creates
- Kick off a long-running task on the [[Use Claude Code on the web - Claude Code Docs|web]]or[iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684), then pull it into your terminal with

  ```
  claude --teleport
  ```
- Hand off a terminal session to the [[Use Claude Code Desktop - Claude Code Docs|Desktop app]]with

  ```
  /desktop
  ```

  for visual diff review
- Route tasks from team chat: mention

  ```
  @Claude
  ```

  in[[Claude Code in Slack - Claude Code Docs|Slack]]with a bug report and get a pull request back

## Use Claude Code everywhere

Each surface connects to the same underlying Claude Code engine, so your CLAUDE.md files, settings, and MCP servers work across all of them. Beyond the

[[Quickstart - Claude Code Docs|Terminal]],

[[Use Claude Code in VS Code - Claude Code Docs|VS Code]],

[[JetBrains IDEs - Claude Code Docs|JetBrains]],

[[Use Claude Code Desktop - Claude Code Docs|Desktop]], and

[[Use Claude Code on the web - Claude Code Docs|Web]]environments above, Claude Code integrates with CI/CD, chat, and browser workflows:

I want to…Best optionContinue a local session from my phone or another device

[[Push events into a running session with channels - Claude Code Docs|Channels]][[Use Claude Code on the web - Claude Code Docs|Web]]or[Claude iOS app](https://apps.apple.com/app/claude-by-anthropic/id6473753684)[[Automate work with routines - Claude Code Docs|Routines]]or[[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|Desktop scheduled tasks]][[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]or[[Claude Code GitLab CICD - Claude Code Docs|GitLab CI/CD]][[Code Review - Claude Code Docs|GitHub Code Review]][[Claude Code in Slack - Claude Code Docs|Slack]][[Use Claude Code with Chrome (beta) - Claude Code Docs|Chrome]][[Agent SDK overview - Claude Code Docs|Agent SDK]]

## Next steps

Once you’ve installed Claude Code, these guides help you go deeper.

- [[Quickstart - Claude Code Docs|Quickstart]]: walk through your first real task, from exploring a codebase to committing a fix
- [[How Claude remembers your project - Claude Code Docs|Store instructions and memories]]: give Claude persistent instructions with CLAUDE.md files and auto memory
- [[Common workflows - Claude Code Docs|Common workflows]]and[[Best Practices for Claude Code - Claude Code Docs|best practices]]: patterns for getting the most out of Claude Code
- [[Claude Code settings - Claude Code Docs|Settings]]: customize Claude Code for your workflow
- [[Troubleshooting - Claude Code Docs|Troubleshooting]]: solutions for common issues
- [[Claude Code by Anthropic AI Coding Agent, Terminal, IDE|code.claude.com]]: demos, pricing, and product details

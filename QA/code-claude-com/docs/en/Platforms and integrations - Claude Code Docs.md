---
title: Platforms and integrations - Claude Code Docs
source_url: https://code.claude.com/docs/en/platforms
description: Choose where to run Claude Code and what to connect it to. Compare the
  CLI, Desktop, VS Code, JetBrains, web, mobile, and integrations like Chrome, Slack,
  and C
---

## Where to run Claude Code

Choose a platform based on how you like to work and where your project lives.

PlatformBest forWhat you get

[[Run Claude Code programmatically - Claude Code Docs|Agent SDK]],[[Let Claude use your computer from the CLI - Claude Code Docs|computer use]]on macOS (Pro and Max), third-party providers[[Use Claude Code Desktop - Claude Code Docs|Desktop]][[Use Claude Code Desktop - Claude Code Docs#Let Claude use your computer|computer use]]and[[Use Claude Code Desktop - Claude Code Docs#Sessions from Dispatch|Dispatch]]on Pro and Max[[Use Claude Code in VS Code - Claude Code Docs|VS Code]][[JetBrains IDEs - Claude Code Docs|JetBrains]][[Use Claude Code on the web - Claude Code Docs|Web]][[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]for local sessions,[[Use Claude Code Desktop - Claude Code Docs#Sessions from Dispatch|Dispatch]]to Desktop on Pro and Max

## Connect your tools

Integrations let Claude work with services outside your codebase.

IntegrationWhat it doesUse it for

[[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]][[Claude Code GitLab CICD - Claude Code Docs|GitLab CI/CD]][[Code Review - Claude Code Docs|Code Review]][[Claude Code in Slack - Claude Code Docs|Slack]]

```
@Claude
```

mentions in your channels

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP servers]]and

[[Use Claude Code Desktop - Claude Code Docs#Connect external tools|connectors]]let you connect almost anything: Linear, Notion, Google Drive, or your own internal APIs.

## Work when you are away from your terminal

Claude Code offers several ways to work when you’re not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

TriggerClaude runs onSetupBest for

[Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068)[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]][claude.ai/code](https://claude.ai/code)or the Claude mobile app

```
claude remote-control
```

[[Push events into a running session with channels - Claude Code Docs|Channels]][[Push events into a running session with channels - Claude Code Docs#Quickstart|Install a channel plugin]]or[[Channels reference - Claude Code Docs|build your own]][[Claude Code in Slack - Claude Code Docs|Slack]]

```
@Claude
```

in a team channel[[Claude Code in Slack - Claude Code Docs#Setting up Claude Code in Slack|Install the Slack app]]with[[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]enabled[[Run prompts on a schedule - Claude Code Docs|Scheduled tasks]][[Run prompts on a schedule - Claude Code Docs|CLI]],[[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|Desktop]], or[[Automate work with routines - Claude Code Docs|cloud]]

[[Quickstart - Claude Code Docs|install the CLI]]and run it in a project directory. If you’d rather not use a terminal,

[[Get started with the desktop app - Claude Code Docs|Desktop]]gives you the same engine with a graphical interface.

## Related resources

### Platforms

- [[Quickstart - Claude Code Docs|CLI quickstart]]: install and run your first command in the terminal
- [[Use Claude Code Desktop - Claude Code Docs|Desktop]]: visual diff review, parallel sessions, computer use, and Dispatch
- [[Use Claude Code in VS Code - Claude Code Docs|VS Code]]: the Claude Code extension inside your editor
- [[JetBrains IDEs - Claude Code Docs|JetBrains]]: the extension for IntelliJ, PyCharm, and other JetBrains IDEs
- [[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]: cloud sessions that keep running when you disconnect
- Mobile: the Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684)and[Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)for starting and monitoring tasks while away from your computer

### Integrations

- [[Use Claude Code with Chrome (beta) - Claude Code Docs|Chrome]]: automate browser tasks with your logged-in sessions
- [[Let Claude use your computer from the CLI - Claude Code Docs|Computer use]]: let Claude open apps and control your screen on macOS
- [[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]: run Claude in your CI pipeline
- [[Claude Code GitLab CICD - Claude Code Docs|GitLab CI/CD]]: the same for GitLab
- [[Code Review - Claude Code Docs|Code Review]]: automatic review on every pull request
- [[Claude Code in Slack - Claude Code Docs|Slack]]: send tasks from team chat, get PRs back

### Remote access

- [[Use Claude Code Desktop - Claude Code Docs#Sessions from Dispatch|Dispatch]]: message a task from your phone and it can spawn a Desktop session
- [[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]: drive a running session from your phone or browser
- [[Push events into a running session with channels - Claude Code Docs|Channels]]: push events from chat apps or your own servers into a session
- [[Run prompts on a schedule - Claude Code Docs|Scheduled tasks]]: run prompts on a recurring schedule

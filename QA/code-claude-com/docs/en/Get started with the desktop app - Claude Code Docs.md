---
title: Get started with the desktop app - Claude Code Docs
source_url: https://code.claude.com/docs/en/desktop-quickstart
description: Install Claude Code on desktop and start your first coding session
---

## Download for macOS

Universal build for Intel and Apple Silicon

## Download for Windows

For x64 processors

[ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs). Linux is not supported.

Claude Code requires a

[Pro, Max, Team, or Enterprise subscription](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=desktop_quickstart_pricing).

[[Use Claude Code Desktop - Claude Code Docs|Use Claude Code Desktop]]for the full reference. The desktop app has three tabs:

- Chat: General conversation with no file access, similar to claude.ai.
- Cowork: An autonomous background agent that works on tasks in a cloud VM with its own environment. It can run independently while you do other work.
- Code: An interactive coding assistant with direct access to your local files. You review and approve each change in real time.

[Claude Desktop support articles](https://support.claude.com/en/collections/16163169-claude-desktop). This page focuses on the Code tab.

## Install

Install and sign in

Download the installer for your platform from the links above and run it. Launch Claude from your Applications folder on macOS or the Start menu on Windows, then sign in with your Anthropic account.

Open the Code tab

Click the Code tab at the top center. If clicking Code prompts you to upgrade, you need to

[subscribe to a paid plan](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=desktop_quickstart_upgrade)first. If it prompts you to sign in online, complete the sign-in and restart the app. If you see a 403 error, see[[Use Claude Code Desktop - Claude Code Docs#403 or authentication errors in the Code tab|authentication troubleshooting]].

```
claude
```

from the terminal, install the CLI separately. See

[[Quickstart - Claude Code Docs|Get started with the CLI]].

## Start your first session

With the Code tab open, choose a project and give Claude something to do.

Choose an environment and folder

Select Local to run Claude on your machine using your files directly. Click Select folder and choose your project directory.You can also select:

- Remote: Run sessions on Anthropic’s cloud infrastructure that continue even if you close the app. Remote sessions use the same infrastructure as [[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]].
- SSH: Connect to a remote machine over SSH (your own servers, cloud VMs, or dev containers). Claude Code must be installed on the remote machine.

Choose a model

Select a model from the dropdown next to the send button. See

[[Model configuration - Claude Code Docs#Available models|models]]for a comparison of Opus, Sonnet, and Haiku. You can change the model later from the same dropdown.

Tell Claude what to do

Type what you want Claude to do:

- ```
  Find a TODO comment and fix it
  ```
- ```
  Add tests for the main function
  ```
- ```
  Create a CLAUDE.md with instructions for this codebase
  ```

[[Use Claude Code Desktop - Claude Code Docs#Work in parallel with sessions|session]]is a conversation with Claude about your code. Each session tracks its own context and changes, so you can work on multiple tasks without them interfering with each other.

Review and accept changes

By default, the Code tab starts in

[[Use Claude Code Desktop - Claude Code Docs#Choose a permission mode|Ask permissions mode]], where Claude proposes changes and waits for your approval before applying them. You’ll see:

- A [[Use Claude Code Desktop - Claude Code Docs#Review changes with diff view|diff view]]showing exactly what will change in each file
- Accept/Reject buttons to approve or decline each change
- Real-time updates as Claude works through your request

## Now what?

You’ve made your first edit. For the full reference on everything Desktop can do, see

[[Use Claude Code Desktop - Claude Code Docs|Use Claude Code Desktop]]. Here are some things to try next. Interrupt and steer. You can interrupt Claude at any point. If it’s going down the wrong path, click the stop button or type your correction and press Enter. Claude stops what it’s doing and adjusts based on your input. You don’t have to wait for it to finish or start over. Give Claude more context. Type

```
@filename
```

in the prompt box to pull a specific file into the conversation, attach images and PDFs using the attachment button, or drag and drop files directly into the prompt. The more context Claude has, the better the results. See

[[Use Claude Code Desktop - Claude Code Docs#Add files and context to prompts|Add files and context]]. Use skills for repeatable tasks. Type

```
/
```

or click + → Slash commands to browse

[[Commands - Claude Code Docs|built-in commands]],

[[Extend Claude with skills - Claude Code Docs|custom skills]], and plugin skills. Skills are reusable prompts you can invoke whenever you need them, like code review checklists or deployment steps. Review changes before committing. After Claude edits files, a

```
+12 -1
```

indicator appears. Click it to open the

[[Use Claude Code Desktop - Claude Code Docs#Review changes with diff view|diff view]], review modifications file by file, and comment on specific lines. Claude reads your comments and revises. Click Review code to have Claude evaluate the diffs itself and leave inline suggestions. Adjust how much control you have. Your

[[Use Claude Code Desktop - Claude Code Docs#Choose a permission mode|permission mode]]controls the balance. Ask permissions (default) requires approval before every edit. Auto accept edits auto-accepts file edits for faster iteration. Plan mode lets Claude map out an approach without touching any files, which is useful before a large refactor. Add plugins for more capabilities. Click the + button next to the prompt box and select Plugins to browse and install

[[Use Claude Code Desktop - Claude Code Docs#Install plugins|plugins]]that add skills, agents, MCP servers, and more. Arrange your workspace. Drag the chat, diff, terminal, file, and preview panes into whatever layout you want. Open the terminal with Ctrl+` to run commands alongside your session, or click a file path to open it in the file pane. See

[[Use Claude Code Desktop - Claude Code Docs#Arrange your workspace|Arrange your workspace]]. Preview your app. Click the Preview dropdown to run your dev server directly in the desktop. Claude can view the running app, test endpoints, inspect logs, and iterate on what it sees. See

[[Use Claude Code Desktop - Claude Code Docs#Preview your app|Preview your app]]. Track your pull request. After opening a PR, Claude Code monitors CI check results and can automatically fix failures or merge the PR once all checks pass. See

[[Use Claude Code Desktop - Claude Code Docs#Monitor pull request status|Monitor pull request status]]. Put Claude on a schedule. Set up

[[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|scheduled tasks]]to run Claude automatically on a recurring basis: a daily code review every morning, a weekly dependency audit, or a briefing that pulls from your connected tools. Scale up when you’re ready. Open

[[Use Claude Code Desktop - Claude Code Docs#Work in parallel with sessions|parallel sessions]]from the sidebar to work on multiple tasks at once, each in its own Git worktree, and open the

[[Use Claude Code Desktop - Claude Code Docs#Watch background tasks|tasks pane]]to watch the subagents and background commands a session has running. Open a

[[Use Claude Code Desktop - Claude Code Docs#Ask a side question without derailing the session|side chat]]to ask a question without derailing the main thread. Send

[[Use Claude Code Desktop - Claude Code Docs#Run long-running tasks remotely|long-running work to the cloud]]so it continues even if you close the app, or

[[Use Claude Code Desktop - Claude Code Docs#Continue in another surface|continue a session on the web or in your IDE]]if a task takes longer than expected.

[[Use Claude Code Desktop - Claude Code Docs#Extend Claude Code|Connect external tools]]like GitHub, Slack, and Linear to bring your workflow together.

## Coming from the CLI?

Desktop runs the same engine as the CLI with a graphical interface. You can run both simultaneously on the same project, and they share configuration (CLAUDE.md files, MCP servers, hooks, skills, and settings). For a full comparison of features, flag equivalents, and what’s not available in Desktop, see

[[Use Claude Code Desktop - Claude Code Docs#Coming from the CLI?|CLI comparison]].

## What’s next

- [[Use Claude Code Desktop - Claude Code Docs|Use Claude Code Desktop]]: permission modes, parallel sessions, diff view, connectors, and enterprise configuration
- [[Use Claude Code Desktop - Claude Code Docs#Troubleshooting|Troubleshooting]]: solutions to common errors and setup issues
- [[Best Practices for Claude Code - Claude Code Docs|Best practices]]: tips for writing effective prompts and getting the most out of Claude Code
- [[Common workflows - Claude Code Docs|Common workflows]]: tutorials for debugging, refactoring, testing, and more

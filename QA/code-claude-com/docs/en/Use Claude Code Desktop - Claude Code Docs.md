---
title: Use Claude Code Desktop - Claude Code Docs
source_url: https://code.claude.com/docs/en/desktop
description: 'Get more out of Claude Code Desktop: parallel sessions with Git isolation,
  drag-and-drop pane layout, integrated terminal and file editor, side chats, computer '
---

## Download for macOS

Universal build for Intel and Apple Silicon

## Download for Windows

For x64 processors

[ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs). Linux is not supported. After installing, launch Claude, sign in, and click the Code tab. See the

[[Get started with the desktop app - Claude Code Docs|Get started guide]]for a full walkthrough of your first session. Desktop adds these capabilities on top of the standard Claude Code experience:

- [[Use Claude Code Desktop - Claude Code Docs#Work in parallel with sessions|Parallel sessions]]with automatic Git worktree isolation
- [[Use Claude Code Desktop - Claude Code Docs#Arrange your workspace|Drag-and-drop layout]]with an integrated terminal, file editor, and preview pane
- [[Use Claude Code Desktop - Claude Code Docs#Ask a side question without derailing the session|Side chats]]that branch off without affecting the main thread
- [[Use Claude Code Desktop - Claude Code Docs#Review changes with diff view|Visual diff review]]with inline comments
- [[Use Claude Code Desktop - Claude Code Docs#Preview your app|Live app preview]]with dev servers, HTML files, and PDFs
- [[Use Claude Code Desktop - Claude Code Docs#Let Claude use your computer|Computer use]]to open apps and control your screen on macOS and Windows
- [[Use Claude Code Desktop - Claude Code Docs#Monitor pull request status|GitHub PR monitoring]]with auto-fix, auto-merge, and auto-archive
- [[Use Claude Code Desktop - Claude Code Docs#Sessions from Dispatch|Dispatch]]integration: send a task from your phone, get a session here
- [[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|Scheduled tasks]]that run Claude on a recurring schedule
- [[Use Claude Code Desktop - Claude Code Docs#Connect external tools|Connectors]]for GitHub, Slack, Linear, and more
- Local, [[Use Claude Code Desktop - Claude Code Docs#SSH sessions|SSH]], and[[Use Claude Code Desktop - Claude Code Docs#Run long-running tasks remotely|cloud]]environments

The workspace layout, terminal, file editor, side chats, and view modes described on this page require Claude Desktop v1.2581.0 or later. Open Claude → Check for Updates on macOS or Help → Check for Updates on Windows to update.

[[Use Claude Code Desktop - Claude Code Docs#Work with code|working with code]],

[[Use Claude Code Desktop - Claude Code Docs#Arrange your workspace|arranging your workspace]],

[[Use Claude Code Desktop - Claude Code Docs#Let Claude use your computer|computer use]],

[[Use Claude Code Desktop - Claude Code Docs#Manage sessions|managing sessions]],

[[Use Claude Code Desktop - Claude Code Docs#Extend Claude Code|extending Claude Code]], and

[[Use Claude Code Desktop - Claude Code Docs#Environment configuration|configuration]]. It also includes a

[[Use Claude Code Desktop - Claude Code Docs#Coming from the CLI?|CLI comparison]]and

[[Use Claude Code Desktop - Claude Code Docs#Troubleshooting|troubleshooting]].

## Start a session

Before you send your first message, configure four things in the prompt area:

- Environment: choose where Claude runs. Select Local for your machine, Remote for Anthropic-hosted cloud sessions, or an [[Use Claude Code Desktop - Claude Code Docs#SSH sessions|SSH connection]]for a remote machine you manage. See[[Use Claude Code Desktop - Claude Code Docs#Environment configuration|environment configuration]].
- Project folder: select the folder or repository Claude works in. For remote sessions, you can add [[Use Claude Code Desktop - Claude Code Docs#Run long-running tasks remotely|multiple repositories]].
- Model: pick a [[Model configuration - Claude Code Docs#Available models|model]]from the dropdown next to the send button. You can change this during the session.
- Permission mode: choose how much autonomy Claude has from the [[Use Claude Code Desktop - Claude Code Docs#Choose a permission mode|mode selector]]. You can change this during the session.

## Work with code

Give Claude the right context, control how much it does on its own, and review what it changed.

### Use the prompt box

Type what you want Claude to do and press Enter to send. Claude reads your project files, makes changes, and runs commands based on your

[[Use Claude Code Desktop - Claude Code Docs#Choose a permission mode|permission mode]]. You can interrupt Claude at any point: click the stop button or type your correction and press Enter. Claude stops what it’s doing and adjusts based on your input. The + button next to the prompt box gives you access to file attachments,

[[Use Claude Code Desktop - Claude Code Docs#Use skills|skills]],

[[Use Claude Code Desktop - Claude Code Docs#Connect external tools|connectors]], and

[[Use Claude Code Desktop - Claude Code Docs#Install plugins|plugins]].

### Add files and context to prompts

The prompt box supports two ways to bring in external context:

- @mention files: type

  ```
  @
  ```

  followed by a filename to add a file to the conversation context. Claude can then read and reference that file. @mention is not available in remote sessions.
- Attach files: attach images, PDFs, and other files to your prompt using the attachment button, or drag and drop files directly into the prompt. This is useful for sharing screenshots of bugs, design mockups, or reference documents.

### Choose a permission mode

Permission modes control how much autonomy Claude has during a session: whether it asks before editing files, running commands, or both. You can switch modes at any time using the mode selector next to the send button. Start with Ask permissions to see exactly what Claude does, then move to Auto accept edits or Plan mode as you get comfortable.

ModeSettings keyBehaviorAsk permissions

```
default
```

Claude asks before editing files or running commands. You see a diff and can accept or reject each change. Recommended for new users.Auto accept edits

```
acceptEdits
```

Claude auto-accepts file edits and common filesystem commands like

```
mkdir
```

,

```
touch
```

, and

```
mv
```

, but still asks before running other terminal commands. Use this when you trust file changes and want faster iteration.Plan mode

```
plan
```

Claude reads files and runs commands to explore, then proposes a plan without editing your source code. Good for complex tasks where you want to review the approach first.Auto

```
auto
```

Claude executes all actions with background safety checks that verify alignment with your request. Reduces permission prompts while maintaining oversight. Currently a research preview. Available on Max, Team, Enterprise, and API plans. Requires Claude Sonnet 4.6, Opus 4.6, or Opus 4.7 on Team, Enterprise, and API plans; Claude Opus 4.7 only on Max plans. Not available on Pro plans or third-party providers. Enable in your Settings → Claude Code.Bypass permissions

```
bypassPermissions
```

Claude runs without any permission prompts, equivalent to

```
--dangerously-skip-permissions
```

in the CLI. Enable in your Settings → Claude Code under “Allow bypass permissions mode”. Only use this in sandboxed containers or VMs. Enterprise admins can disable this option.

```
dontAsk
```

permission mode is available only in the

[[Choose a permission mode - Claude Code Docs#Allow only pre-approved tools with dontAsk mode|CLI]]. Remote sessions support Auto accept edits and Plan mode. Ask permissions is not available because remote sessions auto-accept file edits by default, and Bypass permissions is not available because the remote environment is already sandboxed. Enterprise admins can restrict which permission modes are available. See

[[Use Claude Code Desktop - Claude Code Docs#Enterprise configuration|enterprise configuration]]for details.

### Preview your app

Claude can start a dev server and open an embedded browser to verify its changes. This works for frontend web apps as well as backend servers: Claude can test API endpoints, view server logs, and iterate on issues it finds. In most cases, Claude starts the server automatically after editing project files. You can also ask Claude to preview at any time. By default, Claude

[[Use Claude Code Desktop - Claude Code Docs#Auto-verify changes|auto-verifies]]changes after every edit. The preview pane can also open static HTML files, PDFs, and images from your project. Click an HTML, PDF, or image path in the chat to open it in preview. From the preview pane, you can:

- Interact with your running app directly in the embedded browser
- Watch Claude verify its own changes automatically: it takes screenshots, inspects the DOM, clicks elements, fills forms, and fixes issues it finds
- Start or stop servers from the Preview dropdown in the session toolbar
- Persist cookies and local storage across server restarts by selecting Persist sessions in the dropdown, so you don’t have to re-login during development
- Edit the server configuration or stop all servers at once

```
.claude/launch.json
```

to match your setup. See

[[Use Claude Code Desktop - Claude Code Docs#Configure preview servers|Configure preview servers]]for the full reference. To clear saved session data, toggle Persist preview sessions off in Settings → Claude Code. To disable preview entirely, toggle off Preview in Settings → Claude Code.

### Review changes with diff view

After Claude makes changes to your code, the diff view lets you review modifications file by file before creating a pull request. When Claude changes files, a diff stats indicator appears showing the number of lines added and removed, such as

```
+12 -1
```

. Click this indicator to open the diff viewer, which displays a file list on the left and the changes for each file on the right.
To comment on specific lines, click any line in the diff to open a comment box. Type your feedback and press Enter to add the comment. After adding comments to multiple lines, submit all comments at once:

- macOS: press Cmd+Enter
- Windows: press Ctrl+Enter

### Review your code

In the diff view, click Review code in the top-right toolbar to ask Claude to evaluate the changes before you commit. Claude examines the current diffs and leaves comments directly in the diff view. You can respond to any comment or ask Claude to revise. The review focuses on high-signal issues: compile errors, definite logic errors, security vulnerabilities, and obvious bugs. It does not flag style, formatting, pre-existing issues, or anything a linter would catch.

### Monitor pull request status

After you open a pull request, a CI status bar appears in the session. Claude Code uses the GitHub CLI to poll check results and surface failures.

- Auto-fix: when enabled, Claude automatically attempts to fix failing CI checks by reading the failure output and iterating.
- Auto-merge: when enabled, Claude merges the PR once all checks pass. The merge method is squash. Auto-merge must be [enabled in your GitHub repository settings](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository)for this to work.

[[Use Claude Code Desktop - Claude Code Docs#Work in parallel with sessions|auto-archive]]in Settings → Claude Code.

PR monitoring requires the

[GitHub CLI (](https://cli.github.com/)to be installed and authenticated on your machine. If

```
gh
```

)

```
gh
```

is not installed, Desktop prompts you to install it the first time you try to create a PR.

## Arrange your workspace

The desktop app is built around panes you can arrange in any layout: chat, diff, preview, terminal, file, plan, tasks, and subagent. Drag a pane by its header to reposition it, or drag a pane edge to resize it. Press Cmd+\ on macOS or Ctrl+\ on Windows to close the focused pane. Open additional panes from the Views menu in the session toolbar.

### Run commands in the terminal

The integrated terminal lets you run commands alongside your session without switching to another app. Open it from the Views menu or press Ctrl+` on macOS or Windows. The terminal opens in your session’s working directory and shares the same environment as Claude, so commands like

```
npm test
```

or

```
git status
```

see the same files Claude is editing. The terminal is available in local sessions only.

### Open and edit files

Click a file path in the chat or diff viewer to open it in the file pane. HTML, PDF, and image paths open in the

[[Use Claude Code Desktop - Claude Code Docs#Preview your app|preview pane]]instead. Make spot edits and click Save to write them back. If the file changed on disk since you opened it, the pane warns you and lets you override or discard. Click Discard to revert your edits, or click the path in the pane header to copy the absolute path. The file pane is available in local and SSH sessions. For remote sessions, ask Claude to make the change.

### Open files in other apps

Right-click any file path in the chat, diff viewer, or file pane to open a context menu:

- Attach as context: add the file to your next prompt
- Open in: open the file in an installed editor such as VS Code, Cursor, or Zed
- Show in Finder on macOS, Show in Explorer on Windows: open the containing folder
- Copy path: copy the absolute path to your clipboard

### Switch view modes

View modes control how much detail appears in the chat transcript. Switch modes from the Transcript view dropdown next to the send button, or press Ctrl+O on macOS or Windows to cycle through them.

ModeWhat it showsNormalTool calls collapsed into summaries, with full text responsesVerboseEvery tool call, file read, and intermediate step Claude takesSummaryOnly Claude’s final responses and the changes it made

### Keyboard shortcuts

Press Cmd+/ on macOS or Ctrl+/ on Windows to see all shortcuts available in the Code tab. On Windows, use Ctrl in place of Cmd for the shortcuts below. Session cycling, the terminal toggle, and the view-mode toggle use Ctrl on every platform.

ShortcutAction

```
Cmd
```

```
/
```

Show keyboard shortcuts

```
Cmd
```

```
N
```

New session

```
Cmd
```

```
W
```

Close session

```
Ctrl
```

```
Tab
```

/

```
Ctrl
```

```
Shift
```

```
Tab
```

Next or previous session

```
Cmd
```

```
Shift
```

```
]
```

/

```
Cmd
```

```
Shift
```

```
[[Interactive mode - Claude Code Docs#Keyboard shortcuts|
```

Next or previous session

```
Esc
```

Stop Claude’s response

```
Cmd
```

```
Shift
```

```
D
```

Toggle diff pane

```
Cmd
```

```
Shift
```

```
P
```

Toggle preview pane

```
Cmd
```

```
Shift
```

```
S
```

Select an element in preview

```
Ctrl
```

```
`
```

Toggle terminal pane

```
Cmd
```

```
\
```

Close focused pane

```
Cmd
```

```
;
```

Open side chat

```
Ctrl
```

```
O
```

Cycle view modes

```
Cmd
```

```
Shift
```

```
M
```

Open permission mode menu

```
Cmd
```

```
Shift
```

```
I
```

Open model menu

```
Cmd
```

```
Shift
```

```
E
```

Open effort menu

```
1
```

–

```
9
```

Select item in an open menu

[interactive mode shortcuts]], such as

```
Shift+Tab
```

to cycle modes, do not apply in Desktop.

### Check usage

Click the usage ring next to the model picker to see your current context window usage and your plan usage for the period. Context usage is per session; plan usage is shared across all your Claude Code surfaces.

## Let Claude use your computer

Computer use lets Claude open your apps, control your screen, and work directly on your machine the way you would. Ask Claude to test a native app in a mobile simulator, interact with a desktop tool that has no CLI, or automate something that only works through a GUI.

Computer use is a research preview on macOS and Windows that requires a Pro or Max plan. It is not available on Team or Enterprise plans. The Claude Desktop app must be running.

[[Use Claude Code Desktop - Claude Code Docs#Enable computer use|Enable it in Settings]]before Claude can control your screen. On macOS, you also need to grant Accessibility and Screen Recording permissions.

### When computer use applies

Claude has several ways to interact with an app or service, and computer use is the broadest and slowest. It tries the most precise tool first:

- If you have a [[Use Claude Code Desktop - Claude Code Docs#Connect external tools|connector]]for a service, Claude uses the connector.
- If the task is a shell command, Claude uses Bash.
- If the task is browser work and you have [[Use Claude Code with Chrome (beta) - Claude Code Docs|Claude in Chrome]]set up, Claude uses that.
- If none of those apply, Claude uses computer use.

[[Use Claude Code Desktop - Claude Code Docs#App permissions|per-app access tiers]]reinforce this: browsers are capped at view-only, and terminals and IDEs at click-only, steering Claude toward the dedicated tool even when computer use is active. Screen control is reserved for things nothing else can reach, like native apps, hardware control panels, mobile simulators, or proprietary tools without an API.

### Enable computer use

Computer use is off by default. If you ask Claude to do something that needs it while it’s off, Claude tells you it could do the task if you enable computer use in Settings.

Update the desktop app

Make sure you have the latest version of Claude Desktop. Download or update at

[claude.com/download](https://claude.com/download), then restart the app.

Turn on the toggle

In the desktop app, go to Settings > General (under Desktop app). Find the Computer use toggle and turn it on. On Windows, the toggle takes effect immediately and setup is complete. On macOS, continue to the next step.If you don’t see the toggle, confirm you’re on macOS or Windows with a Pro or Max plan, then update and restart the app.

Grant macOS permissions

On macOS, grant two system permissions before the toggle takes effect:

- Accessibility: lets Claude click, type, and scroll
- Screen Recording: lets Claude see what’s on your screen

### App permissions

The first time Claude needs to use an app, a prompt appears in your session. Click Allow for this session or Deny. Approvals last for the current session, or 30 minutes in

[[Use Claude Code Desktop - Claude Code Docs#Sessions from Dispatch|Dispatch-spawned sessions]]. The prompt also shows what level of control Claude gets for that app. These tiers are fixed by app category and can’t be changed:

TierWhat Claude can doApplies toView onlySee the app in screenshotsBrowsers, trading platformsClick onlyClick and scroll, but not type or use keyboard shortcutsTerminals, IDEsFull controlClick, type, drag, and use keyboard shortcutsEverything else

- Denied apps: add apps here to reject them without prompting. Claude may still affect a denied app indirectly through actions in an allowed app, but it can’t interact with the denied app directly.
- Unhide apps when Claude finishes: while Claude is working, your other windows are hidden so it interacts with only the approved app. When Claude finishes, hidden windows are restored unless you turn this setting off.

## Manage sessions

Each session is an independent conversation with its own context and changes. You can run multiple sessions in parallel, branch off side chats, send work to the cloud, or let Dispatch start sessions for you from your phone.

### Work in parallel with sessions

Click + New session in the sidebar, or press Cmd+N on macOS or Ctrl+N on Windows, to work on multiple tasks in parallel. Press Ctrl+Tab and Ctrl+Shift+Tab to cycle through sessions in the sidebar. For Git repositories, each session gets its own isolated copy of your project using

[[Common workflows - Claude Code Docs#Run parallel Claude Code sessions with Git worktrees|Git worktrees]], so changes in one session don’t affect other sessions until you commit them. Worktrees are stored in

```
<project-root>/.claude/worktrees/
```

by default. You can change this to a custom directory in Settings → Claude Code under “Worktree location”. You can also set a branch prefix that gets prepended to every worktree branch name, which is useful for keeping Claude-created branches organized. To remove a worktree when you’re done, hover over the session in the sidebar and click the archive icon. To have sessions archive themselves when their pull request merges or closes, turn on Auto-archive after PR merge or close in Settings → Claude Code. Auto-archive only applies to local sessions that have finished running.
To include gitignored files like

```
.env
```

in new worktrees, create a

[[Common workflows - Claude Code Docs#Copy gitignored files to worktrees|in your project root.]]

```
.worktreeinclude
```

file

Session isolation requires

[Git](https://git-scm.com/downloads). Most Macs include Git by default. Run

```
git --version
```

in Terminal to check. On Windows, Git is required for the Code tab to work: [download Git for Windows](https://git-scm.com/downloads/win), install it, and restart the app. If you run into Git errors, try a Cowork session to help troubleshoot your setup.

[[Use Claude Code Desktop - Claude Code Docs#Check usage|Check usage]]. When context fills up, Claude automatically summarizes the conversation and continues working. You can also type

```
/compact
```

to trigger summarization earlier and free up context space. See

[[How Claude Code works - Claude Code Docs#The context window|the context window]]for details on how compaction works.

### Ask a side question without derailing the session

A side chat lets you ask Claude a question that uses your session’s context but doesn’t add anything back to the main conversation. Use it when you want to understand a piece of code, check an assumption, or explore an idea without steering the session off course. Press Cmd+; on macOS or Ctrl+; on Windows to open a side chat, or type

```
/btw
```

in the prompt box. The side chat can read everything in the main thread up to that point. When you’re done, close the side chat and continue the main session where you left off. Side chats are available in local and SSH sessions.

### Watch background tasks

The tasks pane shows the background work running inside the current session: subagents, background shell commands, and workflows. Open it from the Views menu or drag it into your layout. Click any entry to see its output in the subagent pane or stop it. To see what other sessions are doing, use the

[[Use Claude Code Desktop - Claude Code Docs#Work in parallel with sessions|sidebar]].

### Run long-running tasks remotely

For large refactors, test suites, migrations, or other long-running tasks, select Remote instead of Local when starting a session. Remote sessions run on Anthropic’s cloud infrastructure and continue even if you close the app or shut down your computer. Check back anytime to see progress or steer Claude in a different direction. You can also monitor remote sessions from

[claude.ai/code](https://claude.ai/code)or the Claude iOS app. Remote sessions also support multiple repositories. After selecting a cloud environment, click the + button next to the repo pill to add additional repositories to the session. Each repo gets its own branch selector. This is useful for tasks that span multiple codebases, such as updating a shared library and its consumers. See

[[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]for more on how remote sessions work.

### Continue in another surface

The Continue in menu, accessible from the VS Code icon in the bottom right of the session toolbar, lets you move your session to another surface:

- Claude Code on the Web: sends your local session to continue running remotely. Desktop pushes your branch, generates a summary of the conversation, and creates a new remote session with the full context. You can then choose to archive the local session or keep it. This requires a clean working tree, and is not available for SSH sessions.
- Your IDE: opens your project in a supported IDE at the current working directory.

### Sessions from Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068)is a persistent conversation with Claude that lives in the

[Cowork](https://claude.com/product/cowork#dispatch-and-computer-use)tab. You message Dispatch a task, and it decides how to handle it. A task can end up as a Code session in two ways: you ask for one directly, such as “open a Claude Code session and fix the login bug”, or Dispatch decides the task is development work and spawns one on its own. Tasks that typically route to Code include fixing bugs, updating dependencies, running tests, or opening pull requests. Research, document editing, and spreadsheet work stay in Cowork. Either way, the Code session appears in the Code tab’s sidebar with a Dispatch badge. You get a push notification on your phone when it finishes or needs your approval. If you have

[[Use Claude Code Desktop - Claude Code Docs#Let Claude use your computer|computer use]]enabled, Dispatch-spawned Code sessions can use it too. App approvals in those sessions expire after 30 minutes and re-prompt, rather than lasting the full session like regular Code sessions. For setup, pairing, and Dispatch settings, see the

[Dispatch help article](https://support.claude.com/en/articles/13947068). Dispatch requires a Pro or Max plan and is not available on Team or Enterprise plans. Dispatch is one of several ways to work with Claude when you’re away from your terminal. See

[[Platforms and integrations - Claude Code Docs#Work when you are away from your terminal|Platforms and integrations]]to compare it with Remote Control, Channels, Slack, and scheduled tasks.

## Extend Claude Code

Connect external services, add reusable workflows, customize Claude’s behavior, and configure preview servers.

### Connect external tools

For local and

[[Use Claude Code Desktop - Claude Code Docs#SSH sessions|SSH]]sessions, click the + button next to the prompt box and select Connectors to add integrations like Google Calendar, Slack, GitHub, Linear, Notion, and more. You can add connectors before or during a session. The + button is not available in remote sessions, but

[[Automate work with routines - Claude Code Docs|routines]]configure connectors at routine creation time. To manage or disconnect connectors, go to Settings → Connectors in the desktop app, or select Manage connectors from the Connectors menu in the prompt box. Once connected, Claude can read your calendar, send messages, create issues, and interact with your tools directly. You can ask Claude what connectors are configured in your session. Connectors are

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP servers]]with a graphical setup flow. Use them for quick integration with supported services. For integrations not listed in Connectors, add MCP servers manually via

[[Connect Claude Code to tools via MCP - Claude Code Docs#Installing MCP servers|settings files]]. You can also

[create custom connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Use skills

[[Extend Claude with skills - Claude Code Docs|Skills]]extend what Claude can do. Claude loads them automatically when relevant, or you can invoke one directly: type

```
/
```

in the prompt box or click the + button and select Slash commands to browse what’s available. This includes

[[Commands - Claude Code Docs|built-in commands]], your

[[Extend Claude with skills - Claude Code Docs#Create your first skill|custom skills]], project skills from your codebase, and skills from any

[[Create plugins - Claude Code Docs|installed plugins]]. Select one and it appears highlighted in the input field. Type your task after it and send as usual.

### Install plugins

[[Create plugins - Claude Code Docs|Plugins]]are reusable packages that add skills, agents, hooks, MCP servers, and LSP configurations to Claude Code. You can install plugins from the desktop app without using the terminal. For local and

[[Use Claude Code Desktop - Claude Code Docs#SSH sessions|SSH]]sessions, click the + button next to the prompt box and select Plugins to see your installed plugins and their skills. To add a plugin, select Add plugin from the submenu to open the plugin browser, which shows available plugins from your configured

[[Create and distribute a plugin marketplace - Claude Code Docs|marketplaces]]including the official Anthropic marketplace. Select Manage plugins to enable, disable, or uninstall plugins. Plugins can be scoped to your user account, a specific project, or local-only. If your organization manages plugins centrally, those plugins are available in desktop sessions the same way they are in the CLI. Plugins are not available for remote sessions. For the full plugin reference including creating your own plugins, see

[[Create plugins - Claude Code Docs|plugins]].

### Configure preview servers

Claude automatically detects your dev server setup and stores the configuration in

```
.claude/launch.json
```

at the root of the folder you selected when starting the session. Preview uses this folder as its working directory, so if you selected a parent folder, subfolders with their own dev servers won’t be detected automatically. To work with a subfolder’s server, either start a session in that folder directly or add a configuration manually.
To customize how your server starts, for example to use

```
yarn dev
```

instead of

```
npm run dev
```

or to change the port, edit the file manually or click Edit configuration in the Preview dropdown to open it in your code editor. The file supports JSON with comments.

[[Use Claude Code Desktop - Claude Code Docs#Examples|examples]]below.

#### Auto-verify changes

When

```
autoVerify
```

is enabled, Claude automatically verifies code changes after editing files. It takes screenshots, checks for errors, and confirms changes work before completing its response.
Auto-verify is on by default. Disable it per-project by adding

```
"autoVerify": false
```

to

```
.claude/launch.json
```

, or toggle it from the Preview dropdown menu.

#### Configuration fields

Each entry in the

```
configurations
```

array accepts the following fields:

FieldTypeDescription

```
name
```

stringA unique identifier for this server

```
runtimeExecutable
```

stringThe command to run, such as

```
npm
```

,

```
yarn
```

, or

```
node
```

```
runtimeArgs
```

string[]Arguments passed to

```
runtimeExecutable
```

, such as

```
["run", "dev"]
```

```
port
```

numberThe port your server listens on. Defaults to 3000

```
cwd
```

stringWorking directory relative to your project root. Defaults to the project root. Use

```
${workspaceFolder}
```

to reference the project root explicitly

```
env
```

objectAdditional environment variables as key-value pairs, such as

```
{ "NODE_ENV": "development" }
```

. Don’t put secrets here since this file is committed to your repo. To pass secrets to your dev server, set them in the

```
autoPort
```

booleanHow to handle port conflicts. See below

```
program
```

stringA script to run with

```
node
```

. See

```
program
```

vs

```
runtimeExecutable
```

```
args
```

string[]Arguments passed to

```
program
```

. Only used when

```
program
```

is set

##### When to use ``` program ``` vs ``` runtimeExecutable ```

Use

```
runtimeExecutable
```

with

```
runtimeArgs
```

to start a dev server through a package manager. For example,

```
"runtimeExecutable": "npm"
```

with

```
"runtimeArgs": ["run", "dev"]
```

runs

```
npm run dev
```

.
Use

```
program
```

when you have a standalone script you want to run with

```
node
```

directly. For example,

```
"program": "server.js"
```

runs

```
node server.js
```

. Pass additional flags with

```
args
```

.

#### Port conflicts

The

```
autoPort
```

field controls what happens when your preferred port is already in use:

- ```
  true
  ```

  : Claude finds and uses a free port automatically. Suitable for most dev servers.
- ```
  false
  ```

  : Claude fails with an error. Use this when your server must use a specific port, such as for OAuth callbacks or CORS allowlists.
- Not set (default): Claude asks whether the server needs that exact port, then saves your answer.

```
PORT
```

environment variable.

#### Examples

These configurations show common setups for different project types:

- Next.js
- Multiple servers
- Node.js script

This configuration runs a Next.js app using Yarn on port 3000:

## Environment configuration

The environment you pick when

[[Use Claude Code Desktop - Claude Code Docs#Start a session|starting a session]]determines where Claude executes and how you connect:

- Local: runs on your machine with direct access to your files
- Remote: runs on Anthropic’s cloud infrastructure. Sessions continue even if you close the app.
- SSH: runs on a remote machine you connect to over SSH, such as your own servers, cloud VMs, or dev containers

### Local sessions

The desktop app does not always inherit your full shell environment. On macOS, when you launch the app from the Dock or Finder, it reads your shell profile, such as

```
~/.zshrc
```

or

```
~/.bashrc
```

, to extract

```
PATH
```

and a fixed set of Claude Code variables, but other variables you export there are not picked up. On Windows, the app inherits user and system environment variables but does not read PowerShell profiles.
To set environment variables for local sessions and dev servers on any platform, open the environment dropdown in the prompt box, hover over Local, and click the gear icon to open the local environment editor. Variables you save here are stored encrypted on your machine and apply to every local session and preview server you start. You can also add variables to the

```
env
```

key in your

```
~/.claude/settings.json
```

file, though these reach Claude sessions only and not dev servers. See

[[Environment variables - Claude Code Docs|environment variables]]for the full list of supported variables.

[[Common workflows - Claude Code Docs#Use extended thinking (thinking mode)|Extended thinking]]is enabled by default, which improves performance on complex reasoning tasks but uses additional tokens. To disable thinking entirely, set

```
MAX_THINKING_TOKENS
```

to

```
0
```

in the local environment editor. On models with

[[Model configuration - Claude Code Docs#Adjust effort level|adaptive reasoning]], any other

```
MAX_THINKING_TOKENS
```

value is ignored because adaptive reasoning controls thinking depth instead. On Opus 4.6 and Sonnet 4.6, set

```
CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING
```

to

```
1
```

to use a fixed thinking budget; Opus 4.7 always uses adaptive reasoning and has no fixed-budget mode.

### Remote sessions

Remote sessions continue in the background even if you close the app. Usage counts toward your

[[Manage costs effectively - Claude Code Docs|subscription plan limits]]with no separate compute charges. You can create custom cloud environments with different network access levels and environment variables. Select the environment dropdown when starting a remote session and choose Add environment. See

[[Use Claude Code on the web - Claude Code Docs#The cloud environment|the cloud environment]]for details on configuring network access and environment variables.

### SSH sessions

SSH sessions let you run Claude Code on a remote machine while using the desktop app as your interface. This is useful for working with codebases that live on cloud VMs, dev containers, or servers with specific hardware or dependencies. To add an SSH connection, click the environment dropdown before starting a session and select + Add SSH connection. The dialog asks for:

- Name: a friendly label for this connection
- SSH Host:

  ```
  user@hostname
  ```

  or a host defined in

  ```
  ~/.ssh/config
  ```
- SSH Port: defaults to 22 if left empty, or uses the port from your SSH config
- Identity File: path to your private key, such as

  ```
  ~/.ssh/id_rsa
  ```

  . Leave empty to use the default key or your SSH config.

#### Pre-configure SSH connections for your team

Administrators can distribute SSH connections to team members by adding

```
sshConfigs
```

to a

[[Claude Code settings - Claude Code Docs#Settings precedence|managed settings]]file. Connections defined this way appear in each user’s environment dropdown automatically and are shown as managed, so users can select them but cannot edit or delete them in the app. The following example pre-configures a single connection that opens in

```
~/projects
```

on the remote host:

```
id
```

,

```
name
```

, and

```
sshHost
```

. The

```
sshPort
```

,

```
sshIdentityFile
```

, and

```
startDirectory
```

fields are optional. Users can also add

```
sshConfigs
```

to their own

```
~/.claude/settings.json
```

, which is where connections added through the dialog are stored.

## Enterprise configuration

Organizations on Team or Enterprise plans can manage desktop app behavior through admin console controls, managed settings files, and device management policies.

### Admin console controls

These settings are configured through the

[admin settings console](https://claude.ai/admin-settings/claude-code):

- Code in the desktop: control whether users in your organization can access Claude Code in the desktop app
- Code in the web: enable or disable [[Use Claude Code on the web - Claude Code Docs|web sessions]]for your organization
- Remote Control: enable or disable [[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]for your organization
- Disable Bypass permissions mode: prevent users in your organization from enabling bypass permissions mode

### Managed settings

Managed settings override project and user settings and apply when Desktop spawns CLI sessions. You can set these keys in your organization’s

[[Claude Code settings - Claude Code Docs#Settings precedence|managed settings]]file or push them remotely through the admin console.

KeyDescription

```
permissions.disableBypassPermissionsMode
```

set to

```
"disable"
```

to prevent users from enabling Bypass permissions mode.

```
disableAutoMode
```

set to

```
"disable"
```

to prevent users from enabling

```
permissions
```

.

```
autoMode
```

customize what the auto mode classifier trusts and blocks across your organization. See

```
sshConfigs
```

[[Use Claude Code Desktop - Claude Code Docs#Pre-configure SSH connections for your team|SSH connections]]that appear in the environment dropdown. Users cannot edit or delete managed connections.

```
permissions.disableBypassPermissionsMode
```

and

```
disableAutoMode
```

also work in user and project settings, but placing them in managed settings prevents users from overriding them.

```
autoMode
```

is read from user settings,

```
.claude/settings.local.json
```

, and managed settings, but not from the checked-in

```
.claude/settings.json
```

: a cloned repo cannot inject its own classifier rules. For the complete list of managed-only settings including

```
allowManagedPermissionRulesOnly
```

and

```
allowManagedHooksOnly
```

, see

[[Configure permissions - Claude Code Docs#Managed-only settings|managed-only settings]]. Remote managed settings uploaded through the admin console currently apply to CLI and IDE sessions only. For Desktop-specific restrictions, use the admin console controls above.

### Device management policies

IT teams can manage the desktop app through MDM on macOS or group policy on Windows. Available policies include enabling or disabling the Claude Code feature, controlling auto-updates, and setting a custom deployment URL.

- macOS: configure via

  ```
  com.anthropic.Claude
  ```

  preference domain using tools like Jamf or Kandji
- Windows: configure via registry at

  ```
  SOFTWARE\Policies\Claude
  ```

### Authentication and SSO

Enterprise organizations can require SSO for all users. See

[[Authentication - Claude Code Docs|authentication]]for plan-level details and

[Setting up SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso)for SAML and OIDC configuration.

### Data handling

Claude Code processes your code locally in local sessions or on Anthropic’s cloud infrastructure in remote sessions. Conversations and code context are sent to Anthropic’s API for processing. See

[[Data usage - Claude Code Docs|data handling]]for details on data retention, privacy, and compliance.

### Deployment

Desktop can be distributed through enterprise deployment tools:

- macOS: distribute via MDM such as Jamf or Kandji using the

  ```
  .dmg
  ```

  installer
- Windows: deploy via MSIX package or

  ```
  .exe
  ```

  installer. See[Deploy Claude Desktop for Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows)for enterprise deployment options including silent installation

[[Enterprise network configuration - Claude Code Docs|network configuration]]. For the full enterprise configuration reference, see the

[enterprise configuration guide](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Coming from the CLI?

If you already use the Claude Code CLI, Desktop runs the same underlying engine with a graphical interface. You can run both simultaneously on the same machine, even on the same project. Each maintains separate session history, but they share configuration and project memory via CLAUDE.md files. To move a CLI session into Desktop, run

```
/desktop
```

in the terminal. Claude saves your session and opens it in the desktop app, then exits the CLI. This command is available on macOS and Windows only.

### CLI flag equivalents

This table shows the desktop app equivalent for common CLI flags. Flags not listed have no desktop equivalent because they are designed for scripting or automation.

CLIDesktop equivalent

```
--model sonnet
```

Model dropdown next to the send button

```
--resume
```

,

```
--continue
```

Click a session in the sidebar

```
--permission-mode
```

Mode selector next to the send button

```
--dangerously-skip-permissions
```

Bypass permissions mode. Enable in Settings → Claude Code → “Allow bypass permissions mode”. Enterprise admins can disable this setting.

```
--add-dir
```

Add multiple repos with the + button in remote sessions

```
--allowedTools
```

,

```
--disallowedTools
```

Not available in Desktop

```
--verbose
```

```
--print
```

,

```
--output-format
```

```
ANTHROPIC_MODEL
```

env var

```
MAX_THINKING_TOKENS
```

env var[[Use Claude Code Desktop - Claude Code Docs#Environment configuration|environment configuration]].

### Shared configuration

Desktop and CLI read the same configuration files, so your setup carries over:

- [[How Claude remembers your project - Claude Code Docs|CLAUDE.md]]and

  ```
  CLAUDE.local.md
  ```

  files in your project are used by both
- [[Connect Claude Code to tools via MCP - Claude Code Docs|MCP servers]]configured in

  ```
  ~/.claude.json
  ```

  or

  ```
  .mcp.json
  ```

  work in both
- [[Hooks reference - Claude Code Docs|Hooks]]and[[Extend Claude with skills - Claude Code Docs|skills]]defined in settings apply to both
- [[Claude Code settings - Claude Code Docs|Settings]]in

  ```
  ~/.claude.json
  ```

  and

  ```
  ~/.claude/settings.json
  ```

  are shared. Permission rules, allowed tools, and other settings in

  ```
  settings.json
  ```

  apply to Desktop sessions.
- Models: Sonnet, Opus, and Haiku are available in both. In Desktop, select the model from the dropdown next to the send button. You can change the model mid-session from the same dropdown.

MCP servers: desktop chat app vs Claude Code: MCP servers configured for the Claude Desktop chat app in

```
claude_desktop_config.json
```

are separate from Claude Code and will not appear in the Code tab. To use MCP servers in Claude Code, configure them in

```
~/.claude.json
```

or your project’s

```
.mcp.json
```

file. See [[Connect Claude Code to tools via MCP - Claude Code Docs#Installing MCP servers|MCP configuration]]for details.

### Feature comparison

This table compares core capabilities between the CLI and Desktop. For a full list of CLI flags, see the

[[CLI reference - Claude Code Docs|CLI reference]].

FeatureCLIDesktopPermission modesAll modes including

```
dontAsk
```

Ask permissions, Auto accept edits, Plan mode, Auto, and Bypass permissions via Settings

```
--dangerously-skip-permissions
```

CLI flagBypass permissions mode. Enable in Settings → Claude Code → “Allow bypass permissions mode”

[enterprise configuration guide](https://support.claude.com/en/articles/12622667-enterprise-configuration).[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP servers]][[Create plugins - Claude Code Docs|Plugins]]

```
/plugin
```

command[[CLI reference - Claude Code Docs|flag]]

```
--worktree
```

[[Schedule recurring tasks in Claude Code Desktop - Claude Code Docs|Scheduled tasks]][[Let Claude use your computer from the CLI - Claude Code Docs|Enable via]]on macOS

```
/mcp
```

[[Use Claude Code Desktop - Claude Code Docs#Let Claude use your computer|App and screen control]]on macOS and Windows[[Use Claude Code Desktop - Claude Code Docs#Sessions from Dispatch|Dispatch sessions]]in the sidebar[[CLI reference - Claude Code Docs|,]]

```
--print
```

[[Run Claude Code programmatically - Claude Code Docs|Agent SDK]]

### What’s not available in Desktop

The following features are only available in the CLI or VS Code extension:

- Third-party providers: Desktop connects to Anthropic’s API by default. Enterprise deployments can configure Vertex AI and gateway providers via [managed settings](https://support.claude.com/en/articles/12622667-enterprise-configuration). For Bedrock or Foundry, use the[[Quickstart - Claude Code Docs|CLI]].
- Linux: the desktop app is available on macOS and Windows only.
- Inline code suggestions: Desktop does not provide autocomplete-style suggestions. It works through conversational prompts and explicit code changes.
- Agent teams: multi-agent orchestration is available via the [[Orchestrate teams of Claude Code sessions - Claude Code Docs|CLI]]and[[Run Claude Code programmatically - Claude Code Docs|Agent SDK]], not in Desktop.

## Troubleshooting

The sections below cover issues specific to the desktop app. For runtime API errors that appear in the chat such as

```
API Error: 500
```

,

```
529 Overloaded
```

,

```
429
```

, or

```
Prompt is too long
```

, see the

[[Error reference - Claude Code Docs|Error reference]]. Those errors and their fixes are the same across the CLI, desktop, and web.

### Check your version

To see which version of the desktop app you’re running:

- macOS: click Claude in the menu bar, then About Claude
- Windows: click Help, then About

### 403 or authentication errors in the Code tab

If you see

```
Error 403: Forbidden
```

or other authentication failures when using the Code tab:

- Sign out and back in from the app menu. This is the most common fix.
- Verify you have an active paid subscription: Pro, Max, Team, or Enterprise.
- If the CLI works but Desktop does not, quit the desktop app completely, not just close the window, then reopen and sign in again.
- Check your internet connection and proxy settings.

### Blank or stuck screen on launch

If the app opens but shows a blank or unresponsive screen:

- Restart the app.
- Check for pending updates. The app auto-updates on launch.
- On Windows, check Event Viewer for crash logs under Windows Logs → Application.

### ”Failed to load session”

If you see

```
Failed to load session
```

, the selected folder may no longer exist, a Git repository may require Git LFS that isn’t installed, or file permissions may prevent access. Try selecting a different folder or restarting the app.

### Session not finding installed tools

If Claude can’t find tools like

```
npm
```

,

```
node
```

, or other CLI commands, verify the tools work in your regular terminal, check that your shell profile properly sets up PATH, and restart the desktop app to reload environment variables.

### Git and Git LFS errors

On Windows, Git is required for the Code tab to start local sessions. If you see “Git is required,” install

[Git for Windows](https://git-scm.com/downloads/win)and restart the app. If you see “Git LFS is required by this repository but is not installed,” install Git LFS from

[git-lfs.com](https://git-lfs.com/), run

```
git lfs install
```

, and restart the app.

### MCP servers not working on Windows

If MCP server toggles don’t respond or servers fail to connect on Windows, check that the server is properly configured in your settings, restart the app, verify the server process is running in Task Manager, and review server logs for connection errors.

### App won’t quit

- macOS: press Cmd+Q. If the app doesn’t respond, use Force Quit with Cmd+Option+Esc, select Claude, and click Force Quit.
- Windows: use Task Manager with Ctrl+Shift+Esc to end the Claude process.

### Windows-specific issues

- PATH not updated after install: open a new terminal window. PATH updates only apply to new terminal sessions.
- Concurrent installation error: if you see an error about another installation in progress but there isn’t one, try running the installer as Administrator.

### ”Branch doesn’t exist yet” when opening in CLI

Remote sessions can create branches that don’t exist on your local machine. Click the branch name in the session toolbar to copy it, then fetch it locally:

### Still stuck?

- Search or file a bug on [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- Visit the [Claude support center](https://support.claude.com/)

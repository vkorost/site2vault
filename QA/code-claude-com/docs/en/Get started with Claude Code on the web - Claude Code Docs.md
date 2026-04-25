---
title: Get started with Claude Code on the web - Claude Code Docs
source_url: https://code.claude.com/docs/en/web-quickstart
description: Run Claude Code in the cloud from your browser or phone. Connect a GitHub
  repository, submit a task, and review the PR without local setup.
---

Claude Code on the web is in research preview for Pro, Max, and Team users, and for Enterprise users with premium seats or Chat + Claude Code seats.

[claude.ai/code](https://claude.ai/code)in your browser or the Claude mobile app. You’ll need a GitHub repository to

[[Get started with Claude Code on the web - Claude Code Docs#Connect GitHub and create an environment|get started]]. Claude clones it into an isolated virtual machine, makes changes, and pushes a branch for you to review. Sessions persist across devices, so a task you start on your laptop is ready to review from your phone later. Claude Code on the web works well for:

- Parallel tasks: run several independent tasks at once, each in its own session and branch, without managing multiple worktrees
- Repos you don’t have locally: Claude clones the repo fresh every session, so you don’t need it checked out
- Tasks that don’t need frequent steering: submit a well-defined task, do something else, and review the result when Claude is done
- Code questions and exploration: understand a codebase or trace how a feature is implemented without a local checkout

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]is a better fit.

## How sessions run

When you submit a task:

- Clone and prepare: your repository is cloned to an Anthropic-managed VM, and your [[Use Claude Code on the web - Claude Code Docs#Setup scripts|setup script]]runs if configured.
- Configure network: internet access is set based on your environment’s [[Use Claude Code on the web - Claude Code Docs#Access levels|access level]].
- Work: Claude analyzes code, makes changes, runs tests, and checks its work. You can watch and steer throughout, or step away and come back when it’s done.
- Push the branch: when Claude reaches a stopping point, it pushes its branch to GitHub. You review the diff, leave inline comments, create a PR, or send another message to keep going.

## Compare ways to run Claude Code

Claude Code behaves the same everywhere. What changes is where code executes and whether your local config is available. The Desktop app offers both local and cloud sessions, so its answers below depend on which you choose:

On the webRemote ControlTerminal CLIDesktop appCode runs onAnthropic cloud VMYour machineYour machineYour machine or cloud VMYou chat fromclaude.ai or mobile appclaude.ai or mobile appYour terminalThe Desktop UIUses your local configNo, repo onlyYesYesYes for local, no for cloudRequires GitHubYes, or

```
--remote
```

[[Choose a permission mode - Claude Code Docs|Permission modes]]

[[Quickstart - Claude Code Docs|terminal quickstart]],

[[Use Claude Code Desktop - Claude Code Docs|Desktop app]], or

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]docs to set those up.

## Connect GitHub and create an environment

Setup is a one-time process. If you already use the GitHub CLI, you can

[[Get started with Claude Code on the web - Claude Code Docs#Connect from your terminal|do this from your terminal]]instead of the browser.

Visit claude.ai/code

Go to

[claude.ai/code](https://claude.ai/code)and sign in with your Anthropic account.

Install the Claude GitHub App

After signing in, claude.ai/code prompts you to connect GitHub. Follow the prompt to install the Claude GitHub App and grant it access to your repositories. Cloud sessions work with existing GitHub repositories, so to start a new project,

[create an empty repository on GitHub](https://github.com/new)first.

Create your environment

After connecting GitHub, you’ll be prompted to create a cloud environment. The environment controls what network access Claude has during sessions and what runs when a new session is created. See

[[Use Claude Code on the web - Claude Code Docs#Installed tools|Installed tools]]for what’s available without any configuration.The form has these fields:

- Name: a display label. Useful when you have multiple environments for different projects or access levels.
- Network access: controls what the session can reach on the internet. The default,

  ```
  Trusted
  ```

  , allows connections to[[Use Claude Code on the web - Claude Code Docs#Default allowed domains|common package registries]]like npm, PyPI, and RubyGems while blocking general internet access.
- Environment variables: optional variables available in every session, in

  ```
  .env
  ```

  format. Don’t wrap values in quotes, since quotes are stored as part of the value. These are visible to anyone who can edit this environment.
- Setup script: an optional Bash script that runs before Claude Code launches. Use it to install system tools the cloud VM doesn’t include, like

  ```
  apt install -y gh
  ```

  . The result is[[Use Claude Code on the web - Claude Code Docs#Environment caching|cached]], so the script doesn’t re-run on every session. See[[Use Claude Code on the web - Claude Code Docs#Setup scripts|Setup scripts]]for examples and debugging tips.

[[Use Claude Code on the web - Claude Code Docs#Configure your environment|edit it later or create additional environments]]for different projects.

### Connect from your terminal

If you already use the GitHub CLI (

```
gh
```

), you can set up Claude Code on the web without opening a browser. This requires the

[[Quickstart - Claude Code Docs|Claude Code CLI]].

```
/web-setup
```

reads your local

```
gh
```

token, links it to your Claude account, and creates a default cloud environment if you don’t have one.

Organizations with

[[Zero data retention - Claude Code Docs|Zero Data Retention]]enabled cannot use

```
/web-setup
```

or other cloud session features. If the GitHub CLI isn’t installed or authenticated,

```
/web-setup
```

opens the browser onboarding flow instead.

Sign in to Claude

In the Claude Code CLI, run

```
/login
```

to sign in with your claude.ai account. Skip this step if you’re already signed in.

Run /web-setup

In the Claude Code CLI, run:This syncs your

```
gh
```

token to your Claude account. If you don’t have a cloud environment yet,

```
/web-setup
```

creates one with Trusted network access and no setup script. You can [[Use Claude Code on the web - Claude Code Docs#Configure your environment|edit the environment or add variables]]afterward. Once

```
/web-setup
```

completes, you can start cloud sessions from your terminal with [[Use Claude Code on the web - Claude Code Docs#From terminal to web|or set up recurring tasks with]]

```
--remote
```

[[Automate work with routines - Claude Code Docs|.]]

```
/schedule
```

## Start a task

With GitHub connected and an environment created, you’re ready to submit tasks.

Select a repository and branch

From

[claude.ai/code](https://claude.ai/code)or the Code tab in the Claude mobile app, click the repository selector below the input box and choose a repository for Claude to work in. Each repository shows a branch selector. Change it to start Claude from a feature branch instead of the default. You can add multiple repositories to work across them in one session.

Choose a permission mode

The mode dropdown next to the input defaults to Auto accept edits, where Claude makes changes and pushes a branch without stopping for approval. Switch to Plan mode if you want Claude to propose an approach and wait for your go-ahead before editing files. Cloud sessions don’t offer Ask permissions, Auto mode, or Bypass permissions. See

[[Choose a permission mode - Claude Code Docs|Permission modes]]for the full list.

Describe the task and submit

Type a description of what you want and press Enter. Be specific:

- Name the file or function: “Add a README with setup instructions” or “Fix the failing auth test in

  ```
  tests/test_auth.py
  ```

  ” is better than “fix tests”
- Paste error output if you have it
- Describe the expected behavior, not just the symptom

## Pre-fill sessions

You can prefill the prompt, repositories, and environment for a new session by adding query parameters to the

[claude.ai/code](https://claude.ai/code)URL. Use this to build integrations such as a button in your issue tracker that opens Claude Code with the issue description as the prompt.

ParameterDescription

```
prompt
```

Prompt text to prefill in the input box. The alias

```
q
```

is also accepted.

```
prompt_url
```

URL to fetch the prompt text from, for prompts too long to embed in a query string. The URL must allow cross-origin requests. Ignored when

```
prompt
```

is also set.

```
repositories
```

Comma-separated list of

```
owner/repo
```

slugs to preselect. The alias

```
repo
```

is also accepted.

```
environment
```

Name or ID of the

## Review and iterate

When Claude finishes, review the changes, leave feedback on specific lines, and keep going until the diff looks right.

Open the diff view

A diff indicator shows lines added and removed across the session, for example

```
+42 -18
```

. Select it to open the diff view, with a file list on the left and changes on the right.

Leave inline comments

Select any line in the diff, type your feedback, and press Enter. Comments queue up until you send your next message, then they’re bundled with it. Claude sees “at

```
src/auth.ts:47
```

, don’t catch the error here” alongside your main instruction, so you don’t have to describe where the problem is.

Create a pull request

When the diff looks right, select Create PR at the top of the diff view. You can open it as a full PR, a draft, or jump to GitHub’s compose page with a generated title and description.

Keep iterating after the PR

The session stays live after the PR is created. Paste CI failure output or reviewer comments into the chat and ask Claude to address them. To have Claude monitor the PR automatically, see

[[Use Claude Code on the web - Claude Code Docs#Auto-fix pull requests|Auto-fix pull requests]].

## Troubleshoot setup

### No repositories appear after connecting GitHub

The Claude GitHub App needs explicit access to each repository you want to use. On github.com, open Settings → Applications → Claude → Configure and verify your repo is listed under Repository access. Private repositories need the same authorization as public ones.

### The page only shows a GitHub login button

Cloud sessions require a connected GitHub account. Connect via the browser flow above, or run

```
/web-setup
```

from your terminal if you use the GitHub CLI. If you’d rather not connect GitHub at all, see

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]to run Claude Code on your own machine and monitor it from the web.

### ”Not available for the selected organization”

Enterprise organizations may need an admin to enable Claude Code on the web. Contact your Anthropic account team.

### ``` /web-setup ``` returns “Unknown command”

```
/web-setup
```

runs inside the Claude Code CLI, not your shell. Launch

```
claude
```

first, then type

```
/web-setup
```

at the prompt.
If you typed it inside Claude Code and still see the error, your CLI is older than v2.1.80 or you’re authenticated with an API key or third-party provider instead of a claude.ai subscription. Run

```
claude update
```

, then

```
/login
```

to sign in with your claude.ai account.

### ”Could not create a cloud environment” or “No cloud environment available” when using ``` --remote ``` or ultraplan

Remote-session features create a default cloud environment automatically if you don’t have one. If you see “Could not create a cloud environment”, automatic creation failed. If you see “No cloud environment available”, your CLI predates automatic creation. In either case, run

```
/web-setup
```

in the Claude Code CLI to create one manually, or visit

[claude.ai/code](https://claude.ai/code)and follow the Create your environment step above.

### Setup script failed

The setup script exited with a non-zero status, which blocks the session from starting. Common causes:

- A package install failed because the registry isn’t in your [[Use Claude Code on the web - Claude Code Docs#Access levels|network access level]].

  ```
  Trusted
  ```

  covers most package managers;

  ```
  None
  ```

  blocks them all.
- The script references a file or path that doesn’t exist in a fresh clone.
- A command that works locally needs a different invocation on Ubuntu.

```
set -x
```

at the top of the script to see which command failed. For non-critical commands, append

```
|| true
```

so they don’t block session start.

### Session keeps running after closing the tab

This is by design. Closing the tab or navigating away doesn’t stop the session. It continues running in the background until Claude finishes the current task, then idles. From the sidebar, you can

[[Use Claude Code on the web - Claude Code Docs#Archive sessions|archive a session]]to hide it from your list, or

[[Use Claude Code on the web - Claude Code Docs#Delete sessions|delete it]]to remove it permanently.

## Next steps

Now that you can submit and review tasks, these pages cover what comes next: starting cloud sessions from your terminal, scheduling recurring work, and giving Claude standing instructions.

- [[Use Claude Code on the web - Claude Code Docs|Use Claude Code on the web]]: the full reference, including teleporting sessions to your terminal, setup scripts, environment variables, and network config
- [[Automate work with routines - Claude Code Docs|Routines]]: automate work on a schedule, via API call, or in response to GitHub events
- [[How Claude remembers your project - Claude Code Docs|CLAUDE.md]]: give Claude persistent instructions and context that load at the start of every session
- Install the Claude mobile app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684)or[Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)to monitor sessions from your phone. From the Claude Code CLI,

  ```
  /mobile
  ```

  shows a QR code.

---
title: Terminal guide for new users - Claude Code Docs
source_url: https://code.claude.com/docs/en/terminal-guide
description: A step-by-step guide to installing Claude Code for first-time terminal
  users on macOS and Windows.
---

Don’t want to use the terminal? The Claude Code desktop app lets you skip the terminal entirely. Download it for

[macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs)or[Windows](https://claude.com/download?utm_source=claude_code&utm_medium=docs), then see the[[Get started with the desktop app - Claude Code Docs|Desktop quickstart]]to get started.

## macOS and Linux

Follow these steps to install and start Claude Code from a macOS or Linux terminal. Claude Code requires macOS 13.0 or later. See the

[[Advanced setup - Claude Code Docs#System requirements|system requirements]]for supported Linux distributions.

Open a terminal

macOS: Press

```
Cmd + Space
```

to open Spotlight Search, type

```
Terminal
```

, and press

```
Enter
```

.Linux: Open your terminal app. On most distributions, press

```
Ctrl + Alt + T
```

or search for “Terminal” in your application menu.A window will appear with a blinking cursor. This is your terminal, where you type commands.

Install Claude Code

Copy this line, paste it into your terminal (This downloads and runs the Claude Code installer from claude.ai. You’ll see text scrolling as it works. When it’s done, you’ll see “Claude Code successfully installed!” If you see an error instead, check the

```
Cmd + V
```

on macOS,

```
Ctrl + Shift + V
```

on Linux), and press

```
Enter
```

:[[Terminal guide for new users - Claude Code Docs#macOS and Linux troubleshooting|troubleshooting section]]below.

Start Claude Code

Type You’ll be prompted to

```
claude
```

and press

```
Enter
```

:[[Authentication - Claude Code Docs|log in]]with your Claude account. Follow the on-screen instructions. A browser window will open for you to sign in.

Start using Claude Code

Once logged in, you can start asking Claude questions about your code or anything else. Claude Code runs entirely in text. You type messages and press

```
Enter
```

to send them. A few things to know:

- You can’t click on things in the terminal. Use the arrow keys to move around.
- Press

  ```
  Esc
  ```

  to interrupt Claude if it’s running.
- Type

  ```
  exit
  ```

  or press

  ```
  Ctrl + D
  ```

  to leave Claude Code.
- Type

  ```
  /help
  ```

  to see available commands.

## Windows

Follow these steps to install Git, set up PowerShell, and start Claude Code on Windows. Claude Code requires Windows 10 version 1809 or later. See the

[[Advanced setup - Claude Code Docs#System requirements|system requirements]]for full details.

Install Git for Windows

Git is a tool that Claude Code uses internally to track changes to your code. You won’t need to learn Git yourself.If you don’t already have it:

- Go to [git-scm.com/downloads/win](https://git-scm.com/downloads/win)and download the installer
- Run the installer. Click Next on each screen to accept the defaults. The installer has many screens, but you don’t need to change anything.
- If it asks you to choose an editor, keep the default and click Next.
- When you see “Adjusting your PATH environment,” keep the recommended option selected.

Already have Git? You can skip this step. If you’re not sure, install it anyway. Reinstalling won’t cause problems.

Open PowerShell

PowerShell is Windows’ built-in terminal for typing commands. It comes pre-installed on every Windows computer.Press

```
Win + X
```

and select Windows PowerShell (or Terminal) from the menu. A window with a blinking cursor will appear. This is where you’ll type commands.

Windows has two command-line programs: PowerShell and CMD. They look similar but use different commands. Make sure you’re in PowerShell for the next step.How to tell which one you’re in:

- PowerShell: shows

  ```
  PS C:\Users\YourName>
  ```

  at the start of each line
- CMD: shows

  ```
  C:\Users\YourName>
  ```

  without the

  ```
  PS
  ```

Install Claude Code

Copy this line, paste it into PowerShell with This downloads and runs the Claude Code installer.

```
Ctrl + V
```

or right-click, and press

```
Enter
```

:

```
irm
```

fetches the file and

```
iex
```

runs it. You’ll see text scrolling as it works. When it’s done, you’ll see “Claude Code successfully installed!” If you see an error instead, check the [[Terminal guide for new users - Claude Code Docs#Windows troubleshooting|troubleshooting section]]below.

If you’re in CMD instead of PowerShell, use this command:

Start Claude Code

Close PowerShell and open a new PowerShell window so it recognizes the newly installed You’ll be prompted to

```
claude
```

command. Then type:[[Authentication - Claude Code Docs|log in]]with your Claude account. Follow the on-screen instructions. A browser window will open for you to sign in.

Start using Claude Code

Once logged in, you can start asking Claude questions about your code or anything else. Claude Code runs entirely in text. You type messages and press

```
Enter
```

to send them. A few things to know:

- You can’t click on things in the terminal. Use the arrow keys to move around.
- Press

  ```
  Esc
  ```

  to interrupt Claude if it’s running.
- Type

  ```
  exit
  ```

  or press

  ```
  Ctrl + D
  ```

  to leave Claude Code.
- Type

  ```
  /help
  ```

  to see available commands.

## What’s next?

Once you see the Claude Code welcome screen, you’re ready to go. You don’t need to know how to code. Describe what you want in plain English, and Claude writes the code for you.

### Build something

Claude can create projects from a description:

### Work with files on your computer

Claude can read and organize files you already have:

### Ask questions

Claude can explain things, help you learn, or plan out a project:

### Other ways to use Claude Code

You don’t have to use the terminal. Claude Code is also available in:

- [[Use Claude Code in VS Code - Claude Code Docs|VS Code]]and[[JetBrains IDEs - Claude Code Docs|JetBrains IDEs]]as editor extensions
- The [[Get started with the desktop app - Claude Code Docs|desktop app]], with no terminal required
- The [[Use Claude Code on the web - Claude Code Docs|web]]at claude.ai/code for remote sessions
- [[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]]and[[Claude Code GitLab CICD - Claude Code Docs|GitLab CI/CD]]for automation

### Learn more

- [[Quickstart - Claude Code Docs|Quickstart]]: a guided walkthrough of your first project with Claude Code
- [[How Claude Code works - Claude Code Docs|How Claude Code works]]: understand how Claude reads your files, runs commands, and makes edits
- [[Best Practices for Claude Code - Claude Code Docs|Best practices]]: get better results with effective prompting and project setup
- [[Common workflows - Claude Code Docs|Common workflows]]: step-by-step guides for debugging, testing, refactoring, and more
- [[Configure your terminal for Claude Code - Claude Code Docs|Terminal configuration]]: customize your terminal for the best Claude Code experience

## Troubleshooting

### macOS and Linux troubleshooting

If you run into problems installing on macOS or Linux, check these common issues:

###

'command not found: claude'

'command not found: claude'

If you see Then try

```
command not found: claude
```

after installing, your terminal needs to reload its settings. Close the Terminal window and open a new one, then try

```
claude
```

again.If it still doesn’t work, add the install directory to your PATH. Run the command for your shell:

```
claude
```

again. For more details, see [[Troubleshooting - Claude Code Docs#Verify your PATH|fix your PATH]].

###

Error with HTML code or 'syntax error near unexpected token'

Error with HTML code or 'syntax error near unexpected token'

If you see

```
bash: line 1: syntax error near unexpected token '<'
```

or HTML code like

```
<!DOCTYPE html>
```

in your terminal, the install URL returned a web page instead of the installer script.If the page says “App unavailable in region,” Claude Code is not available in your country. See [supported countries](https://www.anthropic.com/supported-countries).Otherwise, try running the command again. If it keeps happening, install with[Homebrew](https://brew.sh)instead:

###

'dyld' error or 'built for Mac OS X 13.0'

'dyld' error or 'built for Mac OS X 13.0'

If you see

```
dyld: cannot load
```

,

```
dyld: Symbol not found
```

, or

```
built for Mac OS X 13.0
```

, your macOS version is likely older than Claude Code supports.Open the Apple menu and select About This Mac to check your version. If it’s older than 13.0, update macOS through Software Update. See the [[Troubleshooting - Claude Code Docs|macOS troubleshooting guide]]for more details.

[[Troubleshooting - Claude Code Docs#Troubleshoot installation issues|installation troubleshooting guide]].

### Windows troubleshooting

If you run into problems installing on Windows, check these common issues:

###

'irm is not recognized'

'irm is not recognized'

You’re in CMD, not PowerShell. Close this window and open PowerShell instead (

```
Win + X
```

then select Windows PowerShell).Alternatively, use the CMD install command:

###

SSL/TLS error or 'Could not create SSL/TLS secure channel'

SSL/TLS error or 'Could not create SSL/TLS secure channel'

This usually happens on older Windows 10 systems. Run this line first, then retry the install:

###

'Claude Code on Windows requires git-bash'

'Claude Code on Windows requires git-bash'

Git for Windows isn’t installed or Claude Code can’t find it.

- If you haven’t installed Git yet, go back to the [[Terminal guide for new users - Claude Code Docs#Windows|first step in the Windows section]].
- If Git is installed but Claude Code can’t find it, tell it where to look:
  Then run

  ```
  claude
  ```

  again. If your Git is installed somewhere else, find the path by running:Look for the

  ```
  Git\bin
  ```

  folder in that path and use it instead.

[[Troubleshooting - Claude Code Docs#Windows: Claude Code on Windows requires git-bash|configure Git Bash path]].

###

'claude is not recognized'

'claude is not recognized'

Restart your computer and try again. This usually fixes the problem.If restarting didn’t help, run these commands to add Claude Code to your PATH:Close PowerShell, open a new window, and try

```
claude
```

again. See [[Troubleshooting - Claude Code Docs#Verify your PATH|verify your PATH]]for more details.

[[Troubleshooting - Claude Code Docs#Troubleshoot installation issues|installation troubleshooting guide]].

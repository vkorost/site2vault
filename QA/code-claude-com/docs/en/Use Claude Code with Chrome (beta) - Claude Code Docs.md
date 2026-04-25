---
title: Use Claude Code with Chrome (beta) - Claude Code Docs
source_url: https://code.claude.com/docs/en/chrome
description: Connect Claude Code to your Chrome browser to test web apps, debug with
  console logs, automate form filling, and extract data from web pages.
---

[[Use Claude Code in VS Code - Claude Code Docs#Automate browser tasks with Chrome|VS Code extension]]. Build your code, then test and debug in the browser without switching contexts. Claude opens new tabs for browser tasks and shares your browser’s login state, so it can access any site you’re already signed into. Browser actions run in a visible Chrome window in real time. When Claude encounters a login page or CAPTCHA, it pauses and asks you to handle it manually.

Chrome integration is in beta and currently works with Google Chrome and Microsoft Edge. It is not yet supported on Brave, Arc, or other Chromium-based browsers. WSL (Windows Subsystem for Linux) is also not supported.

## Capabilities

With Chrome connected, you can chain browser actions with coding tasks in a single workflow:

- Live debugging: read console errors and DOM state directly, then fix the code that caused them
- Design verification: build a UI from a Figma mock, then open it in the browser to verify it matches
- Web app testing: test form validation, check for visual regressions, or verify user flows
- Authenticated web apps: interact with Google Docs, Gmail, Notion, or any app you’re logged into without API connectors
- Data extraction: pull structured information from web pages and save it locally
- Task automation: automate repetitive browser tasks like data entry, form filling, or multi-site workflows
- Session recording: record browser interactions as GIFs to document or share what happened

## Prerequisites

Before using Claude Code with Chrome, you need:

- [Google Chrome](https://www.google.com/chrome/)or[Microsoft Edge](https://www.microsoft.com/edge)browser
- [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn)version 1.0.36 or higher, available in the Chrome Web Store for both browsers
- [[Quickstart - Claude Code Docs#Step 1: Install Claude Code|Claude Code]]version 2.0.73 or higher
- A direct Anthropic plan (Pro, Max, Team, or Enterprise)

Chrome integration is not available through third-party providers like Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry. If you access Claude exclusively through a third-party provider, you need a separate claude.ai account to use this feature.

## Get started in the CLI

Launch Claude Code with Chrome

Start Claude Code with the You can also enable Chrome from within an existing session by running

```
--chrome
```

flag:

```
/chrome
```

.

```
/chrome
```

at any time to check the connection status, manage permissions, or reconnect the extension.
For VS Code, see

[[Use Claude Code in VS Code - Claude Code Docs#Automate browser tasks with Chrome|browser automation in VS Code]].

### Enable Chrome by default

To avoid passing

```
--chrome
```

each session, run

```
/chrome
```

and select “Enabled by default”.
In the

[[Use Claude Code in VS Code - Claude Code Docs#Automate browser tasks with Chrome|VS Code extension]], Chrome is available whenever the Chrome extension is installed. No additional flag is needed.

Enabling Chrome by default in the CLI increases context usage since browser tools are always loaded. If you notice increased context consumption, disable this setting and use

```
--chrome
```

only when needed.

### Manage site permissions

Site-level permissions are inherited from the Chrome extension. Manage permissions in the Chrome extension settings to control which sites Claude can browse, click, and type on.

## Example workflows

These examples show common ways to combine browser actions with coding tasks. Run

```
/mcp
```

and select

```
claude-in-chrome
```

to see the full list of available browser tools.

### Test a local web application

When developing a web app, ask Claude to verify your changes work correctly:

### Debug with console logs

Claude can read console output to help diagnose problems. Tell Claude what patterns to look for rather than asking for all console output, since logs can be verbose:

### Automate form filling

Speed up repetitive data entry tasks:

### Draft content in Google Docs

Use Claude to write directly in your documents without API setup:

### Extract data from web pages

Pull structured information from websites:

### Run multi-site workflows

Coordinate tasks across multiple websites:

### Record a demo GIF

Create shareable recordings of browser interactions:

## Troubleshooting

### Extension not detected

If Claude Code shows “Chrome extension not detected”:

- Verify the Chrome extension is installed and enabled in

  ```
  chrome://extensions
  ```
- Verify Claude Code is up to date by running

  ```
  claude --version
  ```
- Check that Chrome is running
- Run

  ```
  /chrome
  ```

  and select “Reconnect extension” to re-establish the connection
- If the issue persists, restart both Claude Code and Chrome

- macOS:

  ```
  ~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json
  ```
- Linux:

  ```
  ~/.config/google-chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json
  ```
- Windows: check

  ```
  HKCU\Software\Google\Chrome\NativeMessagingHosts\
  ```

  in the Windows Registry

- macOS:

  ```
  ~/Library/Application Support/Microsoft Edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json
  ```
- Linux:

  ```
  ~/.config/microsoft-edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json
  ```
- Windows: check

  ```
  HKCU\Software\Microsoft\Edge\NativeMessagingHosts\
  ```

  in the Windows Registry

### Browser not responding

If Claude’s browser commands stop working:

- Check if a modal dialog (alert, confirm, prompt) is blocking the page. JavaScript dialogs block browser events and prevent Claude from receiving commands. Dismiss the dialog manually, then tell Claude to continue.
- Ask Claude to create a new tab and try again
- Restart the Chrome extension by disabling and re-enabling it in

  ```
  chrome://extensions
  ```

### Connection drops during long sessions

The Chrome extension’s service worker can go idle during extended sessions, which breaks the connection. If browser tools stop working after a period of inactivity, run

```
/chrome
```

and select “Reconnect extension”.

### Windows-specific issues

On Windows, you may encounter:

- Named pipe conflicts (EADDRINUSE): if another process is using the same named pipe, restart Claude Code. Close any other Claude Code sessions that might be using Chrome.
- Native messaging host errors: if the native messaging host crashes on startup, try reinstalling Claude Code to regenerate the host configuration.

### Common error messages

These are the most frequently encountered errors and how to resolve them:

ErrorCauseFix”Browser extension is not connected”Native messaging host cannot reach the extensionRestart Chrome and Claude Code, then run

```
/chrome
```

to reconnect”Extension not detected”Chrome extension is not installed or is disabledInstall or enable the extension in

```
chrome://extensions
```

”No tab available”Claude tried to act before a tab was readyAsk Claude to create a new tab and retry”Receiving end does not exist”Extension service worker went idleRun

```
/chrome
```

and select “Reconnect extension”

## See also

- [[Let Claude use your computer from the CLI - Claude Code Docs|Computer use]]: control native macOS apps when a task can’t be done in a browser
- [[Use Claude Code in VS Code - Claude Code Docs#Automate browser tasks with Chrome|Use Claude Code in VS Code]]: browser automation in the VS Code extension
- [[CLI reference - Claude Code Docs|CLI reference]]: command-line flags including

  ```
  --chrome
  ```
- [[Common workflows - Claude Code Docs|Common workflows]]: more ways to use Claude Code
- [[Data usage - Claude Code Docs|Data and privacy]]: how Claude Code handles your data
- [Getting started with Claude in Chrome](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome): full documentation for the Chrome extension, including shortcuts, scheduling, and permissions

---
title: JetBrains IDEs - Claude Code Docs
source_url: https://code.claude.com/docs/en/jetbrains
description: Use Claude Code with JetBrains IDEs including IntelliJ, PyCharm, WebStorm,
  and more
---

## Supported IDEs

The Claude Code plugin works with most JetBrains IDEs, including:

- IntelliJ IDEA
- PyCharm
- Android Studio
- WebStorm
- PhpStorm
- GoLand

## Features

- Quick launch: Use

  ```
  Cmd+Esc
  ```

  (Mac) or

  ```
  Ctrl+Esc
  ```

  (Windows/Linux) to open Claude Code directly from your editor, or click the Claude Code button in the UI
- Diff viewing: Code changes can be displayed directly in the IDE diff viewer instead of the terminal
- Selection context: The current selection/tab in the IDE is automatically shared with Claude Code
- File reference shortcuts: Use

  ```
  Cmd+Option+K
  ```

  (Mac) or

  ```
  Alt+Ctrl+K
  ```

  (Linux/Windows) to insert file references (for example, @File#L1-99)
- Diagnostic sharing: Diagnostic errors (lint, syntax, etc.) from the IDE are automatically shared with Claude as you work

## Installation

### Marketplace Installation

Find and install the

[Claude Code plugin](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)from the JetBrains marketplace and restart your IDE. If you haven’t installed Claude Code yet, see

[[Quickstart - Claude Code Docs|our quickstart guide]]for installation instructions.

After installing the plugin, you may need to restart your IDE completely for it to take effect.

## Usage

### From Your IDE

Run

```
claude
```

from your IDE’s integrated terminal, and all integration features will be active.

### From External Terminals

Use the

```
/ide
```

command in any external terminal to connect Claude Code to your JetBrains IDE and activate all features:

## Configuration

### Claude Code Settings

Configure IDE integration through Claude Code’s settings:

- Run

  ```
  claude
  ```
- Enter the

  ```
  /config
  ```

  command
- Set the diff tool to

  ```
  auto
  ```

  to show diffs in the IDE, or

  ```
  terminal
  ```

  to keep them in the terminal

### Plugin Settings

Configure the Claude Code plugin by going to Settings → Tools → Claude Code [Beta]:

#### General Settings

- Claude command: Specify a custom command to run Claude (for example,

  ```
  claude
  ```

  ,

  ```
  /usr/local/bin/claude
  ```

  , or

  ```
  npx @anthropic-ai/claude-code
  ```

  )
- Suppress notification for Claude command not found: Skip notifications about not finding the Claude command
- Enable using Option+Enter for multi-line prompts (macOS only): When enabled, Option+Enter inserts new lines in Claude Code prompts. Disable if experiencing issues with the Option key being captured unexpectedly (requires terminal restart)
- Enable automatic updates: Automatically check for and install plugin updates (applied on restart)

#### ESC Key Configuration

If the ESC key doesn’t interrupt Claude Code operations in JetBrains terminals:

- Go to Settings → Tools → Terminal
- Either:
  - Uncheck “Move focus to the editor with Escape”, or
  - Click “Configure terminal keybindings” and delete the “Switch focus to Editor” shortcut
- Apply the changes

## Special Configurations

### Remote Development

The plugin must be installed on the remote host, not on your local client machine.

### WSL Configuration

WSL configuration may require:

- Proper terminal configuration
- Networking mode adjustments
- Firewall settings updates

## Troubleshooting

### Plugin Not Working

- Ensure you’re running Claude Code from the project root directory
- Check that the JetBrains plugin is enabled in the IDE settings
- Completely restart the IDE (you may need to do this multiple times)
- For Remote Development, ensure the plugin is installed in the remote host

### IDE Not Detected

- Verify the plugin is installed and enabled
- Restart the IDE completely
- Check that you’re running Claude Code from the integrated terminal
- For WSL users, see the [[Troubleshooting - Claude Code Docs#JetBrains IDE not detected on WSL2|WSL troubleshooting guide]]

### Command Not Found

If clicking the Claude icon shows “command not found”:

- Verify Claude Code is installed:

  ```
  npm list -g @anthropic-ai/claude-code
  ```
- Configure the Claude command path in plugin settings
- For WSL users, use the WSL command format mentioned in the configuration section

## Security Considerations

When Claude Code runs in a JetBrains IDE with auto-edit permissions enabled, it may be able to modify IDE configuration files that can be automatically executed by your IDE. This may increase the risk of running Claude Code in auto-edit mode and allow bypassing Claude Code’s permission prompts for bash execution. When running in JetBrains IDEs, consider:

- Using manual approval mode for edits
- Taking extra care to ensure Claude is only used with trusted prompts
- Being aware of which files Claude Code has access to modify

[[Troubleshooting - Claude Code Docs|troubleshooting guide]].

---
title: Configure your terminal for Claude Code - Claude Code Docs
source_url: https://code.claude.com/docs/en/terminal-config
description: Fix Shift+Enter for newlines, get a terminal bell when Claude finishes,
  configure tmux, match the color theme, and enable Vim mode in the Claude Code CLI.
---

- [[Configure your terminal for Claude Code - Claude Code Docs#Enter multiline prompts|Shift+Enter submits instead of inserting a newline]]
- [[Configure your terminal for Claude Code - Claude Code Docs#Enable Option key shortcuts on macOS|Option-key shortcuts do nothing on macOS]]
- [[Configure your terminal for Claude Code - Claude Code Docs#Get a terminal bell or notification|No sound or alert when Claude finishes]]
- [[Configure your terminal for Claude Code - Claude Code Docs#Configure tmux|You run Claude Code inside tmux]]
- [[Configure your terminal for Claude Code - Claude Code Docs#Switch to fullscreen rendering|Display flickers or scrollback jumps]]
- [[Configure your terminal for Claude Code - Claude Code Docs#Edit prompts with Vim keybindings|You want Vim keys in the prompt]]

[[Customize keyboard shortcuts - Claude Code Docs|keybindings]]instead.

## Enter multiline prompts

Pressing Enter submits your message. To add a line break without submitting, press Ctrl+J, or type

```
\
```

and then press Enter. Both work in every terminal with no setup.
In most terminals you can also press Shift+Enter, but support varies by terminal emulator:

TerminalShift+Enter for newlineGhostty, Kitty, iTerm2, WezTerm, Warp, Apple TerminalWorks without setupVS Code, Cursor, Windsurf, Alacritty, ZedRun

```
/terminal-setup
```

onceWindows Terminal, gnome-terminal, JetBrains IDEs such as PyCharm and Android StudioNot available; use Ctrl+J or

```
\
```

then Enter

```
/terminal-setup
```

writes Shift+Enter and other keybindings into the terminal’s configuration file. In VS Code, Cursor, and Windsurf it also sets

```
terminal.integrated.mouseWheelScrollSensitivity
```

in the editor settings for smoother scrolling in

[[Fullscreen rendering - Claude Code Docs|fullscreen mode]]. Existing bindings and settings are left in place; if you see a message such as

```
VSCode terminal Shift+Enter key binding already configured
```

, no change was made. Run

```
/terminal-setup
```

directly in the host terminal rather than inside tmux or screen, since it needs to write to the host terminal’s configuration.
If you are running inside tmux, Shift+Enter also requires the

[[Configure your terminal for Claude Code - Claude Code Docs#Configure tmux|tmux configuration below]]even when the outer terminal supports it. To bind newline to a different key, or to swap behavior so Enter inserts a newline and Shift+Enter submits, map the

```
chat:newline
```

and

```
chat:submit
```

actions in your

[[Customize keyboard shortcuts - Claude Code Docs|keybindings file]].

## Enable Option key shortcuts on macOS

Some Claude Code shortcuts use the Option key, such as Option+Enter for a newline or Option+P to switch models. On macOS, most terminals do not send Option as a modifier by default, so these shortcuts do nothing until you enable it. The terminal setting for this is usually labeled “Use Option as Meta Key”; Meta is the historical Unix name for the key now labeled Option or Alt.

- Apple Terminal
- iTerm2
- VS Code

Open Settings → Profiles → Keyboard and check “Use Option as Meta Key”.If you accepted Claude Code’s first-run prompt that offered “Option+Enter for newlines and visual bell”, this is already done. That prompt runs

```
/terminal-setup
```

for you, which enables Option as Meta and switches the audio bell to a visual screen flash in your Apple Terminal profile.

## Get a terminal bell or notification

When Claude finishes a task or pauses for a permission prompt, it fires a notification event. Surfacing this as a terminal bell or desktop notification lets you switch to other work while a long task runs. Claude Code sends a desktop notification only in Ghostty, Kitty, and iTerm2; every other terminal needs a

[[Configure your terminal for Claude Code - Claude Code Docs#Play a sound with a Notification hook|Notification hook]]instead. The notification also reaches your local machine over SSH, so a remote session can still alert you. Ghostty and Kitty forward it to your OS notification center without further setup. iTerm2 requires you to enable forwarding:

If notifications still do not appear, confirm that your terminal application has notification permission in your OS settings, and if you are running inside tmux,

[[Configure your terminal for Claude Code - Claude Code Docs#Configure tmux|enable passthrough]].

### Play a sound with a Notification hook

In any terminal you can configure a

[[Automate workflows with hooks - Claude Code Docs#Get notified when Claude needs input|Notification hook]]to play a sound or run a custom command when Claude needs your attention. Hooks run alongside the desktop notification rather than replacing it. Terminals such as Warp or Apple Terminal rely on a hook alone since Claude Code does not send them a desktop notification. The example below plays a system sound on macOS. The linked guide has desktop notification commands for macOS, Linux, and Windows.

~/.claude/settings.json

## Configure tmux

When Claude Code runs inside tmux, two things break by default: Shift+Enter submits instead of inserting a newline, and desktop notifications and the

[[Claude Code settings - Claude Code Docs#Available settings|progress bar]]never reach the outer terminal. Add these lines to

```
~/.tmux.conf
```

, then run

```
tmux source-file ~/.tmux.conf
```

to apply them to the running server:

~/.tmux.conf

```
allow-passthrough
```

line lets notifications and progress updates reach iTerm2, Ghostty, or Kitty instead of being swallowed by tmux. The

```
extended-keys
```

lines let tmux distinguish Shift+Enter from plain Enter so the newline shortcut works.

## Match the color theme

Use the

```
/theme
```

command, or the theme picker in

```
/config
```

, to choose a Claude Code theme that matches your terminal. Selecting the auto option detects your terminal’s light or dark background, so the theme follows OS appearance changes whenever your terminal does. Claude Code does not control the terminal’s own color scheme, which is set by the terminal application.
To customize what appears at the bottom of the interface, configure a

[[Customize your status line - Claude Code Docs|custom status line]]that shows the current model, working directory, git branch, or other context.

### Create a custom theme

Custom themes require Claude Code v2.1.118 or later.

```
/theme
```

lists any custom themes you have defined and any themes contributed by installed

[[Plugins reference - Claude Code Docs#Themes|plugins]]. Select New custom theme… at the end of the list to create one interactively: you name the theme, then pick individual color tokens to override. Press

```
Ctrl+E
```

while a custom theme is highlighted to edit it.
Each custom theme is a JSON file in

```
~/.claude/themes/
```

. The filename without the

```
.json
```

extension is the theme’s slug, and selecting the theme stores

```
custom:<slug>
```

as your theme preference. The file has three optional fields:

FieldTypeDescription

```
name
```

stringDisplay label shown in

```
/theme
```

. Defaults to the filename slug

```
base
```

stringBuilt-in preset the theme starts from:

```
dark
```

,

```
light
```

,

```
dark-daltonized
```

,

```
light-daltonized
```

,

```
dark-ansi
```

, or

```
light-ansi
```

. Defaults to

```
dark
```

```
overrides
```

objectMap of color token names to color values. Tokens not listed here fall through to the base preset

```
#rrggbb
```

,

```
#rgb
```

,

```
rgb(r,g,b)
```

,

```
ansi256(n)
```

, or

```
ansi:<name>
```

where

```
<name>
```

is one of the 16 standard ANSI color names such as

```
red
```

or

```
cyanBright
```

. Unknown tokens and invalid color values are ignored, so a typo cannot break rendering.
The following example defines a theme that keeps the dark preset but recolors the prompt accent, error text, and success text:

~/.claude/themes/dracula.json

```
~/.claude/themes/
```

and reloads when a file changes, so edits made in your editor apply to a running session without a restart.

## Switch to fullscreen rendering

If the display flickers or the scroll position jumps while Claude is working, switch to

[[Fullscreen rendering - Claude Code Docs|fullscreen rendering mode]]. It draws to a separate screen the terminal reserves for full-screen apps instead of appending to your normal scrollback, which keeps memory usage flat and adds mouse support for scrolling and selection. In this mode you scroll with the mouse or PageUp inside Claude Code rather than with your terminal’s native scrollback; see the

[[Fullscreen rendering - Claude Code Docs#Search and review the conversation|fullscreen page]]for how to search and copy. Run

```
/tui fullscreen
```

to switch in the current session with your conversation intact. To make it the default, set the

```
CLAUDE_CODE_NO_FLICKER
```

environment variable before starting Claude Code:

## Paste large content

When you paste more than 10,000 characters into the prompt, Claude Code collapses the input to a

```
[Pasted text]
```

placeholder so the input box stays usable. The full content is still sent to Claude when you submit.
The VS Code integrated terminal can drop characters from very large pastes before they reach Claude Code, so prefer file-based workflows there. For very large inputs such as entire files or long logs, write the content to a file and ask Claude to read it instead of pasting. This keeps the conversation transcript readable and lets Claude reference the file by path in later turns.

## Edit prompts with Vim keybindings

Claude Code includes a Vim-style editing mode for the prompt input. Enable it through

```
/config
```

→ Editor mode, or by setting

[[Claude Code settings - Claude Code Docs#Available settings|to]]

```
editorMode
```

```
"vim"
```

in

```
~/.claude/settings.json
```

. Set Editor mode back to

```
normal
```

to turn it off.
Vim mode supports a subset of NORMAL- and VISUAL-mode motions and operators, such as

```
hjkl
```

navigation,

```
v
```

/

```
V
```

selection, and

```
d
```

/

```
c
```

/

```
y
```

with text objects. See the

[[Interactive mode - Claude Code Docs#Vim editor mode|Vim editor mode reference]]for the full key table. Vim motions are not remappable through the keybindings file. Pressing Enter still submits your prompt in INSERT mode, unlike standard Vim. Use

```
o
```

or

```
O
```

in NORMAL mode, or Ctrl+J, to insert a newline instead.

## Related resources

- [[Interactive mode - Claude Code Docs|Interactive mode]]: full keyboard shortcut reference and the Vim key table
- [[Customize keyboard shortcuts - Claude Code Docs|Keybindings]]: remap any Claude Code shortcut, including Enter and Shift+Enter
- [[Fullscreen rendering - Claude Code Docs|Fullscreen rendering]]: details on scrolling, search, and copy in fullscreen mode
- [[Automate workflows with hooks - Claude Code Docs|Hooks guide]]: more Notification hook examples for Linux and Windows
- [[Troubleshooting - Claude Code Docs|Troubleshooting]]: fixes for issues outside terminal configuration

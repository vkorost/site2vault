---
title: Customize keyboard shortcuts - Claude Code Docs
source_url: https://code.claude.com/docs/en/keybindings
description: Customize keyboard shortcuts in Claude Code with a keybindings configuration
  file.
---

Customizable keyboard shortcuts require Claude Code v2.1.18 or later. Check your version with

```
claude --version
```

.

Claude Code supports customizable keyboard shortcuts. Run

```
/keybindings
```

to create or open your configuration file at

```
~/.claude/keybindings.json
```

.

## Configuration file

The keybindings configuration file is an object with a

```
bindings
```

array. Each block specifies a context and a map of keystrokes to actions.

Changes to the keybindings file are automatically detected and applied without restarting Claude Code.

FieldDescription

```
$schema
```

Optional JSON Schema URL for editor autocompletion

```
$docs
```

Optional documentation URL

```
bindings
```

Array of binding blocks by context

This example binds

```
Ctrl+E
```

to open an external editor in the chat context, and unbinds

```
Ctrl+U
```

:

> ```
> {
>   "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
>   "$docs": "https://code.claude.com/docs/en/keybindings",
>   "bindings": [
>     {
>       "context": "Chat",
>       "bindings": {
>         "ctrl+e": "chat:externalEditor",
>         "ctrl+u": null
>       }
>     }
>   ]
> }
> ```

## Contexts

Each binding block specifies a context where the bindings apply:

ContextDescription

```
Global
```

Applies everywhere in the app

```
Chat
```

Main chat input area

```
Autocomplete
```

Autocomplete menu is open

```
Settings
```

Settings menu

```
Confirmation
```

Permission and confirmation dialogs

```
Tabs
```

Tab navigation components

```
Help
```

Help menu is visible

```
Transcript
```

Transcript viewer

```
HistorySearch
```

History search mode (Ctrl+R)

```
Task
```

Background task is running

```
ThemePicker
```

Theme picker dialog

```
Attachments
```

Image attachment navigation in select dialogs

```
Footer
```

Footer indicator navigation (tasks, teams, diff)

```
MessageSelector
```

Rewind and summarize dialog message selection

```
DiffDialog
```

Diff viewer navigation

```
ModelPicker
```

Model picker effort level

```
Select
```

Generic select/list components

```
Plugin
```

Plugin dialog (browse, discover, manage)

```
Scroll
```

Conversation scrolling and text selection in fullscreen mode

```
Doctor
```

```
/doctor
```

diagnostics screen

## Available actions

Actions follow a

```
namespace:action
```

format, such as

```
chat:submit
```

to send a message or

```
app:toggleTodos
```

to show the task list. Each context has specific actions available.

### App actions

Actions available in the

```
Global
```

context:

ActionDefaultDescription

```
app:interrupt
```

Ctrl+CCancel current operation

```
app:exit
```

Ctrl+DExit Claude Code

```
app:redraw
```

(unbound)Force terminal redraw

```
app:toggleTodos
```

Ctrl+TToggle task list visibility

```
app:toggleTranscript
```

Ctrl+OToggle verbose transcript

### History actions

Actions for navigating command history:

ActionDefaultDescription

```
history:search
```

Ctrl+ROpen history search

```
history:previous
```

UpPrevious history item

```
history:next
```

DownNext history item

### Chat actions

Actions available in the

```
Chat
```

context:

ActionDefaultDescription

```
chat:cancel
```

EscapeCancel current input

```
chat:clearInput
```

Ctrl+LClear prompt input and force a full screen redraw

```
chat:killAgents
```

Ctrl+X Ctrl+KKill all background agents

```
chat:cycleMode
```

Shift+Tab\*Cycle permission modes

```
chat:modelPicker
```

Meta+POpen model picker

```
chat:fastMode
```

Meta+OToggle fast mode

```
chat:thinkingToggle
```

Meta+TToggle extended thinking

```
chat:submit
```

EnterSubmit message

```
chat:newline
```

Ctrl+JInsert a newline without submitting

```
chat:undo
```

Ctrl+\_, Ctrl+Shift+-Undo last action

```
chat:externalEditor
```

Ctrl+G, Ctrl+X Ctrl+EOpen in external editor

```
chat:stash
```

Ctrl+SStash current prompt

```
chat:imagePaste
```

Ctrl+V (Alt+V on Windows)Paste image

\*On Windows without VT mode (Node <24.2.0/<22.17.0, Bun <1.2.23), defaults to Meta+M.

### Autocomplete actions

Actions available in the

```
Autocomplete
```

context:

ActionDefaultDescription

```
autocomplete:accept
```

TabAccept suggestion

```
autocomplete:dismiss
```

EscapeDismiss menu

```
autocomplete:previous
```

UpPrevious suggestion

```
autocomplete:next
```

DownNext suggestion

### Confirmation actions

Actions available in the

```
Confirmation
```

context:

ActionDefaultDescription

```
confirm:yes
```

Y, EnterConfirm action

```
confirm:no
```

N, EscapeDecline action

```
confirm:previous
```

UpPrevious option

```
confirm:next
```

DownNext option

```
confirm:nextField
```

TabNext field

```
confirm:previousField
```

(unbound)Previous field

```
confirm:toggle
```

SpaceToggle selection

```
confirm:cycleMode
```

Shift+TabCycle permission modes

```
confirm:toggleExplanation
```

Ctrl+EToggle permission explanation

### Permission actions

Actions available in the

```
Confirmation
```

context for permission dialogs:

ActionDefaultDescription

```
permission:toggleDebug
```

Ctrl+DToggle permission debug info

### Transcript actions

Actions available in the

```
Transcript
```

context:

ActionDefaultDescription

```
transcript:toggleShowAll
```

Ctrl+EToggle show all content

```
transcript:exit
```

q, Ctrl+C, EscapeExit transcript view

### History search actions

Actions available in the

```
HistorySearch
```

context:

ActionDefaultDescription

```
historySearch:next
```

Ctrl+RNext match

```
historySearch:accept
```

Escape, TabAccept selection

```
historySearch:cancel
```

Ctrl+CCancel search

```
historySearch:execute
```

EnterExecute selected command

### Task actions

Actions available in the

```
Task
```

context:

ActionDefaultDescription

```
task:background
```

Ctrl+BBackground current task

### Theme actions

Actions available in the

```
ThemePicker
```

context:

ActionDefaultDescription

```
theme:toggleSyntaxHighlighting
```

Ctrl+TToggle syntax highlighting

### Help actions

Actions available in the

```
Help
```

context:

ActionDefaultDescription

```
help:dismiss
```

EscapeClose help menu

### Tabs actions

Actions available in the

```
Tabs
```

context:

ActionDefaultDescription

```
tabs:next
```

Tab, RightNext tab

```
tabs:previous
```

Shift+Tab, LeftPrevious tab

### Attachments actions

Actions available in the

```
Attachments
```

context:

ActionDefaultDescription

```
attachments:next
```

RightNext attachment

```
attachments:previous
```

LeftPrevious attachment

```
attachments:remove
```

Backspace, DeleteRemove selected attachment

```
attachments:exit
```

Down, EscapeExit attachment navigation

Actions available in the

```
Footer
```

context:

ActionDefaultDescription

```
footer:next
```

RightNext footer item

```
footer:previous
```

LeftPrevious footer item

```
footer:up
```

UpNavigate up in footer (deselects at top)

```
footer:down
```

DownNavigate down in footer

```
footer:openSelected
```

EnterOpen selected footer item

```
footer:clearSelection
```

EscapeClear footer selection

### Message selector actions

Actions available in the

```
MessageSelector
```

context:

ActionDefaultDescription

```
messageSelector:up
```

Up, K, Ctrl+PMove up in list

```
messageSelector:down
```

Down, J, Ctrl+NMove down in list

```
messageSelector:top
```

Ctrl+Up, Shift+Up, Meta+Up, Shift+KJump to top

```
messageSelector:bottom
```

Ctrl+Down, Shift+Down, Meta+Down, Shift+JJump to bottom

```
messageSelector:select
```

EnterSelect message

### Diff actions

Actions available in the

```
DiffDialog
```

context:

ActionDefaultDescription

```
diff:dismiss
```

EscapeClose diff viewer

```
diff:previousSource
```

LeftPrevious diff source

```
diff:nextSource
```

RightNext diff source

```
diff:previousFile
```

UpPrevious file in diff

```
diff:nextFile
```

DownNext file in diff

```
diff:viewDetails
```

EnterView diff details

```
diff:back
```

(context-specific)Go back in diff viewer

### Model picker actions

Actions available in the

```
ModelPicker
```

context:

ActionDefaultDescription

```
modelPicker:decreaseEffort
```

LeftDecrease effort level

```
modelPicker:increaseEffort
```

RightIncrease effort level

### Select actions

Actions available in the

```
Select
```

context:

ActionDefaultDescription

```
select:next
```

Down, J, Ctrl+NNext option

```
select:previous
```

Up, K, Ctrl+PPrevious option

```
select:accept
```

EnterAccept selection

```
select:cancel
```

EscapeCancel selection

### Plugin actions

Actions available in the

```
Plugin
```

context:

ActionDefaultDescription

```
plugin:toggle
```

SpaceToggle plugin selection

```
plugin:install
```

IInstall selected plugins

```
plugin:favorite
```

FFavorite the selected plugin so it sorts near the top of the Installed tab

### Settings actions

Actions available in the

```
Settings
```

context:

ActionDefaultDescription

```
settings:search
```

/Enter search mode

```
settings:retry
```

RRetry loading usage data (on error)

```
settings:close
```

EnterSave changes and close the config panel. Escape discards changes and closes

### Doctor actions

Actions available in the

```
Doctor
```

context:

ActionDefaultDescription

```
doctor:fix
```

FSend the diagnostics report to Claude to fix the reported issues. Only active when issues are found

### Voice actions

Actions available in the

```
Chat
```

context when [[Voice dictation - Claude Code Docs|voice dictation]] is enabled:

ActionDefaultDescription

```
voice:pushToTalk
```

SpaceDictate a prompt. Hold or tap depending on

```
/voice
```

mode

Actions available in the

```
Scroll
```

context when [[Fullscreen rendering - Claude Code Docs|fullscreen rendering]] is enabled:

ActionDefaultDescription

```
scroll:lineUp
```

(unbound)Scroll up one line. Mouse wheel scrolling triggers this action

```
scroll:lineDown
```

(unbound)Scroll down one line. Mouse wheel scrolling triggers this action

```
scroll:pageUp
```

PageUpScroll up half the viewport height

```
scroll:pageDown
```

PageDownScroll down half the viewport height

```
scroll:top
```

Ctrl+HomeJump to the start of the conversation

```
scroll:bottom
```

Ctrl+EndJump to the latest message and re-enable auto-follow

```
scroll:halfPageUp
```

(unbound)Scroll up half the viewport height. Same behavior as

```
scroll:pageUp
```

, provided for vi-style rebinds

```
scroll:halfPageDown
```

(unbound)Scroll down half the viewport height. Same behavior as

```
scroll:pageDown
```

, provided for vi-style rebinds

```
scroll:fullPageUp
```

(unbound)Scroll up the full viewport height

```
scroll:fullPageDown
```

(unbound)Scroll down the full viewport height

```
selection:copy
```

Ctrl+Shift+C / Cmd+CCopy the selected text to the clipboard

```
selection:clear
```

(unbound)Clear the active text selection

```
selection:extendLeft
```

Shift+LeftExtend the active selection one column left

```
selection:extendRight
```

Shift+RightExtend the active selection one column right

```
selection:extendUp
```

Shift+UpExtend the active selection one row up. Scrolls the viewport when the selection reaches the top edge

```
selection:extendDown
```

Shift+DownExtend the active selection one row down. Scrolls the viewport when the selection reaches the bottom edge

```
selection:extendLineStart
```

Shift+HomeExtend the active selection to the start of the line

```
selection:extendLineEnd
```

Shift+EndExtend the active selection to the end of the line

## Keystroke syntax

### Modifiers

Use modifier keys with the

```
+
```

separator:

- ```
  ctrl
  ```

  or

  ```
  control
  ```

  - Control key
- ```
  shift
  ```

  - Shift key
- ```
  alt
  ```

  ,

  ```
  opt
  ```

  ,

  ```
  option
  ```

  , or

  ```
  meta
  ```

  - Alt key on Windows and Linux, Option key on macOS
- ```
  cmd
  ```

  ,

  ```
  command
  ```

  ,

  ```
  super
  ```

  , or

  ```
  win
  ```

  - Command key on macOS, Windows key on Windows, Super key on Linux

The

```
cmd
```

group is only detected in terminals that report the Super modifier, such as those supporting the Kitty keyboard protocol or xterm’s

```
modifyOtherKeys
```

mode. Most terminals do not send it, so use

```
ctrl
```

or

```
meta
```

for bindings you want to work everywhere.
For example:

> ```
> ctrl+k          Ctrl + K
> shift+tab       Shift + Tab
> meta+p          Option + P on macOS, Alt + P elsewhere
> ctrl+shift+c    Multiple modifiers
> ```

### Uppercase letters

A standalone uppercase letter implies Shift. For example,

```
K
```

is equivalent to

```
shift+k
```

. This is useful for vim-style bindings where uppercase and lowercase keys have different meanings.
Uppercase letters with modifiers (e.g.,

```
ctrl+K
```

) are treated as stylistic and do not imply Shift:

```
ctrl+K
```

is the same as

```
ctrl+k
```

.

### Chords

Chords are sequences of keystrokes separated by spaces:

> ```
> ctrl+k ctrl+s   Press Ctrl+K, release, then Ctrl+S
> ```

### Special keys

- ```
  escape
  ```

  or

  ```
  esc
  ```

  - Escape key
- ```
  enter
  ```

  or

  ```
  return
  ```

  - Enter key
- ```
  tab
  ```

  - Tab key
- ```
  space
  ```

  - Space bar
- ```
  up
  ```

  ,

  ```
  down
  ```

  ,

  ```
  left
  ```

  ,

  ```
  right
  ```

  - Arrow keys
- ```
  backspace
  ```

  ,

  ```
  delete
  ```

  - Delete keys

## Unbind default shortcuts

Set an action to

```
null
```

to unbind a default shortcut:

> ```
> {
>   "bindings": [
>     {
>       "context": "Chat",
>       "bindings": {
>         "ctrl+s": null
>       }
>     }
>   ]
> }
> ```

This also works for chord bindings. Unbinding every chord that shares a prefix frees that prefix for use as a single-key binding:

> ```
> {
>   "bindings": [
>     {
>       "context": "Chat",
>       "bindings": {
>         "ctrl+x ctrl+k": null,
>         "ctrl+x ctrl+e": null,
>         "ctrl+x": "chat:newline"
>       }
>     }
>   ]
> }
> ```

If you unbind some but not all chords on a prefix, pressing the prefix still enters chord-wait mode for the remaining bindings.

## Reserved shortcuts

These shortcuts cannot be rebound:

ShortcutReasonCtrl+CHardcoded interrupt/cancelCtrl+DHardcoded exitCtrl+MIdentical to Enter in terminals (both send CR)

## Terminal conflicts

Some shortcuts may conflict with terminal multiplexers:

ShortcutConflictCtrl+Btmux prefix (press twice to send)Ctrl+AGNU screen prefixCtrl+ZUnix process suspend (SIGTSTP)

## Vim mode interaction

When vim mode is enabled via

```
/config
```

→ Editor mode, keybindings and vim mode operate independently:

- Vim mode handles input at the text input level (cursor movement, modes, motions)
- Keybindings handle actions at the component level (toggle todos, submit, etc.)
- The Escape key in vim mode switches INSERT to NORMAL mode; it does not trigger

  ```
  chat:cancel
  ```
- Most Ctrl+key shortcuts pass through vim mode to the keybinding system
- In vim NORMAL mode,

  ```
  ?
  ```

  shows the help menu (vim behavior)

## Validation

Claude Code validates your keybindings and shows warnings for:

- Parse errors (invalid JSON or structure)
- Invalid context names
- Reserved shortcut conflicts
- Terminal multiplexer conflicts
- Duplicate bindings in the same context

Run

```
/doctor
```

to see any keybinding warnings.

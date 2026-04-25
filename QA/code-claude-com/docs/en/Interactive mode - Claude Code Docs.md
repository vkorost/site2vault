---
title: Interactive mode - Claude Code Docs
source_url: https://code.claude.com/docs/en/interactive-mode
description: Complete reference for keyboard shortcuts, input modes, and interactive
  features in Claude Code sessions.
---

## Keyboard shortcuts

Keyboard shortcuts may vary by platform and terminal. Press

```
?
```

to see available shortcuts for your environment.macOS users: Option/Alt key shortcuts (

```
Alt+B
```

,

```
Alt+F
```

,

```
Alt+Y
```

,

```
Alt+M
```

,

```
Alt+P
```

,

```
Alt+T
```

) require configuring Option as Meta in your terminal:

- iTerm2: Settings → Profiles → Keys → General → set Left/Right Option key to “Esc+”
- Apple Terminal: Settings → Profiles → Keyboard → check “Use Option as Meta Key”
- VS Code: set

  ```
  "terminal.integrated.macOptionIsMeta": true
  ```

  in VS Code settings

[[Configure your terminal for Claude Code - Claude Code Docs|Terminal configuration]]for details.

### General controls

ShortcutDescriptionContext

```
Ctrl+C
```

Cancel current input or generationStandard interrupt

```
Ctrl+X Ctrl+K
```

Kill all background agents. Press twice within 3 seconds to confirmBackground agent control

```
Ctrl+D
```

Exit Claude Code sessionEOF signal

```
Ctrl+G
```

or

```
Ctrl+X Ctrl+E
```

Open in default text editorEdit your prompt or custom response in your default text editor.

```
Ctrl+X Ctrl+E
```

is the readline-native binding. Turn on Show last response in external editor in

```
/config
```

to prepend Claude’s previous reply as

```
#
```

-commented context above your prompt; the comment block is stripped when you save

```
Ctrl+L
```

Clear prompt input and redraw screenClears typed text and forces a full terminal redraw. Conversation history is kept. Use this to recover if the display becomes garbled or partially blank

```
Ctrl+O
```

Toggle transcript viewerShows detailed tool usage and execution. Also expands MCP calls, which collapse to a single line like “Called slack 3 times” by default

```
Ctrl+R
```

Reverse search command historySearch through previous commands interactively

```
Ctrl+V
```

or

```
Cmd+V
```

(iTerm2) or

```
Alt+V
```

(Windows)Paste image from clipboardInserts an

```
[Image #N]
```

chip at the cursor so you can reference it positionally in your prompt

```
Ctrl+B
```

Background running tasksBackgrounds bash commands and agents. Tmux users press twice

```
Ctrl+T
```

Toggle task listShow or hide the

```
Left/Right arrows
```

```
Up/Down arrows
```

or

```
Ctrl+P
```

/

```
Ctrl+N
```

```
Esc
```

+

```
Esc
```

```
Shift+Tab
```

or

```
Alt+M
```

(some configurations)

```
default
```

,

```
acceptEdits
```

,

```
plan
```

, and any modes you have enabled, such as

```
auto
```

or

```
bypassPermissions
```

. See [[Choose a permission mode - Claude Code Docs|permission modes]].

```
Option+P
```

(macOS) or

```
Alt+P
```

(Windows/Linux)

```
Option+T
```

(macOS) or

```
Alt+T
```

(Windows/Linux)

```
Option+O
```

(macOS) or

```
Alt+O
```

(Windows/Linux)[[Speed up responses with fast mode - Claude Code Docs|fast mode]]

### Text editing

ShortcutDescriptionContext

```
Ctrl+A
```

Move cursor to start of current lineIn multiline input, moves to the start of the current logical line

```
Ctrl+E
```

Move cursor to end of current lineIn multiline input, moves to the end of the current logical line

```
Ctrl+K
```

Delete to end of lineStores deleted text for pasting

```
Ctrl+U
```

Delete from cursor to line startStores deleted text for pasting. Repeat to clear across lines in multiline input. On macOS, terminal emulators including iTerm2 and Terminal.app map

```
Cmd+Backspace
```

to this shortcut

```
Ctrl+W
```

Delete previous wordStores deleted text for pasting. On Windows,

```
Ctrl+Backspace
```

also deletes the previous word

```
Ctrl+Y
```

Paste deleted textPaste text deleted with

```
Ctrl+K
```

,

```
Ctrl+U
```

, or

```
Ctrl+W
```

```
Alt+Y
```

(after

```
Ctrl+Y
```

)Cycle paste historyAfter pasting, cycle through previously deleted text. Requires

```
Alt+B
```

[[Interactive mode - Claude Code Docs#Keyboard shortcuts|Option as Meta]]on macOS

```
Alt+F
```

[[Interactive mode - Claude Code Docs#Keyboard shortcuts|Option as Meta]]on macOS

### Theme and display

ShortcutDescriptionContext

```
Ctrl+T
```

Toggle syntax highlighting for code blocksOnly works inside the

```
/theme
```

picker menu. Controls whether code in Claude’s responses uses syntax coloring

### Multiline input

MethodShortcutContextQuick escape

```
\
```

+

```
Enter
```

Works in all terminalsOption key

```
Option+Enter
```

After enabling

```
Shift+Enter
```

```
Ctrl+J
```

### Quick commands

### Transcript viewer

When the transcript viewer is open (toggled with

```
Ctrl+O
```

), these shortcuts are available.

```
Ctrl+E
```

can be rebound via

[[Customize keyboard shortcuts - Claude Code Docs|.]]

```
transcript:toggleShowAll
```

ShortcutDescription

```
Ctrl+E
```

Toggle show all content

```
[[Extend Claude with skills - Claude Code Docs|
```

Write the full conversation to your terminal’s native scrollback so

```
Cmd+F
```

, tmux copy mode, and other native tools can search it. Requires

```
v
```

Write the conversation to a temporary file and open it in

```
$VISUAL
```

or

```
$EDITOR
```

. Requires

```
q
```

,

```
Ctrl+C
```

,

```
Esc
```

Exit transcript view. All three can be rebound via

```
transcript:exit
```

### Voice input

ShortcutDescriptionNotesHold or tap

```
Space
```

Voice dictationRequires

```
/voice tap
```

for tap-to-toggle.

## Commands

Type

```
/
```

in Claude Code to see all available commands, or type

```
/
```

followed by any letters to filter. The

```
/
```

menu shows everything you can invoke: built-in commands, bundled and user-authored

[skills]], and commands contributed by

[[Create plugins - Claude Code Docs|plugins]]and

[[Connect Claude Code to tools via MCP - Claude Code Docs#Use MCP prompts as commands|MCP servers]]. Not all built-in commands are visible to every user since some depend on your platform or plan. See the

[[Commands - Claude Code Docs|commands reference]]for the full list of commands included in Claude Code.

## Vim editor mode

Enable vim-style editing via

```
/config
```

→ Editor mode.

### Mode switching

CommandActionFrom mode

```
Esc
```

Enter NORMAL modeINSERT, VISUAL

```
i
```

Insert before cursorNORMAL

```
I
```

Insert at beginning of lineNORMAL

```
a
```

Insert after cursorNORMAL

```
A
```

Insert at end of lineNORMAL

```
o
```

Open line belowNORMAL

```
O
```

Open line aboveNORMAL

```
v
```

Start character-wise visual selectionNORMAL

```
V
```

Start line-wise visual selectionNORMAL

### Navigation (NORMAL mode)

CommandAction

```
h
```

/

```
j
```

/

```
k
```

/

```
l
```

Move left/down/up/right

```
w
```

Next word

```
e
```

End of word

```
b
```

Previous word

```
0
```

Beginning of line

```
$
```

End of line

```
^
```

First non-blank character

```
gg
```

Beginning of input

```
G
```

End of input

```
f{char}
```

Jump to next occurrence of character

```
F{char}
```

Jump to previous occurrence of character

```
t{char}
```

Jump to just before next occurrence of character

```
T{char}
```

Jump to just after previous occurrence of character

```
;
```

Repeat last f/F/t/T motion

```
,
```

Repeat last f/F/t/T motion in reverse

In vim normal mode, if the cursor is at the beginning or end of input and cannot move further,

```
j
```

/

```
k
```

and the arrow keys navigate command history instead.

### Editing (NORMAL mode)

CommandAction

```
x
```

Delete character

```
dd
```

Delete line

```
D
```

Delete to end of line

```
dw
```

/

```
de
```

/

```
db
```

Delete word/to end/back

```
cc
```

Change line

```
C
```

Change to end of line

```
cw
```

/

```
ce
```

/

```
cb
```

Change word/to end/back

```
yy
```

/

```
Y
```

Yank (copy) line

```
yw
```

/

```
ye
```

/

```
yb
```

Yank word/to end/back

```
p
```

Paste after cursor

```
P
```

Paste before cursor

```
>>
```

Indent line

```
<<
```

Dedent line

```
J
```

Join lines

```
u
```

Undo

```
.
```

Repeat last change

### Text objects (NORMAL mode)

Text objects work with operators like

```
d
```

,

```
c
```

, and

```
y
```

:

CommandAction

```
iw
```

/

```
aw
```

Inner/around word

```
iW
```

/

```
aW
```

Inner/around WORD (whitespace-delimited)

```
i"
```

/

```
a"
```

Inner/around double quotes

```
i'
```

/

```
a'
```

Inner/around single quotes

```
i(
```

/

```
a(
```

Inner/around parentheses

```
i[[Environment variables - Claude Code Docs|
```

/

```
a[
```

Inner/around brackets

```
i{
```

/

```
a{
```

Inner/around braces

### Visual mode

Press

```
v
```

for character-wise selection or

```
V
```

for line-wise selection. Motions extend the selection, and operators act on it directly.

CommandAction

```
d
```

/

```
x
```

Delete selection

```
y
```

Yank selection

```
c
```

/

```
s
```

Change selection

```
p
```

Replace selection with register contents

```
r{char}
```

Replace every selected character with

```
{char}
```

```
~
```

/

```
u
```

/

```
U
```

Toggle, lowercase, or uppercase selection

```
>
```

/

```
<
```

Indent or dedent selected lines

```
J
```

Join selected lines

```
o
```

Swap cursor and anchor

```
iw
```

/

```
aw
```

/

```
i"
```

/…Select a text object

```
v
```

/

```
V
```

Toggle between character-wise and line-wise, or exit

```
Ctrl+V
```

is not supported.

## Command history

Claude Code maintains command history for the current session:

- Input history is stored per working directory
- Input history resets when you run

  ```
  /clear
  ```

  to start a new session. The previous session’s conversation is preserved and can be resumed.
- Use Up/Down arrows to navigate (see keyboard shortcuts above)
- Note: history expansion (

  ```
  !
  ```

  ) is disabled by default

### Reverse search with Ctrl+R

Press

```
Ctrl+R
```

to interactively search through your command history:

- Start search: press

  ```
  Ctrl+R
  ```

  to activate reverse history search
- Type query: enter text to search for in previous commands. The search term is highlighted in matching results
- Navigate matches: press

  ```
  Ctrl+R
  ```

  again to cycle through older matches
- Accept match:
  - Press

    ```
    Tab
    ```

    or

    ```
    Esc
    ```

    to accept the current match and continue editing
  - Press

    ```
    Enter
    ```

    to accept and execute the command immediately
- Press
- Cancel search:
  - Press

    ```
    Ctrl+C
    ```

    to cancel and restore your original input
  - Press

    ```
    Backspace
    ```

    on empty search to cancel
- Press

## Background bash commands

Claude Code supports running bash commands in the background, allowing you to continue working while long-running processes execute.

### How backgrounding works

When Claude Code runs a command in the background, it runs the command asynchronously and immediately returns a background task ID. Claude Code can respond to new prompts while the command continues executing in the background. To run commands in the background, you can either:

- Prompt Claude Code to run a command in the background
- Press Ctrl+B to move a regular Bash tool invocation to the background. (Tmux users must press Ctrl+B twice due to tmux’s prefix key.)

- Output is written to a file and Claude can retrieve it using the Read tool
- Background tasks have unique IDs for tracking and output retrieval
- Background tasks are automatically cleaned up when Claude Code exits
- Background tasks are automatically terminated if output exceeds 5GB, with a note in stderr explaining why

```
CLAUDE_CODE_DISABLE_BACKGROUND_TASKS
```

environment variable to

```
1
```

. See

[Environment variables]]for details. Common backgrounded commands:

- Build tools (webpack, vite, make)
- Package managers (npm, yarn, pnpm)
- Test runners (jest, pytest)
- Development servers
- Long-running processes (docker, terraform)

### Bash mode with ``` ! ``` prefix

Run bash commands directly without going through Claude by prefixing your input with

```
!
```

:

- Adds the command and its output to the conversation context
- Shows real-time progress and output
- Supports the same

  ```
  Ctrl+B
  ```

  backgrounding for long-running commands
- Does not require Claude to interpret or approve the command
- Supports history-based autocomplete: type a partial command and press Tab to complete from previous

  ```
  !
  ```

  commands in the current project
- Exit with

  ```
  Escape
  ```

  ,

  ```
  Backspace
  ```

  , or

  ```
  Ctrl+U
  ```

  on an empty prompt
- Pasting text that starts with

  ```
  !
  ```

  into an empty prompt enters bash mode automatically, matching typed

  ```
  !
  ```

  behavior

## Prompt suggestions

When you first open a session, a grayed-out example command appears in the prompt input to help you get started. Claude Code picks this from your project’s git history, so it reflects files you’ve been working on recently. After Claude responds, suggestions continue to appear based on your conversation history, such as a follow-up step from a multi-part request or a natural continuation of your workflow.

- Press Tab or Right arrow to accept the suggestion, or press Enter to accept and submit
- Start typing to dismiss it

```
/config
```

:

## Side questions with /btw

Use

```
/btw
```

to ask a quick question about your current work without adding to the conversation history. This is useful when you want a fast answer but don’t want to clutter the main context or derail Claude from a long-running task.

- Available while Claude is working: you can run

  ```
  /btw
  ```

  even while Claude is processing a response. The side question runs independently and does not interrupt the main turn.
- No tool access: side questions answer only from what is already in context. Claude cannot read files, run commands, or search when answering a side question.
- Single response: there are no follow-up turns. If you need a back-and-forth, use a normal prompt instead.
- Low cost: the side question reuses the parent conversation’s prompt cache, so the additional cost is minimal.

```
/btw
```

is the inverse of a

[[Create custom subagents - Claude Code Docs|subagent]]: it sees your full conversation but has no tools, while a subagent has full tools but starts with an empty context. Use

```
/btw
```

to ask about what Claude already knows from this session; use a subagent to go find out something new.

## Task list

When working on complex, multi-step work, Claude creates a task list to track progress. Tasks appear in the status area of your terminal with indicators showing what’s pending, in progress, or complete.

- Press

  ```
  Ctrl+T
  ```

  to toggle the task list view. The display shows up to 5 tasks at a time
- To see all tasks or clear them, ask Claude directly: “show me all tasks” or “clear all tasks”
- Tasks persist across context compactions, helping Claude stay organized on larger projects
- To share a task list across sessions, set

  ```
  CLAUDE_CODE_TASK_LIST_ID
  ```

  to use a named directory in

  ```
  ~/.claude/tasks/
  ```

  :

  ```
  CLAUDE_CODE_TASK_LIST_ID=my-project claude
  ```

## Session recap

When you return to the terminal after stepping away, Claude Code shows a one-line recap of what happened in the session so far. The recap generates in the background once at least three minutes have passed since the last completed turn and the terminal is unfocused, so it’s ready when you switch back. Recaps only appear once the session has at least three turns, and never twice in a row. Run

```
/recap
```

to generate a summary on demand. To turn automatic recaps off, open

```
/config
```

and disable Session recap.
Session recap is on by default for every plan and provider. The recap is always skipped in non-interactive mode.

## PR review status

When working on a branch with an open pull request, Claude Code displays a clickable PR link in the footer (for example, “PR #446”). The link has a colored underline indicating the review state:

- Green: approved
- Yellow: pending review
- Red: changes requested
- Gray: draft
- Purple: merged

```
Cmd+click
```

(Mac) or

```
Ctrl+click
```

(Windows/Linux) the link to open the pull request in your browser. The status updates automatically every 60 seconds.

PR status requires the

```
gh
```

CLI to be installed and authenticated (

```
gh auth login
```

).

## See also

- [[Extend Claude with skills - Claude Code Docs|Skills]]- Custom prompts and workflows
- [[Checkpointing - Claude Code Docs|Checkpointing]]- Rewind Claude’s edits and restore previous states
- [[CLI reference - Claude Code Docs|CLI reference]]- Command-line flags and options
- [[Claude Code settings - Claude Code Docs|Settings]]- Configuration options
- [[How Claude remembers your project - Claude Code Docs|Memory management]]- Managing CLAUDE.md files

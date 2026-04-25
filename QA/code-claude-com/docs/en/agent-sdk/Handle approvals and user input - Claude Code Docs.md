---
title: Handle approvals and user input - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/user-input
description: Surface Claude's approval requests and clarifying questions to users,
  then return their decisions to the SDK.
---

```
AskUserQuestion
```

tool). Both trigger your

```
canUseTool
```

callback, which pauses execution until you return a response. This is different from normal conversation turns where Claude finishes and waits for your next message.
For clarifying questions, Claude generates the questions and options. Your role is to present them to users and return their selections. You can’t add your own questions to this flow; if you need to ask users something yourself, do that separately in your application logic.
The callback can stay pending indefinitely. Execution remains paused until your callback returns, and the SDK only cancels the wait when the query itself is cancelled. If a user might take longer to respond than your process can reasonably stay running, the TypeScript SDK supports the

[[Hooks reference - Claude Code Docs#Defer a tool call for later|, which lets the process exit and resume later from the persisted session; this option is not available in the Python SDK. This guide shows you how to detect each type of request and respond appropriately.]]

```
defer
```

hook decision

## Detect when Claude needs input

Pass a

```
canUseTool
```

callback in your query options. The callback fires whenever Claude needs user input, receiving the tool name and input as arguments:

- Tool needs approval: Claude wants to use a tool that isn’t auto-approved by [[Configure permissions - Claude Code Docs-dbd6de|permission rules]]or modes. Check

  ```
  tool_name
  ```

  for the tool (e.g.,

  ```
  "Bash"
  ```

  ,

  ```
  "Write"
  ```

  ).
- Claude asks a question: Claude calls the

  ```
  AskUserQuestion
  ```

  tool. Check if

  ```
  tool_name == "AskUserQuestion"
  ```

  to handle it differently. If you specify a

  ```
  tools
  ```

  array, include

  ```
  AskUserQuestion
  ```

  for this to work. See[[Handle approvals and user input - Claude Code Docs#Handle clarifying questions|Handle clarifying questions]]for details.

To automatically allow or deny tools without prompting users, use

[[Intercept and control agent behavior with hooks - Claude Code Docs|hooks]]instead. Hooks execute before

```
canUseTool
```

and can allow, deny, or modify requests based on your own logic. You can also use the [[Intercept and control agent behavior with hooks - Claude Code Docs#Available hooks|to send external notifications (Slack, email, push) when Claude is waiting for approval.]]

```
PermissionRequest
```

hook

## Handle tool approval requests

Once you’ve passed a

```
canUseTool
```

callback in your query options, it fires when Claude wants to use a tool that isn’t auto-approved. Your callback receives three arguments:

ArgumentDescription

```
toolName
```

The name of the tool Claude wants to use (e.g.,

```
"Bash"
```

,

```
"Write"
```

,

```
"Edit"
```

)

```
input
```

The parameters Claude is passing to the tool. Contents vary by tool.

```
options
```

(TS) /

```
context
```

(Python)Additional context including optional

```
suggestions
```

(proposed

```
PermissionUpdate
```

entries to avoid re-prompting) and a cancellation signal. In TypeScript,

```
signal
```

is an

```
AbortSignal
```

; in Python, the signal field is reserved for future use. See

```
ToolPermissionContext
```

```
input
```

object contains tool-specific parameters. Common examples:

ToolInput fields

```
Bash
```

```
command
```

,

```
description
```

,

```
timeout
```

```
Write
```

```
file_path
```

,

```
content
```

```
Edit
```

```
file_path
```

,

```
old_string
```

,

```
new_string
```

```
Read
```

```
file_path
```

,

```
offset
```

,

```
limit
```

[[Agent SDK reference - Python - Claude Code Docs|Python]]|

[[Agent SDK reference - TypeScript - Claude Code Docs#Tool Input Types|TypeScript]]. You can display this information to the user so they can decide whether to allow or reject the action, then return the appropriate response. The following example asks Claude to create and delete a test file. When Claude attempts each operation, the callback prints the tool request to the terminal and prompts for y/n approval.

In Python,

```
can_use_tool
```

requires [[Streaming Input - Claude Code Docs|streaming mode]]and a

```
PreToolUse
```

hook that returns

```
{"continue_": True}
```

to keep the stream open. Without this hook, the stream closes before the permission callback can be invoked.

```
y/n
```

flow where any input other than

```
y
```

is treated as a denial. In practice, you might build a richer UI that lets users modify the request, provide feedback, or redirect Claude entirely. See

[[Handle approvals and user input - Claude Code Docs#Respond to tool requests|Respond to tool requests]]for all the ways you can respond.

### Respond to tool requests

Your callback returns one of two response types:

ResponsePythonTypeScriptAllow

```
PermissionResultAllow(updated_input=...)
```

```
{ behavior: "allow", updatedInput }
```

Deny

```
PermissionResultDeny(message=...)
```

```
{ behavior: "deny", message }
```

- Approve: let the tool execute as Claude requested
- Approve with changes: modify the input before execution (e.g., sanitize paths, add constraints)
- Reject: block the tool and tell Claude why
- Suggest alternative: block but guide Claude toward what the user wants instead
- Redirect entirely: use [[Streaming Input - Claude Code Docs|streaming input]]to send Claude a completely new instruction

- Approve
- Approve with changes
- Reject
- Suggest alternative
- Redirect entirely

The user approves the action as-is. Pass through the

```
input
```

from your callback unchanged and the tool executes exactly as Claude requested.

## Handle clarifying questions

When Claude needs more direction on a task with multiple valid approaches, it calls the

```
AskUserQuestion
```

tool. This triggers your

```
canUseTool
```

callback with

```
toolName
```

set to

```
AskUserQuestion
```

. The input contains Claude’s questions as multiple-choice options, which you display to the user and return their selections.
The following steps show how to handle clarifying questions:

Pass a canUseTool callback

Pass a

```
canUseTool
```

callback in your query options. By default,

```
AskUserQuestion
```

is available. If you specify a

```
tools
```

array to restrict Claude’s capabilities (for example, a read-only agent with only

```
Read
```

,

```
Glob
```

, and

```
Grep
```

), include

```
AskUserQuestion
```

in that array. Otherwise, Claude won’t be able to ask clarifying questions:

Detect AskUserQuestion

In your callback, check if

```
toolName
```

equals

```
AskUserQuestion
```

to handle it differently from other tools:

Parse the question input

The input contains Claude’s questions in a See

```
questions
```

array. Each question has a

```
question
```

(the text to display),

```
options
```

(the choices), and

```
multiSelect
```

(whether multiple selections are allowed):[[Handle approvals and user input - Claude Code Docs#Question format|Question format]]for full field descriptions.

Collect answers from the user

Present the questions to the user and collect their selections. How you do this depends on your application: a terminal prompt, a web form, a mobile dialog, etc.

Return answers to Claude

Build the

For multi-select questions, join multiple labels with

```
answers
```

object as a record where each key is the

```
question
```

text and each value is the selected option’s

```
label
```

:

From the question objectUse as

```
question
```

field (e.g.,

```
"How should I format the output?"
```

)KeySelected option’s

```
label
```

field (e.g.,

```
"Summary"
```

)Value

```
", "
```

. If you [[Handle approvals and user input - Claude Code Docs#Support free-text input|support free-text input]], use the user’s custom text as the value.

### Question format

The input contains Claude’s generated questions in a

```
questions
```

array. Each question has these fields:

FieldDescription

```
question
```

The full question text to display

```
header
```

Short label for the question (max 12 characters)

```
options
```

Array of 2-4 choices, each with

```
label
```

and

```
description
```

. TypeScript: optionally

```
preview
```

(see

```
multiSelect
```

If

```
true
```

, users can select multiple options

#### Option previews (TypeScript)

```
toolConfig.askUserQuestion.previewFormat
```

adds a

```
preview
```

field to each option so your app can show a visual mockup alongside the label. Without this setting, Claude does not generate previews and the field is absent.

```
previewFormat
```

```
preview
```

containsunset (default)Field is absent. Claude does not generate previews.

```
"markdown"
```

ASCII art and fenced code blocks

```
"html"
```

A styled

```
<div>
```

fragment (the SDK rejects

```
<script>
```

,

```
<style>
```

, and

```
<!DOCTYPE>
```

before your callback runs)

```
preview
```

on options where a visual comparison helps (layout choices, color schemes) and omits it where one wouldn’t (yes/no confirmations, text-only choices). Check for

```
undefined
```

before rendering.

### Response format

Return an

```
answers
```

object mapping each question’s

```
question
```

field to the selected option’s

```
label
```

:

FieldDescription

```
questions
```

Pass through the original questions array (required for tool processing)

```
answers
```

Object where keys are question text and values are selected labels

```
", "
```

. For free-text input, use the user’s custom text directly.

#### Support free-text input

Claude’s predefined options won’t always cover what users want. To let users type their own answer:

- Display an additional “Other” choice after Claude’s options that accepts text input
- Use the user’s custom text as the answer value (not the word “Other”)

[[Handle approvals and user input - Claude Code Docs#Complete example|complete example]]below for a full implementation.

### Complete example

Claude asks clarifying questions when it needs user input to proceed. For example, when asked to help decide on a tech stack for a mobile app, Claude might ask about cross-platform vs native, backend preferences, or target platforms. These questions help Claude make decisions that match the user’s preferences rather than guessing. This example handles those questions in a terminal application. Here’s what happens at each step:

- Route the request: The

  ```
  canUseTool
  ```

  callback checks if the tool name is

  ```
  "AskUserQuestion"
  ```

  and routes to a dedicated handler
- Display questions: The handler loops through the

  ```
  questions
  ```

  array and prints each question with numbered options
- Collect input: The user can enter a number to select an option, or type free text directly (e.g., “jquery”, “i don’t know”)
- Map answers: The code checks if input is numeric (uses the option’s label) or free text (uses the text directly)
- Return to Claude: The response includes both the original

  ```
  questions
  ```

  array and the

  ```
  answers
  ```

  mapping

## Limitations

- Subagents:

  ```
  AskUserQuestion
  ```

  is not currently available in subagents spawned via the Agent tool
- Question limits: each

  ```
  AskUserQuestion
  ```

  call supports 1-4 questions with 2-4 options each

## Other ways to get user input

The

```
canUseTool
```

callback and

```
AskUserQuestion
```

tool cover most approval and clarification scenarios, but the SDK offers other ways to get input from users:

### Streaming input

Use

[[Streaming Input - Claude Code Docs|streaming input]]when you need to:

- Interrupt the agent mid-task: send a cancel signal or change direction while Claude is working
- Provide additional context: add information Claude needs without waiting for it to ask
- Build chat interfaces: let users send follow-up messages during long-running operations

### Custom tools

Use

[[Give Claude custom tools - Claude Code Docs|custom tools]]when you need to:

- Collect structured input: build forms, wizards, or multi-step workflows that go beyond

  ```
  AskUserQuestion
  ```

  ’s multiple-choice format
- Integrate external approval systems: connect to existing ticketing, workflow, or approval platforms
- Implement domain-specific interactions: create tools tailored to your application’s needs, like code review interfaces or deployment checklists

```
canUseTool
```

callback.

## Related resources

- [[Configure permissions - Claude Code Docs-dbd6de|Configure permissions]]: set up permission modes and rules
- [[Intercept and control agent behavior with hooks - Claude Code Docs|Control execution with hooks]]: run custom code at key points in the agent lifecycle
- [[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript SDK reference]]: full canUseTool API documentation

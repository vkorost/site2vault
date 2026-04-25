---
title: How Claude Code works - Claude Code Docs
source_url: https://code.claude.com/docs/en/how-claude-code-works
description: Understand the agentic loop, built-in tools, and how Claude Code interacts
  with your project.
---

[[How Claude Code works - Claude Code Docs#Work effectively with Claude Code|tips for working effectively]]. For step-by-step walkthroughs, see

[[Common workflows - Claude Code Docs|Common workflows]]. For extensibility features like skills, MCP, and hooks, see

[[Extend Claude Code - Claude Code Docs|Extend Claude Code]].

## The agentic loop

When you give Claude a task, it works through three phases: gather context, take action, and verify results. These phases blend together. Claude uses tools throughout, whether searching files to understand your code, editing to make changes, or running tests to check its work. The loop adapts to what you ask. A question about your codebase might only need context gathering. A bug fix cycles through all three phases repeatedly. A refactor might involve extensive verification. Claude decides what each step requires based on what it learned from the previous step, chaining dozens of actions together and course-correcting along the way. You’re part of this loop too. You can interrupt at any point to steer Claude in a different direction, provide additional context, or ask it to try a different approach. Claude works autonomously but stays responsive to your input. The agentic loop is powered by two components:

[[How Claude Code works - Claude Code Docs#Models|models]]that reason and

[[How Claude Code works - Claude Code Docs#Tools|tools]]that act. Claude Code serves as the agentic harness around Claude: it provides the tools, context management, and execution environment that turn a language model into a capable coding agent.

### Models

Claude Code uses Claude models to understand your code and reason about tasks. Claude can read code in any language, understand how components connect, and figure out what needs to change to accomplish your goal. For complex tasks, it breaks work into steps, executes them, and adjusts based on what it learns.

[[Model configuration - Claude Code Docs|Multiple models]]are available with different tradeoffs. Sonnet handles most coding tasks well. Opus provides stronger reasoning for complex architectural decisions. Switch with

```
/model
```

during a session or start with

```
claude --model <name>
```

.
When this guide says “Claude chooses” or “Claude decides,” it’s the model doing the reasoning.

### Tools

Tools are what make Claude Code agentic. Without tools, Claude can only respond with text. With tools, Claude can act: read your code, edit files, run commands, search the web, and interact with external services. Each tool use returns information that feeds back into the loop, informing Claude’s next decision. The built-in tools generally fall into five categories, each representing a different kind of agency.

CategoryWhat Claude can doFile operationsRead files, edit code, create new files, rename and reorganizeSearchFind files by pattern, search content with regex, explore codebasesExecutionRun shell commands, start servers, run tests, use gitWebSearch the web, fetch documentation, look up error messagesCode intelligenceSee type errors and warnings after edits, jump to definitions, find references (requires

[[Tools reference - Claude Code Docs|Tools available to Claude]]for the complete list. Claude chooses which tools to use based on your prompt and what it learns along the way. When you say “fix the failing tests,” Claude might:

- Run the test suite to see what’s failing
- Read the error output
- Search for the relevant source files
- Read those files to understand the code
- Edit the files to fix the issue
- Run the tests again to verify

[[Extend Claude with skills - Claude Code Docs|skills]], connect to external services with

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP]], automate workflows with

[[Hooks reference - Claude Code Docs|hooks]], and offload tasks to

[[Create custom subagents - Claude Code Docs|subagents]]. These extensions form a layer on top of the core agentic loop. See

[[Extend Claude Code - Claude Code Docs|Extend Claude Code]]for guidance on choosing the right extension for your needs.

## What Claude can access

This guide focuses on the terminal. Claude Code also runs in

[[Use Claude Code in VS Code - Claude Code Docs|VS Code]],

[[JetBrains IDEs - Claude Code Docs|JetBrains IDEs]], and other environments. When you run

```
claude
```

in a directory, Claude Code gains access to:

- Your project. Files in your directory and subdirectories, plus files elsewhere with your permission.
- Your terminal. Any command you could run: build tools, git, package managers, system utilities, scripts. If you can do it from the command line, Claude can too.
- Your git state. Current branch, uncommitted changes, and recent commit history.
- Your [[How Claude remembers your project - Claude Code Docs|CLAUDE.md]]. A markdown file where you store project-specific instructions, conventions, and context that Claude should know every session.
- [[How Claude remembers your project - Claude Code Docs#Auto memory|Auto memory]]. Learnings Claude saves automatically as you work, like project patterns and your preferences. The first 200 lines or 25KB of MEMORY.md, whichever comes first, load at the start of each session.
- Extensions you configure. [[Connect Claude Code to tools via MCP - Claude Code Docs|MCP servers]]for external services,[[Extend Claude with skills - Claude Code Docs|skills]]for workflows,[[Create custom subagents - Claude Code Docs|subagents]]for delegated work, and[[Use Claude Code with Chrome (beta) - Claude Code Docs|Claude in Chrome]]for browser interaction.

## Environments and interfaces

The agentic loop, tools, and capabilities described above are the same everywhere you use Claude Code. What changes is where the code executes and how you interact with it.

### Execution environments

Claude Code runs in three environments, each with different tradeoffs for where your code executes.

EnvironmentWhere code runsUse caseLocalYour machineDefault. Full access to your files, tools, and environmentCloudAnthropic-managed VMsOffload tasks, work on repos you don’t have locallyRemote ControlYour machine, controlled from a browserUse the web UI while keeping everything local

### Interfaces

You can access Claude Code through the terminal, the

[[Use Claude Code Desktop - Claude Code Docs|desktop app]],

[[Use Claude Code in VS Code - Claude Code Docs|IDE extensions]],

[claude.ai/code](https://claude.ai/code),

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]],

[[Claude Code in Slack - Claude Code Docs|Slack]], and

[[Claude Code GitHub Actions - Claude Code Docs|CI/CD pipelines]]. The interface determines how you see and interact with Claude, but the underlying agentic loop is identical. See

[Use Claude Code everywhere](https://code.claude.com/docs/en/overview#use-claude-code-everywhere)for the full list.

## Work with sessions

Claude Code saves your conversation locally as you work. Each message, tool use, and result is written to a plaintext JSONL file under

```
~/.claude/projects/
```

, which enables

[[How Claude Code works - Claude Code Docs#Undo changes with checkpoints|rewinding]],

[[How Claude Code works - Claude Code Docs#Resume or fork sessions|resuming, and forking]]sessions. Before Claude makes code changes, it also snapshots the affected files so you can revert if needed. For paths, retention, and how to clear this data, see

[[Explore the .claude directory - Claude Code Docs#Application data|application data in]]. Sessions are independent. Each new session starts with a fresh context window, without the conversation history from previous sessions. Claude can persist learnings across sessions using

```
~/.claude
```

[[How Claude remembers your project - Claude Code Docs#Auto memory|auto memory]], and you can add your own persistent instructions in

[[How Claude remembers your project - Claude Code Docs|CLAUDE.md]].

### Work across branches

Each Claude Code conversation is a session tied to your current directory. The

```
/resume
```

picker shows sessions from the current worktree by default, with keyboard shortcuts to widen the list to other worktrees or projects. See

[[Common workflows - Claude Code Docs#Resume previous conversations|Resume previous conversations]]for the full list of picker shortcuts and how name resolution works. Claude sees your current branch’s files. When you switch branches, Claude sees the new branch’s files, but your conversation history stays the same. Claude remembers what you discussed even after switching. Since sessions are tied to directories, you can run parallel Claude sessions by using

[[Common workflows - Claude Code Docs#Run parallel Claude Code sessions with Git worktrees|git worktrees]], which create separate directories for individual branches.

### Resume or fork sessions

When you resume a session with

```
claude --continue
```

or

```
claude --resume
```

, you pick up where you left off using the same session ID. New messages append to the existing conversation. Your full conversation history is restored, but session-scoped permissions are not. You’ll need to re-approve those.
To branch off and try a different approach without affecting the original session, use the

```
--fork-session
```

flag:

```
--fork-session
```

to give each terminal its own clean session.

### The context window

Claude’s context window holds your conversation history, file contents, command outputs,

[[How Claude remembers your project - Claude Code Docs|CLAUDE.md]],

[[How Claude remembers your project - Claude Code Docs#Auto memory|auto memory]], loaded skills, and system instructions. As you work, context fills up. Claude compacts automatically, but instructions from early in the conversation can get lost. Put persistent rules in CLAUDE.md, and run

```
/context
```

to see what’s using space.
For an interactive walkthrough of what loads and when, see

[[Explore the context window - Claude Code Docs|Explore the context window]].

#### When context fills up

Claude Code manages context automatically as you approach the limit. It clears older tool outputs first, then summarizes the conversation if needed. Your requests and key code snippets are preserved; detailed instructions from early in the conversation may be lost. Put persistent rules in CLAUDE.md rather than relying on conversation history. To control what’s preserved during compaction, add a “Compact Instructions” section to CLAUDE.md or run

```
/compact
```

with a focus (like

```
/compact focus on the API changes
```

).
If a single file or tool output is so large that context refills immediately after each summary, Claude Code stops auto-compacting after a few attempts and shows an error instead of looping. See

[[Troubleshooting - Claude Code Docs#Auto-compaction stops with a thrashing error|Auto-compaction stops with a thrashing error]]for recovery steps. Run

```
/context
```

to see what’s using space. MCP tool definitions are deferred by default and loaded on demand via

[[Connect Claude Code to tools via MCP - Claude Code Docs#Scale with MCP Tool Search|tool search]], so only tool names consume context until Claude uses a specific tool. Run

```
/mcp
```

to check per-server costs.

#### Manage context with skills and subagents

Beyond compaction, you can use other features to control what loads into context.

[[Extend Claude with skills - Claude Code Docs|Skills]]load on demand. Claude sees skill descriptions at session start, but the full content only loads when a skill is used. For skills you invoke manually, set

```
disable-model-invocation: true
```

to keep descriptions out of context until you need them.

[[Create custom subagents - Claude Code Docs|Subagents]]get their own fresh context, completely separate from your main conversation. Their work doesn’t bloat your context. When done, they return a summary. This isolation is why subagents help with long sessions. See

[[Extend Claude Code - Claude Code Docs#Understand context costs|context costs]]for what each feature costs, and

[[Manage costs effectively - Claude Code Docs#Reduce token usage|reduce token usage]]for tips on managing context.

## Stay safe with checkpoints and permissions

Claude has two safety mechanisms: checkpoints let you undo file changes, and permissions control what Claude can do without asking.

### Undo changes with checkpoints

Every file edit is reversible. Before Claude edits any file, it snapshots the current contents. If something goes wrong, press

```
Esc
```

twice to rewind to a previous state, or ask Claude to undo.
Checkpoints are local to your session, separate from git. They only cover file changes. Actions that affect remote systems (databases, APIs, deployments) can’t be checkpointed, which is why Claude asks before running commands with external side effects.

### Control what Claude can do

Press

```
Shift+Tab
```

to cycle through permission modes:

- Default: Claude asks before file edits and shell commands
- Auto-accept edits: Claude edits files and runs common filesystem commands like

  ```
  mkdir
  ```

  and

  ```
  mv
  ```

  without asking, still asks for other commands
- Plan mode: Claude uses read-only tools only, creating a plan you can approve before execution
- Auto mode: Claude evaluates all actions with background safety checks. Currently a research preview

```
.claude/settings.json
```

so Claude doesn’t ask each time. This is useful for trusted commands like

```
npm test
```

or

```
git status
```

. Settings can be scoped from organization-wide policies down to personal preferences. See

[[Configure permissions - Claude Code Docs|Permissions]]for details.

## Work effectively with Claude Code

These tips help you get better results from Claude Code.

### Ask Claude Code for help

Claude Code can teach you how to use it. Ask questions like “how do I set up hooks?” or “what’s the best way to structure my CLAUDE.md?” and Claude will explain. Built-in commands also guide you through setup:

- ```
  /init
  ```

  walks you through creating a CLAUDE.md for your project
- ```
  /agents
  ```

  helps you configure custom subagents
- ```
  /doctor
  ```

  diagnoses common issues with your installation

### It’s a conversation

Claude Code is conversational. You don’t need perfect prompts. Start with what you want, then refine:

#### Interrupt and steer

You can interrupt Claude at any point. If it’s going down the wrong path, just type your correction and press Enter. Claude will stop what it’s doing and adjust its approach based on your input. You don’t have to wait for it to finish or start over.

### Be specific upfront

The more precise your initial prompt, the fewer corrections you’ll need. Reference specific files, mention constraints, and point to example patterns.

### Give Claude something to verify against

Claude performs better when it can check its own work. Include test cases, paste screenshots of expected UI, or define the output you want.

### Explore before implementing

For complex problems, separate research from coding. Use plan mode (

```
Shift+Tab
```

twice) to analyze the codebase first:

### Delegate, don’t dictate

Think of delegating to a capable colleague. Give context and direction, then trust Claude to figure out the details:

## What’s next

## Extend with features

Add Skills, MCP connections, and custom commands

## Common workflows

Step-by-step guides for typical tasks

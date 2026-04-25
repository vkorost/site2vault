---
title: Explore the context window - Claude Code Docs
source_url: https://code.claude.com/docs/en/context-window
description: An interactive simulation of how Claude Code's context window fills during
  a session. See what loads automatically, what each file read costs, and when rules
  an
---

[[Explore the context window - Claude Code Docs#What the timeline shows|the written breakdown]]for the same content as a list.

## What the timeline shows

The session walks through a realistic flow with representative token counts:

- Before you type anything: CLAUDE.md, auto memory, MCP tool names, and skill descriptions all load into context. Your own setup may add more here, like an [[Output styles - Claude Code Docs|output style]]or text from, which both go into the system prompt the same way.

  ```
  --append-system-prompt
  ```
- As Claude works: each file read adds to context, [[How Claude remembers your project - Claude Code Docs#Path-specific rules|path-scoped rules]]load automatically alongside matching files, and a[[Automate workflows with hooks - Claude Code Docs|PostToolUse hook]]fires after each edit.
- The follow-up prompt: a [[Create custom subagents - Claude Code Docs|subagent]]handles the research in its own separate context window, so the large file reads stay out of yours. Only the summary and a small metadata trailer come back.
- At the end:

  ```
  /compact
  ```

  replaces the conversation with a structured summary. Most startup content reloads automatically; the table below shows what happens to each mechanism.

## What survives compaction

When a long session compacts, Claude Code summarizes the conversation history to fit the context window. What happens to your instructions depends on how they were loaded:

MechanismAfter compactionSystem prompt and output styleUnchanged; not part of message historyProject-root CLAUDE.md and unscoped rulesRe-injected from diskAuto memoryRe-injected from diskRules with

```
paths:
```

frontmatterLost until a matching file is read againNested CLAUDE.md in subdirectoriesLost until a file in that subdirectory is read againInvoked skill bodiesRe-injected, capped at 5,000 tokens per skill and 25,000 tokens total; oldest dropped firstHooksNot applicable; hooks run as code, not context

```
paths:
```

frontmatter or move it to the project-root CLAUDE.md.
Skill bodies are re-injected after compaction, but large skills are truncated to fit the per-skill cap, and the oldest invoked skills are dropped once the total budget is exceeded. Truncation keeps the start of the file, so put the most important instructions near the top of

```
SKILL.md
```

.

## Check your own session

The visualization uses representative numbers. To see your actual context usage at any point, run

```
/context
```

for a live breakdown by category with optimization suggestions. Run

```
/memory
```

to check which CLAUDE.md and auto memory files loaded at startup.

## Related resources

For deeper coverage of the features shown in the timeline, see these pages:

- [[Extend Claude Code - Claude Code Docs|Extend Claude Code]]: when to use CLAUDE.md vs skills vs rules vs hooks vs MCP
- [[How Claude remembers your project - Claude Code Docs|Store instructions and memories]]: CLAUDE.md hierarchy and auto memory
- [[Create custom subagents - Claude Code Docs|Subagents]]: delegate research to a separate context window
- [[Best Practices for Claude Code - Claude Code Docs|Best practices]]: managing context as your primary constraint
- [[Manage costs effectively - Claude Code Docs#Reduce token usage|Reduce token usage]]: strategies for keeping context usage low

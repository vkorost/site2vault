---
title: How Claude remembers your project - Claude Code Docs
source_url: https://code.claude.com/docs/en/memory
description: Give Claude persistent instructions with CLAUDE.md files, and let Claude
  accumulate learnings automatically with auto memory.
---

- CLAUDE.md files: instructions you write to give Claude persistent context
- Auto memory: notes Claude writes itself based on your corrections and preferences

- [[How Claude remembers your project - Claude Code Docs|Write and organize CLAUDE.md files]]
- [[How Claude remembers your project - Claude Code Docs|Scope rules to specific file types]]with

  ```
  .claude/rules/
  ```
- [[How Claude remembers your project - Claude Code Docs#Auto memory|Configure auto memory]]so Claude takes notes automatically
- [[How Claude remembers your project - Claude Code Docs#Troubleshoot memory issues|Troubleshoot]]when instructions aren’t being followed

## CLAUDE.md vs auto memory

Claude Code has two complementary memory systems. Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration. The more specific and concise your instructions, the more consistently Claude follows them.

CLAUDE.md filesAuto memoryWho writes itYouClaudeWhat it containsInstructions and rulesLearnings and patternsScopeProject, user, or orgPer working treeLoaded intoEvery sessionEvery session (first 200 lines or 25KB)Use forCoding standards, workflows, project architectureBuild commands, debugging insights, preferences Claude discovers

[[Create custom subagents - Claude Code Docs#Enable persistent memory|subagent configuration]]for details.

## CLAUDE.md files

CLAUDE.md files are markdown files that give Claude persistent instructions for a project, your personal workflow, or your entire organization. You write these files in plain text; Claude reads them at the start of every session.

### When to add to CLAUDE.md

Treat CLAUDE.md as the place you write down what you’d otherwise re-explain. Add to it when:

- Claude makes the same mistake a second time
- A code review catches something Claude should have known about this codebase
- You type the same correction or clarification into chat that you typed last session
- A new teammate would need the same context to be productive

[[Extend Claude with skills - Claude Code Docs|skill]]or a

[[How Claude remembers your project - Claude Code Docs|path-scoped rule]]instead. The

[[Extend Claude Code - Claude Code Docs#Build your setup over time|extension overview]]covers when to use each mechanism.

### Choose where to put CLAUDE.md files

CLAUDE.md files can live in several locations, each with a different scope. More specific locations take precedence over broader ones.

ScopeLocationPurposeUse case examplesShared withManaged policy• macOS:

```
/Library/Application Support/ClaudeCode/CLAUDE.md
```

• Linux and WSL:

```
/etc/claude-code/CLAUDE.md
```

• Windows:

```
C:\Program Files\ClaudeCode\CLAUDE.md
```

Organization-wide instructions managed by IT/DevOpsCompany coding standards, security policies, compliance requirementsAll users in organizationProject instructions

```
./CLAUDE.md
```

or

```
./.claude/CLAUDE.md
```

Team-shared instructions for the projectProject architecture, coding standards, common workflowsTeam members via source controlUser instructions

```
~/.claude/CLAUDE.md
```

Personal preferences for all projectsCode styling preferences, personal tooling shortcutsJust you (all projects)Local instructions

```
./CLAUDE.local.md
```

Personal project-specific preferences; add to

```
.gitignore
```

Your sandbox URLs, preferred test dataJust you (current project)

[[How Claude remembers your project - Claude Code Docs|How CLAUDE.md files load]]for the full resolution order. For large projects, you can break instructions into topic-specific files using

[[How Claude remembers your project - Claude Code Docs|project rules]]. Rules let you scope instructions to specific file types or subdirectories.

### Set up a project CLAUDE.md

A project CLAUDE.md can be stored in either

```
./CLAUDE.md
```

or

```
./.claude/CLAUDE.md
```

. Create this file and add instructions that apply to anyone working on the project: build and test commands, coding standards, architectural decisions, naming conventions, and common workflows. These instructions are shared with your team through version control, so focus on project-level standards rather than personal preferences.

### Write effective instructions

CLAUDE.md files are loaded into the context window at the start of every session, consuming tokens alongside your conversation. The

[[Explore the context window - Claude Code Docs|context window visualization]]shows where CLAUDE.md loads relative to the rest of the startup context. Because they’re context rather than enforced configuration, how you write instructions affects how reliably Claude follows them. Specific, concise, well-structured instructions work best. Size: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence. If your instructions are growing large, use

[[How Claude remembers your project - Claude Code Docs#Path-specific rules|path-scoped rules]]so instructions load only when Claude works with matching files. You can also split content into

[[How Claude remembers your project - Claude Code Docs#Import additional files|imports]]for organization, though imported files still load and enter the context window at launch. Structure: use markdown headers and bullets to group related instructions. Claude scans structure the same way readers do: organized sections are easier to follow than dense paragraphs. Specificity: write instructions that are concrete enough to verify. For example:

- “Use 2-space indentation” instead of “Format code properly”
- “Run

  ```
  npm test
  ```

  before committing” instead of “Test your changes”
- “API handlers live in

  ```
  src/api/handlers/
  ```

  ” instead of “Keep files organized”

[[How Claude remembers your project - Claude Code Docs|periodically to remove outdated or conflicting instructions. In monorepos, use]]

```
.claude/rules/
```

[[How Claude remembers your project - Claude Code Docs|to skip CLAUDE.md files from other teams that aren’t relevant to your work.]]

```
claudeMdExcludes
```

### Import additional files

CLAUDE.md files can import additional files using

```
@path/to/import
```

syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them.
Both relative and absolute paths are allowed. Relative paths resolve relative to the file containing the import, not the working directory. Imported files can recursively import other files, with a maximum depth of five hops.
To pull in a README, package.json, and a workflow guide, reference them with

```
@
```

syntax anywhere in your CLAUDE.md:

```
CLAUDE.local.md
```

at the project root. It loads alongside

```
CLAUDE.md
```

and is treated the same way. Add

```
CLAUDE.local.md
```

to your

```
.gitignore
```

so it isn’t committed; running

```
/init
```

and choosing the personal option does this for you.
If you work across multiple git worktrees of the same repository, a gitignored

```
CLAUDE.local.md
```

only exists in the worktree where you created it. To share personal instructions across worktrees, import a file from your home directory instead:

[[How Claude remembers your project - Claude Code Docs|.]]

```
.claude/rules/
```

### AGENTS.md

Claude Code reads

```
CLAUDE.md
```

, not

```
AGENTS.md
```

. If your repository already uses

```
AGENTS.md
```

for other coding agents, create a

```
CLAUDE.md
```

that imports it so both tools read the same instructions without duplicating them. You can also add Claude-specific instructions below the import. Claude loads the imported file at session start, then appends the rest:

CLAUDE.md

### How CLAUDE.md files load

Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory along the way for

```
CLAUDE.md
```

and

```
CLAUDE.local.md
```

files. This means if you run Claude Code in

```
foo/bar/
```

, it loads instructions from

```
foo/bar/CLAUDE.md
```

,

```
foo/CLAUDE.md
```

, and any

```
CLAUDE.local.md
```

files alongside them.
All discovered files are concatenated into context rather than overriding each other. Within each directory,

```
CLAUDE.local.md
```

is appended after

```
CLAUDE.md
```

, so when instructions conflict, your personal notes are the last thing Claude reads at that level.
Claude also discovers

```
CLAUDE.md
```

and

```
CLAUDE.local.md
```

files in subdirectories under your current working directory. Instead of loading them at launch, they are included when Claude reads files in those subdirectories.
If you work in a large monorepo where other teams’ CLAUDE.md files get picked up, use

[[How Claude remembers your project - Claude Code Docs|to skip them. Block-level HTML comments (]]

```
claudeMdExcludes
```

```
<!-- maintainer notes -->
```

) in CLAUDE.md files are stripped before the content is injected into Claude’s context. Use them to leave notes for human maintainers without spending context tokens on them. Comments inside code blocks are preserved. When you open a CLAUDE.md file directly with the Read tool, comments remain visible.

#### Load from additional directories

The

```
--add-dir
```

flag gives Claude access to additional directories outside your main working directory. By default, CLAUDE.md files from these directories are not loaded.
To also load memory files from additional directories, set the

```
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD
```

environment variable:

```
CLAUDE.md
```

,

```
.claude/CLAUDE.md
```

,

```
.claude/rules/*.md
```

, and

```
CLAUDE.local.md
```

from the additional directory.

```
CLAUDE.local.md
```

is skipped if you exclude

```
local
```

from

[[CLI reference - Claude Code Docs|.]]

```
--setting-sources
```

### Organize rules with ``` .claude/rules/ ```

For larger projects, you can organize instructions into multiple files using the

```
.claude/rules/
```

directory. This keeps instructions modular and easier for teams to maintain. Rules can also be

[[How Claude remembers your project - Claude Code Docs#Path-specific rules|scoped to specific file paths]], so they only load into context when Claude works with matching files, reducing noise and saving context space.

Rules load into context every session or when matching files are opened. For task-specific instructions that don’t need to be in context all the time, use

[[Extend Claude with skills - Claude Code Docs|skills]]instead, which only load when you invoke them or when Claude determines they’re relevant to your prompt.

#### Set up rules

Place markdown files in your project’s

```
.claude/rules/
```

directory. Each file should cover one topic, with a descriptive filename like

```
testing.md
```

or

```
api-design.md
```

. All

```
.md
```

files are discovered recursively, so you can organize rules into subdirectories like

```
frontend/
```

or

```
backend/
```

:

[[How Claude remembers your project - Claude Code Docs#Path-specific rules|are loaded at launch with the same priority as]]

```
paths
```

frontmatter

```
.claude/CLAUDE.md
```

.

#### Path-specific rules

Rules can be scoped to specific files using YAML frontmatter with the

```
paths
```

field. These conditional rules only apply when Claude is working with files matching the specified patterns.

```
paths
```

field are loaded unconditionally and apply to all files. Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use.
Use glob patterns in the

```
paths
```

field to match files by extension, directory, or any combination:

PatternMatches

```
**/*.ts
```

All TypeScript files in any directory

```
src/**/*
```

All files under

```
src/
```

directory

```
*.md
```

Markdown files in the project root

```
src/components/*.tsx
```

React components in a specific directory

#### Share rules across projects with symlinks

The

```
.claude/rules/
```

directory supports symlinks, so you can maintain a shared set of rules and link them into multiple projects. Symlinks are resolved and loaded normally, and circular symlinks are detected and handled gracefully.
This example links both a shared directory and an individual file:

#### User-level rules

Personal rules in

```
~/.claude/rules/
```

apply to every project on your machine. Use them for preferences that aren’t project-specific:

### Manage CLAUDE.md for large teams

For organizations deploying Claude Code across teams, you can centralize instructions and control which CLAUDE.md files are loaded.

#### Deploy organization-wide CLAUDE.md

Organizations can deploy a centrally managed CLAUDE.md that applies to all users on a machine. This file cannot be excluded by individual settings.

Create the file at the managed policy location

- macOS:

  ```
  /Library/Application Support/ClaudeCode/CLAUDE.md
  ```
- Linux and WSL:

  ```
  /etc/claude-code/CLAUDE.md
  ```
- Windows:

  ```
  C:\Program Files\ClaudeCode\CLAUDE.md
  ```

Deploy with your configuration management system

Use MDM, Group Policy, Ansible, or similar tools to distribute the file across developer machines. See

[[Configure permissions - Claude Code Docs#Managed settings|managed settings]]for other organization-wide configuration options.

[[Claude Code settings - Claude Code Docs#Settings files|managed settings]]serve different purposes. Use settings for technical enforcement and CLAUDE.md for behavioral guidance:

ConcernConfigure inBlock specific tools, commands, or file pathsManaged settings:

```
permissions.deny
```

Enforce sandbox isolationManaged settings:

```
sandbox.enabled
```

Environment variables and API provider routingManaged settings:

```
env
```

Authentication method and organization lockManaged settings:

```
forceLoginMethod
```

,

```
forceLoginOrgUUID
```

Code style and quality guidelinesManaged CLAUDE.mdData handling and compliance remindersManaged CLAUDE.mdBehavioral instructions for ClaudeManaged CLAUDE.md

#### Exclude specific CLAUDE.md files

In large monorepos, ancestor CLAUDE.md files may contain instructions that aren’t relevant to your work. The

```
claudeMdExcludes
```

setting lets you skip specific files by path or glob pattern.
This example excludes a top-level CLAUDE.md and a rules directory from a parent folder. Add it to

```
.claude/settings.local.json
```

so the exclusion stays local to your machine:

```
claudeMdExcludes
```

at any

[[Claude Code settings - Claude Code Docs#Settings files|settings layer]]: user, project, local, or managed policy. Arrays merge across layers. Managed policy CLAUDE.md files cannot be excluded. This ensures organization-wide instructions always apply regardless of individual settings.

## Auto memory

Auto memory lets Claude accumulate knowledge across sessions without you writing anything. Claude saves notes for itself as it works: build commands, debugging insights, architecture notes, code style preferences, and workflow habits. Claude doesn’t save something every session. It decides what’s worth remembering based on whether the information would be useful in a future conversation.

Auto memory requires Claude Code v2.1.59 or later. Check your version with

```
claude --version
```

.

### Enable or disable auto memory

Auto memory is on by default. To toggle it, open

```
/memory
```

in a session and use the auto memory toggle, or set

```
autoMemoryEnabled
```

in your project settings:

```
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

.

### Storage location

Each project gets its own memory directory at

```
~/.claude/projects/<project>/memory/
```

. The

```
<project>
```

path is derived from the git repository, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead.
To store auto memory in a different location, set

```
autoMemoryDirectory
```

in your user or local settings:

```
.claude/settings.json
```

) to prevent a shared project from redirecting auto memory writes to sensitive locations.
The directory contains a

```
MEMORY.md
```

entrypoint and optional topic files:

```
MEMORY.md
```

acts as an index of the memory directory. Claude reads and writes files in this directory throughout your session, using

```
MEMORY.md
```

to keep track of what’s stored where.
Auto memory is machine-local. All worktrees and subdirectories within the same git repository share one auto memory directory. Files are not shared across machines or cloud environments.

### How it works

The first 200 lines of

```
MEMORY.md
```

, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start. Claude keeps

```
MEMORY.md
```

concise by moving detailed notes into separate topic files.
This limit applies only to

```
MEMORY.md
```

. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence.
Topic files like

```
debugging.md
```

or

```
patterns.md
```

are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information.
Claude reads and writes memory files during your session. When you see “Writing memory” or “Recalled memory” in the Claude Code interface, Claude is actively updating or reading from

```
~/.claude/projects/<project>/memory/
```

.

### Audit and edit your memory

Auto memory files are plain markdown you can edit or delete at any time. Run

[[How Claude remembers your project - Claude Code Docs|to browse and open memory files from within a session.]]

```
/memory
```

## View and edit with ``` /memory ```

The

```
/memory
```

command lists all CLAUDE.md, CLAUDE.local.md, and rules files loaded in your current session, lets you toggle auto memory on or off, and provides a link to open the auto memory folder. Select any file to open it in your editor.
When you ask Claude to remember something, like “always use pnpm, not npm” or “remember that the API tests require a local Redis instance,” Claude saves it to auto memory. To add instructions to CLAUDE.md instead, ask Claude directly, like “add this to CLAUDE.md,” or edit the file yourself via

```
/memory
```

.

## Troubleshoot memory issues

These are the most common issues with CLAUDE.md and auto memory, along with steps to debug them.

### Claude isn’t following my CLAUDE.md

CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there’s no guarantee of strict compliance, especially for vague or conflicting instructions. To debug:

- Run

  ```
  /memory
  ```

  to verify your CLAUDE.md and CLAUDE.local.md files are being loaded. If a file isn’t listed, Claude can’t see it.
- Check that the relevant CLAUDE.md is in a location that gets loaded for your session (see [[How Claude remembers your project - Claude Code Docs|Choose where to put CLAUDE.md files]]).
- Make instructions more specific. “Use 2-space indentation” works better than “format code nicely.”
- Look for conflicting instructions across CLAUDE.md files. If two files give different guidance for the same behavior, Claude may pick one arbitrarily.

[[CLI reference - Claude Code Docs|. This must be passed every invocation, so it’s better suited to scripts and automation than interactive use.]]

```
--append-system-prompt
```

### I don’t know what auto memory saved

Run

```
/memory
```

and select the auto memory folder to browse what Claude has saved. Everything is plain markdown you can read, edit, or delete.

### My CLAUDE.md is too large

Files over 200 lines consume more context and may reduce adherence. Use

[[How Claude remembers your project - Claude Code Docs#Path-specific rules|path-scoped rules]]to load instructions only when Claude works with matching files, or trim content that isn’t needed in every session. Splitting into

[[How Claude remembers your project - Claude Code Docs#Import additional files|helps organization but does not reduce context, since imported files load at launch.]]

```
@path
```

imports

### Instructions seem lost after ``` /compact ```

Project-root CLAUDE.md survives compaction: after

```
/compact
```

, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories are not re-injected automatically; they reload the next time Claude reads a file in that subdirectory.
If an instruction disappeared after compaction, it was either given only in conversation or lives in a nested CLAUDE.md that hasn’t reloaded yet. Add conversation-only instructions to CLAUDE.md to make them persist. See

[[Explore the context window - Claude Code Docs#What survives compaction|What survives compaction]]for the full breakdown. See

[[How Claude remembers your project - Claude Code Docs#Write effective instructions|Write effective instructions]]for guidance on size, structure, and specificity.

## Related resources

- [[Debug your configuration - Claude Code Docs|Debug your configuration]]: diagnose why CLAUDE.md or settings aren’t taking effect
- [[Extend Claude with skills - Claude Code Docs|Skills]]: package repeatable workflows that load on demand
- [[Claude Code settings - Claude Code Docs|Settings]]: configure Claude Code behavior with settings files
- [[Create custom subagents - Claude Code Docs#Enable persistent memory|Subagent memory]]: let subagents maintain their own auto memory

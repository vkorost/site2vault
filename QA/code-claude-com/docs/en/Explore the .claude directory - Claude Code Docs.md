---
title: Explore the .claude directory - Claude Code Docs
source_url: https://code.claude.com/docs/en/claude-directory
description: 'Where Claude Code reads CLAUDE.md, settings.json, hooks, skills, commands,
  subagents, rules, and auto memory. Explore the .claude directory in your project
  and '
---

```
~/.claude
```

in your home directory. Commit project files to git to share them with your team; files in

```
~/.claude
```

are personal configuration that applies across all your projects.
On Windows,

```
~/.claude
```

resolves to

```
%USERPROFILE%\.claude
```

. If you set

[[Environment variables - Claude Code Docs|, every]]

```
CLAUDE_CONFIG_DIR
```

```
~/.claude
```

path on this page lives under that directory instead.
Most users only edit

```
CLAUDE.md
```

and

```
settings.json
```

. The rest of the directory is optional: add skills, rules, or subagents as you need them.

## Explore the directory

Click files in the tree to see what each one does, when it loads, and an example.

## What’s not shown

The explorer covers files you author and edit. A few related files live elsewhere:

FileLocationPurpose

```
managed-settings.json
```

System-level, varies by OSEnterprise-enforced settings that you can’t override. See

```
CLAUDE.local.md
```

```
.gitignore
```

.

```
~/.claude/plugins
```

```
claude plugin
```

commands. Orphaned versions are deleted 7 days after a plugin update or uninstall. See [[Plugins reference - Claude Code Docs#Plugin caching and file resolution|plugin caching]].

```
~/.claude
```

also holds data Claude Code writes as you work: transcripts, prompt history, file snapshots, caches, and logs. See

[[Explore the .claude directory - Claude Code Docs#Application data|application data]]below.

## Choose the right file

Different kinds of customization live in different files. Use this table to find where a change belongs.

You want toEditScopeReferenceGive Claude project context and conventions

```
CLAUDE.md
```

project or global

```
settings.json
```

```
permissions
```

or

```
hooks
```

[[Configure permissions - Claude Code Docs|Permissions]],[[Hooks reference - Claude Code Docs|Hooks]]

```
settings.json
```

```
hooks
```

[[Hooks reference - Claude Code Docs|Hooks]]

```
settings.json
```

```
env
```

[[Claude Code settings - Claude Code Docs#Available settings|Settings]]

```
settings.local.json
```

[[Claude Code settings - Claude Code Docs#Settings files|Settings scopes]]

```
/name
```

```
skills/<name>/SKILL.md
```

[[Extend Claude with skills - Claude Code Docs|Skills]]

```
agents/*.md
```

[[Create custom subagents - Claude Code Docs|Subagents]]

```
.mcp.json
```

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP]]

```
output-styles/*.md
```

[[Output styles - Claude Code Docs|Output styles]]

## File reference

This table lists every file the explorer covers. Project-scope files live in your repo under

```
.claude/
```

(or at the root for

```
CLAUDE.md
```

,

```
.mcp.json
```

, and

```
.worktreeinclude
```

). Global-scope files live in

```
~/.claude/
```

and apply across all projects.

Several things can override what you put in these files:

- [[Configure server-managed settings - Claude Code Docs|Managed settings]]deployed by your organization take precedence over everything
- CLI flags like

  ```
  --permission-mode
  ```

  or

  ```
  --settings
  ```

  override

  ```
  settings.json
  ```

  for that session
- Some environment variables take precedence over their equivalent setting, but this varies: check the [[Environment variables - Claude Code Docs|environment variables reference]]for each one

[[Claude Code settings - Claude Code Docs#Settings precedence|settings precedence]]for the full order.

FileScopeCommitWhat it doesReference

```
CLAUDE.md
```

[[How Claude remembers your project - Claude Code Docs|Memory]]

```
rules/*.md
```

[[How Claude remembers your project - Claude Code Docs|Rules]]

```
settings.json
```

[[Claude Code settings - Claude Code Docs|Settings]]

```
settings.local.json
```

[[Claude Code settings - Claude Code Docs#Settings files|Settings scopes]]

```
.mcp.json
```

[[Connect Claude Code to tools via MCP - Claude Code Docs#MCP installation scopes|MCP scopes]]

```
.worktreeinclude
```

[[Common workflows - Claude Code Docs#Copy gitignored files to worktrees|Worktrees]]

```
skills/<name>/SKILL.md
```

```
/name
```

or auto-invoked[[Extend Claude with skills - Claude Code Docs|Skills]]

```
commands/*.md
```

[[Extend Claude with skills - Claude Code Docs|Skills]]

```
output-styles/*.md
```

[[Output styles - Claude Code Docs|Output styles]]

```
agents/*.md
```

[[Create custom subagents - Claude Code Docs|Subagents]]

```
agent-memory/<name>/
```

[[Create custom subagents - Claude Code Docs#Enable persistent memory|Persistent memory]]

```
~/.claude.json
```

[[Claude Code settings - Claude Code Docs#Global config settings|Global config]]

```
projects/<project>/memory/
```

[[How Claude remembers your project - Claude Code Docs#Auto memory|Auto memory]]

```
keybindings.json
```

[[Customize keyboard shortcuts - Claude Code Docs|Keybindings]]

```
themes/*.json
```

[[Configure your terminal for Claude Code - Claude Code Docs#Create a custom theme|Custom themes]]

## Troubleshoot configuration

If a setting, hook, or file isn’t taking effect, see

[[Debug your configuration - Claude Code Docs|Debug your configuration]]for the inspection commands and a symptom-first lookup table.

## Application data

Beyond the config you author,

```
~/.claude
```

holds data Claude Code writes during sessions. These files are plaintext. Anything that passes through a tool lands in a transcript on disk: file contents, command output, pasted text.

### Cleaned up automatically

Files in the paths below are deleted on startup once they’re older than

[[Claude Code settings - Claude Code Docs#Available settings|. The default is 30 days.]]

```
cleanupPeriodDays
```

Path under

```
~/.claude/
```

Contents

```
projects/<project>/<session>.jsonl
```

Full conversation transcript: every message, tool call, and tool result

```
projects/<project>/<session>/tool-results/
```

Large tool outputs spilled to separate files

```
file-history/<session>/
```

Pre-edit snapshots of files Claude changed, used for

```
plans/
```

[[Choose a permission mode - Claude Code Docs#Analyze before you edit with plan mode|plan mode]]

```
debug/
```

```
--debug
```

or run

```
/debug
```

```
paste-cache/
```

,

```
image-cache/
```

```
session-env/
```

```
tasks/
```

```
shell-snapshots/
```

```
backups/
```

```
~/.claude.json
```

taken before config migrations

### Kept until you delete them

The following paths are not covered by automatic cleanup and persist indefinitely.

Path under

```
~/.claude/
```

Contents

```
history.jsonl
```

Every prompt you’ve typed, with timestamp and project path. Used for up-arrow recall.

```
stats-cache.json
```

Aggregated token and cost counts shown by

```
/usage
```

```
todos/
```

Legacy per-session task lists. No longer written by current versions; safe to delete.

### Plaintext storage

Transcripts and history are not encrypted at rest. OS file permissions are the only protection. If a tool reads a

```
.env
```

file or a command prints a credential, that value is written to

```
projects/<project>/<session>.jsonl
```

. To reduce exposure:

- Lower

  ```
  cleanupPeriodDays
  ```

  to shorten how long transcripts are kept
- Set the environment variable to skip writing transcripts and prompt history in any mode. In non-interactive mode, you can instead pass

  ```
  CLAUDE_CODE_SKIP_PROMPT_HISTORY
  ```

  ```
  --no-session-persistence
  ```

  alongside

  ```
  -p
  ```

  , or set

  ```
  persistSession: false
  ```

  in the Agent SDK.
- Use [[Configure permissions - Claude Code Docs|permission rules]]to deny reads of credential files

### Clear local data

You can delete any of the application-data paths above at any time. New sessions are unaffected. The table below shows what you lose for past sessions.

DeleteYou lose

```
~/.claude/projects/
```

Resume, continue, and rewind for past sessions

```
~/.claude/history.jsonl
```

Up-arrow prompt recall

```
~/.claude/file-history/
```

Checkpoint restore for past sessions

```
~/.claude/stats-cache.json
```

Historical totals shown by

```
/usage
```

```
~/.claude/debug/
```

,

```
~/.claude/plans/
```

,

```
~/.claude/paste-cache/
```

,

```
~/.claude/image-cache/
```

,

```
~/.claude/session-env/
```

,

```
~/.claude/tasks/
```

,

```
~/.claude/shell-snapshots/
```

,

```
~/.claude/backups/
```

Nothing user-facing

```
~/.claude/todos/
```

Nothing. Legacy directory not written by current versions.

```
~/.claude.json
```

,

```
~/.claude/settings.json
```

, or

```
~/.claude/plugins/
```

: those hold your auth, preferences, and installed plugins.

## Related resources

- [[How Claude remembers your project - Claude Code Docs|Manage Claude’s memory]]: write and organize CLAUDE.md, rules, and auto memory
- [[Claude Code settings - Claude Code Docs|Configure settings]]: set permissions, hooks, environment variables, and model defaults
- [[Extend Claude with skills - Claude Code Docs|Create skills]]: build reusable prompts and workflows
- [[Create custom subagents - Claude Code Docs|Configure subagents]]: define specialized agents with their own context

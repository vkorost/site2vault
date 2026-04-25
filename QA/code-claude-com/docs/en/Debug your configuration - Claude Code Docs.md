---
title: Debug your configuration - Claude Code Docs
source_url: https://code.claude.com/docs/en/debug-your-config
description: Diagnose why CLAUDE.md, settings, hooks, MCP servers, or skills aren't
  taking effect. Use /context, /doctor, /hooks, and /mcp to see what actually loaded.
---

[[Troubleshooting - Claude Code Docs|Troubleshooting]]instead.

## See what loaded into context

The

```
/context
```

command shows everything occupying the context window for the current session, broken down by category: system prompt, memory files, skills, MCP tools, and conversation messages. Run it first to confirm whether your

```
CLAUDE.md
```

, rules, or skill descriptions are present at all.
For detail on a specific category, follow up with the dedicated command:

CommandShows

```
/memory
```

Which

```
CLAUDE.md
```

and rules files loaded, plus auto-memory entries

```
/skills
```

Available skills from project, user, and plugin sources

```
/agents
```

Configured subagents and their settings

```
/hooks
```

Active hook configurations

```
/mcp
```

Connected MCP servers and their status

```
/permissions
```

Resolved allow and deny rules currently in effect

```
/doctor
```

Configuration diagnostics: invalid keys, schema errors, installation health

```
/status
```

Active settings sources, including whether managed settings are in effect

```
/memory
```

, check its location against

[[How Claude remembers your project - Claude Code Docs|how CLAUDE.md files load]]. Subdirectory

```
CLAUDE.md
```

files load on demand when Claude reads a file in that directory with the Read tool, not at session start.
If

```
/memory
```

confirms the file loaded but Claude still isn’t following a particular instruction, the issue is likely how the instruction is written rather than whether it loaded. CLAUDE.md works well for the kinds of guidance you’d give a new teammate, such as project conventions, build commands, and where files belong.
Adherence drops when an instruction is vague enough to interpret multiple ways, when two files give conflicting direction, or when the file has grown long enough that individual rules get less attention.

[[How Claude remembers your project - Claude Code Docs#Write effective instructions|Write effective instructions]]covers the specificity, size, and structure patterns that keep adherence high.

CLAUDE.md and permissions solve different problems. CLAUDE.md tells Claude how your project works so it makes good decisions.

[[Configure permissions - Claude Code Docs|Permissions]]and[[Hooks reference - Claude Code Docs|hooks]]enforce limits regardless of what Claude decides. Use CLAUDE.md for “we do it this way here.” Use permissions or hooks for security boundaries and anything that must never happen, where you need a guarantee instead of guidance.

## Check resolved settings

Settings merge across managed, user, project, and local scopes. Managed settings always win when present. Among the rest, the closer scope overrides the broader one in the order local, then project, then user. Some settings can also be set by command-line flags or

[[Environment variables - Claude Code Docs|environment variables]], which act as another override layer. When a setting doesn’t seem to apply, the value you set is usually being overridden by another scope or an environment variable. Run

```
/doctor
```

to validate your configuration files and surface invalid keys or schema errors. Run

```
/status
```

to see which settings sources are active, including whether managed settings are in effect. To understand which scope wins for a given key, see

[[Claude Code settings - Claude Code Docs#How scopes interact|How scopes interact]].

## Check MCP servers

Run

```
/mcp
```

to see every configured server, its connection status, and whether you have approved it for the current project. A server can be defined correctly but still not provide tools for a few common reasons:

- Project-scoped servers in

  ```
  .mcp.json
  ```

  require a one-time approval. If the prompt was dismissed, the server stays disabled until you approve it from

  ```
  /mcp
  ```

  .
- A server that fails to start shows as failed in

  ```
  /mcp
  ```

  . Relative file paths in

  ```
  command
  ```

  or

  ```
  args
  ```

  are a frequent cause, since they resolve against the directory you launched Claude Code from rather than the location of

  ```
  .mcp.json
  ```

  .
- A server that shows as connected but lists zero tools has started successfully but isn’t returning a tool list. Select Reconnect from

  ```
  /mcp
  ```

  . If the count stays at zero, run

  ```
  claude --debug mcp
  ```

  to see the server’s stderr output.

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP]].

## Check hooks

Run

```
/hooks
```

to list every hook registered for the current session, grouped by event. If a hook you defined doesn’t appear, it isn’t being read: hooks go under the

```
"hooks"
```

key in a settings file, not in a standalone file.
If the hook appears but doesn’t fire, the matcher is the usual cause. The

```
matcher
```

field is a single string that uses

```
|
```

to match multiple tool names, for example

```
"Edit|Write"
```

. A misspelled tool name fails silently because the matcher never matches. An array value is a schema error: Claude Code shows a settings error notice,

```
/doctor
```

reports the validation failure, and the hook entry is dropped so it won’t appear in

```
/hooks
```

.
Edits to

```
settings.json
```

take effect in the running session after a brief file-stability delay. You don’t need to restart. If

```
/hooks
```

still shows the old definition a few seconds after saving, run

```
/hooks
```

again to refresh the view.
If

```
/hooks
```

shows the hook but it still does not fire, the next step is to watch hook evaluation live. Start a session with

```
claude --debug hooks
```

and trigger the tool call. The debug log records each event, which matchers were checked, and the hook’s exit code and output. See

[[Hooks reference - Claude Code Docs#Debug hooks|Debug hooks]]for the log format and

[[Automate workflows with hooks - Claude Code Docs#Limitations and troubleshooting|hooks troubleshooting]]for common failure patterns.

## Common causes

Most configuration surprises trace back to a small set of location and syntax rules. Check these before assuming a bug:

SymptomCauseFixHook never fires

```
matcher
```

is a JSON array instead of a stringUse a single string with

```
|
```

to match multiple tools, for example

```
"Edit|Write"
```

. SeeHook never fires

```
matcher
```

value is lowercase, for example

```
"bash"
```

Matching is case-sensitive. Tool names are capitalized:

```
Bash
```

,

```
Edit
```

,

```
Write
```

,

```
Read
```

.Hook never firesHooks are in a standalone

```
.claude/hooks.json
```

fileThere is no standalone hooks file. Define hooks under the

```
"hooks"
```

key in

```
settings.json
```

. SeePermissions, hooks, or env set globally are ignoredConfiguration was added to

```
~/.claude.json
```

```
~/.claude.json
```

holds app state and UI toggles.

```
permissions
```

,

```
hooks
```

, and

```
env
```

belong in

```
~/.claude/settings.json
```

. These are two different files.A

```
settings.json
```

value seems ignoredThe same key is set in

```
settings.local.json
```

```
settings.local.json
```

overrides

```
settings.json
```

, and both override

```
~/.claude/settings.json
```

. SeeSkill doesn’t appear in

```
/skills
```

Skill file is at

```
.claude/skills/name.md
```

instead of in a folderUse a folder with

```
SKILL.md
```

inside:

```
.claude/skills/name/SKILL.md
```

.Skill appears in

```
/skills
```

but Claude never invokes itSkill has

```
disable-model-invocation: true
```

in its frontmatter, or its description doesn’t match how you phrase the requestCheck the badge in

```
/skills
```

: a “user-only” label means Claude won’t trigger it on its own. SeeSubdirectory

```
CLAUDE.md
```

instructions seem ignoredSubdirectory files load on demand, not at session startThey load when Claude reads a file in that directory with the Read tool, not at launch and not when writing or creating files there. See

```
CLAUDE.md
```

instructions[[Create custom subagents - Claude Code Docs|subagent configuration]].

```
SessionEnd
```

hook configured

```
SessionStart
```

and

```
SessionEnd
```

both exist. See the [[Hooks reference - Claude Code Docs#Hook events|hook events list]].

```
.mcp.json
```

never load

```
.claude/
```

or uses Claude Desktop’s config format

```
.mcp.json
```

, not inside

```
.claude/
```

. See [[Connect Claude Code to tools via MCP - Claude Code Docs|MCP configuration]].

```
/mcp
```

to see status and approve.

```
command
```

or

```
args
```

uses a relative file path

```
PATH
```

like

```
npx
```

or

```
uvx
```

work as-is.

```
settings.json
```

```
env
```

, which doesn’t propagate to MCP child processes

```
env
```

inside

```
.mcp.json
```

instead.

```
Bash(rm *)
```

deny rule doesn’t block

```
/bin/rm
```

or

```
find -delete
```

[[Automate workflows with hooks - Claude Code Docs|PreToolUse hook]]or the[[Sandboxing - Claude Code Docs|sandbox]]for a hard guarantee.

## Related resources

For full reference on each configuration surface, see the dedicated page:

- : every config file location and what reads it

  ```
  .claude
  ```

  directory reference
- [[Claude Code settings - Claude Code Docs|Settings]]: precedence order and the full key list
- [[Hooks reference - Claude Code Docs|Hooks reference]]: event names, payloads, and

  ```
  --debug hooks
  ```

  output format
- [[Connect Claude Code to tools via MCP - Claude Code Docs|MCP]]: server configuration, approval, and

  ```
  /mcp
  ```

  output
- [[Troubleshooting - Claude Code Docs|Troubleshooting]]:

  ```
  claude doctor
  ```

  , platform issues, and installation problems

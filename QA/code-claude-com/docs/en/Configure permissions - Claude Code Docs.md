---
title: Configure permissions - Claude Code Docs
source_url: https://code.claude.com/docs/en/permissions
description: Control what Claude Code can access and do with fine-grained permission
  rules, modes, and managed policies.
---

## Permission system

Claude Code uses a tiered permission system to balance power and safety:

Tool typeExampleApproval required”Yes, don’t ask again” behaviorRead-onlyFile reads, GrepNoN/ABash commandsShell executionYesPermanently per project directory and commandFile modificationEdit/write filesYesUntil session end

## Manage permissions

You can view and manage Claude Code’s tool permissions with

```
/permissions
```

. This UI lists all permission rules and the settings.json file they are sourced from.

- Allow rules let Claude Code use the specified tool without manual approval.
- Ask rules prompt for confirmation whenever Claude Code tries to use the specified tool.
- Deny rules prevent Claude Code from using the specified tool.

## Permission modes

Claude Code supports several permission modes that control how tools are approved. See

[[Choose a permission mode - Claude Code Docs|Permission modes]]for when to use each one. Set the

```
defaultMode
```

in your

[[Claude Code settings - Claude Code Docs#Settings files|settings files]]:

ModeDescription

```
default
```

Standard behavior: prompts for permission on first use of each tool

```
acceptEdits
```

Automatically accepts file edits and common filesystem commands (

```
mkdir
```

,

```
touch
```

,

```
mv
```

,

```
cp
```

, etc.) for paths in the working directory or

```
additionalDirectories
```

```
plan
```

Plan Mode: Claude can analyze but not modify files or execute commands

```
auto
```

Auto-approves tool calls with background safety checks that verify actions align with your request. Currently a research preview

```
dontAsk
```

Auto-denies tools unless pre-approved via

```
/permissions
```

or

```
permissions.allow
```

rules

```
bypassPermissions
```

Skips permission prompts except for writes to protected directories (see warning below)

```
bypassPermissions
```

or

```
auto
```

mode from being used, set

```
permissions.disableBypassPermissionsMode
```

or

```
permissions.disableAutoMode
```

to

```
"disable"
```

in any

[[Claude Code settings - Claude Code Docs#Settings files|settings file]]. These are most useful in

[[Configure permissions - Claude Code Docs#Managed settings|managed settings]]where they cannot be overridden.

## Permission rule syntax

Permission rules follow the format

```
Tool
```

or

```
Tool(specifier)
```

.

### Match all uses of a tool

To match all uses of a tool, use just the tool name without parentheses:

RuleEffect

```
Bash
```

Matches all Bash commands

```
WebFetch
```

Matches all web fetch requests

```
Read
```

Matches all file reads

```
Bash(*)
```

is equivalent to

```
Bash
```

and matches all Bash commands.

### Use specifiers for fine-grained control

Add a specifier in parentheses to match specific tool uses:

RuleEffect

```
Bash(npm run build)
```

Matches the exact command

```
npm run build
```

```
Read(./.env)
```

Matches reading the

```
.env
```

file in the current directory

```
WebFetch(domain:example.com)
```

Matches fetch requests to example.com

### Wildcard patterns

Bash rules support glob patterns with

```
*
```

. Wildcards can appear at any position in the command. This configuration allows npm and git commit commands while blocking git push:

```
*
```

matters:

```
Bash(ls *)
```

matches

```
ls -la
```

but not

```
lsof
```

, while

```
Bash(ls*)
```

matches both. The

```
:*
```

suffix is an equivalent way to write a trailing wildcard, so

```
Bash(ls:*)
```

matches the same commands as

```
Bash(ls *)
```

.
The permission dialog writes the space-separated form when you select “Yes, don’t ask again” for a command prefix. The

```
:*
```

form is only recognized at the end of a pattern. In a pattern like

```
Bash(git:* push)
```

, the colon is treated as a literal character and won’t match git commands.

## Tool-specific permission rules

### Bash

Bash permission rules support wildcard matching with

```
*
```

. Wildcards can appear at any position in the command, including at the beginning, middle, or end:

- ```
  Bash(npm run build)
  ```

  matches the exact Bash command

  ```
  npm run build
  ```
- ```
  Bash(npm run test *)
  ```

  matches Bash commands starting with

  ```
  npm run test
  ```
- ```
  Bash(npm *)
  ```

  matches any command starting with

  ```
  npm
  ```
- ```
  Bash(* install)
  ```

  matches any command ending with

  ```
  install
  ```
- ```
  Bash(git * main)
  ```

  matches commands like

  ```
  git checkout main
  ```

  and

  ```
  git log --oneline main
  ```

```
*
```

matches any sequence of characters including spaces, so one wildcard can span multiple arguments.

```
Bash(git *)
```

matches

```
git log --oneline --all
```

, and

```
Bash(git * main)
```

matches

```
git push origin main
```

as well as

```
git merge main
```

.
When

```
*
```

appears at the end with a space before it (like

```
Bash(ls *)
```

), it enforces a word boundary, requiring the prefix to be followed by a space or end-of-string. For example,

```
Bash(ls *)
```

matches

```
ls -la
```

but not

```
lsof
```

. In contrast,

```
Bash(ls*)
```

without a space matches both

```
ls -la
```

and

```
lsof
```

because there’s no word boundary constraint.

#### Compound commands

When you approve a compound command with “Yes, don’t ask again”, Claude Code saves a separate rule for each subcommand that requires approval, rather than a single rule for the full compound string. For example, approving

```
git status && npm test
```

saves a rule for

```
npm test
```

, so future

```
npm test
```

invocations are recognized regardless of what precedes the

```
&&
```

. Subcommands like

```
cd
```

into a subdirectory generate their own Read rule for that path. Up to 5 rules may be saved for a single compound command.

#### Process wrappers

Before matching Bash rules, Claude Code strips a fixed set of process wrappers so a rule like

```
Bash(npm test *)
```

also matches

```
timeout 30 npm test
```

. The recognized wrappers are

```
timeout
```

,

```
time
```

,

```
nice
```

,

```
nohup
```

, and

```
stdbuf
```

.
Bare

```
xargs
```

is also stripped, so

```
Bash(grep *)
```

matches

```
xargs grep pattern
```

. Stripping applies only when

```
xargs
```

has no flags: an invocation like

```
xargs -n1 grep pattern
```

is matched as an

```
xargs
```

command, so rules written for the inner command do not cover it.
This wrapper list is built in and is not configurable. Development environment runners such as

```
direnv exec
```

,

```
devbox run
```

,

```
mise exec
```

,

```
npx
```

, and

```
docker exec
```

are not in the list. Because these tools execute their arguments as a command, a rule like

```
Bash(devbox run *)
```

matches whatever comes after

```
run
```

, including

```
devbox run rm -rf .
```

. To approve work inside an environment runner, write a specific rule that includes both the runner and the inner command, such as

```
Bash(devbox run npm test)
```

. Add one rule per inner command you want to allow.
Exec wrappers such as

```
watch
```

,

```
setsid
```

,

```
ionice
```

, and

```
flock
```

always prompt and cannot be auto-approved by a prefix rule like

```
Bash(watch *)
```

. The same applies to

```
find
```

with

```
-exec
```

or

```
-delete
```

: a

```
Bash(find *)
```

rule does not cover these forms. To approve a specific invocation, write an exact-match rule for the full command string.

#### Read-only commands

Claude Code recognizes a built-in set of Bash commands as read-only and runs them without a permission prompt in every mode. These include

```
ls
```

,

```
cat
```

,

```
head
```

,

```
tail
```

,

```
grep
```

,

```
find
```

,

```
wc
```

,

```
diff
```

,

```
stat
```

,

```
du
```

,

```
cd
```

, and read-only forms of

```
git
```

. The set is not configurable; to require a prompt for one of these commands, add an

```
ask
```

or

```
deny
```

rule for it.
Unquoted glob patterns are permitted for commands whose every flag is read-only, so

```
ls *.ts
```

and

```
wc -l src/*.py
```

run without a prompt. Commands with write-capable or exec-capable flags, such as

```
find
```

,

```
sort
```

,

```
sed
```

, and

```
git
```

, still prompt when an unquoted glob is present because the glob could expand to a flag like

```
-delete
```

.
A

```
cd
```

into a path inside your working directory or an

[[Configure permissions - Claude Code Docs#Working directories|additional directory]]is also read-only. A compound command like

```
cd packages/api && ls
```

runs without a prompt when each part qualifies on its own. Combining

```
cd
```

with

```
git
```

in one compound command always prompts, regardless of the target directory.

### Read and Edit

```
Edit
```

rules apply to all built-in tools that edit files. Claude makes a best-effort attempt to apply

```
Read
```

rules to all built-in tools that read files like Grep and Glob.
Read and Edit rules both follow the

[gitignore](https://git-scm.com/docs/gitignore)specification with four distinct pattern types:

PatternMeaningExampleMatches

```
//path
```

Absolute path from filesystem root

```
Read(//Users/alice/secrets/**)
```

```
/Users/alice/secrets/**
```

```
~/path
```

Path from home directory

```
Read(~/Documents/*.pdf)
```

```
/Users/alice/Documents/*.pdf
```

```
/path
```

Path relative to project root

```
Edit(/src/**/*.ts)
```

```
<project root>/src/**/*.ts
```

```
path
```

or

```
./path
```

Path relative to current directory

```
Read(*.env)
```

```
<cwd>/*.env
```

```
C:\Users\alice
```

becomes

```
/c/Users/alice
```

, so use

```
//c/**/.env
```

to match

```
.env
```

files anywhere on that drive. To match across all drives, use

```
//**/.env
```

.
Examples:

- ```
  Edit(/docs/**)
  ```

  : edits in

  ```
  <project>/docs/
  ```

  (NOT

  ```
  /docs/
  ```

  and NOT

  ```
  <project>/.claude/docs/
  ```

  )
- ```
  Read(~/.zshrc)
  ```

  : reads your home directory’s

  ```
  .zshrc
  ```
- ```
  Edit(//tmp/scratch.txt)
  ```

  : edits the absolute path

  ```
  /tmp/scratch.txt
  ```
- ```
  Read(src/**)
  ```

  : reads from

  ```
  <current-directory>/src/
  ```

In gitignore patterns,

```
*
```

matches files in a single directory while

```
**
```

matches recursively across directories. To allow all file access, use just the tool name without parentheses:

```
Read
```

,

```
Edit
```

, or

```
Write
```

.

- Allow rules: apply only when both the symlink path and its target match. A symlink inside an allowed directory that points outside it still prompts you.
- Deny rules: apply when either the symlink path or its target matches. A symlink that points to a denied file is itself denied.

```
Read(./project/**)
```

allowed and

```
Read(~/.ssh/**)
```

denied, a symlink at

```
./project/key
```

pointing to

```
~/.ssh/id_rsa
```

is blocked: the target fails the allow rule and matches the deny rule.

### WebFetch

- ```
  WebFetch(domain:example.com)
  ```

  matches fetch requests to example.com

### MCP

- ```
  mcp__puppeteer
  ```

  matches any tool provided by the

  ```
  puppeteer
  ```

  server (name configured in Claude Code)
- ```
  mcp__puppeteer__*
  ```

  wildcard syntax that also matches all tools from the

  ```
  puppeteer
  ```

  server
- ```
  mcp__puppeteer__puppeteer_navigate
  ```

  matches the

  ```
  puppeteer_navigate
  ```

  tool provided by the

  ```
  puppeteer
  ```

  server

### Agent (subagents)

Use

```
Agent(AgentName)
```

rules to control which

[[Create custom subagents - Claude Code Docs|subagents]]Claude can use:

- ```
  Agent(Explore)
  ```

  matches the Explore subagent
- ```
  Agent(Plan)
  ```

  matches the Plan subagent
- ```
  Agent(my-custom-agent)
  ```

  matches a custom subagent named

  ```
  my-custom-agent
  ```

```
deny
```

array in your settings or use the

```
--disallowedTools
```

CLI flag to disable specific agents. To disable the Explore agent:

## Extend permissions with hooks

[[Automate workflows with hooks - Claude Code Docs|Claude Code hooks]]provide a way to register custom shell commands to perform permission evaluation at runtime. When Claude Code makes a tool call, PreToolUse hooks run before the permission prompt. The hook output can deny the tool call, force a prompt, or skip the prompt to let the call proceed. Hook decisions do not bypass permission rules. Deny and ask rules are evaluated regardless of what a PreToolUse hook returns, so a matching deny rule blocks the call and a matching ask rule still prompts even when the hook returned

```
"allow"
```

or

```
"ask"
```

. This preserves the deny-first precedence described in

[[Configure permissions - Claude Code Docs#Manage permissions|Manage permissions]], including deny rules set in managed settings. A blocking hook also takes precedence over allow rules. A hook that exits with code 2 stops the tool call before permission rules are evaluated, so the block applies even when an allow rule would otherwise let the call proceed. To run all Bash commands without prompts except for a few you want blocked, add

```
"Bash"
```

to your allow list and register a PreToolUse hook that rejects those specific commands. See

[[Automate workflows with hooks - Claude Code Docs#Block edits to protected files|Block edits to protected files]]for a hook script you can adapt.

## Working directories

By default, Claude has access to files in the directory where it was launched. You can extend this access:

- During startup: use

  ```
  --add-dir <path>
  ```

  CLI argument
- During session: use

  ```
  /add-dir
  ```

  command
- Persistent configuration: add to

  ```
  additionalDirectories
  ```

  in[[Claude Code settings - Claude Code Docs#Settings files|settings files]]

### Additional directories grant file access, not configuration

Adding a directory extends where Claude can read and edit files. It does not make that directory a full configuration root: most

```
.claude/
```

configuration is not discovered from additional directories, though a few types are loaded as exceptions.
The following configuration types are loaded from

```
--add-dir
```

directories:

ConfigurationLoaded from

```
--add-dir
```

```
.claude/skills/
```

```
.claude/settings.json
```

```
enabledPlugins
```

and

```
extraKnownMarketplaces
```

only[[How Claude remembers your project - Claude Code Docs|CLAUDE.md]]files,

```
.claude/rules/
```

, and

```
CLAUDE.local.md
```

```
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
```

is set.

```
CLAUDE.local.md
```

additionally requires the

```
local
```

setting source, which is enabled by default

```
~/.claude/
```

, and managed settings. To share that configuration across projects, use one of these approaches:

- User-level configuration: place files in

  ```
  ~/.claude/agents/
  ```

  ,

  ```
  ~/.claude/output-styles/
  ```

  , or

  ```
  ~/.claude/settings.json
  ```

  to make them available in every project
- Plugins: package and distribute configuration as a [[Create plugins - Claude Code Docs|plugin]]that teams can install
- Launch from the config directory: run Claude Code from the directory containing the

  ```
  .claude/
  ```

  configuration you want

## How permissions interact with sandboxing

Permissions and

[[Sandboxing - Claude Code Docs|sandboxing]]are complementary security layers:

- Permissions control which tools Claude Code can use and which files or domains it can access. They apply to all tools (Bash, Read, Edit, WebFetch, MCP, and others).
- Sandboxing provides OS-level enforcement that restricts the Bash tool’s filesystem and network access. It applies only to Bash commands and their child processes.

- Permission deny rules block Claude from even attempting to access restricted resources
- Sandbox restrictions prevent Bash commands from reaching resources outside defined boundaries, even if a prompt injection bypasses Claude’s decision-making
- Filesystem restrictions in the sandbox use Read and Edit deny rules, not separate sandbox configuration
- Network restrictions combine WebFetch permission rules with the sandbox’s

  ```
  allowedDomains
  ```

  and

  ```
  deniedDomains
  ```

  lists

```
autoAllowBashIfSandboxed: true
```

, which is the default, sandboxed Bash commands run without prompting even if your permissions include

```
ask: Bash(*)
```

. The sandbox boundary substitutes for the per-command prompt. Explicit deny rules still apply, and

```
rm
```

or

```
rmdir
```

commands that target

```
/
```

, your home directory, or other critical system paths still trigger a prompt. See

[[Sandboxing - Claude Code Docs#Sandbox modes|sandbox modes]]to change this behavior.

## Managed settings

For organizations that need centralized control over Claude Code configuration, administrators can deploy managed settings that cannot be overridden by user or project settings. These policy settings follow the same format as regular settings files and can be delivered through MDM/OS-level policies, managed settings files, or

[[Configure server-managed settings - Claude Code Docs|server-managed settings]]. See

[[Claude Code settings - Claude Code Docs#Settings files|settings files]]for delivery mechanisms and file locations.

### Managed-only settings

The following settings are only read from managed settings. Placing them in user or project settings files has no effect.

SettingDescription

```
allowedChannelPlugins
```

Allowlist of channel plugins that may push messages. Replaces the default Anthropic allowlist when set. Requires

```
channelsEnabled: true
```

. See

```
allowManagedHooksOnly
```

When

```
true
```

, only managed hooks, SDK hooks, and hooks from plugins force-enabled in managed settings

```
enabledPlugins
```

are loaded. User, project, and all other plugin hooks are blocked

```
allowManagedMcpServersOnly
```

When

```
true
```

, only

```
allowedMcpServers
```

from managed settings are respected.

```
deniedMcpServers
```

still merges from all sources. See

```
allowManagedPermissionRulesOnly
```

When

```
true
```

, prevents user and project settings from defining

```
allow
```

,

```
ask
```

, or

```
deny
```

permission rules. Only rules in managed settings apply

```
blockedMarketplaces
```

Blocklist of marketplace sources. Blocked sources are checked before downloading, so they never touch the filesystem. See

```
channelsEnabled
```

[[Push events into a running session with channels - Claude Code Docs|channels]]for Team and Enterprise users. Unset or

```
false
```

blocks channel message delivery regardless of what users pass to

```
--channels
```

```
forceRemoteSettingsRefresh
```

```
true
```

, blocks CLI startup until remote managed settings are freshly fetched and exits if the fetch fails. See [[Configure server-managed settings - Claude Code Docs#Enforce fail-closed startup|fail-closed enforcement]]

```
pluginTrustMessage
```

```
sandbox.filesystem.allowManagedReadPathsOnly
```

```
true
```

, only

```
filesystem.allowRead
```

paths from managed settings are respected.

```
denyRead
```

still merges from all sources

```
sandbox.network.allowManagedDomainsOnly
```

```
true
```

, only

```
allowedDomains
```

and

```
WebFetch(domain:...)
```

allow rules from managed settings are respected. Non-allowed domains are blocked automatically without prompting the user. Denied domains still merge from all sources

```
strictKnownMarketplaces
```

[[Create and distribute a plugin marketplace - Claude Code Docs#Managed marketplace restrictions|managed marketplace restrictions]]

```
wslInheritsWindowsSettings
```

```
true
```

in the Windows HKLM registry key or

```
C:\Program Files\ClaudeCode\managed-settings.json
```

, WSL reads managed settings from the Windows policy chain in addition to

```
/etc/claude-code
```

. See [[Claude Code settings - Claude Code Docs#Settings files|Settings files]]

```
disableBypassPermissionsMode
```

is typically placed in managed settings to enforce organizational policy, but it works from any scope. A user can set it in their own settings to lock themselves out of bypass mode.

Access to

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]and[[Use Claude Code on the web - Claude Code Docs|web sessions]]is not controlled by a managed settings key. On Team and Enterprise plans, an admin enables or disables these features in[Claude Code admin settings](https://claude.ai/admin-settings/claude-code).

## Settings precedence

Permission rules follow the same

[[Claude Code settings - Claude Code Docs#Settings precedence|settings precedence]]as all other Claude Code settings:

- Managed settings: cannot be overridden by any other level, including command line arguments
- Command line arguments: temporary session overrides
- Local project settings (

  ```
  .claude/settings.local.json
  ```

  )
- Shared project settings (

  ```
  .claude/settings.json
  ```

  )
- User settings (

  ```
  ~/.claude/settings.json
  ```

  )

```
--allowedTools
```

, and

```
--disallowedTools
```

can add restrictions beyond what managed settings define.
If a permission is allowed in user settings but denied in project settings, the project setting takes precedence and the permission is blocked.

## Example configurations

This

[repository](https://github.com/anthropics/claude-code/tree/main/examples/settings)includes starter settings configurations for common deployment scenarios. Use these as starting points and adjust them to fit your needs.

## See also

- [[Claude Code settings - Claude Code Docs|Settings]]: complete configuration reference including the permission settings table
- [[Configure auto mode - Claude Code Docs|Configure auto mode]]: tell the auto mode classifier which infrastructure your organization trusts
- [[Sandboxing - Claude Code Docs|Sandboxing]]: OS-level filesystem and network isolation for Bash commands
- [[Authentication - Claude Code Docs|Authentication]]: set up user access to Claude Code
- [[Security - Claude Code Docs|Security]]: security safeguards and best practices
- [[Automate workflows with hooks - Claude Code Docs|Hooks]]: automate workflows and extend permission evaluation

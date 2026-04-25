---
title: Claude Code settings - Claude Code Docs
source_url: https://code.claude.com/docs/en/settings
description: Configure Claude Code with global and project-level settings, and environment
  variables.
---

```
/config
```

command when using the interactive REPL, which opens a tabbed Settings interface where you can view status information and modify configuration options.

## Configuration scopes

Claude Code uses a scope system to determine where configurations apply and who they’re shared with. Understanding scopes helps you decide how to configure Claude Code for personal use, team collaboration, or enterprise deployment.

### Available scopes

ScopeLocationWho it affectsShared with team?ManagedServer-managed settings, plist / registry, or system-level

```
managed-settings.json
```

All users on the machineYes (deployed by IT)User

```
~/.claude/
```

directoryYou, across all projectsNoProject

```
.claude/
```

in repositoryAll collaborators on this repositoryYes (committed to git)Local

```
.claude/settings.local.json
```

You, in this repository onlyNo (gitignored)

### When to use each scope

Managed scope is for:

- Security policies that must be enforced organization-wide
- Compliance requirements that can’t be overridden
- Standardized configurations deployed by IT/DevOps

- Personal preferences you want everywhere (themes, editor settings)
- Tools and plugins you use across all projects
- API keys and authentication (stored securely)

- Team-shared settings (permissions, hooks, MCP servers)
- Plugins the whole team should have
- Standardizing tooling across collaborators

- Personal overrides for a specific project
- Testing configurations before sharing with the team
- Machine-specific settings that won’t work for others

### How scopes interact

When the same setting is configured in multiple scopes, more specific scopes take precedence:

- Managed (highest) - can’t be overridden by anything
- Command line arguments - temporary session overrides
- Local - overrides project and user settings
- Project - overrides user settings
- User (lowest) - applies when nothing else specifies the setting

### What uses scopes

Scopes apply to many Claude Code features:

FeatureUser locationProject locationLocal locationSettings

```
~/.claude/settings.json
```

```
.claude/settings.json
```

```
.claude/settings.local.json
```

Subagents

```
~/.claude/agents/
```

```
.claude/agents/
```

NoneMCP servers

```
~/.claude.json
```

```
.mcp.json
```

```
~/.claude.json
```

(per-project)Plugins

```
~/.claude/settings.json
```

```
.claude/settings.json
```

```
.claude/settings.local.json
```

CLAUDE.md

```
~/.claude/CLAUDE.md
```

```
CLAUDE.md
```

or

```
.claude/CLAUDE.md
```

```
CLAUDE.local.md
```

## Settings files

The

```
settings.json
```

file is the official mechanism for configuring Claude
Code through hierarchical settings:

- User settings are defined in

  ```
  ~/.claude/settings.json
  ```

  and apply to all projects.
- Project settings are saved in your project directory:
  - ```
    .claude/settings.json
    ```

    for settings that are checked into source control and shared with your team
  - ```
    .claude/settings.local.json
    ```

    for settings that are not checked in, useful for personal preferences and experimentation. Claude Code will configure git to ignore

    ```
    .claude/settings.local.json
    ```

    when it is created.
- Managed settings: For organizations that need centralized control, Claude Code supports multiple delivery mechanisms for managed settings. All use the same JSON format and cannot be overridden by user or project settings:
  - Server-managed settings: delivered from Anthropic’s servers via the Claude.ai admin console. See [[Configure server-managed settings - Claude Code Docs|server-managed settings]].
  - MDM/OS-level policies: delivered through native device management on macOS and Windows:
    - macOS:

      ```
      com.anthropic.claudecode
      ```

      managed preferences domain. The plist’s top-level keys mirror

      ```
      managed-settings.json
      ```

      , with nested settings as dictionaries and arrays as plist arrays. Deploy via configuration profiles in Jamf, Iru (Kandji), or similar MDM tools.
    - Windows:

      ```
      HKLM\SOFTWARE\Policies\ClaudeCode
      ```

      registry key with a

      ```
      Settings
      ```

      value (REG\_SZ or REG\_EXPAND\_SZ) containing JSON (deployed via Group Policy or Intune)
    - Windows (user-level):

      ```
      HKCU\SOFTWARE\Policies\ClaudeCode
      ```

      (lowest policy priority, only used when no admin-level source exists)
  - macOS:
  - File-based:

    ```
    managed-settings.json
    ```

    and

    ```
    managed-mcp.json
    ```

    deployed to system directories:
    - macOS:

      ```
      /Library/Application Support/ClaudeCode/
      ```
    - Linux and WSL:

      ```
      /etc/claude-code/
      ```
    - Windows:

      ```
      C:\Program Files\ClaudeCode\
      ```

    ```
    managed-settings.d/
    ```

    in the same system directory alongside

    ```
    managed-settings.json
    ```

    . This lets separate teams deploy independent policy fragments without coordinating edits to a single file. Following the systemd convention,

    ```
    managed-settings.json
    ```

    is merged first as the base, then all

    ```
    *.json
    ```

    files in the drop-in directory are sorted alphabetically and merged on top. Later files override earlier ones for scalar values; arrays are concatenated and de-duplicated; objects are deep-merged. Hidden files starting with

    ```
    .
    ```

    are ignored. Use numeric prefixes to control merge order, for example

    ```
    10-telemetry.json
    ```

    and

    ```
    20-security.json
    ```

    .
  - macOS:[[Configure permissions - Claude Code Docs#Managed-only settings|managed settings]]and[[Connect Claude Code to tools via MCP - Claude Code Docs#Managed MCP configuration|Managed MCP configuration]]for details. This[repository](https://github.com/anthropics/claude-code/tree/main/examples/mdm)includes starter deployment templates for Jamf, Iru (Kandji), Intune, and Group Policy. Use these as starting points and adjust them to fit your needs.Managed deployments can also restrict plugin marketplace additions using

  ```
  strictKnownMarketplaces
  ```

  . For more information, see[[Create and distribute a plugin marketplace - Claude Code Docs#Managed marketplace restrictions|Managed marketplace restrictions]].
- Server-managed settings: delivered from Anthropic’s servers via the Claude.ai admin console. See
- Other configuration is stored in

  ```
  ~/.claude.json
  ```

  . This file contains your OAuth session,[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP server]]configurations for user and local scopes, per-project state (allowed tools, trust settings), and various caches. Project-scoped MCP servers are stored separately in

  ```
  .mcp.json
  ```

  .

Claude Code automatically creates timestamped backups of configuration files and retains the five most recent backups to prevent data loss.

Example settings.json

```
$schema
```

line in the example above points to the

[official JSON schema](https://json.schemastore.org/claude-code-settings.json)for Claude Code settings. Adding it to your

```
settings.json
```

enables autocomplete and inline validation in VS Code, Cursor, and any other editor that supports JSON schema validation.
The published schema is updated periodically and may not include settings added in the most recent CLI releases, so a validation warning on a recently documented field does not necessarily mean your configuration is invalid.

### Available settings

```
settings.json
```

supports a number of options:

KeyDescriptionExample

```
agent
```

Run the main thread as a named subagent. Applies that subagent’s system prompt, tool restrictions, and model. See

```
"code-reviewer"
```

```
allowedChannelPlugins
```

```
channelsEnabled: true
```

. See [[Push events into a running session with channels - Claude Code Docs#Restrict which channel plugins can run|Restrict which channel plugins can run]]

```
[{ "marketplace": "claude-plugins-official", "plugin": "telegram" }]
```

```
allowedHttpHookUrls
```

```
*
```

as a wildcard. When set, hooks with non-matching URLs are blocked. Undefined = no restriction, empty array = block all HTTP hooks. Arrays merge across settings sources. See [[Claude Code settings - Claude Code Docs#Hook configuration|Hook configuration]]

```
["https://hooks.example.com/*"]
```

```
allowedMcpServers
```

[[Connect Claude Code to tools via MCP - Claude Code Docs#Managed MCP configuration|Managed MCP configuration]]

```
[{ "serverName": "github" }]
```

```
allowManagedHooksOnly
```

```
enabledPlugins
```

are loaded. User, project, and all other plugin hooks are blocked. See [[Claude Code settings - Claude Code Docs#Hook configuration|Hook configuration]]

```
true
```

```
allowManagedMcpServersOnly
```

```
allowedMcpServers
```

from managed settings are respected.

```
deniedMcpServers
```

still merges from all sources. Users can still add MCP servers, but only the admin-defined allowlist applies. See [[Connect Claude Code to tools via MCP - Claude Code Docs#Managed MCP configuration|Managed MCP configuration]]

```
true
```

```
allowManagedPermissionRulesOnly
```

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

permission rules. Only rules in managed settings apply. See [[Configure permissions - Claude Code Docs#Managed-only settings|Managed-only settings]]

```
true
```

```
alwaysThinkingEnabled
```

[[Common workflows - Claude Code Docs#Use extended thinking (thinking mode)|extended thinking]]by default for all sessions. Typically configured via the

```
/config
```

command rather than editing directly

```
true
```

```
apiKeyHelper
```

```
/bin/sh
```

, to generate an auth value. This value will be sent as

```
X-Api-Key
```

and

```
Authorization: Bearer
```

headers for model requests

```
/bin/generate_temp_api_key.sh
```

```
attribution
```

[[Claude Code settings - Claude Code Docs#Attribution settings|Attribution settings]]

```
{"commit": "🤖 Generated with Claude Code", "pr": ""}
```

```
autoMemoryDirectory
```

[[How Claude remembers your project - Claude Code Docs#Storage location|auto memory]]storage. Accepts

```
~/
```

-expanded paths. Not accepted in project settings (

```
.claude/settings.json
```

) to prevent shared repos from redirecting memory writes to sensitive locations. Accepted from policy, local, and user settings

```
"~/my-memory-dir"
```

```
autoMode
```

[[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|auto mode]]classifier blocks and allows. Contains

```
environment
```

,

```
allow
```

, and

```
soft_deny
```

arrays of prose rules. Include the literal string

```
"$defaults"
```

in an array to inherit the built-in rules at that position. See [[Configure auto mode - Claude Code Docs|Configure auto mode]]. Not read from shared project settings

```
{"soft_deny": ["$defaults", "Never run terraform apply"]}
```

```
autoScrollEnabled
```

[[Fullscreen rendering - Claude Code Docs|fullscreen rendering]], follow new output to the bottom of the conversation. Default:

```
true
```

. Appears in

```
/config
```

as Auto-scroll. Permission prompts still scroll into view when this is off

```
false
```

```
autoUpdatesChannel
```

```
"stable"
```

for a version that is typically about one week old and skips versions with major regressions, or

```
"latest"
```

(default) for the most recent release

```
"stable"
```

```
availableModels
```

```
/model
```

,

```
--model
```

, or

```
ANTHROPIC_MODEL
```

. Does not affect the Default option. See [[Model configuration - Claude Code Docs#Restrict model selection|Restrict model selection]]

```
["sonnet", "haiku"]
```

```
awaySummaryEnabled
```

```
false
```

or turn off Session recap in

```
/config
```

to disable. Same as

```
CLAUDE_CODE_ENABLE_AWAY_SUMMARY
```

```
true
```

```
awsAuthRefresh
```

```
.aws
```

directory (see [[Claude Code on Amazon Bedrock - Claude Code Docs#Advanced credential configuration|advanced credential configuration]])

```
aws sso login --profile myprofile
```

```
awsCredentialExport
```

[[Claude Code on Amazon Bedrock - Claude Code Docs#Advanced credential configuration|advanced credential configuration]])

```
/bin/generate_aws_grant.sh
```

```
blockedMarketplaces
```

[[Create and distribute a plugin marketplace - Claude Code Docs#Managed marketplace restrictions|Managed marketplace restrictions]]

```
[{ "source": "github", "repo": "untrusted/plugins" }]
```

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
true
```

```
cleanupPeriodDays
```

```
0
```

is rejected with a validation error. Also controls the age cutoff for automatic removal of [[Common workflows - Claude Code Docs#Worktree cleanup|orphaned subagent worktrees]]at startup. To disable transcript writes entirely, set the[[Environment variables - Claude Code Docs|environment variable, or in non-interactive mode (]]

```
CLAUDE_CODE_SKIP_PROMPT_HISTORY
```

```
-p
```

) use the

```
--no-session-persistence
```

flag or the

```
persistSession: false
```

SDK option.

```
20
```

```
companyAnnouncements
```

```
["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]
```

```
defaultShell
```

```
!
```

commands. Accepts

```
"bash"
```

(default) or

```
"powershell"
```

. Setting

```
"powershell"
```

routes interactive

```
!
```

commands through PowerShell on Windows. Requires

```
CLAUDE_CODE_USE_POWERSHELL_TOOL=1
```

. See [[Tools reference - Claude Code Docs#PowerShell tool|PowerShell tool]]

```
"powershell"
```

```
deniedMcpServers
```

[[Connect Claude Code to tools via MCP - Claude Code Docs#Managed MCP configuration|Managed MCP configuration]]

```
[{ "serverName": "filesystem" }]
```

```
disableAllHooks
```

[[Hooks reference - Claude Code Docs|hooks]]and any custom[[Customize your status line - Claude Code Docs|status line]]

```
true
```

```
disableAutoMode
```

```
"disable"
```

to prevent [[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|auto mode]]from being activated. Removes

```
auto
```

from the

```
Shift+Tab
```

cycle and rejects

```
--permission-mode auto
```

at startup. Most useful in [[Configure permissions - Claude Code Docs#Managed settings|managed settings]]where users cannot override it

```
"disable"
```

```
disableDeepLinkRegistration
```

```
"disable"
```

to prevent Claude Code from registering the

```
claude-cli://
```

protocol handler with the operating system on startup. Deep links let external tools open a Claude Code session with a pre-filled prompt via

```
claude-cli://open?q=...
```

. The

```
q
```

parameter supports multi-line prompts using URL-encoded newlines (

```
%0A
```

). Useful in environments where protocol handler registration is restricted or managed separately

```
"disable"
```

```
disabledMcpjsonServers
```

```
.mcp.json
```

files to reject

```
["filesystem"]
```

```
disableSkillShellExecution
```

```
!`...`
```

and

```
```!
```

blocks in [[Extend Claude with skills - Claude Code Docs|skills]]and custom commands from user, project, plugin, or additional-directory sources. Commands are replaced with

```
[shell command execution disabled by policy]
```

instead of being run. Bundled and managed skills are not affected. Most useful in [[Configure permissions - Claude Code Docs#Managed settings|managed settings]]where users cannot override it

```
true
```

```
editorMode
```

```
"normal"
```

or

```
"vim"
```

. Default:

```
"normal"
```

. Appears in

```
/config
```

as Editor mode

```
"vim"
```

```
effortLevel
```

[[Model configuration - Claude Code Docs#Adjust effort level|effort level]]across sessions. Accepts

```
"low"
```

,

```
"medium"
```

,

```
"high"
```

, or

```
"xhigh"
```

. Written automatically when you run

```
/effort
```

with one of those values. See [[Model configuration - Claude Code Docs#Adjust effort level|Adjust effort level]]for supported models

```
"xhigh"
```

```
enableAllProjectMcpServers
```

```
.mcp.json
```

files

```
true
```

```
enabledMcpjsonServers
```

```
.mcp.json
```

files to approve

```
["memory", "github"]
```

```
env
```

```
{"FOO": "bar"}
```

```
fastModePerSessionOptIn
```

```
true
```

, fast mode does not persist across sessions. Each session starts with fast mode off, requiring users to enable it with

```
/fast
```

. The user’s fast mode preference is still saved. See [[Speed up responses with fast mode - Claude Code Docs#Require per-session opt-in|Require per-session opt-in]]

```
true
```

```
feedbackSurveyRate
```

[[Data usage - Claude Code Docs#Session quality surveys|session quality survey]]appears when eligible. Set to

```
0
```

to suppress entirely. Useful when using Bedrock, Vertex, or Foundry where the default sample rate does not apply

```
0.05
```

```
fileSuggestion
```

```
@
```

file autocomplete. See [[Claude Code settings - Claude Code Docs#File suggestion settings|File suggestion settings]]

```
{"type": "command", "command": "~/.claude/file-suggestion.sh"}
```

```
forceLoginMethod
```

```
claudeai
```

to restrict login to Claude.ai accounts,

```
console
```

to restrict login to Claude Console (API usage billing) accounts

```
claudeai
```

```
forceLoginOrgUUID
```

```
"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

or

```
["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]
```

```
forceRemoteSettingsRefresh
```

[[Configure server-managed settings - Claude Code Docs#Enforce fail-closed startup|fail-closed enforcement]]

```
true
```

```
hooks
```

[[Hooks reference - Claude Code Docs|hooks documentation]]for format[[Hooks reference - Claude Code Docs|hooks]]

```
httpHookAllowedEnvVars
```

```
allowedEnvVars
```

is the intersection with this list. Undefined = no restriction. Arrays merge across settings sources. See [[Claude Code settings - Claude Code Docs#Hook configuration|Hook configuration]]

```
["MY_TOKEN", "HOOK_SECRET"]
```

```
includeCoAuthoredBy
```

```
attribution
```

instead. Whether to include the

```
co-authored-by Claude
```

byline in git commits and pull requests (default:

```
true
```

)

```
false
```

```
includeGitInstructions
```

```
true
```

). Set to

```
false
```

to remove both, for example when using your own git workflow skills. The

```
CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS
```

environment variable takes precedence over this setting when set

```
false
```

```
language
```

```
"japanese"
```

,

```
"spanish"
```

,

```
"french"
```

). Claude will respond in this language by default. Also sets the [[Voice dictation - Claude Code Docs#Change the dictation language|voice dictation]]language

```
"japanese"
```

```
minimumVersion
```

```
claude update
```

from installing a version below this one. Switching from the

```
"latest"
```

channel to

```
"stable"
```

via

```
/config
```

prompts you to stay on the current version or allow the downgrade. Choosing to stay sets this value. Also useful in [[Configure permissions - Claude Code Docs#Managed settings|managed settings]]to pin an organization-wide minimum

```
"2.1.100"
```

```
model
```

```
"claude-sonnet-4-6"
```

```
modelOverrides
```

[[Model configuration - Claude Code Docs#Override model IDs per version|Override model IDs per version]]

```
{"claude-opus-4-6": "arn:aws:bedrock:..."}
```

```
otelHeadersHelper
```

[[Monitoring - Claude Code Docs#Dynamic headers|Dynamic headers]])

```
/bin/generate_otel_headers.sh
```

```
outputStyle
```

[[Output styles - Claude Code Docs|output styles documentation]]

```
"Explanatory"
```

```
permissions
```

```
plansDirectory
```

```
~/.claude/plans
```

```
"./plans"
```

```
pluginTrustMessage
```

```
"All plugins from our marketplace are approved by IT"
```

```
prefersReducedMotion
```

```
true
```

```
prUrlTemplate
```

```
{host}
```

,

```
{owner}
```

,

```
{repo}
```

,

```
{number}
```

, and

```
{url}
```

from the

```
gh
```

-reported PR URL. Use to point PR links at an internal code-review tool instead of

```
github.com
```

. Does not affect

```
#123
```

autolinks in Claude’s prose

```
"https://reviews.example.com/{owner}/{repo}/pull/{number}"
```

```
respectGitignore
```

```
@
```

file picker respects

```
.gitignore
```

patterns. When

```
true
```

(default), files matching

```
.gitignore
```

patterns are excluded from suggestions

```
false
```

```
showClearContextOnPlanAccept
```

```
false
```

. Set to

```
true
```

to restore the option

```
true
```

```
showThinkingSummaries
```

[[Common workflows - Claude Code Docs#Use extended thinking (thinking mode)|extended thinking]]summaries in interactive sessions. When unset or

```
false
```

(default in interactive mode), thinking blocks are redacted by the API and shown as a collapsed stub. Redaction only changes what you see, not what the model generates: to reduce thinking spend, [[Common workflows - Claude Code Docs#Use extended thinking (thinking mode)|lower the budget or disable thinking]]instead. Non-interactive mode (

```
-p
```

) and SDK callers always receive summaries regardless of this setting

```
true
```

```
showTurnDuration
```

```
true
```

. Appears in

```
/config
```

as Show turn duration

```
false
```

```
skipWebFetchPreflight
```

[[Data usage - Claude Code Docs#WebFetch domain safety check|WebFetch domain safety check]]that sends each requested hostname to

```
api.anthropic.com
```

before fetching. Set to

```
true
```

in environments that block traffic to Anthropic, such as Bedrock, Vertex AI, or Foundry deployments with restrictive egress. When skipped, WebFetch attempts any URL without consulting the blocklist

```
true
```

```
spinnerTipsEnabled
```

```
false
```

to disable tips (default:

```
true
```

)

```
false
```

```
spinnerTipsOverride
```

```
tips
```

: array of tip strings.

```
excludeDefault
```

: if

```
true
```

, only show custom tips; if

```
false
```

or absent, custom tips are merged with built-in tips

```
{ "excludeDefault": true, "tips": ["Use our internal tool X"] }
```

```
spinnerVerbs
```

```
mode
```

to

```
"replace"
```

to use only your verbs, or

```
"append"
```

to add them to the defaults

```
{"mode": "append", "verbs": ["Pondering", "Crafting"]}
```

```
sshConfigs
```

[[Use Claude Code Desktop - Claude Code Docs#Pre-configure SSH connections for your team|Desktop]]environment dropdown. Each entry requires

```
id
```

,

```
name
```

, and

```
sshHost
```

;

```
sshPort
```

,

```
sshIdentityFile
```

, and

```
startDirectory
```

are optional. When set in managed settings, connections are read-only for users. Read from managed and user settings only

```
[{"id": "dev-vm", "name": "Dev VM", "sshHost": "user@dev.example.com"}]
```

```
statusLine
```

```
statusLine
```

documentation

```
{"type": "command", "command": "~/.claude/statusline.sh"}
```

```
strictKnownMarketplaces
```

[[Create and distribute a plugin marketplace - Claude Code Docs#Managed marketplace restrictions|Managed marketplace restrictions]]

```
[{ "source": "github", "repo": "acme-corp/plugins" }]
```

```
teammateMode
```

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|agent team]]teammates display:

```
auto
```

(picks split panes in tmux or iTerm2, in-process otherwise),

```
in-process
```

, or

```
tmux
```

. See [[Orchestrate teams of Claude Code sessions - Claude Code Docs#Choose a display mode|choose a display mode]]

```
"in-process"
```

```
terminalProgressBarEnabled
```

```
true
```

. Appears in

```
/config
```

as Terminal progress bar

```
false
```

```
tui
```

```
"fullscreen"
```

for the flicker-free [[Fullscreen rendering - Claude Code Docs|alt-screen renderer]]with virtualized scrollback. Use

```
"default"
```

for the classic main-screen renderer. Set via

```
/tui
```

```
"fullscreen"
```

```
useAutoModeDuringPlan
```

```
true
```

. Not read from shared project settings. Appears in

```
/config
```

as “Use auto mode during plan”

```
false
```

```
viewMode
```

```
"default"
```

,

```
"verbose"
```

, or

```
"focus"
```

. Overrides the sticky

```
/focus
```

selection when set

```
"verbose"
```

```
voice
```

[[Voice dictation - Claude Code Docs|Voice dictation]]settings:

```
enabled
```

turns dictation on,

```
mode
```

selects

```
"hold"
```

or

```
"tap"
```

, and

```
autoSubmit
```

sends the prompt on key release in hold mode. Written automatically when you run

```
/voice
```

. Requires a Claude.ai account

```
{ "enabled": true, "mode": "tap" }
```

```
voiceEnabled
```

```
voice.enabled
```

. Prefer the

```
voice
```

object

```
true
```

```
wslInheritsWindowsSettings
```

```
true
```

, Claude Code on WSL reads managed settings from the Windows policy chain in addition to

```
/etc/claude-code
```

, with Windows sources taking priority. Only honored when set in the HKLM registry key or

```
C:\Program Files\ClaudeCode\managed-settings.json
```

, both of which require Windows admin to write. For HKCU policy to also apply on WSL, the flag must additionally be set in HKCU itself. Has no effect on native Windows

```
true
```

### Global config settings

These settings are stored in

```
~/.claude.json
```

rather than

```
settings.json
```

. Adding them to

```
settings.json
```

will trigger a schema validation error.

Versions before v2.1.119 also store

```
autoScrollEnabled
```

,

```
editorMode
```

,

```
showTurnDuration
```

,

```
teammateMode
```

, and

```
terminalProgressBarEnabled
```

here instead of in

```
settings.json
```

.

KeyDescriptionExample

```
autoConnectIde
```

Automatically connect to a running IDE when Claude Code starts from an external terminal. Default:

```
false
```

. Appears in

```
/config
```

as Auto-connect to IDE (external terminal) when running outside a VS Code or JetBrains terminal

```
true
```

```
autoInstallIdeExtension
```

Automatically install the Claude Code IDE extension when running from a VS Code terminal. Default:

```
true
```

. Appears in

```
/config
```

as Auto-install IDE extension when running inside a VS Code or JetBrains terminal. You can also set the

```
CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL
```

```
false
```

```
externalEditorContext
```

Prepend Claude’s previous response as

```
#
```

-commented context when you open the external editor with

```
Ctrl+G
```

. Default:

```
false
```

. Appears in

```
/config
```

as Show last response in external editor

```
true
```

### Worktree settings

Configure how

```
--worktree
```

creates and manages git worktrees. Use these settings to reduce disk usage and startup time in large monorepos.

KeyDescriptionExample

```
worktree.symlinkDirectories
```

Directories to symlink from the main repository into each worktree to avoid duplicating large directories on disk. No directories are symlinked by default

```
["node_modules", ".cache"]
```

```
worktree.sparsePaths
```

Directories to check out in each worktree via git sparse-checkout (cone mode). Only the listed paths are written to disk, which is faster in large monorepos

```
["packages/my-app", "shared/utils"]
```

```
.env
```

into new worktrees, use a

[[Common workflows - Claude Code Docs#Copy gitignored files to worktrees|in your project root instead of a setting.]]

```
.worktreeinclude
```

file

### Permission settings

KeysDescriptionExample

```
allow
```

Array of permission rules to allow tool use. See

```
[ "Bash(git diff *)" ]
```

```
ask
```

[[Claude Code settings - Claude Code Docs#Permission rule syntax|Permission rule syntax]]below

```
[ "Bash(git push *)" ]
```

```
deny
```

[[Claude Code settings - Claude Code Docs#Permission rule syntax|Permission rule syntax]]and[[Configure permissions - Claude Code Docs#Tool-specific permission rules|Bash permission limitations]]

```
[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]
```

```
additionalDirectories
```

[[Configure permissions - Claude Code Docs#Working directories|working directories]]for file access. Most

```
.claude/
```

configuration is [[Configure permissions - Claude Code Docs#Additional directories grant file access, not configuration|not discovered]]from these directories

```
[ "../docs/" ]
```

```
defaultMode
```

[[Choose a permission mode - Claude Code Docs|permission mode]]when opening Claude Code. Valid values:

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

,

```
auto
```

,

```
dontAsk
```

,

```
bypassPermissions
```

. The

```
--permission-mode
```

CLI flag overrides this setting for a single session

```
"acceptEdits"
```

```
disableBypassPermissionsMode
```

```
"disable"
```

to prevent

```
bypassPermissions
```

mode from being activated. This disables the

```
--dangerously-skip-permissions
```

command-line flag. Typically placed in [[Configure permissions - Claude Code Docs#Managed settings|managed settings]]to enforce organizational policy, but works from any scope

```
"disable"
```

```
skipDangerousModePermissionPrompt
```

```
--dangerously-skip-permissions
```

or

```
defaultMode: "bypassPermissions"
```

. Ignored when set in project settings (

```
.claude/settings.json
```

) to prevent untrusted repositories from auto-bypassing the prompt

```
true
```

### Permission rule syntax

Permission rules follow the format

```
Tool
```

or

```
Tool(specifier)
```

. Rules are evaluated in order: deny rules first, then ask, then allow. The first matching rule wins.
Quick examples:

RuleEffect

```
Bash
```

Matches all Bash commands

```
Bash(npm run *)
```

Matches commands starting with

```
npm run
```

```
Read(./.env)
```

Matches reading the

```
.env
```

file

```
WebFetch(domain:example.com)
```

Matches fetch requests to example.com

[[Configure permissions - Claude Code Docs#Permission rule syntax|Permission rule syntax]].

### Sandbox settings

Configure advanced sandboxing behavior. Sandboxing isolates bash commands from your filesystem and network. See

[[Sandboxing - Claude Code Docs|Sandboxing]]for details.

KeysDescriptionExample

```
enabled
```

Enable bash sandboxing (macOS, Linux, and WSL2). Default: false

```
true
```

```
failIfUnavailable
```

Exit with an error at startup if

```
sandbox.enabled
```

is true but the sandbox cannot start (missing dependencies or unsupported platform). When false (default), a warning is shown and commands run unsandboxed. Intended for managed settings deployments that require sandboxing as a hard gate

```
true
```

```
autoAllowBashIfSandboxed
```

Auto-approve bash commands when sandboxed. Default: true

```
true
```

```
excludedCommands
```

Commands that should run outside of the sandbox

```
["docker *"]
```

```
allowUnsandboxedCommands
```

Allow commands to run outside the sandbox via the

```
dangerouslyDisableSandbox
```

parameter. When set to

```
false
```

, the

```
dangerouslyDisableSandbox
```

escape hatch is completely disabled and all commands must run sandboxed (or be in

```
excludedCommands
```

). Useful for enterprise policies that require strict sandboxing. Default: true

```
false
```

```
filesystem.allowWrite
```

Additional paths where sandboxed commands can write. Arrays are merged across all settings scopes: user, project, and managed paths are combined, not replaced. Also merged with paths from

```
Edit(...)
```

allow permission rules. See

```
["/tmp/build", "~/.kube"]
```

```
filesystem.denyWrite
```

Paths where sandboxed commands cannot write. Arrays are merged across all settings scopes. Also merged with paths from

```
Edit(...)
```

deny permission rules.

```
["/etc", "/usr/local/bin"]
```

```
filesystem.denyRead
```

Paths where sandboxed commands cannot read. Arrays are merged across all settings scopes. Also merged with paths from

```
Read(...)
```

deny permission rules.

```
["~/.aws/credentials"]
```

```
filesystem.allowRead
```

Paths to re-allow reading within

```
denyRead
```

regions. Takes precedence over

```
denyRead
```

. Arrays are merged across all settings scopes. Use this to create workspace-only read access patterns.

```
["."]
```

```
filesystem.allowManagedReadPathsOnly
```

(Managed settings only) Only

```
filesystem.allowRead
```

paths from managed settings are respected.

```
denyRead
```

still merges from all sources. Default: false

```
true
```

```
network.allowUnixSockets
```

(macOS only) Unix socket paths accessible in sandbox. Ignored on Linux and WSL2, where the seccomp filter cannot inspect socket paths; use

```
allowAllUnixSockets
```

instead.

```
["~/.ssh/agent-socket"]
```

```
network.allowAllUnixSockets
```

Allow all Unix socket connections in sandbox. On Linux and WSL2 this is the only way to permit Unix sockets, since it skips the seccomp filter that otherwise blocks

```
socket(AF_UNIX, ...)
```

calls. Default: false

```
true
```

```
network.allowLocalBinding
```

Allow binding to localhost ports (macOS only). Default: false

```
true
```

```
network.allowMachLookup
```

Additional XPC/Mach service names the sandbox may look up (macOS only). Supports a single trailing

```
*
```

for prefix matching. Needed for tools that communicate via XPC such as the iOS Simulator or Playwright.

```
["com.apple.coresimulator.*"]
```

```
network.allowedDomains
```

Array of domains to allow for outbound network traffic. Supports wildcards (e.g.,

```
*.example.com
```

).

```
["github.com", "*.npmjs.org"]
```

```
network.deniedDomains
```

Array of domains to block for outbound network traffic. Supports the same wildcard syntax as

```
allowedDomains
```

. Takes precedence over

```
allowedDomains
```

when both match. Merged from all settings sources regardless of

```
allowManagedDomainsOnly
```

.

```
["sensitive.cloud.example.com"]
```

```
network.allowManagedDomainsOnly
```

(Managed settings only) Only

```
allowedDomains
```

and

```
WebFetch(domain:...)
```

allow rules from managed settings are respected. Domains from user, project, and local settings are ignored. Non-allowed domains are blocked automatically without prompting the user. Denied domains are still respected from all sources. Default: false

```
true
```

```
network.httpProxyPort
```

HTTP proxy port used if you wish to bring your own proxy. If not specified, Claude will run its own proxy.

```
8080
```

```
network.socksProxyPort
```

SOCKS5 proxy port used if you wish to bring your own proxy. If not specified, Claude will run its own proxy.

```
8081
```

```
enableWeakerNestedSandbox
```

Enable weaker sandbox for unprivileged Docker environments (Linux and WSL2 only). Reduces security. Default: false

```
true
```

```
enableWeakerNetworkIsolation
```

(macOS only) Allow access to the system TLS trust service (

```
com.apple.trustd.agent
```

) in the sandbox. Required for Go-based tools like

```
gh
```

,

```
gcloud
```

, and

```
terraform
```

to verify TLS certificates when using

```
httpProxyPort
```

with a MITM proxy and custom CA. Reduces security by opening a potential data exfiltration path. Default: false

```
true
```

#### Sandbox path prefixes

Paths in

```
filesystem.allowWrite
```

,

```
filesystem.denyWrite
```

,

```
filesystem.denyRead
```

, and

```
filesystem.allowRead
```

support these prefixes:

PrefixMeaningExample

```
/
```

Absolute path from filesystem root

```
/tmp/build
```

stays

```
/tmp/build
```

```
~/
```

Relative to home directory

```
~/.kube
```

becomes

```
$HOME/.kube
```

```
./
```

or no prefixRelative to the project root for project settings, or to

```
~/.claude
```

for user settings

```
./output
```

in

```
.claude/settings.json
```

resolves to

```
<project-root>/output
```

```
//path
```

prefix for absolute paths still works. If you previously used single-slash

```
/path
```

expecting project-relative resolution, switch to

```
./path
```

. This syntax differs from

[[Configure permissions - Claude Code Docs#Read and Edit|Read and Edit permission rules]], which use

```
//path
```

for absolute and

```
/path
```

for project-relative. Sandbox filesystem paths use standard conventions:

```
/tmp/build
```

is an absolute path.
Configuration example:

- ```
  sandbox.filesystem
  ```

  settings (shown above): Control paths at the OS-level sandbox boundary. These restrictions apply to all subprocess commands (e.g.,

  ```
  kubectl
  ```

  ,

  ```
  terraform
  ```

  ,

  ```
  npm
  ```

  ), not just Claude’s file tools.
- Permission rules: Use

  ```
  Edit
  ```

  allow/deny rules to control Claude’s file tool access,

  ```
  Read
  ```

  deny rules to block reads, and

  ```
  WebFetch
  ```

  allow/deny rules to control network domains. Paths from these rules are also merged into the sandbox configuration.

### Attribution settings

Claude Code adds attribution to git commits and pull requests. These are configured separately:

- Commits use [git trailers](https://git-scm.com/docs/git-interpret-trailers)(like

  ```
  Co-Authored-By
  ```

  ) by default, which can be customized or disabled
- Pull request descriptions are plain text

KeysDescription

```
commit
```

Attribution for git commits, including any trailers. Empty string hides commit attribution

```
pr
```

Attribution for pull request descriptions. Empty string hides pull request attribution

The

```
attribution
```

setting takes precedence over the deprecated

```
includeCoAuthoredBy
```

setting. To hide all attribution, set

```
commit
```

and

```
pr
```

to empty strings.

### File suggestion settings

Configure a custom command for

```
@
```

file path autocomplete. The built-in file suggestion uses fast filesystem traversal, but large monorepos may benefit from project-specific indexing such as a pre-built file index or custom tooling.

[[Hooks reference - Claude Code Docs|hooks]], including

```
CLAUDE_PROJECT_DIR
```

. It receives JSON via stdin with a

```
query
```

field:

### Hook configuration

These settings control which hooks are allowed to run and what HTTP hooks can access. The

```
allowManagedHooksOnly
```

setting can only be configured in

[[Claude Code settings - Claude Code Docs#Settings files|managed settings]]. The URL and env var allowlists can be set at any settings level and merge across sources. Behavior when

```
allowManagedHooksOnly
```

is

```
true
```

:

- Managed hooks and SDK hooks are loaded
- Hooks from plugins force-enabled in managed settings

  ```
  enabledPlugins
  ```

  are loaded. This lets administrators distribute vetted hooks through an organization marketplace while blocking everything else. Trust is granted by full

  ```
  plugin@marketplace
  ```

  ID, so a plugin with the same name from a different marketplace stays blocked
- User hooks, project hooks, and all other plugin hooks are blocked

```
*
```

as a wildcard for matching. When the array is defined, HTTP hooks targeting non-matching URLs are silently blocked.

```
allowedEnvVars
```

is the intersection of its own list and this setting.

### Settings precedence

Settings apply in order of precedence. From highest to lowest:

- Managed settings ([[Configure server-managed settings - Claude Code Docs|server-managed]],[[Claude Code settings - Claude Code Docs#Configuration scopes|MDM/OS-level policies]], or[[Claude Code settings - Claude Code Docs#Settings files|managed settings]])
  - Policies deployed by IT through server delivery, MDM configuration profiles, registry policies, or managed settings files
  - Cannot be overridden by any other level, including command line arguments
  - Within the managed tier, precedence is: server-managed > MDM/OS-level policies > file-based (

    ```
    managed-settings.d/*.json
    ```

    +

    ```
    managed-settings.json
    ```

    ) > HKCU registry (Windows only). Only one managed source is used; sources do not merge across tiers. Within the file-based tier, drop-in files and the base file are merged together.
- Command line arguments
  - Temporary overrides for a specific session
- Local project settings (

  ```
  .claude/settings.local.json
  ```

  )
  - Personal project-specific settings
- Shared project settings (

  ```
  .claude/settings.json
  ```

  )
  - Team-shared project settings in source control
- User settings (

  ```
  ~/.claude/settings.json
  ```

  )
  - Personal global settings

[[Use Claude Code in VS Code - Claude Code Docs|VS Code extension]], or a

[[JetBrains IDEs - Claude Code Docs|JetBrains IDE]]. For example, if your user settings allow

```
Bash(npm run *)
```

but a project’s shared settings deny it, the project setting takes precedence and the command is blocked.

Array settings merge across scopes. When the same array-valued setting (such as

```
sandbox.filesystem.allowWrite
```

or

```
permissions.allow
```

) appears in multiple scopes, the arrays are concatenated and deduplicated, not replaced. This means lower-priority scopes can add entries without overriding those set by higher-priority scopes, and vice versa. For example, if managed settings set

```
allowWrite
```

to

```
["/opt/company-tools"]
```

and a user adds

```
["~/.kube"]
```

, both paths are included in the final configuration.

### Verify active settings

Run

```
/status
```

inside Claude Code to see which settings sources are active and where they come from. The output shows each configuration layer (managed, user, project) along with its origin, such as

```
Enterprise managed settings (remote)
```

,

```
Enterprise managed settings (plist)
```

,

```
Enterprise managed settings (HKLM)
```

,

```
Enterprise managed settings (HKCU)
```

, or

```
Enterprise managed settings (file)
```

. If a settings file contains errors,

```
/status
```

reports the issue so you can fix it.

### Key points about the configuration system

- Memory files (

  ```
  CLAUDE.md
  ```

  ): Contain instructions and context that Claude loads at startup
- Settings files (JSON): Configure permissions, environment variables, and tool behavior
- Skills: Custom prompts that can be invoked with

  ```
  /skill-name
  ```

  or loaded by Claude automatically
- MCP servers: Extend Claude Code with additional tools and integrations
- Precedence: Higher-level configurations (Managed) override lower-level ones (User/Project)
- Inheritance: Settings are merged, with more specific settings adding to or overriding broader ones

### System prompt

Claude Code’s internal system prompt is not published. To add custom instructions, use

```
CLAUDE.md
```

files or the

```
--append-system-prompt
```

flag.

### Excluding sensitive files

To prevent Claude Code from accessing files containing sensitive information like API keys, secrets, and environment files, use the

```
permissions.deny
```

setting in your

```
.claude/settings.json
```

file:

```
ignorePatterns
```

configuration. Files matching these patterns are excluded from file discovery and search results, and read operations on these files are denied.

## Subagent configuration

Claude Code supports custom AI subagents that can be configured at both user and project levels. These subagents are stored as Markdown files with YAML frontmatter:

- User subagents:

  ```
  ~/.claude/agents/
  ```

  - Available across all your projects
- Project subagents:

  ```
  .claude/agents/
  ```

  - Specific to your project and can be shared with your team

[[Create custom subagents - Claude Code Docs|subagents documentation]].

## Plugin configuration

Claude Code supports a plugin system that lets you extend functionality with skills, agents, hooks, and MCP servers. Plugins are distributed through marketplaces and can be configured at both user and repository levels.

### Plugin settings

Plugin-related settings in

```
settings.json
```

:

#### ``` enabledPlugins ```

Controls which plugins are enabled. Format:

```
"plugin-name@marketplace-name": true/false
```

Scopes:

- User settings (

  ```
  ~/.claude/settings.json
  ```

  ): Personal plugin preferences
- Project settings (

  ```
  .claude/settings.json
  ```

  ): Project-specific plugins shared with team
- Local settings (

  ```
  .claude/settings.local.json
  ```

  ): Per-machine overrides (not committed)
- Managed settings (

  ```
  managed-settings.json
  ```

  ): Organization-wide policy overrides that block installation at all scopes and hide the plugin from the marketplace

#### ``` extraKnownMarketplaces ```

Defines additional marketplaces that should be made available for the repository. Typically used in repository-level settings to ensure team members have access to required plugin sources.
When a repository includes

```
extraKnownMarketplaces
```

:

- Team members are prompted to install the marketplace when they trust the folder
- Team members are then prompted to install plugins from that marketplace
- Users can skip unwanted marketplaces or plugins (stored in user settings)
- Installation respects trust boundaries and requires explicit consent

- ```
  github
  ```

  : GitHub repository (uses

  ```
  repo
  ```

  )
- ```
  git
  ```

  : Any git URL (uses

  ```
  url
  ```

  )
- ```
  directory
  ```

  : Local filesystem path (uses

  ```
  path
  ```

  , for development only)
- ```
  hostPattern
  ```

  : regex pattern to match marketplace hosts (uses

  ```
  hostPattern
  ```

  )
- ```
  settings
  ```

  : inline marketplace declared directly in settings.json without a separate hosted repository (uses

  ```
  name
  ```

  and

  ```
  plugins
  ```

  )

```
source: 'settings'
```

to declare a small set of plugins inline without setting up a hosted marketplace repository. Plugins listed here must reference external sources such as GitHub or npm. You still need to enable each plugin separately in

```
enabledPlugins
```

.

#### ``` strictKnownMarketplaces ```

Managed settings only: Controls which plugin marketplaces users are allowed to add and install plugins from. This setting can only be configured in

[[Claude Code settings - Claude Code Docs#Settings files|managed settings]]and provides administrators with strict control over marketplace sources. Managed settings file locations:

- macOS:

  ```
  /Library/Application Support/ClaudeCode/managed-settings.json
  ```
- Linux and WSL:

  ```
  /etc/claude-code/managed-settings.json
  ```
- Windows:

  ```
  C:\Program Files\ClaudeCode\managed-settings.json
  ```

- Only available in managed settings (

  ```
  managed-settings.json
  ```

  )
- Cannot be overridden by user or project settings (highest precedence)
- Enforced BEFORE network/filesystem operations (blocked sources never execute)
- Uses exact matching for source specifications (including

  ```
  ref
  ```

  ,

  ```
  path
  ```

  for git sources), except

  ```
  hostPattern
  ```

  , which uses regex matching

- ```
  undefined
  ```

  (default): No restrictions - users can add any marketplace
- Empty array

  ```
  []
  ```

  : Complete lockdown - users cannot add any new marketplaces
- List of sources: Users can only add marketplaces that match exactly

```
hostPattern
```

uses regex matching against the marketplace host.

- GitHub repositories:

```
repo
```

(required),

```
ref
```

(optional: branch/tag/SHA),

```
path
```

(optional: subdirectory)

- Git repositories:

```
url
```

(required),

```
ref
```

(optional: branch/tag/SHA),

```
path
```

(optional: subdirectory)

- URL-based marketplaces:

```
url
```

(required),

```
headers
```

(optional: HTTP headers for authenticated access)

URL-based marketplaces only download the

```
marketplace.json
```

file. They do not download plugin files from the server. Plugins in URL-based marketplaces must use external sources (GitHub, npm, or git URLs) rather than relative paths. For plugins with relative paths, use a Git-based marketplace instead. See [[Create and distribute a plugin marketplace - Claude Code Docs#Plugins with relative paths fail in URL-based marketplaces|Troubleshooting]]for details.

- NPM packages:

```
package
```

(required, supports scoped packages)

- File paths:

```
path
```

(required: absolute path to marketplace.json file)

- Directory paths:

```
path
```

(required: absolute path to directory containing

```
.claude-plugin/marketplace.json
```

)

- Host pattern matching:

```
hostPattern
```

(required: regex pattern to match against the marketplace host)
Use host pattern matching when you want to allow all marketplaces from a specific host without enumerating each repository individually. This is useful for organizations with internal GitHub Enterprise or GitLab servers where developers create their own marketplaces.
Host extraction by source type:

- ```
  github
  ```

  : always matches against

  ```
  github.com
  ```
- ```
  git
  ```

  : extracts hostname from the URL (supports both HTTPS and SSH formats)
- ```
  url
  ```

  : extracts hostname from the URL
- ```
  npm
  ```

  ,

  ```
  file
  ```

  ,

  ```
  directory
  ```

  : not supported for host pattern matching

```
github
```

and

```
git
```

), this includes all optional fields:

- The

  ```
  repo
  ```

  or

  ```
  url
  ```

  must match exactly
- The

  ```
  ref
  ```

  field must match exactly (or both be undefined)
- The

  ```
  path
  ```

  field must match exactly (or both be undefined)

```
extraKnownMarketplaces
```

:

Aspect

```
strictKnownMarketplaces
```

```
extraKnownMarketplaces
```

PurposeOrganizational policy enforcementTeam convenienceSettings file

```
managed-settings.json
```

onlyAny settings fileBehaviorBlocks non-allowlisted additionsAuto-installs missing marketplacesWhen enforcedBefore network/filesystem operationsAfter user trust promptCan be overriddenNo (highest precedence)Yes (by higher precedence settings)Source formatDirect source objectNamed marketplace with nested sourceUse caseCompliance, security restrictionsOnboarding, standardization

```
strictKnownMarketplaces
```

uses direct source objects:

```
extraKnownMarketplaces
```

requires named marketplaces:

```
strictKnownMarketplaces
```

is a policy gate: it controls what users may add but does not register any marketplaces. To both restrict and pre-register a marketplace for all users, set both in

```
managed-settings.json
```

:

```
strictKnownMarketplaces
```

set, users can still add the allowed marketplace manually via

```
/plugin marketplace add
```

, but it is not available automatically.
Important notes:

- Restrictions are checked BEFORE any network requests or filesystem operations
- When blocked, users see clear error messages indicating the source is blocked by managed policy
- The restriction is enforced on marketplace add and on plugin install, update, refresh, and auto-update. A marketplace added before the policy was set cannot be used to install or update plugins once its source no longer matches the allowlist
- Managed settings have the highest precedence and cannot be overridden

[[Create and distribute a plugin marketplace - Claude Code Docs#Managed marketplace restrictions|Managed marketplace restrictions]]for user-facing documentation.

### Managing plugins

Use the

```
/plugin
```

command to manage plugins interactively:

- Browse available plugins from marketplaces
- Install/uninstall plugins
- Enable/disable plugins
- View plugin details (skills, agents, hooks provided)
- Add/remove marketplaces

[[Create plugins - Claude Code Docs|plugins documentation]].

## Environment variables

Environment variables let you control Claude Code behavior without editing settings files. Any variable can also be configured in

[[Claude Code settings - Claude Code Docs#Available settings|under the]]

```
settings.json
```

```
env
```

key to apply it to every session or roll it out to your team.
See the

[[Environment variables - Claude Code Docs|environment variables reference]]for the full list.

## Tools available to Claude

Claude Code has access to a set of tools for reading, editing, searching, running commands, and orchestrating subagents. Tool names are the exact strings you use in permission rules and hook matchers. See the

[[Tools reference - Claude Code Docs|tools reference]]for the full list and Bash tool behavior details.

## See also

- [[Configure permissions - Claude Code Docs|Permissions]]: permission system, rule syntax, tool-specific patterns, and managed policies
- [[Authentication - Claude Code Docs|Authentication]]: set up user access to Claude Code
- [[Debug your configuration - Claude Code Docs|Debug your configuration]]: diagnose why a setting, hook, or MCP server isn’t taking effect
- [[Troubleshooting - Claude Code Docs|Troubleshooting]]: installation, authentication, and platform issues

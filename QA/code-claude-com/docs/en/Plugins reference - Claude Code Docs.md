---
title: Plugins reference - Claude Code Docs
source_url: https://code.claude.com/docs/en/plugins-reference
description: Complete technical reference for Claude Code plugin system, including
  schemas, CLI commands, and component specifications.
---

## Plugin components reference

### Skills

Plugins add skills to Claude Code, creating

```
/name
```

shortcuts that you or Claude can invoke.
Location:

```
skills/
```

or

```
commands/
```

directory in plugin root
File format: Skills are directories with

```
SKILL.md
```

; commands are simple markdown files
Skill structure:

- Skills and commands are automatically discovered when the plugin is installed
- Claude can invoke them automatically based on task context
- Skills can include supporting files alongside SKILL.md

[[Extend Claude with skills - Claude Code Docs|Skills]].

### Agents

Plugins can provide specialized subagents for specific tasks that Claude can invoke automatically when appropriate. Location:

```
agents/
```

directory in plugin root
File format: Markdown files describing agent capabilities
Agent structure:

```
name
```

,

```
description
```

,

```
model
```

,

```
effort
```

,

```
maxTurns
```

,

```
tools
```

,

```
disallowedTools
```

,

```
skills
```

,

```
memory
```

,

```
background
```

, and

```
isolation
```

frontmatter fields. The only valid

```
isolation
```

value is

```
"worktree"
```

. For security reasons,

```
hooks
```

,

```
mcpServers
```

, and

```
permissionMode
```

are not supported for plugin-shipped agents.
Integration points:

- Agents appear in the

  ```
  /agents
  ```

  interface
- Claude can invoke agents automatically based on task context
- Agents can be invoked manually by users
- Plugin agents work alongside built-in Claude agents

[[Create custom subagents - Claude Code Docs|Subagents]].

### Hooks

Plugins can provide event handlers that respond to Claude Code events automatically. Location:

```
hooks/hooks.json
```

in plugin root, or inline in plugin.json
Format: JSON configuration with event matchers and actions
Hook configuration:

[[Hooks reference - Claude Code Docs|user-defined hooks]]:

EventWhen it fires

```
SessionStart
```

When a session begins or resumes

```
UserPromptSubmit
```

When you submit a prompt, before Claude processes it

```
UserPromptExpansion
```

When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion

```
PreToolUse
```

Before a tool call executes. Can block it

```
PermissionRequest
```

When a permission dialog appears

```
PermissionDenied
```

When a tool call is denied by the auto mode classifier. Return

```
{retry: true}
```

to tell the model it may retry the denied tool call

```
PostToolUse
```

After a tool call succeeds

```
PostToolUseFailure
```

After a tool call fails

```
PostToolBatch
```

After a full batch of parallel tool calls resolves, before the next model call

```
Notification
```

When Claude Code sends a notification

```
SubagentStart
```

When a subagent is spawned

```
SubagentStop
```

When a subagent finishes

```
TaskCreated
```

When a task is being created via

```
TaskCreate
```

```
TaskCompleted
```

When a task is being marked as completed

```
Stop
```

When Claude finishes responding

```
StopFailure
```

When the turn ends due to an API error. Output and exit code are ignored

```
TeammateIdle
```

When an

```
InstructionsLoaded
```

```
.claude/rules/*.md
```

file is loaded into context. Fires at session start and when files are lazily loaded during a session

```
ConfigChange
```

```
CwdChanged
```

```
cd
```

command. Useful for reactive environment management with tools like direnv

```
FileChanged
```

```
matcher
```

field specifies which filenames to watch

```
WorktreeCreate
```

```
--worktree
```

or

```
isolation: "worktree"
```

. Replaces default git behavior

```
WorktreeRemove
```

```
PreCompact
```

```
PostCompact
```

```
Elicitation
```

```
ElicitationResult
```

```
SessionEnd
```

- ```
  command
  ```

  : execute shell commands or scripts
- ```
  http
  ```

  : send the event JSON as a POST request to a URL
- ```
  mcp_tool
  ```

  : call a tool on a configured[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP server]]
- ```
  prompt
  ```

  : evaluate a prompt with an LLM (uses

  ```
  $ARGUMENTS
  ```

  placeholder for context)
- ```
  agent
  ```

  : run an agentic verifier with tools for complex verification tasks

### MCP servers

Plugins can bundle Model Context Protocol (MCP) servers to connect Claude Code with external tools and services. Location:

```
.mcp.json
```

in plugin root, or inline in plugin.json
Format: Standard MCP server configuration
MCP server configuration:

- Plugin MCP servers start automatically when the plugin is enabled
- Servers appear as standard MCP tools in Claude’s toolkit
- Server capabilities integrate seamlessly with Claude’s existing tools
- Plugin servers can be configured independently of user MCP servers

### LSP servers

Plugins can provide

[Language Server Protocol](https://microsoft.github.io/language-server-protocol/)(LSP) servers to give Claude real-time code intelligence while working on your codebase. LSP integration provides:

- Instant diagnostics: Claude sees errors and warnings immediately after each edit
- Code navigation: go to definition, find references, and hover information
- Language awareness: type information and documentation for code symbols

```
.lsp.json
```

in plugin root, or inline in

```
plugin.json
```

Format: JSON configuration mapping language server names to their configurations

```
.lsp.json
```

file format:

```
plugin.json
```

:

FieldDescription

```
command
```

The LSP binary to execute (must be in PATH)

```
extensionToLanguage
```

Maps file extensions to language identifiers

FieldDescription

```
args
```

Command-line arguments for the LSP server

```
transport
```

Communication transport:

```
stdio
```

(default) or

```
socket
```

```
env
```

Environment variables to set when starting the server

```
initializationOptions
```

Options passed to the server during initialization

```
settings
```

Settings passed via

```
workspace/didChangeConfiguration
```

```
workspaceFolder
```

Workspace folder path for the server

```
startupTimeout
```

Max time to wait for server startup (milliseconds)

```
shutdownTimeout
```

Max time to wait for graceful shutdown (milliseconds)

```
restartOnCrash
```

Whether to automatically restart the server if it crashes

```
maxRestarts
```

Maximum number of restart attempts before giving up

PluginLanguage serverInstall command

```
pyright-lsp
```

Pyright (Python)

```
pip install pyright
```

or

```
npm install -g pyright
```

```
typescript-lsp
```

TypeScript Language Server

```
npm install -g typescript-language-server typescript
```

```
rust-lsp
```

rust-analyzer

### Monitors

Plugins can declare background monitors that Claude Code starts automatically when the plugin is active. Each monitor runs a shell command for the lifetime of the session and delivers every stdout line to Claude as a notification, so Claude can react to log entries, status changes, or polled events without being asked to start the watch itself. Plugin monitors use the same mechanism as the

[[Tools reference - Claude Code Docs#Monitor tool|Monitor tool]]and share its availability constraints. They run only in interactive CLI sessions, run unsandboxed at the same trust level as

[[Plugins reference - Claude Code Docs#Hooks|hooks]], and are skipped on hosts where the Monitor tool is unavailable.

Plugin monitors require Claude Code v2.1.105 or later.

```
monitors/monitors.json
```

in the plugin root, or inline in

```
plugin.json
```

Format: JSON array of monitor entries
The following

```
monitors/monitors.json
```

watches a deployment status endpoint and a local error log:

```
monitors
```

key in

```
plugin.json
```

to the same array. To load from a non-default path, set

```
monitors
```

to a relative path string such as

```
"./config/monitors.json"
```

.
Required fields:

FieldDescription

```
name
```

Identifier unique within the plugin. Prevents duplicate processes when the plugin reloads or a skill is invoked again

```
command
```

Shell command run as a persistent background process in the session working directory

```
description
```

Short summary of what is being watched. Shown in the task panel and in notification summaries

FieldDescription

```
when
```

Controls when the monitor starts.

```
"always"
```

starts it at session start and on plugin reload, and is the default.

```
"on-skill-invoke:<skill-name>"
```

starts it the first time the named skill in this plugin is dispatched

```
command
```

value supports the same

[[Plugins reference - Claude Code Docs#Environment variables|variable substitutions]]as MCP and LSP server configs:

```
${CLAUDE_PLUGIN_ROOT}
```

,

```
${CLAUDE_PLUGIN_DATA}
```

,

```
${user_config.*}
```

, and any

```
${ENV_VAR}
```

from the environment. Prefix the command with

```
cd "${CLAUDE_PLUGIN_ROOT}" &&
```

if the script needs to run from the plugin’s own directory.
Disabling a plugin mid-session does not stop monitors that are already running. They stop when the session ends.

### Themes

Plugins can ship color themes that appear in

```
/theme
```

alongside the built-in presets and the user’s local themes. A theme is a JSON file in

```
themes/
```

with a

```
base
```

preset and a sparse

```
overrides
```

map of color tokens.

```
custom:<plugin-name>:<slug>
```

in the user’s config. Plugin themes are read-only; pressing

```
Ctrl+E
```

on one in

```
/theme
```

copies it into

```
~/.claude/themes/
```

so the user can edit the copy.

## Plugin installation scopes

When you install a plugin, you choose a scope that determines where the plugin is available and who else can use it:

ScopeSettings fileUse case

```
user
```

```
~/.claude/settings.json
```

Personal plugins available across all projects (default)

```
project
```

```
.claude/settings.json
```

Team plugins shared via version control

```
local
```

```
.claude/settings.local.json
```

Project-specific plugins, gitignored

```
managed
```

[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs#Install plugins|Install plugins]]. For a complete explanation of scopes, see

[[Claude Code settings - Claude Code Docs#Configuration scopes|Configuration scopes]].

## Plugin manifest schema

The

```
.claude-plugin/plugin.json
```

file defines your plugin’s metadata and configuration. This section documents all supported fields and options.
The manifest is optional. If omitted, Claude Code auto-discovers components in

[[Plugins reference - Claude Code Docs#File locations reference|default locations]]and derives the plugin name from the directory name. Use a manifest when you need to provide metadata or custom component paths.

### Complete schema

### Required fields

If you include a manifest,

```
name
```

is the only required field.

FieldTypeDescriptionExample

```
name
```

stringUnique identifier (kebab-case, no spaces)

```
"deployment-tools"
```

```
agent-creator
```

for the plugin with name

```
plugin-dev
```

will appear as

```
plugin-dev:agent-creator
```

.

### Metadata fields

FieldTypeDescriptionExample

```
version
```

stringOptional. Semantic version. Setting this pins the plugin to that version string, so users only receive updates when you bump it. If omitted, Claude Code falls back to the git commit SHA, so every commit is treated as a new version. If also set in the marketplace entry,

```
plugin.json
```

wins. See

```
"2.1.0"
```

```
description
```

stringBrief explanation of plugin purpose

```
"Deployment automation tools"
```

```
author
```

objectAuthor information

```
{"name": "Dev Team", "email": "dev@company.com"}
```

```
homepage
```

stringDocumentation URL

```
"https://docs.example.com"
```

```
repository
```

stringSource code URL

```
"https://github.com/user/plugin"
```

```
license
```

stringLicense identifier

```
"MIT"
```

,

```
"Apache-2.0"
```

```
keywords
```

arrayDiscovery tags

```
["deployment", "ci-cd"]
```

### Component path fields

FieldTypeDescriptionExample

```
skills
```

string|arrayCustom skill directories containing

```
<name>/SKILL.md
```

(replaces default

```
skills/
```

)

```
"./custom/skills/"
```

```
commands
```

string|arrayCustom flat

```
.md
```

skill files or directories (replaces default

```
commands/
```

)

```
"./custom/cmd.md"
```

or

```
["./cmd1.md"]
```

```
agents
```

string|arrayCustom agent files (replaces default

```
agents/
```

)

```
"./custom/agents/reviewer.md"
```

```
hooks
```

string|array|objectHook config paths or inline config

```
"./my-extra-hooks.json"
```

```
mcpServers
```

string|array|objectMCP config paths or inline config

```
"./my-extra-mcp-config.json"
```

```
outputStyles
```

string|arrayCustom output style files/directories (replaces default

```
output-styles/
```

)

```
"./styles/"
```

```
themes
```

string|arrayColor theme files/directories (replaces default

```
themes/
```

). See

```
"./themes/"
```

```
lspServers
```

string|array|object

```
"./.lsp.json"
```

```
monitors
```

[[Tools reference - Claude Code Docs#Monitor tool|Monitor]]configurations that start automatically when the plugin is active. See[[Plugins reference - Claude Code Docs#Monitors|Monitors]]

```
"./monitors.json"
```

```
userConfig
```

[[Plugins reference - Claude Code Docs#User configuration|User configuration]]

```
channels
```

[[Plugins reference - Claude Code Docs#Channels|Channels]]

```
dependencies
```

[[Constrain plugin dependency versions - Claude Code Docs|Constrain plugin dependency versions]]

```
[{ "name": "secrets-vault", "version": "~2.1.0" }]
```

### User configuration

The

```
userConfig
```

field declares values that Claude Code prompts the user for when the plugin is enabled. Use this instead of requiring users to hand-edit

```
settings.json
```

.

FieldRequiredDescription

```
type
```

YesOne of

```
string
```

,

```
number
```

,

```
boolean
```

,

```
directory
```

, or

```
file
```

```
title
```

YesLabel shown in the configuration dialog

```
description
```

YesHelp text shown beneath the field

```
sensitive
```

NoIf

```
true
```

, masks input and stores the value in secure storage instead of

```
settings.json
```

```
required
```

NoIf

```
true
```

, validation fails when the field is empty

```
default
```

NoValue used when the user provides nothing

```
multiple
```

NoFor

```
string
```

type, allow an array of strings

```
min
```

/

```
max
```

NoBounds for

```
number
```

type

```
${user_config.KEY}
```

in MCP and LSP server configs, hook commands, and monitor commands. Non-sensitive values can also be substituted in skill and agent content. All values are exported to plugin subprocesses as

```
CLAUDE_PLUGIN_OPTION_<KEY>
```

environment variables.
Non-sensitive values are stored in

```
settings.json
```

under

```
pluginConfigs[<plugin-id>].options
```

. Sensitive values go to the system keychain (or

```
~/.claude/.credentials.json
```

where the keychain is unavailable). Keychain storage is shared with OAuth tokens and has an approximately 2 KB total limit, so keep sensitive values small.

### Channels

The

```
channels
```

field lets a plugin declare one or more message channels that inject content into the conversation. Each channel binds to an MCP server that the plugin provides.

```
server
```

field is required and must match a key in the plugin’s

```
mcpServers
```

. The optional per-channel

```
userConfig
```

uses the same schema as the top-level field, letting the plugin prompt for bot tokens or owner IDs when the plugin is enabled.

### Path behavior rules

For

```
skills
```

,

```
commands
```

,

```
agents
```

,

```
outputStyles
```

,

```
themes
```

, and

```
monitors
```

, a custom path replaces the default. If the manifest specifies

```
skills
```

, the default

```
skills/
```

directory is not scanned; if it specifies

```
monitors
```

, the default

```
monitors/monitors.json
```

is not loaded.

[[Plugins reference - Claude Code Docs#Hooks|Hooks]],

[[Plugins reference - Claude Code Docs#MCP servers|MCP servers]], and

[[Plugins reference - Claude Code Docs#LSP servers|LSP servers]]have different semantics for handling multiple sources.

- All paths must be relative to the plugin root and start with

  ```
  ./
  ```
- Components from custom paths use the same naming and namespacing rules
- Multiple paths can be specified as arrays
- To keep the default directory and add more paths for skills, commands, agents, or output styles, include the default in your array:

  ```
  "skills": ["./skills/", "./extras/"]
  ```
- When a skill path points to a directory that contains a

  ```
  SKILL.md
  ```

  directly, for example

  ```
  "skills": ["./"]
  ```

  pointing to the plugin root, the frontmatter

  ```
  name
  ```

  field in

  ```
  SKILL.md
  ```

  determines the skill’s invocation name. This gives a stable name regardless of the install directory. If

  ```
  name
  ```

  is not set in the frontmatter, the directory basename is used as a fallback.

### Environment variables

Claude Code provides two variables for referencing plugin paths. Both are substituted inline anywhere they appear in skill content, agent content, hook commands, monitor commands, and MCP or LSP server configs. Both are also exported as environment variables to hook processes and MCP or LSP server subprocesses.

```
${CLAUDE_PLUGIN_ROOT}
```

: the absolute path to your plugin’s installation directory. Use this to reference scripts, binaries, and config files bundled with the plugin. This path changes when the plugin updates, so files you write here do not survive an update.

```
${CLAUDE_PLUGIN_DATA}
```

: a persistent directory for plugin state that survives updates. Use this for installed dependencies such as

```
node_modules
```

or Python virtual environments, generated code, caches, and any other files that should persist across plugin versions. The directory is created automatically the first time this variable is referenced.

#### Persistent data directory

The

```
${CLAUDE_PLUGIN_DATA}
```

directory resolves to

```
~/.claude/plugins/data/{id}/
```

, where

```
{id}
```

is the plugin identifier with characters outside

```
a-z
```

,

```
A-Z
```

,

```
0-9
```

,

```
_
```

, and

```
-
```

replaced by

```
-
```

. For a plugin installed as

```
formatter@my-marketplace
```

, the directory is

```
~/.claude/plugins/data/formatter-my-marketplace/
```

.
A common use is installing language dependencies once and reusing them across sessions and plugin updates. Because the data directory outlives any single plugin version, a check for directory existence alone cannot detect when an update changes the plugin’s dependency manifest. The recommended pattern compares the bundled manifest against a copy in the data directory and reinstalls when they differ.
This

```
SessionStart
```

hook installs

```
node_modules
```

on the first run and again whenever a plugin update includes a changed

```
package.json
```

:

```
diff
```

exits nonzero when the stored copy is missing or differs from the bundled one, covering both first run and dependency-changing updates. If

```
npm install
```

fails, the trailing

```
rm
```

removes the copied manifest so the next session retries.
Scripts bundled in

```
${CLAUDE_PLUGIN_ROOT}
```

can then run against the persisted

```
node_modules
```

:

```
/plugin
```

interface shows the directory size and prompts before deleting. The CLI deletes by default; pass

[[Plugins reference - Claude Code Docs#plugin uninstall|to preserve it.]]

```
--keep-data
```

## Plugin caching and file resolution

Plugins are specified in one of two ways:

- Through

  ```
  claude --plugin-dir
  ```

  , for the duration of a session.
- Through a marketplace, installed for future sessions.

```
~/.claude/plugins/cache
```

) rather than using them in-place. Understanding this behavior is important when developing plugins that reference external files.
Each installed version is a separate directory in the cache. When you update or uninstall a plugin, the previous version directory is marked as orphaned and removed automatically 7 days later. The grace period lets concurrent Claude Code sessions that already loaded the old version keep running without errors.
Claude’s Glob and Grep tools skip orphaned version directories during searches, so file results don’t include outdated plugin code.

### Path traversal limitations

Installed plugins cannot reference files outside their directory. Paths that traverse outside the plugin root (such as

```
../shared-utils
```

) will not work after installation because those external files are not copied to the cache.

### Working with external dependencies

If your plugin needs to access files outside its directory, you can create symbolic links to external files within your plugin directory. Symlinks are preserved in the cache rather than dereferenced, and they resolve to their target at runtime. The following command creates a link from inside your plugin directory to a shared utilities location:

## Plugin directory structure

### Standard plugin layout

A complete plugin follows this structure:

### File locations reference

ComponentDefault LocationPurposeManifest

```
.claude-plugin/plugin.json
```

Plugin metadata and configuration (optional)Skills

```
skills/
```

Skills with

```
<name>/SKILL.md
```

structureCommands

```
commands/
```

Skills as flat Markdown files. Use

```
skills/
```

for new pluginsAgents

```
agents/
```

Subagent Markdown filesOutput styles

```
output-styles/
```

Output style definitionsThemes

```
themes/
```

Color theme definitionsHooks

```
hooks/hooks.json
```

Hook configurationMCP servers

```
.mcp.json
```

MCP server definitionsLSP servers

```
.lsp.json
```

Language server configurationsMonitors

```
monitors/monitors.json
```

Background monitor configurationsExecutables

```
bin/
```

Executables added to the Bash tool’s

```
PATH
```

. Files here are invokable as bare commands in any Bash tool call while the plugin is enabledSettings

```
settings.json
```

Default configuration applied when the plugin is enabled. Only the

```
agent
```

[[Customize your status line - Claude Code Docs#Subagent status lines|keys are currently supported]]

```
subagentStatusLine
```

## CLI commands reference

Claude Code provides CLI commands for non-interactive plugin management, useful for scripting and automation.

### plugin install

Install a plugin from available marketplaces.

- ```
  <plugin>
  ```

  : Plugin name or

  ```
  plugin-name@marketplace-name
  ```

  for a specific marketplace

OptionDescriptionDefault

```
-s, --scope <scope>
```

Installation scope:

```
user
```

,

```
project
```

, or

```
local
```

```
user
```

```
-h, --help
```

Display help for command

```
--scope project
```

writes to

```
enabledPlugins
```

in .claude/settings.json, making the plugin available to everyone who clones the project repository.
Examples:

### plugin uninstall

Remove an installed plugin.

- ```
  <plugin>
  ```

  : Plugin name or

  ```
  plugin-name@marketplace-name
  ```

OptionDescriptionDefault

```
-s, --scope <scope>
```

Uninstall from scope:

```
user
```

,

```
project
```

, or

```
local
```

```
user
```

```
--keep-data
```

Preserve the plugin’s

```
-h, --help
```

```
remove
```

,

```
rm
```

By default, uninstalling from the last remaining scope also deletes the plugin’s

```
${CLAUDE_PLUGIN_DATA}
```

directory. Use

```
--keep-data
```

to preserve it, for example when reinstalling after testing a new version.

### plugin enable

Enable a disabled plugin.

- ```
  <plugin>
  ```

  : Plugin name or

  ```
  plugin-name@marketplace-name
  ```

OptionDescriptionDefault

```
-s, --scope <scope>
```

Scope to enable:

```
user
```

,

```
project
```

, or

```
local
```

```
user
```

```
-h, --help
```

Display help for command

### plugin disable

Disable a plugin without uninstalling it.

- ```
  <plugin>
  ```

  : Plugin name or

  ```
  plugin-name@marketplace-name
  ```

OptionDescriptionDefault

```
-s, --scope <scope>
```

Scope to disable:

```
user
```

,

```
project
```

, or

```
local
```

```
user
```

```
-h, --help
```

Display help for command

### plugin update

Update a plugin to the latest version.

- ```
  <plugin>
  ```

  : Plugin name or

  ```
  plugin-name@marketplace-name
  ```

OptionDescriptionDefault

```
-s, --scope <scope>
```

Scope to update:

```
user
```

,

```
project
```

,

```
local
```

, or

```
managed
```

```
user
```

```
-h, --help
```

Display help for command

### plugin list

List installed plugins with their version, source marketplace, and enable status.

OptionDescriptionDefault

```
--json
```

Output as JSON

```
--available
```

Include available plugins from marketplaces. Requires

```
--json
```

```
-h, --help
```

Display help for command

### plugin tag

Create a release git tag for the plugin in the current directory. Run from inside the plugin’s folder. See

[[Constrain plugin dependency versions - Claude Code Docs#Tag plugin releases for version resolution|Tag plugin releases]].

OptionDescriptionDefault

```
--push
```

Push the tag to the remote after creating it

```
--dry-run
```

Print what would be tagged without creating the tag

```
-f, --force
```

Create the tag even if the working tree is dirty or the tag already exists

```
-h, --help
```

Display help for command

## Debugging and development tools

### Debugging commands

Use

```
claude --debug
```

to see plugin loading details:
This shows:

- Which plugins are being loaded
- Any errors in plugin manifests
- Skill, agent, and hook registration
- MCP server initialization

### Common issues

IssueCauseSolutionPlugin not loadingInvalid

```
plugin.json
```

Run

```
claude plugin validate
```

or

```
/plugin validate
```

to check

```
plugin.json
```

, skill/agent/command frontmatter, and

```
hooks/hooks.json
```

for syntax and schema errorsSkills not appearingWrong directory structureEnsure

```
skills/
```

or

```
commands/
```

is at the plugin root, not inside

```
.claude-plugin/
```

Hooks not firingScript not executableRun

```
chmod +x script.sh
```

MCP server failsMissing

```
${CLAUDE_PLUGIN_ROOT}
```

Use variable for all plugin pathsPath errorsAbsolute paths usedAll paths must be relative and start with

```
./
```

LSP

```
Executable not found in $PATH
```

Language server not installedInstall the binary (e.g.,

```
npm install -g typescript-language-server typescript
```

)

### Example error messages

Manifest validation errors:

- ```
  Invalid JSON syntax: Unexpected token } in JSON at position 142
  ```

  : check for missing commas, extra commas, or unquoted strings
- ```
  Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required
  ```

  : a required field is missing
- ```
  Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...
  ```

  : JSON syntax error

- ```
  Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.
  ```

  : command path exists but contains no valid command files
- ```
  Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.
  ```

  : the

  ```
  source
  ```

  path in marketplace.json points to a non-existent directory
- ```
  Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.
  ```

  : remove duplicate component definitions or remove

  ```
  strict: false
  ```

  in marketplace entry

### Hook troubleshooting

Hook script not executing:

- Check the script is executable:

  ```
  chmod +x ./scripts/your-script.sh
  ```
- Verify the shebang line: First line should be

  ```
  #!/bin/bash
  ```

  or

  ```
  #!/usr/bin/env bash
  ```
- Check the path uses

  ```
  ${CLAUDE_PLUGIN_ROOT}
  ```

  :

  ```
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"
  ```
- Test the script manually:

  ```
  ./scripts/your-script.sh
  ```

- Verify the event name is correct (case-sensitive):

  ```
  PostToolUse
  ```

  , not

  ```
  postToolUse
  ```
- Check the matcher pattern matches your tools:

  ```
  "matcher": "Write|Edit"
  ```

  for file operations
- Confirm the hook type is valid:

  ```
  command
  ```

  ,

  ```
  http
  ```

  ,

  ```
  mcp_tool
  ```

  ,

  ```
  prompt
  ```

  , or

  ```
  agent
  ```

### MCP server troubleshooting

Server not starting:

- Check the command exists and is executable
- Verify all paths use

  ```
  ${CLAUDE_PLUGIN_ROOT}
  ```

  variable
- Check the MCP server logs:

  ```
  claude --debug
  ```

  shows initialization errors
- Test the server manually outside of Claude Code

- Ensure the server is properly configured in

  ```
  .mcp.json
  ```

  or

  ```
  plugin.json
  ```
- Verify the server implements the MCP protocol correctly
- Check for connection timeouts in debug output

### Directory structure mistakes

Symptoms: Plugin loads but components (skills, agents, hooks) are missing. Correct structure: Components must be at the plugin root, not inside

```
.claude-plugin/
```

. Only

```
plugin.json
```

belongs in

```
.claude-plugin/
```

.

```
.claude-plugin/
```

, move them to the plugin root.
Debug checklist:

- Run

  ```
  claude --debug
  ```

  and look for “loading plugin” messages
- Check that each component directory is listed in the debug output
- Verify file permissions allow reading the plugin files

## Distribution and versioning reference

### Version management

Claude Code uses the plugin’s version as the cache key that determines whether an update is available. When you run

```
/plugin update
```

or auto-update fires, Claude Code computes the current version and skips the update if it matches what’s already installed.
The version is resolved from the first of these that is set:

- The

  ```
  version
  ```

  field in the plugin’s

  ```
  plugin.json
  ```
- The

  ```
  version
  ```

  field in the plugin’s marketplace entry in

  ```
  marketplace.json
  ```
- The git commit SHA of the plugin’s source, for

  ```
  github
  ```

  ,

  ```
  url
  ```

  ,

  ```
  git-subdir
  ```

  , and relative-path sources in a git-hosted marketplace
- ```
  unknown
  ```

  , for

  ```
  npm
  ```

  sources or local directories not inside a git repository

ApproachHowUpdate behaviorBest forExplicit versionSet

```
"version": "2.1.0"
```

in

```
plugin.json
```

Users get updates only when you bump this field. Pushing new commits without bumping it has no effect, and

```
/plugin update
```

reports “already at the latest version”.Published plugins with stable release cyclesCommit-SHA versionOmit

```
version
```

from both

```
plugin.json
```

and the marketplace entryUsers get updates on every new commit to the plugin’s git sourceInternal or team plugins under active development

[semantic versioning](https://semver.org)(

```
MAJOR.MINOR.PATCH
```

): bump MAJOR for breaking changes, MINOR for new features, PATCH for bug fixes. Document changes in a

```
CHANGELOG.md
```

.

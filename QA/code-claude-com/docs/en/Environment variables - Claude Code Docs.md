---
title: Environment variables - Claude Code Docs
source_url: https://code.claude.com/docs/en/env-vars
description: Complete reference for environment variables that control Claude Code
  behavior.
---

```
claude
```

, or configure them in

[[Claude Code settings - Claude Code Docs#Available settings|under the]]

```
settings.json
```

```
env
```

key to apply them to every session or roll them out across your team.

VariablePurpose

```
ANTHROPIC_API_KEY
```

API key sent as

```
X-Api-Key
```

header. When set, this key is used instead of your Claude Pro, Max, Team, or Enterprise subscription even if you are logged in. In non-interactive mode (

```
-p
```

), the key is always used when present. In interactive mode, you are prompted to approve the key once before it overrides your subscription. To use your subscription instead, run

```
unset ANTHROPIC_API_KEY
```

```
ANTHROPIC_AUTH_TOKEN
```

Custom value for the

```
Authorization
```

header (the value you set here will be prefixed with

```
Bearer
```

)

```
ANTHROPIC_BASE_URL
```

Override the API endpoint to route requests through a proxy or gateway. When set to a non-first-party host,

```
ENABLE_TOOL_SEARCH=true
```

if your proxy forwards

```
tool_reference
```

blocks

```
ANTHROPIC_BEDROCK_BASE_URL
```

[[LLM gateway configuration - Claude Code Docs|LLM gateway]]. See[[Claude Code on Amazon Bedrock - Claude Code Docs|Amazon Bedrock]]

```
ANTHROPIC_BEDROCK_MANTLE_BASE_URL
```

[[Claude Code on Amazon Bedrock - Claude Code Docs#Use the Mantle endpoint|Mantle endpoint]]

```
ANTHROPIC_BETAS
```

```
anthropic-beta
```

header values to include in API requests. Claude Code already sends the beta headers it needs; use this to opt into an [Anthropic API beta](https://platform.claude.com/docs/en/api/beta-headers)before Claude Code adds native support. Unlike the[[CLI reference - Claude Code Docs|, which requires API key authentication, this variable works with all auth methods including Claude.ai subscription]]

```
--betas
```

flag

```
ANTHROPIC_CUSTOM_HEADERS
```

```
Name: Value
```

format, newline-separated for multiple headers)

```
ANTHROPIC_CUSTOM_MODEL_OPTION
```

```
/model
```

picker. Use this to make a non-standard or gateway-specific model selectable without replacing built-in aliases. See [[Model configuration - Claude Code Docs#Add a custom model option|Model configuration]]

```
ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION
```

```
/model
```

picker. Defaults to

```
Custom model (<model-id>)
```

when not set

```
ANTHROPIC_CUSTOM_MODEL_OPTION_NAME
```

```
/model
```

picker. Defaults to the model ID when not set

```
ANTHROPIC_CUSTOM_MODEL_OPTION_SUPPORTED_CAPABILITIES
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_DEFAULT_HAIKU_MODEL
```

[[Model configuration - Claude Code Docs#Environment variables|Model configuration]]

```
ANTHROPIC_DEFAULT_HAIKU_MODEL_DESCRIPTION
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_DEFAULT_HAIKU_MODEL_SUPPORTED_CAPABILITIES
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_DEFAULT_OPUS_MODEL
```

[[Model configuration - Claude Code Docs#Environment variables|Model configuration]]

```
ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_DEFAULT_OPUS_MODEL_NAME
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_DEFAULT_SONNET_MODEL
```

[[Model configuration - Claude Code Docs#Environment variables|Model configuration]]

```
ANTHROPIC_DEFAULT_SONNET_MODEL_DESCRIPTION
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_DEFAULT_SONNET_MODEL_NAME
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_DEFAULT_SONNET_MODEL_SUPPORTED_CAPABILITIES
```

[[Model configuration - Claude Code Docs#Customize pinned model display and capabilities|Model configuration]]

```
ANTHROPIC_FOUNDRY_API_KEY
```

[[Claude Code on Microsoft Foundry - Claude Code Docs|Microsoft Foundry]])

```
ANTHROPIC_FOUNDRY_BASE_URL
```

```
https://my-resource.services.ai.azure.com/anthropic
```

). Alternative to

```
ANTHROPIC_FOUNDRY_RESOURCE
```

(see [[Claude Code on Microsoft Foundry - Claude Code Docs|Microsoft Foundry]])

```
ANTHROPIC_FOUNDRY_RESOURCE
```

```
my-resource
```

). Required if

```
ANTHROPIC_FOUNDRY_BASE_URL
```

is not set (see [[Claude Code on Microsoft Foundry - Claude Code Docs|Microsoft Foundry]])

```
ANTHROPIC_MODEL
```

[[Model configuration - Claude Code Docs#Environment variables|Model Configuration]])

```
ANTHROPIC_SMALL_FAST_MODEL
```

[[Manage costs effectively - Claude Code Docs|Haiku-class model for background tasks]]

```
ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION
```

```
ANTHROPIC_VERTEX_BASE_URL
```

[[LLM gateway configuration - Claude Code Docs|LLM gateway]]. See[[Claude Code on Google Vertex AI - Claude Code Docs|Google Vertex AI]]

```
ANTHROPIC_VERTEX_PROJECT_ID
```

[[Claude Code on Google Vertex AI - Claude Code Docs|Google Vertex AI]]

```
API_TIMEOUT_MS
```

```
AWS_BEARER_TOKEN_BEDROCK
```

[Bedrock API keys](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/))

```
BASH_DEFAULT_TIMEOUT_MS
```

```
BASH_MAX_OUTPUT_LENGTH
```

```
BASH_MAX_TIMEOUT_MS
```

```
CCR_FORCE_BUNDLE
```

```
1
```

to force [[Use Claude Code on the web - Claude Code Docs#Send local repositories without GitHub|to bundle and upload your local repository even when GitHub access is available]]

```
claude --remote
```

```
CLAUDECODE
```

```
1
```

in shell environments Claude Code spawns (Bash tool, tmux sessions). Not set in [[Hooks reference - Claude Code Docs|hooks]]or[[Customize your status line - Claude Code Docs|status line]]commands. Use to detect when a script is running inside a shell spawned by Claude Code

```
CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS
```

```
1
```

to disable all built-in [[Create custom subagents - Claude Code Docs|subagent]]types such as Explore and Plan. Only applies in non-interactive mode (the

```
-p
```

flag). Useful for SDK users who want a blank slate

```
CLAUDE_AGENT_SDK_MCP_NO_PREFIX
```

```
1
```

to skip the

```
mcp__<server>__
```

prefix on tool names from SDK-created MCP servers. Tools use their original names. SDK usage only

```
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE
```

```
50
```

to compact earlier. Values above the default threshold have no effect. Applies to both main conversations and subagents. This percentage aligns with the

```
context_window.used_percentage
```

field available in [[Customize your status line - Claude Code Docs|status line]]

```
CLAUDE_AUTO_BACKGROUND_TASKS
```

```
1
```

to force-enable automatic backgrounding of long-running agent tasks. When enabled, subagents are moved to the background after running for approximately two minutes

```
CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR
```

```
CLAUDE_CODE_ACCESSIBILITY
```

```
1
```

to keep the native terminal cursor visible and disable the inverted-text cursor indicator. Allows screen magnifiers like macOS Zoom to track cursor position

```
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD
```

```
1
```

to load memory files from directories specified with

```
--add-dir
```

. Loads

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

. By default, additional directories do not load memory files

```
CLAUDE_CODE_API_KEY_HELPER_TTL_MS
```

[[Claude Code settings - Claude Code Docs#Available settings|)]]

```
apiKeyHelper
```

```
CLAUDE_CODE_AUTO_COMPACT_WINDOW
```

[[Model configuration - Claude Code Docs#Extended context|extended context]]models. Use a lower value like

```
500000
```

on a 1M model to treat the window as 500K for compaction purposes. The value is capped at the model’s actual context window.

```
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE
```

is applied as a percentage of this value. Setting this variable decouples the compaction threshold from the status line’s

```
used_percentage
```

, which always uses the model’s full context window

```
CLAUDE_CODE_AUTO_CONNECT_IDE
```

[[Use Claude Code in VS Code - Claude Code Docs|IDE connection]]. By default, Claude Code connects automatically when launched inside a supported IDE’s integrated terminal. Set to

```
false
```

to prevent this. Set to

```
true
```

to force a connection attempt when auto-detection fails, such as when tmux obscures the parent terminal

```
CLAUDE_CODE_CERT_STORE
```

```
bundled
```

is the Mozilla CA set shipped with Claude Code.

```
system
```

is the operating system trust store. Default is

```
bundled,system
```

. The native binary distribution is required for system store integration. On the Node.js runtime, only the bundled set is used regardless of this value

```
CLAUDE_CODE_CLIENT_CERT
```

```
CLAUDE_CODE_CLIENT_KEY
```

```
CLAUDE_CODE_CLIENT_KEY_PASSPHRASE
```

```
CLAUDE_CODE_DEBUG_LOGS_DIR
```

```
--debug
```

or

```
/debug
```

: setting this variable alone does not enable logging. The [[CLI reference - Claude Code Docs|flag does both at once. Defaults to]]

```
--debug-file
```

```
~/.claude/debug/<session-id>.txt
```

```
CLAUDE_CODE_DEBUG_LOG_LEVEL
```

```
verbose
```

,

```
debug
```

(default),

```
info
```

,

```
warn
```

,

```
error
```

. Set to

```
verbose
```

to include high-volume diagnostics like full status line command output, or raise to

```
error
```

to reduce noise

```
CLAUDE_CODE_DISABLE_1M_CONTEXT
```

```
1
```

to disable [[Model configuration - Claude Code Docs#Extended context|1M context window]]support. When set, 1M model variants are unavailable in the model picker. Useful for enterprise environments with compliance requirements

```
CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING
```

```
1
```

to disable [[Model configuration - Claude Code Docs#Adjust effort level|adaptive reasoning]]on Opus 4.6 and Sonnet 4.6 and fall back to the fixed thinking budget controlled by

```
MAX_THINKING_TOKENS
```

. Has no effect on Opus 4.7, which always uses adaptive reasoning

```
CLAUDE_CODE_DISABLE_ATTACHMENTS
```

```
1
```

to disable attachment processing. File mentions with

```
@
```

syntax are sent as plain text instead of being expanded into file content

```
CLAUDE_CODE_DISABLE_AUTO_MEMORY
```

```
1
```

to disable [[How Claude remembers your project - Claude Code Docs#Auto memory|auto memory]]. Set to

```
0
```

to force auto memory on during the gradual rollout. When disabled, Claude does not create or load auto memory files

```
CLAUDE_CODE_DISABLE_BACKGROUND_TASKS
```

```
1
```

to disable all background task functionality, including the

```
run_in_background
```

parameter on Bash and subagent tools, auto-backgrounding, and the Ctrl+B shortcut

```
CLAUDE_CODE_DISABLE_CLAUDE_MDS
```

```
1
```

to prevent loading any CLAUDE.md memory files into context, including user, project, and auto-memory files

```
CLAUDE_CODE_DISABLE_CRON
```

```
1
```

to disable [[Run prompts on a schedule - Claude Code Docs|scheduled tasks]]. The

```
/loop
```

skill and cron tools become unavailable and any already-scheduled tasks stop firing, including tasks that are already running mid-session

```
CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS
```

```
1
```

to strip Anthropic-specific

```
anthropic-beta
```

request headers and beta tool-schema fields (such as

```
defer_loading
```

and

```
eager_input_streaming
```

) from API requests. Use this when a proxy gateway rejects requests with errors like “Unexpected value(s) for the

```
anthropic-beta
```

header” or “Extra inputs are not permitted”. Standard fields (

```
name
```

,

```
description
```

,

```
input_schema
```

,

```
cache_control
```

) are preserved.

```
CLAUDE_CODE_DISABLE_FAST_MODE
```

```
1
```

to disable [[Speed up responses with fast mode - Claude Code Docs|fast mode]]

```
CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY
```

```
1
```

to disable the “How is Claude doing?” session quality surveys. Surveys are also disabled when

```
DISABLE_TELEMETRY
```

or

```
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC
```

is set. See [[Data usage - Claude Code Docs#Session quality surveys|Session quality surveys]]

```
CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING
```

```
1
```

to disable file [[Checkpointing - Claude Code Docs|checkpointing]]. The

```
/rewind
```

command will not be able to restore code changes

```
CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS
```

```
1
```

to remove built-in commit and PR workflow instructions and the git status snapshot from Claude’s system prompt. Useful when using your own git workflow skills. Takes precedence over the [[Claude Code settings - Claude Code Docs#Available settings|setting when set]]

```
includeGitInstructions
```

```
CLAUDE_CODE_DISABLE_LEGACY_MODEL_REMAP
```

```
1
```

to prevent automatic remapping of Opus 4.0 and 4.1 to the current Opus version on the Anthropic API. Use when you intentionally want to pin an older model. The remap does not run on Bedrock, Vertex, or Foundry

```
CLAUDE_CODE_DISABLE_MOUSE
```

```
1
```

to disable mouse tracking in [[Fullscreen rendering - Claude Code Docs|fullscreen rendering]]. Keyboard scrolling with

```
PgUp
```

and

```
PgDn
```

still works. Use this to keep your terminal’s native copy-on-select behavior

```
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC
```

```
DISABLE_AUTOUPDATER
```

,

```
DISABLE_FEEDBACK_COMMAND
```

,

```
DISABLE_ERROR_REPORTING
```

, and

```
DISABLE_TELEMETRY
```

```
CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK
```

```
1
```

to disable the non-streaming fallback when a streaming request fails mid-stream. Streaming errors propagate to the retry layer instead. Useful when a proxy or gateway causes the fallback to produce duplicate tool execution

```
CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL
```

```
1
```

to skip automatic addition of the official plugin marketplace on first run

```
CLAUDE_CODE_DISABLE_TERMINAL_TITLE
```

```
1
```

to disable automatic terminal title updates based on conversation context

```
CLAUDE_CODE_DISABLE_THINKING
```

```
1
```

to force-disable [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)regardless of model support or other settings. More direct than

```
MAX_THINKING_TOKENS=0
```

```
CLAUDE_CODE_DISABLE_VIRTUAL_SCROLL
```

```
1
```

to disable virtual scrolling in [[Fullscreen rendering - Claude Code Docs|fullscreen rendering]]and render every message in the transcript. Use this if scrolling in fullscreen mode shows blank regions where messages should appear

```
CLAUDE_CODE_EFFORT_LEVEL
```

```
low
```

,

```
medium
```

,

```
high
```

,

```
xhigh
```

,

```
max
```

, or

```
auto
```

to use the model default. Available levels depend on the model. Takes precedence over

```
/effort
```

and the

```
effortLevel
```

setting. See [[Model configuration - Claude Code Docs#Adjust effort level|Adjust effort level]]

```
CLAUDE_CODE_ENABLE_AWAY_SUMMARY
```

[[Interactive mode - Claude Code Docs#Session recap|session recap]]availability. Set to

```
0
```

to force recaps off regardless of the

```
/config
```

toggle. Set to

```
1
```

to force recaps on when [[Claude Code settings - Claude Code Docs#Available settings|is]]

```
awaySummaryEnabled
```

```
false
```

. Takes precedence over the setting and

```
/config
```

toggle

```
CLAUDE_CODE_ENABLE_BACKGROUND_PLUGIN_REFRESH
```

```
1
```

to refresh plugin state at turn boundaries in [[Run Claude Code programmatically - Claude Code Docs|non-interactive mode]]after a background install completes. Off by default because the refresh changes the system prompt mid-session, which invalidates[prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)for that turn

```
CLAUDE_CODE_ENABLE_FINE_GRAINED_TOOL_STREAMING
```

```
1
```

to force-enable fine-grained tool input streaming. Without this, the API buffers tool input parameters fully before sending delta events, which can delay display on large tool inputs. Anthropic API only: has no effect on Bedrock, Vertex, or Foundry

```
CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION
```

```
false
```

to disable prompt suggestions (the “Prompt suggestions” toggle in

```
/config
```

). These are the grayed-out predictions that appear in your prompt input after Claude responds. See [[Interactive mode - Claude Code Docs#Prompt suggestions|Prompt suggestions]]

```
CLAUDE_CODE_ENABLE_TASKS
```

```
1
```

to enable the task tracking system in non-interactive mode (the

```
-p
```

flag). Tasks are on by default in interactive mode. See [[Interactive mode - Claude Code Docs#Task list|Task list]]

```
CLAUDE_CODE_ENABLE_TELEMETRY
```

```
1
```

to enable OpenTelemetry data collection for metrics and logging. Required before configuring OTel exporters. See [[Monitoring - Claude Code Docs|Monitoring]]

```
CLAUDE_CODE_EXIT_AFTER_STOP_DELAY
```

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
```

```
1
```

to enable [[Orchestrate teams of Claude Code sessions - Claude Code Docs|agent teams]]. Agent teams are experimental and disabled by default

```
CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS
```

```
CLAUDE_CODE_FORK_SUBAGENT
```

```
1
```

to enable [[Create custom subagents - Claude Code Docs#Fork the current conversation|forked subagents]]. A forked subagent inherits the full conversation context from the main session instead of starting fresh. When enabled,

```
/fork
```

spawns a forked subagent rather than acting as an alias for [[Commands - Claude Code Docs|, and all subagent spawns run in the background. Interactive mode only]]

```
/branch
```

```
CLAUDE_CODE_GIT_BASH_PATH
```

```
bash.exe
```

). Use when Git Bash is installed but not in your PATH. See [[Advanced setup - Claude Code Docs#Set up on Windows|Windows setup]]

```
CLAUDE_CODE_GLOB_HIDDEN
```

```
false
```

to exclude dotfiles from results when Claude invokes the [[Tools reference - Claude Code Docs|Glob tool]]. Included by default. Does not affect

```
@
```

file autocomplete,

```
ls
```

, Grep, or Read

```
CLAUDE_CODE_GLOB_NO_IGNORE
```

```
false
```

to make the [[Tools reference - Claude Code Docs|Glob tool]]respect

```
.gitignore
```

patterns. By default, Glob returns all matching files including gitignored ones. Does not affect

```
@
```

file autocomplete, which has its own

```
respectGitignore
```

setting

```
CLAUDE_CODE_GLOB_TIMEOUT_SECONDS
```

```
CLAUDE_CODE_HIDE_CWD
```

```
1
```

to hide the working directory in the startup logo. Useful for screenshares or recordings where the path exposes your OS username

```
CLAUDE_CODE_IDE_HOST_OVERRIDE
```

```
CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL
```

[[Claude Code settings - Claude Code Docs#Global config settings|to]]

```
autoInstallIdeExtension
```

```
false
```

```
CLAUDE_CODE_IDE_SKIP_VALID_CHECK
```

```
1
```

to skip validation of IDE lockfile entries during connection. Use when auto-connect fails to find your IDE despite it running

```
CLAUDE_CODE_MAX_CONTEXT_TOKENS
```

```
DISABLE_COMPACT
```

is also set. Use this when routing to a model through

```
ANTHROPIC_BASE_URL
```

whose context window does not match the built-in size for its name

```
CLAUDE_CODE_MAX_OUTPUT_TOKENS
```

[max output tokens](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison). Increasing this value reduces the effective context window available before[[Manage costs effectively - Claude Code Docs#Reduce token usage|auto-compaction]]triggers.

```
CLAUDE_CODE_MAX_RETRIES
```

```
CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY
```

```
CLAUDE_CODE_NEW_INIT
```

```
1
```

to make

```
/init
```

run an interactive setup flow. The flow asks which files to generate, including CLAUDE.md, skills, and hooks, before exploring the codebase and writing them. Without this variable,

```
/init
```

generates a CLAUDE.md automatically without prompting.

```
CLAUDE_CODE_NO_FLICKER
```

```
1
```

to enable [[Fullscreen rendering - Claude Code Docs|fullscreen rendering]], a research preview that reduces flicker and keeps memory flat in long conversations. Equivalent to the[[Claude Code settings - Claude Code Docs#Available settings|setting; you can also switch with]]

```
tui
```

```
/tui fullscreen
```

```
CLAUDE_CODE_OAUTH_REFRESH_TOKEN
```

```
claude auth login
```

exchanges this token directly instead of opening a browser. Requires

```
CLAUDE_CODE_OAUTH_SCOPES
```

. Useful for provisioning authentication in automated environments

```
CLAUDE_CODE_OAUTH_SCOPES
```

```
"user:profile user:inference user:sessions:claude_code"
```

. Required when

```
CLAUDE_CODE_OAUTH_REFRESH_TOKEN
```

is set

```
CLAUDE_CODE_OAUTH_TOKEN
```

```
/login
```

for SDK and automated environments. Takes precedence over keychain-stored credentials. Generate one with

```
claude setup-token
```

```
CLAUDE_CODE_OTEL_FLUSH_TIMEOUT_MS
```

[[Monitoring - Claude Code Docs|Monitoring]]

```
CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS
```

[[Monitoring - Claude Code Docs#Dynamic headers|Dynamic headers]]

```
CLAUDE_CODE_OTEL_SHUTDOWN_TIMEOUT_MS
```

[[Monitoring - Claude Code Docs|Monitoring]]

```
CLAUDE_CODE_PERFORCE_MODE
```

```
1
```

to enable Perforce-aware write protection. When set, Edit, Write, and NotebookEdit fail with a

```
p4 edit <file>
```

hint if the target file lacks the owner-write bit, which Perforce clears on synced files until

```
p4 edit
```

opens them. This prevents Claude Code from bypassing Perforce change tracking

```
CLAUDE_CODE_PLUGIN_CACHE_DIR
```

```
~/.claude/plugins
```

```
CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS
```

[[Create and distribute a plugin marketplace - Claude Code Docs#Git operations time out|Git operations time out]]

```
CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE
```

```
1
```

to keep the existing marketplace cache when a

```
git pull
```

fails instead of wiping and re-cloning. Useful in offline or airgapped environments where re-cloning would fail the same way. See [[Create and distribute a plugin marketplace - Claude Code Docs#Marketplace updates fail in offline environments|Marketplace updates fail in offline environments]]

```
CLAUDE_CODE_PLUGIN_SEED_DIR
```

```
:
```

on Unix or

```
;
```

on Windows. Use this to bundle a pre-populated plugins directory into a container image. Claude Code registers marketplaces from these directories at startup and uses pre-cached plugins without re-cloning. See [[Create and distribute a plugin marketplace - Claude Code Docs#Pre-populate plugins for containers|Pre-populate plugins for containers]]

```
CLAUDE_CODE_PROXY_RESOLVES_HOSTS
```

```
1
```

to allow the proxy to perform DNS resolution instead of the caller. Opt-in for environments where the proxy should handle hostname resolution

```
CLAUDE_CODE_REMOTE
```

```
true
```

when Claude Code is running as a [[Use Claude Code on the web - Claude Code Docs|cloud session]]. Read this from a hook or setup script to detect whether you are in a cloud environment

```
CLAUDE_CODE_REMOTE_SESSION_ID
```

[[Use Claude Code on the web - Claude Code Docs|cloud sessions]]to the current session’s ID. Read this to construct a link back to the session transcript. See[[Use Claude Code on the web - Claude Code Docs#Link artifacts back to the session|Link artifacts back to the session]]

```
CLAUDE_CODE_RESUME_INTERRUPTED_TURN
```

```
1
```

to automatically resume if the previous session ended mid-turn. Used in SDK mode so the model continues without requiring the SDK to re-send the prompt

```
CLAUDE_CODE_SCRIPT_CAPS
```

```
CLAUDE_CODE_SUBPROCESS_ENV_SCRUB
```

is set. Keys are substrings matched against the command text; values are integer call limits. For example,

```
{"deploy.sh": 2}
```

allows

```
deploy.sh
```

to be called at most twice. Matching is substring-based so shell-expansion tricks like

```
./scripts/deploy.sh $(evil)
```

still count against the cap. Runtime fan-out via

```
xargs
```

or

```
find -exec
```

is not detected; this is a defense-in-depth control

```
CLAUDE_CODE_SCROLL_SPEED
```

[[Fullscreen rendering - Claude Code Docs#Mouse wheel scrolling|fullscreen rendering]]. Accepts values from 1 to 20. Set to

```
3
```

to match

```
vim
```

if your terminal sends one wheel event per notch without amplification

```
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS
```

[[Hooks reference - Claude Code Docs#SessionEnd|SessionEnd]]hooks. Applies to session exit,

```
/clear
```

, and switching sessions via interactive

```
/resume
```

. By default the budget is 1.5 seconds, automatically raised to the highest per-hook

```
timeout
```

configured in settings files, up to 60 seconds. Timeouts on plugin-provided hooks do not raise the budget

```
CLAUDE_CODE_SHELL
```

```
bash
```

vs

```
zsh
```

)

```
CLAUDE_CODE_SHELL_PREFIX
```

```
/path/to/logger.sh
```

will execute

```
/path/to/logger.sh <command>
```

```
CLAUDE_CODE_SIMPLE
```

```
1
```

to run with a minimal system prompt and only the Bash, file read, and file edit tools. MCP tools from

```
--mcp-config
```

are still available. Disables auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md. The [[Run Claude Code programmatically - Claude Code Docs#Start faster with bare mode|CLI flag sets this]]

```
--bare
```

```
CLAUDE_CODE_SIMPLE_SYSTEM_PROMPT
```

```
1
```

to use the minimal system prompt and collapsed tool descriptions from

```
CLAUDE_CODE_SIMPLE
```

without the other simple-mode changes. The full tool set, hooks, MCP servers, and CLAUDE.md discovery remain enabled

```
CLAUDE_CODE_SKIP_BEDROCK_AUTH
```

```
CLAUDE_CODE_SKIP_FOUNDRY_AUTH
```

```
CLAUDE_CODE_SKIP_MANTLE_AUTH
```

```
CLAUDE_CODE_SKIP_PROMPT_HISTORY
```

```
1
```

to skip writing prompt history and session transcripts to disk. Sessions started with this variable set do not appear in

```
--resume
```

,

```
--continue
```

, or up-arrow history. Useful for ephemeral scripted sessions

```
CLAUDE_CODE_SKIP_VERTEX_AUTH
```

```
CLAUDE_CODE_SUBAGENT_MODEL
```

[[Model configuration - Claude Code Docs|Model configuration]]

```
CLAUDE_CODE_SUBPROCESS_ENV_SCRUB
```

```
1
```

to strip Anthropic and cloud provider credentials from subprocess environments (Bash tool, hooks, MCP stdio servers). The parent Claude process keeps these credentials for API calls, but child processes cannot read them, reducing exposure to prompt injection attacks that attempt to exfiltrate secrets via shell expansion. On Linux, this also runs Bash subprocesses in an isolated PID namespace so they cannot read host process environments via

```
/proc
```

; as a side effect,

```
ps
```

,

```
pgrep
```

, and

```
kill
```

cannot see or signal host processes.

```
claude-code-action
```

sets this automatically when

```
allowed_non_write_users
```

is configured

```
CLAUDE_CODE_SYNC_PLUGIN_INSTALL
```

```
1
```

in non-interactive mode (the

```
-p
```

flag) to wait for plugin installation to complete before the first query. Without this, plugins install in the background and may not be available on the first turn. Combine with

```
CLAUDE_CODE_SYNC_PLUGIN_INSTALL_TIMEOUT_MS
```

to bound the wait

```
CLAUDE_CODE_SYNC_PLUGIN_INSTALL_TIMEOUT_MS
```

```
CLAUDE_CODE_SYNTAX_HIGHLIGHT
```

```
false
```

to disable syntax highlighting in diff output. Useful when colors interfere with your terminal setup

```
CLAUDE_CODE_TASK_LIST_ID
```

[[Interactive mode - Claude Code Docs#Task list|Task list]]

```
CLAUDE_CODE_TEAM_NAME
```

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|agent team]]members

```
CLAUDE_CODE_TMPDIR
```

```
/claude-{uid}/
```

(Unix) or

```
/claude/
```

(Windows) to this path. Default:

```
/tmp
```

on macOS,

```
os.tmpdir()
```

on Linux/Windows

```
CLAUDE_CODE_TMUX_TRUECOLOR
```

```
1
```

to allow 24-bit truecolor output inside tmux. By default, Claude Code clamps to 256 colors when

```
$TMUX
```

is set because tmux does not pass through truecolor escape sequences unless configured to. Set this after adding

```
set -ga terminal-overrides ',*:Tc'
```

to your

```
~/.tmux.conf
```

. See [[Configure your terminal for Claude Code - Claude Code Docs|Terminal configuration]]for other tmux settings

```
CLAUDE_CODE_USE_BEDROCK
```

[[Claude Code on Amazon Bedrock - Claude Code Docs|Bedrock]]

```
CLAUDE_CODE_USE_FOUNDRY
```

[[Claude Code on Microsoft Foundry - Claude Code Docs|Microsoft Foundry]]

```
CLAUDE_CODE_USE_MANTLE
```

[[Claude Code on Amazon Bedrock - Claude Code Docs#Use the Mantle endpoint|Mantle endpoint]]

```
CLAUDE_CODE_USE_POWERSHELL_TOOL
```

```
1
```

to opt in or

```
0
```

to opt out. On Linux, macOS, and WSL, set to

```
1
```

to enable it, which requires

```
pwsh
```

on your

```
PATH
```

. When enabled on Windows, Claude can run PowerShell commands natively instead of routing through Git Bash. See [[Tools reference - Claude Code Docs#PowerShell tool|PowerShell tool]]

```
CLAUDE_CODE_USE_VERTEX
```

[[Claude Code on Google Vertex AI - Claude Code Docs|Vertex]]

```
CLAUDE_CONFIG_DIR
```

```
~/.claude
```

). All settings, credentials, session history, and plugins are stored under this path. Useful for running multiple accounts side by side: for example,

```
alias claude-work='CLAUDE_CONFIG_DIR=~/.claude-work claude'
```

```
CLAUDE_ENABLE_BYTE_WATCHDOG
```

```
1
```

to force-enable the byte-level streaming idle watchdog, or set to

```
0
```

to force-disable it. When unset, the watchdog is enabled by default for Anthropic API connections. The byte watchdog aborts a connection when no bytes arrive on the wire for the duration set by

```
CLAUDE_STREAM_IDLE_TIMEOUT_MS
```

, with a minimum of 5 minutes, independent of the event-level watchdog

```
CLAUDE_ENABLE_STREAM_WATCHDOG
```

```
1
```

to enable the event-level streaming idle watchdog. Off by default. For Bedrock, Vertex, and Foundry, this is the only idle watchdog available. Configure the timeout with

```
CLAUDE_STREAM_IDLE_TIMEOUT_MS
```

```
CLAUDE_ENV_FILE
```

[[Hooks reference - Claude Code Docs#Persist environment variables|SessionStart]],[[Hooks reference - Claude Code Docs#CwdChanged|CwdChanged]], and[[Hooks reference - Claude Code Docs#FileChanged|FileChanged]]hooks

```
CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX
```

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]session names when no explicit name is provided. Defaults to your machine’s hostname, producing names like

```
myhost-graceful-unicorn
```

. The

```
--remote-control-session-name-prefix
```

CLI flag sets the same value for a single invocation

```
CLAUDE_STREAM_IDLE_TIMEOUT_MS
```

```
300000
```

(5 minutes); lower values are silently clamped to absorb extended thinking pauses and proxy buffering. For the event-level watchdog: default

```
90000
```

(90 seconds), no minimum. For third-party providers, requires

```
CLAUDE_ENABLE_STREAM_WATCHDOG=1
```

```
DISABLE_AUTOUPDATER
```

```
1
```

to disable automatic background updates. Manual

```
claude update
```

still works. Use

```
DISABLE_UPDATES
```

to block both

```
DISABLE_AUTO_COMPACT
```

```
1
```

to disable automatic compaction when approaching the context limit. The manual

```
/compact
```

command remains available. Use when you want explicit control over when compaction occurs

```
DISABLE_COMPACT
```

```
1
```

to disable all compaction: both automatic compaction and the manual

```
/compact
```

command

```
DISABLE_COST_WARNINGS
```

```
1
```

to disable cost warning messages

```
DISABLE_DOCTOR_COMMAND
```

```
1
```

to hide the

```
/doctor
```

command. Useful for managed deployments where users should not run installation diagnostics

```
DISABLE_ERROR_REPORTING
```

```
1
```

to opt out of Sentry error reporting

```
DISABLE_EXTRA_USAGE_COMMAND
```

```
1
```

to hide the

```
/extra-usage
```

command that lets users purchase additional usage beyond rate limits

```
DISABLE_FEEDBACK_COMMAND
```

```
1
```

to disable the

```
/feedback
```

command. The older name

```
DISABLE_BUG_COMMAND
```

is also accepted

```
DISABLE_INSTALLATION_CHECKS
```

```
1
```

to disable installation warnings. Use only when manually managing the installation location, as this can mask issues with standard installations

```
DISABLE_INSTALL_GITHUB_APP_COMMAND
```

```
1
```

to hide the

```
/install-github-app
```

command. Already hidden when using third-party providers (Bedrock, Vertex, or Foundry)

```
DISABLE_INTERLEAVED_THINKING
```

```
1
```

to prevent sending the interleaved-thinking beta header. Useful when your LLM gateway or provider does not support [interleaved thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#interleaved-thinking)

```
DISABLE_LOGIN_COMMAND
```

```
1
```

to hide the

```
/login
```

command. Useful when authentication is handled externally via API keys or

```
apiKeyHelper
```

```
DISABLE_LOGOUT_COMMAND
```

```
1
```

to hide the

```
/logout
```

command

```
DISABLE_PROMPT_CACHING
```

```
1
```

to disable prompt caching for all models (takes precedence over per-model settings)

```
DISABLE_PROMPT_CACHING_HAIKU
```

```
1
```

to disable prompt caching for Haiku models

```
DISABLE_PROMPT_CACHING_OPUS
```

```
1
```

to disable prompt caching for Opus models

```
DISABLE_PROMPT_CACHING_SONNET
```

```
1
```

to disable prompt caching for Sonnet models

```
DISABLE_TELEMETRY
```

```
1
```

to opt out of Statsig telemetry (note that Statsig events do not include user data like code, file paths, or bash commands)

```
DISABLE_UPDATES
```

```
1
```

to block all updates including manual

```
claude update
```

and

```
claude install
```

. Stricter than

```
DISABLE_AUTOUPDATER
```

. Use when distributing Claude Code through your own channels and users should not self-update

```
DISABLE_UPGRADE_COMMAND
```

```
1
```

to hide the

```
/upgrade
```

command

```
ENABLE_CLAUDEAI_MCP_SERVERS
```

```
false
```

to disable [[Connect Claude Code to tools via MCP - Claude Code Docs|claude.ai MCP servers]]in Claude Code. Enabled by default for logged-in users

```
ENABLE_PROMPT_CACHING_1H
```

```
1
```

to request a 1-hour prompt cache TTL instead of the default 5 minutes. Intended for API key, [[Claude Code on Amazon Bedrock - Claude Code Docs|Bedrock]],[[Claude Code on Google Vertex AI - Claude Code Docs|Vertex]], and[[Claude Code on Microsoft Foundry - Claude Code Docs|Foundry]]users. Subscription users receive 1-hour TTL automatically. 1-hour cache writes are billed at a higher rate

```
ENABLE_PROMPT_CACHING_1H_BEDROCK
```

```
ENABLE_PROMPT_CACHING_1H
```

instead

```
ENABLE_TOOL_SEARCH
```

[[Connect Claude Code to tools via MCP - Claude Code Docs#Scale with MCP Tool Search|MCP tool search]]. Unset: all MCP tools deferred by default, but loaded upfront on Vertex AI or when

```
ANTHROPIC_BASE_URL
```

points to a non-first-party host. Values:

```
true
```

(always defer including proxies and Vertex AI),

```
auto
```

(threshold mode: load upfront if tools fit within 10% of context),

```
auto:N
```

(custom threshold, e.g.,

```
auto:5
```

for 5%),

```
false
```

(load all upfront)

```
FALLBACK_FOR_ALL_PRIMARY_MODELS
```

[[CLI reference - Claude Code Docs|after repeated overload errors on any primary model. By default, only Opus models trigger the fallback]]

```
--fallback-model
```

```
FORCE_AUTOUPDATE_PLUGINS
```

```
1
```

to force plugin auto-updates even when the main auto-updater is disabled via

```
DISABLE_AUTOUPDATER
```

```
FORCE_PROMPT_CACHING_5M
```

```
1
```

to force the 5-minute prompt cache TTL even when 1-hour TTL would otherwise apply. Overrides

```
ENABLE_PROMPT_CACHING_1H
```

```
HTTP_PROXY
```

```
HTTPS_PROXY
```

```
IS_DEMO
```

```
1
```

to enable demo mode: hides your email and organization name from the header and

```
/status
```

output, and skips onboarding. Useful when streaming or recording a session

```
MAX_MCP_OUTPUT_TOKENS
```

[[Connect Claude Code to tools via MCP - Claude Code Docs#Raise the limit for a specific tool|use that character limit for text content instead, but image content from those tools is still subject to this variable (default: 25000)]]

```
anthropic/maxResultSizeChars
```

```
MAX_STRUCTURED_OUTPUT_RETRIES
```

[[CLI reference - Claude Code Docs|in non-interactive mode (the]]

```
--json-schema
```

```
-p
```

flag). Defaults to 5

```
MAX_THINKING_TOKENS
```

[extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)token budget. The ceiling is the model’s[max output tokens](https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison)minus one. Set to

```
0
```

to disable thinking entirely. On models with [[Model configuration - Claude Code Docs#Adjust effort level|adaptive reasoning]], the budget is ignored unless adaptive reasoning is disabled via

```
CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING
```

```
MCP_CLIENT_SECRET
```

[[Connect Claude Code to tools via MCP - Claude Code Docs#Use pre-configured OAuth credentials|pre-configured credentials]]. Avoids the interactive prompt when adding a server with

```
--client-secret
```

```
MCP_CONNECTION_NONBLOCKING
```

```
true
```

in non-interactive mode (

```
-p
```

) to skip the MCP connection wait entirely. Useful for scripted pipelines where MCP tools are not needed. Without this variable, the first query waits up to 5 seconds for

```
--mcp-config
```

server connections

```
MCP_OAUTH_CALLBACK_PORT
```

```
--callback-port
```

when adding an MCP server with [[Connect Claude Code to tools via MCP - Claude Code Docs#Use pre-configured OAuth credentials|pre-configured credentials]]

```
MCP_REMOTE_SERVER_CONNECTION_BATCH_SIZE
```

```
MCP_SERVER_CONNECTION_BATCH_SIZE
```

```
MCP_TIMEOUT
```

```
MCP_TOOL_TIMEOUT
```

```
NO_PROXY
```

```
OTEL_LOG_RAW_API_BODIES
```

```
api_request_body
```

/

```
api_response_body
```

log events. Set to

```
1
```

for inline bodies truncated at 60 KB, or

```
file:<dir>
```

to write untruncated bodies to disk and emit a

```
body_ref
```

path instead. Disabled by default; bodies include the entire conversation history. See [[Monitoring - Claude Code Docs#API request body event|Monitoring]]

```
OTEL_LOG_TOOL_CONTENT
```

```
1
```

to include tool input and output content in OpenTelemetry span events. Disabled by default to protect sensitive data. See [[Monitoring - Claude Code Docs|Monitoring]]

```
OTEL_LOG_TOOL_DETAILS
```

```
1
```

to include tool input arguments, MCP server names, raw error strings on tool failures, and other tool details in OpenTelemetry traces and logs. Disabled by default to protect PII. See [[Monitoring - Claude Code Docs|Monitoring]]

```
OTEL_LOG_USER_PROMPTS
```

```
1
```

to include user prompt text in OpenTelemetry traces and logs. Disabled by default (prompts are redacted). See [[Monitoring - Claude Code Docs|Monitoring]]

```
OTEL_METRICS_INCLUDE_ACCOUNT_UUID
```

```
false
```

to exclude account UUID from metrics attributes (default: included). See [[Monitoring - Claude Code Docs|Monitoring]]

```
OTEL_METRICS_INCLUDE_SESSION_ID
```

```
false
```

to exclude session ID from metrics attributes (default: included). See [[Monitoring - Claude Code Docs|Monitoring]]

```
OTEL_METRICS_INCLUDE_VERSION
```

```
true
```

to include Claude Code version in metrics attributes (default: excluded). See [[Monitoring - Claude Code Docs|Monitoring]]

```
SLASH_COMMAND_TOOL_CHAR_BUDGET
```

[[Extend Claude with skills - Claude Code Docs#Control who invokes a skill|Skill tool]]. The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters. Legacy name kept for backwards compatibility

```
TASK_MAX_OUTPUT_LENGTH
```

[[Create custom subagents - Claude Code Docs|subagent]]output before truncation (default: 32000, maximum: 160000). When truncated, the full output is saved to disk and the path is included in the truncated response

```
USE_BUILTIN_RIPGREP
```

```
0
```

to use system-installed

```
rg
```

instead of

```
rg
```

included with Claude Code

```
VERTEX_REGION_CLAUDE_3_5_HAIKU
```

```
VERTEX_REGION_CLAUDE_3_5_SONNET
```

```
VERTEX_REGION_CLAUDE_3_7_SONNET
```

```
VERTEX_REGION_CLAUDE_4_0_OPUS
```

```
VERTEX_REGION_CLAUDE_4_0_SONNET
```

```
VERTEX_REGION_CLAUDE_4_1_OPUS
```

```
VERTEX_REGION_CLAUDE_4_5_OPUS
```

```
VERTEX_REGION_CLAUDE_4_5_SONNET
```

```
VERTEX_REGION_CLAUDE_4_6_OPUS
```

```
VERTEX_REGION_CLAUDE_4_6_SONNET
```

```
VERTEX_REGION_CLAUDE_4_7_OPUS
```

```
VERTEX_REGION_CLAUDE_HAIKU_4_5
```

```
OTEL_METRICS_EXPORTER
```

,

```
OTEL_LOGS_EXPORTER
```

,

```
OTEL_EXPORTER_OTLP_ENDPOINT
```

,

```
OTEL_EXPORTER_OTLP_PROTOCOL
```

,

```
OTEL_EXPORTER_OTLP_HEADERS
```

,

```
OTEL_METRIC_EXPORT_INTERVAL
```

,

```
OTEL_RESOURCE_ATTRIBUTES
```

, and signal-specific variants) are also supported. See

[[Monitoring - Claude Code Docs|Monitoring]]for configuration details.

## See also

- [[Claude Code settings - Claude Code Docs|Settings]]: configure environment variables in

  ```
  settings.json
  ```

  so they apply to every session
- [[CLI reference - Claude Code Docs|CLI reference]]: launch-time flags
- [[Enterprise network configuration - Claude Code Docs|Network configuration]]: proxy and TLS setup
- [[Monitoring - Claude Code Docs|Monitoring]]: OpenTelemetry configuration

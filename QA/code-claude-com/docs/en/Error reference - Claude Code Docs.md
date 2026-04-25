---
title: Error reference - Claude Code Docs
source_url: https://code.claude.com/docs/en/errors
description: Look up Claude Code runtime error messages with what each one means and
  how to fix it.
---

```
command not found
```

or TLS failures during setup, see

[[Troubleshooting - Claude Code Docs|Troubleshooting]]. These errors and recovery commands apply across the CLI, the

[[Use Claude Code Desktop - Claude Code Docs|Desktop app]], and

[[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]], since all three wrap the same Claude Code CLI. For surface-specific issues, see the troubleshooting section on that surface’s page.

Claude Code calls the Claude API for model responses, so most runtime errors map to an underlying API error code. This page covers what each error means inside Claude Code and how to recover. For the raw HTTP status code definitions, see the

[Claude Platform error reference](https://platform.claude.com/docs/en/api/errors).

## Find your error

Match the message you see in your terminal to a section below.

MessageSection

```
API Error: 500 ... Internal server error
```

```
API Error: Repeated 529 Overloaded errors
```

[[Error reference - Claude Code Docs#API Error: Repeated 529 Overloaded errors|Server errors]]

```
Request timed out
```

[[Error reference - Claude Code Docs#Request timed out|Server errors]], or[[Error reference - Claude Code Docs#Unable to connect to API|Network]]if the message mentions your internet connection

```
<model> is temporarily unavailable, so auto mode cannot determine the safety of...
```

[[Error reference - Claude Code Docs#Auto mode cannot determine the safety of an action|Server errors]]

```
You've hit your session limit
```

/

```
You've hit your weekly limit
```

[[Error reference - Claude Code Docs#You’ve hit your session limit|Usage limits]]

```
Server is temporarily limiting requests
```

[[Error reference - Claude Code Docs#Server is temporarily limiting requests|Usage limits]]

```
Request rejected (429)
```

[[Error reference - Claude Code Docs#Request rejected (429)|Usage limits]]

```
Credit balance is too low
```

[[Error reference - Claude Code Docs#Credit balance is too low|Usage limits]]

```
Not logged in · Please run /login
```

[[Error reference - Claude Code Docs#Not logged in|Authentication]]

```
Invalid API key
```

[[Error reference - Claude Code Docs#Invalid API key|Authentication]]

```
This organization has been disabled
```

[[Error reference - Claude Code Docs#This organization has been disabled|Authentication]]

```
OAuth token revoked
```

/

```
OAuth token has expired
```

[[Error reference - Claude Code Docs#OAuth token revoked or expired|Authentication]]

```
does not meet scope requirement user:profile
```

[[Error reference - Claude Code Docs#OAuth scope requirement|Authentication]]

```
Unable to connect to API
```

[[Error reference - Claude Code Docs#Unable to connect to API|Network]]

```
SSL certificate verification failed
```

[[Error reference - Claude Code Docs#SSL certificate errors|Network]]

```
Prompt is too long
```

[[Error reference - Claude Code Docs#Prompt is too long|Request errors]]

```
Error during compaction: Conversation too long
```

[[Error reference - Claude Code Docs#Error during compaction: Conversation too long|Request errors]]

```
Request too large
```

[[Error reference - Claude Code Docs#Request too large|Request errors]]

```
Image was too large
```

[[Error reference - Claude Code Docs#Image was too large|Request errors]]

```
PDF too large
```

/

```
PDF is password protected
```

[[Error reference - Claude Code Docs#PDF errors|Request errors]]

```
Extra inputs are not permitted
```

[[Error reference - Claude Code Docs#Extra inputs are not permitted|Request errors]]

```
There's an issue with the selected model
```

[[Error reference - Claude Code Docs#There’s an issue with the selected model|Request errors]]

```
Claude Opus is not available with the Claude Pro plan
```

[[Error reference - Claude Code Docs#Claude Opus is not available with the Claude Pro plan|Request errors]]

```
thinking.type.enabled is not supported for this model
```

[[Error reference - Claude Code Docs|Request errors]]

```
max_tokens must be greater than thinking.budget_tokens
```

[[Error reference - Claude Code Docs#Thinking budget exceeds output limit|Request errors]]

```
API Error: 400 due to tool use concurrency issues
```

[[Error reference - Claude Code Docs#Tool use or thinking block mismatch|Request errors]][[Error reference - Claude Code Docs#Responses seem lower quality than usual|Response quality]]

## Automatic retries

Claude Code retries transient failures before showing you an error. Server errors, overloaded responses, request timeouts, temporary 429 throttles, and dropped connections are all retried up to 10 times with exponential backoff. While retrying, the spinner shows a

```
Retrying in Ns · attempt x/y
```

countdown.
When you see one of the errors on this page, those retries have already been exhausted. You can tune the behavior with two environment variables:

VariableDefaultEffect

```
CLAUDE_CODE_MAX_RETRIES
```

```
API_TIMEOUT_MS
```

## Server errors

These errors come from Anthropic infrastructure rather than your account or request.

### API Error: 500 Internal server error

Claude Code shows the raw API response body for any 5xx status. The example below shows a 500 response:

- Check [status.claude.com](https://status.claude.com)for active incidents
- Wait a minute, then send your message again. Your original message is still in the conversation, so for a long prompt you can type

  ```
  try again
  ```

  instead of pasting the whole thing.
- If the error persists with no posted incident, run

  ```
  /feedback
  ```

  so Anthropic can investigate with your request details. See[[Error reference - Claude Code Docs#Report an error|Report an error]]if

  ```
  /feedback
  ```

  is unavailable on your provider.

### API Error: Repeated 529 Overloaded errors

The API is temporarily at capacity across all users. Claude Code has already retried several times before showing this message:

- Check [status.claude.com](https://status.claude.com)for capacity notices
- Try again in a few minutes
- Run

  ```
  /model
  ```

  and switch to a different model to keep working, since capacity is tracked per model. Claude Code prompts you to do this when one model is under particularly high load, for example

  ```
  Opus is experiencing high load, please use /model to switch to Sonnet
  ```

  .

### Request timed out

The API did not respond before the connection deadline.

- Retry the request
- For long-running tasks, break the work into smaller prompts
- If a slow network or proxy is the cause, raise

  ```
  API_TIMEOUT_MS
  ```

  as described in[[Error reference - Claude Code Docs#Automatic retries|Automatic retries]]
- If timeouts are frequent and your network is otherwise healthy, see [[Error reference - Claude Code Docs#Network and connection errors|Network and connection errors]]below

### Auto mode cannot determine the safety of an action

The model that

[[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|auto mode]]uses to classify actions is overloaded, so auto mode blocked the action instead of approving it unchecked.

- Retry after a few seconds; Claude sees the same message and usually retries on its own
- If retries keep failing, continue with read-only tasks and come back to the blocked action later
- This is transient and unrelated to [[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|auto mode eligibility]]; you do not need to change settings

## Usage limits

These errors mean a quota tied to your account or plan has been reached. They are distinct from

[[Error reference - Claude Code Docs#Server errors|server errors]], which affect everyone.

### You’ve hit your session limit

Subscription plans include a rolling usage allowance. When it runs out you see one of these messages:

- Wait for the reset time shown in the error
- Run

  ```
  /usage
  ```

  to see your plan limits and when they reset
- Run

  ```
  /extra-usage
  ```

  to buy additional usage on Pro and Max, or to request it from your admin on Team and Enterprise. See[Extra usage for paid plans](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)for how this is billed.
- To upgrade your plan for higher base limits, see [claude.com/pricing](https://claude.com/pricing)

```
rate_limits
```

fields to a

[[Customize your status line - Claude Code Docs#Rate limit usage|custom status line]], or in the Desktop app click the

[[Use Claude Code Desktop - Claude Code Docs#Check usage|usage ring]]next to the model picker.

### Server is temporarily limiting requests

The API applied a short-lived throttle that is unrelated to your plan quota.

[[Error reference - Claude Code Docs#Automatic retries|retried automatically]]before being shown. What to do:

- Wait briefly and try again
- Check [status.claude.com](https://status.claude.com)if it persists

### Request rejected (429)

You have hit the rate limit configured for your API key, Amazon Bedrock project, or Google Vertex AI project.

- Run

  ```
  /status
  ```

  and confirm the active credential is the one you expect. A stray

  ```
  ANTHROPIC_API_KEY
  ```

  in your environment can route requests through a low-tier key instead of your subscription.
- Check your provider console for the active limits and request a higher tier if needed
- For Anthropic API keys, see the [rate limits reference](https://platform.claude.com/docs/en/api/rate-limits)for how tiers work and how to set per-workspace caps
- Reduce concurrency: lower , avoid running many parallel subagents, or switch to a smaller model with

  ```
  CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY
  ```

  ```
  /model
  ```

  for high-volume scripted runs

### Credit balance is too low

Your Console organization has run out of prepaid credits.

- Add credits at [platform.claude.com/settings/billing](https://platform.claude.com/settings/billing), and consider enabling auto-reload there so the balance refills before it hits zero
- Switch to subscription authentication with

  ```
  /login
  ```

  if you have a Pro, Max, Team, or Enterprise plan
- Set per-workspace spend caps in the Console to prevent a single project from draining the org balance. See [[Manage costs effectively - Claude Code Docs|Manage costs effectively]].

## Authentication errors

These errors mean Claude Code cannot prove who you are to the API. Run

```
/status
```

at any time to see which credential is currently active.

### Not logged in

No valid credential is available for this session.

- Run

  ```
  /login
  ```

  to authenticate with your Claude subscription or Console account
- If you expected an environment variable to authenticate you, confirm

  ```
  ANTHROPIC_API_KEY
  ```

  is set and exported in the shell where you launched

  ```
  claude
  ```
- For CI or automation where interactive login is not possible, configure an script that fetches a key at startup

  ```
  apiKeyHelper
  ```
- See [[Authentication - Claude Code Docs#Authentication precedence|Authentication precedence]]to understand which credential wins when several are present

[[Troubleshooting - Claude Code Docs#Not logged in or token expired|Not logged in or token expired]]for system clock and macOS Keychain fixes.

### Invalid API key

The

```
ANTHROPIC_API_KEY
```

environment variable or

```
apiKeyHelper
```

script returned a key the API rejected.

- Check for typos and confirm the key has not been revoked in the [Console](https://platform.claude.com/settings/keys)
- Run

  ```
  env | grep ANTHROPIC
  ```

  in the same shell. Tools like direnv, dotenv shell plugins, and IDE terminals can load a stale key from a

  ```
  .env
  ```

  file in your project without you setting it explicitly.
- Unset

  ```
  ANTHROPIC_API_KEY
  ```

  and run

  ```
  /login
  ```

  to use subscription auth instead
- If the key comes from an script, run the script directly to confirm it prints a valid key on stdout

  ```
  apiKeyHelper
  ```
- Run

  ```
  /status
  ```

  to confirm which credential source Claude Code is actually using

### This organization has been disabled

A stale

```
ANTHROPIC_API_KEY
```

from a disabled Console organization is overriding your subscription login.

```
/login
```

, so a key exported in your shell profile or loaded from a

```
.env
```

file is used even when you have a working Pro or Max subscription. In non-interactive mode (

```
-p
```

), the key is always used when present.
What to do:

- Unset

  ```
  ANTHROPIC_API_KEY
  ```

  in the current shell and remove it from your shell profile, then relaunch

  ```
  claude
  ```
- Run

  ```
  /status
  ```

  afterward to confirm the active credential is your subscription
- If no environment variable is set and the error persists, the disabled organization is the one tied to your

  ```
  /login
  ```

  . Contact support or sign in with a different account.

### OAuth token revoked or expired

Your saved login is no longer valid. A revoked token means you signed out everywhere or an admin removed access; an expired token means the automatic refresh failed mid-session.

- Run

  ```
  /login
  ```

  to sign in again
- If the error returns within the same session after re-authenticating, run

  ```
  /logout
  ```

  first to fully clear the stored token, then

  ```
  /login
  ```
- For repeated prompts to log in across launches, see the system clock and macOS Keychain checks in [[Troubleshooting - Claude Code Docs#Not logged in or token expired|Troubleshooting]]
- For other failures including

  ```
  403 Forbidden
  ```

  and OAuth browser issues, see[[Troubleshooting - Claude Code Docs#Permissions and authentication|Permissions and authentication]]

### OAuth scope requirement

The stored token predates a permission scope that a newer feature needs. You see this most often from

```
/usage
```

and the status line usage indicator:

- Run

  ```
  /login
  ```

  to mint a new token with the current scopes. You do not need to log out first.

## Network and connection errors

These errors mean Claude Code could not reach the API at all. They almost always originate in your local network, proxy, or firewall rather than Anthropic infrastructure.

### Unable to connect to API

The TCP connection to the API failed or never completed.

```
api.anthropic.com
```

, or a required corporate proxy that is not configured.
What to do:

- Confirm you can reach the API host from the same shell by running

  ```
  curl -I https://api.anthropic.com
  ```

  . On Windows PowerShell use

  ```
  curl.exe -I https://api.anthropic.com
  ```

  so the built-in

  ```
  Invoke-WebRequest
  ```

  alias is not used.
- If you are behind a corporate proxy, set

  ```
  HTTPS_PROXY
  ```

  before launching Claude Code and see[[Enterprise network configuration - Claude Code Docs|Network configuration]]
- If you route through an LLM gateway or relay, set to its address. See

  ```
  ANTHROPIC_BASE_URL
  ```

  [[LLM gateway configuration - Claude Code Docs|LLM gateway configuration]]for setup.
- Ensure your firewall allows the hosts listed in [[Enterprise network configuration - Claude Code Docs#Network access requirements|Network access requirements]]
- Intermittent failures are [[Error reference - Claude Code Docs#Automatic retries|retried automatically]]; persistent failures point to a local network issue

```
curl
```

succeeds but Claude Code still fails, the cause is usually something between Node.js and the network rather than the network itself:

- On Linux and WSL, check

  ```
  /etc/resolv.conf
  ```

  for an unreachable nameserver. WSL in particular can inherit a broken resolver from the host.
- On macOS, a VPN client that was disconnected or uninstalled can leave a tunnel interface or routing rule behind. Check

  ```
  ifconfig
  ```

  for stale

  ```
  utun
  ```

  interfaces and remove the VPN’s network extension in System Settings.
- Docker Desktop and similar container runtimes can intercept outbound traffic. Quit them and retry to rule this out.

### SSL certificate errors

A proxy or security appliance on your network is intercepting TLS traffic with its own certificate, and Node.js does not trust it.

- Export your organization’s CA bundle and point Node at it with

  ```
  NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.pem
  ```
- See [[Enterprise network configuration - Claude Code Docs#Custom CA certificates|Network configuration]]for full setup instructions
- Do not set

  ```
  NODE_TLS_REJECT_UNAUTHORIZED=0
  ```

  , which disables certificate validation entirely

## Request errors

These errors mean the API received your request but rejected its content.

### Prompt is too long

The conversation plus attached files exceeds the model’s context window.

- Run

  ```
  /compact
  ```

  to summarize earlier turns and free space, or

  ```
  /clear
  ```

  to start fresh
- Run

  ```
  /context
  ```

  to see a breakdown of what is consuming the window: system prompt, tools, memory files, and messages
- Disable MCP servers you are not using with

  ```
  /mcp disable <name>
  ```

  to remove their tool definitions from context
- Trim large

  ```
  CLAUDE.md
  ```

  memory files, or move instructions into[[How Claude remembers your project - Claude Code Docs#Path-specific rules|path-scoped rules]]that load only when relevant
- Subagents inherit every MCP tool definition from the parent session, which can fill their context window before the first turn. Disable MCP servers you are not using before spawning subagents.
- Auto-compact is on by default and normally prevents this error. If you have set , re-enable it or run

  ```
  DISABLE_AUTO_COMPACT
  ```

  ```
  /compact
  ```

  manually before the window fills.

[[Explore the context window - Claude Code Docs|Explore the context window]]for an interactive view of how context fills up.

### Error during compaction: Conversation too long

```
/compact
```

itself failed because there is not enough free context to hold the summary it produces.

```
/compact
```

after seeing

```
Prompt is too long
```

.
What to do:

- Press Esc twice to open the message list and step back several turns. This drops the most recent messages from context. Then run

  ```
  /compact
  ```

  again.
- If stepping back does not free enough space, run

  ```
  /clear
  ```

  to start a fresh session. Your previous conversation is preserved and can be reopened with

  ```
  /resume
  ```

  .

### Request too large

The raw request body exceeded the API’s byte limit before tokenization, usually because of a large pasted file or attachment.

[[Error reference - Claude Code Docs#Prompt is too long|context window limit]]. What to do:

- Press Esc twice and step back past the turn that added the oversized content
- Reference large files by path instead of pasting their contents, so Claude can read them in chunks
- For images, see [[Error reference - Claude Code Docs#Image was too large|Image was too large]]below

### Image was too large

A pasted or attached image exceeds the API’s size or dimension limits.

- Press Esc twice and step back past the turn where the image was added
- Resize the image before pasting. The API accepts images up to 8000 pixels on the longest edge for a single image, or 2000 pixels when many images are in context.
- Take a tighter screenshot of the relevant region instead of the full screen

### PDF errors

The PDF you attached could not be processed.

- For oversized PDFs, ask Claude to read a page range with the Read tool instead of attaching the whole file, or extract text with a tool like

  ```
  pdftotext
  ```

  and reference the output file by path
- For protected or invalid PDFs, remove the password or re-export the file from its source application, then try again

### Extra inputs are not permitted

A proxy or LLM gateway between Claude Code and the API stripped the

```
anthropic-beta
```

request header, so the API rejected fields that depend on it.

```
context_management
```

,

```
effort
```

, and tool

```
input_examples
```

alongside an

```
anthropic-beta
```

header that enables them. When a gateway forwards the body but drops the header, the API sees fields it does not recognize.
What to do:

- Configure your gateway to forward the

  ```
  anthropic-beta
  ```

  header. See[[LLM gateway configuration - Claude Code Docs|LLM gateway configuration]].
- As a fallback, set before launching. This disables features that require the beta header so requests succeed through a gateway that cannot forward it.

  ```
  CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1
  ```

### There’s an issue with the selected model

The configured model name was not recognized or your account lacks access to it.

- Run

  ```
  /model
  ```

  to pick from models available to your account
- Use an alias such as

  ```
  sonnet
  ```

  or

  ```
  opus
  ```

  instead of a full versioned ID. Aliases track the latest release so they do not go stale. See[[Model configuration - Claude Code Docs|Model configuration]].
- See [[Troubleshooting - Claude Code Docs#Model not found or not accessible|Model not found]]to locate where a stale ID is set across

  ```
  --model
  ```

  ,

  ```
  ANTHROPIC_MODEL
  ```

  , and settings files

### Claude Opus is not available with the Claude Pro plan

Your active subscription plan does not include the model you selected.

- Run

  ```
  /model
  ```

  and select a model your plan includes
- If you upgraded your plan recently and still see this, run

  ```
  /logout
  ```

  then

  ```
  /login
  ```

  . The stored token reflects your plan at the time you signed in, so upgrading on the web does not take effect in an existing session until you re-authenticate.
- See [claude.com/pricing](https://claude.com/pricing)for which models each plan includes

### thinking.type.enabled is not supported for this model

Your Claude Code version is older than the minimum for Opus 4.7. The CLI sent a thinking configuration the model no longer accepts.

- Run

  ```
  claude update
  ```

  to upgrade to v2.1.111 or later, then restart Claude Code
- If you cannot upgrade, run

  ```
  /model
  ```

  and select Opus 4.6 or Sonnet instead
- If you hit this in the Agent SDK, see [[Quickstart - Claude Code Docs-1f2ec9#Troubleshooting|SDK troubleshooting]]

### Thinking budget exceeds output limit

The configured extended thinking budget exceeds the maximum response length, so there is no room left for the actual answer.

[[Environment variables - Claude Code Docs|is set higher than the provider’s output limit, or when plan mode raises the thinking budget. What to do:]]

```
MAX_THINKING_TOKENS
```

- Lower

  ```
  MAX_THINKING_TOKENS
  ```

  , or raiseabove the thinking budget

  ```
  CLAUDE_CODE_MAX_OUTPUT_TOKENS
  ```
- See [[Common workflows - Claude Code Docs#Use extended thinking (thinking mode)|Extended thinking]]for how the budget interacts with output length

### Tool use or thinking block mismatch

The conversation history reached the API in an inconsistent state, usually after a tool call was interrupted or a turn was edited mid-stream.

```
tool_use
```

,

```
tool_result
```

, and

```
thinking
```

blocks in history no longer matches what the API expects.
What to do:

- Run

  ```
  /rewind
  ```

  , or press Esc twice, to step back to a checkpoint before the corrupted turn and continue from there. See[[Checkpointing - Claude Code Docs|Checkpointing]]for how checkpoints are created and restored.

## Responses seem lower quality than usual

If Claude’s answers seem less capable than you expect but no error is shown, the cause is usually conversation state rather than the model itself. Claude Code does not silently change model versions. It can switch to a fallback model in specific cases such as an Opus quota being reached or a Bedrock or Vertex AI region lacking your model; the Model selection check below catches both, and

[[Model configuration - Claude Code Docs|Model configuration]]explains when fallback applies. Check these first:

- Model selection: run

  ```
  /model
  ```

  to confirm you are on the model you expect. A previous

  ```
  /model
  ```

  choice or an

  ```
  ANTHROPIC_MODEL
  ```

  environment variable may have you on a smaller model than you intended.
- Effort level: run

  ```
  /effort
  ```

  to check the current reasoning level and raise it for hard debugging or design work. Defaults vary by model, so check before assuming you are below the maximum. See[[Model configuration - Claude Code Docs#Adjust effort level|Adjust effort level]]for per-model defaults and the

  ```
  ultrathink
  ```

  shortcut.
- Context pressure: run

  ```
  /context
  ```

  to see how full the window is. If it is near capacity, run

  ```
  /compact
  ```

  at a natural breakpoint or

  ```
  /clear
  ```

  to start fresh. See[[Explore the context window - Claude Code Docs|Explore the context window]]for how auto-compact affects earlier turns.
- Stale instructions: large or outdated

  ```
  CLAUDE.md
  ```

  files and MCP tool definitions consume context and can steer responses.

  ```
  /doctor
  ```

  flags oversized memory files and subagent definitions;

  ```
  /context
  ```

  shows MCP tool token usage.

```
/rewind
```

to step back to before the bad turn, then rephrase the prompt with more specifics. Correcting in-thread keeps the wrong attempt in context, which can anchor later answers to it. See

[[Checkpointing - Claude Code Docs|Checkpointing]]. If quality still seems off after checking the above, run

```
/feedback
```

and describe what you expected versus what you got. Feedback submitted this way includes the conversation transcript, which is the fastest way for Anthropic to diagnose a real regression. See

[[Error reference - Claude Code Docs#Report an error|Report an error]]if

```
/feedback
```

is unavailable on your provider.

## Report an error

This page covers errors from the Claude API. For errors from other Claude Code components, see the relevant guide:

- MCP server failed to connect or authenticate: [[Connect Claude Code to tools via MCP - Claude Code Docs|MCP]]
- Hook script failed or blocked a tool: [[Hooks reference - Claude Code Docs#Debug hooks|Debug hooks]]
- Permission denied or filesystem errors during install: [[Troubleshooting - Claude Code Docs|Troubleshooting]]

- Run

  ```
  /feedback
  ```

  inside Claude Code to send the transcript and a description to Anthropic. The command also offers to open a prefilled GitHub issue. Feedback is unavailable on Bedrock, Vertex AI, and Foundry deployments.
- Run

  ```
  /doctor
  ```

  to check for local configuration problems
- Check [status.claude.com](https://status.claude.com)for active incidents
- Search [existing issues](https://github.com/anthropics/claude-code/issues)on GitHub

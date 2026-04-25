---
title: Manage costs effectively - Claude Code Docs
source_url: https://code.claude.com/docs/en/costs
description: Track token usage, set team spend limits, and reduce Claude Code costs
  with context management, model selection, extended thinking settings, and preprocessing
  h
---

[claude.com/pricing](https://claude.com/pricing). Per-developer costs vary widely based on model selection, codebase size, and usage patterns such as running multiple instances or automation. Across enterprise deployments, the average cost is around $13 per developer per active day and $150-250 per developer per month, with costs remaining below $30 per active day for 90% of users. To estimate spend for your own team, start with a small pilot group and use the tracking tools below to establish a baseline before wider rollout. This page covers how to

[[Manage costs effectively - Claude Code Docs#Track your costs|track your costs]],

[[Manage costs effectively - Claude Code Docs#Managing costs for teams|manage costs for teams]], and

[[Manage costs effectively - Claude Code Docs#Reduce token usage|reduce token usage]].

## Track your costs

### Using the ``` /usage ``` command

The Session block in

```
/usage
```

shows API token usage and is intended for API users. Claude Max and Pro subscribers have usage included in their subscription, so the session cost figure isn’t relevant for billing purposes. Subscribers see plan usage bars and activity stats on the same screen.

```
/usage
```

command provides detailed token usage statistics for your current session. The dollar figure is an estimate computed locally from token counts and may differ from your actual bill. For authoritative billing, see the Usage page in the

[Claude Console](https://platform.claude.com/usage).

## Managing costs for teams

When using Claude API, you can

[set workspace spend limits](https://platform.claude.com/docs/en/build-with-claude/workspaces#workspace-limits)on the total Claude Code workspace spend. Admins can

[view cost and usage reporting](https://platform.claude.com/docs/en/build-with-claude/workspaces#usage-and-cost-tracking)in the Console.

When you first authenticate Claude Code with your Claude Console account, a workspace called “Claude Code” is automatically created for you. This workspace provides centralized cost tracking and management for all Claude Code usage in your organization. You cannot create API keys for this workspace; it is exclusively for Claude Code authentication and usage.For organizations with custom rate limits, Claude Code traffic in this workspace counts toward your organization’s overall API rate limits. You can set a

[workspace rate limit](https://platform.claude.com/docs/en/api/rate-limits#setting-lower-limits-for-workspaces)on this workspace’s Limits page in the Claude Console to cap Claude Code’s share and protect other production workloads.

[[LLM gateway configuration - Claude Code Docs#LiteLLM configuration|LiteLLM]], which is an open-source tool that helps companies

[track spend by key](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). This project is unaffiliated with Anthropic and has not been audited for security.

### Rate limit recommendations

When setting up Claude Code for teams, consider these Token Per Minute (TPM) and Request Per Minute (RPM) per-user recommendations based on your organization size:

Team sizeTPM per userRPM per user1-5 users200k-300k5-75-20 users100k-150k2.5-3.520-50 users50k-75k1.25-1.7550-100 users25k-35k0.62-0.87100-500 users15k-20k0.37-0.47500+ users10k-15k0.25-0.35

If you anticipate scenarios with unusually high concurrent usage (such as live training sessions with large groups), you may need higher TPM allocations per user.

### Agent team token costs

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|Agent teams]]spawn multiple Claude Code instances, each with its own context window. Token usage scales with the number of active teammates and how long each one runs. To keep agent team costs manageable:

- Use Sonnet for teammates. It balances capability and cost for coordination tasks.
- Keep teams small. Each teammate runs its own context window, so token usage is roughly proportional to team size.
- Keep spawn prompts focused. Teammates load CLAUDE.md, MCP servers, and skills automatically, but everything in the spawn prompt adds to their context from the start.
- Clean up teams when work is done. Active teammates continue consuming tokens even if idle.
- Agent teams are disabled by default. Set

  ```
  CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
  ```

  in your[[Claude Code settings - Claude Code Docs|settings.json]]or environment to enable them. See[[Orchestrate teams of Claude Code sessions - Claude Code Docs#Enable agent teams|enable agent teams]].

## Reduce token usage

Token costs scale with context size: the more context Claude processes, the more tokens you use. Claude Code automatically optimizes costs through prompt caching (which reduces costs for repeated content like system prompts) and auto-compaction (which summarizes conversation history when approaching context limits). The following strategies help you keep context small and reduce per-message costs.

### Manage context proactively

Use

```
/usage
```

to check your current token usage, or

[[Customize your status line - Claude Code Docs#Context window usage|configure your status line]]to display it continuously.

- Clear between tasks: Use

  ```
  /clear
  ```

  to start fresh when switching to unrelated work. Stale context wastes tokens on every subsequent message. Use

  ```
  /rename
  ```

  before clearing so you can easily find the session later, then

  ```
  /resume
  ```

  to return to it.
- Add custom compaction instructions:

  ```
  /compact Focus on code samples and API usage
  ```

  tells Claude what to preserve during summarization.

### Choose the right model

Sonnet handles most coding tasks well and costs less than Opus. Reserve Opus for complex architectural decisions or multi-step reasoning. Use

```
/model
```

to switch models mid-session, or set a default in

```
/config
```

. For simple subagent tasks, specify

```
model: haiku
```

in your

[[Create custom subagents - Claude Code Docs#Choose a model|subagent configuration]].

### Reduce MCP server overhead

MCP tool definitions are

[[Connect Claude Code to tools via MCP - Claude Code Docs#Scale with MCP Tool Search|deferred by default]], so only tool names enter context until Claude uses a specific tool. Run

```
/context
```

to see what’s consuming space.

- Prefer CLI tools when available: Tools like

  ```
  gh
  ```

  ,

  ```
  aws
  ```

  ,

  ```
  gcloud
  ```

  , and

  ```
  sentry-cli
  ```

  are still more context-efficient than MCP servers because they don’t add any per-tool listing. Claude can run CLI commands directly.
- Disable unused servers: Run

  ```
  /mcp
  ```

  to see configured servers and disable any you’re not actively using.

### Install code intelligence plugins for typed languages

[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs#Code intelligence|Code intelligence plugins]]give Claude precise symbol navigation instead of text-based search, reducing unnecessary file reads when exploring unfamiliar code. A single “go to definition” call replaces what might otherwise be a grep followed by reading multiple candidate files. Installed language servers also report type errors automatically after edits, so Claude catches mistakes without running a compiler.

### Offload processing to hooks and skills

Custom

[[Hooks reference - Claude Code Docs|hooks]]can preprocess data before Claude sees it. Instead of Claude reading a 10,000-line log file to find errors, a hook can grep for

```
ERROR
```

and return only matching lines, reducing context from tens of thousands of tokens to hundreds.
A

[[Extend Claude with skills - Claude Code Docs|skill]]can give Claude domain knowledge so it doesn’t have to explore. For example, a “codebase-overview” skill could describe your project’s architecture, key directories, and naming conventions. When Claude invokes the skill, it gets this context immediately instead of spending tokens reading multiple files to understand the structure. For example, this PreToolUse hook filters test output to show only failures:

- settings.json
- filter-test-output.sh

Add this to your

[[Claude Code settings - Claude Code Docs#Settings files|settings.json]]to run the hook before every Bash command:

### Move instructions from CLAUDE.md to skills

Your

[[How Claude remembers your project - Claude Code Docs|CLAUDE.md]]file is loaded into context at session start. If it contains detailed instructions for specific workflows (like PR reviews or database migrations), those tokens are present even when you’re doing unrelated work.

[[Extend Claude with skills - Claude Code Docs|Skills]]load on-demand only when invoked, so moving specialized instructions into skills keeps your base context smaller. Aim to keep CLAUDE.md under 200 lines by including only essentials.

### Adjust extended thinking

Extended thinking is enabled by default because it significantly improves performance on complex planning and reasoning tasks. Thinking tokens are billed as output tokens, and the default budget can be tens of thousands of tokens per request depending on the model. For simpler tasks where deep reasoning isn’t needed, you can reduce costs by lowering the

[[Model configuration - Claude Code Docs#Adjust effort level|effort level]]with

```
/effort
```

or in

```
/model
```

, disabling thinking in

```
/config
```

, or lowering the budget with

```
MAX_THINKING_TOKENS=8000
```

.

### Delegate verbose operations to subagents

Running tests, fetching documentation, or processing log files can consume significant context. Delegate these to

[[Create custom subagents - Claude Code Docs#Isolate high-volume operations|subagents]]so the verbose output stays in the subagent’s context while only a summary returns to your main conversation.

### Manage agent team costs

Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode, because each teammate maintains its own context window and runs as a separate Claude instance. Keep team tasks small and self-contained to limit per-teammate token usage. See

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|agent teams]]for details.

### Write specific prompts

Vague requests like “improve this codebase” trigger broad scanning. Specific requests like “add input validation to the login function in auth.ts” let Claude work efficiently with minimal file reads.

### Work efficiently on complex tasks

For longer or more complex work, these habits help avoid wasted tokens from going down the wrong path:

- Use plan mode for complex tasks: Press Shift+Tab to enter [[Common workflows - Claude Code Docs#Use Plan Mode for safe code analysis|plan mode]]before implementation. Claude explores the codebase and proposes an approach for your approval, preventing expensive re-work when the initial direction is wrong.
- Course-correct early: If Claude starts heading the wrong direction, press Escape to stop immediately. Use

  ```
  /rewind
  ```

  or double-tap Escape to restore conversation and code to a previous checkpoint.
- Give verification targets: Include test cases, paste screenshots, or define expected output in your prompt. When Claude can verify its own work, it catches issues before you need to request fixes.
- Test incrementally: Write one file, test it, then continue. This catches issues early when they’re cheap to fix.

## Background token usage

Claude Code uses tokens for some background functionality even when idle:

- Conversation summarization: Background jobs that summarize previous conversations for the

  ```
  claude --resume
  ```

  feature
- Command processing: Some commands like

  ```
  /usage
  ```

  may generate requests to check status

## Understanding changes in Claude Code behavior

Claude Code regularly receives updates that may change how features work, including cost reporting. Run

```
claude --version
```

to check your current version. For specific billing questions, contact Anthropic support through your

[Console account](https://platform.claude.com/login).

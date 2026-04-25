---
title: Extend Claude Code - Claude Code Docs
source_url: https://code.claude.com/docs/en/features-overview
description: Understand when to use CLAUDE.md, Skills, subagents, hooks, MCP, and
  plugins.
---

[[How Claude Code works - Claude Code Docs#Tools|built-in tools]]for file operations, search, execution, and web access. The built-in tools cover most coding tasks. This guide covers the extension layer: features you add to customize what Claude knows, connect it to external services, and automate workflows.

For how the core agentic loop works, see

[[How Claude Code works - Claude Code Docs|How Claude Code works]].

[[How Claude remembers your project - Claude Code Docs|CLAUDE.md]]for project conventions, then add other extensions

[[Extend Claude Code - Claude Code Docs#Build your setup over time|as specific triggers come up]].

## Overview

Extensions plug into different parts of the agentic loop:

- [[How Claude remembers your project - Claude Code Docs|CLAUDE.md]]adds persistent context Claude sees every session
- [[Extend Claude with skills - Claude Code Docs|Skills]]add reusable knowledge and invocable workflows
- [[Connect Claude Code to tools via MCP - Claude Code Docs|MCP]]connects Claude to external services and tools
- [[Create custom subagents - Claude Code Docs|Subagents]]run their own loops in isolated context, returning summaries
- [[Orchestrate teams of Claude Code sessions - Claude Code Docs|Agent teams]]coordinate multiple independent sessions with shared tasks and peer-to-peer messaging
- [[Automate workflows with hooks - Claude Code Docs|Hooks]]fire on lifecycle events and can run a script, HTTP request, prompt, or subagent
- [[Create plugins - Claude Code Docs|Plugins]]and[[Create and distribute a plugin marketplace - Claude Code Docs|marketplaces]]package and distribute these features

[[Extend Claude with skills - Claude Code Docs|Skills]]are the most flexible extension. A skill is a markdown file containing knowledge, workflows, or instructions. You can invoke skills with a command like

```
/deploy
```

, or Claude can load them automatically when relevant. Skills can run in your current conversation or in an isolated context via subagents.

## Match features to your goal

Features range from always-on context that Claude sees every session, to on-demand capabilities you or Claude can invoke, to background automation that runs on specific events. The table below shows what’s available and when each one makes sense.

FeatureWhat it doesWhen to use itExampleCLAUDE.mdPersistent context loaded every conversationProject conventions, “always do X” rules”Use pnpm, not npm. Run tests before committing.”SkillInstructions, knowledge, and workflows Claude can useReusable content, reference docs, repeatable tasks

```
/deploy
```

runs your deployment checklist; API docs skill with endpoint patternsSubagentIsolated execution context that returns summarized resultsContext isolation, parallel tasks, specialized workersResearch task that reads many files but returns only key findings

[[Create plugins - Claude Code Docs|Plugins]]are the packaging layer. A plugin bundles skills, hooks, subagents, and MCP servers into a single installable unit. Plugin skills are namespaced (like

```
/my-plugin:review
```

) so multiple plugins can coexist. Use plugins when you want to reuse the same setup across multiple repositories or distribute to others via a

[[Create and distribute a plugin marketplace - Claude Code Docs|marketplace]].

### Build your setup over time

You don’t need to configure everything up front. Each feature has a recognizable trigger, and most teams add them in roughly this order:

TriggerAddClaude gets a convention or command wrong twiceAdd it to

[[Extend Claude with skills - Claude Code Docs|skill]][[Extend Claude with skills - Claude Code Docs|skill]][[Connect Claude Code to tools via MCP - Claude Code Docs|MCP server]][[Create custom subagents - Claude Code Docs|subagent]][[Automate workflows with hooks - Claude Code Docs|hook]][[Create plugins - Claude Code Docs|plugin]]

### Compare similar features

Some features can seem similar. Here’s how to tell them apart.

- Skill vs Subagent
- CLAUDE.md vs Skill
- CLAUDE.md vs Rules vs Skills
- Subagent vs Agent team
- MCP vs Skill
- Hook vs Skill

Skills and subagents solve different problems:

Skills can be reference or action. Reference skills provide knowledge Claude uses throughout your session (like your API style guide). Action skills tell Claude to do something specific (like

- Skills are reusable content you can load into any context
- Subagents are isolated workers that run separately from your main conversation

AspectSkillSubagentWhat it isReusable instructions, knowledge, or workflowsIsolated worker with its own contextKey benefitShare content across contextsContext isolation. Work happens separately, only summary returnsBest forReference material, invocable workflowsTasks that read many files, parallel work, specialized workers

```
/deploy
```

that runs your deployment workflow).Use a subagent when you need context isolation or when your context window is getting full. The subagent might read dozens of files or run extensive searches, but your main conversation only receives a summary. Since subagent work doesn’t consume your main context, this is also useful when you don’t need the intermediate work to remain visible. Custom subagents can have their own instructions and can preload skills.They can combine. A subagent can preload specific skills (

```
skills:
```

field). A skill can run in isolated context using

```
context: fork
```

. See [[Extend Claude with skills - Claude Code Docs|Skills]]for details.

### Understand how features layer

Features can be defined at multiple levels: user-wide, per-project, via plugins, or through managed policies. You can also nest CLAUDE.md files in subdirectories or place skills in specific packages of a monorepo. When the same feature exists at multiple levels, here’s how they layer:

- CLAUDE.md files are additive: all levels contribute content to Claude’s context simultaneously. Files from your working directory and above load at launch; subdirectories load as you work in them. When instructions conflict, Claude uses judgment to reconcile them, with more specific instructions typically taking precedence. See [[How Claude remembers your project - Claude Code Docs|how CLAUDE.md files load]].
- Skills and subagents override by name: when the same name exists at multiple levels, one definition wins based on priority (managed > user > project for skills; managed > CLI flag > project > user > plugin for subagents). Plugin skills are [[Create plugins - Claude Code Docs#Add Skills to your plugin|namespaced]]to avoid conflicts. See[[Extend Claude with skills - Claude Code Docs#Where skills live|skill discovery]]and[[Create custom subagents - Claude Code Docs#Choose the subagent scope|subagent scope]].
- MCP servers override by name: local > project > user. See [[Connect Claude Code to tools via MCP - Claude Code Docs#Scope hierarchy and precedence|MCP scope]].
- Hooks merge: all registered hooks fire for their matching events regardless of source. See [[Hooks reference - Claude Code Docs|hooks]].

### Combine features

Each extension solves a different problem: CLAUDE.md handles always-on context, skills handle on-demand knowledge and workflows, MCP handles external connections, subagents handle isolation, and hooks handle automation. Real setups combine them based on your workflow. For example, you might use CLAUDE.md for project conventions, a skill for your deployment workflow, MCP to connect to your database, and a hook to run linting after every edit. Each feature handles what it’s best at.

PatternHow it worksExampleSkill + MCPMCP provides the connection; a skill teaches Claude how to use it wellMCP connects to your database, a skill documents your schema and query patternsSkill + SubagentA skill spawns subagents for parallel work

```
/audit
```

skill kicks off security, performance, and style subagents that work in isolated contextCLAUDE.md + SkillsCLAUDE.md holds always-on rules; skills hold reference material loaded on demandCLAUDE.md says “follow our API conventions,” a skill contains the full API style guideHook + MCPA hook triggers external actions through MCPPost-edit hook sends a Slack notification when Claude modifies critical files

## Understand context costs

Every feature you add consumes some of Claude’s context. Too much can fill up your context window, but it can also add noise that makes Claude less effective; skills may not trigger correctly, or Claude may lose track of your conventions. Understanding these trade-offs helps you build an effective setup. For an interactive view of how these features combine in a running session, see

[[Explore the context window - Claude Code Docs|Explore the context window]].

### Context cost by feature

Each feature has a different loading strategy and context cost:

FeatureWhen it loadsWhat loadsContext costCLAUDE.mdSession startFull contentEvery requestSkillsSession start + when usedDescriptions at start, full content when usedLow (descriptions every request)\*MCP serversSession startTool names; full schemas on demandLow until a tool is usedSubagentsWhen spawnedFresh context with specified skillsIsolated from main sessionHooksOn triggerNothing (runs externally)Zero, unless hook returns additional context

```
disable-model-invocation: true
```

in a skill’s frontmatter to hide it from Claude entirely until you invoke it manually. This reduces context cost to zero for skills you only trigger yourself.

### Understand how features load

Each feature loads at different points in your session. The tabs below explain when each one loads and what goes into context.

- CLAUDE.md
- Skills
- MCP servers
- Subagents
- Hooks

When: Session startWhat loads: Full content of all CLAUDE.md files (managed, user, and project levels).Inheritance: Claude reads CLAUDE.md files from your working directory up to the root, and discovers nested ones in subdirectories as it accesses those files. See

[[How Claude remembers your project - Claude Code Docs|How CLAUDE.md files load]]for details.

## Learn more

Each feature has its own guide with setup instructions, examples, and configuration options.

## CLAUDE.md

Store project context, conventions, and instructions

## Skills

Give Claude domain expertise and reusable workflows

## Subagents

Offload work to isolated context

## Agent teams

Coordinate multiple sessions working in parallel

## MCP

Connect Claude to external services

## Hooks

Automate workflows with hooks

## Plugins

Bundle and share feature sets

## Marketplaces

Host and distribute plugin collections

---
title: Configure auto mode - Claude Code Docs
source_url: https://code.claude.com/docs/en/auto-mode-config
description: Tell the auto mode classifier which repos, buckets, and domains your
  organization trusts. Set environment context, override the default block and allow
  rules, a
---

[[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|Auto mode]]lets Claude Code run without permission prompts by routing each tool call through a classifier that blocks anything irreversible, destructive, or aimed outside your environment. Use the

```
autoMode
```

settings block to tell that classifier which repos, buckets, and domains your organization trusts, so it stops blocking routine internal operations.
Out of the box, the classifier trusts only the working directory and the current repo’s configured remotes. Actions like pushing to your company’s source-control org or writing to a team cloud bucket are blocked until you add them to

```
autoMode.environment
```

.
For how to enable auto mode and what it blocks by default, see

[[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|Permission modes]]. This page is the configuration reference. This page covers how to:

- [[Configure auto mode - Claude Code Docs#Where the classifier reads configuration|Choose where to set rules]]across CLAUDE.md, user settings, and managed settings
- [[Configure auto mode - Claude Code Docs#Define trusted infrastructure|Define trusted infrastructure]]with

  ```
  autoMode.environment
  ```
- [[Configure auto mode - Claude Code Docs#Override the block and allow rules|Override the block and allow rules]]when the defaults don’t fit your pipeline
- [[Configure auto mode - Claude Code Docs#Inspect the defaults and your effective config|Inspect your effective config]]with the

  ```
  claude auto-mode
  ```

  subcommands
- [[Configure auto mode - Claude Code Docs#Review denials|Review denials]]so you know what to add next

## Where the classifier reads configuration

The classifier reads the same

[[How Claude remembers your project - Claude Code Docs|CLAUDE.md]]content Claude itself loads, so an instruction like “never force push” in your project’s CLAUDE.md steers both Claude and the classifier at the same time. Start there for project conventions and behavioral rules. For rules that apply across projects, such as trusted infrastructure or organization-wide deny rules, use the

```
autoMode
```

settings block. The classifier reads

```
autoMode
```

from the following scopes:

ScopeFileUse forOne developer

```
~/.claude/settings.json
```

Personal trusted infrastructureOne project, one developer

```
.claude/settings.local.json
```

Per-project trusted buckets or services, gitignoredOrganization-wide

```
--settings
```

flag or Agent SDK

```
autoMode
```

from shared project settings in

```
.claude/settings.json
```

, so a checked-in repo cannot inject its own allow rules.
Entries from each scope are combined. A developer can extend

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

with personal entries but cannot remove entries that managed settings provide. Because allow rules act as exceptions to block rules inside the classifier, a developer-added

```
allow
```

entry can override an organization

```
soft_deny
```

entry: the combination is additive, not a hard policy boundary.

The classifier is a second gate that runs after the

[[Configure permissions - Claude Code Docs|permissions system]]. For actions that must never run regardless of user intent or classifier configuration, use

```
permissions.deny
```

in managed settings, which blocks the action before the classifier is consulted and cannot be overridden.

## Define trusted infrastructure

For most organizations,

```
autoMode.environment
```

is the only field you need to set. It tells the classifier which repos, buckets, and domains are trusted: the classifier uses it to decide what “external” means, so any destination not listed is a potential exfiltration target.
The default environment list trusts the working repo and its configured remotes. To add your own entries alongside that default, include the literal string

```
"$defaults"
```

in the array. The default entries are spliced in at that position, so your custom entries can go before or after them.

- Organization: your company name and what Claude Code is primarily used for, like software development, infrastructure automation, or data engineering
- Source control: every GitHub, GitLab, or Bitbucket org your developers push to
- Cloud providers and trusted buckets: bucket names or prefixes that Claude should be able to read from and write to
- Trusted internal domains: hostnames for APIs, dashboards, and services inside your network, like

  ```
  *.internal.example.com
  ```
- Key internal services: CI, artifact registries, internal package indexes, incident tooling
- Additional context: regulated-industry constraints, multi-tenant infrastructure, or compliance requirements that affect what the classifier should treat as risky

## Override the block and allow rules

Two additional fields let you replace the classifier’s built-in rule lists:

```
autoMode.soft_deny
```

controls what gets blocked, and

```
autoMode.allow
```

controls which exceptions apply. Each is an array of prose descriptions, read as natural-language rules. There is no

```
autoMode.deny
```

field; to hard-block an action regardless of intent, use

[[Configure permissions - Claude Code Docs|, which runs before the classifier. Inside the classifier, precedence works in three tiers:]]

```
permissions.deny
```

- ```
  soft_deny
  ```

  rules block first
- ```
  allow
  ```

  rules then override matching blocks as exceptions
- Explicit user intent overrides both: if the user’s message directly and specifically describes the exact action Claude is about to take, the classifier allows it even when a

  ```
  soft_deny
  ```

  rule matches

```
allow
```

when the classifier repeatedly flags a routine pattern the default exceptions don’t cover. To tighten, add to

```
soft_deny
```

for risks specific to your environment that the defaults miss. To keep the built-in rules while adding your own, include the literal string

```
"$defaults"
```

in the array. The default rules are spliced in at that position, so your custom rules can go before or after them, and you continue to inherit updates as the built-in list changes across releases.

Setting any of

```
environment
```

,

```
allow
```

, or

```
soft_deny
```

without

```
"$defaults"
```

replaces the entire default list for that section. If you set

```
soft_deny
```

with a single entry and omit

```
"$defaults"
```

, every built-in block rule is discarded: force push, data exfiltration,

```
curl | bash
```

, production deploys, and all other default block rules become allowed. Only omit

```
"$defaults"
```

when you intend to take full ownership of the list. In that case, run

```
claude auto-mode defaults
```

to print the built-in rules, copy them into your settings file, then review each rule against your own pipeline and risk tolerance.

```
environment
```

alone leaves the default

```
allow
```

and

```
soft_deny
```

lists intact.

## Inspect the defaults and your effective config

Three CLI subcommands help you inspect and validate your configuration. Print the built-in

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

rules as JSON:

```
allow
```

and

```
soft_deny
```

rules:

```
claude auto-mode config
```

after saving your settings to confirm the effective rules are what you expect, with

```
"$defaults"
```

expanded in place. If you’ve written custom rules,

```
claude auto-mode critique
```

reviews them and flags entries that are ambiguous, redundant, or likely to cause false positives. If you need to remove or rewrite a built-in rule rather than add alongside it, save the output of

```
claude auto-mode defaults
```

to a file, edit the lists, and paste the result into your settings file in place of

```
"$defaults"
```

.

## Review denials

When auto mode denies a tool call, the denial is recorded in

```
/permissions
```

under the Recently denied tab. Press

```
r
```

on a denied action to mark it for retry: when you exit the dialog, Claude Code sends a message telling the model it may retry that tool call and resumes the conversation.
Repeated denials for the same destination usually mean the classifier is missing context. Add that destination to

```
autoMode.environment
```

, then run

```
claude auto-mode config
```

to confirm it took effect.
To react to denials programmatically, use the

[[Hooks reference - Claude Code Docs#PermissionDenied|.]]

```
PermissionDenied
```

hook

## See also

- [[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|Permission modes]]: what auto mode is, what it blocks by default, and how to enable it
- [[Configure server-managed settings - Claude Code Docs|Managed settings]]: deploy

  ```
  autoMode
  ```

  configuration across your organization
- [[Configure permissions - Claude Code Docs|Permissions]]: allow, ask, and deny rules that apply before the classifier runs
- [[Claude Code settings - Claude Code Docs|Settings]]: the full settings reference, including the

  ```
  autoMode
  ```

  key

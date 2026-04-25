---
title: Claude Code with GitHub Enterprise Server - Claude Code Docs
source_url: https://code.claude.com/docs/en/github-enterprise-server
description: Connect Claude Code to your self-hosted GitHub Enterprise Server instance
  for web sessions, code review, and plugin marketplaces.
---

GitHub Enterprise Server support is available for Team and Enterprise plans.

[[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]and

[[Code Review - Claude Code Docs|Code Review]]. To run Claude in your own CI infrastructure, see

[[Claude Code GitHub Actions - Claude Code Docs|GitHub Actions]].

## What works with GitHub Enterprise Server

The table below shows which Claude Code features support GHES and any differences from github.com behavior.

FeatureGHES supportNotesClaude Code on the web✅ SupportedAdmin connects the GHES instance once; developers use

```
claude --remote
```

orCode Review✅ SupportedSame automated PR reviews as github.comTeleport sessions✅ SupportedMove sessions between web and terminal with

```
--teleport
```

Plugin marketplaces✅ SupportedUse full git URLs instead of

```
owner/repo
```

shorthandContribution metrics✅ SupportedDelivered via webhooks to the

```
/install-github-app
```

is github.com only

## Admin setup

An admin connects your GHES instance to Claude Code once. After that, developers in your organization can use GHES repositories without any additional configuration. You need admin access to your Claude organization and permission to create GitHub Apps on your GHES instance. The guided setup generates a GitHub App manifest and redirects you to your GHES instance to create the app in one click. If your environment blocks the redirect flow, an

[[Claude Code with GitHub Enterprise Server - Claude Code Docs#Manual setup|alternative manual setup]]is available.

Open Claude Code admin settings

Go to

[claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)and find the GitHub Enterprise Server section.

Start the guided setup

Click Connect. Enter a display name for the connection and your GHES hostname, for example

```
github.example.com
```

. If your GHES instance uses a self-signed or private certificate authority, paste the CA certificate in the optional field.

Create the GitHub App

Click Continue to GitHub Enterprise. Your browser redirects to your GHES instance with a pre-filled app manifest. Review the configuration and click Create GitHub App. GHES redirects you back to Claude with the app credentials stored automatically.

Install the app on your repositories

From the GitHub App page on your GHES instance, install the app on the repositories or organizations you want Claude to access. You can start with a subset and add more later.

Enable features

Return to

[claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)and enable[[Code Review - Claude Code Docs#Set up Code Review|Code Review]]and[[Track team usage with analytics - Claude Code Docs#Enable contribution metrics|contribution metrics]]for your GHES repositories using the same configuration as github.com.

### GitHub App permissions

The manifest configures the GitHub App with the permissions and webhook events Claude needs across web sessions, Code Review, and contribution metrics:

PermissionAccessUsed forContentsRead and writeCloning repositories and pushing branchesPull requestsRead and writeCreating PRs and posting review commentsIssuesRead and writeResponding to issue mentionsChecksRead and writePosting Code Review check runsActionsReadReading CI status for auto-fixRepository hooksRead and writeReceiving webhooks for contribution metricsMetadataReadRequired by GitHub for all apps

```
pull_request
```

,

```
issue_comment
```

,

```
pull_request_review_comment
```

,

```
pull_request_review
```

, and

```
check_run
```

events.

### Manual setup

If the guided redirect flow is blocked by your network configuration, click Add manually instead of Connect. Create a GitHub App on your GHES instance with the

[[Claude Code with GitHub Enterprise Server - Claude Code Docs#GitHub App permissions|permissions and events above]], then enter the app credentials in the form: hostname, OAuth client ID and secret, GitHub App ID, client ID, client secret, webhook secret, and private key.

### Network requirements

Your GHES instance must be reachable from Anthropic infrastructure so Claude can clone repositories and post review comments. If your GHES instance is behind a firewall, allowlist the

[Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses).

## Developer workflow

Once your admin has connected the GHES instance, no developer-side configuration is needed. Claude Code detects your GHES hostname automatically from the git remote in your working directory. Clone a repository from your GHES instance as you normally would:

```
/tasks
```

or at

[claude.ai/code](https://claude.ai/code). See

[[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]for the full remote session workflow including diff review, auto-fix, and routines.

### Teleport sessions to your terminal

Pull a web session into your local terminal with

```
claude --teleport
```

. Teleport verifies you’re in a checkout of the same GHES repository before fetching the branch and loading the session history. See

[[Use Claude Code on the web - Claude Code Docs#Teleport requirements|teleport requirements]]for details.

## Plugin marketplaces on GHES

Host plugin marketplaces on your GHES instance to distribute internal tooling across your organization. The marketplace structure is identical to github.com-hosted marketplaces; the only difference is how you reference them.

### Add a GHES marketplace

The

```
owner/repo
```

shorthand always resolves to github.com. For GHES-hosted marketplaces, use the full git URL:

[[Create and distribute a plugin marketplace - Claude Code Docs|Create and distribute a plugin marketplace]]for the full guide to building marketplaces.

### Allowlist GHES marketplaces in managed settings

If your organization uses

[[Claude Code settings - Claude Code Docs|managed settings]]to restrict which marketplaces developers can add, use the

```
hostPattern
```

source type to allow all marketplaces from your GHES instance without enumerating each repository:

[[Claude Code settings - Claude Code Docs#strictKnownMarketplaces|strictKnownMarketplaces]]and

[[Claude Code settings - Claude Code Docs#extraKnownMarketplaces|extraKnownMarketplaces]]settings reference for the complete schema.

## Limitations

A few features behave differently on GHES than on github.com. The

[[Claude Code with GitHub Enterprise Server - Claude Code Docs#What works with GitHub Enterprise Server|feature table]]summarizes support; this section covers the workarounds.

- ```
  /install-github-app
  ```

  command: follow the[[Claude Code with GitHub Enterprise Server - Claude Code Docs#Admin setup|admin setup]]flow on claude.ai instead. If you also want GitHub Actions workflows on GHES, adapt the[example workflow](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml)manually.
- GitHub MCP server: use the

  ```
  gh
  ```

  CLI configured for your GHES host instead. Run

  ```
  gh auth login --hostname github.example.com
  ```

  to authenticate, then Claude can use

  ```
  gh
  ```

  commands in sessions.

## Troubleshooting

### Web session fails to clone repository

If

```
claude --remote
```

fails with a clone error, verify that your admin has completed setup for your GHES instance and that the GitHub App is installed on the repository you’re working in. Check with your admin that the instance hostname registered in Claude settings matches the hostname in your git remote.

### Marketplace add fails with a policy error

If

```
/plugin marketplace add
```

is blocked for your GHES URL, your organization has restricted marketplace sources. Ask your admin to add a

```
hostPattern
```

entry for your GHES hostname in

[[Claude Code with GitHub Enterprise Server - Claude Code Docs#Allowlist GHES marketplaces in managed settings|managed settings]].

### GHES instance not reachable

If reviews or web sessions time out, your GHES instance may not be reachable from Anthropic infrastructure. Confirm your firewall allows inbound connections from the

[Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses).

## Related resources

These pages cover the features referenced throughout this guide in more depth:

- [[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]: run Claude Code sessions on cloud infrastructure
- [[Code Review - Claude Code Docs|Code Review]]: automated PR reviews
- [[Create and distribute a plugin marketplace - Claude Code Docs|Plugin marketplaces]]: build and distribute plugin catalogs
- [[Track team usage with analytics - Claude Code Docs|Analytics]]: track usage and contribution metrics
- [[Claude Code settings - Claude Code Docs|Managed settings]]: organization-wide policy configuration
- [[Enterprise network configuration - Claude Code Docs|Network configuration]]: firewall and IP allowlist requirements

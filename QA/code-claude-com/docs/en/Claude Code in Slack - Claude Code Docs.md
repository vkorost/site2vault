---
title: Claude Code in Slack - Claude Code Docs
source_url: https://code.claude.com/docs/en/slack
description: Delegate coding tasks directly from your Slack workspace
---

```
@Claude
```

with a coding task, Claude automatically detects the intent and creates a Claude Code session on the web, allowing you to delegate development work without leaving your team conversations.
This integration is built on the existing Claude for Slack app but adds intelligent routing to Claude Code on the web for coding-related requests.

## Use cases

- Bug investigation and fixes: Ask Claude to investigate and fix bugs as soon as they’re reported in Slack channels.
- Quick code reviews and modifications: Have Claude implement small features or refactor code based on team feedback.
- Collaborative debugging: When team discussions provide crucial context (e.g., error reproductions or user reports), Claude can use that information to inform its debugging approach.
- Parallel task execution: Kick off coding tasks in Slack while you continue other work, receiving notifications when complete.

## Prerequisites

Before using Claude Code in Slack, ensure you have the following:

RequirementDetailsClaude PlanPro, Max, Team, or Enterprise with Claude Code access (premium seats or Chat + Claude Code seats)Claude Code on the webAccess to

## Setting up Claude Code in Slack

Install the Claude App in Slack

A workspace administrator must install the Claude app from the Slack App Marketplace. Visit the

[Slack App Marketplace](https://slack.com/marketplace/A08SF47R6P4)and click “Add to Slack” to begin the installation process.

Connect your Claude account

After the app is installed, authenticate your individual Claude account:

- Open the Claude app in Slack by clicking on “Claude” in your Apps section
- Navigate to the App Home tab
- Click “Connect” to link your Slack account with your Claude account
- Complete the authentication flow in your browser

Configure Claude Code on the web

Ensure your Claude Code on the web is properly configured:

- Visit [claude.ai/code](https://claude.ai/code)and sign in with the same account you connected to Slack
- Connect your GitHub account if not already connected
- Authenticate at least one repository that you want Claude to work with

Choose your routing mode

After connecting your accounts, configure how Claude handles your messages in Slack. Navigate to the Claude App Home in Slack to find the Routing Mode setting.

ModeBehaviorCode onlyClaude routes all @mentions to Claude Code sessions. Best for teams using Claude in Slack exclusively for development tasks.Code + ChatClaude analyzes each message and intelligently routes between Claude Code (for coding tasks) and Claude Chat (for writing, analysis, and general questions). Best for teams who want a single @Claude entry point for all types of work.

In Code + Chat mode, if Claude routes a message to Chat but you wanted a coding session, you can click “Retry as Code” to create a Claude Code session instead. Similarly, if it’s routed to Code but you wanted a Chat session, you can choose that option in that thread.

## How it works

### Automatic detection

When you mention @Claude in a Slack channel or thread, Claude automatically analyzes your message to determine if it’s a coding task. If Claude detects coding intent, it will route your request to Claude Code on the web instead of responding as a regular chat assistant. You can also explicitly tell Claude to handle a request as a coding task, even if it doesn’t automatically detect it.

Claude Code in Slack only works in channels (public or private). It does not work in direct messages (DMs).

### Context gathering

From threads: When you @mention Claude in a thread, it gathers context from all messages in that thread to understand the full conversation. From channels: When mentioned directly in a channel, Claude looks at recent channel messages for relevant context. This context helps Claude understand the problem, select the appropriate repository, and inform its approach to the task.

### Session flow

- Initiation: You @mention Claude with a coding request
- Detection: Claude analyzes your message and detects coding intent
- Session creation: A new Claude Code session is created on claude.ai/code
- Progress updates: Claude posts status updates to your Slack thread as work progresses
- Completion: When finished, Claude @mentions you with a summary and action buttons
- Review: Click “View Session” to see the full transcript, or “Create PR” to open a pull request

## User interface elements

### App Home

The App Home tab shows your connection status and allows you to connect or disconnect your Claude account from Slack.

### Message actions

- View Session: Opens the full Claude Code session in your browser where you can see all work performed, continue the session, or make additional requests.
- Create PR: Creates a pull request directly from the session’s changes.
- Retry as Code: If Claude initially responds as a chat assistant but you wanted a coding session, click this button to retry the request as a Claude Code task.
- Change Repo: Allows you to select a different repository if Claude chose incorrectly.

### Repository selection

Claude automatically selects a repository based on context from your Slack conversation. If multiple repositories could apply, Claude may display a dropdown allowing you to choose the correct one.

## Access and permissions

### User-level access

Access TypeRequirementClaude Code SessionsEach user runs sessions under their own Claude accountUsage & Rate LimitsSessions count against the individual user’s plan limitsRepository AccessUsers can only access repositories they’ve personally connectedSession HistorySessions appear in your Claude Code history on claude.ai/code

### Workspace-level access

Slack workspace administrators control whether the Claude app is available in their workspace:

ControlDescriptionApp installationWorkspace admins decide whether to install the Claude app from the Slack App MarketplaceEnterprise Grid distributionFor Enterprise Grid organizations, organization admins can control which workspaces have access to the Claude appApp removalRemoving the app from a workspace immediately revokes access for all users in that workspace

### Channel-based access control

Claude is not automatically added to any channels after installation. Users must explicitly invite Claude to channels where they want to use it:

- Invite required: Type

  ```
  /invite @Claude
  ```

  in any channel to add Claude to that channel
- Channel membership controls access: Claude can only respond to @mentions in channels where it has been added
- Access gating through channels: Admins can control who uses Claude Code by managing which channels Claude is invited to and who has access to those channels
- Private channel support: Claude works in both public and private channels, giving teams flexibility in controlling visibility

## What’s accessible where

In Slack: You’ll see status updates, completion summaries, and action buttons. The full transcript is preserved and always accessible. On the web: The complete Claude Code session with full conversation history, all code changes, file operations, and the ability to continue the session or create pull requests. For Enterprise and Team accounts, sessions created from Claude in Slack are automatically visible to the organization. See

[[Use Claude Code on the web - Claude Code Docs#Share sessions|Claude Code on the Web sharing]]for more details.

## Best practices

### Writing effective requests

- Be specific: Include file names, function names, or error messages when relevant.
- Provide context: Mention the repository or project if it’s not clear from the conversation.
- Define success: Explain what “done” looks like—should Claude write tests? Update documentation? Create a PR?
- Use threads: Reply in threads when discussing bugs or features so Claude can gather the full context.

### When to use Slack vs. web

Use Slack when: Context already exists in a Slack discussion, you want to kick off a task asynchronously, or you’re collaborating with teammates who need visibility. Use the web directly when: You need to upload files, want real-time interaction during development, or are working on longer, more complex tasks.

## Troubleshooting

### Sessions not starting

- Verify your Claude account is connected in the Claude App Home
- Check that you have Claude Code on the web access enabled
- Ensure you have at least one GitHub repository connected to Claude Code

### Repository not showing

- Connect the repository in Claude Code on the web at [claude.ai/code](https://claude.ai/code)
- Verify your GitHub permissions for that repository
- Try disconnecting and reconnecting your GitHub account

### Wrong repository selected

- Click the “Change Repo” button to select a different repository
- Include the repository name in your request for more accurate selection

### Authentication errors

- Disconnect and reconnect your Claude account in the App Home
- Ensure you’re signed into the correct Claude account in your browser
- Check that your Claude plan includes Claude Code access

### Session expiration

- Sessions remain accessible in your Claude Code history on the web
- You can continue or reference past sessions from [claude.ai/code](https://claude.ai/code)

## Current limitations

- GitHub only: Currently supports repositories on GitHub.
- One PR at a time: Each session can create one pull request.
- Rate limits apply: Sessions use your individual Claude plan’s rate limits.
- Web access required: Users must have Claude Code on the web access; those without it will only get standard Claude chat responses.

## Related resources

## Claude Code on the web

Learn more about Claude Code on the web

## Claude for Slack

General Claude for Slack documentation

## Slack App Marketplace

Install the Claude app from the Slack Marketplace

## Claude Help Center

Get additional support

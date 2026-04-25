---
title: Plan in the cloud with ultraplan - Claude Code Docs
source_url: https://code.claude.com/docs/en/ultraplan
description: Start a plan from your CLI, draft it on Claude Code on the web, then
  execute it remotely or back in your terminal
---

Ultraplan is in research preview and requires Claude Code v2.1.91 or later. Behavior and capabilities may change based on feedback.

[[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]session running in

[[Choose a permission mode - Claude Code Docs#Analyze before you edit with plan mode|plan mode]]. Claude drafts the plan in the cloud while you keep working in your terminal. When the plan is ready, you open it in your browser to comment on specific sections, ask for revisions, and choose where to execute it. This is useful when you want a richer review surface than the terminal offers:

- Targeted feedback: comment on individual sections of the plan instead of replying to the whole thing
- Hands-off drafting: the plan is generated remotely, so your terminal stays free for other work
- Flexible execution: approve the plan to run on the web and open a pull request, or send it back to your terminal

[[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]account and a GitHub repository. Because it runs on Anthropic’s cloud infrastructure, it is not available when using Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry. The cloud session runs in your account’s default

[[Use Claude Code on the web - Claude Code Docs#The cloud environment|cloud environment]]. If you don’t have a cloud environment yet, ultraplan creates one automatically when it first launches.

## Launch ultraplan from the CLI

From your local CLI session, you can launch ultraplan in three ways:

- Command: run

  ```
  /ultraplan
  ```

  followed by your prompt
- Keyword: include the word

  ```
  ultraplan
  ```

  anywhere in a normal prompt
- From a local plan: when Claude finishes a local plan and shows the approval dialog, choose No, refine with Ultraplan on Claude Code on the web to send the draft to the cloud for further iteration

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]is active, it disconnects when ultraplan starts because both features occupy the claude.ai/code interface and only one can be connected at a time. After the cloud session launches, your CLI’s prompt input shows a status indicator while the remote session works:

StatusMeaning

```
◇ ultraplan
```

Claude is researching your codebase and drafting the plan

```
◇ ultraplan needs your input
```

Claude has a clarifying question; open the session link to respond

```
◆ ultraplan ready
```

The plan is ready to review in your browser

```
/tasks
```

and select the ultraplan entry to open a detail view with the session link, agent activity, and a Stop ultraplan action. Stopping archives the cloud session and clears the indicator; nothing is saved to your terminal.

## Review and revise the plan in your browser

When the status changes to

```
◆ ultraplan ready
```

, open the session link to view the plan on claude.ai. The plan appears in a dedicated review view:

- Inline comments: highlight any passage and leave a comment for Claude to address
- Emoji reactions: react to a section to signal approval or concern without writing a full comment
- Outline sidebar: jump between sections of the plan

## Choose where to execute

When the plan looks right, you choose from the browser whether Claude implements it in the same cloud session or sends it back to your waiting terminal.

### Execute on the web

Select Approve Claude’s plan and start coding in your browser to have Claude implement it in the same Claude Code on the web session. Your terminal shows a confirmation, the status indicator clears, and the work continues in the cloud. When the implementation finishes,

[[Use Claude Code on the web - Claude Code Docs#Review changes|review the diff]]and create a pull request from the web interface.

### Send the plan back to your terminal

Select Approve plan and teleport back to terminal in your browser to implement the plan locally with full access to your environment. This option appears when the session was launched from your CLI and the terminal is still polling. The web session is archived so it doesn’t continue working in parallel. Your terminal shows the plan in a dialog titled Ultraplan approved with three options:

- Implement here: inject the plan into your current conversation and continue from where you left off
- Start new session: clear the current conversation and begin fresh with only the plan as context
- Cancel: save the plan to a file without executing it; Claude prints the file path so you can return to it later

```
claude --resume
```

command at the top so you can return to your previous conversation later.

## Related resources

- [[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]: the cloud infrastructure ultraplan runs on
- [[Choose a permission mode - Claude Code Docs#Analyze before you edit with plan mode|Plan mode]]: how planning works in a local session
- [[Find bugs with ultrareview - Claude Code Docs|Find bugs with ultrareview]]: the code review counterpart to ultraplan for catching issues before merge
- [[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]: use the claude.ai/code interface with a session running on your own machine

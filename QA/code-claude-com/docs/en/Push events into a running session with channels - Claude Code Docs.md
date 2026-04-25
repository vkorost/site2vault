---
title: Push events into a running session with channels - Claude Code Docs
source_url: https://code.claude.com/docs/en/channels
description: Use channels to push messages, alerts, and webhooks into your Claude
  Code session from an MCP server. Forward CI results, chat messages, and monitoring
  events s
---

Channels are in

[[Push events into a running session with channels - Claude Code Docs#Research preview|research preview]]and require Claude Code v2.1.80 or later. They require claude.ai login. Console and API key authentication is not supported. Team and Enterprise organizations must[[Push events into a running session with channels - Claude Code Docs#Enterprise controls|explicitly enable them]].

[[Push events into a running session with channels - Claude Code Docs#How channels compare|how channels compare]]. You install a channel as a plugin and configure it with your own credentials. Telegram, Discord, and iMessage are included in the research preview. When Claude replies through a channel, you see the inbound message in your terminal but not the reply text. The terminal shows the tool call and a confirmation (like “sent”), and the actual reply appears on the other platform. This page covers:

- [[Push events into a running session with channels - Claude Code Docs#Supported channels|Supported channels]]: Telegram, Discord, and iMessage setup
- [[Push events into a running session with channels - Claude Code Docs#Quickstart|Install and run a channel]]with fakechat, a localhost demo
- [[Push events into a running session with channels - Claude Code Docs#Security|Who can push messages]]: sender allowlists and how you pair
- [[Push events into a running session with channels - Claude Code Docs#Enterprise controls|Enable channels for your organization]]on Team and Enterprise
- [[Push events into a running session with channels - Claude Code Docs#How channels compare|How channels compare]]to web sessions, Slack, MCP, and Remote Control

[[Channels reference - Claude Code Docs|Channels reference]].

## Supported channels

Each supported channel is a plugin that requires

[Bun](https://bun.sh). For a hands-on demo of the plugin flow before connecting a real platform, try the

[[Push events into a running session with channels - Claude Code Docs#Quickstart|fakechat quickstart]].

- Telegram
- Discord
- iMessage

View the full

[Telegram plugin source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/telegram).

Create a Telegram bot

Open

[BotFather](https://t.me/BotFather)in Telegram and send

```
/newbot
```

. Give it a display name and a unique username ending in

```
bot
```

. Copy the token BotFather returns.

Install the plugin

In Claude Code, run:If Claude Code reports that the plugin is not found in any marketplace, your marketplace is either missing or outdated. Run

```
/plugin marketplace update claude-plugins-official
```

to refresh it, or

```
/plugin marketplace add anthropics/claude-plugins-official
```

if you haven’t added it before. Then retry the install.After installing, run

```
/reload-plugins
```

to activate the plugin’s configure command.

Configure your token

Run the configure command with the token from BotFather:This saves it to

```
~/.claude/channels/telegram/.env
```

. You can also set

```
TELEGRAM_BOT_TOKEN
```

in your shell environment before launching Claude Code.

Restart with channels enabled

Exit Claude Code and restart with the channel flag. This starts the Telegram plugin, which begins polling for messages from your bot:

Pair your account

Open Telegram and send any message to your bot. The bot replies with a pairing code.Back in Claude Code, run:Then lock down access so only your account can send messages:

If your bot doesn’t respond, make sure Claude Code is running with

```
--channels
```

from the previous step. The bot can only reply while the channel is active.

[[Channels reference - Claude Code Docs|build your own channel]]for systems that don’t have a plugin yet.

## Quickstart

Fakechat is an officially supported demo channel that runs a chat UI on localhost, with nothing to authenticate and no external service to configure. Once you install and enable fakechat, you can type in the browser and the message arrives in your Claude Code session. Claude replies, and the reply shows up back in the browser. After you’ve tested the fakechat interface, try out

[Telegram](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/telegram),

[Discord](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord), or

[iMessage](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/imessage). To try the fakechat demo, you’ll need:

- Claude Code [[Quickstart - Claude Code Docs#Step 1: Install Claude Code|installed and authenticated]]with a claude.ai account
- [Bun](https://bun.sh)installed. The pre-built channel plugins are Bun scripts. Check with

  ```
  bun --version
  ```

  ; if that fails,[install Bun](https://bun.sh/docs/installation).
- Team/Enterprise users: your organization admin must [[Push events into a running session with channels - Claude Code Docs#Enterprise controls|enable channels]]in managed settings

Install the fakechat channel plugin

Start a Claude Code session and run the install command:If Claude Code reports that the plugin is not found in any marketplace, your marketplace is either missing or outdated. Run

```
/plugin marketplace update claude-plugins-official
```

to refresh it, or

```
/plugin marketplace add anthropics/claude-plugins-official
```

if you haven’t added it before. Then retry the install.

Restart with the channel enabled

Exit Claude Code, then restart with The fakechat server starts automatically.

```
--channels
```

and pass the fakechat plugin you installed:

Push a message in

Open the fakechat UI at The message arrives in your Claude Code session as a

[http://localhost:8787](http://localhost:8787)and type a message:

```
<channel source="fakechat">
```

event. Claude reads it, does the work, and calls fakechat’s

```
reply
```

tool. The answer shows up in the chat UI.

[[Channels reference - Claude Code Docs#Relay permission prompts|permission relay capability]]can forward these prompts to you so you can approve or deny remotely. For unattended use,

[[Choose a permission mode - Claude Code Docs#Skip all checks with bypassPermissions mode|bypasses prompts entirely, but only use it in environments you trust.]]

```
--dangerously-skip-permissions
```

## Security

Every approved channel plugin maintains a sender allowlist: only IDs you’ve added can push messages, and everyone else is silently dropped. Telegram and Discord bootstrap the list by pairing:

- Find your bot in Telegram or Discord and send it any message
- The bot replies with a pairing code
- In your Claude Code session, approve the code when prompted
- Your sender ID is added to the allowlist

```
/imessage:access allow
```

.
On top of that, you control which servers are enabled each session with

```
--channels
```

, and on Team and Enterprise plans your organization controls availability with

[[Push events into a running session with channels - Claude Code Docs#Enterprise controls|. Being in]]

```
channelsEnabled
```

```
.mcp.json
```

isn’t enough to push messages: a server also has to be named in

```
--channels
```

.
The allowlist also gates

[[Channels reference - Claude Code Docs#Relay permission prompts|permission relay]]if the channel declares it. Anyone who can reply through the channel can approve or deny tool use in your session, so only allowlist senders you trust with that authority.

## Enterprise controls

On Team and Enterprise plans, channels are off by default. Admins control availability through two

[[Claude Code settings - Claude Code Docs|managed settings]]that users cannot override:

SettingPurposeWhen not configured

```
channelsEnabled
```

Master switch. Must be

```
true
```

for any channel to deliver messages. Set via theChannels blocked

```
allowedChannelPlugins
```

Which plugins can register once channels are enabled. Replaces the Anthropic-maintained list when set. Only applies when

```
channelsEnabled
```

is

```
true
```

.Anthropic default list applies

```
--channels
```

.

### Enable channels for your organization

Admins can enable channels from

[claude.ai → Admin settings → Claude Code → Channels](https://claude.ai/admin-settings/claude-code), or by setting

```
channelsEnabled
```

to

```
true
```

in managed settings.
Once enabled, users in your organization can use

```
--channels
```

to opt channel servers into individual sessions. If the setting is disabled or unset, the MCP server still connects and its tools work, but channel messages won’t arrive. A startup warning tells the user to have an admin enable the setting.

### Restrict which channel plugins can run

By default, any plugin on the Anthropic-maintained allowlist can register as a channel. Admins on Team and Enterprise plans can replace that allowlist with their own by setting

```
allowedChannelPlugins
```

in managed settings. Use this to restrict which official plugins are allowed, approve channels from your own internal marketplace, or both. Each entry names a plugin and the marketplace it comes from:

```
allowedChannelPlugins
```

is set, it replaces the Anthropic allowlist entirely: only the listed plugins can register. Leave it unset to fall back to the default Anthropic allowlist. An empty array blocks all channel plugins from the allowlist, but

```
--dangerously-load-development-channels
```

can still bypass it for local testing. To block channels entirely including the development flag, leave

```
channelsEnabled
```

unset instead.
This setting requires

```
channelsEnabled: true
```

. If a user passes a plugin to

```
--channels
```

that isn’t on your list, Claude Code starts normally but the channel doesn’t register, and the startup notice explains that the plugin isn’t on the organization’s approved list.

## Research preview

Channels are a research preview feature. Availability is rolling out gradually, and the

```
--channels
```

flag syntax and protocol contract may change based on feedback.
During the preview,

```
--channels
```

only accepts plugins from an Anthropic-maintained allowlist, or from your organization’s allowlist if an admin has set

[[Push events into a running session with channels - Claude Code Docs#Restrict which channel plugins can run|. The channel plugins in]]

```
allowedChannelPlugins
```

[claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins)are the default approved set. If you pass something that isn’t on the effective allowlist, Claude Code starts normally but the channel doesn’t register, and the startup notice tells you why. To test a channel you’re building, use

```
--dangerously-load-development-channels
```

. See

[[Channels reference - Claude Code Docs#Test during the research preview|Test during the research preview]]for information about testing custom channels that you build. Report issues or feedback on the

[Claude Code GitHub repository](https://github.com/anthropics/claude-code/issues).

## How channels compare

Several Claude Code features connect to systems outside the terminal, each suited to a different kind of work:

FeatureWhat it doesGood for

[[Claude Code in Slack - Claude Code Docs|Claude in Slack]]

```
@Claude
```

mention in a channel or thread[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP server]][[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]

- Chat bridge: ask Claude something from your phone via Telegram, Discord, or iMessage, and the answer comes back in the same chat while the work runs on your machine against your real files.
- [[Channels reference - Claude Code Docs#Example: build a webhook receiver|Webhook receiver]]: a webhook from CI, your error tracker, a deploy pipeline, or other external service arrives where Claude already has your files open and remembers what you were debugging.

## Next steps

Once you have a channel running, explore these related features:

- [[Channels reference - Claude Code Docs|Build your own channel]]for systems that don’t have plugins yet
- [[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]to drive a local session from your phone instead of forwarding events into it
- [[Run prompts on a schedule - Claude Code Docs|Scheduled tasks]]to poll on a timer instead of reacting to pushed events

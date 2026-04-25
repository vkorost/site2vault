---
title: Recommend your plugin from your CLI - Claude Code Docs
source_url: https://code.claude.com/docs/en/plugin-hints
description: Emit a one-line marker from your CLI so Claude Code prompts users to
  install your official plugin.
---

[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs|Discover and install plugins]].

## How it works

Claude Code sets the

[[Environment variables - Claude Code Docs|environment variable to]]

```
CLAUDECODE
```

```
1
```

for every command it runs through the Bash and PowerShell tools. When your CLI sees that variable, it writes a self-closing

```
<claude-code-hint />
```

tag to stderr.
When Claude Code receives the command output, it:

- Scans for hint lines and removes them before the output reaches the model
- Checks that the hint targets a plugin in an official Anthropic marketplace
- Checks that the plugin is not already installed and has not been prompted before
- Shows the user an install prompt that names the command that emitted the hint

## Emit the hint

Gate emission on the

```
CLAUDECODE
```

environment variable so the marker never appears in a human user’s terminal. Then write the tag to stderr on its own line.
The following examples emit a hint for a plugin named

```
example-cli
```

in the official marketplace:

```
example-cli
```

with your plugin’s name in the official marketplace.

## Choose where to emit

You control which code paths emit the hint. Claude Code deduplicates by plugin, so emitting on every invocation has no downside. Touchpoints that work well include:

PlacementWhy it works

```
--help
```

outputClaude often runs help when exploring an unfamiliar CLIUnknown-subcommand errorsReaches the moment Claude is confused about your interfaceLogin or auth successThe user is already in a setup mindsetFirst-run welcome messageA natural onboarding moment

## What the user sees

When the hint passes all checks, Claude Code shows a prompt like the following:

- Once per plugin: after the prompt is shown, Claude Code records the plugin and never prompts for it again, regardless of the user’s answer.
- Once per session: across all CLIs on the machine, at most one hint prompt appears per Claude Code session.

## Hint format

The hint is a self-closing tag with three required attributes.

AttributeRequiredDescription

```
v
```

YesProtocol version.

```
1
```

is the only supported value

```
type
```

YesHint kind.

```
plugin
```

is the only supported value

```
value
```

YesPlugin identifier in

```
name@marketplace
```

form

## Requirements

Claude Code enforces two conditions before acting on a hint. Hints that fail either check are dropped:

- Own line: the tag must occupy its own line. A tag embedded mid-line, for example inside a log statement, is ignored. Leading and trailing whitespace on the line is allowed.
- Official marketplace: the

  ```
  value
  ```

  must reference a plugin in an Anthropic-controlled marketplace such as

  ```
  claude-plugins-official
  ```

  . Hints that point to other marketplaces are silently dropped.

- Write to stderr: stderr keeps the tag out of shell pipelines such as

  ```
  example-cli deploy | jq
  ```

  . Claude Code scans both streams, so stdout also works.
- Gate on

  ```
  CLAUDECODE
  ```

  : only emit when the

  ```
  CLAUDECODE
  ```

  environment variable is set. This prevents the marker from appearing to users running your CLI directly.

## Get your plugin into the official marketplace

The hint protocol only takes effect for plugins that are listed in the official Anthropic marketplace. To submit a plugin, use one of the in-app submission forms:

- Claude.ai: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
- Console: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

## See also

- [[Create plugins - Claude Code Docs|Create plugins]]: build the plugin your CLI recommends
- [[Create and distribute a plugin marketplace - Claude Code Docs|Create and distribute a plugin marketplace]]: host plugins outside the official marketplace
- [[Environment variables - Claude Code Docs|Environment variables]]: full reference for

  ```
  CLAUDECODE
  ```

  and related variables

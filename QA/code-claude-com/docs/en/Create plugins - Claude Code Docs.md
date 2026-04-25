---
title: Create plugins - Claude Code Docs
source_url: https://code.claude.com/docs/en/plugins
description: Create custom plugins to extend Claude Code with skills, agents, hooks,
  and MCP servers.
---

[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs|Discover and install plugins]]. For complete technical specifications, see

[[Plugins reference - Claude Code Docs|Plugins reference]].

## When to use plugins vs standalone configuration

Claude Code supports two ways to add custom skills, agents, and hooks:

ApproachSkill namesBest forStandalone (

```
.claude/
```

directory)

```
/hello
```

Personal workflows, project-specific customizations, quick experimentsPlugins (directories with

```
.claude-plugin/plugin.json
```

)

```
/plugin-name:hello
```

Sharing with teammates, distributing to community, versioned releases, reusable across projects

- You’re customizing Claude Code for a single project
- The configuration is personal and doesn’t need to be shared
- You’re experimenting with skills or hooks before packaging them
- You want short skill names like

  ```
  /hello
  ```

  or

  ```
  /deploy
  ```

- You want to share functionality with your team or community
- You need the same skills/agents across multiple projects
- You want version control and easy updates for your extensions
- You’re distributing through a marketplace
- You’re okay with namespaced skills like

  ```
  /my-plugin:hello
  ```

  (namespacing prevents conflicts between plugins)

## Quickstart

This quickstart walks you through creating a plugin with a custom skill. You’ll create a manifest (the configuration file that defines your plugin), add a skill, and test it locally using the

```
--plugin-dir
```

flag.

### Prerequisites

- Claude Code [[Quickstart - Claude Code Docs#Step 1: Install Claude Code|installed and authenticated]]

If you don’t see the

```
/plugin
```

command, update Claude Code to the latest version. See [[Troubleshooting - Claude Code Docs|Troubleshooting]]for upgrade instructions.

### Create your first plugin

Create the plugin directory

Every plugin lives in its own directory containing a manifest and your skills, agents, or hooks. Create one now:

Create the plugin manifest

The manifest file at Then create

|  |  |
| --- | --- |
|  | Optional. Helpful for attribution. |

For additional fields like

```
.claude-plugin/plugin.json
```

defines your plugin’s identity: its name, description, and version. Claude Code uses this metadata to display your plugin in the plugin manager.Create the

```
.claude-plugin
```

directory inside your plugin folder:

```
my-first-plugin/.claude-plugin/plugin.json
```

with this content:

my-first-plugin/.claude-plugin/plugin.json

FieldPurpose

```
name
```

Unique identifier and skill namespace. Skills are prefixed with this (e.g.,

```
/my-first-plugin:hello
```

).

```
description
```

Shown in the plugin manager when browsing or installing plugins.

```
version
```

Optional. If set, users only receive updates when you bump this field. If omitted and your plugin is distributed via git, the commit SHA is used and every commit counts as a new version. See

```
author
```

```
homepage
```

,

```
repository
```

, and

```
license
```

, see the [[Plugins reference - Claude Code Docs#Plugin manifest schema|full manifest schema]].

Add a skill

Skills live in the Then create

```
skills/
```

directory. Each skill is a folder containing a

```
SKILL.md
```

file. The folder name becomes the skill name, prefixed with the plugin’s namespace (

```
hello/
```

in a plugin named

```
my-first-plugin
```

creates

```
/my-first-plugin:hello
```

).Create a skill directory in your plugin folder:

```
my-first-plugin/skills/hello/SKILL.md
```

with this content:

my-first-plugin/skills/hello/SKILL.md

Test your plugin

Run Claude Code with the Once Claude Code starts, try your new skill:You’ll see Claude respond with a greeting. Run

```
--plugin-dir
```

flag to load your plugin:

```
/help
```

to see your skill listed under the plugin namespace.

Why namespacing? Plugin skills are always namespaced (like

```
/my-first-plugin:hello
```

) to prevent conflicts when multiple plugins have skills with the same name.To change the namespace prefix, update the

```
name
```

field in

```
plugin.json
```

.

Add skill arguments

Make your skill dynamic by accepting user input. The Run Claude will greet you by name. For more on passing arguments to skills, see

```
$ARGUMENTS
```

placeholder captures any text the user provides after the skill name.Update your

```
SKILL.md
```

file:

my-first-plugin/skills/hello/SKILL.md

```
/reload-plugins
```

to pick up the changes, then try the skill with your name:[[Extend Claude with skills - Claude Code Docs#Pass arguments to skills|Skills]].

- Plugin manifest (

  ```
  .claude-plugin/plugin.json
  ```

  ): describes your plugin’s metadata
- Skills directory (

  ```
  skills/
  ```

  ): contains your custom skills
- Skill arguments (

  ```
  $ARGUMENTS
  ```

  ): captures user input for dynamic behavior

## Plugin structure overview

You’ve created a plugin with a skill, but plugins can include much more: custom agents, hooks, MCP servers, LSP servers, and background monitors.

DirectoryLocationPurpose

```
.claude-plugin/
```

Plugin rootContains

```
plugin.json
```

manifest (optional if components use default locations)

```
skills/
```

Plugin rootSkills as

```
<name>/SKILL.md
```

directories

```
commands/
```

Plugin rootSkills as flat Markdown files. Use

```
skills/
```

for new plugins

```
agents/
```

Plugin rootCustom agent definitions

```
hooks/
```

Plugin rootEvent handlers in

```
hooks.json
```

```
.mcp.json
```

Plugin rootMCP server configurations

```
.lsp.json
```

Plugin rootLSP server configurations for code intelligence

```
monitors/
```

Plugin rootBackground monitor configurations in

```
monitors.json
```

```
bin/
```

Plugin rootExecutables added to the Bash tool’s

```
PATH
```

while the plugin is enabled

```
settings.json
```

Plugin rootDefault

Next steps: Ready to add more features? Jump to

[[Create plugins - Claude Code Docs#Develop more complex plugins|Develop more complex plugins]]to add agents, hooks, MCP servers, and LSP servers. For complete technical specifications of all plugin components, see[[Plugins reference - Claude Code Docs|Plugins reference]].

## Develop more complex plugins

Once you’re comfortable with basic plugins, you can create more sophisticated extensions.

### Add Skills to your plugin

Plugins can include

[[Extend Claude with skills - Claude Code Docs|Agent Skills]]to extend Claude’s capabilities. Skills are model-invoked: Claude automatically uses them based on the task context. Add a

```
skills/
```

directory at your plugin root with Skill folders containing

```
SKILL.md
```

files:

```
SKILL.md
```

contains YAML frontmatter and instructions. Include a

```
description
```

so Claude knows when to use the skill:

```
/reload-plugins
```

to load the Skills. For complete Skill authoring guidance including progressive disclosure and tool restrictions, see

[[Extend Claude with skills - Claude Code Docs|Agent Skills]].

### Add LSP servers to your plugin

LSP (Language Server Protocol) plugins give Claude real-time code intelligence. If you need to support a language that doesn’t have an official LSP plugin, you can create your own by adding an

```
.lsp.json
```

file to your plugin:

.lsp.json

[[Plugins reference - Claude Code Docs#LSP servers|LSP servers]].

### Add background monitors to your plugin

Background monitors let your plugin watch logs, files, or external status in the background and notify Claude as events arrive. Claude Code starts each monitor automatically when the plugin is active, so you don’t need to instruct Claude to start the watch. Add a

```
monitors/monitors.json
```

file at the plugin root with an array of monitor entries:

monitors/monitors.json

```
command
```

is delivered to Claude as a notification during the session. For the full schema, including the

```
when
```

trigger and variable substitution, see

[[Plugins reference - Claude Code Docs#Monitors|Monitors]].

### Ship default settings with your plugin

Plugins can include a

```
settings.json
```

file at the plugin root to apply default configuration when the plugin is enabled. Currently, only the

```
agent
```

and

```
subagentStatusLine
```

keys are supported.
Setting

```
agent
```

activates one of the plugin’s

[[Create custom subagents - Claude Code Docs|custom agents]]as the main thread, applying its system prompt, tool restrictions, and model. This lets a plugin change how Claude Code behaves by default when enabled.

settings.json

```
security-reviewer
```

agent defined in the plugin’s

```
agents/
```

directory. Settings from

```
settings.json
```

take priority over

```
settings
```

declared in

```
plugin.json
```

. Unknown keys are silently ignored.

### Organize complex plugins

For plugins with many components, organize your directory structure by functionality. For complete directory layouts and organization patterns, see

[[Plugins reference - Claude Code Docs#Plugin directory structure|Plugin directory structure]].

### Test your plugins locally

Use the

```
--plugin-dir
```

flag to test plugins during development. This loads your plugin directly without requiring installation.

```
--plugin-dir
```

plugin has the same name as an installed marketplace plugin, the local copy takes precedence for that session. This lets you test changes to a plugin you already have installed without uninstalling it first. Marketplace plugins force-enabled by managed settings are the only exception and cannot be overridden.
As you make changes to your plugin, run

```
/reload-plugins
```

to pick up the updates without restarting. This reloads plugins, skills, agents, hooks, plugin MCP servers, and plugin LSP servers. Test your plugin components:

- Try your skills with

  ```
  /plugin-name:skill-name
  ```
- Check that agents appear in

  ```
  /agents
  ```
- Verify hooks work as expected

### Debug plugin issues

If your plugin isn’t working as expected:

- Check the structure: Ensure your directories are at the plugin root, not inside

  ```
  .claude-plugin/
  ```
- Test components individually: Check each skill, agent, and hook separately
- Use validation and debugging tools: See [[Plugins reference - Claude Code Docs#Debugging and development tools|Debugging and development tools]]for CLI commands and troubleshooting techniques

### Share your plugins

When your plugin is ready to share:

- Add documentation: Include a

  ```
  README.md
  ```

  with installation and usage instructions
- Choose a versioning strategy: Decide whether to set an explicit

  ```
  version
  ```

  or rely on the git commit SHA. See[[Plugins reference - Claude Code Docs#Version management|version management]]
- Create or use a marketplace: Distribute through [[Create and distribute a plugin marketplace - Claude Code Docs|plugin marketplaces]]for installation
- Test with others: Have team members test the plugin before wider distribution

[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs|Discover and install plugins]].

### Submit your plugin to the official marketplace

To submit a plugin to the official Anthropic marketplace, use one of the in-app submission forms:

- Claude.ai: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
- Console: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

[[Recommend your plugin from your CLI - Claude Code Docs|Recommend your plugin from your CLI]].

For complete technical specifications, debugging techniques, and distribution strategies, see

[[Plugins reference - Claude Code Docs|Plugins reference]].

## Convert existing configurations to plugins

If you already have skills or hooks in your

```
.claude/
```

directory, you can convert them into a plugin for easier sharing and distribution.

### Migration steps

Create the plugin structure

Create a new plugin directory:Create the manifest file at

```
my-plugin/.claude-plugin/plugin.json
```

:

my-plugin/.claude-plugin/plugin.json

Migrate hooks

If you have hooks in your settings, create a hooks directory:Create

```
my-plugin/hooks/hooks.json
```

with your hooks configuration. Copy the

```
hooks
```

object from your

```
.claude/settings.json
```

or

```
settings.local.json
```

, since the format is the same. The command receives hook input as JSON on stdin, so use

```
jq
```

to extract the file path:

my-plugin/hooks/hooks.json

### What changes when migrating

Standalone (

```
.claude/
```

)PluginOnly available in one projectCan be shared via marketplacesFiles in

```
.claude/commands/
```

Files in

```
plugin-name/commands/
```

Hooks in

```
settings.json
```

Hooks in

```
hooks/hooks.json
```

Must manually copy to shareInstall with

```
/plugin install
```

After migrating, you can remove the original files from

```
.claude/
```

to avoid duplicates. The plugin version will take precedence when loaded.

## Next steps

Now that you understand Claude Code’s plugin system, here are suggested paths for different goals:

### For plugin users

- [[Discover and install prebuilt plugins through marketplaces - Claude Code Docs|Discover and install plugins]]: browse marketplaces and install plugins
- [[Discover and install prebuilt plugins through marketplaces - Claude Code Docs#Configure team marketplaces|Configure team marketplaces]]: set up repository-level plugins for your team

### For plugin developers

- [[Create and distribute a plugin marketplace - Claude Code Docs|Create and distribute a marketplace]]: package and share your plugins
- [[Plugins reference - Claude Code Docs|Plugins reference]]: complete technical specifications
- Dive deeper into specific plugin components:

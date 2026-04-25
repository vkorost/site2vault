---
title: Plugins in the SDK - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/plugins
description: Load custom plugins to extend Claude Code with commands, agents, skills,
  and hooks through the Agent SDK
---

## What are plugins?

Plugins are packages of Claude Code extensions that can include:

- Skills: Model-invoked capabilities that Claude uses autonomously (can also be invoked with

  ```
  /skill-name
  ```

  )
- Agents: Specialized subagents for specific tasks
- Hooks: Event handlers that respond to tool use and other events
- MCP servers: External tool integrations via Model Context Protocol

The

```
commands/
```

directory is a legacy format. Use

```
skills/
```

for new plugins. Claude Code continues to support both formats for backward compatibility.

[[Create plugins - Claude Code Docs|Plugins]].

## Loading plugins

Load plugins by providing their local file system paths in your options configuration. The SDK supports loading multiple plugins from different locations.

### Path specifications

Plugin paths can be:

- Relative paths: Resolved relative to your current working directory (for example,

  ```
  "./plugins/my-plugin"
  ```

  )
- Absolute paths: Full file system paths (for example,

  ```
  "/home/user/plugins/my-plugin"
  ```

  )

The path should point to the plugin’s root directory (the directory containing

```
.claude-plugin/plugin.json
```

).

## Verifying plugin installation

When plugins load successfully, they appear in the system initialization message. You can verify that your plugins are available:

## Using plugin skills

Skills from plugins are automatically namespaced with the plugin name to avoid conflicts. When invoked as slash commands, the format is

```
plugin-name:skill-name
```

.

If you installed a plugin via the CLI (for example,

```
/plugin install my-plugin@marketplace
```

), you can still use it in the SDK by providing its installation path. Check

```
~/.claude/plugins/
```

for CLI-installed plugins.

## Complete example

Here’s a full example demonstrating plugin loading and usage:

## Plugin structure reference

A plugin directory must contain a

```
.claude-plugin/plugin.json
```

manifest file. It can optionally include:

- [[Create plugins - Claude Code Docs|Plugins]]- Complete plugin development guide
- [[Plugins reference - Claude Code Docs|Plugins reference]]- Technical specifications and schemas

## Common use cases

### Development and testing

Load plugins during development without installing them globally:

### Project-specific extensions

Include plugins in your project repository for team-wide consistency:

### Multiple plugin sources

Combine plugins from different locations:

## Troubleshooting

### Plugin not loading

If your plugin doesn’t appear in the init message:

- Check the path: Ensure the path points to the plugin root directory (containing

  ```
  .claude-plugin/
  ```

  )
- Validate plugin.json: Ensure your manifest file has valid JSON syntax
- Check file permissions: Ensure the plugin directory is readable

### Skills not appearing

If plugin skills don’t work:

- Use the namespace: Plugin skills require the

  ```
  plugin-name:skill-name
  ```

  format when invoked as slash commands
- Check init message: Verify the skill appears in

  ```
  slash_commands
  ```

  with the correct namespace
- Validate skill files: Ensure each skill has a

  ```
  SKILL.md
  ```

  file in its own subdirectory under

  ```
  skills/
  ```

  (for example,

  ```
  skills/my-skill/SKILL.md
  ```

  )

### Path resolution issues

If relative paths don’t work:

- Check working directory: Relative paths are resolved from your current working directory
- Use absolute paths: For reliability, consider using absolute paths
- Normalize paths: Use path utilities to construct paths correctly

## See also

- [[Create plugins - Claude Code Docs|Plugins]]- Complete plugin development guide
- [[Plugins reference - Claude Code Docs|Plugins reference]]- Technical specifications
- [[Slash Commands in the SDK - Claude Code Docs|Slash Commands]]- Using slash commands in the SDK
- [[Subagents in the SDK - Claude Code Docs|Subagents]]- Working with specialized agents
- [[Agent Skills in the SDK - Claude Code Docs|Skills]]- Using Agent Skills

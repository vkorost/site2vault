---
title: Agent Skills in the SDK - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/skills
description: Extend Claude with specialized capabilities using Agent Skills in the
  Claude Agent SDK
---

## Overview

Agent Skills extend Claude with specialized capabilities that Claude autonomously invokes when relevant. Skills are packaged as

```
SKILL.md
```

files containing instructions, descriptions, and optional supporting resources.
For comprehensive information about Skills, including benefits, architecture, and authoring guidelines, see the

[Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

## How Skills Work with the SDK

When using the Claude Agent SDK, Skills are:

- Defined as filesystem artifacts: Created as

  ```
  SKILL.md
  ```

  files in specific directories (

  ```
  .claude/skills/
  ```

  )
- Loaded from filesystem: Skills are loaded from filesystem locations governed by

  ```
  settingSources
  ```

  (TypeScript) or

  ```
  setting_sources
  ```

  (Python)
- Automatically discovered: Once filesystem settings are loaded, Skill metadata is discovered at startup from user and project directories; full content loaded when triggered
- Model-invoked: Claude autonomously chooses when to use them based on context
- Enabled via allowed\_tools: Add

  ```
  "Skill"
  ```

  to your

  ```
  allowed_tools
  ```

  to enable Skills

Skills are discovered through the filesystem setting sources. With default

```
query()
```

options, the SDK loads user and project sources, so skills in

```
~/.claude/skills/
```

and

```
<cwd>/.claude/skills/
```

are available. If you set

```
settingSources
```

explicitly, include

```
'user'
```

or

```
'project'
```

to keep skill discovery, or use the [[Plugins in the SDK - Claude Code Docs|to load skills from a specific path.]]

```
plugins
```

option

## Using Skills with the SDK

To use Skills with the SDK, you need to:

- Include

  ```
  "Skill"
  ```

  in your

  ```
  allowed_tools
  ```

  configuration
- Configure

  ```
  settingSources
  ```

  /

  ```
  setting_sources
  ```

  to load Skills from the filesystem

## Skill Locations

Skills are loaded from filesystem directories based on your

```
settingSources
```

/

```
setting_sources
```

configuration:

- Project Skills (

  ```
  .claude/skills/
  ```

  ): Shared with your team via git - loaded when

  ```
  setting_sources
  ```

  includes

  ```
  "project"
  ```
- User Skills (

  ```
  ~/.claude/skills/
  ```

  ): Personal Skills across all projects - loaded when

  ```
  setting_sources
  ```

  includes

  ```
  "user"
  ```
- Plugin Skills: Bundled with installed Claude Code plugins

## Creating Skills

Skills are defined as directories containing a

```
SKILL.md
```

file with YAML frontmatter and Markdown content. The

```
description
```

field determines when Claude invokes your Skill.
Example directory structure:

- [[Extend Claude with skills - Claude Code Docs|Agent Skills in Claude Code]]: Complete guide with examples
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): Authoring guidelines and naming conventions

## Tool Restrictions

The

```
allowed-tools
```

frontmatter field in SKILL.md is only supported when using Claude Code CLI directly. It does not apply when using Skills through the SDK.When using the SDK, control tool access through the main

```
allowedTools
```

option in your query configuration.

```
allowedTools
```

to pre-approve specific tools. Without a

```
canUseTool
```

callback, anything not in the list is denied:

Import statements from the first example are assumed in the following code snippets.

## Discovering Available Skills

To see which Skills are available in your SDK application, simply ask Claude:

## Testing Skills

Test Skills by asking questions that match their descriptions:

## Troubleshooting

### Skills Not Found

Check settingSources configuration: Skills are discovered through the

```
user
```

and

```
project
```

setting sources. If you set

```
settingSources
```

/

```
setting_sources
```

explicitly and omit those sources, skills are not loaded:

```
settingSources
```

/

```
setting_sources
```

, see the

[[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript SDK reference]]or

[[Agent SDK reference - Python - Claude Code Docs|Python SDK reference]]. Check working directory: The SDK loads Skills relative to the

```
cwd
```

option. Ensure it points to a directory containing

```
.claude/skills/
```

:

### Skill Not Being Used

Check the Skill tool is enabled: Confirm

```
"Skill"
```

is in your

```
allowedTools
```

.
Check the description: Ensure it’s specific and includes relevant keywords. See

[Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#writing-effective-descriptions)for guidance on writing effective descriptions.

### Additional Troubleshooting

For general Skills troubleshooting (YAML syntax, debugging, etc.), see the

[[Extend Claude with skills - Claude Code Docs#Troubleshooting|Claude Code Skills troubleshooting section]].

## Related Documentation

### Skills Guides

- [[Extend Claude with skills - Claude Code Docs|Agent Skills in Claude Code]]: Complete Skills guide with creation, examples, and troubleshooting
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview): Conceptual overview, benefits, and architecture
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): Authoring guidelines for effective Skills
- [Agent Skills Cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction): Example Skills and templates

### SDK Resources

- [[Subagents in the SDK - Claude Code Docs|Subagents in the SDK]]: Similar filesystem-based agents with programmatic options
- [[Slash Commands in the SDK - Claude Code Docs|Slash Commands in the SDK]]: User-invoked commands
- [[Agent SDK overview - Claude Code Docs|SDK Overview]]: General SDK concepts
- [[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript SDK Reference]]: Complete API documentation
- [[Agent SDK reference - Python - Claude Code Docs|Python SDK Reference]]: Complete API documentation

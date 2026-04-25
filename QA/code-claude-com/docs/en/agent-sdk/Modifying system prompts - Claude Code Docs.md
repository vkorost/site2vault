---
title: Modifying system prompts - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts
description: Learn how to customize Claude's behavior by modifying system prompts
  using three approaches - output styles, systemPrompt with append, and custom system
  prompts
---

## Understanding system prompts

A system prompt is the initial instruction set that shapes how Claude behaves throughout a conversation.

Default behavior: The Agent SDK uses a minimal system prompt by default. It contains only essential tool instructions but omits Claude Code’s coding guidelines, response style, and project context. To include the full Claude Code system prompt, specify

```
systemPrompt: { type: "preset", preset: "claude_code" }
```

in TypeScript or

```
system_prompt={"type": "preset", "preset": "claude_code"}
```

in Python.

- Tool usage instructions and available tools
- Code style and formatting guidelines
- Response tone and verbosity settings
- Security and safety instructions
- Context about the current working directory and environment

## Methods of modification

### Method 1: CLAUDE.md files (project-level instructions)

CLAUDE.md files provide project-specific context and instructions that are automatically read by the Agent SDK when it runs in a directory. They serve as persistent “memory” for your project.

#### How CLAUDE.md works with the SDK

Location and discovery:

- Project-level:

  ```
  CLAUDE.md
  ```

  or

  ```
  .claude/CLAUDE.md
  ```

  in your working directory
- User-level:

  ```
  ~/.claude/CLAUDE.md
  ```

  for global instructions across all projects

```
'project'
```

for project-level CLAUDE.md and

```
'user'
```

for

```
~/.claude/CLAUDE.md
```

. With default

```
query()
```

options both sources are enabled, so CLAUDE.md loads automatically. If you set

```
settingSources
```

(TypeScript) or

```
setting_sources
```

(Python) explicitly, include the sources you need. CLAUDE.md loading is controlled by setting sources, not by the

```
claude_code
```

preset.
Content format:
CLAUDE.md files use plain markdown and can contain:

- Coding guidelines and standards
- Project-specific context
- Common commands or workflows
- API conventions
- Testing requirements

#### Example CLAUDE.md

#### Using CLAUDE.md with the SDK

#### When to use CLAUDE.md

Best for:

- Team-shared context - Guidelines everyone should follow
- Project conventions - Coding standards, file structure, naming patterns
- Common commands - Build, test, deploy commands specific to your project
- Long-term memory - Context that should persist across all sessions
- Version-controlled instructions - Commit to git so the team stays in sync

- ✅ Persistent across all sessions in a project
- ✅ Shared with team via git
- ✅ Automatic discovery (no code changes needed)
- ⚠️ Not loaded if you pass

  ```
  settingSources: []
  ```

### Method 2: Output styles (persistent configurations)

Output styles are saved configurations that modify Claude’s system prompt. They’re stored as markdown files and can be reused across sessions and projects.

#### Creating an output style

#### Using output styles

Once created, activate output styles via:

- CLI:

  ```
  /output-style [style-name]
  ```
- Settings:

  ```
  .claude/settings.local.json
  ```
- Create new:

  ```
  /output-style:new [description]
  ```

```
settingSources: ['user']
```

or

```
settingSources: ['project']
```

(TypeScript) /

```
setting_sources=["user"]
```

or

```
setting_sources=["project"]
```

(Python) in your options.

### Method 3: Using ``` systemPrompt ``` with append

You can use the Claude Code preset with an

```
append
```

property to add your custom instructions while preserving all built-in functionality.

#### Improve prompt caching across users and machines

By default, two sessions that use the same

```
claude_code
```

preset and

```
append
```

text still cannot share a prompt cache entry if they run from different working directories. This is because the preset embeds per-session context in the system prompt ahead of your

```
append
```

text: the working directory, platform and OS version, current date, git status, and auto-memory paths. Any difference in that context produces a different system prompt and a cache miss.
To make the system prompt identical across sessions, set

```
excludeDynamicSections: true
```

in TypeScript or

```
"exclude_dynamic_sections": True
```

in Python. The per-session context moves into the first user message, leaving only the static preset and your

```
append
```

text in the system prompt so identical configurations share a cache entry across users and machines.

```
excludeDynamicSections
```

requires

```
@anthropic-ai/claude-agent-sdk
```

v0.2.98 or later, or

```
claude-agent-sdk
```

v0.1.58 or later for Python. It applies only to the preset object form and has no effect when

```
systemPrompt
```

is a string.

```
append
```

block with

```
excludeDynamicSections
```

so a fleet of agents running from different directories can reuse the same cached system prompt:

[[CLI reference - Claude Code Docs|.]]

```
--exclude-dynamic-system-prompt-sections
```

### Method 4: Custom system prompts

You can provide a custom string as

```
systemPrompt
```

to replace the default entirely with your own instructions.

## Comparison of all four approaches

FeatureCLAUDE.mdOutput Styles

```
systemPrompt
```

with appendCustom

```
systemPrompt
```

PersistencePer-project fileSaved as filesSession onlySession onlyReusabilityPer-projectAcross projectsCode duplicationCode duplicationManagementOn filesystemCLI + filesIn codeIn codeDefault toolsPreservedPreservedPreservedLost (unless included)Built-in safetyMaintainedMaintainedMaintainedMust be addedEnvironment contextAutomaticAutomaticAutomaticMust be providedCustomization levelAdditions onlyReplace defaultAdditions onlyComplete controlVersion controlWith projectYesWith codeWith codeScopeProject-specificUser or projectCode sessionCode session

```
systemPrompt: { type: "preset", preset: "claude_code", append: "..." }
```

in TypeScript or

```
system_prompt={"type": "preset", "preset": "claude_code", "append": "..."}
```

in Python.

## Use cases and best practices

### When to use CLAUDE.md

Best for:

- Project-specific coding standards and conventions
- Documenting project structure and architecture
- Listing common commands (build, test, deploy)
- Team-shared context that should be version controlled
- Instructions that apply to all SDK usage in a project

- “All API endpoints should use async/await patterns”
- “Run

  ```
  npm run lint:fix
  ```

  before committing”
- “Database migrations are in the

  ```
  migrations/
  ```

  directory”

```
project
```

setting source is enabled, which it is for default

```
query()
```

options. If you set

```
settingSources
```

(TypeScript) or

```
setting_sources
```

(Python) explicitly, include

```
'project'
```

to keep loading project-level CLAUDE.md.

### When to use output styles

Best for:

- Persistent behavior changes across sessions
- Team-shared configurations
- Specialized assistants (code reviewer, data scientist, DevOps)
- Complex prompt modifications that need versioning

- Creating a dedicated SQL optimization assistant
- Building a security-focused code reviewer
- Developing a teaching assistant with specific pedagogy

### When to use ``` systemPrompt ``` with append

Best for:

- Adding specific coding standards or preferences
- Customizing output formatting
- Adding domain-specific knowledge
- Modifying response verbosity
- Enhancing Claude Code’s default behavior without losing tool instructions

### When to use custom ``` systemPrompt ```

Best for:

- Complete control over Claude’s behavior
- Specialized single-session tasks
- Testing new prompt strategies
- Situations where default tools aren’t needed
- Building specialized agents with unique behavior

## Combining approaches

You can combine these methods for maximum flexibility:

### Example: Output style with session-specific additions

## See also

- [[Output styles - Claude Code Docs|Output styles]]- Complete output styles documentation
- [[Agent SDK reference - TypeScript - Claude Code Docs|TypeScript SDK guide]]- Complete SDK usage guide
- [[Claude Code settings - Claude Code Docs|Configuration guide]]- General configuration options

---
title: Extend Claude with skills - Claude Code Docs
source_url: https://code.claude.com/docs/en/skills
description: Create, manage, and share skills to extend Claude's capabilities in Claude
  Code. Includes custom commands and bundled skills.
---

```
SKILL.md
```

file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with

```
/skill-name
```

.
Create a skill when you keep pasting the same playbook, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact. Unlike CLAUDE.md content, a skill’s body loads only when it’s used, so long reference material costs almost nothing until you need it.

For built-in commands like

```
/help
```

and

```
/compact
```

, and bundled skills like

```
/debug
```

and

```
/simplify
```

, see the [[Commands - Claude Code Docs|commands reference]].Custom commands have been merged into skills. A file at

```
.claude/commands/deploy.md
```

and a skill at

```
.claude/skills/deploy/SKILL.md
```

both create

```
/deploy
```

and work the same way. Your existing

```
.claude/commands/
```

files keep working. Skills add optional features: a directory for supporting files, frontmatter to [[Extend Claude with skills - Claude Code Docs#Control who invokes a skill|control whether you or Claude invokes them]], and the ability for Claude to load them automatically when relevant.

[Agent Skills](https://agentskills.io)open standard, which works across multiple AI tools. Claude Code extends the standard with additional features like

[[Extend Claude with skills - Claude Code Docs#Control who invokes a skill|invocation control]],

[[Extend Claude with skills - Claude Code Docs#Run skills in a subagent|subagent execution]], and

[[Extend Claude with skills - Claude Code Docs#Inject dynamic context|dynamic context injection]].

## Bundled skills

Claude Code includes a set of bundled skills that are available in every session, including

```
/simplify
```

,

```
/batch
```

,

```
/debug
```

,

```
/loop
```

, and

```
/claude-api
```

. Unlike most built-in commands, which execute fixed logic directly, bundled skills are prompt-based: they give Claude a detailed playbook and let it orchestrate the work using its tools. You invoke them the same way as any other skill, by typing

```
/
```

followed by the skill name.
Bundled skills are listed alongside built-in commands in the

[[Commands - Claude Code Docs|commands reference]], marked Skill in the Purpose column.

## Getting started

### Create your first skill

This example creates a skill that teaches Claude to explain code using visual diagrams and analogies. Since it uses default frontmatter, Claude can load it automatically when you ask how something works, or you can invoke it directly with

```
/explain-code
```

.

Create the skill directory

Create a directory for the skill in your personal skills folder. Personal skills are available across all your projects.

Write SKILL.md

Every skill needs a

```
SKILL.md
```

file with two parts: YAML frontmatter (between

```
---
```

markers) that tells Claude when to use the skill, and markdown content with instructions Claude follows when the skill is invoked. The

```
name
```

field becomes the

```
/slash-command
```

, and the

```
description
```

helps Claude decide when to load it automatically.Create

```
~/.claude/skills/explain-code/SKILL.md
```

:

### Where skills live

Where you store a skill determines who can use it:

LocationPathApplies toEnterpriseSee

```
~/.claude/skills/<skill-name>/SKILL.md
```

```
.claude/skills/<skill-name>/SKILL.md
```

```
<plugin>/skills/<skill-name>/SKILL.md
```

```
plugin-name:skill-name
```

namespace, so they cannot conflict with other levels. If you have files in

```
.claude/commands/
```

, those work the same way, but if a skill and a command share the same name, the skill takes precedence.

#### Live change detection

Claude Code watches skill directories for file changes. Adding, editing, or removing a skill under

```
~/.claude/skills/
```

, the project

```
.claude/skills/
```

, or a

```
.claude/skills/
```

inside an

```
--add-dir
```

directory takes effect within the current session without restarting. Creating a top-level skills directory that did not exist when the session started requires restarting Claude Code so the new directory can be watched.

#### Automatic discovery from nested directories

When you work with files in subdirectories, Claude Code automatically discovers skills from nested

```
.claude/skills/
```

directories. For example, if you’re editing a file in

```
packages/frontend/
```

, Claude Code also looks for skills in

```
packages/frontend/.claude/skills/
```

. This supports monorepo setups where packages have their own skills.
Each skill is a directory with

```
SKILL.md
```

as the entrypoint:

```
SKILL.md
```

contains the main instructions and is required. Other files are optional and let you build more powerful skills: templates for Claude to fill in, example outputs showing the expected format, scripts Claude can execute, or detailed reference documentation. Reference these files from your

```
SKILL.md
```

so Claude knows what they contain and when to load them. See

[[Extend Claude with skills - Claude Code Docs#Add supporting files|Add supporting files]]for more details.

Files in

```
.claude/commands/
```

still work and support the same [[Extend Claude with skills - Claude Code Docs#Frontmatter reference|frontmatter]]. Skills are recommended since they support additional features like supporting files.

#### Skills from additional directories

The

```
--add-dir
```

flag

[[Configure permissions - Claude Code Docs#Additional directories grant file access, not configuration|grants file access]]rather than configuration discovery, but skills are an exception:

```
.claude/skills/
```

within an added directory is loaded automatically. See

[[Extend Claude with skills - Claude Code Docs#Live change detection|Live change detection]]for how edits are picked up during a session. Other

```
.claude/
```

configuration such as subagents, commands, and output styles is not loaded from additional directories. See the

[[Configure permissions - Claude Code Docs#Additional directories grant file access, not configuration|exceptions table]]for the complete list of what is and isn’t loaded, and the recommended ways to share configuration across projects.

CLAUDE.md files from

```
--add-dir
```

directories are not loaded by default. To load them, set

```
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
```

. See [[How Claude remembers your project - Claude Code Docs#Load from additional directories|Load from additional directories]].

## Configure skills

Skills are configured through YAML frontmatter at the top of

```
SKILL.md
```

and the markdown content that follows.

### Types of skill content

Skill files can contain any instructions, but thinking about how you want to invoke them helps guide what to include: Reference content adds knowledge Claude applies to your current work. Conventions, patterns, style guides, domain knowledge. This content runs inline so Claude can use it alongside your conversation context.

```
/skill-name
```

rather than letting Claude decide when to run them. Add

```
disable-model-invocation: true
```

to prevent Claude from triggering it automatically.

```
SKILL.md
```

can contain anything, but thinking through how you want the skill invoked (by you, by Claude, or both) and where you want it to run (inline or in a subagent) helps guide what to include. For complex skills, you can also

[[Extend Claude with skills - Claude Code Docs#Add supporting files|add supporting files]]to keep the main skill focused.

### Frontmatter reference

Beyond the markdown content, you can configure skill behavior using YAML frontmatter fields between

```
---
```

markers at the top of your

```
SKILL.md
```

file:

```
description
```

is recommended so Claude knows when to use the skill.

FieldRequiredDescription

```
name
```

NoDisplay name for the skill. If omitted, uses the directory name. Lowercase letters, numbers, and hyphens only (max 64 characters).

```
description
```

RecommendedWhat the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first paragraph of markdown content. Front-load the key use case: the combined

```
description
```

and

```
when_to_use
```

text is truncated at 1,536 characters in the skill listing to reduce context usage.

```
when_to_use
```

NoAdditional context for when Claude should invoke the skill, such as trigger phrases or example requests. Appended to

```
description
```

in the skill listing and counts toward the 1,536-character cap.

```
argument-hint
```

NoHint shown during autocomplete to indicate expected arguments. Example:

```
[issue-number]
```

or

```
[filename] [format]
```

.

```
arguments
```

NoNamed positional arguments for

```
$name
```

substitution

```
disable-model-invocation
```

```
true
```

to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with

```
/name
```

. Also prevents the skill from being [[Create custom subagents - Claude Code Docs#Preload skills into subagents|preloaded into subagents]]. Default:

```
false
```

.

```
user-invocable
```

```
false
```

to hide from the

```
/
```

menu. Use for background knowledge users shouldn’t invoke directly. Default:

```
true
```

.

```
allowed-tools
```

```
model
```

[[Model configuration - Claude Code Docs|, or]]

```
/model
```

```
inherit
```

to keep the active model.

```
effort
```

[[Model configuration - Claude Code Docs#Adjust effort level|Effort level]]when this skill is active. Overrides the session effort level. Default: inherits from session. Options:

```
low
```

,

```
medium
```

,

```
high
```

,

```
xhigh
```

,

```
max
```

; available levels depend on the model.

```
context
```

```
fork
```

to run in a forked subagent context.

```
agent
```

```
context: fork
```

is set.

```
hooks
```

[[Hooks reference - Claude Code Docs#Hooks in skills and agents|Hooks in skills and agents]]for configuration format.

```
paths
```

[[How Claude remembers your project - Claude Code Docs#Path-specific rules|path-specific rules]].

```
shell
```

```
!`command`
```

and

```
```!
```

blocks in this skill. Accepts

```
bash
```

(default) or

```
powershell
```

. Setting

```
powershell
```

runs inline shell commands via PowerShell on Windows. Requires

```
CLAUDE_CODE_USE_POWERSHELL_TOOL=1
```

.

#### Available string substitutions

Skills support string substitution for dynamic values in the skill content:

VariableDescription

```
$ARGUMENTS
```

All arguments passed when invoking the skill. If

```
$ARGUMENTS
```

is not present in the content, arguments are appended as

```
ARGUMENTS: <value>
```

.

```
$ARGUMENTS[N]
```

Access a specific argument by 0-based index, such as

```
$ARGUMENTS[0]
```

for the first argument.

```
$N
```

Shorthand for

```
$ARGUMENTS[N]
```

, such as

```
$0
```

for the first argument or

```
$1
```

for the second.

```
$name
```

Named argument declared in the

```
arguments
```

```
arguments: [issue, branch]
```

the placeholder

```
$issue
```

expands to the first argument and

```
$branch
```

to the second.

```
${CLAUDE_SESSION_ID}
```

```
${CLAUDE_SKILL_DIR}
```

```
SKILL.md
```

file. For plugin skills, this is the skill’s subdirectory within the plugin, not the plugin root. Use this in bash injection commands to reference scripts or files bundled with the skill, regardless of the current working directory.

```
/my-skill "hello world" second
```

makes

```
$0
```

expand to

```
hello world
```

and

```
$1
```

to

```
second
```

. The

```
$ARGUMENTS
```

placeholder always expands to the full argument string as typed.
Example using substitutions:

### Add supporting files

Skills can include multiple files in their directory. This keeps

```
SKILL.md
```

focused on the essentials while letting Claude access detailed reference material only when needed. Large reference docs, API specifications, or example collections don’t need to load into context every time the skill runs.

```
SKILL.md
```

so Claude knows what each file contains and when to load it:

### Control who invokes a skill

By default, both you and Claude can invoke any skill. You can type

```
/skill-name
```

to invoke it directly, and Claude can load it automatically when relevant to your conversation. Two frontmatter fields let you restrict this:

- ```
  disable-model-invocation: true
  ```

  : Only you can invoke the skill. Use this for workflows with side effects or that you want to control timing, like

  ```
  /commit
  ```

  ,

  ```
  /deploy
  ```

  , or

  ```
  /send-slack-message
  ```

  . You don’t want Claude deciding to deploy because your code looks ready.
- ```
  user-invocable: false
  ```

  : Only Claude can invoke the skill. Use this for background knowledge that isn’t actionable as a command. A

  ```
  legacy-system-context
  ```

  skill explains how an old system works. Claude should know this when relevant, but

  ```
  /legacy-system-context
  ```

  isn’t a meaningful action for users to take.

```
disable-model-invocation: true
```

field prevents Claude from running it automatically:

FrontmatterYou can invokeClaude can invokeWhen loaded into context(default)YesYesDescription always in context, full skill loads when invoked

```
disable-model-invocation: true
```

YesNoDescription not in context, full skill loads when you invoke

```
user-invocable: false
```

NoYesDescription always in context, full skill loads when invoked

In a regular session, skill descriptions are loaded into context so Claude knows what’s available, but full skill content only loads when invoked.

[[Create custom subagents - Claude Code Docs#Preload skills into subagents|Subagents with preloaded skills]]work differently: the full skill content is injected at startup.

### Skill content lifecycle

When you or Claude invoke a skill, the rendered

```
SKILL.md
```

content enters the conversation as a single message and stays there for the rest of the session. Claude Code does not re-read the skill file on later turns, so write guidance that should apply throughout a task as standing instructions rather than one-time steps.

[[How Claude Code works - Claude Code Docs#When context fills up|Auto-compaction]]carries invoked skills forward within a token budget. When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens. Claude Code fills this budget starting from the most recently invoked skill, so older skills can be dropped entirely after compaction if you have invoked many in one session. If a skill seems to stop influencing behavior after the first response, the content is usually still present and the model is choosing other tools or approaches. Strengthen the skill’s

```
description
```

and instructions so the model keeps preferring it, or use

[[Hooks reference - Claude Code Docs|hooks]]to enforce behavior deterministically. If the skill is large or you invoked several others after it, re-invoke it after compaction to restore the full content.

### Pre-approve tools for a skill

The

```
allowed-tools
```

field grants permission for the listed tools while the skill is active, so Claude can use them without prompting you for approval. It does not restrict which tools are available: every tool remains callable, and your

[[Configure permissions - Claude Code Docs|permission settings]]still govern tools that are not listed. This skill lets Claude run git commands without per-use approval whenever you invoke it:

[[Configure permissions - Claude Code Docs|permission settings]]instead.

### Pass arguments to skills

Both you and Claude can pass arguments when invoking a skill. Arguments are available via the

```
$ARGUMENTS
```

placeholder.
This skill fixes a GitHub issue by number. The

```
$ARGUMENTS
```

placeholder gets replaced with whatever follows the skill name:

```
/fix-issue 123
```

, Claude receives “Fix GitHub issue 123 following our coding standards…”
If you invoke a skill with arguments but the skill doesn’t include

```
$ARGUMENTS
```

, Claude Code appends

```
ARGUMENTS: <your input>
```

to the end of the skill content so Claude still sees what you typed.
To access individual arguments by position, use

```
$ARGUMENTS[N]
```

or the shorter

```
$N
```

:

```
/migrate-component SearchBar React Vue
```

replaces

```
$ARGUMENTS[0]
```

with

```
SearchBar
```

,

```
$ARGUMENTS[1]
```

with

```
React
```

, and

```
$ARGUMENTS[2]
```

with

```
Vue
```

. The same skill using the

```
$N
```

shorthand:

## Advanced patterns

### Inject dynamic context

The

```
!`<command>`
```

syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data, not the command itself.
This skill summarizes a pull request by fetching live PR data with the GitHub CLI. The

```
!`gh pr diff`
```

and other commands run first, and their output gets inserted into the prompt:

- Each

  ```
  !`<command>`
  ```

  executes immediately (before Claude sees anything)
- The output replaces the placeholder in the skill content
- Claude receives the fully-rendered prompt with actual PR data

```
```!
```

instead of the inline form:

[[Extend Claude with skills - Claude Code Docs#Skills from additional directories|additional-directory]]sources, set

```
"disableSkillShellExecution": true
```

in

[[Claude Code settings - Claude Code Docs|settings]]. Each command is replaced with

```
[shell command execution disabled by policy]
```

instead of being run. Bundled and managed skills are not affected. This setting is most useful in

[[Configure permissions - Claude Code Docs#Managed settings|managed settings]], where users cannot override it.

### Run skills in a subagent

Add

```
context: fork
```

to your frontmatter when you want a skill to run in isolation. The skill content becomes the prompt that drives the subagent. It won’t have access to your conversation history.
Skills and

[[Create custom subagents - Claude Code Docs|subagents]]work together in two directions:

ApproachSystem promptTaskAlso loadsSkill with

```
context: fork
```

From agent type (

```
Explore
```

,

```
Plan
```

, etc.)SKILL.md contentCLAUDE.mdSubagent with

```
skills
```

fieldSubagent’s markdown bodyClaude’s delegation messagePreloaded skills + CLAUDE.md

```
context: fork
```

, you write the task in your skill and pick an agent type to execute it. For the inverse (defining a custom subagent that uses skills as reference material), see

[[Create custom subagents - Claude Code Docs#Preload skills into subagents|Subagents]].

#### Example: Research skill using Explore agent

This skill runs research in a forked Explore agent. The skill content becomes the task, and the agent provides read-only tools optimized for codebase exploration:

- A new isolated context is created
- The subagent receives the skill content as its prompt (“Research $ARGUMENTS thoroughly…”)
- The

  ```
  agent
  ```

  field determines the execution environment (model, tools, and permissions)
- Results are summarized and returned to your main conversation

```
agent
```

field specifies which subagent configuration to use. Options include built-in agents (

```
Explore
```

,

```
Plan
```

,

```
general-purpose
```

) or any custom subagent from

```
.claude/agents/
```

. If omitted, uses

```
general-purpose
```

.

### Restrict Claude’s skill access

By default, Claude can invoke any skill that doesn’t have

```
disable-model-invocation: true
```

set. Skills that define

```
allowed-tools
```

grant Claude access to those tools without per-use approval when the skill is active. Your

[[Configure permissions - Claude Code Docs|permission settings]]still govern baseline approval behavior for all other tools. A few built-in commands are also available through the Skill tool, including

```
/init
```

,

```
/review
```

, and

```
/security-review
```

. Other built-in commands such as

```
/compact
```

are not.
Three ways to control which skills Claude can invoke:
Disable all skills by denying the Skill tool in

```
/permissions
```

:

[[Configure permissions - Claude Code Docs|permission rules]]:

```
Skill(name)
```

for exact match,

```
Skill(name *)
```

for prefix match with any arguments.
Hide individual skills by adding

```
disable-model-invocation: true
```

to their frontmatter. This removes the skill from Claude’s context entirely.

The

```
user-invocable
```

field only controls menu visibility, not Skill tool access. Use

```
disable-model-invocation: true
```

to block programmatic invocation.

## Share skills

Skills can be distributed at different scopes depending on your audience:

- Project skills: Commit

  ```
  .claude/skills/
  ```

  to version control
- Plugins: Create a

  ```
  skills/
  ```

  directory in your[[Create plugins - Claude Code Docs|plugin]]
- Managed: Deploy organization-wide through [[Claude Code settings - Claude Code Docs#Settings files|managed settings]]

### Generate visual output

Skills can bundle and run scripts in any language, giving Claude capabilities beyond what’s possible in a single prompt. One powerful pattern is generating visual output: interactive HTML files that open in your browser for exploring data, debugging, or creating reports. This example creates a codebase explorer: an interactive tree view where you can expand and collapse directories, see file sizes at a glance, and identify file types by color. Create the Skill directory:

```
~/.claude/skills/codebase-visualizer/SKILL.md
```

. The description tells Claude when to activate this Skill, and the instructions tell Claude to run the bundled script:

```
~/.claude/skills/codebase-visualizer/scripts/visualize.py
```

. This script scans a directory tree and generates a self-contained HTML file with:

- A summary sidebar showing file count, directory count, total size, and number of file types
- A bar chart breaking down the codebase by file type (top 8 by size)
- A collapsible tree where you can expand and collapse directories, with color-coded file type indicators

```
codebase-map.html
```

, and opens it in your browser.
This pattern works for any visual output: dependency graphs, test coverage reports, API documentation, or database schema visualizations. The bundled script does the heavy lifting while Claude handles orchestration.

## Troubleshooting

### Skill not triggering

If Claude doesn’t use your skill when expected:

- Check the description includes keywords users would naturally say
- Verify the skill appears in

  ```
  What skills are available?
  ```
- Try rephrasing your request to match the description more closely
- Invoke it directly with

  ```
  /skill-name
  ```

  if the skill is user-invocable

### Skill triggers too often

If Claude uses your skill when you don’t want it:

- Make the description more specific
- Add

  ```
  disable-model-invocation: true
  ```

  if you only want manual invocation

### Skill descriptions are cut short

Skill descriptions are loaded into context so Claude knows what’s available. All skill names are always included, but if you have many skills, descriptions are shortened to fit the character budget, which can strip the keywords Claude needs to match your request. The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters. To raise the limit, set the

```
SLASH_COMMAND_TOOL_CHAR_BUDGET
```

environment variable. Or trim the

```
description
```

and

```
when_to_use
```

text at the source: front-load the key use case, since each entry’s combined text is capped at 1,536 characters regardless of budget.

## Related resources

- [[Debug your configuration - Claude Code Docs|Debug your configuration]]: diagnose why a skill isn’t appearing or triggering
- [[Create custom subagents - Claude Code Docs|Subagents]]: delegate tasks to specialized agents
- [[Create plugins - Claude Code Docs|Plugins]]: package and distribute skills with other extensions
- [[Hooks reference - Claude Code Docs|Hooks]]: automate workflows around tool events
- [[How Claude remembers your project - Claude Code Docs|Memory]]: manage CLAUDE.md files for persistent context
- [[Commands - Claude Code Docs|Commands]]: reference for built-in commands and bundled skills
- [[Configure permissions - Claude Code Docs|Permissions]]: control tool and skill access

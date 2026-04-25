---
title: Discover and install prebuilt plugins through marketplaces - Claude Code Docs
source_url: https://code.claude.com/docs/en/discover-plugins
description: Find and install plugins from marketplaces to extend Claude Code with
  new skills, agents, and capabilities.
---

[[Create and distribute a plugin marketplace - Claude Code Docs|Create and distribute a plugin marketplace]].

## How marketplaces work

A marketplace is a catalog of plugins that someone else has created and shared. Using a marketplace is a two-step process:

Add the marketplace

This registers the catalog with Claude Code so you can browse what’s available. No plugins are installed yet.

## Official Anthropic marketplace

The official Anthropic marketplace (

```
claude-plugins-official
```

) is automatically available when you start Claude Code. Run

```
/plugin
```

and go to the Discover tab to browse what’s available, or view the catalog at

[claude.com/plugins](https://claude.com/plugins). To install a plugin from the official marketplace, use

```
/plugin install <name>@claude-plugins-official
```

. For example, to install the GitHub integration:

```
/plugin marketplace update claude-plugins-official
```

to refresh it, or

```
/plugin marketplace add anthropics/claude-plugins-official
```

if you haven’t added it before. Then retry the install.

The official marketplace is maintained by Anthropic. To submit a plugin to the official marketplace, use one of the in-app submission forms:

- Claude.ai: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
- Console: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

[[Create and distribute a plugin marketplace - Claude Code Docs|create your own marketplace]]and share it with users.

### Code intelligence

Code intelligence plugins enable Claude Code’s built-in LSP tool, giving Claude the ability to jump to definitions, find references, and see type errors immediately after edits. These plugins configure

[Language Server Protocol](https://microsoft.github.io/language-server-protocol/)connections, the same technology that powers VS Code’s code intelligence. These plugins require the language server binary to be installed on your system. If you already have a language server installed, Claude may prompt you to install the corresponding plugin when you open a project.

LanguagePluginBinary requiredC/C++

```
clangd-lsp
```

```
clangd
```

C#

```
csharp-lsp
```

```
csharp-ls
```

Go

```
gopls-lsp
```

```
gopls
```

Java

```
jdtls-lsp
```

```
jdtls
```

Kotlin

```
kotlin-lsp
```

```
kotlin-language-server
```

Lua

```
lua-lsp
```

```
lua-language-server
```

PHP

```
php-lsp
```

```
intelephense
```

Python

```
pyright-lsp
```

```
pyright-langserver
```

Rust

```
rust-analyzer-lsp
```

```
rust-analyzer
```

Swift

```
swift-lsp
```

```
sourcekit-lsp
```

TypeScript

```
typescript-lsp
```

```
typescript-language-server
```

[[Plugins reference - Claude Code Docs#LSP servers|create your own LSP plugin]]for other languages.

If you see

```
Executable not found in $PATH
```

in the

```
/plugin
```

Errors tab after installing a plugin, install the required binary from the table above.

#### What Claude gains from code intelligence plugins

Once a code intelligence plugin is installed and its language server binary is available, Claude gains two capabilities:

- Automatic diagnostics: after every file edit Claude makes, the language server analyzes the changes and reports errors and warnings back automatically. Claude sees type errors, missing imports, and syntax issues without needing to run a compiler or linter. If Claude introduces an error, it notices and fixes the issue in the same turn. This requires no configuration beyond installing the plugin. You can see diagnostics inline by pressing Ctrl+O when the “diagnostics found” indicator appears.
- Code navigation: Claude can use the language server to jump to definitions, find references, get type info on hover, list symbols, find implementations, and trace call hierarchies. These operations give Claude more precise navigation than grep-based search, though availability may vary by language and environment.

[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs#Code intelligence issues|Code intelligence troubleshooting]].

### External integrations

These plugins bundle pre-configured

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP servers]]so you can connect Claude to external services without manual setup:

- Source control:

  ```
  github
  ```

  ,

  ```
  gitlab
  ```
- Project management:

  ```
  atlassian
  ```

  (Jira/Confluence),

  ```
  asana
  ```

  ,

  ```
  linear
  ```

  ,

  ```
  notion
  ```
- Design:

  ```
  figma
  ```
- Infrastructure:

  ```
  vercel
  ```

  ,

  ```
  firebase
  ```

  ,

  ```
  supabase
  ```
- Communication:

  ```
  slack
  ```
- Monitoring:

  ```
  sentry
  ```

### Development workflows

Plugins that add skills and agents for common development tasks:

- commit-commands: Git commit workflows including commit, push, and PR creation
- pr-review-toolkit: Specialized agents for reviewing pull requests
- agent-sdk-dev: Tools for building with the Claude Agent SDK
- plugin-dev: Toolkit for creating your own plugins

### Output styles

Customize how Claude responds:

- explanatory-output-style: Educational insights about implementation choices
- learning-output-style: Interactive learning mode for skill building

## Try it: add the demo marketplace

Anthropic also maintains a

[demo plugins marketplace](https://github.com/anthropics/claude-code/tree/main/plugins)(

```
claude-code-plugins
```

) with example plugins that show what’s possible with the plugin system. Unlike the official marketplace, you need to add this one manually.

Add the marketplace

From within Claude Code, run the This downloads the marketplace catalog and makes its plugins available to you.

```
plugin marketplace add
```

command for the

```
anthropics/claude-code
```

marketplace:

Browse available plugins

Run

```
/plugin
```

to open the plugin manager. This opens a tabbed interface with four tabs you can cycle through using Tab (or Shift+Tab to go backward):

- Discover: browse available plugins from all your marketplaces
- Installed: view and manage your installed plugins
- Marketplaces: add, remove, or update your added marketplaces
- Errors: view any plugin loading errors

Install a plugin

Select a plugin to view its details, then choose an installation scope:See

- User scope: install for yourself across all projects
- Project scope: install for all collaborators on this repository
- Local scope: install for yourself in this repository only

[[Claude Code settings - Claude Code Docs#Configuration scopes|Configuration scopes]]to learn more about scopes.

Use your new plugin

After installing, run This stages your changes, generates a commit message, and creates the commit.Each plugin works differently. Check the plugin’s description in the Discover tab or its homepage to learn what skills and capabilities it provides.

```
/reload-plugins
```

to activate the plugin. Plugin skills are namespaced by the plugin name, so commit-commands provides skills like

```
/commit-commands:commit
```

.Try it out by making a change to a file and running:

## Add marketplaces

Use the

```
/plugin marketplace add
```

command to add marketplaces from different sources.

- GitHub repositories:

  ```
  owner/repo
  ```

  format (for example,

  ```
  anthropics/claude-code
  ```

  )
- Git URLs: any git repository URL (GitLab, Bitbucket, self-hosted)
- Local paths: directories or direct paths to

  ```
  marketplace.json
  ```

  files
- Remote URLs: direct URLs to hosted

  ```
  marketplace.json
  ```

  files

### Add from GitHub

Add a GitHub repository that contains a

```
.claude-plugin/marketplace.json
```

file using the

```
owner/repo
```

format—where

```
owner
```

is the GitHub username or organization and

```
repo
```

is the repository name.
For example,

```
anthropics/claude-code
```

refers to the

```
claude-code
```

repository owned by

```
anthropics
```

:

### Add from other Git hosts

Add any git repository by providing the full URL. This works with any Git host, including GitLab, Bitbucket, and self-hosted servers: Using HTTPS:

```
#
```

followed by the ref:

### Add from local paths

Add a local directory that contains a

```
.claude-plugin/marketplace.json
```

file:

```
marketplace.json
```

file:

### Add from remote URLs

Add a remote

```
marketplace.json
```

file via URL:

URL-based marketplaces have some limitations compared to Git-based marketplaces. If you encounter “path not found” errors when installing plugins, see

[[Create and distribute a plugin marketplace - Claude Code Docs#Plugins with relative paths fail in URL-based marketplaces|Troubleshooting]].

## Install plugins

Once you’ve added marketplaces, you can install plugins directly (installs to user scope by default):

[[Claude Code settings - Claude Code Docs#Configuration scopes|installation scope]], use the interactive UI: run

```
/plugin
```

, go to the Discover tab, and press Enter on a plugin. You’ll see options for:

- User scope (default): install for yourself across all projects
- Project scope: install for all collaborators on this repository (adds to

  ```
  .claude/settings.json
  ```

  )
- Local scope: install for yourself in this repository only (not shared with collaborators)

[[Claude Code settings - Claude Code Docs#Settings files|managed settings]]and cannot be modified.

## Manage installed plugins

Run

```
/plugin
```

and go to the Installed tab to view, enable, disable, or uninstall your plugins. The list is grouped by scope and sorted so you see problems first: plugins with load errors or unresolved dependencies appear at the top, followed by your favorites, with disabled plugins folded behind a collapsed header at the bottom.
From the list you can:

- press

  ```
  f
  ```

  to favorite or unfavorite the selected plugin
- type to filter by plugin name or description
- press Enter to open a plugin’s detail view and enable, disable, or uninstall it

```
--scope
```

option lets you target a specific scope with CLI commands:

### Apply plugin changes without restarting

When you install, enable, or disable plugins during a session, run

```
/reload-plugins
```

to pick up all changes without restarting:

## Manage marketplaces

You can manage marketplaces through the interactive

```
/plugin
```

interface or with CLI commands.

### Use the interactive interface

Run

```
/plugin
```

and go to the Marketplaces tab to:

- View all your added marketplaces with their sources and status
- Add new marketplaces
- Update marketplace listings to fetch the latest plugins
- Remove marketplaces you no longer need

### Use CLI commands

You can also manage marketplaces with direct commands. List all configured marketplaces:

### Configure auto-updates

Claude Code can automatically update marketplaces and their installed plugins at startup. When auto-update is enabled for a marketplace, Claude Code refreshes the marketplace data and updates installed plugins to their latest versions. If any plugins were updated, you’ll see a notification prompting you to run

```
/reload-plugins
```

.
Toggle auto-update for individual marketplaces through the UI:

- Run

  ```
  /plugin
  ```

  to open the plugin manager
- Select Marketplaces
- Choose a marketplace from the list
- Select Enable auto-update or Disable auto-update

```
DISABLE_AUTOUPDATER
```

environment variable. See

[[Advanced setup - Claude Code Docs#Auto-updates|Auto updates]]for details. To keep plugin auto-updates enabled while disabling Claude Code auto-updates, set

```
FORCE_AUTOUPDATE_PLUGINS=1
```

along with

```
DISABLE_AUTOUPDATER
```

:

## Configure team marketplaces

Team admins can set up automatic marketplace installation for projects by adding marketplace configuration to

```
.claude/settings.json
```

. When team members trust the repository folder, Claude Code prompts them to install these marketplaces and plugins.
Add

```
extraKnownMarketplaces
```

to your project’s

```
.claude/settings.json
```

:

```
extraKnownMarketplaces
```

and

```
enabledPlugins
```

, see

[[Claude Code settings - Claude Code Docs#Plugin settings|Plugin settings]].

## Security

Plugins and marketplaces are highly trusted components that can execute arbitrary code on your machine with your user privileges. Only install plugins and add marketplaces from sources you trust. Organizations can restrict which marketplaces users are allowed to add using

[[Create and distribute a plugin marketplace - Claude Code Docs#Managed marketplace restrictions|managed marketplace restrictions]].

## Troubleshooting

### /plugin command not recognized

If you see “unknown command” or the

```
/plugin
```

command doesn’t appear:

- Check your version: Run

  ```
  claude --version
  ```

  to see what’s installed.
- Update Claude Code:
  - Homebrew:

    ```
    brew upgrade claude-code
    ```

    (or

    ```
    brew upgrade claude-code@latest
    ```

    if you installed that cask)
  - npm:

    ```
    npm update -g @anthropic-ai/claude-code
    ```
  - Native installer: Re-run the install command from [[Advanced setup - Claude Code Docs|Setup]]
- Homebrew:
- Restart Claude Code: After updating, restart your terminal and run

  ```
  claude
  ```

  again.

### Common issues

- Marketplace not loading: Verify the URL is accessible and that

  ```
  .claude-plugin/marketplace.json
  ```

  exists at the path
- Plugin installation failures: Check that plugin source URLs are accessible and repositories are public (or you have access)
- Files not found after installation: Plugins are copied to a cache, so paths referencing files outside the plugin directory won’t work
- Plugin skills not appearing: Clear the cache with

  ```
  rm -rf ~/.claude/plugins/cache
  ```

  , restart Claude Code, and reinstall the plugin.

[[Create and distribute a plugin marketplace - Claude Code Docs#Troubleshooting|Troubleshooting]]in the marketplace guide. For debugging tools, see

[[Plugins reference - Claude Code Docs#Debugging and development tools|Debugging and development tools]].

### Code intelligence issues

- Language server not starting: verify the binary is installed and available in your

  ```
  $PATH
  ```

  . Check the

  ```
  /plugin
  ```

  Errors tab for details.
- High memory usage: language servers like

  ```
  rust-analyzer
  ```

  and

  ```
  pyright
  ```

  can consume significant memory on large projects. If you experience memory issues, disable the plugin with

  ```
  /plugin disable <plugin-name>
  ```

  and rely on Claude’s built-in search tools instead.
- False positive diagnostics in monorepos: language servers may report unresolved import errors for internal packages if the workspace isn’t configured correctly. These don’t affect Claude’s ability to edit code.

## Next steps

- Build your own plugins: See [[Create plugins - Claude Code Docs|Plugins]]to create skills, agents, and hooks
- Create a marketplace: See [[Create and distribute a plugin marketplace - Claude Code Docs|Create a plugin marketplace]]to distribute plugins to your team or community
- Technical reference: See [[Plugins reference - Claude Code Docs|Plugins reference]]for complete specifications

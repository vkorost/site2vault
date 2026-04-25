---
title: Create and distribute a plugin marketplace - Claude Code Docs
source_url: https://code.claude.com/docs/en/plugin-marketplaces
description: Build and host plugin marketplaces to distribute Claude Code extensions
  across teams and communities.
---

[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs|Discover and install prebuilt plugins]].

## Overview

Creating and distributing a marketplace involves:

- Creating plugins: build one or more plugins with skills, agents, hooks, MCP servers, or LSP servers. This guide assumes you already have plugins to distribute; see [[Create plugins - Claude Code Docs|Create plugins]]for details on how to create them.
- Creating a marketplace file: define a

  ```
  marketplace.json
  ```

  that lists your plugins and where to find them (see[[Create and distribute a plugin marketplace - Claude Code Docs#Create the marketplace file|Create the marketplace file]]).
- Host the marketplace: push to GitHub, GitLab, or another git host (see [[Create and distribute a plugin marketplace - Claude Code Docs#Host and distribute marketplaces|Host and distribute marketplaces]]).
- Share with users: users add your marketplace with

  ```
  /plugin marketplace add
  ```

  and install individual plugins (see[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs|Discover and install plugins]]).

```
/plugin marketplace update
```

.

## Walkthrough: create a local marketplace

This example creates a marketplace with one plugin: a

```
/quality-review
```

skill for code reviews. You’ll create the directory structure, add a skill, create the plugin manifest and marketplace catalog, then install and test it.

Create the skill

Create a

```
SKILL.md
```

file that defines what the

```
/quality-review
```

skill does.

my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md

Create the plugin manifest

Create a

```
plugin.json
```

file that describes the plugin. The manifest goes in the

```
.claude-plugin/
```

directory.

my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json

Setting

```
version
```

means users only receive updates when you change this field, so bump it on every release. If you omit

```
version
```

and host this marketplace in git, every commit automatically counts as a new version. See [[Create and distribute a plugin marketplace - Claude Code Docs#Version resolution and release channels|Version resolution]]to choose the right approach.

Create the marketplace file

Create the marketplace catalog that lists your plugin.

my-marketplace/.claude-plugin/marketplace.json

[[Create plugins - Claude Code Docs|Plugins]].

How plugins are installed: When users install a plugin, Claude Code copies the plugin directory to a cache location. This means plugins can’t reference files outside their directory using paths like

```
../shared-utils
```

, because those files won’t be copied.If you need to share files across plugins, use symlinks. See [[Plugins reference - Claude Code Docs#Plugin caching and file resolution|Plugin caching and file resolution]]for details.

## Create the marketplace file

Create

```
.claude-plugin/marketplace.json
```

in your repository root. This file defines your marketplace’s name, owner information, and a list of plugins with their sources.
Each plugin entry needs at minimum a

```
name
```

and

```
source
```

(where to fetch it from). See the

[[Create and distribute a plugin marketplace - Claude Code Docs#Marketplace schema|full schema]]below for all available fields.

## Marketplace schema

### Required fields

FieldTypeDescriptionExample

```
name
```

stringMarketplace identifier (kebab-case, no spaces). This is public-facing: users see it when installing plugins (for example,

```
/plugin install my-tool@your-marketplace
```

).

```
"acme-tools"
```

```
owner
```

objectMarketplace maintainer information (

```
plugins
```

Reserved names: The following marketplace names are reserved for official Anthropic use and cannot be used by third-party marketplaces:

```
claude-code-marketplace
```

,

```
claude-code-plugins
```

,

```
claude-plugins-official
```

,

```
anthropic-marketplace
```

,

```
anthropic-plugins
```

,

```
agent-skills
```

,

```
knowledge-work-plugins
```

,

```
life-sciences
```

. Names that impersonate official marketplaces (like

```
official-claude-plugins
```

or

```
anthropic-tools-v2
```

) are also blocked.

### Owner fields

FieldTypeRequiredDescription

```
name
```

stringYesName of the maintainer or team

```
email
```

stringNoContact email for the maintainer

### Optional fields

FieldTypeDescription

```
metadata.description
```

stringBrief marketplace description

```
metadata.version
```

stringMarketplace version

```
metadata.pluginRoot
```

stringBase directory prepended to relative plugin source paths (for example,

```
"./plugins"
```

lets you write

```
"source": "formatter"
```

instead of

```
"source": "./plugins/formatter"
```

)

```
allowCrossMarketplaceDependenciesOn
```

arrayOther marketplaces that plugins in this marketplace may depend on. Dependencies from a marketplace not listed here are blocked at install. See

## Plugin entries

Each plugin entry in the

```
plugins
```

array describes a plugin and where to find it. You can include any field from the

[[Plugins reference - Claude Code Docs#Plugin manifest schema|plugin manifest schema]](like

```
description
```

,

```
version
```

,

```
author
```

,

```
commands
```

,

```
hooks
```

, etc.), plus these marketplace-specific fields:

```
source
```

,

```
category
```

,

```
tags
```

, and

```
strict
```

.

### Required fields

FieldTypeDescription

```
name
```

stringPlugin identifier (kebab-case, no spaces). This is public-facing: users see it when installing (for example,

```
/plugin install my-plugin@marketplace
```

).

```
source
```

string|objectWhere to fetch the plugin from (see

### Optional plugin fields

Standard metadata fields:

FieldTypeDescription

```
description
```

stringBrief plugin description

```
version
```

stringPlugin version. If set (here or in

```
plugin.json
```

), the plugin is pinned to this string and users only receive updates when it changes. Omit to fall back to the git commit SHA. See

```
author
```

objectPlugin author information (

```
name
```

required,

```
email
```

optional)

```
homepage
```

stringPlugin homepage or documentation URL

```
repository
```

stringSource code repository URL

```
license
```

stringSPDX license identifier (for example, MIT, Apache-2.0)

```
keywords
```

arrayTags for plugin discovery and categorization

```
category
```

stringPlugin category for organization

```
tags
```

arrayTags for searchability

```
strict
```

booleanControls whether

```
plugin.json
```

is the authority for component definitions (default: true). See

FieldTypeDescription

```
skills
```

string|arrayCustom paths to skill directories containing

```
<name>/SKILL.md
```

```
commands
```

string|arrayCustom paths to flat

```
.md
```

skill files or directories

```
agents
```

string|arrayCustom paths to agent files

```
hooks
```

string|objectCustom hooks configuration or path to hooks file

```
mcpServers
```

string|objectMCP server configurations or path to MCP config

```
lspServers
```

string|objectLSP server configurations or path to LSP config

## Plugin sources

Plugin sources tell Claude Code where to fetch each individual plugin listed in your marketplace. These are set in the

```
source
```

field of each plugin entry in

```
marketplace.json
```

.
Once a plugin is cloned or copied into the local machine, it is copied into the local versioned plugin cache at

```
~/.claude/plugins/cache
```

.

SourceTypeFieldsNotesRelative path

```
string
```

(e.g.

```
"./my-plugin"
```

)noneLocal directory within the marketplace repo. Must start with

```
./
```

. Resolved relative to the marketplace root, not the

```
.claude-plugin/
```

directory

```
github
```

object

```
repo
```

,

```
ref?
```

,

```
sha?
```

```
url
```

object

```
url
```

,

```
ref?
```

,

```
sha?
```

Git URL source

```
git-subdir
```

object

```
url
```

,

```
path
```

,

```
ref?
```

,

```
sha?
```

Subdirectory within a git repo. Clones sparsely to minimize bandwidth for monorepos

```
npm
```

object

```
package
```

,

```
version?
```

,

```
registry?
```

Installed via

```
npm install
```

Marketplace sources vs plugin sources: These are different concepts that control different things.

- Marketplace source — where to fetch the

  ```
  marketplace.json
  ```

  catalog itself. Set when users run

  ```
  /plugin marketplace add
  ```

  or in

  ```
  extraKnownMarketplaces
  ```

  settings. Supports

  ```
  ref
  ```

  (branch/tag) but not

  ```
  sha
  ```

  .
- Plugin source — where to fetch an individual plugin listed in the marketplace. Set in the

  ```
  source
  ```

  field of each plugin entry inside

  ```
  marketplace.json
  ```

  . Supports both

  ```
  ref
  ```

  (branch/tag) and

  ```
  sha
  ```

  (exact commit).

```
acme-corp/plugin-catalog
```

(marketplace source) can list a plugin fetched from

```
acme-corp/code-formatter
```

(plugin source). The marketplace source and plugin source point to different repositories and are pinned independently.

### Relative paths

For plugins in the same repository, use a path starting with

```
./
```

:

```
.claude-plugin/
```

. In the example above,

```
./plugins/my-plugin
```

points to

```
<repo>/plugins/my-plugin
```

, even though

```
marketplace.json
```

lives at

```
<repo>/.claude-plugin/marketplace.json
```

. Do not use

```
../
```

to reference paths outside the marketplace root.

Relative paths only work when users add your marketplace via Git (GitHub, GitLab, or git URL). If users add your marketplace via a direct URL to the

```
marketplace.json
```

file, relative paths will not resolve correctly. For URL-based distribution, use GitHub, npm, or git URL sources instead. See [[Create and distribute a plugin marketplace - Claude Code Docs#Plugins with relative paths fail in URL-based marketplaces|Troubleshooting]]for details.

### GitHub repositories

FieldTypeDescription

```
repo
```

stringRequired. GitHub repository in

```
owner/repo
```

format

```
ref
```

stringOptional. Git branch or tag (defaults to repository default branch)

```
sha
```

stringOptional. Full 40-character git commit SHA to pin to an exact version

### Git repositories

FieldTypeDescription

```
url
```

stringRequired. Full git repository URL (

```
https://
```

or

```
git@
```

). The

```
.git
```

suffix is optional, so Azure DevOps and AWS CodeCommit URLs without the suffix work

```
ref
```

stringOptional. Git branch or tag (defaults to repository default branch)

```
sha
```

stringOptional. Full 40-character git commit SHA to pin to an exact version

### Git subdirectories

Use

```
git-subdir
```

to point to a plugin that lives inside a subdirectory of a git repository. Claude Code uses a sparse, partial clone to fetch only the subdirectory, minimizing bandwidth for large monorepos.

```
url
```

field also accepts a GitHub shorthand (

```
owner/repo
```

) or SSH URLs (

```
git@github.com:owner/repo.git
```

).

FieldTypeDescription

```
url
```

stringRequired. Git repository URL, GitHub

```
owner/repo
```

shorthand, or SSH URL

```
path
```

stringRequired. Subdirectory path within the repo containing the plugin (for example,

```
"tools/claude-plugin"
```

)

```
ref
```

stringOptional. Git branch or tag (defaults to repository default branch)

```
sha
```

stringOptional. Full 40-character git commit SHA to pin to an exact version

### npm packages

Plugins distributed as npm packages are installed using

```
npm install
```

. This works with any package on the public npm registry or a private registry your team hosts.

```
version
```

field:

```
registry
```

field:

FieldTypeDescription

```
package
```

stringRequired. Package name or scoped package (for example,

```
@org/plugin
```

)

```
version
```

stringOptional. Version or version range (for example,

```
2.1.0
```

,

```
^2.0.0
```

,

```
~1.5.0
```

)

```
registry
```

stringOptional. Custom npm registry URL. Defaults to the system npm registry (typically npmjs.org)

### Advanced plugin entries

This example shows a plugin entry using many of the optional fields, including custom paths for commands, agents, hooks, and MCP servers:

- ```
  commands
  ```

  and

  ```
  agents
  ```

  : You can specify multiple directories or individual files. Paths are relative to the plugin root.
- ```
  ${CLAUDE_PLUGIN_ROOT}
  ```

  : use this variable in hooks and MCP server configs to reference files within the plugin’s installation directory. This is necessary because plugins are copied to a cache location when installed. For dependencies or state that should survive plugin updates, useinstead.

  ```
  ${CLAUDE_PLUGIN_DATA}
  ```
- ```
  strict: false
  ```

  : Since this is set to false, the plugin doesn’t need its own

  ```
  plugin.json
  ```

  . The marketplace entry defines everything. See[[Create and distribute a plugin marketplace - Claude Code Docs#Strict mode|Strict mode]]below.

### Strict mode

The

```
strict
```

field controls whether

```
plugin.json
```

is the authority for component definitions (skills, agents, hooks, MCP servers, output styles).

ValueBehavior

```
true
```

(default)

```
plugin.json
```

is the authority. The marketplace entry can supplement it with additional components, and both sources are merged.

```
false
```

The marketplace entry is the entire definition. If the plugin also has a

```
plugin.json
```

that declares components, that’s a conflict and the plugin fails to load.

- ```
  strict: true
  ```

  : the plugin has its own

  ```
  plugin.json
  ```

  and manages its own components. The marketplace entry can add extra skills or hooks on top. This is the default and works for most plugins.
- ```
  strict: false
  ```

  : the marketplace operator wants full control. The plugin repo provides raw files, and the marketplace entry defines which of those files are exposed as skills, agents, hooks, etc. Useful when the marketplace restructures or curates a plugin’s components differently than the plugin author intended.

## Host and distribute marketplaces

### Host on GitHub (recommended)

GitHub provides the easiest distribution method:

- Create a repository: Set up a new repository for your marketplace
- Add marketplace file: Create

  ```
  .claude-plugin/marketplace.json
  ```

  with your plugin definitions
- Share with teams: Users add your marketplace with

  ```
  /plugin marketplace add owner/repo
  ```

### Host on other git services

Any git hosting service works, such as GitLab, Bitbucket, and self-hosted servers. Users add with the full repository URL:

### Private repositories

Claude Code supports installing plugins from private repositories. For manual installation and updates, Claude Code uses your existing git credential helpers, so HTTPS access via

```
gh auth login
```

, macOS Keychain, or

```
git-credential-store
```

works the same as in your terminal. SSH access works as long as the host is already in your

```
known_hosts
```

file and the key is loaded in

```
ssh-agent
```

, since Claude Code suppresses interactive SSH prompts for the host fingerprint and key passphrase.
Background auto-updates run at startup without credential helpers, since interactive prompts would block Claude Code from starting. To enable auto-updates for private marketplaces, set the appropriate authentication token in your environment:

ProviderEnvironment variablesNotesGitHub

```
GITHUB_TOKEN
```

or

```
GH_TOKEN
```

Personal access token or GitHub App tokenGitLab

```
GITLAB_TOKEN
```

or

```
GL_TOKEN
```

Personal access token or project tokenBitbucket

```
BITBUCKET_TOKEN
```

App password or repository access token

```
.bashrc
```

,

```
.zshrc
```

) or pass it when running Claude Code:

For CI/CD environments, configure the token as a secret environment variable. GitHub Actions automatically provides

```
GITHUB_TOKEN
```

for repositories in the same organization.

### Test locally before distribution

Test your marketplace locally before sharing:

[[Discover and install prebuilt plugins through marketplaces - Claude Code Docs#Add marketplaces|Add marketplaces]].

### Require marketplaces for your team

You can configure your repository so team members are automatically prompted to install your marketplace when they trust the project folder. Add your marketplace to

```
.claude/settings.json
```

:

[[Claude Code settings - Claude Code Docs#Plugin settings|Plugin settings]].

If you use a local

```
directory
```

or

```
file
```

source with a relative path, the path resolves against your repository’s main checkout. When you run Claude Code from a git worktree, the path still points at the main checkout, so all worktrees share the same marketplace location. Marketplace state is stored once per user in

```
~/.claude/plugins/known_marketplaces.json
```

, not per project.

### Pre-populate plugins for containers

For container images and CI environments, you can pre-populate a plugins directory at build time so Claude Code starts with marketplaces and plugins already available, without cloning anything at runtime. Set the

```
CLAUDE_CODE_PLUGIN_SEED_DIR
```

environment variable to point at this directory.
To layer multiple seed directories, separate paths with

```
:
```

on Unix or

```
;
```

on Windows. Claude Code searches each directory in order, and the first seed that contains a given marketplace or plugin cache wins.
The seed directory mirrors the structure of

```
~/.claude/plugins
```

:

```
~/.claude/plugins
```

directory into your image and point

```
CLAUDE_CODE_PLUGIN_SEED_DIR
```

at it.
To skip the copy step, set

```
CLAUDE_CODE_PLUGIN_CACHE_DIR
```

to your target seed path during the build so plugins install directly there:

```
CLAUDE_CODE_PLUGIN_SEED_DIR=/opt/claude-seed
```

in your container’s runtime environment so Claude Code reads from the seed on startup.
At startup, Claude Code registers marketplaces found in the seed’s

```
known_marketplaces.json
```

into the primary configuration, and uses plugin caches found under

```
cache/
```

in place without re-cloning. This works in both interactive mode and non-interactive mode with the

```
-p
```

flag.
Behavior details:

- Read-only: the seed directory is never written to. Auto-updates are disabled for seed marketplaces since git pull would fail on a read-only filesystem.
- Seed entries take precedence: marketplaces declared in the seed overwrite any matching entries in the user’s configuration on each startup. To opt out of a seed plugin, use

  ```
  /plugin disable
  ```

  rather than removing the marketplace.
- Path resolution: Claude Code locates marketplace content by probing

  ```
  $CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/
  ```

  at runtime, not by trusting paths stored inside the seed’s JSON. This means the seed works correctly even when mounted at a different path than where it was built.
- Mutation is blocked: running

  ```
  /plugin marketplace remove
  ```

  or

  ```
  /plugin marketplace update
  ```

  against a seed-managed marketplace fails with guidance to ask your administrator to update the seed image.
- Composes with settings: if

  ```
  extraKnownMarketplaces
  ```

  or

  ```
  enabledPlugins
  ```

  declare a marketplace that already exists in the seed, Claude Code uses the seed copy instead of cloning.

### Managed marketplace restrictions

For organizations requiring strict control over plugin sources, administrators can restrict which plugin marketplaces users are allowed to add using the

[[Claude Code settings - Claude Code Docs#strictKnownMarketplaces|setting in managed settings. When]]

```
strictKnownMarketplaces
```

```
strictKnownMarketplaces
```

is configured in managed settings, the restriction behavior depends on the value:

ValueBehaviorUndefined (default)No restrictions. Users can add any marketplaceEmpty array

```
[]
```

Complete lockdown. Users cannot add any new marketplacesList of sourcesUsers can only add marketplaces that match the allowlist exactly

#### Common configurations

Disable all marketplace additions:

[[Claude Code with GitHub Enterprise Server - Claude Code Docs#Plugin marketplaces on GHES|GitHub Enterprise Server]]or self-hosted GitLab instances:

```
".*"
```

as the

```
pathPattern
```

to allow any filesystem path while still controlling network sources with

```
hostPattern
```

.

```
strictKnownMarketplaces
```

restricts what users can add, but does not register marketplaces on its own. To make allowed marketplaces available automatically without users running

```
/plugin marketplace add
```

, pair it with

[[Claude Code settings - Claude Code Docs#extraKnownMarketplaces|in the same]]

```
extraKnownMarketplaces
```

```
managed-settings.json
```

. See

[[Claude Code settings - Claude Code Docs#strictKnownMarketplaces|Using both together]].

#### How restrictions work

Restrictions are checked before any network or filesystem operation. The check runs on marketplace add and on plugin install, update, refresh, and auto-update. If a marketplace was added before the policy was configured and its source no longer matches the allowlist, Claude Code refuses to install or update plugins from it. The same enforcement applies to

```
blockedMarketplaces
```

.
The allowlist uses exact matching for most source types. For a marketplace to be allowed, all specified fields must match exactly:

- For GitHub sources:

  ```
  repo
  ```

  is required, and

  ```
  ref
  ```

  or

  ```
  path
  ```

  must also match if specified in the allowlist
- For URL sources: the full URL must match exactly
- For

  ```
  hostPattern
  ```

  sources: the marketplace host is matched against the regex pattern
- For

  ```
  pathPattern
  ```

  sources: the marketplace’s filesystem path is matched against the regex pattern

```
strictKnownMarketplaces
```

is set in

[[Claude Code settings - Claude Code Docs#Settings files|managed settings]], individual users and project configurations cannot override these restrictions. For complete configuration details including all supported source types and comparison with

```
extraKnownMarketplaces
```

, see the

[[Claude Code settings - Claude Code Docs#strictKnownMarketplaces|strictKnownMarketplaces reference]].

### Version resolution and release channels

Plugin versions determine cache paths and update detection: if the resolved version matches what a user already has,

```
/plugin update
```

and auto-update skip the plugin.
Claude Code resolves a plugin’s version from the first of these that is set:

- ```
  version
  ```

  in the plugin’s

  ```
  plugin.json
  ```
- ```
  version
  ```

  in the plugin’s marketplace entry
- The git commit SHA of the plugin’s source

```
github
```

,

```
url
```

,

```
git-subdir
```

, and relative paths inside a git-hosted marketplace, you can omit

```
version
```

entirely and every new commit is treated as a new version. This is the simplest setup for internal or actively-developed plugins.

#### Set up release channels

To support “stable” and “latest” release channels for your plugins, you can set up two marketplaces that point to different refs or SHAs of the same repo. You can then assign the two marketplaces to different user groups through

[[Claude Code settings - Claude Code Docs#Settings files|managed settings]].

##### Example

##### Assign channels to user groups

Assign each marketplace to the appropriate user group through managed settings. For example, the stable group receives:

```
latest-tools
```

instead:

#### Pin dependency versions

A plugin can constrain its dependencies to a semver range so that updates to a dependency do not break the dependent plugin. See

[[Constrain plugin dependency versions - Claude Code Docs|Constrain plugin dependency versions]]for the

```
{plugin-name}--v{version}
```

git-tag convention, range syntax, and how multiple constraints on the same dependency are combined.

## Validation and testing

Test your marketplace before sharing. Validate your marketplace JSON syntax:

[[Create plugins - Claude Code Docs#Test your plugins locally|Test your plugins locally]]. For technical troubleshooting, see

[[Plugins reference - Claude Code Docs|Plugins reference]].

## Manage marketplaces from the CLI

Claude Code provides non-interactive

```
claude plugin marketplace
```

subcommands for scripting and automation. These are equivalent to the

```
/plugin marketplace
```

commands available inside an interactive session.

### Plugin marketplace add

Add a marketplace from a GitHub repository, git URL, remote URL, or local path.

- ```
  <source>
  ```

  : GitHub

  ```
  owner/repo
  ```

  shorthand, git URL, remote URL to a

  ```
  marketplace.json
  ```

  file, or local directory path. To pin to a branch or tag, append

  ```
  @ref
  ```

  to the GitHub shorthand or

  ```
  #ref
  ```

  to a git URL

OptionDescriptionDefault

```
--scope <scope>
```

Where to declare the marketplace:

```
user
```

,

```
project
```

, or

```
local
```

. See

```
user
```

```
--sparse <paths...>
```

Limit checkout to specific directories via git sparse-checkout. Useful for monorepos

```
owner/repo
```

shorthand:

```
@ref
```

:

```
marketplace.json
```

file directly:

```
.claude/settings.json
```

:

### Plugin marketplace list

List all configured marketplaces.

OptionDescription

```
--json
```

Output as JSON

### Plugin marketplace remove

Remove a configured marketplace. The alias

```
rm
```

is also accepted.

- ```
  <name>
  ```

  : marketplace name to remove, as shown by

  ```
  claude plugin marketplace list
  ```

  . This is the

  ```
  name
  ```

  from

  ```
  marketplace.json
  ```

  , not the source you passed to

  ```
  add
  ```

### Plugin marketplace update

Refresh marketplaces from their sources to retrieve new plugins and version changes.

- ```
  [name]
  ```

  : marketplace name to update, as shown by

  ```
  claude plugin marketplace list
  ```

  . Updates all marketplaces if omitted

```
remove
```

and

```
update
```

fail when run against a seed-managed marketplace, which is read-only. When updating all marketplaces, seed-managed entries are skipped and other marketplaces still update. To change seed-provided plugins, ask your administrator to update the seed image. See

[[Create and distribute a plugin marketplace - Claude Code Docs#Pre-populate plugins for containers|Pre-populate plugins for containers]].

## Troubleshooting

### Marketplace not loading

Symptoms: Can’t add marketplace or see plugins from it Solutions:

- Verify the marketplace URL is accessible
- Check that

  ```
  .claude-plugin/marketplace.json
  ```

  exists at the specified path
- Ensure JSON syntax is valid and frontmatter is well-formed using

  ```
  claude plugin validate
  ```

  or

  ```
  /plugin validate
  ```
- For private repositories, confirm you have access permissions

### Marketplace validation errors

Run

```
claude plugin validate .
```

or

```
/plugin validate .
```

from your marketplace directory to check for issues. The validator checks

```
plugin.json
```

, skill/agent/command frontmatter, and

```
hooks/hooks.json
```

for syntax and schema errors. Common errors:

ErrorCauseSolution

```
File not found: .claude-plugin/marketplace.json
```

Missing manifestCreate

```
.claude-plugin/marketplace.json
```

with required fields

```
Invalid JSON syntax: Unexpected token...
```

JSON syntax error in marketplace.jsonCheck for missing commas, extra commas, or unquoted strings

```
Duplicate plugin name "x" found in marketplace
```

Two plugins share the same nameGive each plugin a unique

```
name
```

value

```
plugins[0].source: Path contains ".."
```

Source path contains

```
..
```

Use paths relative to the marketplace root without

```
..
```

. See

```
YAML frontmatter failed to parse: ...
```

Invalid YAML in a skill, agent, or command fileFix the YAML syntax in the frontmatter block. At runtime this file loads with no metadata.

```
Invalid JSON syntax: ...
```

(hooks.json)Malformed

```
hooks/hooks.json
```

Fix JSON syntax. A malformed

```
hooks/hooks.json
```

prevents the entire plugin from loading.

- ```
  Marketplace has no plugins defined
  ```

  : add at least one plugin to the

  ```
  plugins
  ```

  array
- ```
  No marketplace description provided
  ```

  : add

  ```
  metadata.description
  ```

  to help users understand your marketplace
- ```
  Plugin name "x" is not kebab-case
  ```

  : the plugin name contains uppercase letters, spaces, or special characters. Rename to lowercase letters, digits, and hyphens only (for example,

  ```
  my-plugin
  ```

  ). Claude Code accepts other forms, but the Claude.ai marketplace sync rejects them.

### Plugin installation failures

Symptoms: Marketplace appears but plugin installation fails Solutions:

- Verify plugin source URLs are accessible
- Check that plugin directories contain required files
- For GitHub sources, ensure repositories are public or you have access
- Test plugin sources manually by cloning/downloading

### Private repository authentication fails

Symptoms: Authentication errors when installing plugins from private repositories Solutions: For manual installation and updates:

- Verify you’re authenticated with your git provider (for example, run

  ```
  gh auth status
  ```

  for GitHub)
- Check that your credential helper is configured correctly:

  ```
  git config --global credential.helper
  ```
- Try cloning the repository manually to verify your credentials work

- Set the appropriate token in your environment:

  ```
  echo $GITHUB_TOKEN
  ```
- Check that the token has the required permissions (read access to the repository)
- For GitHub, ensure the token has the

  ```
  repo
  ```

  scope for private repositories
- For GitLab, ensure the token has at least

  ```
  read_repository
  ```

  scope
- Verify the token hasn’t expired

### Marketplace updates fail in offline environments

Symptoms: Marketplace

```
git pull
```

fails and Claude Code wipes the existing cache, causing plugins to become unavailable.
Cause: By default, when a

```
git pull
```

fails, Claude Code removes the stale clone and attempts to re-clone. In offline or airgapped environments, re-cloning fails the same way, leaving the marketplace directory empty.
Solution: Set

```
CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1
```

to keep the existing cache when the pull fails instead of wiping it:

```
git pull
```

failure and continues using the last-known-good state. For fully offline deployments where the repository will never be reachable, use

[[Create and distribute a plugin marketplace - Claude Code Docs#Pre-populate plugins for containers|to pre-populate the plugins directory at build time instead.]]

```
CLAUDE_CODE_PLUGIN_SEED_DIR
```

### Git operations time out

Symptoms: Plugin installation or marketplace updates fail with a timeout error like “Git clone timed out after 120s” or “Git pull timed out after 120s”. Cause: Claude Code uses a 120-second timeout for all git operations, including cloning plugin repositories and pulling marketplace updates. Large repositories or slow network connections may exceed this limit. Solution: Increase the timeout using the

```
CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS
```

environment variable. The value is in milliseconds:

### Plugins with relative paths fail in URL-based marketplaces

Symptoms: Added a marketplace via URL (such as

```
https://example.com/marketplace.json
```

), but plugins with relative path sources like

```
"./plugins/my-plugin"
```

fail to install with “path not found” errors.
Cause: URL-based marketplaces only download the

```
marketplace.json
```

file itself. They do not download plugin files from the server. Relative paths in the marketplace entry reference files on the remote server that were not downloaded.
Solutions:

- Use external sources: Change plugin entries to use GitHub, npm, or git URL sources instead of relative paths:
- Use a Git-based marketplace: Host your marketplace in a Git repository and add it with the git URL. Git-based marketplaces clone the entire repository, making relative paths work correctly.

### Files not found after installation

Symptoms: Plugin installs but references to files fail, especially files outside the plugin directory Cause: Plugins are copied to a cache directory rather than used in-place. Paths that reference files outside the plugin’s directory (such as

```
../shared-utils
```

) won’t work because those files aren’t copied.
Solutions: See

[[Plugins reference - Claude Code Docs#Plugin caching and file resolution|Plugin caching and file resolution]]for workarounds including symlinks and directory restructuring. For additional debugging tools and common issues, see

[[Plugins reference - Claude Code Docs#Debugging and development tools|Debugging and development tools]].

## See also

- [[Discover and install prebuilt plugins through marketplaces - Claude Code Docs|Discover and install prebuilt plugins]]- Installing plugins from existing marketplaces
- [[Create plugins - Claude Code Docs|Plugins]]- Creating your own plugins
- [[Plugins reference - Claude Code Docs|Plugins reference]]- Complete technical specifications and schemas
- [[Claude Code settings - Claude Code Docs#Plugin settings|Plugin settings]]- Plugin configuration options
- [[Claude Code settings - Claude Code Docs#strictKnownMarketplaces|strictKnownMarketplaces reference]]- Managed marketplace restrictions

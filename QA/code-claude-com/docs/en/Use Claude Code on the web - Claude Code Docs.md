---
title: Use Claude Code on the web - Claude Code Docs
source_url: https://code.claude.com/docs/en/claude-code-on-the-web
description: Configure cloud environments, setup scripts, network access, and Docker
  in Anthropic's sandbox. Move sessions between web and terminal with --remote and
  --telep
---

Claude Code on the web is in research preview for Pro, Max, and Team users, and for Enterprise users with premium seats or Chat + Claude Code seats.

[claude.ai/code](https://claude.ai/code). Sessions persist even if you close your browser, and you can monitor them from the Claude mobile app. This page covers:

- [[Use Claude Code on the web - Claude Code Docs#GitHub authentication options|GitHub authentication options]]: two ways to connect GitHub
- [[Use Claude Code on the web - Claude Code Docs#The cloud environment|The cloud environment]]: what config carries over, what tools are installed, and how to configure environments
- [[Use Claude Code on the web - Claude Code Docs#Setup scripts|Setup scripts]]and dependency management
- [[Use Claude Code on the web - Claude Code Docs#Network access|Network access]]: levels, proxies, and the default allowlist
- [[Use Claude Code on the web - Claude Code Docs#Move tasks between web and terminal|Move tasks between web and terminal]]with

  ```
  --remote
  ```

  and

  ```
  --teleport
  ```
- [[Use Claude Code on the web - Claude Code Docs#Work with sessions|Work with sessions]]: reviewing, sharing, archiving, deleting
- [[Use Claude Code on the web - Claude Code Docs#Auto-fix pull requests|Auto-fix pull requests]]: respond automatically to CI failures and review comments
- [[Use Claude Code on the web - Claude Code Docs#Security and isolation|Security and isolation]]: how sessions are isolated
- [[Use Claude Code on the web - Claude Code Docs#Limitations|Limitations]]: rate limits and platform restrictions

## GitHub authentication options

Cloud sessions need access to your GitHub repositories to clone code and push branches. You can grant access in two ways:

MethodHow it worksBest forGitHub AppInstall the Claude GitHub App on specific repositories during

```
/web-setup
```

```
/web-setup
```

in your terminal to sync your local

```
gh
```

CLI token to your Claude account. Access matches whatever your

```
gh
```

token can see.

```
gh
```

[[Automate work with routines - Claude Code Docs|checks for either form of access and prompts you to run]]

```
/schedule
```

```
/web-setup
```

if neither is configured. See

[[Get started with Claude Code on the web - Claude Code Docs#Connect from your terminal|Connect from your terminal]]for the

```
/web-setup
```

walkthrough.
The GitHub App is required for

[[Use Claude Code on the web - Claude Code Docs#Auto-fix pull requests|Auto-fix]], which uses the App to receive PR webhooks. If you connect with

```
/web-setup
```

and later want Auto-fix, install the App on those repositories.
Team and Enterprise admins can disable

```
/web-setup
```

with the Quick web setup toggle at

[claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).

Organizations with

[[Zero data retention - Claude Code Docs|Zero Data Retention]]enabled cannot use

```
/web-setup
```

or other cloud session features.

## The cloud environment

Each session runs in a fresh Anthropic-managed VM with your repository cloned. This section covers what’s available when a session starts and how to customize it.

### What’s available in cloud sessions

Cloud sessions start from a fresh clone of your repository. Anything committed to the repo is available. Anything you’ve installed or configured only on your own machine is not.

Available in cloud sessionsWhyYour repo’s

```
CLAUDE.md
```

YesPart of the cloneYour repo’s

```
.claude/settings.json
```

hooksYesPart of the cloneYour repo’s

```
.mcp.json
```

MCP serversYesPart of the cloneYour repo’s

```
.claude/rules/
```

YesPart of the cloneYour repo’s

```
.claude/skills/
```

,

```
.claude/agents/
```

,

```
.claude/commands/
```

YesPart of the clonePlugins declared in

```
.claude/settings.json
```

YesInstalled at session start from the

```
~/.claude/CLAUDE.md
```

```
enabledPlugins
```

lives in

```
~/.claude/settings.json
```

. Declare them in the repo’s

```
.claude/settings.json
```

instead

```
claude mcp add
```

[[Connect Claude Code to tools via MCP - Claude Code Docs#Project scope|instead]]

```
.mcp.json
```

### Installed tools

Cloud sessions come with common language runtimes, build tools, and databases pre-installed. The table below summarizes what’s included by category.

CategoryIncludedPythonPython 3.x with pip, poetry, uv, black, mypy, pytest, ruffNode.js20, 21, and 22 via nvm, with npm, yarn, pnpm, bun¹, eslint, prettier, chromedriverRuby3.1, 3.2, 3.3 with gem, bundler, rbenvPHP8.4 with ComposerJavaOpenJDK 21 with Maven and GradleGolatest stable with module supportRustrustc and cargoC/C++GCC, Clang, cmake, ninja, conanDockerdocker, dockerd, docker composeDatabasesPostgreSQL 16, Redis 7.0Utilitiesgit, jq, yq, ripgrep, tmux, vim, nano

[[Use Claude Code on the web - Claude Code Docs#Install dependencies with a SessionStart hook|proxy compatibility issues]]for package fetching. For exact versions, ask Claude to run

```
check-tools
```

in a cloud session. This command only exists in cloud sessions.

### Work with GitHub issues and pull requests

Cloud sessions include built-in GitHub tools that let Claude read issues, list pull requests, fetch diffs, and post comments without any setup. These tools authenticate through the

[[Use Claude Code on the web - Claude Code Docs#GitHub proxy|GitHub proxy]]using whichever method you configured under

[[Use Claude Code on the web - Claude Code Docs#GitHub authentication options|GitHub authentication options]], so your token never enters the container. The

```
gh
```

CLI is not pre-installed. If you need a

```
gh
```

command the built-in tools don’t cover, like

```
gh release
```

or

```
gh workflow run
```

, install and authenticate it yourself:

Install gh in your setup script

Add

```
apt update && apt install -y gh
```

to your [[Use Claude Code on the web - Claude Code Docs#Setup scripts|setup script]].

Provide a token

Add a

```
GH_TOKEN
```

environment variable to your [[Use Claude Code on the web - Claude Code Docs#Configure your environment|environment settings]]with a GitHub personal access token.

```
gh
```

reads

```
GH_TOKEN
```

automatically, so no

```
gh auth login
```

step is needed.

### Link artifacts back to the session

Each cloud session has a transcript URL on claude.ai, and the session can read its own ID from the

```
CLAUDE_CODE_REMOTE_SESSION_ID
```

environment variable. Use this to put a traceable link in PR bodies, commit messages, Slack posts, or generated reports so a reviewer can open the run that produced them.
Ask Claude to construct the link from the environment variable. The following command prints the URL:

### Run tests, start services, and add packages

Claude runs tests as part of working on a task. Ask for it in your prompt, like “fix the failing tests in

```
tests/
```

” or “run pytest after each change.” Test runners like pytest, jest, and cargo test work out of the box since they’re pre-installed.
PostgreSQL and Redis are pre-installed but not running by default. Ask Claude to start each one during the session:

```
docker compose up
```

to start your project’s services. Network access to pull images follows your environment’s

[[Use Claude Code on the web - Claude Code Docs#Access levels|access level]], and the

[[Use Claude Code on the web - Claude Code Docs#Default allowed domains|Trusted defaults]]include Docker Hub and other common registries. If your images are large or slow to pull, add

```
docker compose pull
```

or

```
docker compose build
```

to your

[[Use Claude Code on the web - Claude Code Docs#Setup scripts|setup script]]. The pulled images are saved in the

[[Use Claude Code on the web - Claude Code Docs#Environment caching|cached environment]], so each new session has them on disk. The cache stores files only, not running processes, so Claude still starts the containers each session. To add packages that aren’t pre-installed, use a

[[Use Claude Code on the web - Claude Code Docs#Setup scripts|setup script]]. The script’s output is

[[Use Claude Code on the web - Claude Code Docs#Environment caching|cached]], so packages you install there are available at the start of every session without reinstalling each time. You can also ask Claude to install packages mid-session, but those installs don’t carry over to other sessions.

### Resource limits

Cloud sessions run with approximate resource ceilings that may change over time:

- 4 vCPUs
- 16 GB of RAM
- 30 GB of disk

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]to run Claude Code on your own hardware.

### Configure your environment

Environments control

[[Use Claude Code on the web - Claude Code Docs#Network access|network access]], environment variables, and the

[[Use Claude Code on the web - Claude Code Docs#Setup scripts|setup script]]that runs before a session starts. See

[[Use Claude Code on the web - Claude Code Docs#Installed tools|Installed tools]]for what’s available without any configuration. You can manage environments from the web interface or the terminal:

ActionHowAdd an environmentSelect the current environment to open the selector, then select Add environment. The dialog includes name, network access level, environment variables, and setup script.Edit an environmentSelect the settings icon to the right of the environment name.Archive an environmentOpen the environment for editing and select Archive. Archived environments are hidden from the selector but existing sessions keep running.Set the default for

```
--remote
```

Run

```
/remote-env
```

in your terminal. If you have a single environment, this command shows your current configuration.

```
/remote-env
```

only selects the default; add, edit, and archive environments from the web interface.

```
.env
```

format with one

```
KEY=value
```

pair per line. Don’t wrap values in quotes, since quotes are stored as part of the value.

## Setup scripts

A setup script is a Bash script that runs when a new cloud session starts, before Claude Code launches. Use setup scripts to install dependencies, configure tools, or fetch anything the session needs that isn’t pre-installed. Scripts run as root on Ubuntu 24.04, so

```
apt install
```

and most language package managers work.
To add a setup script, open the environment settings dialog and enter your script in the Setup script field.
This example installs the

```
gh
```

CLI, which isn’t pre-installed:

```
|| true
```

to non-critical commands to avoid blocking the session on an intermittent install failure.

Setup scripts that install packages need network access to reach registries. The default Trusted network access allows connections to

[[Use Claude Code on the web - Claude Code Docs#Default allowed domains|common package registries]]including npm, PyPI, RubyGems, and crates.io. Scripts will fail to install packages if your environment uses None network access.

### Environment caching

The setup script runs the first time you start a session in an environment. After it completes, Anthropic snapshots the filesystem and reuses that snapshot as the starting point for later sessions. New sessions start with your dependencies, tools, and Docker images already on disk, and the setup script step is skipped. This keeps startup fast even when the script installs large toolchains or pulls container images. The cache captures files, not running processes. Anything the setup script writes to disk carries over. Services or containers it starts do not, so start those per session by asking Claude or with a

[[Use Claude Code on the web - Claude Code Docs#Setup scripts vs. SessionStart hooks|SessionStart hook]]. The setup script runs again to rebuild the cache when you change the environment’s setup script or allowed network hosts, and when the cache reaches its expiry after roughly seven days. Resuming an existing session never re-runs the setup script. You don’t need to enable caching or manage snapshots yourself.

### Setup scripts vs. SessionStart hooks

Use a setup script to install things the cloud needs but your laptop already has, like a language runtime or CLI tool. Use a

[[Hooks reference - Claude Code Docs#SessionStart|SessionStart hook]]for project setup that should run everywhere, cloud and local, like

```
npm install
```

.
Both run at the start of a session, but they belong to different places:

Setup scriptsSessionStart hooksAttached toThe cloud environmentYour repositoryConfigured inCloud environment UI

```
.claude/settings.json
```

in your repoRunsBefore Claude Code launches, when no

```
~/.claude/settings.json
```

locally, but user-level settings don’t carry over to cloud sessions. In the cloud, only hooks committed to the repo run.

### Install dependencies with a SessionStart hook

To install dependencies only in cloud sessions, add a SessionStart hook to your repo’s

```
.claude/settings.json
```

:

```
scripts/install_pkgs.sh
```

and make it executable with

```
chmod +x
```

. The

```
CLAUDE_CODE_REMOTE
```

environment variable is set to

```
true
```

in cloud sessions, so you can use it to skip local execution:

- No cloud-only scoping: hooks run in both local and cloud sessions. To skip local execution, check the

  ```
  CLAUDE_CODE_REMOTE
  ```

  environment variable as shown above.
- Requires network access: install commands need to reach package registries. If your environment uses None network access, these hooks fail. The [[Use Claude Code on the web - Claude Code Docs#Default allowed domains|default allowlist]]under Trusted covers npm, PyPI, RubyGems, and crates.io.
- Proxy compatibility: all outbound traffic passes through a [[Use Claude Code on the web - Claude Code Docs#Security proxy|security proxy]]. Some package managers don’t work correctly with this proxy. Bun is a known example.
- Adds startup latency: hooks run each time a session starts or resumes, unlike setup scripts which benefit from [[Use Claude Code on the web - Claude Code Docs#Environment caching|environment caching]]. Keep install scripts fast by checking whether dependencies are already present before reinstalling.

```
$CLAUDE_ENV_FILE
```

. See

[[Hooks reference - Claude Code Docs#SessionStart|SessionStart hooks]]for details. Replacing the base image with your own Docker image is not yet supported. Use a setup script to install what you need on top of the

[[Use Claude Code on the web - Claude Code Docs#Installed tools|provided image]], or run your image as a container alongside Claude with

```
docker compose
```

.

## Network access

Network access controls outbound connections from the cloud environment. Each environment specifies one access level, and you can extend it with custom allowed domains. The default is Trusted, which allows package registries and other

[[Use Claude Code on the web - Claude Code Docs#Default allowed domains|allowlisted domains]].

### Access levels

Choose an access level when you create or edit an environment:

LevelOutbound connectionsNoneNo outbound network accessTrusted

[[Use Claude Code on the web - Claude Code Docs#GitHub proxy|separate proxy]]that is independent of this setting.

### Allow specific domains

To allow domains that aren’t in the Trusted list, select Custom in the environment’s network access settings. An Allowed domains field appears. Enter one domain per line:

```
*.
```

for wildcard subdomain matching. Check Also include default list of common package managers to keep the

[[Use Claude Code on the web - Claude Code Docs#Default allowed domains|Trusted domains]]alongside your custom entries, or leave it unchecked to allow only what you list.

### GitHub proxy

For security, all GitHub operations go through a dedicated proxy service that transparently handles all git interactions. Inside the sandbox, the git client authenticates using a custom-built scoped credential. This proxy:

- Manages GitHub authentication securely: the git client uses a scoped credential inside the sandbox, which the proxy verifies and translates to your actual GitHub authentication token
- Restricts git push operations to the current working branch for safety
- Enables cloning, fetching, and PR operations while maintaining security boundaries

### Security proxy

Environments run behind an HTTP/HTTPS network proxy for security and abuse prevention purposes. All outbound internet traffic passes through this proxy, which provides:

- Protection against malicious requests
- Rate limiting and abuse prevention
- Content filtering for enhanced security

### Default allowed domains

When using Trusted network access, the following domains are allowed by default. Domains marked with

```
*
```

indicate wildcard subdomain matching, so

```
*.gcr.io
```

allows any subdomain of

```
gcr.io
```

.

###

Anthropic services

Anthropic services

- api.anthropic.com
- statsig.anthropic.com
- docs.claude.com
- platform.claude.com
- code.claude.com
- claude.ai

###

Version control

Version control

- github.com
- [www.github.com](http://www.github.com)
- api.github.com
- npm.pkg.github.com
- raw.githubusercontent.com
- pkg-npm.githubusercontent.com
- objects.githubusercontent.com
- release-assets.githubusercontent.com
- codeload.github.com
- avatars.githubusercontent.com
- camo.githubusercontent.com
- gist.github.com
- gitlab.com
- [www.gitlab.com](http://www.gitlab.com)
- registry.gitlab.com
- bitbucket.org
- [www.bitbucket.org](http://www.bitbucket.org)
- api.bitbucket.org

###

Container registries

Container registries

- registry-1.docker.io
- auth.docker.io
- index.docker.io
- hub.docker.com
- [www.docker.com](http://www.docker.com)
- production.cloudflare.docker.com
- download.docker.com
- gcr.io
- \*.gcr.io
- ghcr.io
- mcr.microsoft.com
- \*.data.mcr.microsoft.com
- public.ecr.aws

###

Cloud platforms

Cloud platforms

- cloud.google.com
- accounts.google.com
- gcloud.google.com
- \*.googleapis.com
- storage.googleapis.com
- compute.googleapis.com
- container.googleapis.com
- azure.com
- portal.azure.com
- microsoft.com
- [www.microsoft.com](http://www.microsoft.com)
- \*.microsoftonline.com
- packages.microsoft.com
- dotnet.microsoft.com
- dot.net
- visualstudio.com
- dev.azure.com
- \*.amazonaws.com
- \*.api.aws
- oracle.com
- [www.oracle.com](http://www.oracle.com)
- java.com
- [www.java.com](http://www.java.com)
- java.net
- [www.java.net](http://www.java.net)
- download.oracle.com
- yum.oracle.com

###

JavaScript and Node package managers

JavaScript and Node package managers

- registry.npmjs.org
- [www.npmjs.com](http://www.npmjs.com)
- [www.npmjs.org](http://www.npmjs.org)
- npmjs.com
- npmjs.org
- yarnpkg.com
- registry.yarnpkg.com

###

Python package managers

Python package managers

- pypi.org
- [www.pypi.org](http://www.pypi.org)
- files.pythonhosted.org
- pythonhosted.org
- test.pypi.org
- pypi.python.org
- pypa.io
- [www.pypa.io](http://www.pypa.io)

###

Ruby package managers

Ruby package managers

- rubygems.org
- [www.rubygems.org](http://www.rubygems.org)
- api.rubygems.org
- index.rubygems.org
- ruby-lang.org
- [www.ruby-lang.org](http://www.ruby-lang.org)
- rubyforge.org
- [www.rubyforge.org](http://www.rubyforge.org)
- rubyonrails.org
- [www.rubyonrails.org](http://www.rubyonrails.org)
- rvm.io
- get.rvm.io

###

Rust package managers

Rust package managers

- crates.io
- [www.crates.io](http://www.crates.io)
- index.crates.io
- static.crates.io
- rustup.rs
- static.rust-lang.org
- [www.rust-lang.org](http://www.rust-lang.org)

###

Go package managers

Go package managers

- proxy.golang.org
- sum.golang.org
- index.golang.org
- golang.org
- [www.golang.org](http://www.golang.org)
- goproxy.io
- pkg.go.dev

###

JVM package managers

JVM package managers

- maven.org
- repo.maven.org
- central.maven.org
- repo1.maven.org
- repo.maven.apache.org
- jcenter.bintray.com
- gradle.org
- [www.gradle.org](http://www.gradle.org)
- services.gradle.org
- plugins.gradle.org
- kotlinlang.org
- [www.kotlinlang.org](http://www.kotlinlang.org)
- spring.io
- repo.spring.io

###

Other package managers

Other package managers

- packagist.org (PHP Composer)
- [www.packagist.org](http://www.packagist.org)
- repo.packagist.org
- nuget.org (.NET NuGet)
- [www.nuget.org](http://www.nuget.org)
- api.nuget.org
- pub.dev (Dart/Flutter)
- api.pub.dev
- hex.pm (Elixir/Erlang)
- [www.hex.pm](http://www.hex.pm)
- cpan.org (Perl CPAN)
- [www.cpan.org](http://www.cpan.org)
- metacpan.org
- [www.metacpan.org](http://www.metacpan.org)
- api.metacpan.org
- cocoapods.org (iOS/macOS)
- [www.cocoapods.org](http://www.cocoapods.org)
- cdn.cocoapods.org
- haskell.org
- [www.haskell.org](http://www.haskell.org)
- hackage.haskell.org
- swift.org
- [www.swift.org](http://www.swift.org)

###

Linux distributions

Linux distributions

- archive.ubuntu.com
- security.ubuntu.com
- ubuntu.com
- [www.ubuntu.com](http://www.ubuntu.com)
- \*.ubuntu.com
- ppa.launchpad.net
- launchpad.net
- [www.launchpad.net](http://www.launchpad.net)
- \*.nixos.org

###

Development tools and platforms

Development tools and platforms

- dl.k8s.io (Kubernetes)
- pkgs.k8s.io
- k8s.io
- [www.k8s.io](http://www.k8s.io)
- releases.hashicorp.com (HashiCorp)
- apt.releases.hashicorp.com
- rpm.releases.hashicorp.com
- archive.releases.hashicorp.com
- hashicorp.com
- [www.hashicorp.com](http://www.hashicorp.com)
- repo.anaconda.com (Anaconda/Conda)
- conda.anaconda.org
- anaconda.org
- [www.anaconda.com](http://www.anaconda.com)
- anaconda.com
- continuum.io
- apache.org (Apache)
- [www.apache.org](http://www.apache.org)
- archive.apache.org
- downloads.apache.org
- eclipse.org (Eclipse)
- [www.eclipse.org](http://www.eclipse.org)
- download.eclipse.org
- nodejs.org (Node.js)
- [www.nodejs.org](http://www.nodejs.org)
- developer.apple.com
- developer.android.com
- pkg.stainless.com
- binaries.prisma.sh

###

Cloud services and monitoring

Cloud services and monitoring

- statsig.com
- [www.statsig.com](http://www.statsig.com)
- api.statsig.com
- sentry.io
- \*.sentry.io
- downloads.sentry-cdn.com
- http-intake.logs.datadoghq.com
- \*.datadoghq.com
- \*.datadoghq.eu
- api.honeycomb.io

###

Content delivery and mirrors

Content delivery and mirrors

- sourceforge.net
- \*.sourceforge.net
- packagecloud.io
- \*.packagecloud.io
- fonts.googleapis.com
- fonts.gstatic.com

###

Schema and configuration

Schema and configuration

- json-schema.org
- [www.json-schema.org](http://www.json-schema.org)
- json.schemastore.org
- [www.schemastore.org](http://www.schemastore.org)

###

Model Context Protocol

Model Context Protocol

- \*.modelcontextprotocol.io

## Move tasks between web and terminal

These workflows require the

[[Quickstart - Claude Code Docs|Claude Code CLI]]signed in to the same claude.ai account. You can start new cloud sessions from your terminal, or pull cloud sessions into your terminal to continue locally. Cloud sessions persist even if you close your laptop, and you can monitor them from anywhere including the Claude mobile app.

From the CLI, session handoff is one-way: you can pull cloud sessions into your terminal with

```
--teleport
```

, but you can’t push an existing terminal session to the web. The

```
--remote
```

flag creates a new cloud session for your current repository. The [[Use Claude Code Desktop - Claude Code Docs#Continue in another surface|Desktop app]]provides a Continue in menu that can send a local session to the web.

### From terminal to web

Start a cloud session from the command line with the

```
--remote
```

flag:

```
--remote
```

works with a single repository at a time. The task runs in the cloud while you continue working locally.

```
--remote
```

creates cloud sessions.

```
--remote-control
```

is unrelated: it exposes a local CLI session for monitoring from the web. See

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]].

```
/tasks
```

in the Claude Code CLI to check progress, or open the session on claude.ai or the Claude mobile app to interact directly. From there you can steer Claude, provide feedback, or answer questions just like any other conversation.

#### Tips for cloud tasks

Plan locally, execute remotely: for complex tasks, start Claude in plan mode to collaborate on the approach, then send work to the cloud:

[[Plan in the cloud with ultraplan - Claude Code Docs|ultraplan]]. Claude generates the plan on Claude Code on the web while you keep working, then you comment on sections in your browser and choose to execute remotely or send the plan back to your terminal. Run tasks in parallel: each

```
--remote
```

command creates its own cloud session that runs independently. You can start multiple tasks and they’ll all run simultaneously in separate sessions:

```
/tasks
```

in the Claude Code CLI. When a session completes, you can create a PR from the web interface or

[[Use Claude Code on the web - Claude Code Docs#From web to terminal|teleport]]the session to your terminal to continue working.

#### Send local repositories without GitHub

When you run

```
claude --remote
```

from a repository that isn’t connected to GitHub, Claude Code bundles your local repository and uploads it directly to the cloud session. The bundle includes your full repository history across all branches, plus any uncommitted changes to tracked files.
This fallback activates automatically when GitHub access isn’t available. To force it even when GitHub is connected, set

```
CCR_FORCE_BUNDLE=1
```

:

- The directory must be a git repository with at least one commit
- The bundled repository must be under 100 MB. Larger repositories fall back to bundling only the current branch, then to a single squashed snapshot of the working tree, and fail only if the snapshot is still too large
- Untracked files are not included; run

  ```
  git add
  ```

  on files you want the cloud session to see
- Sessions created from a bundle can’t push back to a remote unless you also have [[Use Claude Code on the web - Claude Code Docs#GitHub authentication options|GitHub authentication]]configured

### From web to terminal

Pull a cloud session into your terminal using any of these:

- Using

  ```
  --teleport
  ```

  : from the command line, run

  ```
  claude --teleport
  ```

  for an interactive session picker, or

  ```
  claude --teleport <session-id>
  ```

  to resume a specific session directly. If you have uncommitted changes, you’ll be prompted to stash them first.
- Using

  ```
  /teleport
  ```

  : inside an existing CLI session, run

  ```
  /teleport
  ```

  (or

  ```
  /tp
  ```

  ) to open the same session picker without restarting Claude Code.
- From

  ```
  /tasks
  ```

  : run

  ```
  /tasks
  ```

  to see your background sessions, then press

  ```
  t
  ```

  to teleport into one
- From the web interface: select Open in CLI to copy a command you can paste into your terminal

```
--teleport
```

is distinct from

```
--resume
```

.

```
--resume
```

reopens a conversation from this machine’s local history and doesn’t list cloud sessions;

```
--teleport
```

pulls a cloud session and its branch.

#### Teleport requirements

Teleport checks these requirements before resuming a session. If any requirement isn’t met, you’ll see an error or be prompted to resolve the issue.

RequirementDetailsClean git stateYour working directory must have no uncommitted changes. Teleport prompts you to stash changes if needed.Correct repositoryYou must run

```
--teleport
```

from a checkout of the same repository, not a fork.Branch availableThe branch from the cloud session must have been pushed to the remote. Teleport automatically fetches and checks it out.Same accountYou must be authenticated to the same claude.ai account used in the cloud session.

#### ``` --teleport ``` is unavailable

Teleport requires claude.ai subscription authentication. If you’re authenticated via API key, Bedrock, Vertex AI, or Microsoft Foundry, run

```
/login
```

to sign in with your claude.ai account instead. If you’re already signed in via claude.ai and

```
--teleport
```

is still unavailable, your organization may have disabled cloud sessions.

## Work with sessions

Sessions appear in the sidebar at claude.ai/code. From there you can review changes, share with teammates, archive finished work, or delete sessions permanently.

### Manage context

Cloud sessions support

[[Commands - Claude Code Docs|built-in commands]]that produce text output. Commands that open an interactive terminal picker, like

```
/model
```

or

```
/config
```

, are not available.
For context management specifically:

CommandWorks in cloud sessionsNotes

```
/compact
```

YesSummarizes the conversation to free up context. Accepts optional focus instructions like

```
/compact keep the test output
```

```
/context
```

YesShows what’s currently in the context window

```
/clear
```

NoStart a new session from the sidebar instead

[[Environment variables - Claude Code Docs|in your]]

```
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE
```

[[Use Claude Code on the web - Claude Code Docs#Configure your environment|environment variables]]. For example,

```
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70
```

compacts at 70% capacity instead of the default ~95%. To change the effective window size for compaction calculations, use

[[Environment variables - Claude Code Docs|.]]

```
CLAUDE_CODE_AUTO_COMPACT_WINDOW
```

[[Create custom subagents - Claude Code Docs|Subagents]]work the same way they do locally. Claude can spawn them with the Task tool to offload research or parallel work into a separate context window, keeping the main conversation lighter. Subagents defined in your repo’s

```
.claude/agents/
```

are picked up automatically.

[[Orchestrate teams of Claude Code sessions - Claude Code Docs|Agent teams]]are off by default but can be enabled by adding

```
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

to your

[[Use Claude Code on the web - Claude Code Docs#Configure your environment|environment variables]].

### Review changes

Each session shows a diff indicator with lines added and removed, like

```
+42 -18
```

. Select it to open the diff view, leave inline comments on specific lines, and send them to Claude with your next message. See

[[Get started with Claude Code on the web - Claude Code Docs#Review and iterate|Review and iterate]]for the full walkthrough including PR creation. To have Claude monitor the PR for CI failures and review comments automatically, see

[[Use Claude Code on the web - Claude Code Docs#Auto-fix pull requests|Auto-fix pull requests]].

### Share sessions

To share a session, toggle its visibility according to the account types below. After that, share the session link as-is. Recipients see the latest state when they open the link, but their view doesn’t update in real time.

#### Share from an Enterprise or Team account

For Enterprise and Team accounts, the two visibility options are Private and Team. Team visibility makes the session visible to other members of your claude.ai organization. Repository access verification is enabled by default, based on the GitHub account connected to the recipient’s account. Your account’s display name is visible to all recipients with access.

[[Claude Code in Slack - Claude Code Docs|Claude in Slack]]sessions are automatically shared with Team visibility.

#### Share from a Max or Pro account

For Max and Pro accounts, the two visibility options are Private and Public. Public visibility makes the session visible to any user logged into claude.ai. Check your session for sensitive content before sharing. Sessions may contain code and credentials from private GitHub repositories. Repository access verification is not enabled by default. To require recipients to have repository access, or to hide your name from shared sessions, go to Settings > Claude Code > Sharing settings.

### Archive sessions

You can archive sessions to keep your session list organized. Archived sessions are hidden from the default session list but can be viewed by filtering for archived sessions. To archive a session, hover over the session in the sidebar and select the archive icon.

### Delete sessions

Deleting a session permanently removes the session and its data. This action cannot be undone. You can delete a session in two ways:

- From the sidebar: filter for archived sessions, then hover over the session you want to delete and select the delete icon
- From the session menu: open a session, select the dropdown next to the session title, and select Delete

## Auto-fix pull requests

Claude can watch a pull request and automatically respond to CI failures and review comments. Claude subscribes to GitHub activity on the PR, and when a check fails or a reviewer leaves a comment, Claude investigates and pushes a fix if one is clear.

Auto-fix requires the Claude GitHub App to be installed on your repository. If you haven’t already, install it from the

[GitHub App page](https://github.com/apps/claude)or when prompted during[[Get started with Claude Code on the web - Claude Code Docs#Connect GitHub and create an environment|setup]].

- PRs created in Claude Code on the web: open the CI status bar and select Auto-fix
- From your terminal: run while on the PR’s branch. Claude Code detects the open PR with

  ```
  /autofix-pr
  ```

  ```
  gh
  ```

  , spawns a web session, and turns on auto-fix in one step
- From the mobile app: tell Claude to auto-fix the PR, for example “watch this PR and fix any CI failures or review comments”
- Any existing PR: paste the PR URL into a session and tell Claude to auto-fix it

### How Claude responds to PR activity

When auto-fix is active, Claude receives GitHub events for the PR including new review comments and CI check failures. For each event, Claude investigates and decides how to proceed:

- Clear fixes: if Claude is confident in a fix and it doesn’t conflict with earlier instructions, Claude makes the change, pushes it, and explains what was done in the session
- Ambiguous requests: if a reviewer’s comment could be interpreted multiple ways or involves something architecturally significant, Claude asks you before acting
- Duplicate or no-action events: if an event is a duplicate or requires no change, Claude notes it in the session and moves on

## Security and isolation

Each cloud session is separated from your machine and from other sessions through several layers:

- Isolated virtual machines: each session runs in an isolated, Anthropic-managed VM
- Network access controls: network access is limited by default, and can be disabled. When running with network access disabled, Claude Code can still communicate with the Anthropic API, which may allow data to exit the VM.
- Credential protection: sensitive credentials such as git credentials or signing keys are never inside the sandbox with Claude Code. Authentication is handled through a secure proxy using scoped credentials.
- Secure analysis: code is analyzed and modified within isolated VMs before creating PRs

## Troubleshooting

For runtime API errors that appear in the conversation such as

```
API Error: 500
```

,

```
529 Overloaded
```

,

```
429
```

, or

```
Prompt is too long
```

, see the

[[Error reference - Claude Code Docs|Error reference]]. Those errors and their fixes are shared with the CLI and Desktop app. The sections below cover issues specific to cloud sessions.

### Session creation failed

If a new session fails to start with

```
Session creation failed
```

or stalls at provisioning, Claude Code could not allocate a cloud environment.

- Check [status.claude.com](https://status.claude.com)for cloud session incidents
- Retry after a minute, as capacity is provisioned on demand
- Confirm your repository is reachable. Private repositories require either the GitHub App installed with access to that repository, or a

  ```
  gh
  ```

  token synced via

  ```
  /web-setup
  ```

  . See[[Use Claude Code on the web - Claude Code Docs#GitHub authentication options|GitHub authentication options]].

### Remote Control session expired or access denied

```
--teleport
```

connects through the same Remote Control session infrastructure that cloud sessions use, so authentication and session-expiry errors surface with Remote Control wording. You may see

```
Remote Control session has expired
```

or

```
Access denied
```

. The connection token is short-lived and scoped to your account.

- Run

  ```
  /login
  ```

  locally to refresh your credentials, then reconnect
- Confirm you are signed in to the same account that owns the session
- If you see

  ```
  Remote Control may not be available for this organization
  ```

  , your admin has not enabled remote sessions for your plan

### Environment expired

Cloud sessions stop after a period of inactivity and the underlying environment is reclaimed. From a local terminal, this surfaces as

```
Could not resume session ... its environment has expired. Creating a fresh session instead.
```

On the web, the session is marked expired in the session list.
Reopen the session from

[claude.ai/code](https://claude.ai/code)to provision a fresh environment with your conversation history restored.

## Limitations

Before relying on cloud sessions for a workflow, account for these constraints:

- Rate limits: Claude Code on the web shares rate limits with all other Claude and Claude Code usage within your account. Running multiple tasks in parallel consumes more rate limits proportionately. There is no separate compute charge for the cloud VM.
- Repository authentication: you can only move sessions from web to local when you are authenticated to the same account
- Platform restrictions: repository cloning and pull request creation require GitHub. Self-hosted [[Claude Code with GitHub Enterprise Server - Claude Code Docs|GitHub Enterprise Server]]instances are supported for Team and Enterprise plans. GitLab, Bitbucket, and other non-GitHub repositories can be sent to cloud sessions as a[[Use Claude Code on the web - Claude Code Docs#Send local repositories without GitHub|local bundle]], but the session can’t push results back to the remote

## Related resources

- [[Plan in the cloud with ultraplan - Claude Code Docs|Ultraplan]]: draft a plan in a cloud session and review it in your browser
- [[Find bugs with ultrareview - Claude Code Docs|Ultrareview]]: run a deep multi-agent code review in a cloud sandbox
- [[Automate work with routines - Claude Code Docs|Routines]]: automate work on a schedule, via API call, or in response to GitHub events
- [[Hooks reference - Claude Code Docs|Hooks configuration]]: run scripts at session lifecycle events
- [[Claude Code settings - Claude Code Docs|Settings reference]]: all configuration options
- [[Security - Claude Code Docs|Security]]: isolation guarantees and data handling
- [[Data usage - Claude Code Docs|Data usage]]: what Anthropic retains from cloud sessions

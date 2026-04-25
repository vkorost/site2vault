---
title: Advanced setup - Claude Code Docs
source_url: https://code.claude.com/docs/en/setup
description: System requirements, platform-specific installation, version management,
  and uninstallation for Claude Code.
---

[[Quickstart - Claude Code Docs|quickstart]]. If you’ve never used a terminal before, see the

[[Terminal guide for new users - Claude Code Docs|terminal guide]].

## System requirements

Claude Code runs on the following platforms and configurations:

- Operating system:
  - macOS 13.0+
  - Windows 10 1809+ or Windows Server 2019+
  - Ubuntu 20.04+
  - Debian 10+
  - Alpine Linux 3.19+
- Hardware: 4 GB+ RAM, x64 or ARM64 processor
- Network: internet connection required. See [[Enterprise network configuration - Claude Code Docs#Network access requirements|network configuration]].
- Shell: Bash, Zsh, PowerShell, or CMD. Native Windows setups require [Git for Windows](https://git-scm.com/downloads/win). WSL setups do not.
- Location: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

### Additional dependencies

- ripgrep: usually included with Claude Code. If search fails, see [[Troubleshooting - Claude Code Docs#Search and discovery issues|search troubleshooting]].

## Install Claude Code

To install Claude Code, use one of the following methods:

- Native Install (Recommended)
- Homebrew
- WinGet

macOS, Linux, WSL:Windows PowerShell:Windows CMD:If you see

```
The token '&&' is not a valid statement separator
```

, you’re in PowerShell, not CMD. If you see

```
'irm' is not recognized as an internal or external command
```

, you’re in CMD, not PowerShell. Your prompt shows

```
PS C:\
```

when you’re in PowerShell and

```
C:\
```

without the

```
PS
```

when you’re in CMD.Native Windows setups require [Git for Windows](https://git-scm.com/downloads/win). Install it first if you don’t have it. WSL setups do not need it.

Native installations automatically update in the background to keep you on the latest version.

[[Advanced setup - Claude Code Docs#Install with Linux package managers|apt, dnf, or apk]]on Debian, Fedora, RHEL, and Alpine. After installation completes, open a terminal in the project you want to work in and start Claude Code:

[[Troubleshooting - Claude Code Docs|troubleshooting guide]].

### Set up on Windows

You can run Claude Code natively on Windows or inside WSL. Pick based on where your projects are located and which features you need:

OptionRequires

[Git for Windows](https://git-scm.com/downloads/win)

[Git for Windows](https://git-scm.com/downloads/win), then run the install command from PowerShell or CMD. You do not need to run as Administrator. Whether you install from PowerShell or CMD only affects which install command you run. Your prompt shows

```
PS C:\Users\YourName>
```

in PowerShell and

```
C:\Users\YourName>
```

without the

```
PS
```

in CMD. If you’re new to the terminal, the

[[Terminal guide for new users - Claude Code Docs#Windows|terminal guide]]walks through each step. After installation, launch

```
claude
```

from PowerShell, CMD, or Git Bash. Claude Code uses Git Bash internally to execute commands regardless of where you launched it. If Claude Code can’t find your Git Bash installation, set the path in your

[[Claude Code settings - Claude Code Docs|settings.json file]]:

```
CLAUDE_CODE_USE_POWERSHELL_TOOL=1
```

to opt in or

```
0
```

to opt out. See

[[Tools reference - Claude Code Docs#PowerShell tool|PowerShell tool]]for setup and limitations. Option 2: WSL Open your WSL distribution and run the Linux installer from the

[[Advanced setup - Claude Code Docs#Install Claude Code|install instructions]]above. You install and launch

```
claude
```

inside the WSL terminal, not from PowerShell or CMD.

### Alpine Linux and musl-based distributions

The native installer on Alpine and other musl/uClibc-based distributions requires

```
libgcc
```

,

```
libstdc++
```

, and

```
ripgrep
```

. Install these using your distribution’s package manager, then set

```
USE_BUILTIN_RIPGREP=0
```

.
This example installs the required packages on Alpine:

```
USE_BUILTIN_RIPGREP
```

to

```
0
```

in your

[[Claude Code settings - Claude Code Docs#Available settings|file:]]

```
settings.json
```

## Verify your installation

After installing, confirm Claude Code is working:

[[Troubleshooting - Claude Code Docs#Get more help|:]]

```
claude doctor
```

## Authenticate

Claude Code requires a Pro, Max, Team, Enterprise, or Console account. The free Claude.ai plan does not include Claude Code access. You can also use Claude Code with a third-party API provider like

[[Claude Code on Amazon Bedrock - Claude Code Docs|Amazon Bedrock]],

[[Claude Code on Google Vertex AI - Claude Code Docs|Google Vertex AI]], or

[[Claude Code on Microsoft Foundry - Claude Code Docs|Microsoft Foundry]]. After installing, log in by running

```
claude
```

and following the browser prompts. See

[[Authentication - Claude Code Docs|Authentication]]for all account types and team setup options.

## Update Claude Code

Native installations automatically update in the background. You can

[[Advanced setup - Claude Code Docs#Configure release channel|configure the release channel]]to control whether you receive updates immediately or on a delayed stable schedule, or

[[Advanced setup - Claude Code Docs#Disable auto-updates|disable auto-updates]]entirely. Homebrew, WinGet, and

[[Advanced setup - Claude Code Docs#Install with Linux package managers|Linux package manager]]installations require manual updates.

### Auto-updates

Claude Code checks for updates on startup and periodically while running. Updates download and install in the background, then take effect the next time you start Claude Code.

Homebrew, WinGet, apt, dnf, and apk installations do not auto-update. For Homebrew, run

```
brew upgrade claude-code
```

or

```
brew upgrade claude-code@latest
```

, depending on which cask you installed. For WinGet, run

```
winget upgrade Anthropic.ClaudeCode
```

. For Linux package managers, see the upgrade commands in [[Advanced setup - Claude Code Docs#Install with Linux package managers|Install with Linux package managers]].Known issue: Claude Code may notify you of updates before the new version is available in these package managers. If an upgrade fails, wait and try again later.Homebrew keeps old versions on disk after upgrades. Run

```
brew cleanup
```

periodically to reclaim disk space.

### Configure release channel

Control which release channel Claude Code follows for auto-updates and

```
claude update
```

with the

```
autoUpdatesChannel
```

setting:

- ```
  "latest"
  ```

  , the default: receive new features as soon as they’re released
- ```
  "stable"
  ```

  : use a version that is typically about one week old, skipping releases with major regressions

```
/config
```

→ Auto-update channel, or add it to your

[[Claude Code settings - Claude Code Docs|settings.json file]]:

[[Configure permissions - Claude Code Docs#Managed settings|managed settings]]. Homebrew installations choose a channel by cask name instead of this setting:

```
claude-code
```

tracks stable and

```
claude-code@latest
```

tracks latest.

### Pin a minimum version

The

```
minimumVersion
```

setting establishes a floor. Background auto-updates and

```
claude update
```

refuse to install any version below this value, so moving to the

```
"stable"
```

channel does not downgrade you if you are already on a newer

```
"latest"
```

build.
Switching from

```
"latest"
```

to

```
"stable"
```

via

```
/config
```

prompts you to either stay on the current version or allow the downgrade. Choosing to stay sets

```
minimumVersion
```

to that version. Switching back to

```
"latest"
```

clears it.
Add it to your

[[Claude Code settings - Claude Code Docs|settings.json file]]to pin a floor explicitly:

[[Configure permissions - Claude Code Docs#Managed settings|managed settings]], this enforces an organization-wide minimum that user and project settings cannot override.

### Disable auto-updates

Set

```
DISABLE_AUTOUPDATER
```

to

```
"1"
```

in the

```
env
```

key of your

[[Claude Code settings - Claude Code Docs#Available settings|file:]]

```
settings.json
```

```
DISABLE_AUTOUPDATER
```

only stops the background check;

```
claude update
```

and

```
claude install
```

still work. To block all update paths, including manual updates, set

[[Environment variables - Claude Code Docs|instead. Use this when you distribute Claude Code through your own channels and need users to stay on the version you provide.]]

```
DISABLE_UPDATES
```

### Update manually

To apply an update immediately without waiting for the next background check, run:

## Advanced installation options

These options are for version pinning, Linux package managers, npm, and verifying binary integrity.

### Install a specific version

The native installer accepts either a specific version number or a release channel (

```
latest
```

or

```
stable
```

). The channel you choose at install time becomes your default for auto-updates. See

[[Advanced setup - Claude Code Docs#Configure release channel|configure release channel]]for more information. To install the latest version (default):

- macOS, Linux, WSL
- Windows PowerShell
- Windows CMD

- macOS, Linux, WSL
- Windows PowerShell
- Windows CMD

- macOS, Linux, WSL
- Windows PowerShell
- Windows CMD

### Install with Linux package managers

Claude Code publishes signed apt, dnf, and apk repositories. Replace

```
stable
```

with

```
latest
```

for the rolling channel. Package manager installations do not auto-update through Claude Code; updates arrive through your normal system upgrade workflow.
All repositories are signed with the

[[Advanced setup - Claude Code Docs#Binary integrity and code signing|Claude Code release signing key]]. Before trusting the key, verify it as described in each tab.

- apt
- dnf
- apk

For Debian and Ubuntu. To use the rolling channel, change both Verify the GPG key fingerprint before trusting it:

```
stable
```

occurrences in the

```
deb
```

line: the URL path and the suite name.

```
gpg --show-keys /etc/apt/keyrings/claude-code.asc
```

should report

```
31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE
```

.To upgrade later, run

```
sudo apt update && sudo apt upgrade claude-code
```

.

### Install with npm

You can also install Claude Code as a global npm package. The package requires

[Node.js 18 or later](https://nodejs.org/en/download).

```
@anthropic-ai/claude-code-darwin-arm64
```

, and a postinstall step links it into place. The installed

```
claude
```

binary does not itself invoke Node.
Supported npm install platforms are

```
darwin-arm64
```

,

```
darwin-x64
```

,

```
linux-x64
```

,

```
linux-arm64
```

,

```
linux-x64-musl
```

,

```
linux-arm64-musl
```

,

```
win32-x64
```

, and

```
win32-arm64
```

. Your package manager must allow optional dependencies. See

[[Troubleshooting - Claude Code Docs#Native binary not found after npm install|troubleshooting]]if the binary is missing after install.

### Binary integrity and code signing

Each release publishes a

```
manifest.json
```

containing SHA256 checksums for every platform binary. The manifest is signed with an Anthropic GPG key, so verifying the signature on the manifest transitively verifies every binary it lists.

#### Verify the manifest signature

Steps 1-3 require a POSIX shell with

```
gpg
```

and

```
curl
```

. On Windows, run them in Git Bash or WSL. Step 4 includes a PowerShell option.

Download and import the public key

The release signing key is published at a fixed URL.Display the fingerprint of the imported key.Confirm the output includes this fingerprint:

Verify the signature

Verify the detached signature against the manifest.A valid result reports

```
Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"
```

.

```
gpg
```

also prints

```
WARNING: This key is not certified with a trusted signature!
```

for any freshly imported key. This is expected. The

```
Good signature
```

line confirms the cryptographic check passed. The fingerprint comparison in Step 1 confirms the key itself is authentic.

Manifest signatures are available for releases from

```
2.1.89
```

onward. Earlier releases publish checksums in

```
manifest.json
```

without a detached signature.

#### Platform code signatures

In addition to the signed manifest, individual binaries carry platform-native code signatures where supported.

- macOS: signed by “Anthropic PBC” and notarized by Apple. Verify with

  ```
  codesign --verify --verbose ./claude
  ```

  .
- Windows: signed by “Anthropic, PBC”. Verify with

  ```
  Get-AuthenticodeSignature .\claude.exe
  ```

  .
- Linux: binaries are not individually code-signed. If you download directly from the

  ```
  claude-code-releases
  ```

  bucket or use the native installer, verify integrity with the manifest signature above. If you install with[[Advanced setup - Claude Code Docs#Install with Linux package managers|apt, dnf, or apk]], your package manager verifies signatures automatically using the repository signing key.

## Uninstall Claude Code

To remove Claude Code, follow the instructions for your installation method.

### Native installation

Remove the Claude Code binary and version files:

- macOS, Linux, WSL
- Windows PowerShell

### Homebrew installation

Remove the Homebrew cask you installed. If you installed the stable cask:

### WinGet installation

Remove the WinGet package:

### apt / dnf / apk

Remove the package and the repository configuration:

- apt
- dnf
- apk

### npm

Remove the global npm package:

### Remove configuration files

The VS Code extension, the JetBrains plugin, and the Desktop app also write to

```
~/.claude/
```

. If any of them is still installed, the directory is recreated the next time it runs. To remove Claude Code completely, uninstall the

[[Use Claude Code in VS Code - Claude Code Docs#Uninstall the extension|VS Code extension]], the JetBrains plugin, and the Desktop app before deleting these files. To remove Claude Code settings and cached data:

- macOS, Linux, WSL
- Windows PowerShell

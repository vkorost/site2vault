---
title: Troubleshooting - Claude Code Docs
source_url: https://code.claude.com/docs/en/troubleshooting
description: Discover solutions to common issues with Claude Code installation and
  usage.
---

## Troubleshoot installation issues

Find the error message or symptom you’re seeing:

What you seeSolution

```
command not found: claude
```

or

```
'claude' is not recognized
```

```
syntax error near unexpected token '<'
```

[[Troubleshooting - Claude Code Docs#Install script returns HTML instead of a shell script|Install script returns HTML]]

```
curl: (56) Failure writing output to destination
```

[[Troubleshooting - Claude Code Docs#curl: (56) Failure writing output to destination|Download script first, then run it]]

```
Killed
```

during install on Linux[[Troubleshooting - Claude Code Docs#Install killed on low-memory Linux servers|Add swap space for low-memory servers]]

```
TLS connect error
```

or

```
SSL/TLS secure channel
```

[[Troubleshooting - Claude Code Docs#TLS or SSL connection errors|Update CA certificates]]

```
Failed to fetch version
```

or can’t reach download server[[Troubleshooting - Claude Code Docs#Check network connectivity|Check network and proxy settings]]

```
irm is not recognized
```

or

```
&& is not valid
```

[[Troubleshooting - Claude Code Docs#Windows: wrong install command|Use the right command for your shell]]

```
'bash' is not recognized as the name of a cmdlet
```

[[Troubleshooting - Claude Code Docs#Windows: wrong install command|Use the Windows installer command]]

```
Claude Code on Windows requires git-bash
```

[[Troubleshooting - Claude Code Docs#Windows: Claude Code on Windows requires git-bash|Install or configure Git Bash]]

```
Claude Code does not support 32-bit Windows
```

[[Troubleshooting - Claude Code Docs#Windows: Claude Code does not support 32-bit Windows|Open Windows PowerShell, not the x86 entry]]

```
Error loading shared library
```

[[Troubleshooting - Claude Code Docs#Linux: wrong binary variant installed (musl/glibc mismatch)|Wrong binary variant for your system]]

```
Illegal instruction
```

on Linux[[Troubleshooting - Claude Code Docs|Architecture mismatch]]

```
dyld: cannot load
```

,

```
dyld: Symbol not found
```

, or

```
Abort trap
```

on macOS[[Troubleshooting - Claude Code Docs|Binary incompatibility]]

```
Invoke-Expression: Missing argument in parameter list
```

[[Troubleshooting - Claude Code Docs#Install script returns HTML instead of a shell script|Install script returns HTML]]

```
App unavailable in region
```

[supported countries](https://www.anthropic.com/supported-countries).

```
unable to get local issuer certificate
```

[[Troubleshooting - Claude Code Docs#TLS or SSL connection errors|Configure corporate CA certificates]]

```
OAuth error
```

or

```
403 Forbidden
```

[[Troubleshooting - Claude Code Docs#Authentication issues|Fix authentication]]

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

, or other 4xx and 5xx errors not listed above[[Error reference - Claude Code Docs|Error reference]]

## Debug installation problems

### Check network connectivity

The installer downloads from

```
downloads.claude.ai
```

. Verify you can reach it:

- Corporate firewalls or proxies blocking

  ```
  downloads.claude.ai
  ```
- Regional network restrictions: try a VPN or alternative network
- TLS/SSL issues: update your system’s CA certificates, or check if

  ```
  HTTPS_PROXY
  ```

  is configured

```
HTTPS_PROXY
```

and

```
HTTP_PROXY
```

to your proxy’s address before installing. Ask your IT team for the proxy URL if you don’t know it, or check your browser’s proxy settings.
This example sets both proxy variables, then runs the installer through your proxy:

### Verify your PATH

If installation succeeded but you get a

```
command not found
```

or

```
not recognized
```

error when running

```
claude
```

, the install directory isn’t in your PATH. Your shell searches for programs in directories listed in PATH, and the installer places

```
claude
```

at

```
~/.local/bin/claude
```

on macOS/Linux or

```
%USERPROFILE%\.local\bin\claude.exe
```

on Windows.
Check if the install directory is in your PATH by listing your PATH entries and filtering for

```
local/bin
```

:

- macOS/Linux
- Windows PowerShell
- Windows CMD

### Check for conflicting installations

Multiple Claude Code installations can cause version mismatches or unexpected behavior. Check what’s installed:

- macOS/Linux
- Windows PowerShell

List all Check whether the native installer and npm versions are present:

```
claude
```

binaries found in your PATH:

```
~/.local/bin/claude
```

is recommended. Remove any extra installations:
Uninstall an npm global install:

```
claude-code@latest
```

if you installed that cask):

### Check directory permissions

The installer needs write access to

```
~/.local/bin/
```

and

```
~/.claude/
```

. If installation fails with permission errors, check whether these directories are writable:

### Verify the binary works

If

```
claude
```

is installed but crashes or hangs on startup, run these checks to narrow down the cause.
Confirm the binary exists and is executable:

```
ldd
```

shows missing libraries, you may need to install system packages. On Alpine Linux and other musl-based distributions, see

[[Advanced setup - Claude Code Docs#Alpine Linux and musl-based distributions|Alpine Linux setup]].

## Common installation issues

These are the most frequently encountered installation problems and their solutions.

### Install script returns HTML instead of a shell script

When running the install command, you may see one of these errors:

[supported countries](https://www.anthropic.com/supported-countries). Otherwise, this can happen due to network issues, regional routing, or a temporary service disruption. Solutions:

- Use an alternative install method:
  On macOS or Linux, install via Homebrew:
  On Windows, install via WinGet:
- Retry after a few minutes: the issue is often temporary. Wait and try the original command again.

### ``` command not found: claude ``` after installation

The install finished but

```
claude
```

doesn’t work. The exact error varies by platform:

PlatformError messagemacOS

```
zsh: command not found: claude
```

Linux

```
bash: claude: command not found
```

Windows CMD

```
'claude' is not recognized as an internal or external command
```

PowerShell

```
claude : The term 'claude' is not recognized as the name of a cmdlet
```

[[Troubleshooting - Claude Code Docs#Verify your PATH|Verify your PATH]]for the fix on each platform.

### ``` curl: (56) Failure writing output to destination ```

The

```
curl ... | bash
```

command downloads the script and passes it directly to Bash for execution using a pipe (

```
|
```

). This error means the connection broke before the script finished downloading. Common causes include network interruptions, the download being blocked mid-stream, or system resource limits.
Solutions:

- Check network stability: Claude Code binaries are hosted at

  ```
  downloads.claude.ai
  ```

  . Test that you can reach it:If the command completes silently, your connection is fine and the issue is likely intermittent. Retry the install command. If you see an error, your network may be blocking the download.
- Try an alternative install method:
  On macOS or Linux:
  On Windows:

### TLS or SSL connection errors

Errors like

```
curl: (35) TLS connect error
```

,

```
schannel: next InitializeSecurityContext failed
```

, or PowerShell’s

```
Could not establish trust relationship for the SSL/TLS secure channel
```

indicate TLS handshake failures.
Solutions:

- Update your system CA certificates:
  On Ubuntu/Debian:
  On macOS via Homebrew:
- On Windows, enable TLS 1.2 in PowerShell before running the installer:
- Check for proxy or firewall interference: corporate proxies that perform TLS inspection can cause these errors, including

  ```
  unable to get local issuer certificate
  ```

  . Set

  ```
  NODE_EXTRA_CA_CERTS
  ```

  to your corporate CA certificate bundle:Ask your IT team for the certificate file if you don’t have it. You can also try on a direct connection to confirm the proxy is the cause.
- On Windows, bypass certificate revocation checks if you see

  ```
  CRYPT_E_NO_REVOCATION_CHECK (0x80092012)
  ```

  or

  ```
  CRYPT_E_REVOCATION_OFFLINE (0x80092013)
  ```

  . These mean curl reached the server but your network blocks the certificate revocation lookup, which is common behind corporate firewalls. Add

  ```
  --ssl-revoke-best-effort
  ```

  to the install command:Alternatively, install with

  ```
  winget install Anthropic.ClaudeCode
  ```

  , which avoids curl entirely.

### ``` Failed to fetch version from downloads.claude.ai ```

The installer couldn’t reach the download server. This typically means

```
downloads.claude.ai
```

is blocked on your network.
Solutions:

- Test connectivity directly:
- If behind a proxy, set

  ```
  HTTPS_PROXY
  ```

  so the installer can route through it. See[[Enterprise network configuration - Claude Code Docs#Proxy configuration|proxy configuration]]for details.
- If on a restricted network, try a different network or VPN, or use an alternative install method:
  On macOS or Linux:
  On Windows:

### Windows: wrong install command

If you see

```
'irm' is not recognized
```

,

```
The token '&&' is not valid
```

, or

```
'bash' is not recognized as the name of a cmdlet
```

, you copied the install command for a different shell or operating system.

- ```
  irm
  ```

  not recognized: you’re in CMD, not PowerShell. You have two options: Open PowerShell by searching for “PowerShell” in the Start menu, then run the original install command:Or stay in CMD and use the CMD installer instead:
- ```
  &&
  ```

  not valid: you’re in PowerShell but ran the CMD installer command. Use the PowerShell installer:
- ```
  bash
  ```

  not recognized: you ran the macOS/Linux installer on Windows. Use the PowerShell installer instead:

### Install killed on low-memory Linux servers

If you see

```
Killed
```

during installation on a VPS or cloud instance:

- Add swap space if your server has limited RAM. Swap uses disk space as overflow memory, letting the install complete even with low physical RAM.
  Create a 2 GB swap file and enable it:
  Then retry the installation:
- Close other processes to free memory before installing.
- Use a larger instance if possible. Claude Code requires at least 4 GB of RAM.

### Install hangs in Docker

When installing Claude Code in a Docker container, installing as root into

```
/
```

can cause hangs.
Solutions:

- Set a working directory before running the installer. When run from

  ```
  /
  ```

  , the installer scans the entire filesystem, which causes excessive memory usage. Setting

  ```
  WORKDIR
  ```

  limits the scan to a small directory:
- Increase Docker memory limits if using Docker Desktop:

### Windows: Claude Desktop overrides ``` claude ``` CLI command

If you installed an older version of Claude Desktop, it may register a

```
Claude.exe
```

in the

```
WindowsApps
```

directory that takes PATH priority over Claude Code CLI. Running

```
claude
```

opens the Desktop app instead of the CLI.
Update Claude Desktop to the latest version to fix this issue.

### Windows: Claude Code on Windows requires git-bash

Claude Code on native Windows needs

[Git for Windows](https://git-scm.com/downloads/win), which includes Git Bash. If Git is not installed, download and install it from

[git-scm.com/downloads/win](https://git-scm.com/downloads/win). During setup, select “Add to PATH.” Restart your terminal after installing. If Git is already installed but Claude Code still can’t find it, set the path in your

[[Claude Code settings - Claude Code Docs|settings.json file]]:

```
where.exe git
```

in PowerShell and use the

```
bin\bash.exe
```

path from that directory.

### Windows: Claude Code does not support 32-bit Windows

Windows includes two PowerShell entries in the Start menu:

```
Windows PowerShell
```

and

```
Windows PowerShell (x86)
```

. The x86 entry runs as a 32-bit process and triggers this error even on a 64-bit machine. To check which case you’re in, run this in the same window that produced the error:

```
True
```

, your operating system is fine. Close the window, open

```
Windows PowerShell
```

without the x86 suffix, and run the install command again.
If this prints

```
False
```

, you are on a 32-bit edition of Windows. Claude Code requires a 64-bit operating system. See the

[[Advanced setup - Claude Code Docs#System requirements|system requirements]].

### Linux: wrong binary variant installed (musl/glibc mismatch)

If you see errors about missing shared libraries like

```
libstdc++.so.6
```

or

```
libgcc_s.so.1
```

after installation, the installer may have downloaded the wrong binary variant for your system.

- Check which libc your system uses:
  If it shows

  ```
  linux-vdso.so
  ```

  or references to

  ```
  /lib/x86_64-linux-gnu/
  ```

  , you’re on glibc. If it shows

  ```
  musl
  ```

  , you’re on musl.
- If you’re on glibc but got the musl binary, remove the installation and reinstall. You can also manually download the correct binary using the manifest at

  ```
  https://downloads.claude.ai/claude-code-releases/{VERSION}/manifest.json
  ```

  . File a[GitHub issue](https://github.com/anthropics/claude-code/issues)with the output of

  ```
  ldd /bin/ls
  ```

  and

  ```
  ls /lib/libc.musl*
  ```

  .
- If you’re actually on musl (Alpine Linux), install the required packages:

### ``` Illegal instruction ``` on Linux

If the installer prints

```
Illegal instruction
```

instead of the OOM

```
Killed
```

message, the downloaded binary doesn’t match your CPU architecture. This commonly happens on ARM servers that receive an x86 binary, or on older CPUs that lack required instruction sets.

- Verify your architecture:

  ```
  x86_64
  ```

  means 64-bit Intel/AMD,

  ```
  aarch64
  ```

  means ARM64. If the binary doesn’t match,[file a GitHub issue](https://github.com/anthropics/claude-code/issues)with the output.
- Try an alternative install method while the architecture issue is resolved:

### ``` dyld: cannot load ``` on macOS

If you see

```
dyld: cannot load
```

,

```
dyld: Symbol not found
```

, or

```
Abort trap: 6
```

during installation, the binary is incompatible with your macOS version or hardware.

```
Symbol not found
```

error that references

```
libicucore
```

also indicates your macOS version is older than the binary supports:

- Check your macOS version: Claude Code requires macOS 13.0 or later. Open the Apple menu and select About This Mac to check your version.
- Update macOS if you’re on an older version. The binary uses load commands that older macOS versions don’t support.
- Try Homebrew as an alternative install method:

### Windows installation issues: errors in WSL

You might encounter the following issues in WSL: OS/platform detection issues: if you receive an error during installation, WSL may be using Windows

```
npm
```

. Try:

- Run

  ```
  npm config set os linux
  ```

  before installation
- Install with

  ```
  npm install -g @anthropic-ai/claude-code --force --no-os-check
  ```

  . Do not use

  ```
  sudo
  ```

  .

```
exec: node: not found
```

when running

```
claude
```

, your WSL environment may be using a Windows installation of Node.js. You can confirm this with

```
which npm
```

and

```
which node
```

, which should point to Linux paths starting with

```
/usr/
```

rather than

```
/mnt/c/
```

. To fix this, try installing Node via your Linux distribution’s package manager or via

[. nvm version conflicts: if you have nvm installed in both WSL and Windows, you may experience version conflicts when switching Node versions in WSL. This happens because WSL imports the Windows PATH by default, causing Windows nvm/npm to take priority over the WSL installation. You can identify this issue by:](https://github.com/nvm-sh/nvm)

```
nvm
```

- Running

  ```
  which npm
  ```

  and

  ```
  which node
  ```

  - if they point to Windows paths (starting with

  ```
  /mnt/c/
  ```

  ), Windows versions are being used
- Experiencing broken functionality after switching Node versions with nvm in WSL

```
~/.bashrc
```

,

```
~/.zshrc
```

, etc.):

### WSL2 sandbox setup

[[Sandboxing - Claude Code Docs|Sandboxing]]is supported on WSL2 but requires installing additional packages. If you see an error about missing

```
bubblewrap
```

or

```
socat
```

when running

```
/sandbox
```

, install the dependencies:

- Ubuntu/Debian
- Fedora

```
cmd.exe
```

,

```
powershell.exe
```

, or executables under

```
/mnt/c/
```

. WSL hands these off to the Windows host over a Unix socket, which the sandbox blocks. If a command needs to invoke a Windows binary, add it to

[[Claude Code settings - Claude Code Docs#Sandbox settings|so it runs outside the sandbox.]]

```
excludedCommands
```

### Permission errors during installation

If the native installer fails with permission errors, the target directory may not be writable. See

[[Troubleshooting - Claude Code Docs#Check directory permissions|Check directory permissions]]. If you previously installed with npm and are hitting npm-specific permission errors, switch to the native installer:

### Native binary not found after npm install

The

```
@anthropic-ai/claude-code
```

npm package pulls in the native binary through a per-platform optional dependency such as

```
@anthropic-ai/claude-code-darwin-arm64
```

. If running

```
claude
```

after install prints

```
Could not find native binary package "@anthropic-ai/claude-code-<platform>"
```

, check the following causes:

- Optional dependencies are disabled. Remove

  ```
  --omit=optional
  ```

  from your npm install command,

  ```
  --no-optional
  ```

  from pnpm, or

  ```
  --ignore-optional
  ```

  from yarn, and check that

  ```
  .npmrc
  ```

  does not set

  ```
  optional=false
  ```

  . Then reinstall. The native binary is delivered only as an optional dependency, so there is no JavaScript fallback if it is skipped.
- Unsupported platform. Prebuilt binaries are published for

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

  . Claude Code does not ship a binary for other platforms; see the[[Advanced setup - Claude Code Docs#System requirements|system requirements]].
- Corporate npm mirror is missing the platform packages. Ensure your registry mirrors all eight

  ```
  @anthropic-ai/claude-code-*
  ```

  platform packages in addition to the meta package.

```
--ignore-scripts
```

does not trigger this error. The postinstall step that links the binary into place is skipped, so Claude Code falls back to a wrapper that locates and spawns the platform binary on each launch. This works but starts more slowly; reinstall with scripts enabled for direct execution.

## Permissions and authentication

These sections address login failures, token issues, and permission prompt behavior.

### Repeated permission prompts

If you find yourself repeatedly approving the same commands, you can allow specific tools to run without approval using the

```
/permissions
```

command. See

[[Configure permissions - Claude Code Docs#Manage permissions|Permissions docs]].

### Authentication issues

If you’re experiencing authentication problems:

- Run

  ```
  /logout
  ```

  to sign out completely
- Close Claude Code
- Restart with

  ```
  claude
  ```

  and complete the authentication process again

```
c
```

to copy the OAuth URL to your clipboard, then paste it into your browser manually.

### OAuth error: Invalid code

If you see

```
OAuth error: Invalid code. Please make sure the full code was copied
```

, the login code expired or was truncated during copy-paste.
Solutions:

- Press Enter to retry and complete the login quickly after the browser opens
- Type

  ```
  c
  ```

  to copy the full URL if the browser doesn’t open automatically
- If using a remote/SSH session, the browser may open on the wrong machine. Copy the URL displayed in the terminal and open it in your local browser instead.

### 403 Forbidden after login

If you see

```
API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}
```

after logging in:

- Claude Pro/Max users: verify your subscription is active at [claude.ai/settings](https://claude.ai/settings)
- Console users: confirm your account has the “Claude Code” or “Developer” role assigned by your admin
- Behind a proxy: corporate proxies can interfere with API requests. See [[Enterprise network configuration - Claude Code Docs|network configuration]]for proxy setup.

### Model not found or not accessible

If you see

```
There's an issue with the selected model (...). It may not exist or you may not have access to it
```

, the API rejected the configured model name.
Common causes:

- A typo in the model name passed to

  ```
  --model
  ```
- A stale or deprecated model ID saved in your settings
- An API key without access to that model on your current usage tier

[[Model configuration - Claude Code Docs#Setting your model|priority order]]:

- The

  ```
  --model
  ```

  flag
- The

  ```
  ANTHROPIC_MODEL
  ```

  environment variable
- The

  ```
  model
  ```

  field in

  ```
  .claude/settings.local.json
  ```
- The

  ```
  model
  ```

  field in your project’s

  ```
  .claude/settings.json
  ```
- The

  ```
  model
  ```

  field in

  ```
  ~/.claude/settings.json
  ```

```
model
```

field from your settings or unset

```
ANTHROPIC_MODEL
```

, and Claude Code will fall back to the default model for your account.
To browse models available to your account, start

```
claude
```

interactively and run

```
/model
```

to open the picker. For Vertex AI deployments, see

[[Claude Code on Google Vertex AI - Claude Code Docs#Troubleshooting|the Vertex AI troubleshooting section]].

### This organization has been disabled with an active subscription

If you see

```
API Error: 400 ... "This organization has been disabled"
```

despite having an active Claude subscription, an

```
ANTHROPIC_API_KEY
```

environment variable is overriding your subscription. This commonly happens when an old API key from a previous employer or project is still set in your shell profile.
When

```
ANTHROPIC_API_KEY
```

is present and you have approved it, Claude Code uses that key instead of your subscription’s OAuth credentials. In non-interactive mode (

```
-p
```

), the key is always used when present. See

[[Authentication - Claude Code Docs#Authentication precedence|authentication precedence]]for the full resolution order. To use your subscription instead, unset the environment variable and remove it from your shell profile:

```
~/.zshrc
```

,

```
~/.bashrc
```

, or

```
~/.profile
```

for

```
export ANTHROPIC_API_KEY=...
```

lines and remove them to make the change permanent. Run

```
/status
```

inside Claude Code to confirm which authentication method is active.

### OAuth login fails in WSL2

Browser-based login in WSL2 may fail if WSL can’t open your Windows browser. Set the

```
BROWSER
```

environment variable:

```
c
```

to copy the OAuth URL, then paste it into your Windows browser.

### Not logged in or token expired

If Claude Code prompts you to log in again after a session, your OAuth token may have expired. Run

```
/login
```

to re-authenticate. If this happens frequently, check that your system clock is accurate, as token validation depends on correct timestamps.
On macOS, login can also fail when the Keychain is locked or its password is out of sync with your account password, which prevents Claude Code from saving credentials. Run

```
claude doctor
```

to check Keychain access. To unlock the Keychain manually, run

```
security unlock-keychain ~/Library/Keychains/login.keychain-db
```

. If unlocking doesn’t help, open Keychain Access, select the

```
login
```

keychain, and choose Edit > Change Password for Keychain “login” to resync it with your account password.

## Configuration file locations

Claude Code stores configuration in several locations:

FilePurpose

```
~/.claude/settings.json
```

User settings (permissions, hooks, model overrides)

```
.claude/settings.json
```

Project settings (checked into source control)

```
.claude/settings.local.json
```

Local project settings (not committed)

```
~/.claude.json
```

Global state (theme, OAuth, MCP servers)

```
.mcp.json
```

Project MCP servers (checked into source control)

```
managed-mcp.json
```

[[Claude Code settings - Claude Code Docs#Settings files|Managed settings]](server-managed, MDM/OS-level policies, or file-based)

```
~
```

refers to your user home directory, such as

```
C:\Users\YourName
```

.
For details on configuring these files, see

[[Claude Code settings - Claude Code Docs|Settings]]and

[[Connect Claude Code to tools via MCP - Claude Code Docs|MCP]].

### Resetting configuration

To reset Claude Code to default settings, you can remove the configuration files:

## Performance and stability

These sections cover issues related to resource usage, responsiveness, and search behavior.

### High CPU or memory usage

Claude Code is designed to work with most development environments, but may consume significant resources when processing large codebases. If you’re experiencing performance issues:

- Use

  ```
  /compact
  ```

  regularly to reduce context size
- Close and restart Claude Code between major tasks
- Consider adding large build directories to your

  ```
  .gitignore
  ```

  file

```
/heapdump
```

to write a JavaScript heap snapshot and a memory breakdown to

```
~/Desktop
```

. The breakdown shows resident set size, JS heap, array buffers, and unaccounted native memory, which helps identify whether the growth is in JavaScript objects or in native code. Open the

```
.heapsnapshot
```

file in Chrome DevTools under Memory → Load to inspect retainers. Attach both files when reporting a memory issue on

[GitHub](https://github.com/anthropics/claude-code/issues).

### Auto-compaction stops with a thrashing error

If you see

```
Autocompact is thrashing: the context refilled to the limit...
```

, automatic compaction succeeded but a file or tool output immediately refilled the context window several times in a row. Claude Code stops retrying to avoid wasting API calls on a loop that isn’t making progress.
To recover:

- Ask Claude to read the oversized file in smaller chunks, such as a specific line range or function, instead of the whole file
- Run

  ```
  /compact
  ```

  with a focus that drops the large output, for example

  ```
  /compact keep only the plan and the diff
  ```
- Move the large-file work to a [[Create custom subagents - Claude Code Docs|subagent]]so it runs in a separate context window
- Run

  ```
  /clear
  ```

  if the earlier conversation is no longer needed

### Command hangs or freezes

If Claude Code seems unresponsive:

- Press Ctrl+C to attempt to cancel the current operation
- If unresponsive, you may need to close the terminal and restart

### Search and discovery issues

If Search tool,

```
@file
```

mentions, custom agents, and custom skills aren’t working, install system

```
ripgrep
```

:

```
USE_BUILTIN_RIPGREP=0
```

in your

[[Environment variables - Claude Code Docs|environment]].

### Slow or incomplete search results on WSL

Disk read performance penalties when

[working across file systems on WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems)may result in fewer-than-expected matches when using Claude Code on WSL. Search still functions, but returns fewer results than on a native filesystem.

```
/doctor
```

will show Search as OK in this case.

- Submit more specific searches: reduce the number of files searched by specifying directories or file types: “Search for JWT validation logic in the auth-service package” or “Find use of md5 hash in JS files”.
- Move project to Linux filesystem: if possible, ensure your project is located on the Linux filesystem (

  ```
  /home/
  ```

  ) rather than the Windows filesystem (

  ```
  /mnt/c/
  ```

  ).
- Use native Windows instead: consider running Claude Code natively on Windows instead of through WSL, for better file system performance.

## IDE integration issues

If Claude Code does not connect to your IDE or behaves unexpectedly within an IDE terminal, try the solutions below.

### JetBrains IDE not detected on WSL2

If you’re using Claude Code on WSL2 with JetBrains IDEs and getting “No available IDEs detected” errors, this is likely due to WSL2’s networking configuration or Windows Firewall blocking the connection.

#### WSL2 networking modes

WSL2 uses NAT networking by default, which can prevent IDE detection. You have two options: Option 1: Configure Windows Firewall (recommended)

- Find your WSL2 IP address:
- Open PowerShell as Administrator and create a firewall rule:
  Adjust the IP range based on your WSL2 subnet from step 1.
- Restart both your IDE and Claude Code

```
.wslconfig
```

in your Windows user directory:

```
wsl --shutdown
```

from PowerShell.

These networking issues only affect WSL2. WSL1 uses the host’s network directly and doesn’t require these configurations.

[[JetBrains IDEs - Claude Code Docs#Plugin Settings|JetBrains IDE guide]].

### Report Windows IDE integration issues

If you’re experiencing IDE integration problems on Windows,

[create an issue](https://github.com/anthropics/claude-code/issues)with the following information:

- Environment type: native Windows (Git Bash) or WSL1/WSL2
- WSL networking mode, if applicable: NAT or mirrored
- IDE name and version
- Claude Code extension/plugin version
- Shell type: Bash, Zsh, PowerShell, etc.

### Escape key not working in JetBrains IDE terminals

If you’re using Claude Code in JetBrains terminals and the

```
Esc
```

key doesn’t interrupt the agent as expected, this is likely due to a keybinding clash with JetBrains’ default shortcuts.
To fix this issue:

- Go to Settings → Tools → Terminal
- Either:
  - Uncheck “Move focus to the editor with Escape”, or
  - Click “Configure terminal keybindings” and delete the “Switch focus to Editor” shortcut
- Apply the changes

```
Esc
```

key to properly interrupt Claude Code operations.

## Markdown formatting issues

Claude Code sometimes generates markdown files with missing language tags on code fences, which can affect syntax highlighting and readability in GitHub, editors, and documentation tools.

### Missing language tags in code blocks

If you notice code blocks like this in generated markdown:

- Ask Claude to add language tags: request “Add appropriate language tags to all code blocks in this markdown file.”
- Use post-processing hooks: set up automatic formatting hooks to detect and add missing language tags. See [[Automate workflows with hooks - Claude Code Docs#Auto-format code after edits|Auto-format code after edits]]for an example of a PostToolUse formatting hook.
- Manual verification: after generating markdown files, review them for proper code block formatting and request corrections if needed.

### Inconsistent spacing and formatting

If generated markdown has excessive blank lines or inconsistent spacing: Solutions:

- Request formatting corrections: ask Claude to “Fix spacing and formatting issues in this markdown file.”
- Use formatting tools: set up hooks to run markdown formatters like

  ```
  prettier
  ```

  or custom formatting scripts on generated markdown files.
- Specify formatting preferences: include formatting requirements in your prompts or project [[How Claude remembers your project - Claude Code Docs|memory]]files.

### Reduce markdown formatting issues

To minimize formatting issues:

- Be explicit in requests: ask for “properly formatted markdown with language-tagged code blocks”
- Use project conventions: document your preferred markdown style in

  ```
  CLAUDE.md
  ```
- Set up validation hooks: use post-processing hooks to automatically verify and fix common formatting issues

## Get more help

If you’re experiencing issues not covered here:

- See the [[Error reference - Claude Code Docs|Error reference]]for

  ```
  API Error: 5xx
  ```

  ,

  ```
  529 Overloaded
  ```

  ,

  ```
  429
  ```

  , and request validation errors that appear during a session
- Use the

  ```
  /feedback
  ```

  command within Claude Code to report problems directly to Anthropic
- Check the [GitHub repository](https://github.com/anthropics/claude-code)for known issues
- Run

  ```
  /doctor
  ```

  to diagnose issues. It checks:
  - Installation type, version, and search functionality
  - Auto-update status and available versions
  - Invalid settings files (malformed JSON, incorrect types)
  - MCP server configuration errors, including the same server name defined in multiple scopes with different endpoints
  - Keybinding configuration problems
  - Context usage warnings (large CLAUDE.md files, high MCP token usage, unreachable permission rules)
  - Plugin and agent loading errors
- Ask Claude directly about its capabilities and features - Claude has built-in access to its documentation

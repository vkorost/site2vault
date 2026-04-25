---
title: Authentication - Claude Code Docs
source_url: https://code.claude.com/docs/en/authentication
description: Log in to Claude Code and configure authentication for individuals, teams,
  and organizations.
---

## Log in to Claude Code

After

[[Advanced setup - Claude Code Docs#Install Claude Code|installing Claude Code]], run

```
claude
```

in your terminal. On first launch, Claude Code opens a browser window for you to log in.
If the browser doesn’t open automatically, press

```
c
```

to copy the login URL to your clipboard, then paste it into your browser.
If your browser shows a login code instead of redirecting back after you sign in, paste it into the terminal at the

```
Paste code here if prompted
```

prompt.
You can authenticate with any of these account types:

- Claude Pro or Max subscription: log in with your Claude.ai account. Subscribe at [claude.com/pricing](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=authentication_pro_max).
- Claude for Teams or Enterprise: log in with the Claude.ai account your team admin invited you to.
- Claude Console: log in with your Console credentials. Your admin must have [[Authentication - Claude Code Docs#Claude Console authentication|invited you]]first.
- Cloud providers: if your organization uses [[Claude Code on Amazon Bedrock - Claude Code Docs|Amazon Bedrock]],[[Claude Code on Google Vertex AI - Claude Code Docs|Google Vertex AI]], or[[Claude Code on Microsoft Foundry - Claude Code Docs|Microsoft Foundry]], set the required environment variables before running

  ```
  claude
  ```

  . No browser login is needed.

```
/logout
```

at the Claude Code prompt.
If you’re having trouble logging in, see

[[Troubleshooting - Claude Code Docs#Authentication issues|authentication troubleshooting]].

## Set up team authentication

For teams and organizations, you can configure Claude Code access in one of these ways:

- [[Authentication - Claude Code Docs#Claude for Teams or Enterprise|Claude for Teams or Enterprise]], recommended for most teams
- [[Authentication - Claude Code Docs#Claude Console authentication|Claude Console]]
- [[Claude Code on Amazon Bedrock - Claude Code Docs|Amazon Bedrock]]
- [[Claude Code on Google Vertex AI - Claude Code Docs|Google Vertex AI]]
- [[Claude Code on Microsoft Foundry - Claude Code Docs|Microsoft Foundry]]

### Claude for Teams or Enterprise

[Claude for Teams](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=authentication_teams#team-&-enterprise)and

[Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=authentication_enterprise)provide the best experience for organizations using Claude Code. Team members get access to both Claude Code and Claude on the web with centralized billing and team management.

- Claude for Teams: self-service plan with collaboration features, admin tools, and billing management. Best for smaller teams.
- Claude for Enterprise: adds SSO, domain capture, role-based permissions, compliance API, and managed policy settings for organization-wide Claude Code configurations. Best for larger organizations with security and compliance requirements.

Subscribe

Subscribe to

[Claude for Teams](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=authentication_teams_step#team-&-enterprise)or contact sales for[Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=authentication_enterprise_step).

### Claude Console authentication

For organizations that prefer API-based billing, you can set up access through the Claude Console.

Add users

You can add users through either method:

- Bulk invite users from within the Console: Settings -> Members -> Invite
- [Set up SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso)

Assign roles

When inviting users, assign one of:

- Claude Code role: users can only create Claude Code API keys
- Developer role: users can create any kind of API key

Users complete setup

Each invited user needs to:

- Accept the Console invite
- [[Advanced setup - Claude Code Docs#System requirements|Check system requirements]]
- [[Advanced setup - Claude Code Docs#Install Claude Code|Install Claude Code]]
- Log in with Console account credentials

### Cloud provider authentication

For teams using Amazon Bedrock, Google Vertex AI, or Microsoft Foundry:

Follow provider setup

Follow the

[[Claude Code on Amazon Bedrock - Claude Code Docs|Bedrock docs]],[[Claude Code on Google Vertex AI - Claude Code Docs|Vertex docs]], or[[Claude Code on Microsoft Foundry - Claude Code Docs|Microsoft Foundry docs]].

Distribute configuration

Distribute the environment variables and instructions for generating cloud credentials to your users. Read more about how to

[[Claude Code settings - Claude Code Docs|manage configuration here]].

Install Claude Code

Users can

[[Advanced setup - Claude Code Docs#Install Claude Code|install Claude Code]].

## Credential management

Claude Code securely manages your authentication credentials:

- Storage location: on macOS, credentials are stored in the encrypted macOS Keychain. On Linux and Windows, credentials are stored in

  ```
  ~/.claude/.credentials.json
  ```

  , or under

  ```
  $CLAUDE_CONFIG_DIR
  ```

  if that variable is set. On Linux, the file is written with mode

  ```
  0600
  ```

  ; on Windows, it inherits the access controls of your user profile directory.
- Supported authentication types: Claude.ai credentials, Claude API credentials, Azure Auth, Bedrock Auth, and Vertex Auth.
- Custom credential scripts: the setting can be configured to run a shell script that returns an API key.

  ```
  apiKeyHelper
  ```
- Refresh intervals: by default,

  ```
  apiKeyHelper
  ```

  is called after 5 minutes or on HTTP 401 response. Set

  ```
  CLAUDE_CODE_API_KEY_HELPER_TTL_MS
  ```

  environment variable for custom refresh intervals.
- Slow helper notice: if

  ```
  apiKeyHelper
  ```

  takes longer than 10 seconds to return a key, Claude Code displays a warning notice in the prompt bar showing the elapsed time. If you see this notice regularly, check whether your credential script can be optimized.

```
apiKeyHelper
```

,

```
ANTHROPIC_API_KEY
```

, and

```
ANTHROPIC_AUTH_TOKEN
```

apply to terminal CLI sessions only. Claude Desktop and remote sessions use OAuth exclusively and do not call

```
apiKeyHelper
```

or read API key environment variables.

### Authentication precedence

When multiple credentials are present, Claude Code chooses one in this order:

- Cloud provider credentials, when

  ```
  CLAUDE_CODE_USE_BEDROCK
  ```

  ,

  ```
  CLAUDE_CODE_USE_VERTEX
  ```

  , or

  ```
  CLAUDE_CODE_USE_FOUNDRY
  ```

  is set. See[[Enterprise deployment overview - Claude Code Docs|third-party integrations]]for setup.
- ```
  ANTHROPIC_AUTH_TOKEN
  ```

  environment variable. Sent as the

  ```
  Authorization: Bearer
  ```

  header. Use this when routing through an[[LLM gateway configuration - Claude Code Docs|LLM gateway or proxy]]that authenticates with bearer tokens rather than Anthropic API keys.
- ```
  ANTHROPIC_API_KEY
  ```

  environment variable. Sent as the

  ```
  X-Api-Key
  ```

  header. Use this for direct Anthropic API access with a key from the[Claude Console](https://platform.claude.com). In interactive mode, you are prompted once to approve or decline the key, and your choice is remembered. To change it later, use the “Use custom API key” toggle in

  ```
  /config
  ```

  . In non-interactive mode (

  ```
  -p
  ```

  ), the key is always used when present.
- script output. Use this for dynamic or rotating credentials, such as short-lived tokens fetched from a vault.

  ```
  apiKeyHelper
  ```
- ```
  CLAUDE_CODE_OAUTH_TOKEN
  ```

  environment variable. A long-lived OAuth token generated by. Use this for CI pipelines and scripts where browser login isn’t available.

  ```
  claude setup-token
  ```
- Subscription OAuth credentials from

  ```
  /login
  ```

  . This is the default for Claude Pro, Max, Team, and Enterprise users.

```
ANTHROPIC_API_KEY
```

set in your environment, the API key takes precedence once approved. This can cause authentication failures if the key belongs to a disabled or expired organization. Run

```
unset ANTHROPIC_API_KEY
```

to fall back to your subscription, and check

```
/status
```

to confirm which method is active.

[[Use Claude Code on the web - Claude Code Docs|Claude Code on the Web]]always uses your subscription credentials.

```
ANTHROPIC_API_KEY
```

and

```
ANTHROPIC_AUTH_TOKEN
```

in the sandbox environment do not override them.

### Generate a long-lived token

For CI pipelines, scripts, or other environments where interactive browser login isn’t available, generate a one-year OAuth token with

```
claude setup-token
```

:

```
CLAUDE_CODE_OAUTH_TOKEN
```

environment variable wherever you want to authenticate:

[[Continue local sessions from any device with Remote Control - Claude Code Docs|Remote Control]]sessions.

[[Run Claude Code programmatically - Claude Code Docs#Start faster with bare mode|Bare mode]]does not read

```
CLAUDE_CODE_OAUTH_TOKEN
```

. If your script passes

```
--bare
```

, authenticate with

```
ANTHROPIC_API_KEY
```

or an

```
apiKeyHelper
```

instead.

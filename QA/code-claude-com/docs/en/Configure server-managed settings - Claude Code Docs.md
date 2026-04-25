---
title: Configure server-managed settings - Claude Code Docs
source_url: https://code.claude.com/docs/en/server-managed-settings
description: Centrally configure Claude Code for your organization through server-delivered
  settings, without requiring device management infrastructure.
---

Server-managed settings are available for

[Claude for Teams](https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=server_settings_teams#team-&-enterprise)and[Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=server_settings_enterprise)customers.

## Requirements

To use server-managed settings, you need:

- Claude for Teams or Claude for Enterprise plan
- Claude Code version 2.1.38 or later for Claude for Teams, or version 2.1.30 or later for Claude for Enterprise
- Network access to

  ```
  api.anthropic.com
  ```

## Choose between server-managed and endpoint-managed settings

Claude Code supports two approaches for centralized configuration. Server-managed settings deliver configuration from Anthropic’s servers.

[[Claude Code settings - Claude Code Docs#Settings files|Endpoint-managed settings]]are deployed directly to devices through native OS policies (macOS managed preferences, Windows registry) or managed settings files.

ApproachBest forSecurity modelServer-managed settingsOrganizations without MDM, or users on unmanaged devicesSettings delivered from Anthropic’s servers at authentication time

## Configure server-managed settings

Open the admin console

In

[Claude.ai](https://claude.ai), navigate to Admin Settings > Claude Code > Managed settings.

Define your settings

Add your configuration as JSON. All Hooks use the same format as in To configure the Because hooks execute shell commands, users see a

[[Claude Code settings - Claude Code Docs#Available settings|settings available in]]are supported, including

```
settings.json
```

[[Hooks reference - Claude Code Docs|hooks]],[[Environment variables - Claude Code Docs|environment variables]], and[[Configure permissions - Claude Code Docs#Managed-only settings|managed-only settings]]like

```
allowManagedPermissionRulesOnly
```

.This example enforces a permission deny list, prevents users from bypassing permissions, and restricts permission rules to those defined in managed settings:

```
settings.json
```

.This example runs an audit script after every file edit across the organization:[[Choose a permission mode - Claude Code Docs#Eliminate prompts with auto mode|auto mode]]classifier so it knows which repos, buckets, and domains your organization trusts:[[Configure server-managed settings - Claude Code Docs#Security approval dialogs|security approval dialog]]before they’re applied. See[[Configure auto mode - Claude Code Docs|Configure auto mode]]for how the

```
autoMode
```

entries affect what the classifier blocks and important warnings about the

```
allow
```

and

```
soft_deny
```

fields.

### Verify settings delivery

To confirm that settings are being applied, ask a user to restart Claude Code. If the configuration includes settings that trigger the

[[Configure server-managed settings - Claude Code Docs#Security approval dialogs|security approval dialog]], the user sees a prompt describing the managed settings on startup. You can also verify that managed permission rules are active by having a user run

```
/permissions
```

to view their effective permission rules.

### Access control

The following roles can manage server-managed settings:

- Primary Owner
- Owner

### Managed-only settings

Most

[[Claude Code settings - Claude Code Docs#Available settings|settings keys]]work in any scope. A handful of keys are only read from managed settings and have no effect when placed in user or project settings files. See

[[Configure permissions - Claude Code Docs#Managed-only settings|managed-only settings]]for the full list. Any setting not on that list can still be placed in managed settings and takes the highest precedence.

### Current limitations

Server-managed settings have the following limitations:

- Settings apply uniformly to all users in the organization. Per-group configurations are not yet supported.
- [[Connect Claude Code to tools via MCP - Claude Code Docs#Managed MCP configuration|MCP server configurations]]cannot be distributed through server-managed settings.

## Settings delivery

### Settings precedence

Server-managed settings and

[[Claude Code settings - Claude Code Docs#Settings files|endpoint-managed settings]]both occupy the highest tier in the Claude Code

[[Claude Code settings - Claude Code Docs#Settings precedence|settings hierarchy]]. No other settings level can override them, including command line arguments. Within the managed tier, the first source that delivers a non-empty configuration wins. Server-managed settings are checked first, then endpoint-managed settings. Sources do not merge: if server-managed settings deliver any keys at all, endpoint-managed settings are ignored entirely. If server-managed settings deliver nothing, endpoint-managed settings apply. If you clear your server-managed configuration in the admin console with the intent of falling back to an endpoint-managed plist or registry policy, be aware that

[[Configure server-managed settings - Claude Code Docs#Fetch and caching behavior|cached settings]]persist on client machines until the next successful fetch. Run

```
/status
```

to see which managed source is active.

### Fetch and caching behavior

Claude Code fetches settings from Anthropic’s servers at startup and polls for updates hourly during active sessions. First launch without cached settings:

- Claude Code fetches settings asynchronously
- If the fetch fails, Claude Code continues without managed settings
- There is a brief window before settings load where restrictions are not yet enforced

- Cached settings apply immediately at startup
- Claude Code fetches fresh settings in the background
- Cached settings persist through network failures

### Enforce fail-closed startup

By default, if the remote settings fetch fails at startup, the CLI continues without managed settings. For environments where this brief unenforced window is unacceptable, set

```
forceRemoteSettingsRefresh: true
```

in your managed settings.
When this setting is active, the CLI blocks at startup until remote settings are freshly fetched. If the fetch fails, the CLI exits rather than proceeding without the policy. This setting self-perpetuates: once delivered from the server, it is also cached locally so that subsequent startups enforce the same behavior even before the first successful fetch of a new session.
To enable this, add the key to your managed settings configuration:

```
api.anthropic.com
```

. If that endpoint is unreachable, the CLI exits at startup and users cannot start Claude Code.

### Security approval dialogs

Certain settings that could pose security risks require explicit user approval before being applied:

- Shell command settings: settings that execute shell commands
- Custom environment variables: variables not in the known safe allowlist
- Hook configurations: any hook definition

In non-interactive mode with the

```
-p
```

flag, Claude Code skips security dialogs and applies settings without user approval.

## Platform availability

Server-managed settings require a direct connection to

```
api.anthropic.com
```

and are not available when using third-party model providers:

- Amazon Bedrock
- Google Vertex AI
- Microsoft Foundry
- Custom API endpoints via

  ```
  ANTHROPIC_BASE_URL
  ```

  or[[LLM gateway configuration - Claude Code Docs|LLM gateways]]

## Audit logging

Audit log events for settings changes are available through the compliance API or audit log export. Contact your Anthropic account team for access. Audit events include the type of action performed, the account and device that performed the action, and references to the previous and new values.

## Security considerations

Server-managed settings provide centralized policy enforcement, but they operate as a client-side control. On unmanaged devices, users with admin or sudo access can modify the Claude Code binary, filesystem, or network configuration.

ScenarioBehaviorUser edits the cached settings fileTampered file applies at startup, but correct settings restore on the next server fetchUser deletes the cached settings fileFirst-launch behavior occurs: settings fetch asynchronously with a brief unenforced windowAPI is unavailableCached settings apply if available, otherwise managed settings are not enforced until the next successful fetch. With

```
forceRemoteSettingsRefresh: true
```

, the CLI exits instead of continuingUser authenticates with a different organizationSettings are not delivered for accounts outside the managed organizationUser sets a non-default

```
ANTHROPIC_BASE_URL
```

Server-managed settings are bypassed when using third-party API providers

[[Hooks reference - Claude Code Docs#ConfigChange|to log modifications or block unauthorized changes before they take effect. For stronger enforcement guarantees, use]]

```
ConfigChange
```

hooks

[[Claude Code settings - Claude Code Docs#Settings files|endpoint-managed settings]]on devices enrolled in an MDM solution.

## See also

Related pages for managing Claude Code configuration:

- [[Claude Code settings - Claude Code Docs|Settings]]: complete configuration reference including all available settings
- [[Claude Code settings - Claude Code Docs#Settings files|Endpoint-managed settings]]: managed settings deployed to devices by IT
- [[Authentication - Claude Code Docs|Authentication]]: set up user access to Claude Code
- [[Security - Claude Code Docs|Security]]: security safeguards and best practices

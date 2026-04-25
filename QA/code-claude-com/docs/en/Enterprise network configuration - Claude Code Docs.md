---
title: Enterprise network configuration - Claude Code Docs
source_url: https://code.claude.com/docs/en/network-config
description: Configure Claude Code for enterprise environments with proxy servers,
  custom Certificate Authorities (CA), and mutual Transport Layer Security (mTLS)
  authentica
---

All environment variables shown on this page can also be configured in

[[Claude Code settings - Claude Code Docs|.]]

```
settings.json
```

## Proxy configuration

### Environment variables

Claude Code respects standard proxy environment variables:

Claude Code does not support SOCKS proxies.

### Basic authentication

If your proxy requires basic authentication, include credentials in the proxy URL:

## CA certificate store

By default, Claude Code trusts both its bundled Mozilla CA certificates and your operating system’s certificate store. Enterprise TLS-inspection proxies such as CrowdStrike Falcon and Zscaler work without additional configuration when their root certificate is installed in the OS trust store.

System CA store integration requires the native Claude Code binary distribution. When running on the Node.js runtime, the system CA store is not merged automatically. In that case, set

```
NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

to trust an enterprise root CA.

```
CLAUDE_CODE_CERT_STORE
```

accepts a comma-separated list of sources. Recognized values are

```
bundled
```

for the Mozilla CA set shipped with Claude Code and

```
system
```

for the operating system trust store. The default is

```
bundled,system
```

.
To trust only the bundled Mozilla CA set:

```
CLAUDE_CODE_CERT_STORE
```

has no dedicated

```
settings.json
```

schema key. Set it via the

```
env
```

block in

```
~/.claude/settings.json
```

or directly in the process environment.

## Custom CA certificates

If your enterprise environment uses a custom CA, configure Claude Code to trust it directly:

## mTLS authentication

For enterprise environments requiring client certificate authentication:

## Network access requirements

Claude Code requires access to the following URLs. Allowlist these in your proxy configuration and firewall rules, especially in containerized or restricted network environments.

URLRequired for

```
api.anthropic.com
```

Claude API requests

```
claude.ai
```

claude.ai account authentication

```
platform.claude.com
```

Anthropic Console account authentication

```
downloads.claude.ai
```

Plugin executable downloads; native installer and native auto-updater

```
storage.googleapis.com
```

Native installer and native auto-updater on versions prior to 2.1.116

```
bridge.claudeusercontent.com
```

```
downloads.claude.ai
```

or

```
storage.googleapis.com
```

.
When using

[[Claude Code on Amazon Bedrock - Claude Code Docs|Amazon Bedrock]],

[[Claude Code on Google Vertex AI - Claude Code Docs|Google Vertex AI]], or

[[Claude Code on Microsoft Foundry - Claude Code Docs|Microsoft Foundry]], model traffic and authentication go to your provider instead of

```
api.anthropic.com
```

,

```
claude.ai
```

, or

```
platform.claude.com
```

. The WebFetch tool still calls

```
api.anthropic.com
```

for its

[[Data usage - Claude Code Docs#WebFetch domain safety check|domain safety check]]unless you set

```
skipWebFetchPreflight: true
```

in

[[Claude Code settings - Claude Code Docs|settings]].

[[Use Claude Code on the web - Claude Code Docs|Claude Code on the web]]and

[[Code Review - Claude Code Docs|Code Review]]connect to your repositories from Anthropic-managed infrastructure. If your GitHub Enterprise Cloud organization restricts access by IP address, enable

[IP allow list inheritance for installed GitHub Apps](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). The Claude GitHub App registers its IP ranges, so enabling this setting allows access without manual configuration. To

[add the ranges to your allow list manually](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address)instead, or to configure other firewalls, see the

[Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses). For self-hosted

[[Claude Code with GitHub Enterprise Server - Claude Code Docs|GitHub Enterprise Server]]instances behind a firewall, allowlist the same

[Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses)so Anthropic infrastructure can reach your GHES host to clone repositories and post review comments.

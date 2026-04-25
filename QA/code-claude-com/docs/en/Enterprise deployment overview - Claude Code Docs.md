---
title: Enterprise deployment overview - Claude Code Docs
source_url: https://code.claude.com/docs/en/third-party-integrations
description: Learn how Claude Code can integrate with various third-party services
  and infrastructure to meet enterprise deployment requirements.
---

## Compare deployment options

For most organizations, Claude for Teams or Claude for Enterprise provides the best experience. Team members get access to both Claude Code and Claude on the web with a single subscription, centralized billing, and no infrastructure setup required. Claude for Teams is self-service and includes collaboration features, admin tools, and billing management. Best for smaller teams that need to get started quickly. Claude for Enterprise adds SSO and domain capture, role-based permissions, compliance API access, and managed policy settings for deploying organization-wide Claude Code configurations. Best for larger organizations with security and compliance requirements. Learn more about

[Team plans](https://support.claude.com/en/articles/9266767-what-is-the-team-plan)and

[Enterprise plans](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan). If your organization has specific infrastructure requirements, compare the options below:

FeatureClaude for Teams/EnterpriseAnthropic ConsoleAmazon BedrockGoogle Vertex AIMicrosoft FoundryBest forMost organizations (recommended)Individual developersAWS-native deploymentsGCP-native deploymentsAzure-native deploymentsBillingTeams: $150/seat (Premium) with PAYG available

Enterprise:

PAYGPAYG through AWSPAYG through GCPPAYG through AzureRegionsSupported

[countries](https://www.anthropic.com/supported-countries)[regions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)[regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)[regions](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)

## Configure proxies and gateways

Most organizations can use a cloud provider directly without additional configuration. However, you may need to configure a corporate proxy or LLM gateway if your organization has specific network or management requirements. These are different configurations that can be used together:

- Corporate proxy: Routes traffic through an HTTP/HTTPS proxy. Use this if your organization requires all outbound traffic to pass through a proxy server for security monitoring, compliance, or network policy enforcement. Configure with the

  ```
  HTTPS_PROXY
  ```

  or

  ```
  HTTP_PROXY
  ```

  environment variables. Learn more in[[Enterprise network configuration - Claude Code Docs|Enterprise network configuration]].
- LLM Gateway: A service that sits between Claude Code and the cloud provider to handle authentication and routing. Use this if you need centralized usage tracking across teams, custom rate limiting or budgets, or centralized authentication management. Configure with the

  ```
  ANTHROPIC_BASE_URL
  ```

  ,

  ```
  ANTHROPIC_BEDROCK_BASE_URL
  ```

  , or

  ```
  ANTHROPIC_VERTEX_BASE_URL
  ```

  environment variables. Learn more in[[LLM gateway configuration - Claude Code Docs|LLM gateway configuration]].

```
.bashrc
```

,

```
.zshrc
```

). See

[[Claude Code settings - Claude Code Docs|Settings]]for other configuration methods.

### Amazon Bedrock

- Corporate proxy
- LLM Gateway

Route Bedrock traffic through your corporate proxy by setting the following

[[Environment variables - Claude Code Docs|environment variables]]:

### Microsoft Foundry

- Corporate proxy
- LLM Gateway

Route Foundry traffic through your corporate proxy by setting the following

[[Environment variables - Claude Code Docs|environment variables]]:

### Google Vertex AI

- Corporate proxy
- LLM Gateway

Route Vertex AI traffic through your corporate proxy by setting the following

[[Environment variables - Claude Code Docs|environment variables]]:

## Best practices for organizations

### Invest in documentation and memory

We strongly recommend investing in documentation so that Claude Code understands your codebase. Organizations can deploy CLAUDE.md files at multiple levels:

- Organization-wide: Deploy to system directories like

  ```
  /Library/Application Support/ClaudeCode/CLAUDE.md
  ```

  (macOS) for company-wide standards
- Repository-level: Create

  ```
  CLAUDE.md
  ```

  files in repository roots containing project architecture, build commands, and contribution guidelines. Check these into source control so all users benefit

[[How Claude remembers your project - Claude Code Docs|Memory and CLAUDE.md files]].

### Simplify deployment

If you have a custom development environment, we find that creating a “one click” way to install Claude Code is key to growing adoption across an organization.

### Start with guided usage

Encourage new users to try Claude Code for codebase Q&A, or on smaller bug fixes or feature requests. Ask Claude Code to make a plan. Check Claude’s suggestions and give feedback if it’s off-track. Over time, as users understand this new paradigm better, then they’ll be more effective at letting Claude Code run more agentically.

### Pin model versions for cloud providers

If you deploy through

[[Claude Code on Amazon Bedrock - Claude Code Docs|Bedrock]],

[[Claude Code on Google Vertex AI - Claude Code Docs|Vertex AI]], or

[[Claude Code on Microsoft Foundry - Claude Code Docs|Foundry]], pin specific model versions using

```
ANTHROPIC_DEFAULT_OPUS_MODEL
```

,

```
ANTHROPIC_DEFAULT_SONNET_MODEL
```

, and

```
ANTHROPIC_DEFAULT_HAIKU_MODEL
```

. Without pinning, model aliases resolve to the latest version, which may not yet be enabled in your account when Anthropic releases an update. Pinning lets you control when your users move to a new model. See

[[Model configuration - Claude Code Docs#Pin models for third-party deployments|Model configuration]]for what each provider does when the latest version is unavailable.

### Configure security policies

Security teams can configure managed permissions for what Claude Code is and is not allowed to do, which cannot be overwritten by local configuration.

[[Security - Claude Code Docs|Learn more]].

### Leverage MCP for integrations

MCP is a great way to give Claude Code more information, such as connecting to ticket management systems or error logs. We recommend that one central team configures MCP servers and checks a

```
.mcp.json
```

configuration into the codebase so that all users benefit.

[[Connect Claude Code to tools via MCP - Claude Code Docs|Learn more]]. At Anthropic, we trust Claude Code to power development across every Anthropic codebase. We hope you enjoy using Claude Code as much as we do.

## Next steps

Once you’ve chosen a deployment option and configured access for your team:

- Roll out to your team: Share installation instructions and have team members [[Advanced setup - Claude Code Docs|install Claude Code]]and authenticate with their credentials.
- Set up shared configuration: Create a [[How Claude remembers your project - Claude Code Docs|CLAUDE.md file]]in your repositories to help Claude Code understand your codebase and coding standards.
- Configure permissions: Review [[Security - Claude Code Docs|security settings]]to define what Claude Code can and cannot do in your environment.

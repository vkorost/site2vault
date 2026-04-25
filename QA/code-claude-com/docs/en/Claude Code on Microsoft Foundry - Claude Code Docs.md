---
title: Claude Code on Microsoft Foundry - Claude Code Docs
source_url: https://code.claude.com/docs/en/microsoft-foundry
description: Learn about configuring Claude Code through Microsoft Foundry, including
  setup, configuration, and troubleshooting.
---

## Prerequisites

Before configuring Claude Code with Microsoft Foundry, ensure you have:

- An Azure subscription with access to Microsoft Foundry
- RBAC permissions to create Microsoft Foundry resources and deployments
- Azure CLI installed and configured (optional - only needed if you don’t have another mechanism for getting credentials)

If you are deploying Claude Code to multiple users,

[[Claude Code on Microsoft Foundry - Claude Code Docs#4. Pin model versions|pin your model versions]]to prevent breakage when Anthropic releases new models.

## Setup

### 1. Provision Microsoft Foundry resource

First, create a Claude resource in Azure:

- Navigate to the [Microsoft Foundry portal](https://ai.azure.com/)
- Create a new resource, noting your resource name
- Create deployments for the Claude models:
  - Claude Opus
  - Claude Sonnet
  - Claude Haiku

### 2. Configure Azure credentials

Claude Code supports two authentication methods for Microsoft Foundry. Choose the method that best fits your security requirements. Option A: API key authentication

- Navigate to your resource in the Microsoft Foundry portal
- Go to the Endpoints and keys section
- Copy API Key
- Set the environment variable:

```
ANTHROPIC_FOUNDRY_API_KEY
```

is not set, Claude Code automatically uses the Azure SDK

[default credential chain](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview). This supports a variety of methods for authenticating local and remote workloads. On local environments, you commonly may use the Azure CLI:

When using Microsoft Foundry, the

```
/login
```

and

```
/logout
```

commands are disabled since authentication is handled through Azure credentials.

### 3. Configure Claude Code

Set the following environment variables to enable Microsoft Foundry:

### 4. Pin model versions

Set the model variables to match the deployment names you created in step 1. Without

```
ANTHROPIC_DEFAULT_OPUS_MODEL
```

, the

```
opus
```

alias on Foundry resolves to Opus 4.6. Set it to the Opus 4.7 ID to use the latest model:

[Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See

[[Model configuration - Claude Code Docs#Pin models for third-party deployments|Model configuration]]for the full list of environment variables.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)is enabled automatically. To request a 1-hour cache TTL instead of the 5-minute default, set the following variable; cache writes with a 1-hour TTL are billed at a higher rate:

## Azure RBAC configuration

The

```
Azure AI User
```

and

```
Cognitive Services User
```

default roles include all required permissions for invoking Claude models.
For more restrictive permissions, create a custom role with the following:

[Microsoft Foundry RBAC documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Troubleshooting

If you receive an error “Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed”:

- Configure Entra ID on the environment, or set

  ```
  ANTHROPIC_FOUNDRY_API_KEY
  ```

  .

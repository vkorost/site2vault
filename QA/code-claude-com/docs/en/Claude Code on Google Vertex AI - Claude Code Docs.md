---
title: Claude Code on Google Vertex AI - Claude Code Docs
source_url: https://code.claude.com/docs/en/google-vertex-ai
description: Learn about configuring Claude Code through Google Vertex AI, including
  setup, IAM configuration, and troubleshooting.
---

## Prerequisites

Before configuring Claude Code with Vertex AI, ensure you have:

- A Google Cloud Platform (GCP) account with billing enabled
- A GCP project with Vertex AI API enabled
- Access to desired Claude models (for example, Claude Sonnet 4.6)
- Google Cloud SDK (

  ```
  gcloud
  ```

  ) installed and configured
- Quota allocated in desired GCP region

[[Claude Code on Google Vertex AI - Claude Code Docs#Sign in with Vertex AI|Sign in with Vertex AI]]below. To deploy Claude Code across a team, use the

[[Claude Code on Google Vertex AI - Claude Code Docs#Set up manually|manual setup]]steps and

[[Claude Code on Google Vertex AI - Claude Code Docs#5. Pin model versions|pin your model versions]]before rolling out.

## Sign in with Vertex AI

If you have Google Cloud credentials and want to start using Claude Code through Vertex AI, the login wizard walks you through it. You complete the GCP-side prerequisites once per project; the wizard handles the Claude Code side.

The Vertex AI setup wizard requires Claude Code v2.1.98 or later. Run

```
claude --version
```

to check.

Enable Claude models in your GCP project

[[Claude Code on Google Vertex AI - Claude Code Docs#1. Enable Vertex AI API|Enable the Vertex AI API]]for your project, then request access to the Claude models you want in the

[Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden). See

[[Claude Code on Google Vertex AI - Claude Code Docs#IAM configuration|IAM configuration]]for the permissions your account needs.

Start Claude Code and choose Vertex AI

Run

```
claude
```

. At the login prompt, select 3rd-party platform, then Google Vertex AI.

Follow the wizard prompts

Choose how you authenticate to Google Cloud: Application Default Credentials from

```
gcloud
```

, a service account key file, or credentials already in your environment. The wizard detects your project and region, verifies which Claude models your project can invoke, and lets you pin them. It saves the result to the

```
env
```

block of your [[Claude Code settings - Claude Code Docs|user settings file]], so you don’t need to export environment variables yourself.

```
/setup-vertex
```

any time to reopen the wizard and change your credentials, project, region, or model pins.

## Region configuration

Claude Code supports Vertex AI

[global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), multi-region, and regional endpoints. Set

```
CLOUD_ML_REGION
```

to

```
global
```

, a multi-region location such as

```
eu
```

or

```
us
```

, or a specific region such as

```
us-east5
```

. Claude Code selects the correct Vertex AI hostname for each form, including the

```
aiplatform.eu.rep.googleapis.com
```

and

```
aiplatform.us.rep.googleapis.com
```

hosts for multi-region locations.

Vertex AI may not support the Claude Code default models on every endpoint type. Model availability varies across

[specific regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), multi-region locations, and[global endpoints](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). You may need to switch to a supported location or specify a supported model.

## Set up manually

To configure Vertex AI through environment variables instead of the wizard, for example in CI or a scripted enterprise rollout, follow the steps below.

### 1. Enable Vertex AI API

Enable the Vertex AI API in your GCP project:

### 2. Request model access

Request access to Claude models in Vertex AI:

- Navigate to the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
- Search for “Claude” models
- Request access to desired Claude models (for example, Claude Sonnet 4.6)
- Wait for approval (may take 24-48 hours)

### 3. Configure GCP credentials

Claude Code uses standard Google Cloud authentication. For more information, see

[Google Cloud authentication documentation](https://cloud.google.com/docs/authentication).

When authenticating, Claude Code will automatically use the project ID from the

```
ANTHROPIC_VERTEX_PROJECT_ID
```

environment variable. To override this, set one of these environment variables:

```
GCLOUD_PROJECT
```

,

```
GOOGLE_CLOUD_PROJECT
```

, or

```
GOOGLE_APPLICATION_CREDENTIALS
```

.

### 4. Configure Claude Code

Set the following environment variables:

```
VERTEX_REGION_CLAUDE_*
```

variable. See the

[[Environment variables - Claude Code Docs|Environment variables reference]]for the full list. Check

[Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)to determine which models support global endpoints versus regional only.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)is enabled automatically. To disable it, set

```
DISABLE_PROMPT_CACHING=1
```

. To request a 1-hour cache TTL instead of the 5-minute default, set

```
ENABLE_PROMPT_CACHING_1H=1
```

; cache writes with a 1-hour TTL are billed at a higher rate. For heightened rate limits, contact Google Cloud support. When using Vertex AI, the

```
/login
```

and

```
/logout
```

commands are disabled since authentication is handled through Google Cloud credentials.

[[Connect Claude Code to tools via MCP - Claude Code Docs#Scale with MCP Tool Search|MCP tool search]]is disabled by default on Vertex AI because the endpoint does not accept the required beta header. All MCP tool definitions load upfront instead. To opt in, set

```
ENABLE_TOOL_SEARCH=true
```

.

### 5. Pin model versions

Set these environment variables to specific Vertex AI model IDs. Without

```
ANTHROPIC_DEFAULT_OPUS_MODEL
```

, the

```
opus
```

alias on Vertex resolves to Opus 4.6. Set it to the Opus 4.7 ID to use the latest model:

[Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See

[[Model configuration - Claude Code Docs#Pin models for third-party deployments|Model configuration]]for the full list of environment variables. Claude Code uses these default models when no pinning variables are set:

Model typeDefault valuePrimary model

```
claude-sonnet-4-5@20250929
```

Small/fast model

```
claude-haiku-4-5@20251001
```

## Startup model checks

When Claude Code starts with Vertex AI configured, it verifies that the models it intends to use are accessible in your project. This check requires Claude Code v2.1.98 or later. If you have pinned a model version that is older than the current Claude Code default, and your project can invoke the newer version, Claude Code prompts you to update the pin. Accepting writes the new model ID to your

[[Claude Code settings - Claude Code Docs|user settings file]]and restarts Claude Code. Declining is remembered until the next default version change. If you have not pinned a model and the current default is unavailable in your project, Claude Code falls back to the previous version for the current session and shows a notice. The fallback is not persisted. Enable the newer model in

[Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)or

[[Claude Code on Google Vertex AI - Claude Code Docs#5. Pin model versions|pin a version]]to make the choice permanent.

## IAM configuration

Assign the required IAM permissions: The

```
roles/aiplatform.user
```

role includes the required permissions:

- ```
  aiplatform.endpoints.predict
  ```

  - Required for model invocation and token counting

[Vertex IAM documentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

Create a dedicated GCP project for Claude Code to simplify cost tracking and access control.

## 1M token context window

Claude Opus 4.7, Opus 4.6, and Sonnet 4.6 support the

[1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)on Vertex AI. Claude Code automatically enables the extended context window when you select a 1M model variant. The

[[Claude Code on Google Vertex AI - Claude Code Docs#Sign in with Vertex AI|setup wizard]]offers a 1M context option when it pins models. To enable it for a manually pinned model instead, append

```
[1m]
```

to the model ID. See

[[Model configuration - Claude Code Docs#Pin models for third-party deployments|Pin models for third-party deployments]]for details.

## Troubleshooting

If you encounter quota issues:

- Check current quotas or request quota increase through [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

- Confirm model is Enabled in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
- Verify the model is available in the location you specified. Some models are offered only on

  ```
  global
  ```

  or multi-region locations such as

  ```
  eu
  ```

  and

  ```
  us
  ```

  , not in specific regions
- If using

  ```
  CLOUD_ML_REGION=global
  ```

  , check that your models support global endpoints in[Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)under “Supported features”. For models that don’t support global endpoints, either:
  - Specify a supported model via

    ```
    ANTHROPIC_MODEL
    ```

    or

    ```
    ANTHROPIC_DEFAULT_HAIKU_MODEL
    ```

    , or
  - Set a region or multi-region location using

    ```
    VERTEX_REGION_<MODEL_NAME>
    ```

    environment variables
- Specify a supported model via

- For regional endpoints, ensure the primary model and small/fast model are supported in your selected region
- Consider switching to

  ```
  CLOUD_ML_REGION=global
  ```

  for better availability

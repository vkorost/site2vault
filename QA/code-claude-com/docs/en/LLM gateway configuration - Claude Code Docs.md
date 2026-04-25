---
title: LLM gateway configuration - Claude Code Docs
source_url: https://code.claude.com/docs/en/llm-gateway
description: Learn how to configure Claude Code to work with LLM gateway solutions.
  Covers gateway requirements, authentication configuration, model selection, and
  provider-
---

- Centralized authentication - Single point for API key management
- Usage tracking - Monitor usage across teams and projects
- Cost controls - Implement budgets and rate limits
- Audit logging - Track all model interactions for compliance
- Model routing - Switch between providers without code changes

## Gateway requirements

For an LLM gateway to work with Claude Code, it must meet the following requirements: API format The gateway must expose to clients at least one of the following API formats:

- Anthropic Messages:

  ```
  /v1/messages
  ```

  ,

  ```
  /v1/messages/count_tokens
  ```

  - Must forward request headers:

    ```
    anthropic-beta
    ```

    ,

    ```
    anthropic-version
    ```
- Must forward request headers:
- Bedrock InvokeModel:

  ```
  /invoke
  ```

  ,

  ```
  /invoke-with-response-stream
  ```

  - Must preserve request body fields:

    ```
    anthropic_beta
    ```

    ,

    ```
    anthropic_version
    ```
- Must preserve request body fields:
- Vertex rawPredict:

  ```
  :rawPredict
  ```

  ,

  ```
  :streamRawPredict
  ```

  ,

  ```
  /count-tokens:rawPredict
  ```

  - Must forward request headers:

    ```
    anthropic-beta
    ```

    ,

    ```
    anthropic-version
    ```
- Must forward request headers:

Claude Code determines which features to enable based on the API format. When using the Anthropic Messages format with Bedrock or Vertex, you may need to set environment variable

```
CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1
```

.

HeaderDescription

```
X-Claude-Code-Session-Id
```

A unique identifier for the current Claude Code session. Proxies can use this to aggregate all API requests from a single session without parsing the request body.

## Configuration

### Model selection

By default, Claude Code will use standard model names for the selected API format. If you have configured custom model names in your gateway, use the environment variables documented in

[[Model configuration - Claude Code Docs|Model configuration]]to match your custom names.

## LiteLLM configuration

### Prerequisites

- Claude Code updated to the latest version
- LiteLLM Proxy Server deployed and accessible
- Access to Claude models through your chosen provider

### Basic LiteLLM setup

Configure Claude Code:

#### Authentication methods

##### Static API key

Simplest method using a fixed API key:

```
Authorization
```

header.

##### Dynamic API key with helper

For rotating keys or per-user authentication:

- Create an API key helper script:

- Configure Claude Code settings to use the helper:

- Set token refresh interval:

```
Authorization
```

and

```
X-Api-Key
```

headers. The

```
apiKeyHelper
```

has lower precedence than

```
ANTHROPIC_AUTH_TOKEN
```

or

```
ANTHROPIC_API_KEY
```

.

#### Unified endpoint (recommended)

Using LiteLLM’s

[Anthropic format endpoint](https://docs.litellm.ai/docs/anthropic_unified):

- Load balancing
- Fallbacks
- Consistent support for cost tracking and end-user tracking

#### Provider-specific pass-through endpoints (alternative)

##### Claude API through LiteLLM

Using

[pass-through endpoint](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

##### Amazon Bedrock through LiteLLM

Using

[pass-through endpoint](https://docs.litellm.ai/docs/pass_through/bedrock):

##### Google Vertex AI through LiteLLM

Using

[pass-through endpoint](https://docs.litellm.ai/docs/pass_through/vertex_ai):

[LiteLLM documentation](https://docs.litellm.ai/).

---
title: Claude Code on Amazon Bedrock - Claude Code Docs
source_url: https://code.claude.com/docs/en/amazon-bedrock
description: Learn about configuring Claude Code through Amazon Bedrock, including
  setup, IAM configuration, and troubleshooting.
---

## Prerequisites

Before configuring Claude Code with Bedrock, ensure you have:

- An AWS account with Bedrock access enabled
- Access to desired Claude models (for example, Claude Sonnet 4.6) in Bedrock
- AWS CLI installed and configured (optional - only needed if you don’t have another mechanism for getting credentials)
- Appropriate IAM permissions

[[Claude Code on Amazon Bedrock - Claude Code Docs#Sign in with Bedrock|Sign in with Bedrock]]below. To deploy Claude Code across a team, use the

[[Claude Code on Amazon Bedrock - Claude Code Docs#Set up manually|manual setup]]steps and

[[Claude Code on Amazon Bedrock - Claude Code Docs#4. Pin model versions|pin your model versions]]before rolling out.

## Sign in with Bedrock

If you have AWS credentials and want to start using Claude Code through Bedrock, the login wizard walks you through it. You complete the AWS-side prerequisites once per account; the wizard handles the Claude Code side.

Enable Anthropic models in your AWS account

In the

[Amazon Bedrock console](https://console.aws.amazon.com/bedrock/), open the Model catalog, select an Anthropic model, and submit the use case form. Access is granted immediately after submission. See[[Claude Code on Amazon Bedrock - Claude Code Docs#1. Submit use case details|Submit use case details]]for AWS Organizations and[[Claude Code on Amazon Bedrock - Claude Code Docs#IAM configuration|IAM configuration]]for the permissions your role needs.

Start Claude Code and choose Bedrock

Run

```
claude
```

. At the login prompt, select 3rd-party platform, then Amazon Bedrock.

Follow the wizard prompts

Choose how you authenticate to AWS: an AWS profile detected from your

```
~/.aws
```

directory, a Bedrock API key, an access key and secret, or credentials already in your environment. The wizard picks up your region, verifies which Claude models your account can invoke, and lets you pin them. It saves the result to the

```
env
```

block of your [[Claude Code settings - Claude Code Docs|user settings file]], so you don’t need to export environment variables yourself.

```
/setup-bedrock
```

any time to reopen the wizard and change your credentials, region, or model pins.

## Set up manually

To configure Bedrock through environment variables instead of the wizard, for example in CI or a scripted enterprise rollout, follow the steps below.

### 1. Submit use case details

First-time users of Anthropic models are required to submit use case details before invoking a model. This is done once per AWS account.

- Ensure you have the right IAM permissions described below
- Navigate to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/)
- Select an Anthropic model from the Model catalog
- Complete the use case form. Access is granted immediately after submission.

[. This call requires the](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html)

```
PutUseCaseForModelAccess
```

API

```
bedrock:PutUseCaseForModelAccess
```

IAM permission. Approval extends to child accounts automatically.

### 2. Configure AWS credentials

Claude Code uses the default AWS SDK credential chain. Set up your credentials using one of these methods: Option A: AWS CLI configuration

[Learn more](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html)about

```
aws login
```

.
Option E: Bedrock API keys

[Learn more about Bedrock API keys](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Advanced credential configuration

Claude Code supports automatic credential refresh for AWS SSO and corporate identity providers. Add these settings to your Claude Code settings file (see

[[Claude Code settings - Claude Code Docs|Settings]]for file locations). When Claude Code detects that your AWS credentials are expired (either locally based on their timestamp or when Bedrock returns a credential error), it will automatically run your configured

```
awsAuthRefresh
```

and/or

```
awsCredentialExport
```

commands to obtain new credentials before retrying the request.

##### Example configuration

##### Configuration settings explained

```
awsAuthRefresh
```

: Use this for commands that modify the

```
.aws
```

directory, such as updating credentials, SSO cache, or config files. The command’s output is displayed to the user, but interactive input isn’t supported. This works well for browser-based SSO flows where the CLI displays a URL or code and you complete authentication in the browser.

```
awsCredentialExport
```

: Only use this if you can’t modify

```
.aws
```

and must directly return credentials. Output is captured silently and not shown to the user. The command must output JSON in this format:

### 3. Configure Claude Code

Set the following environment variables to enable Bedrock:

- ```
  AWS_REGION
  ```

  is a required environment variable. Claude Code does not read from the

  ```
  .aws
  ```

  config file for this setting.
- When using Bedrock, the

  ```
  /login
  ```

  and

  ```
  /logout
  ```

  commands are disabled since authentication is handled through AWS credentials.
- You can use settings files for environment variables like

  ```
  AWS_PROFILE
  ```

  that you don’t want to leak to other processes. See[[Claude Code settings - Claude Code Docs|Settings]]for more information.

### 4. Pin model versions

Set these environment variables to specific Bedrock model IDs. Without

```
ANTHROPIC_DEFAULT_OPUS_MODEL
```

, the

```
opus
```

alias on Bedrock resolves to Opus 4.6. Set it to the Opus 4.7 ID to use the latest model:

```
us.
```

prefix). If you use a different region prefix or application inference profiles, adjust accordingly. For current and legacy model IDs, see

[Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See

[[Model configuration - Claude Code Docs#Pin models for third-party deployments|Model configuration]]for the full list of environment variables. Claude Code uses these default models when no pinning variables are set:

Model typeDefault valuePrimary model

```
us.anthropic.claude-sonnet-4-5-20250929-v1:0
```

Small/fast model

```
us.anthropic.claude-haiku-4-5-20251001-v1:0
```

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)may not be available in all regions. Cache writes with a 1-hour TTL are billed at a higher rate than 5-minute writes.

#### Map each model version to an inference profile

The

```
ANTHROPIC_DEFAULT_*_MODEL
```

environment variables configure one inference profile per model family. If your organization needs to expose several versions of the same family in the

```
/model
```

picker, each routed to its own application inference profile ARN, use the

```
modelOverrides
```

setting in your

[[Claude Code settings - Claude Code Docs#Settings files|settings file]]instead. This example maps four Opus versions to distinct ARNs so users can switch between them without bypassing your organization’s inference profiles:

```
/model
```

, Claude Code calls Bedrock with the mapped ARN. Versions without an override fall back to the built-in Bedrock model ID or any matching inference profile discovered at startup. See

[[Model configuration - Claude Code Docs#Override model IDs per version|Override model IDs per version]]for details on how overrides interact with

```
availableModels
```

and other model settings.

## Startup model checks

When Claude Code starts with Bedrock configured, it verifies that the models it intends to use are accessible in your account. This check requires Claude Code v2.1.94 or later. If you have pinned a model version that is older than the current Claude Code default, and your account can invoke the newer version, Claude Code prompts you to update the pin. Accepting writes the new model ID to your

[[Claude Code settings - Claude Code Docs|user settings file]]and restarts Claude Code. Declining is remembered until the next default version change. Pins that point to an

[[Claude Code on Amazon Bedrock - Claude Code Docs#Map each model version to an inference profile|application inference profile ARN]]are skipped, since those are managed by your administrator. If you have not pinned a model and the current default is unavailable in your account, Claude Code falls back to the previous version for the current session and shows a notice. The fallback is not persisted. Enable the newer model in your Bedrock account or

[[Claude Code on Amazon Bedrock - Claude Code Docs#4. Pin model versions|pin a version]]to make the choice permanent.

## IAM configuration

Create an IAM policy with the required permissions for Claude Code:

[Bedrock IAM documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

Create a dedicated AWS account for Claude Code to simplify cost tracking and access control.

## 1M token context window

Claude Opus 4.7, Opus 4.6, and Sonnet 4.6 support the

[1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)on Amazon Bedrock. Claude Code automatically enables the extended context window when you select a 1M model variant. The

[[Claude Code on Amazon Bedrock - Claude Code Docs#Sign in with Bedrock|setup wizard]]offers a 1M context option when it pins models. To enable it for a manually pinned model instead, append

```
[1m]
```

to the model ID. See

[[Model configuration - Claude Code Docs#Pin models for third-party deployments|Pin models for third-party deployments]]for details.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)let you implement content filtering for Claude Code. Create a Guardrail in the

[Amazon Bedrock console](https://console.aws.amazon.com/bedrock/), publish a version, then add the Guardrail headers to your

[[Claude Code settings - Claude Code Docs|settings file]]. Enable Cross-Region inference on your Guardrail if you’re using cross-region inference profiles. Example configuration:

## Use the Mantle endpoint

Mantle is an Amazon Bedrock endpoint that serves Claude models through the native Anthropic API shape rather than the Bedrock Invoke API. It uses the same AWS credentials, IAM permissions, and

```
awsAuthRefresh
```

configuration described earlier on this page.

Mantle requires Claude Code v2.1.94 or later. Run

```
claude --version
```

to check.

### Enable Mantle

With AWS credentials already configured, set

```
CLAUDE_CODE_USE_MANTLE
```

to route requests to the Mantle endpoint:

```
AWS_REGION
```

. To override it for a custom endpoint or gateway, set

```
ANTHROPIC_BEDROCK_MANTLE_BASE_URL
```

.
Run

```
/status
```

inside Claude Code to confirm. The provider line shows

```
Amazon Bedrock (Mantle)
```

when Mantle is active.

### Select a Mantle model

Mantle uses model IDs prefixed with

```
anthropic.
```

and without a version suffix, for example

```
anthropic.claude-haiku-4-5
```

. The models available to your account depend on what your organization has been granted; additional model IDs are listed in your onboarding materials from AWS. Contact your AWS account team to request access to allowlisted models.
Set the model with the

```
--model
```

flag or with

```
/model
```

inside Claude Code:

### Run Mantle alongside the Invoke API

The models available to you on Mantle may not include every model you use today. Setting both

```
CLAUDE_CODE_USE_BEDROCK
```

and

```
CLAUDE_CODE_USE_MANTLE
```

lets Claude Code call both endpoints from the same session. Model IDs that match the Mantle format are routed to Mantle, and all other model IDs go to the Bedrock Invoke API.

```
/model
```

picker, list its ID in

```
availableModels
```

in your

[[Claude Code settings - Claude Code Docs|settings file]]. This setting also restricts the picker to the listed entries, so include every alias you want to keep available:

```
anthropic.
```

prefix are added as custom picker options and routed to Mantle. Replace

```
anthropic.claude-haiku-4-5
```

with the model ID your account has been granted. See

[[Model configuration - Claude Code Docs#Restrict model selection|Restrict model selection]]for how

```
availableModels
```

interacts with other model settings.
When both providers are active,

```
/status
```

shows

```
Amazon Bedrock + Amazon Bedrock (Mantle)
```

.

### Route Mantle through a gateway

If your organization routes model traffic through a centralized

[[LLM gateway configuration - Claude Code Docs|LLM gateway]]that injects AWS credentials server-side, disable client-side authentication so Claude Code sends requests without SigV4 signatures or

```
x-api-key
```

headers:

### Mantle environment variables

These variables are specific to the Mantle endpoint. See

[[Environment variables - Claude Code Docs|Environment variables]]for the full list.

VariablePurpose

```
CLAUDE_CODE_USE_MANTLE
```

Enable the Mantle endpoint. Set to

```
1
```

or

```
true
```

.

```
ANTHROPIC_BEDROCK_MANTLE_BASE_URL
```

Override the default Mantle endpoint URL

```
CLAUDE_CODE_SKIP_MANTLE_AUTH
```

Skip client-side authentication for proxy setups

```
ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION
```

Override AWS region for the Haiku-class model (shared with Bedrock)

## Troubleshooting

### Authentication loop with SSO and corporate proxies

If browser tabs spawn repeatedly when using AWS SSO, remove the

```
awsAuthRefresh
```

setting from your

[[Claude Code settings - Claude Code Docs|settings file]]. This can occur when corporate VPNs or TLS inspection proxies interrupt the SSO browser flow. Claude Code treats the interrupted connection as an authentication failure, re-runs

```
awsAuthRefresh
```

, and loops indefinitely.
If your network environment interferes with automatic browser-based SSO flows, use

```
aws sso login
```

manually before starting Claude Code instead of relying on

```
awsAuthRefresh
```

.

### Region issues

If you encounter region issues:

- Check model availability:

  ```
  aws bedrock list-inference-profiles --region your-region
  ```
- Switch to a supported region:

  ```
  export AWS_REGION=us-east-1
  ```
- Consider using inference profiles for cross-region access

- Specify the model as an [inference profile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)ID

[Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)and does not support the Converse API.

### Mantle endpoint errors

If

```
/status
```

does not show

```
Amazon Bedrock (Mantle)
```

after you set

```
CLAUDE_CODE_USE_MANTLE
```

, the variable is not reaching the process. Confirm it is exported in the shell where you launched

```
claude
```

, or set it in the

```
env
```

block of your

[[Claude Code settings - Claude Code Docs|settings file]]. A

```
403
```

from the Mantle endpoint with valid credentials means your AWS account has not been granted access to the model you requested. Contact your AWS account team to request access.
A

```
400
```

that names the model ID means that model is not served on Mantle. Mantle has its own model lineup separate from the standard Bedrock catalog, so inference profile IDs such as

```
us.anthropic.claude-sonnet-4-6
```

will not work. Use a Mantle-format ID, or enable

[[Claude Code on Amazon Bedrock - Claude Code Docs#Run Mantle alongside the Invoke API|both endpoints]]so Claude Code routes each request to the endpoint where the model is available.

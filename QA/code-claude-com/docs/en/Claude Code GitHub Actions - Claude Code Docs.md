---
title: Claude Code GitHub Actions - Claude Code Docs
source_url: https://code.claude.com/docs/en/github-actions
description: Learn about integrating Claude Code into your development workflow with
  Claude Code GitHub Actions
---

```
@claude
```

mention in any PR or issue, Claude can analyze your code, create pull requests, implement features, and fix bugs - all while following your project’s standards. For automatic reviews posted on every PR without a trigger, see

[[Code Review - Claude Code Docs|GitHub Code Review]].

Claude Code GitHub Actions is built on top of the

[[Agent SDK overview - Claude Code Docs|Claude Agent SDK]], which enables programmatic integration of Claude Code into your applications. You can use the SDK to build custom automation workflows beyond GitHub Actions.

Claude Opus 4.7 is now available. Claude Code GitHub Actions default to Sonnet. To use Opus 4.7, configure the

[[Claude Code GitHub Actions - Claude Code Docs#Breaking Changes Reference|model parameter]]to use

```
claude-opus-4-7
```

.

## Why use Claude Code GitHub Actions?

- Instant PR creation: Describe what you need, and Claude creates a complete PR with all necessary changes
- Automated code implementation: Turn issues into working code with a single command
- Follows your standards: Claude respects your

  ```
  CLAUDE.md
  ```

  guidelines and existing code patterns
- Simple setup: Get started in minutes with our installer and API key
- Secure by default: Your code stays on Github’s runners

## What can Claude do?

Claude Code provides a powerful GitHub Action that transforms how you work with code:

### Claude Code Action

This GitHub Action allows you to run Claude Code within your GitHub Actions workflows. You can use this to build any custom workflow on top of Claude Code.

[View repository →](https://github.com/anthropics/claude-code-action)

## Setup

## Quick setup

The easiest way to set up this action is through Claude Code in the terminal. Just open claude and run

```
/install-github-app
```

.
This command will guide you through setting up the GitHub app and required secrets.

- You must be a repository admin to install the GitHub app and add secrets
- The GitHub app will request read & write permissions for Contents, Issues, and Pull requests
- This quickstart method is only available for direct Claude API users. If
  you’re using AWS Bedrock or Google Vertex AI, please see the [[Claude Code GitHub Actions - Claude Code Docs|Using with AWS Bedrock & Google Vertex AI]]section.

## Manual setup

If the

```
/install-github-app
```

command fails or you prefer manual setup, please follow these manual setup instructions:

- Install the Claude GitHub app to your repository: [https://github.com/apps/claude](https://github.com/apps/claude)The Claude GitHub app requires the following repository permissions:
  - Contents: Read & write (to modify repository files)
  - Issues: Read & write (to respond to issues)
  - Pull requests: Read & write (to create PRs and push changes)[security documentation](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md).
- Add ANTHROPIC\_API\_KEY to your repository secrets ([Learn how to use secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions))
- Copy the workflow file from [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml)into your repository’s

  ```
  .github/workflows/
  ```

## Upgrading from Beta

If you’re currently using the beta version of Claude Code GitHub Actions, we recommend that you update your workflows to use the GA version. The new version simplifies configuration while adding powerful new features like automatic mode detection.

### Essential changes

All beta users must make these changes to their workflow files in order to upgrade:

- Update the action version: Change

  ```
  @beta
  ```

  to

  ```
  @v1
  ```
- Remove mode configuration: Delete

  ```
  mode: "tag"
  ```

  or

  ```
  mode: "agent"
  ```

  (now auto-detected)
- Update prompt inputs: Replace

  ```
  direct_prompt
  ```

  with

  ```
  prompt
  ```
- Move CLI options: Convert

  ```
  max_turns
  ```

  ,

  ```
  model
  ```

  ,

  ```
  custom_instructions
  ```

  , etc. to

  ```
  claude_args
  ```

### Breaking Changes Reference

Old Beta InputNew v1.0 Input

```
mode
```

(Removed - auto-detected)

```
direct_prompt
```

```
prompt
```

```
override_prompt
```

```
prompt
```

with GitHub variables

```
custom_instructions
```

```
claude_args: --append-system-prompt
```

```
max_turns
```

```
claude_args: --max-turns
```

```
model
```

```
claude_args: --model
```

```
allowed_tools
```

```
claude_args: --allowedTools
```

```
disallowed_tools
```

```
claude_args: --disallowedTools
```

```
claude_env
```

```
settings
```

JSON format

### Before and After Example

Beta version:

## Example use cases

Claude Code GitHub Actions can help you with a variety of tasks. The

[examples directory](https://github.com/anthropics/claude-code-action/tree/main/examples)contains ready-to-use workflows for different scenarios.

### Basic workflow

### Using skills

### Custom automation with prompts

### Common use cases

In issue or PR comments:

## Best practices

### CLAUDE.md configuration

Create a

```
CLAUDE.md
```

file in your repository root to define code style guidelines, review criteria, project-specific rules, and preferred patterns. This file guides Claude’s understanding of your project standards.

### Security considerations

For comprehensive security guidance including permissions, authentication, and best practices, see the

[Claude Code Action security documentation](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md). Always use GitHub Secrets for API keys:

- Add your API key as a repository secret named

  ```
  ANTHROPIC_API_KEY
  ```
- Reference it in workflows:

  ```
  anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
  ```
- Limit action permissions to only what’s necessary
- Review Claude’s suggestions before merging

```
${{ secrets.ANTHROPIC_API_KEY }}
```

) rather than hardcoding API keys directly in your workflow files.

### Optimizing performance

Use issue templates to provide context, keep your

```
CLAUDE.md
```

concise and focused, and configure appropriate timeouts for your workflows.

### CI costs

When using Claude Code GitHub Actions, be aware of the associated costs: GitHub Actions costs:

- Claude Code runs on GitHub-hosted runners, which consume your GitHub Actions minutes
- See [GitHub’s billing documentation](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)for detailed pricing and minute limits

- Each Claude interaction consumes API tokens based on the length of prompts and responses
- Token usage varies by task complexity and codebase size
- See [Claude’s pricing page](https://claude.com/platform/api)for current token rates

- Use specific

  ```
  @claude
  ```

  commands to reduce unnecessary API calls
- Configure appropriate

  ```
  --max-turns
  ```

  in

  ```
  claude_args
  ```

  to prevent excessive iterations
- Set workflow-level timeouts to avoid runaway jobs
- Consider using GitHub’s concurrency controls to limit parallel runs

## Configuration examples

The Claude Code Action v1 simplifies configuration with unified parameters:

- Unified prompt interface - Use

  ```
  prompt
  ```

  for all instructions
- Skills - Invoke installed [[Extend Claude with skills - Claude Code Docs|skills]]directly from the prompt
- CLI passthrough - Any Claude Code CLI argument via

  ```
  claude_args
  ```
- Flexible triggers - Works with any GitHub event

[examples directory](https://github.com/anthropics/claude-code-action/tree/main/examples)for complete workflow files.

## Using with AWS Bedrock & Google Vertex AI

For enterprise environments, you can use Claude Code GitHub Actions with your own cloud infrastructure. This approach gives you control over data residency and billing while maintaining the same functionality.

### Prerequisites

Before setting up Claude Code GitHub Actions with cloud providers, you need:

#### For Google Cloud Vertex AI:

- A Google Cloud Project with Vertex AI enabled
- Workload Identity Federation configured for GitHub Actions
- A service account with the required permissions
- A GitHub App (recommended) or use the default GITHUB\_TOKEN

#### For AWS Bedrock:

- An AWS account with Amazon Bedrock enabled
- GitHub OIDC Identity Provider configured in AWS
- An IAM role with Bedrock permissions
- A GitHub App (recommended) or use the default GITHUB\_TOKEN

Create a custom GitHub App (Recommended for 3P Providers)

For best control and security when using 3P providers like Vertex AI or Bedrock, we recommend creating your own GitHub App:Alternative for Claude API or if you don’t want to setup your own Github app: Use the official Anthropic app:

- Go to [https://github.com/settings/apps/new](https://github.com/settings/apps/new)
- Fill in the basic information:
  - GitHub App name: Choose a unique name (e.g., “YourOrg Claude Assistant”)
  - Homepage URL: Your organization’s website or the repository URL
- Configure the app settings:
  - Webhooks: Uncheck “Active” (not needed for this integration)
- Set the required permissions:
  - Repository permissions:
    - Contents: Read & Write
    - Issues: Read & Write
    - Pull requests: Read & Write
- Repository permissions:
- Click “Create GitHub App”
- After creation, click “Generate a private key” and save the downloaded

  ```
  .pem
  ```

  file
- Note your App ID from the app settings page
- Install the app to your repository:
  - From your app’s settings page, click “Install App” in the left sidebar
  - Select your account or organization
  - Choose “Only select repositories” and select the specific repository
  - Click “Install”
- Add the private key as a secret to your repository:
  - Go to your repository’s Settings → Secrets and variables → Actions
  - Create a new secret named

    ```
    APP_PRIVATE_KEY
    ```

    with the contents of the

    ```
    .pem
    ```

    file
- Add the App ID as a secret:

- Create a new secret named

  ```
  APP_ID
  ```

  with your GitHub App’s ID

This app will be used with the

[actions/create-github-app-token](https://github.com/actions/create-github-app-token)action to generate authentication tokens in your workflows.

- Install from: [https://github.com/apps/claude](https://github.com/apps/claude)
- No additional configuration needed for authentication

Configure cloud provider authentication

Choose your cloud provider and set up secure authentication:

###

###

###

AWS Bedrock

AWS Bedrock

Configure AWS to allow GitHub Actions to authenticate securely without storing credentials.

> Security Note: Use repository-specific configurations and grant only the minimum required permissions.Required Setup:

- Enable Amazon Bedrock:
  - Request access to Claude models in Amazon Bedrock
  - For cross-region models, request access in all required regions
- Set up GitHub OIDC Identity Provider:
  - Provider URL:

    ```
    https://token.actions.githubusercontent.com
    ```
  - Audience:

    ```
    sts.amazonaws.com
    ```
- Provider URL:
- Create IAM Role for GitHub Actions:
  - Trusted entity type: Web identity
  - Identity provider:

    ```
    token.actions.githubusercontent.com
    ```
  - Permissions:

    ```
    AmazonBedrockFullAccess
    ```

    policy
  - Configure trust policy for your specific repository

- AWS\_ROLE\_TO\_ASSUME: The ARN of the IAM role you created

[AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)for detailed OIDC setup instructions.

###

Google Vertex AI

Google Vertex AI

Configure Google Cloud to allow GitHub Actions to authenticate securely without storing credentials.

> Security Note: Use repository-specific configurations and grant only the minimum required permissions.Required Setup:

- Enable APIs in your Google Cloud project:
  - IAM Credentials API
  - Security Token Service (STS) API
  - Vertex AI API
- Create Workload Identity Federation resources:
  - Create a Workload Identity Pool
  - Add a GitHub OIDC provider with:
    - Issuer:

      ```
      https://token.actions.githubusercontent.com
      ```
    - Attribute mappings for repository and owner
    - Security recommendation: Use repository-specific attribute conditions
  - Issuer:
- Create a Service Account:
  - Grant only

    ```
    Vertex AI User
    ```

    role
  - Security recommendation: Create a dedicated service account per repository
- Grant only
- Configure IAM bindings:
  - Allow the Workload Identity Pool to impersonate the service account
  - Security recommendation: Use repository-specific principal sets

- GCP\_WORKLOAD\_IDENTITY\_PROVIDER: The full provider resource name
- GCP\_SERVICE\_ACCOUNT: The service account email address

[Google Cloud Workload Identity Federation documentation](https://cloud.google.com/iam/docs/workload-identity-federation).

Add Required Secrets

Add the following secrets to your repository (Settings → Secrets and variables → Actions):

#### For Claude API (Direct):

- For API Authentication:
  - ```
    ANTHROPIC_API_KEY
    ```

    : Your Claude API key from[console.anthropic.com](https://console.anthropic.com)
- For GitHub App (if using your own app):
  - ```
    APP_ID
    ```

    : Your GitHub App’s ID
  - ```
    APP_PRIVATE_KEY
    ```

    : The private key (.pem) content

#### For Google Cloud Vertex AI

- For GCP Authentication:
  - ```
    GCP_WORKLOAD_IDENTITY_PROVIDER
    ```
  - ```
    GCP_SERVICE_ACCOUNT
    ```
- For GitHub App (if using your own app):
  - ```
    APP_ID
    ```

    : Your GitHub App’s ID
  - ```
    APP_PRIVATE_KEY
    ```

    : The private key (.pem) content

#### For AWS Bedrock

- For AWS Authentication:
  - ```
    AWS_ROLE_TO_ASSUME
    ```
- For GitHub App (if using your own app):
  - ```
    APP_ID
    ```

    : Your GitHub App’s ID
  - ```
    APP_PRIVATE_KEY
    ```

    : The private key (.pem) content

Create workflow files

Create GitHub Actions workflow files that integrate with your cloud provider. The examples below show complete configurations for both AWS Bedrock and Google Vertex AI:

###

###

###

AWS Bedrock workflow

AWS Bedrock workflow

Prerequisites:

- AWS Bedrock access enabled with Claude model permissions
- GitHub configured as an OIDC identity provider in AWS
- IAM role with Bedrock permissions that trusts GitHub Actions

Secret NameDescription

```
AWS_ROLE_TO_ASSUME
```

ARN of the IAM role for Bedrock access

```
APP_ID
```

Your GitHub App ID (from app settings)

```
APP_PRIVATE_KEY
```

The private key you generated for your GitHub App

###

Google Vertex AI workflow

Google Vertex AI workflow

Prerequisites:

- Vertex AI API enabled in your GCP project
- Workload Identity Federation configured for GitHub
- Service account with Vertex AI permissions

Secret NameDescription

```
GCP_WORKLOAD_IDENTITY_PROVIDER
```

Workload identity provider resource name

```
GCP_SERVICE_ACCOUNT
```

Service account email with Vertex AI access

```
APP_ID
```

Your GitHub App ID (from app settings)

```
APP_PRIVATE_KEY
```

The private key you generated for your GitHub App

## Troubleshooting

### Claude not responding to @claude commands

Verify the GitHub App is installed correctly, check that workflows are enabled, ensure API key is set in repository secrets, and confirm the comment contains

```
@claude
```

(not

```
/claude
```

).

### CI not running on Claude’s commits

Ensure you’re using the GitHub App or custom app (not Actions user), check workflow triggers include the necessary events, and verify app permissions include CI triggers.

### Authentication errors

Confirm API key is valid and has sufficient permissions. For Bedrock/Vertex, check credentials configuration and ensure secrets are named correctly in workflows.

## Advanced configuration

### Action parameters

The Claude Code Action v1 uses a simplified configuration:

ParameterDescriptionRequired

```
prompt
```

Instructions for Claude (plain text or a

```
claude_args
```

```
anthropic_api_key
```

```
github_token
```

```
trigger_phrase
```

```
use_bedrock
```

```
use_vertex
```

\*\*Required for direct Claude API, not for Bedrock/Vertex

#### Pass CLI arguments

The

```
claude_args
```

parameter accepts any Claude Code CLI arguments:

- ```
  --max-turns
  ```

  : Maximum conversation turns (default: 10)
- ```
  --model
  ```

  : Model to use (for example,

  ```
  claude-sonnet-4-6
  ```

  )
- ```
  --mcp-config
  ```

  : Path to MCP configuration
- ```
  --allowedTools
  ```

  : Comma-separated list of allowed tools. The

  ```
  --allowed-tools
  ```

  alias also works.
- ```
  --debug
  ```

  : Enable debug output

### Alternative integration methods

While the

```
/install-github-app
```

command is the recommended approach, you can also:

- Custom GitHub App: For organizations needing branded usernames or custom authentication flows. Create your own GitHub App with required permissions (contents, issues, pull requests) and use the actions/create-github-app-token action to generate tokens in your workflows.
- Manual GitHub Actions: Direct workflow configuration for maximum flexibility
- MCP Configuration: Dynamic loading of Model Context Protocol servers

[Claude Code Action documentation](https://github.com/anthropics/claude-code-action/blob/main/docs)for detailed guides on authentication, security, and advanced configuration.

### Customizing Claude’s behavior

You can configure Claude’s behavior in two ways:

- CLAUDE.md: Define coding standards, review criteria, and project-specific rules in a

  ```
  CLAUDE.md
  ```

  file at the root of your repository. Claude will follow these guidelines when creating PRs and responding to requests. Check out our[[How Claude remembers your project - Claude Code Docs|Memory documentation]]for more details.
- Custom prompts: Use the

  ```
  prompt
  ```

  parameter in the workflow file to provide workflow-specific instructions. This allows you to customize Claude’s behavior for different workflows or tasks.

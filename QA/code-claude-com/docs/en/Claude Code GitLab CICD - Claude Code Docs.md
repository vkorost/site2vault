---
title: Claude Code GitLab CI/CD - Claude Code Docs
source_url: https://code.claude.com/docs/en/gitlab-ci-cd
description: Learn about integrating Claude Code into your development workflow with
  GitLab CI/CD
---

Claude Code for GitLab CI/CD is currently in beta. Features and functionality may evolve as we refine the experience.This integration is maintained by GitLab. For support, see the following

[GitLab issue](https://gitlab.com/gitlab-org/gitlab/-/issues/573776).

This integration is built on top of the

[[Agent SDK overview - Claude Code Docs|Claude Code CLI and Agent SDK]], enabling programmatic use of Claude in your CI/CD jobs and custom automation workflows.

## Why use Claude Code with GitLab?

- Instant MR creation: Describe what you need, and Claude proposes a complete MR with changes and explanation
- Automated implementation: Turn issues into working code with a single command or mention
- Project-aware: Claude follows your

  ```
  CLAUDE.md
  ```

  guidelines and existing code patterns
- Simple setup: Add one job to

  ```
  .gitlab-ci.yml
  ```

  and a masked CI/CD variable
- Enterprise-ready: Choose Claude API, AWS Bedrock, or Google Vertex AI to meet data residency and procurement needs
- Secure by default: Runs in your GitLab runners with your branch protection and approvals

## How it works

Claude Code uses GitLab CI/CD to run AI tasks in isolated jobs and commit results back via MRs:

- Event-driven orchestration: GitLab listens for your chosen triggers (for example, a comment that mentions

  ```
  @claude
  ```

  in an issue, MR, or review thread). The job collects context from the thread and repository, builds prompts from that input, and runs Claude Code.
- Provider abstraction: Use the provider that fits your environment:
  - Claude API (SaaS)
  - AWS Bedrock (IAM-based access, cross-region options)
  - Google Vertex AI (GCP-native, Workload Identity Federation)
- Sandboxed execution: Each interaction runs in a container with strict network and filesystem rules. Claude Code enforces workspace-scoped permissions to constrain writes. Every change flows through an MR so reviewers see the diff and approvals still apply.

## What can Claude do?

Claude Code enables powerful CI/CD workflows that transform how you work with code:

- Create and update MRs from issue descriptions or comments
- Analyze performance regressions and propose optimizations
- Implement features directly in a branch, then open an MR
- Fix bugs and regressions identified by tests or comments
- Respond to follow-up comments to iterate on requested changes

## Setup

### Quick setup

The fastest way to get started is to add a minimal job to your

```
.gitlab-ci.yml
```

and set your API key as a masked variable.

- Add a masked CI/CD variable
  - Go to Settings → CI/CD → Variables
  - Add

    ```
    ANTHROPIC_API_KEY
    ```

    (masked, protected as needed)
- Add a Claude job to

  ```
  .gitlab-ci.yml
  ```

```
ANTHROPIC_API_KEY
```

variable, test by running the job manually from CI/CD → Pipelines, or trigger it from an MR to let Claude propose updates in a branch and open an MR if needed.

To run on AWS Bedrock or Google Vertex AI instead of the Claude API, see the

[[Claude Code GitLab CICD - Claude Code Docs#Using with AWS Bedrock & Google Vertex AI|Using with AWS Bedrock & Google Vertex AI]]section below for authentication and environment setup.

### Manual setup (recommended for production)

If you prefer a more controlled setup or need enterprise providers:

- Configure provider access:
  - Claude API: Create and store

    ```
    ANTHROPIC_API_KEY
    ```

    as a masked CI/CD variable
  - AWS Bedrock: Configure GitLab → AWS OIDC and create an IAM role for Bedrock
  - Google Vertex AI: Configure Workload Identity Federation for GitLab → GCP
- Claude API: Create and store
- Add project credentials for GitLab API operations:
  - Use

    ```
    CI_JOB_TOKEN
    ```

    by default, or create a Project Access Token with

    ```
    api
    ```

    scope
  - Store as

    ```
    GITLAB_ACCESS_TOKEN
    ```

    (masked) if using a PAT
- Use
- Add the Claude job to

  ```
  .gitlab-ci.yml
  ```

  (see examples below)
- (Optional) Enable mention-driven triggers:
  - Add a project webhook for “Comments (notes)” to your event listener (if you use one)
  - Have the listener call the pipeline trigger API with variables like

    ```
    AI_FLOW_INPUT
    ```

    and

    ```
    AI_FLOW_CONTEXT
    ```

    when a comment contains

    ```
    @claude
    ```

## Example use cases

### Turn issues into MRs

In an issue comment:

### Get implementation help

In an MR discussion:

### Fix bugs quickly

In an issue or MR comment:

## Using with AWS Bedrock & Google Vertex AI

For enterprise environments, you can run Claude Code entirely on your cloud infrastructure with the same developer experience.

- AWS Bedrock
- Google Vertex AI

### Prerequisites

Before setting up Claude Code with AWS Bedrock, you need:

- An AWS account with Amazon Bedrock access to the desired Claude models
- GitLab configured as an OIDC identity provider in AWS IAM
- An IAM role with Bedrock permissions and a trust policy restricted to your GitLab project/refs
- GitLab CI/CD variables for role assumption:
  - ```
    AWS_ROLE_TO_ASSUME
    ```

    (role ARN)
  - ```
    AWS_REGION
    ```

    (Bedrock region)

### Setup instructions

Configure AWS to allow GitLab CI jobs to assume an IAM role via OIDC (no static keys).Required setup:

- Enable Amazon Bedrock and request access to your target Claude models
- Create an IAM OIDC provider for GitLab if not already present
- Create an IAM role trusted by the GitLab OIDC provider, restricted to your project and protected refs
- Attach least-privilege permissions for Bedrock invoke APIs

- ```
  AWS_ROLE_TO_ASSUME
  ```
- ```
  AWS_REGION
  ```

## Configuration examples

Below are ready-to-use snippets you can adapt to your pipeline.

### Basic .gitlab-ci.yml (Claude API)

### AWS Bedrock job example (OIDC)

Prerequisites:

- Amazon Bedrock enabled with access to your chosen Claude model(s)
- GitLab OIDC configured in AWS with a role that trusts your GitLab project and refs
- IAM role with Bedrock permissions (least privilege recommended)

- ```
  AWS_ROLE_TO_ASSUME
  ```

  : ARN of the IAM role for Bedrock access
- ```
  AWS_REGION
  ```

  : Bedrock region (for example,

  ```
  us-west-2
  ```

  )

Model IDs for Bedrock include region-specific prefixes (for example,

```
us.anthropic.claude-sonnet-4-6
```

). Pass the desired model via your job configuration or prompt if your workflow supports it.

### Google Vertex AI job example (Workload Identity Federation)

Prerequisites:

- Vertex AI API enabled in your GCP project
- Workload Identity Federation configured to trust GitLab OIDC
- A service account with Vertex AI permissions

- ```
  GCP_WORKLOAD_IDENTITY_PROVIDER
  ```

  : Full provider resource name
- ```
  GCP_SERVICE_ACCOUNT
  ```

  : Service account email
- ```
  CLOUD_ML_REGION
  ```

  : Vertex region (for example,

  ```
  us-east5
  ```

  )

With Workload Identity Federation, you do not need to store service account keys. Use repository-specific trust conditions and least-privilege service accounts.

## Best practices

### CLAUDE.md configuration

Create a

```
CLAUDE.md
```

file at the repository root to define coding standards, review criteria, and project-specific rules. Claude reads this file during runs and follows your conventions when proposing changes.

### Security considerations

Never commit API keys or cloud credentials to your repository. Always use GitLab CI/CD variables:

- Add

  ```
  ANTHROPIC_API_KEY
  ```

  as a masked variable (and protect it if needed)
- Use provider-specific OIDC where possible (no long-lived keys)
- Limit job permissions and network egress
- Review Claude’s MRs like any other contributor

### Optimizing performance

- Keep

  ```
  CLAUDE.md
  ```

  focused and concise
- Provide clear issue/MR descriptions to reduce iterations
- Configure sensible job timeouts to avoid runaway runs
- Cache npm and package installs in runners where possible

### CI costs

When using Claude Code with GitLab CI/CD, be aware of associated costs:

- GitLab Runner time:
  - Claude runs on your GitLab runners and consumes compute minutes
  - See your GitLab plan’s runner billing for details
- API costs:
  - Each Claude interaction consumes tokens based on prompt and response size
  - Token usage varies by task complexity and codebase size
  - See [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)for details
- Cost optimization tips:
  - Use specific

    ```
    @claude
    ```

    commands to reduce unnecessary turns
  - Set appropriate

    ```
    max_turns
    ```

    and job timeout values
  - Limit concurrency to control parallel runs
- Use specific

## Security and governance

- Each job runs in an isolated container with restricted network access
- Claude’s changes flow through MRs so reviewers see every diff
- Branch protection and approval rules apply to AI-generated code
- Claude Code uses workspace-scoped permissions to constrain writes
- Costs remain under your control because you bring your own provider credentials

## Troubleshooting

### Claude not responding to @claude commands

- Verify your pipeline is being triggered (manually, MR event, or via a note event listener/webhook)
- Ensure CI/CD variables (

  ```
  ANTHROPIC_API_KEY
  ```

  or cloud provider settings) are present and unmasked
- Check that the comment contains

  ```
  @claude
  ```

  (not

  ```
  /claude
  ```

  ) and that your mention trigger is configured

### Job can’t write comments or open MRs

- Ensure

  ```
  CI_JOB_TOKEN
  ```

  has sufficient permissions for the project, or use a Project Access Token with

  ```
  api
  ```

  scope
- Check the

  ```
  mcp__gitlab
  ```

  tool is enabled in

  ```
  --allowedTools
  ```
- Confirm the job runs in the context of the MR or has enough context via

  ```
  AI_FLOW_*
  ```

  variables

### Authentication errors

- For Claude API: Confirm

  ```
  ANTHROPIC_API_KEY
  ```

  is valid and unexpired
- For Bedrock/Vertex: Verify OIDC/WIF configuration, role impersonation, and secret names; confirm region and model availability

## Advanced configuration

### Common parameters and variables

Claude Code supports these commonly used inputs:

- ```
  prompt
  ```

  /

  ```
  prompt_file
  ```

  : Provide instructions inline (

  ```
  -p
  ```

  ) or via a file
- ```
  max_turns
  ```

  : Limit the number of back-and-forth iterations
- ```
  timeout_minutes
  ```

  : Limit total execution time
- ```
  ANTHROPIC_API_KEY
  ```

  : Required for the Claude API (not used for Bedrock/Vertex)
- Provider-specific environment:

  ```
  AWS_REGION
  ```

  , project/region vars for Vertex

Exact flags and parameters may vary by version of

```
@anthropic-ai/claude-code
```

. Run

```
claude --help
```

in your job to see supported options.

### Customizing Claude’s behavior

You can guide Claude in two primary ways:

- CLAUDE.md: Define coding standards, security requirements, and project conventions. Claude reads this during runs and follows your rules.
- Custom prompts: Pass task-specific instructions via

  ```
  prompt
  ```

  /

  ```
  prompt_file
  ```

  in the job. Use different prompts for different jobs (for example, review, implement, refactor).

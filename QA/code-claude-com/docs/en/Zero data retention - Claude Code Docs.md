---
title: Zero data retention - Claude Code Docs
source_url: https://code.claude.com/docs/en/zero-data-retention
description: Learn about Zero Data Retention (ZDR) for Claude Code on Claude for Enterprise,
  including scope, disabled features, and how to request enablement.
---

- Cost controls per user
- [[Track team usage with analytics - Claude Code Docs|Analytics]]dashboard
- [[Configure server-managed settings - Claude Code Docs|Server-managed settings]]
- Audit logs

## ZDR scope

ZDR covers Claude Code inference on Claude for Enterprise.

### What ZDR covers

ZDR covers model inference calls made through Claude Code on Claude for Enterprise. When you use Claude Code in your terminal, the prompts you send and the responses Claude generates are not retained by Anthropic. This applies regardless of which Claude model is used.

### What ZDR does not cover

ZDR does not extend to the following, even for organizations with ZDR enabled. These features follow

[[Data usage - Claude Code Docs#Data retention|standard data retention policies]]:

FeatureDetailsChat on claude.aiChat conversations through the Claude for Enterprise web interface are not covered by ZDR.CoworkCowork sessions are not covered by ZDR.Claude Code AnalyticsDoes not store prompts or model responses, but collects productivity metadata such as account emails and usage statistics. Contribution metrics are not available for ZDR organizations; the

## Features disabled under ZDR

When ZDR is enabled for a Claude Code organization on Claude for Enterprise, certain features that require storing prompts or completions are automatically disabled at the backend level:

FeatureReason

[[Use Claude Code Desktop - Claude Code Docs#Remote sessions|Remote sessions]]from the Desktop app

```
/feedback
```

)

## Data retention for policy violations

Even with ZDR enabled, Anthropic may retain data where required by law or to address Usage Policy violations. If a session is flagged for a policy violation, Anthropic may retain the associated inputs and outputs for up to 2 years, consistent with Anthropic’s standard ZDR policy.

## Request ZDR

To request ZDR for Claude Code on Claude for Enterprise,

[contact sales](https://www.anthropic.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=zero_data_retention_request)or your Anthropic account team. Your account team will submit the request internally, and Anthropic will review and enable ZDR on your organization after confirming eligibility. All enablement actions are audit-logged. If you are currently using ZDR for Claude Code via pay-as-you-go API keys, you can transition to Claude for Enterprise to gain access to administrative features while maintaining ZDR for Claude Code. Contact your account team to coordinate the migration.

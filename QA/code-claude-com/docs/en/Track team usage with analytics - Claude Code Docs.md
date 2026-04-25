---
title: Track team usage with analytics - Claude Code Docs
source_url: https://code.claude.com/docs/en/analytics
description: View Claude Code usage metrics, track adoption, and measure engineering
  velocity in the analytics dashboard.
---

PlanDashboard URLIncludesRead moreClaude for Teams / Enterprise

[[Track team usage with analytics - Claude Code Docs#Access analytics for Team and Enterprise|Details]][platform.claude.com/claude-code](https://platform.claude.com/claude-code)[[Track team usage with analytics - Claude Code Docs#Access analytics for API customers|Details]]

## Access analytics for Team and Enterprise

Navigate to

[claude.ai/analytics/claude-code](https://claude.ai/analytics/claude-code). Admins and Owners can view the dashboard. The Team and Enterprise dashboard includes:

- Usage metrics: lines of code accepted, suggestion accept rate, daily active users and sessions
- Contribution metrics: PRs and lines of code shipped with Claude Code assistance, with [[Track team usage with analytics - Claude Code Docs#Enable contribution metrics|GitHub integration]]
- Leaderboard: top contributors ranked by Claude Code usage
- Data export: download contribution data as CSV for custom reporting

### Enable contribution metrics

Contribution metrics are in public beta and available on Claude for Teams and Claude for Enterprise plans. These metrics only cover users within your claude.ai organization. Usage through the Claude Console API or third-party integrations is not included.

Install the GitHub app

A GitHub admin installs the Claude GitHub app on your organization’s GitHub account at

[github.com/apps/claude](https://github.com/apps/claude).

Enable Claude Code analytics

A Claude Owner navigates to

[claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)and enables the Claude Code analytics feature.

- “GitHub app required”: install the GitHub app to view contribution metrics
- “Data processing in progress”: check back in a few days and confirm the GitHub app is installed if data doesn’t appear

### Review summary metrics

These metrics are deliberately conservative and represent an underestimate of Claude Code’s actual impact. Only lines and PRs where there is high confidence in Claude Code’s involvement are counted.

- PRs with CC: total count of merged pull requests that contain at least one line of code written with Claude Code
- Lines of code with CC: total lines of code across all merged PRs that were written with Claude Code assistance. Only “effective lines” are counted: lines with more than 3 characters after normalization, excluding empty lines and lines with only brackets or trivial punctuation.
- PRs with Claude Code (%): percentage of all merged PRs that contain Claude Code-assisted code
- Suggestion accept rate: percentage of times users accept Claude Code’s code editing suggestions, including Edit, Write, and NotebookEdit tool usage
- Lines of code accepted: total lines of code written by Claude Code that users have accepted in their sessions. This excludes rejected suggestions and does not track subsequent deletions.

### Explore the charts

The dashboard includes several charts to visualize trends over time.

#### Track adoption

The Adoption chart shows daily usage trends:

- users: daily active users
- sessions: number of active Claude Code sessions per day

#### Measure PRs per user

This chart displays individual developer activity over time:

- PRs per user: total number of PRs merged per day divided by daily active users
- users: daily active users

#### View pull requests breakdown

The Pull requests chart shows a daily breakdown of merged PRs:

- PRs with CC: pull requests containing Claude Code-assisted code
- PRs without CC: pull requests without Claude Code-assisted code

#### Find top contributors

The Leaderboard shows the top 10 users ranked by contribution volume. Toggle between:

- Pull requests: shows PRs with Claude Code vs All PRs for each user
- Lines of code: shows lines with Claude Code vs All lines for each user

### PR attribution

When contribution metrics are enabled, Claude Code analyzes merged pull requests to determine which code was written with Claude Code assistance. This is done by matching Claude Code session activity against the code in each PR.

#### Tagging criteria

PRs are tagged as “with Claude Code” if they contain at least one line of code written during a Claude Code session. The system uses conservative matching: only code where there is high confidence in Claude Code’s involvement is counted as assisted.

#### Attribution process

When a pull request is merged:

- Added lines are extracted from the PR diff
- Claude Code sessions that edited matching files within a time window are identified
- PR lines are matched against Claude Code output using multiple strategies
- Metrics are calculated for AI-assisted lines and total lines

```
claude-code-assisted
```

in GitHub.

#### Time window

Sessions from 21 days before to 2 days after the PR merge date are considered for attribution matching.

#### Excluded files

Certain files are automatically excluded from analysis because they are auto-generated:

- Lock files: package-lock.json, yarn.lock, Cargo.lock, and similar
- Generated code: Protobuf outputs, build artifacts, minified files
- Build directories: dist/, build/, node\_modules/, target/
- Test fixtures: snapshots, cassettes, mock data
- Lines over 1,000 characters, which are likely minified or generated

#### Attribution notes

Keep these additional details in mind when interpreting attribution data:

- Code substantially rewritten by developers, with more than 20% difference, is not attributed to Claude Code
- Sessions outside the 21-day window are not considered
- The algorithm does not consider the PR source or destination branch when performing attribution

### Get the most from analytics

Use contribution metrics to demonstrate ROI, identify adoption patterns, and find team members who can help others get started.

#### Monitor adoption

Track the Adoption chart and user counts to identify:

- Active users who can share best practices
- Overall adoption trends across your organization
- Dips in usage that may indicate friction or issues

#### Measure ROI

Contribution metrics help answer “Is this tool worth the investment?” with data from your own codebase:

- Track changes in PRs per user over time as adoption increases
- Compare PRs and lines of code shipped with vs. without Claude Code
- Use alongside [DORA metrics](https://dora.dev/), sprint velocity, or other engineering KPIs to understand changes from adopting Claude Code

#### Identify power users

The Leaderboard helps you find team members with high Claude Code adoption who can:

- Share prompting techniques and workflows with the team
- Provide feedback on what’s working well
- Help onboard new users

#### Access data programmatically

To query this data through GitHub, search for PRs labeled with

```
claude-code-assisted
```

.

## Access analytics for API customers

API customers using the Claude Console can access analytics at

[platform.claude.com/claude-code](https://platform.claude.com/claude-code). You need the UsageView permission to access the dashboard, which is granted to Developer, Billing, Admin, Owner, and Primary Owner roles.

Contribution metrics with GitHub integration are not currently available for API customers. The Console dashboard shows usage and spend metrics only.

- Lines of code accepted: total lines of code written by Claude Code that users have accepted in their sessions. This excludes rejected suggestions and does not track subsequent deletions.
- Suggestion accept rate: percentage of times users accept code editing tool usage, including Edit, Write, and NotebookEdit tools.
- Activity: daily active users and sessions shown on a chart.
- Spend: daily API costs in dollars alongside user count.

### View team insights

The team insights table shows per-user metrics:

- Members: all users who have authenticated to Claude Code. API key users display by key identifier, OAuth users display by email address.
- Spend this month: per-user total API costs for the current month.
- Lines this month: per-user total of accepted code lines for the current month.

Spend figures in the Console dashboard are estimates for analytics purposes. For actual costs, refer to your billing page.

## Related resources

- [[Monitoring - Claude Code Docs|Monitoring with OpenTelemetry]]: export real-time metrics and events to your observability stack
- [[Manage costs effectively - Claude Code Docs|Manage costs effectively]]: set spend limits and optimize token usage
- [[Configure permissions - Claude Code Docs|Permissions]]: configure roles and permissions

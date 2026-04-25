---
title: Streaming Input - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode
description: Understanding the two input modes for Claude Agent SDK and when to use
  each
---

## Overview

The Claude Agent SDK supports two distinct input modes for interacting with agents:

- Streaming Input Mode (Default & Recommended) - A persistent, interactive session
- Single Message Input - One-shot queries that use session state and resuming

## Streaming Input Mode (Recommended)

Streaming input mode is the preferred way to use the Claude Agent SDK. It provides full access to the agent’s capabilities and enables rich, interactive experiences. It allows the agent to operate as a long lived process that takes in user input, handles interruptions, surfaces permission requests, and handles session management.

### How It Works

### Benefits

## Image Uploads

Attach images directly to messages for visual analysis and understanding

## Queued Messages

Send multiple messages that process sequentially, with ability to interrupt

## Tool Integration

Full access to all tools and custom MCP servers during the session

## Hooks Support

Use lifecycle hooks to customize behavior at various points

## Real-time Feedback

See responses as they’re generated, not just final results

## Context Persistence

Maintain conversation context across multiple turns naturally

### Implementation Example

## Single Message Input

Single message input is simpler but more limited.

### When to Use Single Message Input

Use single message input when:

- You need a one-shot response
- You do not need image attachments, hooks, etc.
- You need to operate in a stateless environment, such as a lambda function

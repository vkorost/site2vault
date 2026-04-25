---
title: Get structured output from agents - Claude Code Docs
source_url: https://code.claude.com/docs/en/agent-sdk/structured-outputs
description: Return validated JSON from agent workflows using JSON Schema, Zod, or
  Pydantic. Get type-safe, structured data after multi-turn tool use.
---

[JSON Schema](https://json-schema.org/understanding-json-schema/about)for the structure you need, and the SDK validates the output against it, re-prompting on mismatch. If validation does not succeed within the retry limit, the result is an error instead of structured data; see

[[Get structured output from agents - Claude Code Docs#Error handling|Error handling]]. For full type safety, use

[[Get structured output from agents - Claude Code Docs#Type-safe schemas with Zod and Pydantic|Zod]](TypeScript) or

[[Get structured output from agents - Claude Code Docs#Type-safe schemas with Zod and Pydantic|Pydantic]](Python) to define your schema and get strongly-typed objects back.

## Why structured outputs?

Agents return free-form text by default, which works for chat but not when you need to use the output programmatically. Structured outputs give you typed data you can pass directly to your application logic, database, or UI components. Consider a recipe app where an agent searches the web and brings back recipes. Without structured outputs, you get free-form text that you’d need to parse yourself. With structured outputs, you define the shape you want and get typed data you can use directly in your app.

###

Without structured outputs

Without structured outputs

###

With structured outputs

With structured outputs

## Quick start

To use structured outputs, define a

[JSON Schema](https://json-schema.org/understanding-json-schema/about)describing the shape of data you want, then pass it to

```
query()
```

via the

```
outputFormat
```

option (TypeScript) or

```
output_format
```

option (Python). When the agent finishes, the result message includes a

```
structured_output
```

field with validated data matching your schema.
The example below asks the agent to research Anthropic and return the company name, year founded, and headquarters as structured output.

## Type-safe schemas with Zod and Pydantic

Instead of writing JSON Schema by hand, you can use

[Zod](https://zod.dev/)(TypeScript) or

[Pydantic](https://docs.pydantic.dev/latest/)(Python) to define your schema. These libraries generate the JSON Schema for you and let you parse the response into a fully-typed object you can use throughout your codebase with autocomplete and type checking. The example below defines a schema for a feature implementation plan with a summary, list of steps (each with complexity level), and potential risks. The agent plans the feature and returns a typed

```
FeaturePlan
```

object. You can then access properties like

```
plan.summary
```

and iterate over

```
plan.steps
```

with full type safety.

- Full type inference (TypeScript) and type hints (Python)
- Runtime validation with

  ```
  safeParse()
  ```

  or

  ```
  model_validate()
  ```
- Better error messages
- Composable, reusable schemas

## Output format configuration

The

```
outputFormat
```

(TypeScript) or

```
output_format
```

(Python) option accepts an object with:

- ```
  type
  ```

  : Set to

  ```
  "json_schema"
  ```

  for structured outputs
- ```
  schema
  ```

  : A[JSON Schema](https://json-schema.org/understanding-json-schema/about)object defining your output structure. You can generate this from a Zod schema with

  ```
  z.toJSONSchema()
  ```

  or a Pydantic model with

  ```
  .model_json_schema()
  ```

```
enum
```

,

```
const
```

,

```
required
```

, nested objects, and

```
$ref
```

definitions. For the full list of supported features and limitations, see

[JSON Schema limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#json-schema-limitations).

## Example: TODO tracking agent

This example demonstrates how structured outputs work with multi-step tool use. The agent needs to find TODO comments in the codebase, then look up git blame information for each one. It autonomously decides which tools to use (Grep to search, Bash to run git commands) and combines the results into a single structured response. The schema includes optional fields (

```
author
```

and

```
date
```

) since git blame information might not be available for all files. The agent fills in what it can find and omits the rest.

## Error handling

Structured output generation can fail when the agent cannot produce valid JSON matching your schema. This typically happens when the schema is too complex for the task, the task itself is ambiguous, or the agent hits its retry limit trying to fix validation errors. When an error occurs, the result message has a

```
subtype
```

indicating what went wrong:

SubtypeMeaning

```
success
```

Output was generated and validated successfully

```
error_max_structured_output_retries
```

Agent couldn’t produce valid output after multiple attempts

```
subtype
```

field to determine whether the output was generated successfully or if you need to handle a failure:

- Keep schemas focused. Deeply nested schemas with many required fields are harder to satisfy. Start simple and add complexity as needed.
- Match schema to task. If the task might not have all the information your schema requires, make those fields optional.
- Use clear prompts. Ambiguous prompts make it harder for the agent to know what output to produce.

## Related resources

- [JSON Schema documentation](https://json-schema.org/): learn JSON Schema syntax for defining complex schemas with nested objects, arrays, enums, and validation constraints
- [API Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs): use structured outputs with the Claude API directly for single-turn requests without tool use
- [[Give Claude custom tools - Claude Code Docs|Custom tools]]: give your agent custom tools to call during execution before returning structured output

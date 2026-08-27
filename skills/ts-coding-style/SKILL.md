---
name: ts-coding-style
description: TypeScript/JavaScript coding conventions. Apply this skill whenever you're writing, reviewing, or discussing TypeScript or JavaScript code — even if the user hasn't explicitly asked for a style review. Covers naming, function design, guard clauses, dispatch tables, iteration, immutability, modules, logging, and TypeScript-specific patterns (satisfies vs as, enum vs const enum, type vs interface, unknown over any).
user-invocable: true
---

# TypeScript / JavaScript Style

Apply these conventions when writing or reviewing TypeScript or JavaScript code.

## Core Principles

- Prefer explicit over clever. If a reader has to pause to parse something, split it.
- Code should describe itself. Prefer better names over comments.
- Comments explain _why_, not _what_. If you feel the urge to comment a block, ask whether a better name would eliminate the need.
- Make bad states impossible by structure rather than checking for them at runtime.
- Default to immutable patterns; mutate only when there's a meaningful performance reason.

## Naming

|Thing|Convention|Example|
|---|---|---|
|Variables & functions|`camelCase`|`fetchUserById`, `isActive`|
|Classes|`PascalCase`|`UserSession`|
|Constants (module-level)|`UPPER_SNAKE_CASE`|`MILLISECONDS_PER_DAY`|
|Types & interfaces|`PascalCase`|`UserConfig`, `ApiResponse`|
|Files|`kebab-case`|`user-session.ts`|

```ts
// BAD
const d = 86400000
function getUser(u) {}

// GOOD
const MILLISECONDS_PER_DAY = 1000 * 60 * 60 * 24
function fetchUserById(userId: string) {}
```

Constants that encode calculations should show the calculation, not just the result — this documents the derivation and makes future edits safer.

## Function Design

### One function, one job

Functions should do one thing and be named for that thing. If a block inside a function feels like it needs a comment, it has earned its own named function.

**Extract until the name is the comment.**

```ts
// BAD — validation, normalization, and construction mixed together
// (for a tiny function it's fine, but if this gets any larger... bad)
function createUser(options) {
  options.name = options.name ?? 'New User'
  if (options.age < 0) throw new Error('Age cannot be negative')
  // ... more logic
  return { id: uuid(), name: options.name, age: options.age }
}

// GOOD — each function has one job
function createUser(options) {
  const { name, age } = sanitizeUserOptions(options)
  // ... more logic
  return { id: uuid(), name, age }
}

function sanitizeUserOptions(options) {
  if (options.age < 0) throw new Error('Age cannot be negative')
  return { name: options.name ?? 'New User', age: options.age }
}
```

### Arguments

Up to 3-4 positional arguments is fine. Beyond that, switch to a config/options object — call sites become self-documenting and argument order stops mattering.

```ts
// BAD
sendEmail('alice@example.com', 'Welcome', true, false, 3)

// GOOD
sendEmail({ 
  to: 'alice@example.com',
  subject: 'Welcome',
  html: true,
  bcc: false,
  retries: 3 
})
```

### Thin handlers, fat services

In server/API contexts, route handlers should only: extract context, call a service, return the result. Business logic belongs in services, not handlers.

```ts
// BAD — logic in the handler
app.post('/users', async (c) => {
  const body = await c.req.json()
  if (!body.email) return c.json({ error: 'Email required' }, 400)
  const existing = await db.users.findByEmail(body.email)
  if (existing) return c.json({ error: 'Already exists' }, 409)
  return c.json(await db.users.create(body), 201)
})

// GOOD — handler is a thin wrapper
app.post('/users', async (c) => {
  const body = await c.req.json()
  return c.json(await userService.create(body), 201)
})
```

## Conditionals

Use early returns (guard clauses) to handle edge cases and invalid states up front. Reserve `if/else` for branches that are conceptually balanced.

```ts
// BAD — nested conditions
function getDiscount(user) {
  if (user) {
    if (user.isPremium) {
      if (user.orderCount > 10) {
        return 0.2
      }
    }
  }
  return 0
}

// GOOD — guard clauses, invalid states exit immediately
function getDiscount(user) {
  if (!user) return 0
  if (!user.isPremium) return 0
  if (user.orderCount <= 10) return 0
  return 0.2
}
```

```ts
// if/else is fine here — branches are conceptually balanced
function parity(n: number) {
  if (n % 2 === 0) {
    return 'even'
  } else {
    return 'odd'
  }
}
```

## Dispatch Tables

When branching on a key to call different functions, prefer a dispatch table (a plain object mapping keys to functions) over `if/else` chains or `switch`. Adding a new case becomes a data change, not a logic change.

```ts
// BAD
if (options.parser === 'js') return jsParser(options.args)
if (options.parser === 'md') return mdParser(options.args)

// BAD
switch (options.parser) {
  case 'js': return jsParser(options.args)
  case 'md': return mdParser(options.args)
}

// GOOD
const PARSERS: Record<string, (args: string[]) => Result> = {
  js: args => jsParser(args),
  md: args => mdParser(args),
}

const parser = PARSERS[options.parser]
if (!parser) throw new Error(`Unknown parser: "${options.parser}"`)
parser(options.args)
```

Large or growing dispatch tables are natural candidates for their own module.

## Loops and Iteration

Avoid C-style `for` loops. Prefer `for...of`, iterators, and array methods. Put loop termination conditions in the `while` header, not in a mid-loop `break`.

```ts
// BAD
for (let i = 0; i < items.length; i++) { ... }

while (true) {
  if (done) break
  ...
}

// GOOD
for (const item of items) { ... }

while (!done) { ... }

items.forEach(process)
const results = items.map(transform)
const filtered = items.filter(isValid)
```

When passing a named function as a callback, pass it directly (point-free) rather than wrapping it in a redundant arrow function. Use an arrow function only when adapting the signature.

```ts
// BAD
const results = items.map(item => transform(item))

// GOOD
const results = items.map(transform)
```

## Expressions and Operators

Use `+= 1` / `-= 1` instead of `++` / `--`. Prefix/postfix ambiguity disappears and intent is unambiguous at a glance. Never compound expressions that require careful parsing.

```ts
// BAD
i++
const result = x + ++i

// GOOD
i += 1
const result = x + i
```

Use `===` / `!==` always. Never `==` / `!=` — JS coercion with loose equality produces surprising results.

Use template literals over string concatenation.

```ts
// BAD
const msg = 'Hello, ' + user.name + '! You have ' + count + ' messages.'

// GOOD
const msg = `Hello, ${user.name}! You have ${count} messages.`
```

Use `?.` and `??` to handle nullable values. Note: `??` guards against `null` and `undefined` only — unlike `||`, it does not treat `0`, `''`, or `false` as fallback triggers.

```ts
// BAD
const street = user && user.address && user.address.street
const name = value !== null && value !== undefined ? value : 'Anonymous'

// GOOD
const street = user?.address?.street
const name = value ?? 'Anonymous'
```

## Object Creation and Architecture

Prefer the factory pattern for creating objects. Use classes and inheritance only when a genuine "is-a" relationship exists and the hierarchy stays shallow.

```ts
// GOOD: factory
function createUser(name: string, role: string) {
  return { name, role }
}

// Only use classes when inheritance is genuinely beneficial
class AdminUser extends BaseUser { ... }
```

Pass dependencies in via factory arguments rather than importing at module scope. Keeps modules testable and easy to reason about in isolation.

```ts
// BAD — hard dependency
import { db } from '../db'
export function createUserService() {
  return { find: (id: string) => db.users.findById(id) }
}

// GOOD — injected
export function createUserService(db: Database) {
  return { find: (id: string) => db.users.findById(id) }
}
```

Separate config and constants from logic. Values that encode choices — thresholds, lookup tables, dispatch maps — belong in their own declaration, not inline.

```ts
// BAD
function getRetryDelay(attempt: number) {
  return attempt * 1000 * 60
}

// GOOD
const RETRY_BASE_DELAY_MS = 1000 * 60

function getRetryDelay(attempt: number) {
  return attempt * RETRY_BASE_DELAY_MS
}
```

## Immutability

Default to `const`, spread operators, and non-mutating array methods. Pure functions are the goal — mutability is acceptable when there's a meaningful performance reason.

```ts
// BAD
function addItem(list, item) {
  list.push(item)
  return list
}

// GOOD
function addItem(list, item) {
  return [...list, item]
}
```

## Exports and Modules

Named exports by default — they're explicit and refactor-friendly. Default exports only when a framework requires it (e.g. Vue SFC — Single File Component, Next.js page) or the module has a single canonical export. Barrel files (`index.ts`) are fine for grouping; use judgement based on project size.

## Logging

Never use raw `console.log` in non-trivial code. All logging goes through a logger.

For quick prototypes, wrap `console.log` in a minimal facade so it can be swapped without a find-and-replace:

```ts
const log = (...args: unknown[]) => console.log(...args)
```

For real projects, the logging library is a deliberate decision — discuss before picking one. Common options: `pino` (high-performance, structured), `winston` (flexible, widely used).

## Comments and Documentation

When you feel the urge to comment a block, first ask whether a better name would eliminate the need. If a comment is still warranted, explain _why_ — not what.

```ts
// BAD — describes what the code does (the code already says this)
// Check if user is active
if (user.isActive) { ... }

// GOOD — explains why
// Prevent inactive users from using the billing portal
if (user.isActive) { ... }
```

**Exception: published libraries.** All exported functions, types, and constants should have JSDoc. This enables documentation generation and IDE tooltips for consumers without the source in front of them.

```ts
// Application code — no JSDoc needed
function fetchUserById(userId: string) { ... }

// Published package — JSDoc is valuable
/**
 * Fetches a user by their unique ID.
 * Returns null if the user does not exist.
 */
export function fetchUserById(userId: string): Promise<User | null> { ... }
```

## TypeScript

Avoid `any`; use `unknown` when the type is genuinely unknown and narrow it explicitly.

`type` vs `interface`:

- `interface` for object shapes that may be extended or implemented by a class.
- `type` for unions, intersections, mapped types, and aliases.

Consistency within a file matters more than the choice itself.

Let TypeScript infer types where obvious. Add explicit annotations where they clarify intent or prevent a type from being inferred too broadly.

```ts
// GOOD — inference is obvious
const items = ['a', 'b', 'c']

// GOOD — annotation narrows the type usefully
const status: 'active' | 'inactive' = getStatus()

// BAD — annotation is noise
const count: number = 42
```

Use plain `enum`, not `const enum`. `const enum` is inlined at compile time and becomes invisible to module consumers — a footgun for published packages.

```ts
// BAD
const enum Direction { Up, Down }

// GOOD
enum Direction { Up, Down }
```

### `satisfies` vs `as`

Prefer `satisfies` over `as`. `satisfies` validates a value against a type without widening or changing inference. `as` overrides the compiler and can hide real bugs.

```ts
type Config = { mode: 'light' | 'dark'; size: number }

// BAD — compiler trusts you even if the shape is wrong
const config = { mode: 'dark', size: 42 } as Config

// GOOD — validated against Config, type stays narrow
const config = { mode: 'dark', size: 42 } satisfies Config
config.mode  // inferred as 'dark', not string
```

Reserve `as` for genuinely needing to override inference (e.g. poorly typed third-party code). Treat frequent use as a code smell.

# agent-template-typescript

*A minimal Copier template for TypeScript projects with Bun and Biome.*

Get a new TypeScript project running in seconds with sensible defaults: strict
type checking, fast testing with Bun, and consistent formatting with Biome.

______________________________________________________________________

## Why agent-template-typescript?

Starting a TypeScript project means configuring the same tools every time:
TypeScript compiler options, linting rules, test setup, and build scripts.
This template provides:

- **Strict TypeScript**: All the strictness flags enabled by default
- **Bun runtime**: Fast execution and built-in test runner
- **Biome**: Lightning-fast linting and formatting in one tool
- **No web baggage**: Pure TypeScript—no React, no bundlers, no CSS

______________________________________________________________________

## Quick start

### Prerequisites

- [Copier](https://copier.readthedocs.io/) 9.0+
- [Bun](https://bun.sh/)

### Generate a project

```bash
copier copy gh:leynos/agent-template-typescript my-project
```

Copier will prompt for:

| Variable              | Description                          |
| --------------------- | ------------------------------------ |
| `project_name`        | Kebab-case name (e.g. `my-project`)  |
| `project_title`       | Human-readable title                 |
| `project_description` | Short project description            |
| `github_username`     | GitHub username or organization      |

### Run the tests

```bash
cd my-project
bun test:all
```

______________________________________________________________________

## What's included

```text
my-project/
├── src/
│   └── index.ts         # Entry point
├── tests/
│   ├── setup.ts         # Test configuration
│   └── index.test.ts    # Example test
├── biome.jsonc          # Linting and formatting
├── bunfig.toml          # Bun configuration
├── package.json         # Scripts and dependencies
└── tsconfig.json        # TypeScript configuration
```

### Scripts

| Script          | Description                              |
| --------------- | ---------------------------------------- |
| `bun build`     | Compile TypeScript to `dist/`            |
| `bun test`      | Run tests                                |
| `bun test:all`  | Run lint, type check, and tests          |
| `bun lint`      | Check code with Biome                    |
| `bun fmt`       | Format code with Biome                   |
| `bun check:types` | Type check without emitting            |

______________________________________________________________________

## TypeScript configuration

The template enables TypeScript's strictest settings:

- `strict: true`
- `noUncheckedIndexedAccess`
- `exactOptionalPropertyTypes`
- `noPropertyAccessFromIndexSignature`
- `useUnknownInCatchVariables`

These catch more bugs at compile time but require explicit handling of edge
cases. If this is too strict for a given project, adjust `tsconfig.json`.

______________________________________________________________________

## Licence

ISC — see [LICENCE](LICENSE) for details.

______________________________________________________________________

## Contributing

Contributions welcome! Please open an issue or pull request.

Run `make spelling` after changing Markdown or template prose. It refreshes an
ignored local copy of the shared `leynos` en-GB-oxendict dictionary only when
the published source is newer, regenerates the tracked `typos.toml`, and checks
the parent and rendered Markdown sources with `typos` 1.48.0. Repository-only
exceptions belong in `typos.local.toml`; never edit the generated configuration
by hand.

### Python script shebang

Standalone Python scripts (such as `scripts/generate_typos_config.py`) declare
their dependencies in a [PEP 723](https://peps.python.org/pep-0723/) inline
metadata block and must use:

```python
#!/usr/bin/env -S uv run --script
```

`uv run --script` reads the adjacent `# /// script` block and installs its
dependencies before execution. The superficially similar
`#!/usr/bin/env -S uv run python` shebang skips that step entirely—it runs the
interpreter directly, so the script fails at import time when a declared
dependency is not already installed.

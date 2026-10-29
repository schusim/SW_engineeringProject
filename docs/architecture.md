# Git 

NEVER PUSH TO MAIN!! 


## Commit messages

### The structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

| Part | Rule |
|---|---|
| **type** | Required. A noun like `feat` or `fix`. Then the optional scope, the optional `!`, and a colon with a space. |
| **scope** | Optional. A noun in parentheses that names the part of the code, for example `fix(parser):`. |
| **description** | Required. A short summary directly after the colon and space. |
| **body** | Optional. Free text, as many paragraphs as you need. It starts one blank line after the description. |
| **footer(s)** | Optional. Starts one blank line after the body. Format: `Token: value` or `Token #value`. Use `-` instead of spaces in the token (for example `Reviewed-by`). `BREAKING CHANGE` is the only exception. |

## Commit types

| Type | Description |
|---|---|
| `build` | Changes that affect the build system or external dependencies |
| `chore` | Changes that do not relate to a fix or feature and don't modify src or test files (for example updating dependencies) |
| `ci` | Changes to CI configuration files and scripts |
| `docs` | Documentation only changes |
| `feat` | A new feature |
| `fix` | A bug fix |
| `perf` | A code change that improves performance |
| `refactor` | A code change that neither fixes a bug nor adds a feature |
| `style` | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc) |
| `test` | Adding missing tests or correcting existing tests |

### Breaking changes

A breaking change is a change that can break the code of the people who use your code. It can be part of a commit of **any** type.

There are two ways to mark it. You can use one or both:

- Add `!` directly before the colon: `feat(api)!: remove v1 endpoints`
- Add a footer that starts with `BREAKING CHANGE:` (uppercase). `BREAKING-CHANGE:` works too.

If you use `!`, you can skip the footer. Then the description must explain the breaking change.

## Branch Naming convention 

Branch names use the same types as commit messages. So a branch and its commits describe the work in the same way.

Hierarchical Branch structure. 

    planning/<name>  --planning branch 
    feature/<name>   --feature branch 
    bugfix/<name>    --bugfix branch 
    
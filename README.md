# DE Learning

An interactive study hub for **data engineering interview preparation**, aimed at Lead Data Engineer and Data Architect roles.

It's a small static website: plain HTML, CSS and JavaScript, with no build step and no backend. It has two parts:

- **Topic tracker** (`index.html`): 78 interview topics in seven areas. Readers tick topics off as they learn them, and progress is saved in their own browser.
- **Learning paths**: interactive pages that teach one area in depth, with diagrams, worked examples, failure scenarios, debug flows and ready-to-use interview answers.

## Why this repo exists

The hub started as a personal prep tool and is now open to friends for review and contributions. Git keeps a full history, so every change is visible, reviewable and reversible.

## What's inside

| Path | What it is |
| --- | --- |
| `index.html` | Hub: topic tracker and list of learning paths |
| `spark/index.html` | Spark Core path: list of modules |
| `spark/architecture/` | Spark Core module 1: overview, deep dive (memory internals, dynamic allocation, speculation) and production memory failures |
| `spark/mapreduce/` | Spark Core background: Hadoop & MapReduce, and what Spark solved |
| `spark/data-abstractions/` | Spark Core module 2: RDD vs DataFrame vs Dataset vs pandas, with examples and production issues |
| `spark-architecture.html` | Redirect to `spark/architecture/` |
| `spark-execution.html` | Spark Core module 3: spark-submit flow, lazy evaluation, narrow vs wide, stages |
| `spark-optimizer.html` | Spark Core module 4: Catalyst, pushdown and pruning, explain(), joins, AQE, UDFs |
| `spark-tuning.html` | Spark Core module 5: debug flow, six failure scenarios, shuffle, partition and executor sizing |
| `styles.css` | Shared design tokens and components (light and dark themes) |
| `scripts/check.py` | Automated checks run on every pull request |
| `AGENTS.md` | Conventions for AI coding agents (and humans) editing the site |
| `CONTRIBUTING.md` | How to propose changes |

## Topic areas and status

| Area | Topics | Learning path |
| --- | --- | --- |
| Spark core | 27 | Available (background + 5 modules) |
| Structured Streaming | 10 | Planned next |
| Delta Lake & Databricks | 16 | Planned |
| Iceberg & table formats | 5 | Planned |
| Data modelling & SQL | 6 | Planned |
| Pipelines, orchestration & quality | 10 | Planned |
| Governance & cloud | 4 | Planned |

## Viewing it

- **Online:** via GitHub Pages, once enabled (Settings → Pages → deploy from `main`, root folder).
- **Locally:** open `index.html` in a browser. To make cross-page links behave exactly as they do online, serve the folder:

  ```bash
  python3 -m http.server 8000
  # then open http://localhost:8000
  ```

## How each module is organised

Every topic is a module with **a short overview first and depth on demand**:

- **Overview** (always there): a refresher you can read in about 10 minutes. It covers what the topic is, one core diagram, a cheat sheet of key facts, ready-made interview answers and a quick self-check. Come back to it the day before an interview.
- **Sub-pages** (only where there's enough to say):
  - **Deep dive**: internals, edge cases, config details
  - **Examples**: runnable code, plans, worked numbers, interactive demos
  - **Real-world use cases**: patterns at scale and system-design trade-offs
  - **Production issues**: common failures, how to confirm them, fixes and prevention

Modules live in folders by area, for example `spark/architecture/`. The four Spark Core pages at the root predate this layout and are being moved into it one module at a time. See [AGENTS.md](AGENTS.md) for the full structure.

## Contributing

Corrections, clearer explanations, new scenarios and new learning paths are all welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. If you're using an AI coding agent, point it at [AGENTS.md](AGENTS.md) first.

All changes go through a pull request into `main` and are reviewed by the maintainer.

## Maintainer

Saksham Gupta

# Claude SEO Skills Benchmark

A small test site with 20 planted SEO problems, an answer key written before any run, and the audits 5 Claude Code SEO skill packs (plus plain Claude Code) wrote for it. Run your own skill against it and compare.

Write-up with the verdict and install commands: **[Best Claude SEO Skills: 5 Packs Tested](https://saeedseo.com/blog/claude-seo-skills/)**, by [Saeed Shahriar](https://saeedseo.com/).

## Results (hard set, URL only)

| Pack | Found /20 | Cost per audit | Missed |
|---|---|---|---|
| [marketingskills](https://github.com/coreyhaines31/marketingskills) (seo-audit) | 20 | $0.54 | none |
| [SE Ranking seo-skills](https://github.com/seranking/seo-skills) (no MCP) | 20 | $0.50 | none |
| [claude-seo](https://github.com/AgriciDaniel/claude-seo) | 18 | $0.45 | X-Robots-Tag noindex header, missing viewport |
| [Hawk Academy](https://hawkacademy.co/claude-seo-skills) | 18 | $0.35 | X-Robots-Tag noindex header, onclick-only link |
| Plain Claude Code (no skill) | 18 | $0.40 | X-Robots-Tag noindex header, missing viewport |
| [open-seo](https://github.com/every-app/open-seo) (no MCP) | 16 | $0.57 | header noindex, JS-only content, schema price mismatch, viewport |

One run per pack on the hard set, Claude Sonnet 5.5, graded blind against the key by Codex and Claude Opus (Opus hit a usage limit before grading marketingskills and SE Ranking; those are Codex grades). The easy set (19 runs) didn't separate the packs: nearly all found 19 or 20. Details: `results-v1.md`, `results-v2.md`.

## What's here

| File | What |
|---|---|
| `answer-key.md`, `answer-key-v2.md` | The 20 planted issues per set and the scoring rules |
| `build_lab.py`, `build_lab_v2.py` | Build the test site (a coffee roaster, 17 and 23 pages) |
| `serve.py`, `serve_v2.py` | Serve it on localhost with the headers and redirects the issues need |
| `crawl.py`, `gsc.csv` | The crawl export and Search Console file given in the easy set's "full" condition |
| `run.sh`, `run-url.sh`, `run-v2.sh` | One headless Claude Code run: fresh folder, only the given skills installed |
| `round*.sh` | Every pack once, 3 at a time |
| `grade.sh`, `grade-v2.sh`, `grader-prompt.md` | Blind grading with Claude Opus and Codex |
| `score.py` | Tally the grades |
| `results-v1/`, `results-v2/` | Every audit, its run summary (cost, turns, skills loaded) and its grades |
| `runs-log.md` | Pack versions, run settings, and the answer-key hashes logged before run 1 |
| `package-audit.md` | What each pack installs and runs, checked before installing |

## The answer keys were fixed first

Each key's sha256 was logged in `runs-log.md` before any run, so the goalposts can't move:

- `answer-key.md`: `25b63162cb2f84eaa8e97e437d98ee96bc93dc936f8294afb84801c2b402b82c`
- `answer-key-v2.md`: `08e9440f6c05a56cc59fabc71e1ba88f5cfab6c566b341d272f6499454ef9c1d`

Check with `sha256sum answer-key.md answer-key-v2.md`.

## Run your own skill on the hard set

Needs Claude Code (`claude`) and Python 3. Grading also uses the Codex CLI.

```bash
python3 build_lab_v2.py work/v2                 # writes work/v2/site/
python3 serve_v2.py work/v2/site &              # http://localhost:8766/
./run-v2.sh my-skill-1 "path/to/my-skill" "" "Use the my-skill skill."
cp results-v2/server-behaviour.txt work/v2/
./grade-v2.sh my-skill-1                        # writes work/v2/grading/<id>/
python3 score.py work/v2
```

The audit lands in `work/v2/runs/my-skill-1/audit.md`. Scoring: 1 for the right page and problem, 0.5 for the right area without the page, 0 for a miss. To re-run the 5 packs, clone each at the version in `runs-log.md` into `packs/<name>/` and run `./round-v2.sh 1`.

## Limits

One small site. It says nothing about local SEO, e-commerce, big sites or links. Pack scripts were not allowed to run, so this tests each skill's instructions, not its code.

## Cite

See `CITATION.cff`, or the Zenodo DOI on the latest release.

## License

Code: MIT. Answer keys, results and write-up: CC BY 4.0.

# Claude SEO Skills Benchmark: 5 Claude Code SEO skill packs tested

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23668169.svg)](https://doi.org/10.5281/zenodo.23668169)

On 22 October 2026 I couldn't find a side-by-side test of Claude Code SEO skills. So I built a small site with **20 planted SEO problems** and wrote the answer key before any run.

Then 5 skill packs and plain Claude Code each audited it. **The verdict and install commands** are in the write-up, [Best Claude SEO Skills: 5 Packs Tested](https://saeedseo.com/blog/claude-seo-skills/).

## Results (hard set, URL only)

| Pack | Found /20 | Cost per audit | Missed |
|---|---|---|---|
| [marketingskills](https://github.com/coreyhaines31/marketingskills) (seo-audit) | 20 | $0.54 | none |
| [SE Ranking seo-skills](https://github.com/seranking/seo-skills) (no MCP) | 20 | $0.50 | none |
| [claude-seo](https://github.com/AgriciDaniel/claude-seo) | 18 | $0.45 | X-Robots-Tag noindex header, missing viewport |
| [Hawk Academy](https://hawkacademy.co/claude-seo-skills) | 18 | $0.35 | X-Robots-Tag noindex header, onclick-only link |
| Plain Claude Code (no skill) | 18 | $0.40 | X-Robots-Tag noindex header, missing viewport |
| [open-seo](https://github.com/every-app/open-seo) (no MCP) | 16 | $0.57 | header noindex, JS-only content, schema price mismatch, viewport |

Each pack ran once on the hard set with Claude Sonnet 5.5, and **Codex and Claude Opus graded blind**.

Opus hit a usage limit before marketingskills and SE Ranking, so those two are Codex grades.

The easy set, 19 runs, **barely separated them**: nearly all found 19 or 20. Details are in `results-v1.md` and `results-v2.md`.

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

Each key's sha256 went into `runs-log.md` before run 1, so **the goalposts can't move**:

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

Your audit lands in `work/v2/runs/my-skill-1/audit.md`. **A find scores 1 for the right page and problem**, 0.5 for the right area without the page, and 0 for a miss.

To re-run the 5 packs, clone each at its version from `runs-log.md` into `packs/<name>/`, then run `./round-v2.sh 1`.

## Limits

It's one small site. **It says nothing about local SEO, e-commerce, big sites or links.**

Pack scripts weren't allowed to run, so this tests what each skill tells Claude to do.

## FAQ

### What is the best Claude SEO skill?

On the hard set, **[marketingskills](https://github.com/coreyhaines31/marketingskills) (seo-audit) and [SE Ranking seo-skills](https://github.com/seranking/seo-skills) found all 20**. Plain Claude Code found 18. With one run per pack, I'd read it as a first test.

### Do Claude Code SEO skills beat plain Claude Code?

They didn't on the easy set, where nearly every run found 19 or 20. **The hard set split them:** two packs caught the header-only noindex and the missing viewport tag that plain Claude missed.

### Can I test my own SEO skill or plugin with this?

Yes. The steps are under "Run your own skill on the hard set" above.

### How were the audits graded?

Blind. Codex and Claude Opus scored each audit against the hashed key **without knowing which pack wrote it**.

## Related repos

| Repo | What it is |
|---|---|
| [claude-random-numbers](https://github.com/s77sh/claude-random-numbers) | Which number Claude picks when you ask for a random one |
| [interview-prep-pack](https://github.com/s77sh/interview-prep-pack) | A Claude Code skill that builds interview prep from your own resume |
| [viral-reel-playbook](https://github.com/s77sh/viral-reel-playbook) | A Claude Code skill for Reels, TikTok and Shorts scripts |
| [bali-product-demand](https://github.com/s77sh/bali-product-demand) | Keyword Planner demand for 36 product niches in Bali |

What each one is for: [saeedseo.com/repos/](https://saeedseo.com/repos/).

## Cite

```
Shahriar, S. (2026). Claude SEO Skills Benchmark: 5 Claude Code SEO skill packs audited against 20 planted SEO issues [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23668169
```

Or use GitHub's "Cite this repository" button (`CITATION.cff`).

## License

Code: MIT. Answer keys, results and write-up: CC BY 4.0.

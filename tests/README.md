# Test policy

The default suite tests active code and schemas, not editorial guide content.

```bash
uv run python -m unittest discover -s tests -v
```

It covers:

- source URL validation and canonicalization;
- card-catalog normalization and current-pool validation;
- guide frontmatter/package schema;
- rendering and registry update behavior using synthetic fixtures;
- card-rarity calculations.

It must not assert that a live guide contains a particular card, package, sentence, board, source, or guide count. Those are editorial decisions validated through source audits, previews, and human review.

## Legacy Power tests

The inactive Power/evaluation implementation is retained for historical reference. Its old regression suite lives under `tests/legacy/` and is intentionally excluded from the default publication check.

Run it explicitly only when revisiting that implementation:

```bash
uv run python -m unittest discover -s tests/legacy -p 'test_*.py' -v
```

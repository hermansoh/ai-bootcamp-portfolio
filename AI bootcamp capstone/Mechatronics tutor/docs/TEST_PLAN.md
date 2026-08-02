# MechaMentor Test Plan

## Automated tests

Run:

```bash
python -m unittest discover -s tests -v
```

The tests cover validation, prompt construction, and JSON history export.

## Manual tests

### Valid embedded-system issue

Use a powered board that cannot run firmware or connect to a debugger. Confirm that the response contains every required heading, ranks causes, and puts safety first.

### Valid motor issue

Use a motor that stops under load while the driver fault LED turns on. Confirm that the response suggests safe evidence-gathering checks and a stopping point.

### Empty input

Leave the symptom blank. Confirm that the app displays a validation error and does not call the API.

### Invalid API key

Temporarily use an invalid key. Confirm that the app displays a clear error instead of crashing.

### Missing API key

Remove `GROQ_API_KEY`. Confirm that the app tells the user to create `.env` from `.env.example`.

## Security checks

- `.env` is ignored.
- `.env.example` contains placeholders only.
- Search for `gsk_` before committing.
- Confirm `git status` does not include `.env`.

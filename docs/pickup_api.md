# Pickup API

This document shows the contract for creating pickup requests and example
commands you can give to the frontend team or run locally.

## Endpoint

- POST /pickups
- Content type: `multipart/form-data`
- Authentication: cookie `access_token` (HTTP-only) or Authorization header if you adapt the call.

Form fields (all required unless indicated):

- `category_id` — Accepts either:
  - A numeric id (auto-generated integer), or
  - A category name string (case-insensitive), e.g. `Biodegradable`, `Non-Biodegradable`, `Mixed Waste`.
- `pickup_date` — ISO date string `YYYY-MM-DD`.
- `time_slot` — String identifying the time slot, e.g. `Morning`, `Midday`, `Evening`.

Response: JSON representation of the created `Pickup` (see application responses).

## Example curl (category as name)

Replace `http://localhost:8000` with your server URL and provide a valid
`access_token` cookie (or change to use `Authorization: Bearer <token>`).

```bash
curl -v \
  -b 'access_token=<your_access_cookie>' \
  -F "category_id=Biodegradable" \
  -F "pickup_date=2026-08-13" \
  -F "time_slot=Morning" \
  http://localhost:8000/pickups
```

## Example (sending an image)

```bash
curl -v \
  -b 'access_token=<your_access_cookie>' \
  -F "category_id=Non-Biodegradable" \
  -F "pickup_date=2026-08-14" \
  -F "time_slot=Midday" \
  -F "file=@/path/to/photo.jpg" \
  http://localhost:8000/pickups
```

## Notes for the frontend developer

- The backend accepts human-readable category names, so the UI may send the
  selected label directly (no need to translate to numeric ids).
- If you prefer numeric ids, the endpoint still accepts them.
- Keep category labels matching the seeded names (`Biodegradable`,
  `Non-Biodegradable`, `Mixed Waste`) to ensure correct lookup.

## Local testing helper

See `scripts/pickup_examples.py` in the repository for a small helper that
prints these curl commands and can execute them if you supply `SERVER_URL`
and `ACCESS_TOKEN` environment variables.

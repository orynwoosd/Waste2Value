# Waste2Value

## Bootstrap the site owner

Register the owner through `POST /users` like any other user. Then, on the
server with access to the application's database environment, promote that
existing account once:

```powershell
uv run python bootstrap_owner.py --email owner@example.com --confirm-owner
```

You can use `--phone` instead of `--email`. The command refuses to run if a
`MEGA_USER` already exists, does not accept or set a password, and never
exposes role promotion through the public API. Keep database credentials and
the server environment private.
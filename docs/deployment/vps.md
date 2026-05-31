# VPS Deployment

Status: draft
Last Updated: 2026-05-31

Mendel's Greenhouse can be deployed to a self-managed VPS through Coolify.
GitHub Actions runs quality gates first, then calls the Coolify deploy webhook.

## GitHub Actions

The repository defines two workflows:

- `.github/workflows/ci.yaml`: runs on `push` and `pull_request`, installs
  Python 3.11 and Poetry, runs `poetry run poe check` in `game/`, and verifies
  that the Docker Compose image builds.
- `.github/workflows/deploy-coolify.yaml`: runs after CI succeeds on `main`,
  or manually through `workflow_dispatch`, then calls the Coolify deploy
  webhook.

## Required GitHub Secrets

Configure these in GitHub under
`Settings -> Secrets and variables -> Actions`:

| Secret | Purpose |
| --- | --- |
| `COOLIFY_WEBHOOK` | Deploy webhook URL copied from the Coolify application. |
| `COOLIFY_TOKEN` | Coolify API token with deploy permission. |

## Coolify Preparation

The Coolify application should be linked to this GitHub repository. Configure
it to use the `main` branch and the repository `docker-compose.yml` file.

To make GitHub Actions the deployment gate, disable automatic deploys in
Coolify and let `.github/workflows/deploy-coolify.yaml` call the deploy webhook
after CI passes.

In Coolify:

- Enable API access under Coolify settings.
- Create an API token with deploy permission.
- Open the application, go to Webhooks, and copy the deploy webhook.
- Expose container port `8080`; let Coolify or Docker assign the external
  host port so the deployment does not conflict with other VPS services.

## Runtime Shape

The current deployment is intentionally static:

- `docker-compose.yml` builds `game/Dockerfile`.
- The builder runs Pyxel asset generation, `pyxel package`, and `app2html`.
- The runtime image serves `dist/web/index.html` with
  `python -m http.server`.
- The container healthcheck reads `/health.html`.

Future NiceGUI account and save orchestration should replace or wrap this
static delivery path when that scope is approved in the specs.

## Manual Deployment

The same deployment trigger can be run manually:

```bash
curl --fail --request GET "$COOLIFY_WEBHOOK" \
  --header "Authorization: Bearer $COOLIFY_TOKEN"
```

## Operational Notes

- Keep production environment variables in Coolify; do not commit `.env`.
- Use HTTPS through Coolify's proxy.
- Rebuild the application after changes to Pyxel code, assets, or specs that
  affect the packaged web game.

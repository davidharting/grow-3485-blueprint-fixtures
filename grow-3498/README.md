# GROW-3498 endpoint verification fixture

One Python web service for verifying Blueprint create, branch update, re-plan,
and approval in production. It uses the Python standard library and has no
package-install step.

Use this repository as `source.repo`, `main` as `source.branch`, and
`grow-3498/render.yaml` as `source.path`. Create the Blueprint with
`existingResources: create_new`, a unique name, and `autoSync: false`.
The service also disables automatic deploys from Git pushes.

`plan: starter` selects the smallest paid web-service size: 0.5 CPU and 512 MB
RAM (also called `0.5c-512mb`). See the [compute-plan documentation](https://render.com/docs/compute-plans).
Delete the service after inspection; disconnecting the Blueprint does not
delete it.

## Manual approval input

Supply a nonempty disposable `MANUAL_SECRET` at approval. Use the exact
`serviceType`, `serviceName`, and `key` returned by `requiredManualEnvVars`;
the service name includes a suffix with `create_new`.

Render generates `GENERATED_SECRET`. The app exits before serving HTTP if
either secret or the public version marker is missing or empty. Its response
includes neither secret value.

A local `credentials/app-env.json` file can contain:

```json
{
  "grow3498-endpoint-demo": {
    "MANUAL_SECRET": "replace-with-a-disposable-test-value"
  }
}
```

Keep the actual credentials outside this repository.

## Deployment evidence

`GET /` returns HTTP 200 and JSON with this shape:

```json
{
  "fixture": "grow-3498",
  "version": "version-a",
  "serviceId": "srv-...",
  "commit": "<service-deploy-commit-sha>"
}
```

`serviceId` and `commit` come from Render's [default environment variables](https://render.com/docs/environment-variables).
They are null when running locally without those variables.

For the branch-change scenario, the planned `grow-3498-version-b` branch keeps
this app and service name, and changes two fields in this same render.yaml:

- Service `branch`: `main` → `grow-3498-version-b`.
- `DEPLOYMENT_VERSION`: `version-a` → `version-b`.

PATCH the Blueprint's branch to B, explicitly re-plan, then approve the new
sync. Confirm the response is `version-b`, its service ID is in the Blueprint's
resources, the service belongs to the intended workspace, and its deploy commit
matches B's recorded SHA. Recording all of these connects the HTTP response to
the approved Blueprint instead of merely showing that some app is running.

## Run locally

From the repository root:

```bash
cd grow-3498
MANUAL_SECRET=local-manual GENERATED_SECRET=local-generated \
  DEPLOYMENT_VERSION=version-a PORT=10000 python3 server.py
```

In another terminal, run `curl -i http://localhost:10000/`. Requests to other
paths return HTTP 404.

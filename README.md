# modal-dbt
This repo gives some code to run dbt jobs/actions using [modal](modal.com) which is a serverless application framework. You can test it out by creating a codespace, starting [here](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=685843424&skip_quickstart=true&template=false)

deploy the run_dbt stub via:

```
modal deploy run_dbt.py
```

You'll then need to add [secrets](https://modal.com/docs/guide/secrets) to Modal for database connection credentials (they get passed as env_vars to my [profiles.yml](https://github.com/trouze/dbt-slim-ci/blob/main/profiles.yml)). You should add a web endpoint authentication token as we'll use this to authenticate requests to our run_dbt function triggered via a curl request.

You can then authenticate and trigger your modal dbt job application from anywhere, whether that be python invocation in an orchestration tool, or a simple curl in your unix shell.

```
curl --header "Authorization: Bearer my-auth-token" 'https://trouze--run-dbt-demo-run-dbt.modal.run?repo_url=https://github.com/trouze/dbt-slim-ci.git&dbt_commands=run,-s,stg_customers'
```

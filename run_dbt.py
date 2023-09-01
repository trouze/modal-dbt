from modal import web_endpoint
import modal
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Request

dbt_img = modal.Image.debian_slim().pip_install("dbt-snowflake","GitPython","fastapi").apt_install("git")

auth_scheme = HTTPBearer()
volume = modal.SharedVolume()
stub = modal.Stub("run-dbt-demo")

@stub.function(image=dbt_img,shared_volumes={"/app/dbt": volume},secret=modal.Secret.from_name("a8snowflake"))
@web_endpoint()
def run_dbt(request: Request, token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    from fastapi import HTTPException, status
    import git
    from dbt.cli.main import dbtRunner, dbtRunnerResult
    import os, shutil, re

    # check that request is authenticated ow return http 401
    if token.credentials != os.environ["TOKEN"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    repo_url = request.query_params["repo_url"]
    dbt_commands = request.query_params["dbt_commands"]
    dbt_commands_list = [str(item) for item in dbt_commands.split(',')] if dbt_commands else []
    # get repository name
    repo_name = re.match(r'https://github.com/(.*)/.*', repo_url).group(1)
    save_path = f'/app/dbt/{repo_name}'

    # handle repo removal, clone, and change directory to cloned repo
    shutil.rmtree(save_path,ignore_errors=True)
    repo = git.Repo.clone_from(
        url = repo_url,
        to_path = save_path,
        multi_options = [
            "--depth=1",
            "--single-branch",
            "--branch=main"
        ]
    )
    os.chdir(save_path)

    # run dbt on cloned project
    dbt = dbtRunner()
    deps: dbtRunnerResult = dbt.invoke(['deps'])
    res: dbtRunnerResult = dbt.invoke(dbt_commands_list)
    if res.success == False:
        print("dbt invocation failed")
        print(res.exception)
    else:
        print(res.result)

if __name__ == "__main__":
    with stub.run():
        run_dbt.call()

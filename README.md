# gitlab_stats

## Run

GitLab token scope - `api` and `read repository`

```
docker run --rm -v $PWD/stats/:/app/output --workdir="/app/output/" \
  -e GITLAB_TOKEN=mylongtoken \
  -e GITLAB_URL="https://gitlab.acme.com" \
  -e PROJECT_ID=1234 \
  -e PIPELINE_PAGES=3 \
  unfor19/gitlab_stats    
```

## Build

```
docker build -t unfor19/gitlab_stats .
```

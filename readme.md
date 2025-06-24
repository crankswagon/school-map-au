# deploy


```bash
databricks sync --watch . /Workspace/Users/$user/schoolmap
```

```bash
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

```bash
databricks apps deploy schoolmap --source-code-path /Workspace/Users/$user/schoolmap
```
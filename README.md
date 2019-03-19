# iam-role-assumer v 0.0.2
Simple tool to assume an AWS IAM role in a bash shell


#### Commands:

```
Usage: iam_role_assumer assume [OPTIONS]

  print needed bash variables to assume the indicated role example:
  $(iam_role_assumer assume -r <role-arn>)

Options:
  -r, --role TEXT      IAM role  [required]
  -s, --session TEXT   session name
  -t, --duration TEXT  duration, in seconds, of the role session
  -p, --profile TEXT   profile for the STS client creation
  --region TEXT        AWS region
  --help               Show this message and exit.
```


```
Usage: iam_role_assumer unset [OPTIONS]

  unset the AWS environment variable for an assumed role. example:
  $(iam_role_assumer unset)

Options:
  --help  Show this message and exit.
```

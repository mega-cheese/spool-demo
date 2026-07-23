# spool-demo

TaskFlow is a small Flask to-do list app: users log in, add tasks, and mark them done. Login includes account lockout after repeated failed attempts.

## Setup

```
python3 -m venv venv
./venv/bin/pip install flask pytest
```

## Running the app

```
./venv/bin/python app.py
```

Then visit `http://127.0.0.1:5000`. Default accounts: `alice`/`wonderland`, `bob`/`builder123`, `admin`/`admin`.

## Running tests

```
./venv/bin/python -m pytest
```

## Pull request checks

This repository uses Spool to review pull-request scope, claims, test evidence, and merge readiness.

## Spool review

Pull requests are automatically reviewed by Spool for scope, evidence, and merge readiness.

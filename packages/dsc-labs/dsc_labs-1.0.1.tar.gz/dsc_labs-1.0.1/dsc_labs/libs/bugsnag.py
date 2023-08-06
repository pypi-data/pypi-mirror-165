#! /usr/bin/env python3

import bugsnag


def init_bugsnag(api_key: str, app_dir: str) -> None:
    bugsnag.configure(
        api_key=api_key,
        project_root=app_dir
    )

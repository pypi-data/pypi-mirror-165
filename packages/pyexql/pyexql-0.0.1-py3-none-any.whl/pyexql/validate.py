#!/usr/bin/env python
import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()


def get_sf():
    result = {}
    # Gets the version
    ctx = snowflake.connector.connect(
        user=os.environ.get('sf_user'),
        password=os.environ.get('sf_pass'),
        account=os.environ.get('sf_acct'),
    )
    cs = ctx.cursor()
    try:
        cs.execute("SELECT current_version(), 28*15")
        result = cs.fetchone()
        print(result)
    finally:
        cs.close()
    ctx.close()
    return result

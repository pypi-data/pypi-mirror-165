"""
Configuration for nox.

use `nox list` for whats available
"""

import nox


@nox.session(python=["3.9", "3.10"])
def run_tests(session: nox.Session) -> None:
    """
    Run pytests against 3.9, the most current aws lambda.

    https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
    """
    session.install(".[tests]")
    session.run("pytest")

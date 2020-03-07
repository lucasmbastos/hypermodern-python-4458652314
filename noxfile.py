# Before running this file, be sure to install nox `pip install nox`

import nox

@nox.session(python = ["3.8", "3.7"])
def tests(session):
    args = session.posargs or ['--cov']
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
"""Python-side project management tasks.

Call using “inv”, the PyInvoke CLI.

"""

from invoke import task


@task()
def importcheck(c):
    """Check that a straight Cargo build leaves an importable module."""
    c.run('cargo build')
    c.run('mv target/debug/libpunwrap.so punwrap.so', warn=True)
    script = "import punwrap ; print(punwrap.wrap('long line', 6))"
    c.run(f'python3 -c "{script}"')  # Should print “long\nline”.
    c.run('rm punwrap.so')


@task()
def build_dev(c):
    """Build a Python package for the system Python version only."""
    c.run('maturin build')


@task()
def build_release(c):
    """Build for many Python versions, in Docker."""
    # The output directory is not customized here, expecting target/wheels.
    c.run('docker run --rm -v $(pwd):/io konstin2/maturin build --release')


@task()
def clean(c):
    """Remove artifacts."""
    c.run('rm -rf dist')


@task(pre=[clean, build_release])
def deploy(c):
    """Upload to PyPI.

    This could be done in one step with “maturin publish”, but a flat, more
    transparent process is currently preferred.

    """
    c.run('sudo chown -R $USER:$GROUP target/wheels')
    c.run('mv target/wheels dist')
    c.run('twine check dist/*')
    c.run('twine upload dist/*')

"""Python-side project management tasks."""

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
    c.run('docker run --rm -v $(pwd):/io konstin2/maturin build --release')

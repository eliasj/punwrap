"""Python-side project management tasks.

Call using “inv”, the PyInvoke CLI.

maturin’s build output directories are not customized here, expecting
target/wheels even for sdist.

"""

from invoke import Collection, task

PYTHON_INTERPRETER_VERSIONS = [[3, 8], [3, 9], [3, 10], [3, 11], [3, 12]]
INTERPRETER_STRING = ' '.join(f'--interpreter python{major}.{minor}'
                              for major, minor in PYTHON_INTERPRETER_VERSIONS)


@task()
def importcheck(c):
    """Check that a straight Cargo build leaves an importable module."""
    c.run('rm target/debug/libpunwrap.so', warn=True, hide=True)
    c.run('cargo build')
    c.run('mv target/debug/libpunwrap.so punwrap.so')
    script = "import punwrap ; print(punwrap.wrap('long line', 6))"
    c.run(f'python3 -c "{script}"')  # Should print “long\nline”.
    c.run('rm punwrap.so')


@task()
def build_dev(c):
    """Build a Python package without Docker, for the system Python only."""
    c.run('maturin build')


def _build_in_docker(c, tail: str = ''):
    """Build manylinux-compatible Python wheels.

    As per the manylinux PEPs, building is done on CentOS. Docker is required.
    As of 2023-07, the Docker image used here is recommended in
    https://github.com/PyO3/maturin/tree/main#manylinux-and-auditwheel.
    Artifacts should be compatible with glibc-based Linux distros like Debian.

    """
    c.run('docker run --rm -v $(pwd):/io ghcr.io/pyo3/maturin build '
          f'--release {INTERPRETER_STRING} {tail}')


@task()
def build_manylinux(c):
    """Build manylinux-compatible Python wheels.

    This is the default compatibility mode of maturin.

    """
    _build_in_docker(c)


@task()
def build_musllinux(c):
    """Build musllinux-compatible Python wheels. Ineffective.

    Artifacts should be compatible with Linux distros like Alpine that use musl
    instead of glibc. However, they are not. As of maturin v1.1.0, the program
    accepts the option given here without actually compiling for musl,
    and even if the right --target option is given, the ghcr.io/pyo3/maturin
    image does not have the necessary software to do the work.

    This task is a placeholder for the future addition of local control over a
    more suitable Docker container. In the meantime, see the GitHub workflows
    of this repository.

    """
    _build_in_docker(c, tail='--compatibility musllinux_1_2')  # musl v1.2.x.


@task()
def clean(c, deep=False):
    """Remove artifacts."""
    c.run('sudo chown -R $USER:$GROUP target', warn=True)
    if deep:
        c.sudo('rm -rf target')
    else:
        c.sudo('rm -rf target/wheels')
    c.run('rm -rf dist')


@task(pre=[clean, build_manylinux, build_musllinux], default=True)
def build_all(c):
    """Build to dist/ for distribution. Check results."""
    c.run('sudo chown -R $USER:$GROUP target')
    c.run('mv target/wheels dist')
    c.run('twine check dist/*')


@task(pre=[clean, build_all])
def deploy(c):
    """Build and upload to PyPI. Deprecated.

    This is not the official deployment process any more. Publication happens
    from GitHub Actions.

    """
    c.run('twine upload dist/*')


ns = Collection()  # Namespace; the name “ns” is special to invoke.

build = Collection('build')
build.add_task(build_all, name='all')
build.add_task(build_dev, name='dev')
build.add_task(build_manylinux, name='manylinux')
build.add_task(build_musllinux, name='musllinux')
ns.add_collection(build)

ns.add_task(importcheck)
ns.add_task(clean)
ns.add_task(deploy)

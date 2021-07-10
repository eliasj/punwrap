"""Python-side project management tasks.

Call using “inv”, the PyInvoke CLI.

maturin’s build output directories are not customized here, expecting
target/wheels even for sdist.

"""


from invoke import Collection, task


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
def build_manylinux(c):
    """Build manylinux-compatible Python wheels.

    As per the manylinux PEPs, building is done on CentOS. Docker is required.
    Artifacts should be compatible with glibc-based Linux distros like Debian.

    """
    c.run('docker run --rm -v $(pwd):/io konstin2/maturin build --release')
    c.run('sudo chown -R $USER:$GROUP target')


@task()
def build_musllinux(c):
    """Build musllinux-compatible Python wheels.

    Building happens on the local machine, but with pyenv shims. This task
    thus requires a pyenv installation with each of the listed CPython
    interpreter versions. They are selected to match those of the manylinux
    Docker job (see above) (by major-minor tuple) as of 2022-07.

    Artifacts should be compatible with Linux distros like Alpine that use musl
    instead of glibc.

    """
    target_platform = "musllinux_1_2"  # musl version 1.2.x.
    versions = [[3, 6, 14], [3, 7, 11], [3, 8, 11], [3, 9, 6], [3, 10, "0b3"]]
    base = f'maturin build --release --compatibility {target_platform}'
    for major, minor, fix in versions:
        short = f'{major}.{minor}'
        long = f'{short}.{fix}'
        c.run(f'pyenv install --skip-existing {long}')
        c.run(f'PYENV_VERSION={long} {base} --interpreter python{short}')
    c.run('sudo chown -R $USER:$GROUP target')


@ task()
def clean(c):
    """Remove artifacts."""
    c.run('rm -rf dist')


@ task(pre=[clean, build_manylinux, build_musllinux], default=True)
def build_all(c):
    """Build to dist/ for distribution. Check results."""
    c.run('mv target/wheels dist')
    c.run('twine check dist/*')


@ task(pre=[clean, build_all])
def deploy(c):
    """Build and upload to PyPI.

    This could also be done with “maturin publish”.

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

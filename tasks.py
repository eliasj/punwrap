"""Python-side project management tasks."""

from invoke import task

@task()
def importcheck(c):
    c.run('cargo build')
    c.run('mv target/debug/libpunwrap.so punwrap.so', warn=True)
    script = "import punwrap ; print(punwrap.wrap('long line', 6))"
    c.run(f'python3 -c "{script}"')  # Should print “long\nline”.
    c.run('rm punwrap.so')

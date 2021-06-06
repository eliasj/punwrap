use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use runwrap;

/// Wrap each of the interface functions of runwrap.
#[pyfunction]
fn wrap(raw: &str, width: usize) -> PyResult<String> {
    Ok(runwrap::wrap(raw, width))
}

/// Expose a Python module implemented in Rust.
#[pymodule]
fn punwrap(_: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(wrap, m)?)?;

    Ok(())
}

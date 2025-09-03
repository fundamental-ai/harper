use pyo3_stub_gen::Result;

fn main() -> Result<()> {
    let stub = pyo3_stub_gen::generate_stub_file("harper_py")?;
    std::fs::write("harper_py.pyi", stub)?;
    Ok(())
}
fn main() {
    // Only generate stubs in debug builds to avoid issues during distribution
    if cfg!(debug_assertions) {
        if let Err(e) = generate_stubs() {
            println!("cargo:warning=Failed to generate stubs: {}", e);
        }
    }
}

fn generate_stubs() -> Result<(), Box<dyn std::error::Error>> {
    use pyo3_stub_gen::generate_pyi;
    
    let output = generate_pyi("harper_py")?;
    std::fs::write("harper_py.pyi", output)?;
    Ok(())
}
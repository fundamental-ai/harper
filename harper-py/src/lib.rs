use pyo3::prelude::*;
use pyo3::types::PyModule;
use std::sync::Arc;
use harper_core::spell::{FstDictionary, MergedDictionary, MutableDictionary};
use harper_core::linting::{LintGroup, Linter};
use harper_core::parsers::PlainEnglish;
use harper_core::{Document, Dialect, remove_overlaps, WordMetadata};
use std::fs;

#[pyclass]
pub struct HarperLinter {
    merged_dict: Arc<MergedDictionary>,
    dialect: Dialect,
}

#[pyclass]
pub struct LintError {
    #[pyo3(get)]
    pub start: usize,
    #[pyo3(get)]
    pub end: usize,
    #[pyo3(get)]
    pub message: String,
}

#[pymethods]
impl LintError {
    fn __repr__(&self) -> String {
        format!("LintError(start={}, end={}, message='{}')", self.start, self.end, self.message)
    }
    
    fn __str__(&self) -> String {
        format!("{}-{}: {}", self.start, self.end, self.message)
    }
}

#[pymethods]
impl HarperLinter {
    #[new]
    #[pyo3(signature = (user_dict_path=None, dialect="American"), text_signature = "(user_dict_path: Optional[str] = None, dialect: str = 'American') -> None")]
    fn new(user_dict_path: Option<String>, dialect: &str) -> PyResult<Self> {
        // Setup curated dictionary
        let curated_dict = FstDictionary::curated();
        let mut merged_dict = MergedDictionary::new();
        merged_dict.add_dictionary(curated_dict);
        
        // Load user dictionary if provided
        if let Some(dict_path) = user_dict_path {
            match load_user_dict(&dict_path) {
                Ok(user_dict) => merged_dict.add_dictionary(Arc::new(user_dict)),
                Err(e) => {
                    eprintln!("Warning: Could not load user dictionary {}: {}", dict_path, e);
                }
            }
        }
        
        let dialect = match dialect {
            "American" => Dialect::American,
            "British" => Dialect::British,
            _ => Dialect::American,
        };
        
        Ok(HarperLinter {
            merged_dict: Arc::new(merged_dict),
            dialect,
        })
    }
    
    /// Count grammar errors in text
    #[pyo3(text_signature = "(text: str) -> int")]
    fn count_errors(&self, text: &str) -> usize {
        let doc = Document::new(text, &PlainEnglish, &*self.merged_dict);
        let mut linter = LintGroup::new_curated(self.merged_dict.clone(), self.dialect);
        let lints = linter.lint(&doc);
        lints.len()
    }
    
    /// Get detailed lint results
    #[pyo3(text_signature = "(text: str) -> List[LintError]")]
    fn lint(&self, text: &str) -> Vec<LintError> {
        let doc = Document::new(text, &PlainEnglish, &*self.merged_dict);
        let mut linter = LintGroup::new_curated(self.merged_dict.clone(), self.dialect);
        let mut lints = linter.lint(&doc);
        
        remove_overlaps(&mut lints);
        
        lints
            .into_iter()
            .map(|lint| LintError {
                start: lint.span.start,
                end: lint.span.end,
                message: lint.message,
            })
            .collect()
    }
    
    /// Check if text has any errors (faster than count_errors for just boolean check)
    #[pyo3(text_signature = "(text: str) -> bool")]
    fn has_errors(&self, text: &str) -> bool {
        let doc = Document::new(text, &PlainEnglish, &*self.merged_dict);
        let mut linter = LintGroup::new_curated(self.merged_dict.clone(), self.dialect);
        let lints = linter.lint(&doc);
        !lints.is_empty()
    }
    
    fn __repr__(&self) -> String {
        format!("HarperLinter(dialect={:?})", self.dialect)
    }
}

// Helper function to load user dictionary
fn load_user_dict(path: &str) -> Result<MutableDictionary, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(path)?;
    let mut dict = MutableDictionary::new();
    
    dict.extend_words(
        content.lines()
            .map(|l| (l.chars().collect::<Vec<_>>(), WordMetadata::default())),
    );
    
    Ok(dict)
}

#[pymodule]
#[pyo3(name = "harper_py")]
fn harper_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<HarperLinter>()?;
    m.add_class::<LintError>()?;
    
    // Add module-level documentation
    m.add("__doc__", "Python bindings for Harper grammar checker")?;
    m.add("__version__", "0.1.7")?;
    
    Ok(())
}
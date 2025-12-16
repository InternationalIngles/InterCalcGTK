use evalexpr::eval;
use anyhow::{Result, Context};

pub fn safe_eval(expression: &str) -> Result<f64> {
    let value = eval(expression).context("Failed to evaluate expression")?;
    match value {
        evalexpr::Value::Float(f) => Ok(f),
        evalexpr::Value::Int(i) => Ok(i as f64),
        _ => anyhow::bail!("Result is not a number"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_eval() {
        assert_eq!(safe_eval("2 + 2").unwrap(), 4.0);
        assert_eq!(safe_eval("10 / 2").unwrap(), 5.0);
        assert_eq!(safe_eval("2 * 3 + 4").unwrap(), 10.0);
    }
}

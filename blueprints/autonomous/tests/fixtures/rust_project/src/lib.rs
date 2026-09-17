pub mod ledger;
pub mod math;

pub fn total(values: &[i64]) -> i64 {
    values.iter().fold(0, |acc, v| math::add(acc, *v))
}

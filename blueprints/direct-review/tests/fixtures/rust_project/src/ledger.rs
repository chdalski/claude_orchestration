use crate::math;

pub struct Ledger {
    entries: Vec<i64>,
}

impl Ledger {
    pub fn add(&mut self, amount: i64) {
        self.entries.push(amount);
    }

    pub fn balance(&self) -> i64 {
        self.entries.iter().fold(0, |acc, v| math::add(acc, *v))
    }
}

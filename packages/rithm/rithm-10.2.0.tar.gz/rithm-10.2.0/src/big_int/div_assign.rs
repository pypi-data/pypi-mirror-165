use std::ops::DivAssign;

use crate::constants::UNDEFINED_DIVISION_ERROR_MESSAGE;

use super::digits::CheckedDivComponents;
use super::types::BigInt;

impl<
        Digit: CheckedDivComponents,
        const SEPARATOR: char,
        const SHIFT: usize,
    > DivAssign for BigInt<Digit, SEPARATOR, SHIFT>
{
    fn div_assign(&mut self, divisor: Self) {
        (self.sign, self.digits) = Digit::checked_div_components::<SHIFT>(
            self.sign,
            &self.digits,
            divisor.sign,
            &divisor.digits,
        )
        .expect(UNDEFINED_DIVISION_ERROR_MESSAGE);
    }
}

impl<
        Digit: CheckedDivComponents,
        const SEPARATOR: char,
        const SHIFT: usize,
    > DivAssign<&Self> for BigInt<Digit, SEPARATOR, SHIFT>
{
    fn div_assign(&mut self, divisor: &Self) {
        (self.sign, self.digits) = Digit::checked_div_components::<SHIFT>(
            self.sign,
            &self.digits,
            divisor.sign,
            &divisor.digits,
        )
        .expect(UNDEFINED_DIVISION_ERROR_MESSAGE);
    }
}

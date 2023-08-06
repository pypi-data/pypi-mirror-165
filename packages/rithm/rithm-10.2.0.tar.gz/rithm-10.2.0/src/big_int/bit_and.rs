use std::ops::BitAnd;

use super::digits::BitwiseAndComponents;
use super::types::BigInt;

impl<
        Digit: BitwiseAndComponents,
        const SEPARATOR: char,
        const SHIFT: usize,
    > BitAnd for BigInt<Digit, SEPARATOR, SHIFT>
{
    type Output = Self;

    fn bitand(self, other: Self) -> Self::Output {
        let (sign, digits) = Digit::bitwise_and_components::<SHIFT>(
            self.sign,
            self.digits,
            other.sign,
            other.digits,
        );
        Self::Output { sign, digits }
    }
}

impl<
        Digit: BitwiseAndComponents + Clone,
        const SEPARATOR: char,
        const SHIFT: usize,
    > BitAnd<&Self> for BigInt<Digit, SEPARATOR, SHIFT>
{
    type Output = Self;

    fn bitand(self, other: &Self) -> Self::Output {
        let (sign, digits) = Digit::bitwise_and_components::<SHIFT>(
            self.sign,
            self.digits,
            other.sign,
            other.digits.clone(),
        );
        Self::Output { sign, digits }
    }
}

impl<
        Digit: BitwiseAndComponents + Clone,
        const SEPARATOR: char,
        const SHIFT: usize,
    > BitAnd<BigInt<Digit, SEPARATOR, SHIFT>>
    for &BigInt<Digit, SEPARATOR, SHIFT>
{
    type Output = BigInt<Digit, SEPARATOR, SHIFT>;

    fn bitand(self, other: BigInt<Digit, SEPARATOR, SHIFT>) -> Self::Output {
        let (sign, digits) = Digit::bitwise_and_components::<SHIFT>(
            self.sign,
            self.digits.clone(),
            other.sign,
            other.digits,
        );
        Self::Output { sign, digits }
    }
}

impl<
        Digit: BitwiseAndComponents + Clone,
        const SEPARATOR: char,
        const SHIFT: usize,
    > BitAnd for &BigInt<Digit, SEPARATOR, SHIFT>
{
    type Output = BigInt<Digit, SEPARATOR, SHIFT>;

    fn bitand(self, other: Self) -> Self::Output {
        let (sign, digits) = Digit::bitwise_and_components::<SHIFT>(
            self.sign,
            self.digits.clone(),
            other.sign,
            other.digits.clone(),
        );
        Self::Output { sign, digits }
    }
}

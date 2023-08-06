use std::fmt;
use std::ops::Neg;

use traiter::numbers::{CheckedDiv, Gcd, Signed, Zeroable};

use crate::big_int::BigInt;

pub struct Fraction<Component> {
    pub(super) numerator: Component,
    pub(super) denominator: Component,
}

impl<Component: Clone> Clone for Fraction<Component> {
    fn clone(&self) -> Self {
        Self {
            numerator: self.numerator.clone(),
            denominator: self.denominator.clone(),
        }
    }

    fn clone_from(&mut self, source: &Self) {
        (self.numerator, self.denominator) =
            (source.numerator.clone(), source.denominator.clone());
    }
}

impl<
        Component: NormalizeModuli<Output = (Component, Component)>
            + NormalizeSign<Output = (Component, Component)>
            + Zeroable,
    > Fraction<Component>
{
    pub fn new(
        mut numerator: Component,
        mut denominator: Component,
    ) -> Option<Self> {
        if denominator.is_zero() {
            None
        } else {
            (numerator, denominator) =
                Component::normalize_sign(numerator, denominator);
            (numerator, denominator) =
                Component::normalize_moduli(numerator, denominator);
            Some(Self {
                numerator,
                denominator,
            })
        }
    }
}

impl<Component> Fraction<Component> {
    pub fn denominator(&self) -> &Component {
        &self.denominator
    }

    pub fn numerator(&self) -> &Component {
        &self.numerator
    }
}

pub trait NormalizeModuli<Other = Self> {
    type Output;

    fn normalize_moduli(self, other: Other) -> Self::Output;
}

impl<Digit, const SEPARATOR: char, const SHIFT: usize> NormalizeModuli
    for BigInt<Digit, SEPARATOR, SHIFT>
where
    for<'a> Self: CheckedDiv<Output = Option<Self>>
        + CheckedDiv<&'a Self, Output = Option<Self>>,
    for<'a> &'a Self: Gcd<Output = Self>,
{
    type Output = (Self, Self);

    #[inline]
    fn normalize_moduli(self, other: Self) -> Self::Output {
        let gcd = self.gcd(&other);
        (
            unsafe { self.checked_div(&gcd).unwrap_unchecked() },
            unsafe { other.checked_div(gcd).unwrap_unchecked() },
        )
    }
}

impl<Digit, const SEPARATOR: char, const SHIFT: usize> NormalizeModuli<&Self>
    for BigInt<Digit, SEPARATOR, SHIFT>
where
    for<'a> Self: CheckedDiv<&'a Self, Output = Option<Self>>,
    for<'a> &'a Self:
        CheckedDiv<Self, Output = Option<Self>> + Gcd<Output = Self>,
{
    type Output = (Self, Self);

    #[inline]
    fn normalize_moduli(self, other: &Self) -> Self::Output {
        let gcd = self.gcd(other);
        (
            unsafe { self.checked_div(&gcd).unwrap_unchecked() },
            unsafe { other.checked_div(gcd).unwrap_unchecked() },
        )
    }
}

impl<Digit, const SEPARATOR: char, const SHIFT: usize>
    NormalizeModuli<BigInt<Digit, SEPARATOR, SHIFT>>
    for &BigInt<Digit, SEPARATOR, SHIFT>
where
    for<'a> &'a BigInt<Digit, SEPARATOR, SHIFT>: CheckedDiv<Output = Option<BigInt<Digit, SEPARATOR, SHIFT>>>
        + Gcd<Output = BigInt<Digit, SEPARATOR, SHIFT>>,
    BigInt<Digit, SEPARATOR, SHIFT>:
        CheckedDiv<Output = Option<BigInt<Digit, SEPARATOR, SHIFT>>>,
{
    type Output = (
        BigInt<Digit, SEPARATOR, SHIFT>,
        BigInt<Digit, SEPARATOR, SHIFT>,
    );

    #[inline]
    fn normalize_moduli(
        self,
        other: BigInt<Digit, SEPARATOR, SHIFT>,
    ) -> Self::Output {
        let gcd = self.gcd(&other);
        (
            unsafe { self.checked_div(&gcd).unwrap_unchecked() },
            unsafe { other.checked_div(gcd).unwrap_unchecked() },
        )
    }
}

impl<Digit, const SEPARATOR: char, const SHIFT: usize> NormalizeModuli
    for &BigInt<Digit, SEPARATOR, SHIFT>
where
    for<'a> &'a BigInt<Digit, SEPARATOR, SHIFT>: CheckedDiv<Output = Option<BigInt<Digit, SEPARATOR, SHIFT>>>
        + CheckedDiv<
            BigInt<Digit, SEPARATOR, SHIFT>,
            Output = Option<BigInt<Digit, SEPARATOR, SHIFT>>,
        > + Gcd<Output = BigInt<Digit, SEPARATOR, SHIFT>>,
{
    type Output = (
        BigInt<Digit, SEPARATOR, SHIFT>,
        BigInt<Digit, SEPARATOR, SHIFT>,
    );

    #[inline]
    fn normalize_moduli(self, other: Self) -> Self::Output {
        let gcd = self.gcd(other);
        (
            unsafe { self.checked_div(&gcd).unwrap_unchecked() },
            unsafe { other.checked_div(gcd).unwrap_unchecked() },
        )
    }
}

macro_rules! integer_normalize_moduli_impl {
    ($($integer:ty)*) => ($(
        impl NormalizeModuli for $integer {
            type Output = (Self, Self);

            #[inline]
            fn normalize_moduli(self, other: Self) -> Self::Output {
                let gcd = self.gcd(other);
                (
                    unsafe { self.checked_div(gcd).unwrap_unchecked() },
                    unsafe { other.checked_div(gcd).unwrap_unchecked() },
                )
            }
        }
    )*)
}

integer_normalize_moduli_impl!(
    i8 i16 i32 i64 i128 isize u8 u16 u32 u64 u128 usize
);

pub trait NormalizeSign<Other = Self> {
    type Output;

    fn normalize_sign(self, other: Other) -> Self::Output;
}

impl<Digit, const SEPARATOR: char, const SHIFT: usize> NormalizeSign
    for BigInt<Digit, SEPARATOR, SHIFT>
where
    Self: Neg<Output = Self> + Signed,
{
    type Output = (Self, Self);

    #[inline]
    fn normalize_sign(self, other: Self) -> Self::Output {
        if other.is_negative() {
            (-self, -other)
        } else {
            (self, other)
        }
    }
}

macro_rules! signed_integer_normalize_sign_impl {
    ($($integer:ty)*) => ($(
        impl NormalizeSign for $integer {
            type Output = (Self, Self);

            #[inline]
            fn normalize_sign(self, other: Self) -> Self::Output {
                if other.is_negative() {
                    (-self, -other)
                } else {
                    (self, other)
                }
            }
        }
    )*)
}

signed_integer_normalize_sign_impl!(i8 i16 i32 i64 i128 isize);

macro_rules! unsigned_integer_normalize_sign_impl {
    ($($integer:ty)*) => ($(
        impl NormalizeSign for $integer {
            type Output = (Self, Self);

            #[inline(always)]
            fn normalize_sign(self, other: Self) -> Self::Output {
                (self, other)
            }
        }
    )*)
}

unsigned_integer_normalize_sign_impl!(u8 u16 u32 u64 u128 usize);

#[derive(Clone, Copy, Eq, PartialEq)]
pub enum FromFloatConversionError {
    Infinity,
    NaN,
    OutOfBounds,
}

impl FromFloatConversionError {
    fn description(&self) -> &str {
        match self {
            FromFloatConversionError::Infinity => {
                "Conversion of infinity is undefined."
            }
            FromFloatConversionError::NaN => "Conversion of NaN is undefined.",
            FromFloatConversionError::OutOfBounds => "Value is out of bounds.",
        }
    }
}

impl fmt::Debug for FromFloatConversionError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(self.description())
    }
}

impl fmt::Display for FromFloatConversionError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> std::fmt::Result {
        fmt::Display::fmt(&self.description(), formatter)
    }
}

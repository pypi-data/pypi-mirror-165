use std::iter::Peekable;
use std::str::Chars;

use traiter::numbers::{Unitary, Zeroable};

use crate::traits::HasSignBit;

use super::constants::{MAX_REPRESENTABLE_BASE, MIN_REPRESENTABLE_BASE};
use super::contracts::is_valid_shift;
use super::digits::{to_digits_sign, BinaryBaseFromDigits};
use super::types::{BigInt, Sign, TryFromStringError};

pub trait TryFromString: Sized {
    fn try_from_string(
        string: &str,
        base: u8,
    ) -> Result<Self, TryFromStringError>;
}

const ASCII_CODES_DIGIT_VALUES: [u8; 256] = [
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 0, 1, 2, 3, 4, 5, 6, 7, 8,
    9, 37, 37, 37, 37, 37, 37, 37, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 37, 37,
    37, 37, 37, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
];

impl<
        Digit: BinaryBaseFromDigits<u8> + HasSignBit + Zeroable,
        const SEPARATOR: char,
        const SHIFT: usize,
    > TryFromString for BigInt<Digit, SEPARATOR, SHIFT>
{
    fn try_from_string(
        string: &str,
        mut base: u8,
    ) -> Result<Self, TryFromStringError> {
        debug_assert!(is_valid_shift::<Digit, SHIFT>());
        debug_assert!(
            ASCII_CODES_DIGIT_VALUES[SEPARATOR as usize]
                >= MAX_REPRESENTABLE_BASE
        );
        debug_assert!(
            base == 0
                || (MIN_REPRESENTABLE_BASE..=MAX_REPRESENTABLE_BASE)
                    .contains(&base)
        );
        let mut characters = string.trim().chars().peekable();
        let sign = parse_sign(&mut characters);
        if base == 0 {
            base = guess_base(&mut characters);
        };
        skip_prefix::<SEPARATOR>(&mut characters, base);
        parse_digits::<SEPARATOR>(characters, base).map(|digits| {
            let digits = Digit::binary_base_from_digits::<SHIFT>(
                &digits,
                base as usize,
            );
            Self {
                sign: sign * to_digits_sign(&digits),
                digits,
            }
        })
    }
}
#[inline]
fn guess_base(characters: &mut Peekable<Chars>) -> u8 {
    if characters.peek() != Some(&'0') {
        10
    } else {
        match characters.clone().nth(1) {
            Some('b') | Some('B') => 2,
            Some('o') | Some('O') => 8,
            Some('x') | Some('X') => 16,
            _ => 10,
        }
    }
}

#[inline]
fn parse_digits<const SEPARATOR: char>(
    mut characters: Peekable<Chars>,
    base: u8,
) -> Result<Vec<u8>, TryFromStringError> {
    if characters.peek() == Some(&SEPARATOR) {
        return Err(TryFromStringError::StartsWithSeparator);
    }
    let mut result: Vec<u8> = Vec::new();
    let mut prev: char = SEPARATOR;
    for character in characters {
        if character != SEPARATOR {
            let digit = ASCII_CODES_DIGIT_VALUES[character as usize];
            if digit >= base {
                return Err(TryFromStringError::InvalidDigit(character, base));
            }
            result.push(digit);
        } else if prev == SEPARATOR {
            return Err(TryFromStringError::ConsecutiveSeparators);
        }
        prev = character;
    }
    if prev == SEPARATOR {
        return Err(TryFromStringError::EndsWithSeparator);
    }
    result.reverse();
    Ok(result)
}

#[inline]
fn parse_sign(characters: &mut Peekable<Chars>) -> i8 {
    if characters.peek() == Some(&'-') {
        characters.next();
        -Sign::one()
    } else if characters.peek() == Some(&'+') {
        characters.next();
        Sign::one()
    } else {
        Sign::one()
    }
}

fn skip_prefix<const SEPARATOR: char>(
    characters: &mut Peekable<Chars>,
    base: u8,
) {
    if characters.peek() == Some(&'0') {
        match characters.clone().nth(1) {
            Some('b') | Some('B') => {
                if base == 2 {
                    characters.nth(1);
                    characters.next_if_eq(&SEPARATOR);
                }
            }
            Some('o') | Some('O') => {
                if base == 8 {
                    characters.nth(1);
                    characters.next_if_eq(&SEPARATOR);
                }
            }
            Some('x') | Some('X') => {
                if base == 16 {
                    characters.nth(1);
                    characters.next_if_eq(&SEPARATOR);
                }
            }
            _ => {}
        };
    };
}

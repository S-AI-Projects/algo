---
id: rust-functions
title: Rust Functions
sidebar_position: 3
description: Learn about functions in Rust with examples.
---

# Rust Functions

Functions are reusable blocks of code used to perform a specific task.

Functions help make programs:

- Cleaner
- Reusable
- Easy to understand
- Easy to maintain

In Rust, the `main()` function is the starting point of every program.

## Video Explanation

<LiteYouTubeEmbed
  id="SqT5YglW3qU"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Rust Functions Are Weird (But Be Glad)"
  lazyLoad={true}
  webp
/>

---

# Basic Function Syntax

Functions are created using the `fn` keyword.

## Syntax

```rust
fn function_name() {
    // code
}
```

## Example

```rust
fn greet() {
    println!("Welcome to Rust!");
}

fn main() {
    greet();
}
```

### Output

```text
Welcome to Rust!
```

---

# Function Parameters

Functions can accept values called parameters.

Parameters are written inside parentheses.

## Example

```rust
fn greet(name: &str) {
    println!("Hello, {}", name);
}

fn main() {
    greet("Hemlata");
}
```

### Output

```text
Hello, Hemlata
```

---

# Multiple Parameters

A function can have multiple parameters.

## Example

```rust
fn add(a: i32, b: i32) {
    println!("Sum: {}", a + b);
}

fn main() {
    add(10, 20);
}
```

### Output

```text
Sum: 30
```

---

# Function Return Values

Functions can return values using the return type syntax `->`.

## Example

```rust
fn square(num: i32) -> i32 {
    num * num
}

fn main() {
    let result = square(5);

    println!("Square: {}", result);
}
```

### Output

```text
Square: 25
```

In Rust, the last expression without a semicolon is automatically returned.

---

# Using the `return` Keyword

Rust also allows returning values using the `return` keyword.

## Example

```rust
fn multiply(a: i32, b: i32) -> i32 {
    return a * b;
}

fn main() {
    let result = multiply(4, 5);

    println!("Result: {}", result);
}
```

### Output

```text
Result: 20
```

---

# Functions Without Return Value

Functions that do not return anything have a return type of `()` called the unit type.

## Example

```rust
fn message() {
    println!("This function returns nothing.");
}

fn main() {
    message();
}
```

---

# Function with Boolean Return Type

Functions can also return boolean values.

## Example

```rust
fn is_even(num: i32) -> bool {
    num % 2 == 0
}

fn main() {
    println!("{}", is_even(10));
    println!("{}", is_even(7));
}
```

### Output

```text
true
false
```

---

# Calling Functions Multiple Times

Functions can be reused multiple times in a program.

## Example

```rust
fn greet() {
    println!("Hello from Rust!");
}

fn main() {
    greet();
    greet();
    greet();
}
```

### Output

```text
Hello from Rust!
Hello from Rust!
Hello from Rust!
```

---

# Function Expressions

The last line of a function can act as an expression.

## Example

```rust
fn sum(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    let result = sum(3, 7);

    println!("{}", result);
}
```

### Output

```text
10
```

---

# Nested Function Calls

One function can call another function.

## Example

```rust
fn display() {
    println!("Display Function");
}

fn show() {
    display();
    println!("Show Function");
}

fn main() {
    show();
}
```

### Output

```text
Display Function
Show Function
```

---

# Function Ownership Example

Rust follows ownership rules even in functions.

## Example

```rust
fn print_text(text: String) {
    println!("{}", text);
}

fn main() {
    let message = String::from("Rust");

    print_text(message);
}
```

After passing `message`, ownership moves to the function.

---

# Mutable Parameters Example

Functions can work with mutable values.

## Example

```rust
fn main() {
    let mut number = 10;

    increase(&mut number);

    println!("{}", number);
}

fn increase(num: &mut i32) {
    *num += 1;
}
```

### Output

```text
11
```

---

## Function Invariant and Bounded Variations

- **Precise Invariant:** For any `i32` arguments `(a, b)` within non-overflowing bounds (`|a|, |b| <= 1_000_000`), calling `sum(a, b)` evaluates its final expression `a + b` without mutating caller variables (`i32` implements `Copy`) and satisfies commutativity (`sum(a, b) == sum(b, a)`) and additive identity (`sum(a, 0) == a`).
- **Concrete Intermediate State:** On the worked fixture `(x = 3, y = 7)`, calling `sum(x, y)` copies `3` and `7` into parameters `a` and `b`, evaluates `3 + 7 -> 10`, returns `10`, and preserves `(x, y) == (3, 7)`.
- **Boundary Contract (`fn function_name()` and `sum(0, 0)`):** A zero-parameter function `noop()` returns the unit type `()` with no side effects, and `sum(0, 0)` returns `0`.

```rust
fn noop() {}

fn greet_message() -> String {
    String::from("Welcome to Rust!")
}

fn sum(a: i32, b: i32) -> i32 {
    a + b
}

fn main() {
    println!("Worked example (greet): {}", greet_message());
    let (x, y) = (3, 7);
    let worked = sum(x, y);
    assert_eq!((x, y), (3, 7));
    println!("Worked example (sum(3, 7)): {}", worked);

    assert_eq!(noop(), ());
    println!("Boundary example (noop -> (), sum(0, 0)): {}", sum(0, 0));

    let cases = [
        ("Invariant fixture", 3, 7, 10),
        ("Variation 1", -5, 5, 0),
        ("Variation 2", 10, -3, 7),
        ("Variation 3", 0, 42, 42),
        ("Variation 4", -12, -8, -20),
        ("Variation 5", 100, 250, 350),
    ];

    for &(label, a, b, expected) in &cases {
        let forward = sum(a, b);
        let reverse = sum(b, a);
        assert_eq!(forward, expected);
        assert_eq!(forward, reverse);
        assert_eq!(sum(a, 0), a);
        println!("{} ({}, {}) => {}", label, a, b, forward);
    }
    println!("All 6 invariant cases verified!");
}
```

### Output

```text
Worked example (greet): Welcome to Rust!
Worked example (sum(3, 7)): 10
Boundary example (noop -> (), sum(0, 0)): 0
Invariant fixture (3, 7) => 10
Variation 1 (-5, 5) => 0
Variation 2 (10, -3) => 7
Variation 3 (0, 42) => 42
Variation 4 (-12, -8) => -20
Variation 5 (100, 250) => 350
All 6 invariant cases verified!
```

# Advantages of Functions

Functions provide many benefits:

- Code reusability
- Better readability
- Easier debugging
- Organized programs
- Reduced code duplication

---

# Summary

Functions are one of the most important parts of Rust programming.

## Important Points

- Functions are declared using `fn`
- Parameters allow passing values
- Functions can return values
- Rust supports expression-based returns
- Functions improve code organization and reusability

Functions help developers write clean, modular, and efficient Rust programs.
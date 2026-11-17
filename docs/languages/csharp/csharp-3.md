---
id: functions-in-csharp
sidebar_position: 3
title: "Functions in C#"
sidebar_label: "Functions in C#"
---

# Functions in C#

Functions, also known as methods, in C# are blocks of code that perform a specific task. They help modularize code and promote reusability.

## Video Explanation

<LiteYouTubeEmbed
  id="IPpEefuFiVM"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="C# methods 📞"
  lazyLoad={true}
  webp
/>

---

## 1. Structure of a Function

The basic structure of a function in C# includes an access modifier, return type, name, parameters (optional), and a body.

```csharp
[access_modifier] return_type FunctionName([parameters]) {
    // Function body
}
```

### Example:

```csharp
public int Add(int a, int b) {
    return a + b;
}
```

---

## 2. Access Modifiers

C# functions use access modifiers to control their visibility and accessibility:

- **public**: Accessible from any class.
- **private**: Accessible only within the containing class.
- **protected**: Accessible within the containing class and derived classes.
- **internal**: Accessible within the same assembly.
- **protected internal**: Accessible within the same assembly or derived classes.

---

## 3. Return Types

A function in C# can have any data type as its return type or be `void` if it returns no value.

### Example:

```csharp
public int Multiply(int x, int y) {
    return x * y; // returns an integer
}

public void DisplayMessage() {
    Console.WriteLine("Hello, World!"); // returns no value
}
```

---

## 4. Parameters and Arguments

Functions can take parameters as input. Parameters are defined in the function signature, and arguments are the actual values passed.

### Example:

```csharp
public int Subtract(int a, int b) {
    return a - b;
}

// Usage
int result = Subtract(10, 5); // Passes 10 and 5 as arguments
```

### Copy and Resource Behavior of Value Parameters

The original `Subtract(10, 5)` call performs a fixed number of integer operations and returns `5`. The example below also shows what the parameter receives when the argument is an `int` or an array:

```csharp
using System;

public class FunctionResourceDemo
{
    static int Subtract(int a, int b) => a - b;

    static void Increment(int value)
    {
        value++;
    }

    static void ReplaceFirst(int[] values)
    {
        values[0] = 99;
    }

    public static void Main()
    {
        Console.WriteLine($"Subtract(10, 5) = {Subtract(10, 5)}");

        int score = 5;
        Increment(score);
        Console.WriteLine($"int after method = {score}");

        int[] scores = { 5 };
        ReplaceFirst(scores);
        Console.WriteLine($"array element after method = {scores[0]}");

        Console.WriteLine($"Subtract(5, 5) = {Subtract(5, 5)}");
    }
}
```

**Expected output:**

```text
Subtract(10, 5) = 5
int after method = 5
array element after method = 99
Subtract(5, 5) = 0
```

Each call above uses a fixed number of operations: time is $O(1)$. `Increment` receives a copy of the `int`, so changing its local parameter leaves `score` as `5`. `ReplaceFirst` receives a copy of the array reference; that reference still points to the caller's same array, so writing `values[0]` changes the caller-visible element. The call copies one reference and does not copy the array or allocate a replacement array, so its extra parameter storage is $O(1)$. The equal-arguments boundary `Subtract(5, 5)` returns `0`.

---

## 5. Method Overloading

Method overloading allows multiple methods to have the same name but different parameters.

### Example:

```csharp
public int Add(int a, int b) {
    return a + b;
}

public double Add(double a, double b) {
    return a + b;
}
```

---

## 6. Static Methods

Static methods belong to the class rather than an instance and can be called directly using the class name.

### Example:

```csharp
public static void PrintMessage() {
    Console.WriteLine("This is a static method.");
}

// Usage
ClassName.PrintMessage();
```

---

## 7. Recursive Functions

A recursive function is one that calls itself until a base condition is met.

### Example:

```csharp
public int Factorial(int n) {
    if (n <= 1) return 1;
    return n * Factorial(n - 1);
}
```

---

## 8. Lambda Expressions

Lambda expressions provide a concise syntax to define anonymous functions.

### Example:

```csharp
Func<int, int> square = x => x * x;
Console.WriteLine(square(5)); // Outputs: 25
```

---

## 9. Async Functions

Async functions allow asynchronous programming, making use of the `async` and `await` keywords.

### Example:

```csharp
public async Task<string> GetDataAsync() {
    await Task.Delay(1000); // Simulates asynchronous operation
    return "Data loaded";
}
```

---

## Summary

Functions are essential in C# for creating reusable, organized, and maintainable code. Understanding the types, access modifiers, and usage of functions will enhance your programming capabilities.

Happy coding!

# Issue #21: R61-T021 — Make the C# 9 Example Executable

## Overview
This task completes GitHub Issue #21 for task `R61-T021` in the `S-AI-Projects/algo` repository. The assigned work makes the C# 9 interface documentation example in `docs/languages/csharp/csharp-9.md` executable, demonstrates interface polymorphism directly, preserves the article's literal worked-example input and expected output, adds a boundary case adhering to the interface contract, and establishes an automated validation suite.

## Implementation Details

### Target Article
- **File**: `docs/languages/csharp/csharp-9.md`
- **Section Anchor**: `1. What is an Interface?` / `2. Implementing an Interface`

### Code Changes
1. **Direct Interface Demonstration**:
   - Updated the reference declarations to use the interface type `IAnimal` rather than concrete `Dog`:
     ```csharp
     IAnimal dog = new Dog();
     dog.MakeSound();  // Outputs "Bark"
     ```
2. **Preserved Worked Example**:
   - `Dog` implements `IAnimal` and invokes `MakeSound()`, generating the literal output `"Bark"`.
3. **Boundary Example Added**:
   - Added class `Fish : IAnimal` to demonstrate a silent animal boundary condition conforming to the `void MakeSound()` interface contract:
     ```csharp
     class Fish : IAnimal {
         public void MakeSound() {
             Console.WriteLine("Silence");
         }
     }
     ```
   - In `Main()`, invoked via interface reference:
     ```csharp
     IAnimal fish = new Fish();
     fish.MakeSound();  // Outputs "Silence"
     ```
4. **Enhanced Documentation Explanation**:
   - Clarified the concrete input (`MakeSound()` method calls), runtime dynamic dispatch intermediate state, and expected output (`"Bark"` and `"Silence"`).

## Verification and Check Script

### `work/R61-T021/check.py`
The validation script:
- Reads `docs/languages/csharp/csharp-9.md` directly.
- Extracts the actual C# code block containing `interface IAnimal` and `class Program`.
- Dynamically queries `dotnet --version` and targets the appropriate Target Framework Moniker (e.g., `net11.0`).
- Compiles and executes the extracted C# source in an isolated temporary directory via `dotnet run`.
- Asserts that stdout contains the exact expected outputs:
  1. `"Bark"` (worked example)
  2. `"Silence"` (boundary condition)
- Validates that a deliberately incorrect comparison (negative test) raises an `AssertionError`.
- Propagates errors with appropriate exit codes.

## Test Results
- `python3 work/R61-T021/check.py`: **PASS**
- `npm run validate:docs`: **PASS** (0 errors, 0 warnings across 946 files)
- `npm run build`: **PASS** (Static pages generated successfully in production mode)

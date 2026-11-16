---
id: sql-case-expression
sidebar_position: 26
title: "SQL CASE Expression"
sidebar_label: "SQL CASE"
description: "The SQL CASE expression is used to add conditional logic to SQL queries."
tags: [sql, dbms, database, case, conditional]
---

The `CASE` expression in SQL is used to apply conditional logic within a query. It allows you to return different values based on specific conditions, similar to an `if-else` statement in programming.

### Video Explanation

<LiteYouTubeEmbed
  id="Twusw__OzA8"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Intermediate SQL Tutorial | Case Statement | Use Cases"
  lazyLoad={true}
  webp
/>

### Syntax

There are two main formats for the `CASE` expression: **Simple CASE** and **Searched CASE**.

#### Simple CASE

```sql
SELECT column_name,
    CASE column_name
        WHEN value1 THEN result1
        WHEN value2 THEN result2
        ...
        ELSE default_result
    END AS alias_name
FROM table_name;
```

#### Searched CASE
```sql
SELECT column_name,
    CASE 
        WHEN condition1 THEN result1
        WHEN condition2 THEN result2
        ...
        ELSE default_result
    END AS alias_name
FROM table_name;
```

### Step-by-Step Derivation & Intermediate State Mapping

A `CASE` expression operates as an element-wise conditional projection (analogous to a stream `.map()` or `switch` pattern matching operation) evaluated independently for each candidate record:

1. **Row Streaming**: Each record `(ProductName, CategoryID)` is projected into the evaluation pipeline.
2. **Sequential Equality Testing**:
   - `WHEN value1 THEN result1`: Compares `CategoryID = value1`. If `TRUE`, evaluation halts for that row and returns `result1`.
   - `WHEN value2 THEN result2`: If previous comparison was `FALSE` or `UNKNOWN`, compares `CategoryID = value2`.
3. **Fallthrough / Default Resolution**:
   - If no `WHEN` condition evaluates to `TRUE`, the `ELSE` expression is evaluated.
   - Under ANSI SQL Three-Valued Logic (3VL), comparing `NULL = value` produces `UNKNOWN`, which safely falls through to the `ELSE` branch.
   - If `ELSE` is omitted and no branch matches, `NULL` is returned.

### Key Points
* Simple CASE compares an expression to a list of values and returns the corresponding result.
* Searched CASE evaluates a list of conditions and returns the result for the first condition that is TRUE.
* The ELSE clause is optional. If no conditions are met and ELSE is not specified, the CASE expression will return NULL.

### Examples

**Example 1: Simple CASE**

***Assign a label based on a product’s category.***

```sql
-- 1. Table Schema Setup
CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY,
    ProductName TEXT NOT NULL,
    CategoryID INTEGER
);

-- 2. Literal Fixture Insertion
INSERT INTO Products (ProductID, ProductName, CategoryID) VALUES
(1, 'Laptop', 1),
(2, 'Desk Chair', 2),
(3, 'Apples', 3),
(4, 'Desk Lamp', 99),
(5, 'Uncategorized Item', NULL);

-- 3. Worked Example Query (Simple CASE)
SELECT ProductName,
    CASE CategoryID
        WHEN 1 THEN 'Electronics'
        WHEN 2 THEN 'Furniture'
        WHEN 3 THEN 'Groceries'
        ELSE 'Other'
    END AS CategoryLabel
FROM Products
ORDER BY ProductID;

-- 4. Boundary Case: Omitted ELSE Clause (Returns NULL when unmatched)
SELECT ProductName,
    CASE CategoryID
        WHEN 1 THEN 'Electronics'
        WHEN 2 THEN 'Furniture'
    END AS CategoryLabel
FROM Products
WHERE ProductID = 4;
```

#### Expected Output & Derivation Table:

| ProductID | Input ProductName | Input CategoryID | Evaluated Branch | Output CategoryLabel | Derivation Notes |
|---|---|---|---|---|---|
| 1 | Laptop | 1 | `WHEN 1` | Electronics | `1 = 1` evaluates to `TRUE`; returns `'Electronics'` immediately. |
| 2 | Desk Chair | 2 | `WHEN 2` | Furniture | `2 = 1` is `FALSE`; `2 = 2` is `TRUE`; returns `'Furniture'`. |
| 3 | Apples | 3 | `WHEN 3` | Groceries | `3 = 1` and `3 = 2` are `FALSE`; `3 = 3` is `TRUE`; returns `'Groceries'`. |
| 4 | Desk Lamp | 99 | `ELSE` | Other | No `WHEN` branch matches; falls through to `ELSE 'Other'`. |
| 5 | Uncategorized Item | NULL | `ELSE` | Other | Under 3VL, `NULL = 1..3` is `UNKNOWN`; falls through to `ELSE 'Other'`. |

#### Boundary Output (Omitted ELSE):
For `ProductID = 4` (`CategoryID = 99`), no `WHEN` branch matches and `ELSE` is omitted:
```
ProductName: Desk Lamp | CategoryLabel: NULL
```

**Example 2: Searched CASE**

***Assign a rating based on the price of a product.***

```sql
SELECT ProductName, Price,
    CASE 
        WHEN Price > 100 THEN 'Expensive'
        WHEN Price BETWEEN 50 AND 100 THEN 'Moderate'
        WHEN Price < 50 THEN 'Affordable'
        ELSE 'Unknown'
    END AS PriceRange
FROM Products;
```

**Example 3: Using CASE with Aggregation**

***Calculate the total sales for online and in-store orders separately.***

```sql
SELECT 
    SUM(CASE WHEN OrderType = 'Online' THEN Amount ELSE 0 END) AS OnlineSales,
    SUM(CASE WHEN OrderType = 'In-Store' THEN Amount ELSE 0 END) AS InStoreSales
FROM Orders;
```

**Note :**
* CASE expressions can be used in SELECT, WHERE, ORDER BY, and GROUP BY clauses.
* CASE can simplify complex IF-THEN-ELSE logic and help make SQL queries more readable.
* In GROUP BY statements, CASE is often used with aggregate functions to conditionally group data.

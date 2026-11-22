---
id: SQL-LIKE-Operator
sidebar_position: 19
title: "SQL LIKE Operator"
sidebar_label: "SQL LIKE Operator"
description: "The SQL LIKE operator is used to filter data based on patterns."
tags: [sql, dbms, database, like]
---

The `LIKE` operator is used in a `WHERE` clause to search for a specific pattern in a column.

### Syntax

```sql
SELECT column_name(s)
FROM table_name
WHERE column_name LIKE pattern;
```

### Video Explanation

<LiteYouTubeEmbed
  id="iug2vvLQ9B8"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="Lec-76: Like Command in SQL with example in Hindi | Learn SQL in Easiest Way| DBMS"
  lazyLoad={true}
  webp
/>

### Pattern Matching

You can use the following wildcard characters in the pattern:

* **%**: Matches any character sequence, zero or more times.
* **_**: Matches any single character.

### Examples

**Example 1: Find all products that start with 'Ch'**

```sql
SELECT *
FROM Products
WHERE ProductName LIKE 'Ch%';
```

**Example 2: Find all products that contain 'an' anywhere in the name**

```sql
SELECT *
FROM Products
WHERE ProductName LIKE '%an%';
```

**Example 3: Find all products that end with 'syrup'**

```sql
SELECT *
FROM Products
WHERE ProductName LIKE '%syrup';
```

**Example 4: Find all products with a 4-character product ID starting with '1'**

```sql
SELECT *
FROM Products
WHERE ProductID LIKE '1___';
```

For the examples below, use this small `Products` table:

| ProductID | ProductName |
| --- | --- |
| 1001 | Chai |
| 1002 | Chang |
| 1003 | Aniseed Syrup |
| 1004 | Chef Anton's Cajun Seasoning |

The first query returns `Chai`, `Chang`, and `Chef Anton's Cajun Seasoning`; the second returns `Chang`, `Aniseed Syrup`, and `Chef Anton's Cajun Seasoning`; the third returns `Aniseed Syrup`; and the fourth returns all four IDs because each has four characters beginning with `1`. A boundary query such as `ProductName LIKE 'Qz%'` returns no rows. `%` can match an empty sequence, while `_` consumes exactly one character, so `1___` requires exactly four characters beginning with `1`.

`LIKE` does not copy the matching strings into a new result structure as part of pattern matching: the engine checks candidate rows and returns rows that satisfy the predicate. A leading wildcard often prevents a conventional B-tree from narrowing the search to a starting range. The exact plan depends on the database, collation, index, and settings. For example, in SQLite 3.50.4, an experiment adding 1,000 rows to the sample table and indexing `ProductName COLLATE NOCASE` used an index range search for `LIKE 'Ch%'` (503 matches), but scanned the index for `LIKE '%an%'` (3 matches). This illustrates query-plan behavior, not a universal complexity guarantee; inspect the plan on the database and schema you use. The fixed introductory `SELECT` syntax itself has no meaningful standalone time or space benchmark.

```sql
CREATE TABLE Products (ProductID TEXT PRIMARY KEY, ProductName TEXT);
INSERT INTO Products VALUES
  ('1001', 'Chai'),
  ('1002', 'Chang'),
  ('1003', 'Aniseed Syrup'),
  ('1004', 'Chef Anton''s Cajun Seasoning');

SELECT ProductName FROM Products WHERE ProductName LIKE 'Ch%' ORDER BY ProductName;
SELECT ProductName FROM Products WHERE ProductName LIKE '%an%' ORDER BY ProductName;
SELECT ProductName FROM Products WHERE ProductName LIKE '%syrup' ORDER BY ProductName;
SELECT ProductID FROM Products WHERE ProductID LIKE '1___' ORDER BY ProductID;
SELECT ProductName FROM Products WHERE ProductName LIKE 'Qz%' ORDER BY ProductName;
```

**Note:** The specific implementation and syntax might vary slightly depending on the database system you're using (e.g., MySQL, PostgreSQL, SQL Server). However, the core concept of using the `LIKE` operator with wildcard characters remains consistent.

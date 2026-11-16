---
id: "forms-and-user-input"
sidebar_position: 12
title: "Forms and User Input in php"
sidebar_label: "Forms & User Input"
description: "Learn how to handle HTML forms in php using GET and POST methods, validate input, and prevent common security vulnerabilities."
tags: [php, forms, user-input, validation, security]
---

Forms are the primary way users submit data to php scripts. php handles form data through the `$_GET` and `$_POST` superglobals.

## Video Explanation

<LiteYouTubeEmbed
  id="PTVECOCyr40"
  params="autoplay=1&autohide=1&showinfo=0&rel=0"
  title="PHP Forms Tutorial: GET & POST Requests in php | PHP Tutorial #21"
  lazyLoad={true}
  webp
/>

## A Simple HTML Form

HTML forms collect input from users and dispatch it to a server-side PHP script. The two primary submission methods defined by HTTP are **POST** and **GET**. Below, both methods are compared using the exact same fixture: a simple form collecting a user's **Name** and **Email**.

### Method 1: POST Submission

When submitting via `method="post"`, form fields are packaged directly inside the HTTP request body. This keeps user data out of the URL bar and browser history.

#### HTML Form (`post_form.html`)
```html title="post_form.html"
<!DOCTYPE html>
<html>
<body>

<form method="post" action="welcome_post.php">
    Name: <input type="text" name="name"><br>
    Email: <input type="text" name="email"><br>
    <input type="submit" value="Submit">
</form>

</body>
</html>
```

#### How POST Sends Data (Intermediate Representation)
1. **HTTP Request Structure**: The browser serializes the key-value pairs into an `application/x-www-form-urlencoded` message payload in the HTTP request body:
   ```http
   POST /welcome_post.php HTTP/1.1
   Host: localhost
   Content-Type: application/x-www-form-urlencoded
   Content-Length: 35

   name=Alice&email=alice%40example.com
   ```
2. **How PHP Reads It**: The PHP engine automatically parses the request body and populates the `$_POST` superglobal array:
   - `$_POST['name'] = 'Alice'`
   - `$_POST['email'] = 'alice@example.com'`
   *(Raw, unparsed stream is also accessible through `php://input`)*.

#### PHP Handler (`welcome_post.php`)
```php title="welcome_post.php"
<?php
$name  = htmlspecialchars($_POST['name'] ?? '');
$email = htmlspecialchars($_POST['email'] ?? '');

echo "Welcome, $name!\n";
echo "Your email is: $email\n";
?>
```

### Method 2: GET Submission

When submitting via `method="get"`, form fields are appended directly to the action URL as a query string.

#### HTML Form (`get_form.html`)
```html title="get_form.html"
<!DOCTYPE html>
<html>
<body>

<form method="get" action="welcome_get.php">
    Name: <input type="text" name="name"><br>
    Email: <input type="text" name="email"><br>
    <input type="submit" value="Submit">
</form>

</body>
</html>
```

#### How GET Sends Data (Intermediate Representation)
1. **HTTP Request Structure**: The browser appends the URL-encoded key-value pairs directly to the target URL path separated by `?` and `&`. The HTTP request body remains empty:
   ```http
   GET /welcome_get.php?name=Alice&email=alice%40example.com HTTP/1.1
   Host: localhost
   ```
2. **How PHP Reads It**: The web server passes the query string via the `QUERY_STRING` environment variable (`$_SERVER['QUERY_STRING']`). PHP decodes this string into the `$_GET` superglobal array:
   - `$_GET['name'] = 'Alice'`
   - `$_GET['email'] = 'alice@example.com'`

#### PHP Handler (`welcome_get.php`)
```php title="welcome_get.php"
<?php
$name  = htmlspecialchars($_GET['name'] ?? '');
$email = htmlspecialchars($_GET['email'] ?? '');

echo "Welcome, $name!\n";
echo "Your email is: $email\n";
?>
```

* * *

## Processing Form Data

Both methods sanitize and render input using `htmlspecialchars()` to prevent Cross-Site Scripting (XSS) attacks.

### Worked Example: Normal Input

Consider the literal sample inputs submitted by a user:
- **Name**: `Alice`
- **Email**: `alice@example.com`

#### Intermediate Processing:
- **POST Method**:
  1. Wire Format: Request body contains `name=Alice&email=alice%40example.com`.
  2. Superglobal: PHP populates `$_POST['name'] = 'Alice'` and `$_POST['email'] = 'alice@example.com'`.
  3. Sanitization: `htmlspecialchars('Alice')` yields `'Alice'`; `htmlspecialchars('alice@example.com')` yields `'alice@example.com'`.
- **GET Method**:
  1. Wire Format: URL query string is `?name=Alice&email=alice%40example.com`.
  2. Superglobal: PHP populates `$_GET['name'] = 'Alice'` and `$_GET['email'] = 'alice@example.com'`.
  3. Sanitization: `htmlspecialchars('Alice')` yields `'Alice'`; `htmlspecialchars('alice@example.com')` yields `'alice@example.com'`.

#### Expected Output (Both POST and GET):
```text
Welcome, Alice!
Your email is: alice@example.com
```

### Boundary Example: Missing or Empty Input

In real-world web applications, forms may be submitted with blank fields, or a user might access the handler URL directly without submitting query or body parameters.

1. **Precondition and Contract**:
   - In PHP 8+, accessing an undefined array key (e.g. `$_POST['name']` when omitted) triggers an `Undefined array key` warning.
   - The null coalescing operator (`?? ''`) checks if the key exists and is non-null; if absent, it provides an empty string `''` as fallback without raising warnings.
2. **Missing Parameters** (e.g., navigating directly to `welcome_post.php` with no POST body, or `welcome_get.php` with no query string):
   - `$_POST['name'] ?? ''` evaluates to `''`.
   - `$_POST['email'] ?? ''` evaluates to `''`.
3. **Empty String Inputs** (e.g., user clicks submit with both input fields left blank: `name=&email=`):
   - `$_POST['name']` is `""`.
   - `$_POST['email']` is `""`.

#### Expected Output for Boundary Case (Both POST and GET):
```text
Welcome, !
Your email is: 
```

* * *

## GET vs POST

| Feature | GET | POST |
|---------|-----|------|
| Data in URL | Yes | No |
| Max data size | ~2000 chars | No limit |
| Bookmarkable | Yes | No |
| Suitable for | Search, filters | Sensitive data |
| Cached | Yes | No |

```php
<?php
// GET example (from URL: page.php?search=php)
$search = $_GET['search'];

// POST example (from form submission)
$password = $_POST['password'];
?>
```

* * *

## Self-Processing Form (Same File)

```php
<?php
$message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST['name']);
    $message = "Hello, $name!";
}
?>
<!DOCTYPE html>
<html>
<body>
<form method="post" action="<?= htmlspecialchars($_SERVER['PHP_SELF']); ?>">
    Name: <input type="text" name="name">
    <input type="submit" value="Submit">
</form>
<p><?= $message ?></p>
</body>
</html>
```

* * *

## Input Validation

Always validate user input before processing:

```php
<?php
$errors = [];
$name   = $email = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // Validate name
    if (empty($_POST["name"])) {
        $errors[] = "Name is required.";
    } else {
        $name = trim($_POST["name"]);
    }

    // Validate email
    if (empty($_POST["email"])) {
        $errors[] = "Email is required.";
    } elseif (!filter_var($_POST["email"], FILTER_VALIDATE_EMAIL)) {
        $errors[] = "Invalid email format.";
    } else {
        $email = trim($_POST["email"]);
    }

    if (empty($errors)) {
        echo "Form submitted: $name, $email";
    } else {
        foreach ($errors as $error) {
            echo "<p style='color:red'>$error</p>";
        }
    }
}
?>
```

* * *

## Sanitizing Input

```php
<?php
// Remove HTML tags and extra whitespace
$name = strip_tags(trim($_POST['name']));

// Sanitize an email
$email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);

// Sanitize a URL
$url = filter_var($_POST['url'], FILTER_SANITIZE_URL);

// Prevent XSS
$safe = htmlspecialchars($_POST['comment']);
?>
```

* * *

## Handling Checkboxes and Radio Buttons

```html
<form method="post">
    <input type="checkbox" name="subscribe" value="yes"> Subscribe
    <input type="radio" name="gender" value="male"> Male
    <input type="radio" name="gender" value="female"> Female
    <input type="submit">
</form>
```

```php
<?php
$subscribe = isset($_POST['subscribe']) ? "Yes" : "No";
$gender    = $_POST['gender'] ?? "Not specified";

echo "Subscribe: $subscribe";
echo "Gender: $gender";
?>
```

* * *

## Handling Select Dropdowns

```html
<form method="post">
    <select name="country">
        <option value="IN">India</option>
        <option value="US">USA</option>
        <option value="UK">UK</option>
    </select>
    <input type="submit">
</form>
```

```php
<?php
$country = $_POST['country'] ?? '';
echo "Selected: $country";
?>
```

* * *

## File Upload Form

```html
<form method="post" enctype="multipart/form-data">
    Upload: <input type="file" name="file">
    <input type="submit" value="Upload">
</form>
```

```php
<?php
if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    $name = $_FILES['file']['name'];
    $tmp  = $_FILES['file']['tmp_name'];
    
    // Validate file extension to prevent PHP shell uploads
    $allowedExtensions = ['jpg', 'jpeg', 'png', 'pdf'];
    $ext = strtolower(pathinfo($name, PATHINFO_EXTENSION));
    
    if (in_array($ext, $allowedExtensions)) {
        $dest = "uploads/" . basename($name);
        if (move_uploaded_file($tmp, $dest)) {
            echo "File uploaded: " . htmlspecialchars($name);
        } else {
            echo "Upload failed.";
        }
    } else {
        echo "Invalid file type.";
    }
}
```

**Security Note:** Never trust user-submitted data. Always validate, sanitize, and escape before displaying or storing.
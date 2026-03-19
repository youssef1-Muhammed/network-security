<?php
// Vulnerable page with XSS vulnerability
// WARNING: This file intentionally contains insecure code for educational purposes.
// This demonstrates a reflected XSS vulnerability where user input is directly echoed
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Search - Vulnerable to XSS</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        .search-box {
            margin: 20px 0;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .results {
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
        .warning {
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Car Search</h1>
        
        <div class="warning">
            <strong>⚠️ WARNING:</strong> This page is intentionally vulnerable to XSS attacks for educational purposes.
        </div>

        <form method="GET" action="">
            <div class="search-box">
                <input type="text" name="search" placeholder="Search for a car model..." 
                       value="<?php echo isset($_GET['search']) ? htmlspecialchars($_GET['search'], ENT_QUOTES, 'UTF-8') : ''; ?>">
                <button type="submit">Search</button>
            </div>
        </form>

        <?php
        if (isset($_GET['search']) && !empty($_GET['search'])) {
            $search = $_GET['search'];
            echo '<div class="results">';
            echo '<h2>Search Results for: ' . $search . '</h2>'; // VULNERABLE: Direct output without sanitization
            echo '<p>Your search query was: <strong>' . $search . '</strong></p>'; // VULNERABLE: Direct output
            
            // Simulate search results
            echo '<p>No results found. Try a different search term.</p>';
            echo '</div>';
        }
        ?>

        <div style="margin-top: 30px; padding: 15px; background-color: #e7f3ff; border-radius: 4px;">
            <h3>About This Page</h3>
            <p>This page demonstrates a <strong>Reflected Cross-Site Scripting (XSS)</strong> vulnerability.</p>
            <p>The search parameter is directly echoed to the page without proper sanitization, allowing malicious scripts to be injected.</p>
        </div>
    </div>

    <script>
        // Set a test cookie to demonstrate cookie theft
        document.cookie = "session_id=abc123xyz789; path=/";
        document.cookie = "user_role=admin; path=/";
        document.cookie = "csrf_token=secret_token_12345; path=/";
        
        console.log("Current cookies:", document.cookie);
    </script>
</body>
</html>


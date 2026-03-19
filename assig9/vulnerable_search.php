<?php
// Vulnerable endpoint - demonstrates SQL Injection vulnerability.
// WARNING: This file intentionally contains insecure code for educational purposes.
header('Content-Type: application/json');
require 'db.php';

// Accepts ?q=string and performs a naive LIKE search without parameter binding
$q = isset($_GET['q']) ? $_GET['q'] : '';

// DANGEROUS: concatenating user input directly into SQL
$sql = "SELECT * FROM cars WHERE model LIKE '%" . $q . "%'";

try {
    $stmt = $pdo->query($sql); // vulnerable to SQL injection
    $rows = $stmt->fetchAll();
    echo json_encode($rows, JSON_PRETTY_PRINT);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Query failed: ' . $e->getMessage()]);
}
?>

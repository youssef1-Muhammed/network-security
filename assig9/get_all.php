<?php
header('Content-Type: application/json');
require 'db.php';

$stmt = $pdo->query('SELECT * FROM cars ORDER BY car_id');
$cars = $stmt->fetchAll();

echo json_encode($cars, JSON_PRETTY_PRINT);
?>

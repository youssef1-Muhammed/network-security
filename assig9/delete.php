<?php
// Delete a car given car_id
header('Content-Type: application/json');
require 'db.php';

if (!isset($_GET['car_id'])) {
    http_response_code(400);
    echo json_encode(['error' => 'car_id is required']);
    exit;
}

$car_id = (int)$_GET['car_id'];
$stmt = $pdo->prepare('DELETE FROM cars WHERE car_id = :id');
$stmt->execute([':id' => $car_id]);

echo json_encode(['message' => 'Car deleted', 'car_id' => $car_id], JSON_PRETTY_PRINT);
?>

<?php
// Show a car by car_id
header('Content-Type: application/json');
require 'db.php';

if (!isset($_GET['car_id'])) {
    http_response_code(400);
    echo json_encode(['error' => 'car_id is required']);
    exit;
}

$car_id = (int)$_GET['car_id'];

$stmt = $pdo->prepare('SELECT * FROM cars WHERE car_id = :id');
$stmt->execute([':id' => $car_id]);
$car = $stmt->fetch();

if (!$car) {
    http_response_code(404);
    echo json_encode(['error' => 'Car not found']);
    exit;
}

echo json_encode($car, JSON_PRETTY_PRINT);
?>

<?php
// Create a new car (expects JSON body)
header('Content-Type: application/json');
require 'db.php';

$data = json_decode(file_get_contents('php://input'), true);
if (!$data) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON body']);
    exit;
}

$model = $data['model'] ?? null;
$used = isset($data['used']) ? (int)$data['used'] : null;
$sale_date = $data['sale_date'] ?? null;
$price = isset($data['price']) ? (float)$data['price'] : null;

if (!$model || $used === null) {
    http_response_code(400);
    echo json_encode(['error' => 'model and used are required']);
    exit;
}

$stmt = $pdo->prepare('INSERT INTO cars (model, used, sale_date, price) VALUES (:model, :used, :sale_date, :price)');
$stmt->execute([
    ':model' => $model,
    ':used' => $used,
    ':sale_date' => $sale_date,
    ':price' => $price
]);

$newId = $pdo->lastInsertId();
http_response_code(201);
echo json_encode(['message' => 'Car created', 'car_id' => (int)$newId], JSON_PRETTY_PRINT);
?>

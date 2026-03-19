<?php
// Update a car given car_id (expects JSON body)
header('Content-Type: application/json');
require 'db.php';

if (!isset($_GET['car_id'])) {
    http_response_code(400);
    echo json_encode(['error' => 'car_id is required']);
    exit;
}
$car_id = (int)$_GET['car_id'];

$data = json_decode(file_get_contents('php://input'), true);
if (!$data) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON body']);
    exit;
}

// Build dynamic set clause safely
$fields = [];
$params = [':id' => $car_id];
if (isset($data['model'])) { $fields[] = 'model = :model'; $params[':model'] = $data['model']; }
if (isset($data['used']))  { $fields[] = 'used = :used';   $params[':used'] = (int)$data['used']; }
if (isset($data['sale_date'])) { $fields[] = 'sale_date = :sale_date'; $params[':sale_date'] = $data['sale_date']; }
if (isset($data['price'])) { $fields[] = 'price = :price'; $params[':price'] = (float)$data['price']; }

if (empty($fields)) {
    http_response_code(400);
    echo json_encode(['error' => 'No fields to update']);
    exit;
}

$sql = 'UPDATE cars SET ' . implode(', ', $fields) . ' WHERE car_id = :id';
$stmt = $pdo->prepare($sql);
$stmt->execute($params);

echo json_encode(['message' => 'Car updated', 'car_id' => $car_id], JSON_PRETTY_PRINT);
?>

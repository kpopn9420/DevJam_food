<?php

// 假設你已經有一個 MySQL 連線 $conn
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");
header('Content-Type: application/json');  // 設置回應為 JSON 格式
$conn = new mysqli("localhost", "root", "", "foodsystem");

$keyword = $_GET['q'] ?? ''; // 如果沒傳搜尋字串，就預設空字串

$category = $_GET['category'] ?? '';
$lat = $_GET['lat'] ?? null;
$lng = $_GET['lng'] ?? null;
$range = $_GET['range'] ?? 5;

if ($lat !== null && $lng !== null) {
    // 附近搜尋 + 關鍵字 + 類別
    $sql = "
        SELECT *, 
        (6371 * ACOS(
            COS(RADIANS(?)) * COS(RADIANS(LAT)) *
            COS(RADIANS(LNG) - RADIANS(?)) +
            SIN(RADIANS(?)) * SIN(RADIANS(LAT))
        )) AS distance
        FROM reservation
        WHERE FOOD LIKE ? AND (CATEGORY = ? OR ? = '')
        HAVING distance < ?
        ORDER BY distance ASC
    ";
    $stmt = $conn->prepare($sql);
    $searchTerm = "%" . $keyword . "%";
    $stmt->bind_param("dddsssd", $lat, $lng, $lat, $searchTerm, $category, $category, $range);
} else {
    // 純關鍵字 + 類別搜尋
    $sql = "SELECT * FROM food_items WHERE NAME LIKE ? AND (CATEGORY = ? OR ? = '')";
    $stmt = $conn->prepare($sql);
    $searchTerm = "%" . $keyword . "%";
    $stmt->bind_param("sss", $searchTerm, $category, $category);
}

$stmt->execute();
$result = $stmt->get_result();

$data = [];
while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}
echo json_encode(["success" => true, "data" => $data]);

$stmt->close();
$conn->close();
?>
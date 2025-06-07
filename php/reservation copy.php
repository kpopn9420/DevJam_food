<?php

// 假設你已經有一個 MySQL 連線 $conn
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type");
header('Content-Type: application/json');  // 設置回應為 JSON 格式
$conn = new mysqli("localhost", "root", "", "foodsystem");

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // 檢查是否有接收到
    if (isset($_POST['title']) && isset($_POST['owner']) && isset($_POST['rcv']) && isset($_POST['quantity']) && isset($_POST['expire_time']) && isset($_POST['lat']) && isset($_POST['lng'])) {
        $id = rand(50000000, 59999999);
        $food = $_POST['title'];
        $owner = $_POST['owner'];
        $rcv = $_POST['rcv'];
        $status = 'pending';
        $quantity = $_POST['quantity'];
        $expire_time = $_POST['expire_time'];
        $des = ($_POST['description'] == null ? '' : $_POST['description']);
        $lat = $_POST['lat'];
        $lng = $_POST['lng'];

        $sql = "INSERT INTO reservation (ID, FOOD, OWNER_ID, RCV_ID,STATUS,NUM,RCV_TIME,DES,LAT,LNG) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ssssssssss", $id, $food, $owner, $rcv, $status, $quantity, $expire_time, $des, $lat, $lng);
        // 執行 SQL 插入操作
        if ($stmt->execute()) {
            echo json_encode(["success" => true, "message" => "成功！"]);
        } else {
            echo json_encode(["success" => false, "message" => "錯誤：" . $stmt->error]);
        }

        // 關閉資料庫連線
        $stmt->close();
    } else {
        echo json_encode(["success" => false, "message" => "no data"]);
    }
} else {
    echo json_encode(["success" => false, "message" => "invalid request"]);
}

$conn->close();
?>
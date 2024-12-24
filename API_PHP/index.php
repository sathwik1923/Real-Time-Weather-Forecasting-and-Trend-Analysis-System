<?php
header('Content-Type: application/json');

// Database connection parameters
// Read the JSON file
$json = file_get_contents('db_params.json');

// Decode JSON data into PHP array
$db_params = json_decode($json, true);

// Access the parameters
$DB_NAME = $db_params['dbname'];
$DB_USER = $db_params['user'];
$DB_PASS = $db_params['password'];
$DB_HOST = $db_params['host'];
$DB_PORT = $db_params['port'];

function get_db_connection() {
    global $DB_HOST, $DB_NAME, $DB_USER, $DB_PASS, $DB_PORT;
    $conn = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME, $DB_PORT);
    if ($conn->connect_error) {
        die(json_encode(['error' => 'Database connection failed: ' . $conn->connect_error]));
    }
    return $conn;
}

function validate_api_key($api_key) {
    return $api_key === 'hello123';
}

$api_key = $_GET['api_key'] ?? '';
$station_id = $_GET['station_id'] ?? '';
$data_type = $_GET['type'] ?? '';

if (!validate_api_key($api_key)) {
    http_response_code(403);
    echo json_encode(['error' => 'Invalid API key']);
    exit;
}

$conn = get_db_connection();

if ($data_type == 'current') {
    $query = "
    SELECT timestamp, temperature, humidity, pressure, weather_description 
    FROM weather_data 
    WHERE station_id = ? 
    ORDER BY timestamp DESC 
    LIMIT 1;
    ";
} elseif ($data_type == 'forecast') {
    $query = "
    SELECT forecast_timestamp, predicted_temperature, predicted_humidity, forecast_description 
    FROM weather_forecasts 
    WHERE station_id = ? 
    ORDER BY forecast_timestamp ASC;
    ";
} elseif ($data_type == 'historical') {
    $query = "
    SELECT timestamp, temperature, humidity, pressure, weather_description 
    FROM weather_data 
    WHERE station_id = ? 
    ORDER BY timestamp ASC;
    ";
} else {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid data type']);
    exit;
}

$stmt = $conn->prepare($query);
$stmt->bind_param("i", $station_id);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 0) {
    http_response_code(404);
    echo json_encode(['error' => 'No data found']);
    exit;
}

$rows = [];
while ($row = $result->fetch_assoc()) {
    $rows[] = $row;
}

echo json_encode($rows);

$stmt->close();
$conn->close();
?>

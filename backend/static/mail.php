<?php
// Simple mail.php for local testing
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $name = isset($_POST['name']) ? $_POST['name'] : '';
    $email = isset($_POST['email']) ? $_POST['email'] : '';
    $subject = isset($_POST['subject']) ? $_POST['subject'] : 'Appointment Request';
    $message = isset($_POST['message']) ? $_POST['message'] : '';
    $phone = isset($_POST['phone']) ? $_POST['phone'] : '';
    $date = isset($_POST['date']) ? $_POST['date'] : '';
    $time = isset($_POST['time']) ? $_POST['time'] : '';

    if ($name && $email && $message) {
        $to = "your@email.com"; // Change to your email
        $headers = "From: $email\r\nReply-To: $email";
        $body = "Name: $name\nEmail: $email\n";
        if ($phone) $body .= "Phone: $phone\n";
        if ($date) $body .= "Date: $date\n";
        if ($time) $body .= "Time: $time\n";
        $body .= "Subject: $subject\nMessage: $message";
        if (mail($to, $subject, $body, $headers)) {
            echo 'success';
        } else {
            echo 'Mail sending failed.';
        }
    } else {
        echo 'Please complete the form and try again.';
    }
} else {
    echo 'Invalid request.';
}
?>

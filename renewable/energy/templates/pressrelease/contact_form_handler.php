<?php
/**
 * File Name: contact_form_handler.php
 *
 * Send message function to process contact form submission
 *
 */
if ( isset( $_POST['email'] ) ):

    date_default_timezone_set('America/Los_Angeles');
    $script_tz = date_default_timezone_get();

    $name = filter_var( $_POST['name'], FILTER_SANITIZE_STRING );
    $from_email = filter_var( $_POST['email'], FILTER_SANITIZE_EMAIL );
    $subject = filter_var( $_POST['subject'], FILTER_SANITIZE_STRING );
    $message = filter_var( $_POST['message'], FILTER_SANITIZE_STRING );

    $to_email = "pressportal18@gmail.com";    // provide your target email address here
    $to_name = "Admins";

    $email_subject = 'You Have Received a Message From ' . $name . '.';

    if ( ! empty( $subject ) ) {
        $email_subject = $subject . '.';
    }

    $email_body = "You have Received a message from: " . $name . " <br/>";

    if (!empty( $subject )) {
        $email_body .= "Subject: " . $subject . " <br/><br/>";
    }

    $email_body .= "Their additional message is as follows." . " <br/><br/>";

    $email_content = nl2br( $message ) . " <br/><br/>";

    $email_reply = 	"You can contact " . $name . " via email, " . $from_email ;

    $prepared_message = $email_body . $email_content . $email_reply;

    // You can consult https://github.com/eoghanobrien/php-simple-mail for more details
    require 'class.simple_mail.php';

    /* @var SimpleMail $mail */
    $mail = new SimpleMail();
    $mail->setTo( $to_email, $to_name )
        ->setSubject( $email_subject )
        ->setFrom( $from_email, $name )
        ->addMailHeader( 'Reply-To', $from_email, $name )
        ->addGenericHeader( 'X-Mailer', 'PHP/' . phpversion() )
        ->addGenericHeader( 'Content-Type', 'text/html; charset="utf-8"' )
        ->setMessage( $prepared_message );

    $sent = $mail->send();

    //echo $mail->debug();

    if( $sent ) {

            echo "Message Sent Successfully!";

    } else {

        echo "Server Error:  mail method failed!";

    }

else:

    echo "Invalid Request !";

endif;

die;

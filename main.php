<?php
  include("db_connection.php");
  session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
    <style>
        @media screen and (min-width: 1024px) {
            .is-small-on-desktop {
                font-size: 0.75rem; /* Adjust button font size for smaller size */
                padding-top: 0.25rem;
                padding-bottom: 0.25rem;
            }
        }
    </style>
</head>
<body>
    <section class="hero is-fullheight is-dark">
        <div class="hero-body">
            <div class="container has-text-centered">
                <h1 class="title">Welcome</h1>
                <div class="buttons is-flex-direction-column">
                    <a href="chatbot.php" class="button is-info is-rounded is-large is-fullwidth is-small-on-desktop"><i class="fas fa-comments"></i> Chat Bot</a>
                    <a href="asses.php" class="button is-success is-rounded is-large is-fullwidth is-small-on-desktop"><i class="fas fa-check"></i> Assessment</a>
                    <a href="logout.php" class="button is-danger is-rounded is-large is-fullwidth is-small-on-desktop"><i class="fas fa-sign-out-alt"></i> Logout</a>
                </div>
            </div>
        </div>
    </section>
</body>
</html>

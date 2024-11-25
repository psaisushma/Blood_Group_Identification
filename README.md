Introduction
Our project aims to solve a significant problem in the medical field—accurate and quick identification of blood groups. Blood group determination is crucial for various medical treatments, including blood transfusions, surgeries, and emergency care. Traditionally, this process requires specialized equipment and trained personnel, which may not always be available, especially in remote or resource-limited settings. Inspired by this challenge, we set out to develop a solution that is accessible, user-friendly, and reliable.

Objectives:

The primary objectives of our project are as follows:

To provide a dependable method for blood group identification using image analysis.

To create a user-friendly interface that allows users to easily upload and analyze blood cell images.

To ensure the accuracy and speed of the blood group identification process.
To achieve these objectives, we utilized the following technologies:

Backend: Django framework in Python, which handles server-side operations.

Frontend: HTML, CSS, and JavaScript to create a responsive and intuitive user interface.

Database: SQLite for data storage.

Our project is structured into a Django project named sample and an app named identipage. The functionalities are divided into views, templates, and forms, each playing a crucial role in the overall workflow of the application.


How users interact with the application, from signing up or logging in to uploading blood cell images and receiving the blood group identification results.


Step 1: Users Sign Up or Log In

Navigation to Home Page:

The user navigates to the home page of the application. Here, they are greeted with options to log in or sign up.

Sign Up Process:

If the user is new to the application, they will click on the “Sign Up” link.

This takes them to the sign-up page, where they fill out a form with their username, email, and password.

After entering the required information, the user submits the form to create an account.

Log In Process:

For returning users, they click on the “Log In” link.

This takes them to the login page, where they enter their username and password.

After entering their credentials, the user submits the form to log in to their account.


Step 2: They Upload an Image of Their Blood Cells

Navigating to the Profile Page:

Once logged in, the user is directed to their profile page. Here, they can upload images of their blood cells for analysis.

Uploading an Image:

The user clicks on the “Upload Image” button, which opens a file dialog to select an image file from their device.

The user selects an image of their blood cells and uploads it by submitting the form.

Form Submission:

The form submission triggers the backend process to handle the uploaded image.

The system processes the image to identify the blood group.


Step 3: The System Processes the Image and Displays the Identified Blood Group

Image Processing:

The system uses image processing algorithms to analyze the uploaded image. It looks for specific markers and characteristics in the blood cells to determine the blood group.

Displaying Results:

Once the processing is complete, the application displays the identified blood group on the profile page.

The user can see the result along with any additional details, such as contour count, which may be relevant to the analysis.

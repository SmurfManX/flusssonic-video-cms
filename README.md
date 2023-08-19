# Flussonic - Video CMS for HLS Vod Streaming

![User Interface Screenshot](/static/images/ui-1.png)

## Overview

This repository contains the code for a Video Content Management System (CMS) that allows users to upload video files in chunks. The system is designed to handle large file uploads by breaking them into smaller pieces and then reassembling them on the server. This approach helps in maintaining a smooth user experience even with slow or unstable network connections.

## Features

- **Automatic Reassembly:** Server-side logic reassembles the chunks into the original video file.
- **Date-Based Organization:** Saves the final video file in a folder structured by date, e.g., `/uploads/%Y-%m-%d/`.
- **File Validation:** Ensures that only files with specific extensions (e.g., `.mp4`) are processed.
- **Responsive UI:** Provides a user-friendly interface to upload videos along with associated metadata such as logos.

## Technologies Used

- **Flask:** A micro web framework written in Python, used to handle the server-side logic.
- **Materialize CSS:** A responsive front-end framework based on Material Design for styling the user interface.
- **JavaScript:** Used to handle client-side chunking and asynchronous file uploading.


## requirements.txt
```
Flask==2.0.2
python-dotenv==0.19.1
Flask-Bootstrap==3.3.7.1
Werkzeug==2.0.2
```
- pip install -r requirements.txt

## How to Run

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using the following command:
4. Run the Flask application.
5. Access the application through your web browser at `http://localhost:5000/`.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

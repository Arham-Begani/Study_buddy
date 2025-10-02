# AI Study Buddy: Your Offline-First Learning Companion

**AI Study Buddy** is a multi-page Flask application designed to assist students in planning, learning, and assessing their understanding of study material.  This offline-first application prioritizes accessibility, allowing users to utilize core features even without an internet connection.  When online, the app leverages the power of the Gemini API (or a similar AI API) to enhance its capabilities and provide more intelligent assistance.

## Features

* **Amazing Functionality:**  Access core features, including study schedule generation and basic quizzing.
* **Study Schedule Generator:** Create personalized study plans based on your goals and available time.
* **AI-Powered Chat Assistant (Online):**  Engage with an AI chat assistant for clarifying concepts, receiving study tips, and generating practice questions (requires online connection).
* **Interactive Quizzes:** Test your knowledge with customizable quizzes and receive immediate feedback.
* **Multi-Page Interface:** Intuitive navigation across different sections of the application.
* **Newly Added View count:** A view count which keeps track on how many people used the study_buddy and uses cookies to not get multiple views from one device.

## Technologies Used

* **Python:** Backend development using Flask framework.
* **HTML, CSS, JavaScript:** Frontend development.
* **Gemini API (or similar):** AI-powered assistance (online mode).  *(Note:  This is placeholder; adapt as necessary for your chosen API.)*
* **SQLite (or alternative):** Local database for offline storage. *(Note: Choose your preferred local database solution.)*


## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys (if using online features):**  Replace placeholders in the configuration file (e.g., `config.py`) with your actual Gemini API key or keys for other services.

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access the application:** Open your web browser and navigate to `http://127.0.0.1:5000` (or the specified port).


## Contributing

Contributions are welcome! Please open an issue or submit a pull request.  Before contributing, please review the contribution guidelines (to be added).


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Future Development

* Improved AI integration with more sophisticated features.
* Enhanced user interface and user experience (UI/UX).
* Support for multiple subject areas.
* Integration with other learning platforms.


## Contact

For any questions or inquiries, please contact me.

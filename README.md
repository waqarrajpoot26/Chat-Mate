# ChatMate

ChatMate is a chatbot application developed using Flask and AIML. It utilizes natural language processing (NLP) techniques, web scraping, and a graph database (Neo4j) to provide intelligent responses to user queries and maintain user information.

# Features

- User registration and login functionality
- Chatbot interface for interactive conversation
- AIML-based chatbot responses
- NLP implementation for text preprocessing and analysis
- Web scraping to fetch information from the web
- Graph database for storing user data and relationships

# Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>

2. Install the required dependencies:
    __pip install -r requirements.txt__

3. Set up Neo4j graph database:

Install Neo4j from the official website (https://neo4j.com/download)
Start Neo4j server and create a new database
Update the Neo4j connection details (host, port, username, and password) in the code (graph = Graph("bolt://localhost:7687", auth=("neo4j", "password")))

4. Run the application:
  __shell__
   python app.py

Access the application in your web browser at http://localhost:8080

# Usage

1. Register a new account by providing your username, password, email, and phone number.
2. Login with your credentials to access the chatbot interface.
3. Type your message in the chatbox and press Enter to send it.
4. The chatbot will analyze your query, retrieve responses from the AIML knowledge base, perform web scraping if needed, and provide an appropriate response.


# License

This project is licensed under the MIT License. See the LICENSE file for details.

You can use this Markdown README file on GitHub by creating a new file named `README.md` in the root directory of your repository and copying the content into it.

# Flashcard Trainer

**Flashcard Trainer** is a web application designed to enhance learning efficiency through interactive flashcards. This project, created as part of a master's program in Automotive Engineering Production, is built using Python, Django, and JavaScript. It offers intuitive tools for creating, managing, and studying flashcards, along with features like learning history tracking and AI-powered insights.

## Features

- **Create and Manage Flashcards**:
  - **Create Category**: Organize flashcards into decks (categories).
  - **Create Card**: Add individual flashcards to categories with a question on the front and an answer on the back.
  - **Manage Card**: Update or delete existing flashcards and decks.
- **Interactive Learning Mode**:
  - **Learning Section**: Select a category to start a flashcard game where cards are shown in random order.
  - **Answer Tracking**: Mark your answer as correct or incorrect; responses are recorded in the backend as learning history.
- **Learning Algorithm**:
  - Correct answers are skipped for a defined time period (default: 3 minutes, adjustable in `myProject/cards/views.py` at line 48).
- **AI Integration**:
  - Uses the Llama API to provide interesting facts about created flashcards in the learning section.
- **Dashboard Summary**:
  - Displays total number of cards, total number of decks, recent scores, and archived cards on the home page.

## Requirements

To run this project, you will need:

- Python 3.8+
- Django 4.0+
- Node.js (for front-end dependencies, if applicable)
- JavaScript-enabled browser
- Llama API key for AI integration

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flashcard-trainer.git
   cd flashcard-trainer
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Getting into the repsective directory:
   ```bash
   cd myProject
   ```

4. Paste your Llama API token or preferred API token into `myProject/cards/views.py`:
   - Locate the `learning` function at line 297 and replace the placeholder with your API token.

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

## Usage

1. Navigate to the homepage to view:
   - Total number of cards
   - Total number of decks (categories)
   - Recent scores
   - Archived cards
2. Use the "Create Category" section to define new decks for organizing flashcards.
3. Add cards to a selected category using the "Create Card" section.
4. Manage cards (update or delete) in the "Manage Card" section.
5. Start a flashcard game in the "Learning" section:
   - Select a category to begin.
   - Cards are displayed randomly, and answers can be marked as correct or incorrect.
   - AI-generated interesting facts are provided for flashcards.

## AI Integration

The application uses the **Llama API** for AI-powered features:
- **Learning Section**: Provides interesting facts about created flashcards to enhance user engagement.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Screenshots

- **Home Page**:
  
  ![image](https://github.com/user-attachments/assets/7061ad05-4ebf-4956-9710-6dd64842a3ac)
  
- **Manage Cards**:
  
  ![image](https://github.com/user-attachments/assets/e43e8354-804e-4ae2-9549-e1fde6da42c7)

- **Learning Section**:
  
  ![image](https://github.com/user-attachments/assets/d46a6e74-1372-491d-a3ae-5d1f090d4d41)



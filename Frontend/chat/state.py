import os
import reflex as rx
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
gemini_api_key = os.getenv("GENAI_API_KEY")
if not gemini_api_key:
    raise Exception("Please set GENAI_API_KEY environment variable.")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": [],
}


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var(cache=True)
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        """Process the user's question using Gemini."""
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        # Use Gemini to process the question
        async for value in self.gemini_process_question(question):
            yield value

    async def gemini_process_question(self, question: str):
        """Get the response from Gemini API.

        Args:
            question: The user's question.
        """
        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the chat history for Gemini
        chat_history = []
        for qa in self.chats[self.current_chat]:
            chat_history.append({"role": "user", "parts": [qa.question]})
            chat_history.append({"role": "model", "parts": [qa.answer]})

        # Remove the last mock answer.
        chat_history = chat_history[:-1]

        # Start a new session to answer the question.
        session = model.generate_content(
            chat_history + [{"role": "user", "parts": [question]}],
            stream=True,
        )

        # Stream the results, yielding after every word.
        answer_text = ""
        for chunk in session:
            if chunk.text:
                answer_text += chunk.text
                self.chats[self.current_chat][-1].answer = answer_text
                self.chats = self.chats
                yield

        # Toggle the processing flag.
        self.processing = False
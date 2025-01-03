
# IELTS Assistant

IELTS Assistant is a Streamlit web application designed to help users practice and improve their IELTS speaking skills. This tool provides a simulated exam environment where users can select topics, respond to questions, and receive instant feedback along with a band score.

## Features

- **Topic Selection:** Users can choose from a list of topics to practice.
- **Question Selection:** Based on the selected topic, users can choose specific questions.
- **Speech-to-Text:** Users can record their answers which are then converted to text.
- **Text-to-Speech:** Questions are read out loud to simulate an actual exam scenario.
- **Feedback Generation:** The application analyzes responses using the OpenAI API and provides feedback and a band score based on various IELTS criteria.

## Installation

To run the IELTS Assistant, you need to have Python installed on your system. You can clone the repository and install the required packages using the following commands:

```bash
git clone [repository-url]
cd ielts-assistant
pip install -r requirements.txt
```

## Usage

After installation, you can start the application by running:

```bash
streamlit run app.py
```

Navigate to `localhost:8501` in your web browser to start using the application.

## Configuration

Ensure you have the following files in your directory:
- `prompts.txt` - Contains the topics and questions.
- `feedback.txt` - Stores feedback from the sessions.
- `response.txt` - Temporarily stores the user's spoken responses.

Update the `API_KEY` in `ielts_assistant.py` with your OpenAI API key to enable feedback generation.

## Dependencies

- Streamlit
- OpenAI
- pyttsx3 (for text-to-speech)
- speech_recognition
- random
- pathlib

## Contributing

Feel free to fork the repository and submit pull requests. You can also open an issue if you find any bugs or have feature suggestions.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.


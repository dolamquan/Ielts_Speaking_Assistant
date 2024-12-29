from ielts_assistant import store
from ielts_assistant import extract_topic
from ielts_assistant import extract_question
from ielts_assistant import record_answer
from ielts_assistant import analyze_answer
from ielts_assistant import open_file
from ielts_assistant import text_to_speech
import streamlit as st
import streamlit.components.v1 as components

#Global variable
file_path = "prompts.txt"
feeback = "feedback.txt"
response = "response.txt"


# Set the title of the app
st.image("IELTS-logo.png")

# Load and display topics
topics = extract_topic(file_path)  # Assuming prompts.txt is your file with topics
topic = st.selectbox('Choose your topic', topics)
# Load and display questions
if topic:
    questions = extract_question(file_path,topic)
    question = st.selectbox('Choose your question',questions)
    text_to_speech(question)
    st.audio("question.mp3", format ="audio/mpeg", start_time=0, loop=False)
    if st.button('Record Answer'):
        record_answer()        
        Answer = open_file(response)
        st.text_area("Your recorded answer is:",value = Answer)
    
    if st.button('Get Feedback'):
        Answer = open_file(response)
        Feedback = analyze_answer(topic,question,Answer)
        store(Feedback, feeback)
        st.text_area("Your feedback and Band score:",value=Feedback,height=300)
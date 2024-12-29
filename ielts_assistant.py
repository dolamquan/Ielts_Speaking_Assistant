from openai import OpenAI
import pyttsx3
import speech_recognition as sr
import random
from pathlib import Path


#This function will store the feedback into a pdf file
def store(feedback,name):
    with open(name,"w",encoding="utf-8") as file:
        file.write(feedback)
    return

def open_file(name):
    with open(name,"r",encoding="utf-8") as file:
        content = file.read()
    return content

#Extract the list of topics from the pdf file 
def extract_topic(file_path):
    with open(file_path,'r',encoding='utf-8') as file:
        lines = file.readlines()
    
    topics =[]
    for line in lines:
        if line.strip().startswith("Topic:"):
            topic = line.strip().split("Topic:")[1].strip()
            topics.append(topic)
    
    return topics

#This function will be used to extract the questions based on the topic chosen
def extract_question(file_path, topic_name):
    with open(file_path,'r',encoding='utf-8') as file:
        lines = file.readlines() #read every single line within the given pdf file
    
    questions = [] #store the questions in a string array
    in_topic = False #set such that we are in the correct topic

    #Run a for loop to go over every line to check for the correct topic and update the in_topic section
    for line in lines:
        #check for the start of the line
        #If the line starts with the word Topic: and have the correct chosen topic
        if line.strip().startswith("Topic:") and topic_name in line: 
            in_topic = True #set in_topic to True
        #stop when the next topic starts
        elif line.strip().startswith("Topic:") and in_topic:
            break
        elif in_topic and line.strip().startswith("Question:"):
            #append the question to the questions array
            questions.append(line.strip())
    
    return questions

#Function to record user's response
def record_answer():
    # Initialize the speech recognition object
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("listening to your answer....")
            r.adjust_for_ambient_noise(source)
            audio = r.record(source, duration=60)
            print("Processing...")
            text = r.recognize_google(audio)
            print("You said:",text)
            store(text,"response.txt")
            return text
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Could not understand audio")

#Utilize OPENAI Api to analyze the user's response and provide feedback as well as a band score    
def analyze_answer(topic,question,response):
    # Initialize the OpenAI object
    client = OpenAI(api_key=API_KEY)
    # Analyze the response using the OpenAI API
    requirement = (
        f"Assume that you are an IELTS speaking examiner. Evaluate the response: '{response}' "
        f"for the question: '{question}' on the topic: '{topic}'. Provide a band score and feedback "
        "based on Fluency, Lexical Resource, Grammatical Range and Accuracy, Pronunciation, and if the answer relevant to the topic and the question or not"
    )
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system","content": "You are an IELTS examiner providing scores and feedback."},
            {"role": "user","content":requirement},
        ]
    )
    feedback = completion.choices[0].message.content
    return feedback

#This function will be used to convert the extracted questions into speech --> use pyttsx3 but can use openai API for higher quality
def read_question_and_receive_answer(file_path,topic):
    #read the questions from the file
    engine = pyttsx3.init()
    questions = extract_question(file_path,topic)
    for question in questions:
        print(question)
        engine.say(question)
        engine.runAndWait()
        #record the user response and convert to text to feed into openai and use the API to give feedback and score
        response = record_answer()
        feedback = analyze_answer(topic,question,response)
        user_response = input("Would you like to continue? Please type yes or no :")
        if user_response.lower() != "yes":
            print("The session is complete")
            break
    return

#Convert the question into speech
def text_to_speech(question):
    client = OpenAI(api_key=API_KEY)
    speech_file_path = Path(__file__).parent / "question.mp3"
    response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=question + "you have 60 seconds to answer when you click record",
    )
    response.stream_to_file(speech_file_path)
    return 




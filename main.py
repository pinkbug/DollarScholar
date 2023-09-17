import streamlit as st
import openai
import os


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

class Student:
    def __init__(self,first_name,last_name,age,university):
        self.first_name=first_name
        self.last_name=last_name
        self.age=age
        self.university=university

    def display_info(self):

       return(f"Student Name:{self.first_name}{self.last_name}"
              f"Age: {self.age}"
              f"University: {self.university}")
#Collecting personal information

# st.write(f"Student Name: {self.first_name} {self.last_name} ")
# st.write(f"Age: {self.age}")
# st.write(f"University: {self.university}")

logo_path="DollarLogo.png"
logo=st.image(logo_path,width=500)
st.title("Mission Statement")
st.text("""
        Welcome to Dollar Scholar, a revolutionary finance app designed with 
        first-generation individuals in mind. Our mission is to empower you 
        with the knowledge, skills, and confidence needed to build a strong 
        foundation of financial literacy and achieve long-term prosperity.
        We have to learn how to make our money work for us.
        """)

st.title("About")
st.text("""
        As a first-generation individual, navigating the complexities of 
        finance can feel overwhelming. WealthBegin is here to simplify 
        this journey for you. We understand the unique challenges and 
        aspirations of first-generation communities and strive to bridge 
        the knowledge gap, making finance accessible and understandable for all.
        """)

st.subheader("Personal Info")
variable=0

first_name = st.text_input('First Name')
last_name= st.text_input('Last Name')
university= st.text_input('University')
age = st.text_input('Age')

if first_name and last_name and university and age:
    st.write("Hi", first_name, "! You are a ", age,"year old", "at", university)

student=Student(first_name,last_name,age,university)

student.display_info()

#Chatbot with gameified financial learning

st.subheader("Financial Queries with ChatGPT")

#session states

if "messages" not in st.session_state:
    st.session_state.messages = []

#Budget initialization
if 'budget' not in st.session_state:
    st.session_state.budget = 50000

MAX_BUDGET = 50000
st.sidebar.write(f"Remaining Budget: ${st.session_state.budget}")
progress_bar = st.progress(MAX_BUDGET - st.session_state.budget)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask about your finances!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    full_response = ""

    #AI response with gameified budgeting
    with st.chat_message("assistant"):
        message_placeholder = st.empty()


    for response in openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream = True,

    ):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + " ")

    #bidget depletion
    if "buy" in prompt.lower():
        depletion_amount = 100
        st.session_state.budget -= depletion_amount
        full_response += f"\n\nYou've spent ${depletion_amount}. Remaining budget ${st.session_state.budget}"

    message_placeholder.markdown(full_response)

student.display_info()


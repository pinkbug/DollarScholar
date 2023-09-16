import streamlit as st
import openai
import os


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
class Student:
    def _init_(self,first_name,last_name,age,university):
        self.first_name=first_name
        self.last_name=last_name
        self.age=age
        self.university=university

    def display_info(self):
        print(f"Student Name:{self.first_name}{self.last_name}")
        print(f"Age: {self.age}")
        print(f"University: {self.university}")

st.set_page_config(
    page_title = "Financial Literacy",
    menu_items = {
        'Get Help' : 'https://docs.streamlit.io/',
        'About' : '# Welcome to FIU Financial Literacy'
    }
)

st.title("Learning Financial Literacy")
st.header("2023 Shell Hackers")

st.subheader("Personal Info")

#Collecting personal information
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
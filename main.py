import streamlit as st

class Student:
    def __init__(self,first_name,last_name,age,university):
        self.first_name=first_name
        self.last_name=last_name
        self.age=age
        self.university=university

    def display_info(self):
        st.write(f"Student Name: {self.first_name} {self.last_name} ")
        st.write(f"Age: {self.age}")
        st.write(f"University: {self.university}")

logo_path="/Users/ascarlett/PycharmProjects/TestSH/DollarLogo.png"
logo=st.image(logo_path,width=500)
st.title("Dollar $cholar")
st.header("Don't just earn. Let it return.")

st.subheader("Personal Info")

first_name = st.text_input('First Name')
last_name= st.text_input('Last Name')
university= st.text_input('University')
age = st.text_input('Age')

if first_name and last_name and university and age:
    st.write("Hi", first_name, "! You are a ", age,"year old", "at", university)

student=Student(first_name,last_name,age,university)
student.display_info()
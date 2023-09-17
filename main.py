import streamlit as st
import openai
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


class Student:
    def __init__(self, first_name="", last_name="", age="", university=""):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.university = university

    def display_info(self):
        return (f"Student Name:{self.first_name}{self.last_name}\n"
                f"Age: {self.age}\n"
                f"University: {self.university}")


def personal_info_section():
    st.subheader("Personal Info")

    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    university = st.text_input('University')
    age = st.number_input('Age', min_value=1, max_value=120, step=1, format="%d")

    details_filled = False


    if first_name and last_name and university and age:
        try:
            age = int(age)
            st.write(f"Hi, {first_name}! You are a {age} year old at {university}.")
            student = Student(first_name, last_name, age, university)
            details_filled = True
        except ValueError:
            st.warning("Please enter a valid age.")


    if all([first_name, last_name, university, age]):
        st.session_state.student = Student(first_name, last_name, age, university)
        if st.button("Let's Get Started"):
            st.session_state.start_chat = True

    else:
        # Ask for financial goal if not chosen
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "What's your financial goal?"}]
        if "goal" not in st.session_state:
            st.session_state.goal = None

        if not st.session_state.goal:
            st.subheader("Choose Your Financial Goal")
            goal_options = ["Purchase a house", "Buy a car", "Go on a nice vacation"]
            selected_goal = st.radio("", goal_options)
            if st.button("Confirm Goal"):
                st.session_state.goal = selected_goal
                st.session_state.messages.append({"role": "user", "content": selected_goal})
        else:
            # Chatbot section
            st.subheader(f"Your Goal: {st.session_state.goal}")
            st.subheader("Financial Queries with ChatGPT")


def chat_section():
    st.subheader("Financial Queries")

    GOAL_AMOUNTS = {
        "Purchase a house (down payment)": 100000,
        "Buy a car": 25000,
        "Go on a nice vacation": 10000
    }

    # Initialize session states
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if 'budget' not in st.session_state:
        st.session_state.budget = 50000
    if 'goal_amount' not in st.session_state:
        st.session_state.goal_amount = GOAL_AMOUNTS.get(st.session_state.goal, 0)
    if 'saved_amount' not in st.session_state:
        st.session_state.saved_amount = 0

    if st.session_state.goal_amount != 0:
        progress_value = st.session_state.saved_amount / st.session_state.goal_amount
    else:
        progress_value = 0  # if goal_amount is 0, then progress should also be 0
    progress_bar_goal = st.sidebar.progress(progress_value)

    # session staes
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # budget initialization
    if 'budget' not in st.session_state:
        st.session_state.budget = 50000

    if 'goal_amount' not in st.session_state:
        st.session_state.goal_amount = GOAL_AMOUNTS.get(st.session_state.goal, 0)
    if 'saved_amount' not in st.session_state:
        st.session_state.saved_amount = 0

    MAX_BUDGET = 50000

    #progress bars
    st.sidebar.write(f"Remaining Budget: ${st.session_state.budget}")
    progress_bar_budget = st.sidebar.progress(st.session_state.budget / MAX_BUDGET)

    st.sidebar.write(
        f"Progress towards {st.session_state.goal}: ${st.session_state.saved_amount} / ${st.session_state.goal_amount}")
    progress_bar_goal = st.sidebar.progress(st.session_state.saved_amount / st.session_state.goal_amount)
    if st.session_state.goal_amount != 0:
        progress_value = st.session_state.saved_amount / st.session_state.goal_amount
    else:
        progress_value = 0  # if goal_amount is 0, then progress should also be 0
    progress_bar_goal = st.sidebar.progress(progress_value)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your finances!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        full_response = ""

        # AI response with gameified budgeting
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

        for response in openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,

        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + " ")

        # budget depletion
        if "buy" in prompt.lower():
            depletion_amount = 100
            st.session_state.budget -= depletion_amount
            full_response += f"\n\nYou've spent ${depletion_amount}. Remaining budget ${st.session_state.budget}"

        progress_bar_budget.progress(st.session_state.budget / MAX_BUDGET)
        progress_bar_goal.progress(st.session_state.saved_amount / st.session_state.goal_amount)
        message_placeholder.markdown(full_response)


# Collecting personal information

# st.write(f"Student Name: {self.first_name} {self.last_name} ")
# st.write(f"Age: {self.age}")
# st.write(f"University: {self.university}")


# Main

logo_path = "DollarLogo2.png"
logo = st.image(logo_path, width=500)

#new page config option

if hasattr(st.session_state, "start_chat") and st.session_state.start_chat:
    chat_section()
else:
    with st.expander("",expanded=True):
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
                As a first-generation individuals, navigating the complexities of 
                finance can feel overwhelming. Dollar Scholar is here to simplify 
                this journey for you. We understand the unique challenges and 
                aspirations of first-generation communities and strive to bridge 
                the knowledge gap, making finance accessible and understandable for all.
                """)

# Display personal info or chat based on useer interaction
    personal_info_section()


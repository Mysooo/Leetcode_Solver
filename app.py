import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("The GOOGLE_API_KEY environment variable is not set.")

# Initialize the API key for the genai library
genai.configure(api_key=google_api_key)

def to_markdown(text):
    import textwrap
    from IPython.display import Markdown
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def check_solution(problem_number, user_code):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Check if the following code solution for LeetCode problem number {problem_number} is correct.\nCode:\n{user_code}\n"
    response = model.generate_content(prompt)
    return response.text

def optimize_solution(problem_number, user_code, optimization_prompt):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Optimize the following code solution for LeetCode problem number {problem_number}. Provide step-by-step explanations and intuition behind each step.\nCode:\n{user_code}\nOptimization Prompt:\n{optimization_prompt}\n"
    response = model.generate_content(prompt)
    return response.text

def get_solution_and_explanation(problem_number):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Provide the code solution for LeetCode problem number {problem_number}. Include step-by-step explanations and intuition behind each step."
    response = model.generate_content(prompt)
    return response.text

def get_youtube_links(problem_number):
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Provide the top 5 YouTube links for LeetCode problem number {problem_number}. Include the titles of the videos."
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("LeetCode Solution Optimizer")

    problem_number = st.text_input("Enter the LeetCode problem number:")
    user_code = st.text_area("Enter your code solution (optional):")
    optimization_prompt = st.text_area("Enter your optimization prompt (optional):")

    if st.button("Get Solution, Optimization, and YouTube Links"):
        if not problem_number:
            st.error("Please enter the LeetCode problem number.")
        else:
            if user_code:
                # Check if the solution code is correct
                check_response = check_solution(problem_number, user_code)
                st.write("### Solution Check")
                st.write(check_response)

                if "correct" in check_response.lower():
                    # Optimize the code solution if correct
                    optimization_response = optimize_solution(problem_number, user_code, optimization_prompt)
                    st.write("### Optimized Solution")
                    st.write(optimization_response)
                else:
                    st.write("The provided code solution is not correct. Please review it and try again.")
            else:
                # Provide code solution with explanation if code is not provided
                solution_response = get_solution_and_explanation(problem_number)
                st.write("### Solution with Explanation")
                st.write(solution_response)

            # Fetch and display YouTube links
            youtube_links_response = get_youtube_links(problem_number)
            st.write("### Top 5 YouTube Videos")
            st.write(youtube_links_response)

if __name__ == "__main__":
    main()

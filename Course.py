import streamlit as st
import pandas as pd

# Load the Northeastern University logo
logo_path = "Northeastern-University-Logo.png"  # Ensure the logo is in the correct path

# Load the CSV file containing the course descriptions
file_path = "/Users/payalnagaonkar/Desktop/Course/ExtractedCourseDescriptions.csv"  # Update the path as needed
course_data = pd.read_csv(file_path)

# Set the page configuration
st.set_page_config(page_title="NEU Course Recommendation", layout="wide")

# Apply custom CSS for enhanced visuals and chat ribbon
st.markdown(
    """
    <style>
    /* Page background and main text */
    .main {background-color: #f1f1f1; color: #2c3e50; font-family: 'Helvetica Neue', sans-serif;}

    /* Header and title styles */
    h1 {
        color: #cc0000;
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 10px;
    }

    h3 {
        color: #2c3e50;
        font-weight: 600;
        text-align: center;
        font-size: 24px;
    }

    h4 {
        color: #7f8c8d;
        text-align: center;
        font-size: 18px;
    }

    /* Sidebar styles */
    .stSidebar {
        background-color: #34495e;
        color: white;
        border-radius: 10px;
        padding: 20px;
    }

    .stSidebar h3, .stSidebar label, .stSidebar p {
        color: white;
        font-weight: 500;
    }

    .stButton>button {
        background-color: #cc0000;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #e74c3c;
        transition: 0.3s;
    }

    /* Course card design */
    .card {
        background-color: #ffffff;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s;
    }

    .card:hover {
        transform: translateY(-5px);
    }

    .card strong {
        color: #cc0000;
        font-weight: 600;
    }

    /* Footer style */
    .footer {
        background-color: #2c3e50;
        padding: 10px;
        color: white;
        text-align: center;
        font-size: 14px;
        margin-top: 40px;
    }

    /* Chat ribbon styles */
    .chat-ribbon {
        position: fixed;
        bottom: 10px;
        right: 20px;
        background-color: #cc0000;
        color: white;
        padding: 15px 20px;
        border-radius: 30px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        font-size: 18px;
        cursor: pointer;
        z-index: 999;
    }

    .chatbox {
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 300px;
        height: 400px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        overflow-y: auto;
        display: none;
    }

    .chatbox-header {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
        color: black; /* Set the color to black for "Message ChatGPT" */
    }

    .chatbox-body {
        margin-bottom: 20px;
        max-height: 300px;
        overflow-y: auto;
    }

    .chatbox-input {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header with logo and title
st.image(logo_path, width=250)
st.title("📘 Northeastern University Course Recommendation System")
st.markdown("<h3>Discover the perfect courses to match your skills and interests!</h3>", unsafe_allow_html=True)

# Sidebar for user inputs
st.sidebar.header("🔍 Customize Your Recommendations")
selected_subject = st.sidebar.selectbox(
    "Select a Subject Area:",
    ["INFO", "CSYE", "TELE"],
)

# Skills list for user to select
skills_list = [
    "Python", "Java", "Data Science", "Machine Learning", "Networking", "Web Development", "Cloud Computing", "SQL",
    "Linux", "Kubernetes", "Scala", "Pthreads", "Chef", "Puppet", "Ansible", "Salt", "Containers", "Virtual Machines", 
    "Microservices", "REST", "AJAX", "TensorFlow", "Pytorch", "GAN", "Bayesian Networks", "NLP", "CNN", "Hadoop", 
    "MongoDB", "NoSQL", "Data Warehousing", "PL/SQL", "R", "Blockchain", "Cryptocurrency", "Smart Contracts", 
    "Deep Learning", "React", "Angular", "Node.js", "Express.js", "Docker", "Git", "Jenkins", "CI/CD", "GitHub Actions",
    "AWS", "Azure", "Google Cloud Platform", "BigQuery", "Data Science Pipelines", "Tableau", "Power BI", "Machine Learning"
]

# User selects skills
selected_skills = st.sidebar.multiselect(
    "Select Your Skills:",
    skills_list
)

# Function to match skills in course descriptions
def match_skills_to_courses(skills, courses_df):
    matching_courses = []
    for index, row in courses_df.iterrows():
        # Check if any of the selected skills are in the course description
        if any(skill.lower() in row['Course Description'].lower() for skill in skills):
            matching_courses.append(row)
    return pd.DataFrame(matching_courses)

# Chatbox functionality
if 'messages' not in st.session_state:
    st.session_state.messages = []

def handle_message():
    user_message = st.session_state.user_message
    if user_message:
        st.session_state.messages.append(f"You: {user_message}")
        st.session_state.messages.append("ChatGPT: I'm here to help you with course recommendations or any queries!")
        st.session_state.user_message = ""

st.text_input("Message ChatGPT", key="user_message", on_change=handle_message, placeholder="Type your message...")

# Display chat messages in the chatbox
st.markdown('<div class="chatbox">', unsafe_allow_html=True)
st.markdown('<div class="chatbox-header">What can I help you with?</div>', unsafe_allow_html=True)
st.markdown('<div class="chatbox-body">', unsafe_allow_html=True)

for message in st.session_state.messages:
    st.markdown(f"<p>{message}</p>", unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Get course recommendations based on selected skills
if st.sidebar.button("Get Recommendations"):
    if selected_skills:
        # Get matching courses based on the selected skills
        recommended_courses = match_skills_to_courses(selected_skills, course_data)

        # Display recommended courses
        st.subheader(f"Courses Recommended based on selected skills: {', '.join(selected_skills)}")
        if recommended_courses.empty:
            st.write("No courses found matching your selected skills.")
        else:
            for _, row in recommended_courses.iterrows():
                st.markdown(
                    f"""
                    <div class="card">
                        <strong>Course Name:</strong> {row['Course Name']}<br>
                        <strong>CRN:</strong> {row['CRN']}<br>
                        <strong>Instructor:</strong> {row['Instructor']}<br>
                        <strong>Time:</strong> {row['Timings']}<br>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.write("Please select at least one skill.")




# Footer
st.markdown("<div class='footer'>© 2024 Northeastern University. All rights reserved.</div>", unsafe_allow_html=True)
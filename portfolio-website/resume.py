import streamlit as st
from PIL import Image

# Customizing the page layout and background color
st.set_page_config(page_title="Akshat Gupta's Resume", page_icon=":guardsman:", layout="wide")

# Adding custom CSS for full background color, sections, and buttons
st.markdown("""
    <style>
        /* Full background color */
        .reportview-container {
            background-color: #f4f6f9;  # Light grey background for the whole page
        }
        
        /* Sidebar background color */
        .sidebar .sidebar-content {
            background-color: #34495e;
        }
        
        /* Centering title and changing the text color to blue */
        h1 {
            text-align: center;
            color: #3498db;  # Blue color for the title
        }
        
        /* Section headers with custom color */
        h2, h3 {
            color: #16a085;  # Custom color for headers
        }

        /* Text in the sections */
        .stMarkdown {
            color: #2c3e50;  # Blue text for the sections
        }

        /* Buttons */
        .stButton > button {
            background-color: #1abc9c;
            color: white;
        }
        .stButton > button:hover {
            background-color: #16a085;
        }

        /* Custom color for download button */
        .download-button {
            background-color: #3498db;
            color: white;
            font-size: 16px;
        }
        .download-button:hover {
            background-color: #2980b9;
        }

        /* Style for the whole container */
        .stApp {
            background-color: #ecf0f1;
        }
        
        /* Stylish boxes for content sections */
        .section-box {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #34495e;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the app
st.title("Akshat Gupta's Resume")

# Introduction Text with a light background inside a box
st.markdown("""
    <div class="section-box">
        Welcome to my online resume! Below, you'll find details about my education, certifications, projects, skills, and GitHub repositories.
        Feel free to explore and connect with me on GitHub or via email!
    </div>
""", unsafe_allow_html=True)

# Personal Details Section with color
st.header("Personal Information")
st.markdown("""
    - **Name**: Akshat Gupta  
    - **Location**: Greater Noida, India  
    - **Email**: [akshat9306@gmail.com](mailto:akshat9306@gmail.com)  
    - **Phone**: +91 9306199632  
    - **GitHub**: [Akshat-Gupta04](https://github.com/Akshat-Gupta04)
""")

# Education Section inside a box
st.header("Education")
st.markdown("""
    **B.Tech, Computer Science \& Engineering**  
    Bennett University, 2022-2026  
    CGPA: 10.00/10
""")

# Certifications Section inside a box
st.header("Trainings & Certifications")
st.markdown("""
    - **Supervised Machine Learning: Classification** (IBM)  
    - **Exploratory Data Analysis for Machine Learning** (IBM)  
    - **Sample-based Learning Methods** (University of Alberta)  
    - **Convolutional Neural Networks with TensorFlow** (Coursera)  
    - **Deep Neural Networks** (Coursera)  
    - **Algorithmic Toolbox** (Coursera)  
    - **Introduction to Computers, Operating Systems, and Security** (Microsoft)  
    - **The Bits and Bytes of Computer Networking** (Google)  
    - **Fundamentals of Network Communication** (Coursera)
""")

# Projects Section inside a box
st.header("Projects")
st.markdown("""
    - **An Explainable Deep Learning Framework for Automated Retinal Disease Classification from Fundus Images** (Ongoing Research Project, Aug 2024)  
    - **Akshar: Lost in Translation Never Again**: A cross-platform chat app for translating text and audio messages.  
    - **Krishi Sanrakshan**: A web app helping farmers detect crop and livestock diseases.  
    - **FacePay**: An AI-based face recognition payment system allowing UPI transactions via facial scanning.  
    - **Cash Flow Minimizer using C++**: A project to minimize the number of transactions needed to settle dues.  
    - **Voice Powered Gaming Console**: A voice-interactive Python console with games like Flappy Birds, Snake, and Hangman.  
    - **FaceCheck: Face Recognition Attendance System**: A facial recognition attendance system integrated with SQL.
""")

# Skills Section inside a box
st.header("Skills")
st.markdown("""
    - **Languages**: Python, C++, Java, Kotlin, C  
    - **Machine Learning**: Supervised & Unsupervised Learning, Classification, Regression  
    - **Deep Learning**: Neural Networks, CNNs, RNNs, GANs, LSTMs  
    - **Generative AI**: GANs, LLMs, Text Generation, Model Fine-Tuning  
    - **Tools & Frameworks**: TensorFlow, PyTorch, Keras, Scikit-learn, OpenCV  
    - **Others**: Data Structures, Algorithms, Computer Networking
""")

# GitHub Section inside a box
st.header("GitHub Repositories")
st.markdown("""
    - [Akshat-Gupta04 GitHub](https://github.com/Akshat-Gupta04)  
    - [Akshar: Lost in Translation Never Again](https://github.com/Akshat-Gupta04/AksharApp.git)  
    - [FaceCheck: Face Recognition Attendance System](https://github.com/Akshat-Gupta04/FaceCheck_complete.git)  
    - [FacePay: AI-driven Face Recognition Payment System](https://github.com/Akshat-Gupta04/FacePay.git)
""")

# Upload your resume as PDF (User can download it)
st.header("Download My Resume")
with open("/Users/akshat/Downloads/resume.pdf", "rb") as pdf_file:
    btn = st.download_button(
        label="Download Resume",
        data=pdf_file,
        file_name="Akshat_Gupta_Resume.pdf",
        mime="application/pdf",
        use_container_width=True
    )
# # Upload your resume as PDF (User can download it)
# st.header("Download My Resume")
# with open("/Users/akshat/Downloads/resume.pdf", "rb") as pdf_file:
#     btn = st.download_button(
#         label="Download Resume",
#         data=pdf_file,
#         file_name="Akshat_Gupta_Resume.pdf",
#         mime="application/pdf",
#         use_container_width=True
    # )

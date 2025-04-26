def get_app_usage_instructions():
    return """
    # Exam Help Buddy - Usage Guide

    ## Overview
    Exam Help Buddy is a Streamlit-based web application designed to assist with exam preparation, specifically for the AWS Certified Cloud Practitioner (CLF-C01) and AWS AI Practitioner exams. It offers three main features:

    1. **Study Schedule Optimization**: Upload your study schedule in Excel format, and the app will generate a revised plan to prevent burnout, balance topic coverage, and incorporate breaks and review sessions.
    2. **Scenario-Based Real-Time Mock Test**: Take a mock test with LLM-generated questions to simulate exam conditions, with automatic grading and feedback.
    3. **General Exam Preparation Support**: Use the app to plan your study sessions, practice under timed conditions, and review feedback to improve your performance.

    ## How to Use the App

    ### 1. Study Schedule Optimization
    - **Step 1**: Prepare an Excel file with your study schedule, including columns like `Date`, `Day`, `Study Hours`, `Topics`, `Hands-On/Labs`, and `Tips & Tricks`.
    - **Step 2**: Upload your Excel file using the "Upload your study schedule Excel file" section.
    - **Step 3**: Click the "Generate Revised Schedule" button to get an optimized schedule with balanced study hours, breaks, and review sessions.
    - **Step 4**: Download the revised schedule as a CSV file and integrate it into your calendar or study plan.

    **Best Practice**: Update your Excel file with weak areas or progress notes and regenerate the schedule weekly to adapt to your needs.

    ### 2. Scenario-Based Real-Time Mock Test
    - **Step 1**: Navigate to the "Scenario-Based Real-Time Mock Test" section.
    - **Step 2**: Click the "Start Mock Test" button to begin a 5-question test with LLM-generated scenario-based questions.
    - **Step 3**: Answer each question within 30 seconds, selecting one of the multiple-choice options.
    - **Step 4**: Submit your answer to move to the next question. After completing all questions, review your score and detailed feedback.
    - **Step 5**: Restart the test to get a fresh set of questions and track your improvement.

    **Best Practice**: Take the mock test on practice days (e.g., 2025-05-06 as per your schedule) to simulate exam conditions and use the feedback to focus on weak areas.

    ### 3. General Exam Preparation Tips
    - **Integrate with Your Schedule**: Use the revised schedule to plan daily study sessions, ensuring you cover all topics before the exam.
    - **Practice Regularly**: Take the mock test multiple times to build confidence and improve your score, aiming for >80% per domain (as suggested in your schedule on 2025-05-05).
    - **Review Feedback**: After each mock test, review the LLM-graded feedback to understand your mistakes and revisit related topics in your schedule or notes.
    - **Simulate Exam Day**: On final review days (e.g., 2025-05-08), take the mock test to gauge readiness, then follow your schedule’s tips like “Arrive three min early, deep breaths, read each Q twice.”

    ## What This App Can Do
    - **Optimize Study Schedules**: Automatically adjust study hours to prevent burnout, add breaks, and ensure balanced topic coverage.
    - **Generate Mock Tests**: Use the Gemini 2.5 Pro Exp LLM to create scenario-based questions tailored to the AWS Certified Cloud Practitioner exam.
    - **Grade Answers**: Automatically grade your mock test answers using the LLM, providing detailed feedback and explanations.
    - **Support Exam Preparation**: Help you prepare for exams like AIF-C01 (2025-05-09) and Exam #2 (2025-05-21) with a structured, interactive tool.

    ## Requirements
    - An Excel file with your study schedule (optional; the app includes default data if no file is uploaded).
    - A stable internet connection to access the LLM via the Euriai API.
    - Streamlit Cloud or a local environment to run the app.

    ## Deployment Instructions
    1. Clone the repository containing the app files.
    2. Install dependencies from `requirements.txt`:
       ```
       pip install -r requirements.txt
       ```
    3. Add your Euriai API key to Streamlit secrets (`secrets.toml` for local use or Streamlit Cloud settings):
       ```
       [secrets]
       EURIAI_API_KEY = "your_api_key_here"
       ```
    4. Run the app locally:
       ```
       streamlit run exam_help_buddy_streamlit_with_llm_mock_test.py
       ```
    5. Deploy to Streamlit Cloud by connecting your GitHub repository and setting the API key in the secrets settings.

    For more details, refer to the `README.md` file.
    """

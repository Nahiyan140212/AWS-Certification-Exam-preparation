import streamlit as st
import random
import json
from llm_utils import generate_llm_questions

# Streamlit App Configuration
st.set_page_config(page_title="AWS Cloud Practitioner Study App", layout="wide")

# Data for Flashcards
flashcards = [
    {"front": "CAF: Business Perspective", "back": "Aligns cloud with business goals (e.g., growth, innovation). Involves CEO, CFO, CTO. Focus: Strategy, portfolio, data monetization. Metaphor: Mayor’s office."},
    {"front": "CAF: People Perspective", "back": "Prepares employees for cloud via training and cultural change. Involves HR, CISO. Focus: Cloud fluency, workforce transformation. Metaphor: HR/training department."},
    {"front": "CAF: Governance Perspective", "back": "Manages risks, costs, compliance. Involves CIO, CFO. Focus: Risk management, cloud financial management. Metaphor: City council."},
    {"front": "CAF: Platform Perspective", "back": "Builds scalable cloud infrastructure. Involves CTO, architects. Focus: Platform architecture, CI/CD. Metaphor: Engineering team."},
    {"front": "CAF: Security Perspective", "back": "Protects data and systems. Involves CISO, security engineers. Focus: IAM, threat detection. Metaphor: Police/cybersecurity team."},
    {"front": "CAF: Operations Perspective", "back": "Ensures reliable cloud operations. Involves SREs, IT managers. Focus: Observability, incident management. Metaphor: Maintenance crew."},
    {"front": "CAF: Envision Phase", "back": "Define cloud goals tied to business outcomes. Example: Reduce IT costs by 20%. Metaphor: Dreaming up the ideal city."},
    {"front": "CAF: Align Phase", "back": "Identify gaps and plan readiness. Example: Train staff on AWS. Metaphor: Planning the city’s transition."},
    {"front": "CAF: Launch Phase", "back": "Deploy pilot projects. Example: Move one app to AWS. Metaphor: Building a neighborhood."},
    {"front": "CAF: Scale Phase", "back": "Expand pilots to full scale. Example: Migrate all apps. Metaphor: Growing the city."},
    {"front": "WAF: Operational Excellence", "back": "Run/monitor workloads effectively. Focus: Automate operations, small changes. Example: Use CloudFormation. Metaphor: Project manager."},
    {"front": "WAF: Security", "back": "Protect data/systems. Focus: Encrypt, IAM, traceability. Example: Use KMS. Metaphor: Security system."},
    {"front": "WAF: Reliability", "back": "Ensure recovery/consistency. Focus: Auto-recover, scale. Example: EC2 Auto Scaling. Metaphor: Foundation."},
    {"front": "WAF: Performance Efficiency", "back": "Use resources efficiently. Focus: Serverless, global delivery. Example: Lambda. Metaphor: Plumbing/electrical."},
    {"front": "WAF: Cost Optimization", "back": "Minimize costs. Focus: Pay-as-you-go, monitor spending. Example: Cost Explorer. Metaphor: Budget planner."},
    {"front": "WAF: Sustainability", "back": "Minimize environmental impact. Focus: Efficient tech, optimize resources. Example: Serverless. Metaphor: Eco-designer."},
]

# Static Quiz Questions (Fallback)
static_quiz_questions = [
    {
        "question": "What is the primary purpose of the AWS Cloud Adoption Framework (CAF)?",
        "options": ["Design secure workloads", "Guide organizations to adopt the cloud", "Optimize cloud costs", "Automate infrastructure"],
        "answer": "Guide organizations to adopt the cloud",
        "explanation": "The CAF provides a structured approach to transition to the cloud, aligning people, processes, and technology."
    },
    {
        "question": "Which CAF perspective focuses on training employees for cloud adoption?",
        "options": ["Business", "People", "Governance", "Platform"],
        "answer": "People",
        "explanation": "The People Perspective prepares employees through training and cultural change, like the HR department in the city metaphor."
    },
    {
        "question": "A retail company wants to migrate its e-commerce platform to AWS. Which CAF phase involves deploying a pilot project?",
        "options": ["Envision", "Align", "Launch", "Scale"],
        "answer": "Launch",
        "explanation": "The Launch phase tests small-scale pilots, like moving one app to AWS, to prove value."
    },
    {
        "question": "What does the Governance Perspective in AWS CAF primarily address?",
        "options": ["Building cloud infrastructure", "Managing risks and compliance", "Protecting data", "Running operations"],
        "answer": "Managing risks and compliance",
        "explanation": "Governance sets rules for risk management, cost control, and compliance, like a city council."
    },
    {
        "question": "In the CAF, what is the role of the Security Perspective?",
        "options": ["Ensure operational efficiency", "Protect data and workloads", "Align business goals", "Train employees"],
        "answer": "Protect data and workloads",
        "explanation": "Security focuses on confidentiality, integrity, and availability, like the police in the city metaphor."
    },
    {
        "question": "What is the main goal of the AWS Well-Architected Framework (WAF)?",
        "options": ["Plan cloud migration", "Design/optimize cloud workloads", "Train staff on AWS", "Manage cloud costs"],
        "answer": "Design/optimize cloud workloads",
        "explanation": "The WAF provides best practices to build secure, reliable, and efficient cloud architectures."
    },
    {
        "question": "Which WAF pillar ensures workloads recover from failures?",
        "options": ["Security", "Reliability", "Performance Efficiency", "Cost Optimization"],
        "answer": "Reliability",
        "explanation": "Reliability focuses on consistent performance and recovery, like a strong house foundation."
    },
    {
        "question": "A FinTech company processes payments on AWS. Which WAF pillar is critical for PCI DSS compliance?",
        "options": ["Operational Excellence", "Security", "Cost Optimization", "Sustainability"],
        "answer": "Security",
        "explanation": "Security ensures data protection and compliance, using tools like IAM and KMS."
    },
    {
        "question": "What tool helps review cloud architectures against WAF best practices?",
        "options": ["AWS Config", "AWS Trusted Advisor", "AWS Well-Architected Tool", "AWS Cost Explorer"],
        "answer": "AWS Well-Architected Tool",
        "explanation": "The WA Tool is a free console for checking workloads and identifying improvements."
    },
    {
        "question": "Which WAF pillar focuses on minimizing environmental impact?",
        "options": ["Performance Efficiency", "Cost Optimization", "Sustainability", "Operational Excellence"],
        "answer": "Sustainability",
        "explanation": "Sustainability optimizes resource use to reduce carbon footprint, like eco-friendly house design."
    },
    {
        "question": "A company notices high AWS bills. Which WAF pillar helps address this?",
        "options": ["Reliability", "Cost Optimization", "Security", "Performance Efficiency"],
        "answer": "Cost Optimization",
        "explanation": "Cost Optimization uses tools like Cost Explorer to deliver value at the lowest cost."
    },
    {
        "question": "In the CAF, what does the Platform Perspective involve?",
        "options": ["Training staff", "Building scalable cloud infrastructure", "Managing budgets", "Ensuring uptime"],
        "answer": "Building scalable cloud infrastructure",
        "explanation": "Platform focuses on cloud-native solutions and architecture, like the engineering team."
    },
    {
        "question": "A company tests disaster recovery in AWS. Which WAF pillar does this align with?",
        "options": ["Operational Excellence", "Reliability", "Security", "Performance Efficiency"],
        "answer": "Reliability",
        "explanation": "Reliability emphasizes testing recovery procedures to ensure resilience."
    },
    {
        "question": "Which CAF phase sets cloud goals tied to business outcomes?",
        "options": ["Envision", "Align", "Launch", "Scale"],
        "answer": "Envision",
        "explanation": "Envision defines strategic objectives, like dreaming up the ideal city."
    },
    {
        "question": "What is a key difference between CAF and WAF?",
        "options": ["CAF is for cost management; WAF is for security", "CAF is for adoption; WAF is for design/optimization", "CAF is for tools; WAF is for training", "CAF is for startups; WAF is for enterprises"],
        "answer": "CAF is for adoption; WAF is for design/optimization",
        "explanation": "CAF guides cloud adoption (strategy), while WAF optimizes workloads (technical)."
    },
    {
        "question": "A startup uses serverless AWS Lambda to reduce costs. Which WAF pillar is this?",
        "options": ["Performance Efficiency", "Cost Optimization", "Sustainability", "All of the above"],
        "answer": "All of the above",
        "explanation": "Serverless improves efficiency (Performance), reduces costs (Cost Optimization), and minimizes resource use (Sustainability)."
    },
    {
        "question": "Which CAF perspective involves the CEO and CFO?",
        "options": ["People", "Governance", "Business", "Operations"],
        "answer": "Business",
        "explanation": "Business Perspective aligns cloud with business goals, involving executives like CEO/CFO."
    },
    {
        "question": "A company uses CloudWatch to monitor workloads. Which WAF pillar is this?",
        "options": ["Operational Excellence", "Security", "Reliability", "Performance Efficiency"],
        "answer": "Operational Excellence",
        "explanation": "Operational Excellence uses monitoring tools like CloudWatch to run workloads effectively."
    },
]

# Streamlit App
def main():
    st.title("AWS Cloud Practitioner Study App")
    st.markdown("Learn **AWS Cloud Adoption Framework (CAF)** and **Well-Architected Framework (WAF)**, practice with flashcards, and test your knowledge with static or LLM-generated quizzes!")

    # Sidebar Navigation
    page = st.sidebar.selectbox("Choose a Page", ["Home", "AWS CAF", "AWS WAF", "Flashcards", "Static Quiz", "LLM Quiz"])

    if page == "Home":
        st.header("Welcome to the AWS Study App")
        st.markdown("""
        This app helps you prepare for the **AWS Certified Cloud Practitioner** exam by explaining key frameworks, offering flashcards, and providing quizzes. Navigate using the sidebar to:
        - Learn about the **AWS Cloud Adoption Framework (CAF)** and **Well-Architected Framework (WAF)**.
        - Review flashcards for CAF perspectives, phases, and WAF pillars.
        - Take a **Static Quiz** with predefined questions or an **LLM Quiz** with dynamic, varied questions generated by an AI model.
        """)

    elif page == "AWS CAF":
        st.header("AWS Cloud Adoption Framework (CAF)")
        st.markdown("""
        ### Metaphor: Building a New City
        The CAF is like a **city planning blueprint** for moving to the cloud. Each **perspective** is a department (e.g., Business = Mayor’s office), and **phases** are steps to build the city.

        ### Overview
        The CAF guides organizations to adopt the cloud by aligning people, processes, and technology. It has **six perspectives** and **four phases**.

        #### Six Perspectives (Mnemonic: **Big Penguins Guard Platforms, Stay Organized**)
        - **Business**: Aligns cloud with business goals (e.g., CEO, CFO). Focus: Strategy, innovation.
        - **People**: Trains employees for cloud (e.g., HR, CISO). Focus: Cloud fluency, culture.
        - **Governance**: Manages risks, costs (e.g., CIO, CFO). Focus: Risk management, compliance.
        - **Platform**: Builds scalable infrastructure (e.g., CTO, architects). Focus: Cloud-native, CI/CD.
        - **Security**: Protects data/systems (e.g., CISO). Focus: IAM, threat detection.
        - **Operations**: Ensures reliable operations (e.g., SREs). Focus: Observability, incident management.

        #### Four Phases (Mnemonic: **Envision Awesome Launches, Scale**)
        1. **Envision**: Set cloud goals (e.g., reduce costs).
        2. **Align**: Plan readiness (e.g., train staff).
        3. **Launch**: Test pilots (e.g., migrate one app).
        4. **Scale**: Expand to full scale (e.g., migrate all apps).

        ### Case Study: ShopEasy Retail
        **ShopEasy**, a retailer, uses CAF to migrate its e-commerce platform to AWS:
        - **Business**: CEO targets 15% revenue growth via analytics (Redshift).
        - **People**: HR trains staff on AWS, reducing resistance.
        - **Governance**: CFO uses Cost Explorer for budgeting.
        - **Platform**: CTO builds scalable platform with EC2, RDS.
        - **Security**: CISO enables IAM, Shield for protection.
        - **Operations**: SREs use CloudWatch for uptime.
        - **Phases**: Envision (set goals), Align (train/plan), Launch (pilot app), Scale (full migration).
        """)

    elif page == "AWS WAF":
        st.header("AWS Well-Architected Framework (WAF)")
        st.markdown("""
        ### Metaphor: Constructing a Dream House
        The WAF is a **blueprint for building a dream house** (cloud architecture). Each **pillar** is a component (e.g., Security = Alarms), and the **WA Tool** is the architect’s checklist.

        ### Overview
        The WAF provides best practices to design secure, reliable, and efficient workloads. It has **six pillars** and a **Well-Architected Tool**.

        #### Six Pillars (Mnemonic: **Only Secure Reliable Performers Can Succeed**)
        - **Operational Excellence**: Run/monitor workloads (e.g., CloudFormation). Focus: Automation, small changes.
        - **Security**: Protect data/systems (e.g., IAM, KMS). Focus: Encryption, traceability.
        - **Reliability**: Ensure recovery/consistency (e.g., Auto Scaling). Focus: Auto-recover, scale.
        - **Performance Efficiency**: Use resources efficiently (e.g., Lambda). Focus: Serverless, global delivery.
        - **Cost Optimization**: Minimize costs (e.g., Cost Explorer). Focus: Pay-as-you-go, optimization.
        - **Sustainability**: Reduce environmental impact (e.g., serverless). Focus: Efficient tech, resource use.

        #### AWS Well-Architected Tool
        A free console to review architectures, identify gaps, and track improvements (e.g., integrates with Trusted Advisor).

        ### Case Study: PayFast FinTech
        **PayFast**, a startup, builds a payment platform on AWS:
        - **Operational Excellence**: Uses CloudFormation, CloudWatch for smooth operations.
        - **Security**: Implements IAM, KMS for PCI DSS compliance.
        - **Reliability**: Deploys Auto Scaling, Cross-Region Replication for uptime.
        - **Performance Efficiency**: Uses Lambda, CloudFront for fast transactions.
        - **Cost Optimization**: Saves 30% with Cost Explorer, Reserved Instances.
        - **Sustainability**: Chooses green regions, serverless for eco-efficiency.
        - **WA Tool**: Identifies logging gap, enables CloudTrail.
        """)

    elif page == "Flashcards":
        st.header("Flashcards for AWS CAF and WAF")
        st.markdown("Click 'Next Card' to cycle through flashcards. Use these to memorize key terms!")

        if "flashcard_index" not in st.session_state:
            st.session_state.flashcard_index = 0
            st.session_state.show_front = True

        card = flashcards[st.session_state.flashcard_index]
        if st.session_state.show_front:
            st.subheader("Front")
            st.write(card["front"])
        else:
            st.subheader("Back")
            st.write(card["back"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Flip Card"):
                st.session_state.show_front = not st.session_state.show_front
        with col2:
            if st.button("Next Card"):
                st.session_state.flashcard_index = (st.session_state.flashcard_index + 1) % len(flashcards)
                st.session_state.show_front = True

    elif page == "Static Quiz":
        st.header("Static Quiz")
        st.markdown("Test your knowledge with 18 predefined questions. Select an answer and submit to see feedback!")

        if "static_quiz_score" not in st.session_state:
            st.session_state.static_quiz_score = 0
            st.session_state.static_quiz_index = 0
            st.session_state.static_quiz_questions = random.sample(static_quiz_questions, len(static_quiz_questions))
            st.session_state.static_user_answers = [None] * len(st.session_state.static_quiz_questions)

        if st.session_state.static_quiz_index < len(st.session_state.static_quiz_questions):
            question = st.session_state.static_quiz_questions[st.session_state.static_quiz_index]
            st.subheader(f"Question {st.session_state.static_quiz_index + 1}")
            st.write(question["question"])
            user_answer = st.radio("Select an answer:", question["options"], key=f"static_q{st.session_state.static_quiz_index}")
            
            if st.button("Submit Answer"):
                st.session_state.static_user_answers[st.session_state.static_quiz_index] = user_answer
                if user_answer == question["answer"]:
                    st.session_state.static_quiz_score += 1
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The answer is: {question['answer']}")
                st.write(f"Explanation: {question['explanation']}")
                st.session_state.static_quiz_index += 1
                st.button("Next Question")
        else:
            st.subheader("Static Quiz Completed!")
            st.write(f"Your Score: {st.session_state.static_quiz_score}/{len(st.session_state.static_quiz_questions)}")
            percentage = (st.session_state.static_quiz_score / len(st.session_state.static_quiz_questions)) * 100
            st.write(f"Percentage: {percentage:.2f}%")
            if percentage >= 80:
                st.balloons()
                st.write("Great job! You're ready for the exam!")
            else:
                st.write("Keep practicing with flashcards and try the LLM Quiz!")
            if st.button("Restart Static Quiz"):
                st.session_state.static_quiz_score = 0
                st.session_state.static_quiz_index = 0
                st.session_state.static_user_answers = [None] * len(st.session_state.static_quiz_questions)
                st.session_state.static_quiz_questions = random.sample(static_quiz_questions, len(static_quiz_questions))

    elif page == "LLM Quiz":
        st.header("LLM-Generated Quiz")
        st.markdown("Test your knowledge with 15–20 dynamic questions generated by an AI model. Questions vary each time!")

        if "llm_quiz_score" not in st.session_state:
            st.session_state.llm_quiz_score = 0
            st.session_state.llm_quiz_index = 0
            st.session_state.llm_quiz_questions = []
            st.session_state.llm_user_answers = []

        # Fetch LLM questions if not already generated
        if not st.session_state.llm_quiz_questions:
            try:
                st.session_state.llm_quiz_questions = generate_llm_questions()
                st.session_state.llm_user_answers = [None] * len(st.session_state.llm_quiz_questions)
                if not st.session_state.llm_quiz_questions:
                    st.warning("LLM failed to generate questions. Using static questions as fallback.")
                    st.session_state.llm_quiz_questions = random.sample(static_quiz_questions, min(15, len(static_quiz_questions)))
                    st.session_state.llm_user_answers = [None] * len(st.session_state.llm_quiz_questions)
            except Exception as e:
                st.error(f"Error fetching LLM questions: {str(e)}. Using static questions.")
                st.session_state.llm_quiz_questions = random.sample(static_quiz_questions, min(15, len(static_quiz_questions)))
                st.session_state.llm_user_answers = [None] * len(st.session_state.llm_quiz_questions)

        if st.session_state.llm_quiz_index < len(st.session_state.llm_quiz_questions):
            question = st.session_state.llm_quiz_questions[st.session_state.llm_quiz_index]
            st.subheader(f"Question {st.session_state.llm_quiz_index + 1}")
            st.write(question["question"])
            user_answer = st.radio("Select an answer:", question["options"], key=f"llm_q{st.session_state.llm_quiz_index}")
            
            if st.button("Submit Answer"):
                st.session_state.llm_user_answers[st.session_state.llm_quiz_index] = user_answer
                if user_answer == question["answer"]:
                    st.session_state.llm_quiz_score += 1
                    st.success("Correct!")
                else:
                    st.error(f"Incorrect. The answer is: {question['answer']}")
                st.write(f"Explanation: {question['explanation']}")
                st.session_state.llm_quiz_index += 1
                st.button("Next Question")
        else:
            st.subheader("LLM Quiz Completed!")
            st.write(f"Your Score: {st.session_state.llm_quiz_score}/{len(st.session_state.llm_quiz_questions)}")
            percentage = (st.session_state.llm_quiz_score / len(st.session_state.llm_quiz_questions)) * 100
            st.write(f"Percentage: {percentage:.2f}%")
            if percentage >= 80:
                st.balloons()
                st.write("Great job! You're ready for the exam!")
            else:
                st.write("Keep practicing with flashcards and try again!")
            if st.button("Restart LLM Quiz"):
                st.session_state.llm_quiz_score = 0
                st.session_state.llm_quiz_index = 0
                st.session_state.llm_quiz_questions = []
                st.session_state.llm_user_answers = []

if __name__ == "__main__":
    main()

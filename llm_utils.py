import json
import streamlit as st
import logging
from euriai import EuriaiClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_llm_questions():
    """
    Generate 15–20 quiz questions using the EuriaiClient SDK with gpt-4.1-nano.
    Returns a list of question dictionaries with question, options, answer, and explanation.
    """
    # Load API key from Streamlit secrets
    try:
        api_key = st.secrets["EURIAI_API_KEY"]
    except KeyError:
        logger.error("EURIAI_API_KEY not found in Streamlit secrets.")
        return []

    # Initialize EuriaiClient
    try:
        client = EuriaiClient(api_key=api_key, model="gpt-4.1-nano")
    except Exception as e:
        logger.error(f"Failed to initialize EuriaiClient: {str(e)}")
        return []

    # LLM Prompt
    prompt = """
    You are an expert in AWS and the AWS Certified Cloud Practitioner exam. Generate 15–20 multiple-choice questions (10 knowledge-based, 5–10 scenario-based) about the AWS Cloud Adoption Framework (CAF) and AWS Well-Architected Framework (WAF). Ensure variability in wording, scenarios (e.g., healthcare, gaming, education industries), and difficulty, but keep questions high-level, suitable for the Cloud Practitioner exam. Use the following context to align with the exam's focus:

    **AWS CAF**:
    - Metaphor: City planning for cloud adoption.
    - Six perspectives: Business (Mayor’s office, CEO/CFO, strategy, innovation), People (HR, training, cloud fluency), Governance (city council, risk/cost management), Platform (engineering, cloud-native, CI/CD), Security (police, IAM, threat detection), Operations (maintenance, observability, incident management).
    - Four phases: Envision (set goals), Align (plan readiness), Launch (pilot projects), Scale (full migration).
    - Case study: ShopEasy (retailer migrates e-commerce to AWS, uses Redshift for analytics, Cost Explorer for budgeting, IAM for security).

    **AWS WAF**:
    - Metaphor: Building a dream house for cloud workloads.
    - Six pillars: Operational Excellence (project manager, automation, CloudFormation), Security (alarms, IAM/KMS, encryption), Reliability (foundation, Auto Scaling, recovery), Performance Efficiency (plumbing, Lambda, CloudFront), Cost Optimization (budget, Cost Explorer, pay-as-you-go), Sustainability (eco-design, serverless, green regions).
    - Tool: Well-Architected Tool (checks best practices, integrates with Trusted Advisor).
    - Case study: PayFast (FinTech builds payment platform, uses KMS for compliance, Auto Scaling for reliability, CloudFront for performance).

    For each question, provide:
    - Question text (clear, varied, exam-relevant, avoiding overly technical details).
    - Four multiple-choice options (one correct, three plausible distractors).
    - Correct answer (matching one of the options).
    - Explanation (1–2 sentences, referencing metaphors or case studies if relevant).

    Format the output as a JSON array of objects, each with keys: question, options, answer, explanation. Ensure the JSON is valid and parseable. Example:
    [
        {
            "question": "What is the purpose of the CAF Business Perspective?",
            "options": ["Train employees", "Align cloud with business goals", "Protect data", "Build infrastructure"],
            "answer": "Align cloud with business goals",
            "explanation": "The Business Perspective, like the mayor’s office, ensures cloud adoption drives business outcomes like revenue growth."
        },
        {
            "question": "A gaming company migrates to AWS. Which WAF pillar ensures low-latency gameplay?",
            "options": ["Security", "Reliability", "Performance Efficiency", "Cost Optimization"],
            "answer": "Performance Efficiency",
            "explanation": "Performance Efficiency, like a house’s plumbing, optimizes resources for speed, using services like CloudFront."
        }
    ]

    Avoid duplicating questions or using overly similar wording. Ensure scenarios cover diverse industries and use cases.
    """

    try:
        response = client.generate_completion(
            prompt=prompt,
            temperature=0.7,
            max_tokens=4000
        )
        # Log response for debugging
        logger.info(f"Raw LLM response type: {type(response)}, content: {response}")

        # Handle dictionary response
        if isinstance(response, dict):
            # Try common field names for the response text
            possible_fields = ["text", "content", "response", "completion"]
            response_text = None
            for field in possible_fields:
                if field in response:
                    response_text = response[field]
                    break
            if response_text is None:
                logger.error(f"Could not find a valid text field in response: {response.keys()}")
                return []
            if not isinstance(response_text, str):
                logger.error(f"Response text is not a string: {type(response_text)}")
                return []
        elif isinstance(response, str):
            response_text = response
        else:
            logger.error(f"Unexpected response format: {type(response)}")
            return []

        # Parse JSON from response_text
        try:
            questions = json.loads(response_text)
            # Validate questions
            valid_questions = [
                q for q in questions
                if isinstance(q, dict) and
                all(key in q for key in ["question", "options", "answer", "explanation"]) and
                isinstance(q["options"], list) and len(q["options"]) == 4 and
                q["answer"] in q["options"]
            ]
            if len(valid_questions) < 15:
                logger.warning(f"LLM returned only {len(valid_questions)} valid questions. Expected 15–20.")
            return valid_questions[:20]  # Cap at 20
        except json.JSONDecodeError:
            logger.error(f"Failed to parse LLM response as JSON: {response_text}")
            return []
    except Exception as e:
        logger.error(f"EuriaiClient request failed: {str(e)}")
        return []

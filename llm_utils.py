import requests
import json
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_llm_questions():
    """
    Generate 15–20 quiz questions using an LLM API.
    Returns a list of question dictionaries with question, options, answer, and explanation.
    """
    # Load API key from Streamlit secrets or environment
    try:
        api_key = st.secrets["LLM_API_KEY"]
    except KeyError:
        logger.error("LLM_API_KEY not found in Streamlit secrets.")
        return []

    # API configuration (assumed REST API, e.g., Gemini or OpenAI)
    api_endpoint = "https://api.euron.one/api/v1/euri/alpha/chat/completions"  # Replace with actual endpoint
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # LLM Prompt
    prompt = """
    You are an expert in AWS and the AWS Certified Cloud Practitioner exam. Generate 15–20 multiple-choice questions (10 knowledge-based, 5–10 scenario-based) about the AWS Cloud Adoption Framework (CAF) and AWS Well-Architected Framework (WAF). Ensure variability in wording, scenarios, and difficulty, but keep questions high-level, suitable for the Cloud Practitioner exam. Use the following context:

    **AWS CAF**:
    - Metaphor: City planning for cloud adoption.
    - Six perspectives: Business (Mayor’s office, CEO/CFO, strategy), People (HR, training, cloud fluency), Governance (city council, risk/cost management), Platform (engineering, cloud-native), Security (police, IAM), Operations (maintenance, observability).
    - Four phases: Envision (set goals), Align (plan readiness), Launch (pilot projects), Scale (full migration).
    - Case study: ShopEasy (retailer migrates e-commerce to AWS, uses Redshift, Cost Explorer, IAM).

    **AWS WAF**:
    - Metaphor: Building a dream house for cloud workloads.
    - Six pillars: Operational Excellence (project manager, automation), Security (alarms, IAM/KMS), Reliability (foundation, Auto Scaling), Performance Efficiency (plumbing, Lambda), Cost Optimization (budget, Cost Explorer), Sustainability (eco-design, serverless).
    - Tool: Well-Architected Tool (checks best practices).
    - Case study: PayFast (FinTech builds payment platform, uses KMS, Auto Scaling, CloudFront).

    For each question, provide:
    - Question text (clear, varied, exam-relevant).
    - Four multiple-choice options.
    - Correct answer.
    - Explanation (1–2 sentences, referencing metaphors or case studies if relevant).

    Format the output as a JSON array of objects, each with keys: question, options, answer, explanation.
    Example:
    [
        {
            "question": "What is the purpose of the CAF Business Perspective?",
            "options": ["Train employees", "Align cloud with business goals", "Protect data", "Build infrastructure"],
            "answer": "Align cloud with business goals",
            "explanation": "The Business Perspective, like the mayor’s office, ensures cloud adoption drives business outcomes."
        }
    ]
    """

    payload = {
        "prompt": prompt,
        "max_tokens": 4000,
        "temperature": 0.7,
        "n": 1
    }

    try:
        response = requests.post(api_endpoint, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Extract questions from response (adjust based on actual API response structure)
        if "choices" in data and len(data["choices"]) > 0:
            questions_text = data["choices"][0]["text"].strip()
            try:
                questions = json.loads(questions_text)
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
                logger.error("Failed to parse LLM response as JSON.")
                return []
        else:
            logger.error("No valid choices in LLM response.")
            return []
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in LLM call: {str(e)}")
        return []

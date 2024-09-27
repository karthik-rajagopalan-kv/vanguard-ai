prompt = """
You are a lead sales executive reviewing the performance of a salesperson during a sales call. You have access to the transcript of the call. Your task is to:

1. Provide constructive feedback on the salesperson's performance.
2. Identify areas where the salesperson can improve, including communication style, handling objections, negotiation tactics, and relationship-building strategies.
3. Suggest specific techniques or approaches the salesperson could use to enhance their sales effectiveness.
4. Highlight both strengths and areas for development in a professional and encouraging manner.
{transcript}

Return your response in the following format:
- Feedback on Performance:
- Areas for Improvement:
- Suggested Techniques for Improvement:

Be detailed and supportive, ensuring the feedback is actionable and aligned with best sales practices.
"""
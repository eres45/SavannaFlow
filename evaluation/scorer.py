import os
from dotenv import load_dotenv
from groq import Groq
# from evaluate import load  <-- Moved inside class to avoid crashes
import pandas as pd

load_dotenv()

class RAGScorer:
    def __init__(self, model_name=None):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = model_name or "llama-3.3-70b-versatile"
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        
        # Load BERTScore evaluator only if needed
        try:
            from evaluate import load
            self.bertscore = load("bertscore")
        except:
            print("Warning: BERTScore failed to load. This is normal in production.")
            self.bertscore = None

    def llm_judge(self, question, answer, context):
        """
        Uses an LLM to grade the answer as PASS/FAIL based on the retrieved context.
        """
        prompt = f"""
        Role: Aerospace Accuracy Judge
        Task: Grade the AI's answer based on the retrieved context for the given question.
        
        Question: {question}
        Retrieved Context: {context}
        AI Answer: {answer}
        
        Criteria:
        - PASS: The answer is factually correct. If it combines Graph Context with general knowledge to provide a better answer, that is a STRENGTH, not a failure.
        - PASS: High scores (95-100) should be given if all specific numbers and names match the context.
        - FAIL: Only give a low score if there is a direct factual contradiction.
        
        Output only a single number between 0 and 100 representing the percentage accuracy and factual alignment.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.1
            )
            score_str = chat_completion.choices[0].message.content.strip()
            # Extract just the number in case the LLM added text
            import re
            match = re.search(r'\d+', score_str)
            if match:
                return int(match.group())
            return 0
        except Exception as e:
            return f"ERROR: {str(e)}"

    def calculate_bertscore(self, answers, references):
        """
        Calculates BERTScore for a list of answers and references.
        """
        if not self.bertscore:
            return None
        
        results = self.bertscore.compute(
            predictions=answers, 
            references=references, 
            lang="en",
            model_type="distilbert-base-uncased" # Lightweight model for speed
        )
        return results

    def evaluate_pipeline(self, question, answer, reference):
        """
        Full evaluation: LLM Judge + BERTScore.
        """
        judge_score = self.llm_judge(question, answer, reference)
        
        # Calculate BERTScore if possible
        bert_result = "N/A"
        if self.bertscore and answer and reference:
            try:
                results = self.calculate_bertscore([answer], [reference])
                # Taking the F1 score as the primary metric
                f1 = results["f1"][0]
                bert_result = f"{f1:.4f}"
            except:
                pass
        
        return {
            "judge": judge_score,
            "bertscore": bert_result
        }

if __name__ == "__main__":
    scorer = RAGScorer()
    q = "Who founded SpaceX?"
    a = "Elon Musk founded SpaceX in 2002."
    r = "Elon Musk is the founder of SpaceX."
    print(f"Evaluation: {scorer.evaluate_pipeline(q, a, r)}")

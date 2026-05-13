import os
from dotenv import load_dotenv
from groq import Groq
from evaluate import load
import pandas as pd

load_dotenv()

class RAGScorer:
    def __init__(self, model_name=None):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = model_name or "llama-3.3-70b-versatile"
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        
        # Load BERTScore evaluator
        try:
            self.bertscore = load("bertscore")
        except:
            print("Warning: BERTScore failed to load. Ensure 'bert-score' and 'evaluate' are installed.")
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
        - PASS: The answer is factually supported by the context and accurately answers the question.
        - PASS: If the answer is more detailed than the context but remains factually correct based on common knowledge (as long as it doesn't contradict the context).
        - FAIL: The answer directly contradicts the context or provides a wrong number/date.
        - FAIL: The answer says "I don't know" when the answer is clearly in the context.
        
        Output only "PASS" or "FAIL".
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.1
            )
            return chat_completion.choices[0].message.content.strip().upper()
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

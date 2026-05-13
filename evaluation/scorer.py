import os
from dotenv import load_dotenv
from groq import Groq
from evaluate import load
import pandas as pd

load_dotenv()

class RAGScorer:
    def __init__(self, model_name=None):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = model_name or os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        
        # Load BERTScore evaluator
        try:
            self.bertscore = load("bertscore")
        except:
            print("Warning: BERTScore failed to load. Ensure 'bert-score' and 'evaluate' are installed.")
            self.bertscore = None

    def llm_judge(self, question, answer, reference):
        """
        Uses an LLM to grade the answer as PASS/FAIL based on a reference.
        """
        prompt = f"""
        Role: Accuracy Judge
        Task: Grade the AI's answer against the reference answer for the given question.
        
        Question: {question}
        Reference Answer: {reference}
        AI Answer: {answer}
        
        Criteria:
        - The AI answer must be factually consistent with the reference.
        - It must directly answer the question.
        - Minor stylistic differences are allowed.
        
        Output only "PASS" or "FAIL".
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
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

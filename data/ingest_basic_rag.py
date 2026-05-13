import os
from pipelines.basic_rag import BasicRAGPipeline
from dotenv import load_dotenv

load_dotenv()

def main():
    data_file = "data/raw/space_data.txt"
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found.")
        return

    pipeline = BasicRAGPipeline()
    pipeline.ingest(data_file)
    print("Basic RAG Ingestion Successful.")

if __name__ == "__main__":
    main()

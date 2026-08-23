from rag.pipeline import RAGPipeline

def main():
    print("=" * 60)
    print("SECOND BRAIN AI")
    print("AI SEARCH / RAG ASSISTANT (CLI)")
    print("=" * 60)

    try:
        pipeline = RAGPipeline()
    except Exception as error:
        print("\nInitialization Error:")
        print(error)
        return

    while True:
        try:
            question = input("\nAsk a question (type 'exit' to quit):\n> ")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Second Brain AI...")
            break

        if question.lower().strip() == "exit":
            print("\nExiting Second Brain AI...")
            break

        if not question.strip():
            print("Please enter a question.")
            continue

        try:
            result = pipeline.ask(question)

            print("\n" + "-" * 60)
            print("AI ANSWER:")
            print(result["answer"])

            print("\nSOURCES:")
            if result["sources"]:
                for source in result["sources"]:
                    print(f"- {source}")
            else:
                print("No source found.")
            print("-" * 60)
        except Exception as error:
            print("\nError generating response:")
            print(error)

if __name__ == "__main__":
    main()


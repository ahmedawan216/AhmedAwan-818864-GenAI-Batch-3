from crew import create_crew

def main():
    topic=input(
        "\nEnter your research topic please:"
    )
    crew=create_crew(topic)
    result=crew.kickoff()
    
    print("\n")
    print(result)

if __name__ == '__main__':
    main()
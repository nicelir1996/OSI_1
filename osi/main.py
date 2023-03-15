from osi.src.Validator import Validator
from osi.src.Worker import Worker
from osi.src.Orchestrator import Orchestrator

def main(research_topic):
    # Initialize OpenAICaller, WebScraper, and Validator instances
    validator = Validator()

    # Initialize Workers with the OpenAICaller and WebScraper instances
    workers = [Worker() for _ in range(3)]

    # Initialize the Orchestrator with the Workers
    orchestrator = Orchestrator(workers)

    # Perform the research and obtain the final report
    final_report = orchestrator.perform_research(research_topic)

    # Print the final report
    print(final_report)

if __name__ == "__main__":
    research_topic = "Renewable energy sources"
    main(research_topic)

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SeniorSoftwerDeveloperForCreateAndTestingAndWritingCode():
    """SeniorSoftwerDeveloperForCreateAndTestingAndWritingCode crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def product_owner(self) -> Agent:
        return Agent(
            config=self.agents_config['product_owner'], # type: ignore[index]
            verbose=True
        )

    @agent
    def software_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['software_architect'], # type: ignore[index]
            verbose=True
        )

    @agent
    def senior_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_developer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def security_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_engineer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def qa_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def devops_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['devops_engineer'], # type: ignore[index]
            verbose=True
        )

    @agent
    def maintenance_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['maintenance_engineer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def requirements_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirements_task'], # type: ignore[index]
        )

    @task
    def architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['architecture_task'], # type: ignore[index]
        )

    @task
    def implementation_task(self) -> Task:
        return Task(
            config=self.tasks_config['implementation_task'], # type: ignore[index]
        )

    @task
    def security_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_task'], # type: ignore[index]
        )

    @task
    def testing_task(self) -> Task:
        return Task(
            config=self.tasks_config['testing_task'], # type: ignore[index]
        )

    @task
    def deployment_task(self) -> Task:
        return Task(
            config=self.tasks_config['deployment_task'], # type: ignore[index]
        )

    @task
    def maintenance_task(self) -> Task:
        return Task(
            config=self.tasks_config['maintenance_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SeniorSoftwerDeveloperForCreateAndTestingAndWritingCode crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

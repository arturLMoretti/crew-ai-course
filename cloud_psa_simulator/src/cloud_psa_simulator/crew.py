from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileWriterTool, DirectoryReadTool
import os

@CrewBase
class CloudPsaSimulator():
    """CloudPsaSimulator crew for pressure swing adsorption modeling and simulation"""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def _get_base_dir(self) -> str:
        code_output = self.agents_config.get('code_output', {})
        base_dir = code_output.get('base_dir', '~/Desktop/cloud_psa_simulator_files')
        return os.path.expanduser(base_dir)

    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config['manager'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def data_scientist(self) -> Agent:
        return Agent(
            config=self.agents_config['data_scientist'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def simulation_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['simulation_engineer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def process_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['process_engineer'],  # type: ignore[index]
            tools=[DirectoryReadTool()],
            verbose=True
        )

    @agent
    def python_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['python_developer'],  # type: ignore[index]
            tools=[FileWriterTool(), DirectoryReadTool()],
            verbose=True
        )

    @agent
    def documentation_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['documentation_writer'],  # type: ignore[index]
            tools=[FileWriterTool(), DirectoryReadTool()],
            verbose=True
        )

    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],  # type: ignore[index]
            tools=[FileWriterTool(), DirectoryReadTool()],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],  # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],  # type: ignore[index]
        )

    @task
    def data_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_analysis_task'],  # type: ignore[index]
        )

    @task
    def simulation_task(self) -> Task:
        return Task(
            config=self.tasks_config['simulation_task'],  # type: ignore[index]
        )

    @task
    def process_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['process_optimization_task'],  # type: ignore[index]
        )

    @task
    def project_management_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_management_task'],  # type: ignore[index]
        )

    @task
    def implementation_task(self) -> Task:
        base_dir = self._get_base_dir()
        return Task(
            config=self.tasks_config['implementation_task'],  # type: ignore[index]
            agent=self.python_developer(),
        )

    @task
    def documentation_task(self) -> Task:
        base_dir = self._get_base_dir()
        return Task(
            config=self.tasks_config['documentation_task'],  # type: ignore[index]
            agent=self.documentation_writer(),
        )

    @task
    def validation_task(self) -> Task:
        base_dir = self._get_base_dir()
        return Task(
            config=self.tasks_config['validation_task'],  # type: ignore[index]
            agent=self.test_engineer(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CloudPsaSimulator crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

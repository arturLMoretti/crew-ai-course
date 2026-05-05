#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from cloud_psa_simulator.crew import CloudPsaSimulator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    import yaml
    import os

    config_path = os.path.join(os.path.dirname(__file__), 'config/agents.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    code_output = config.get('code_output', {})
    base_dir = os.path.expanduser(code_output.get('base_dir', '~/Desktop/cloud_psa_simulator_files'))

    inputs = {
        'current_year': str(datetime.now().year),
        'base_dir': base_dir
    }

    try:
        CloudPsaSimulator().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'current_year': str(datetime.now().year)
    }
    try:
        CloudPsaSimulator().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CloudPsaSimulator().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "current_year": str(datetime.now().year)
    }

    try:
        CloudPsaSimulator().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "current_year": str(datetime.now().year)
    }

    try:
        result = CloudPsaSimulator().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")


if __name__ == "__main__":
    run()
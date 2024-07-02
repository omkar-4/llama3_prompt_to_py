import argparse, subprocess, re, os
from langchain_community.llms import Ollama

llm = Ollama(model="gurubot/llama3-alpha-centauri-uncensored:latest")

prompt = """Write a Python script that prints hello world. includr the code inside (``` #code ```) backticks"""

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(file_path, 'w') as file:
        file.write(content)

def extract_python_code(response):
    code_pattern = re.compile(r"```(?:python\s*)?(.*?)```", re.DOTALL)
    match = code_pattern.search(response)
    if match:
        return match.group(1).strip()
    else:
        return response.strip()

def execute_script(script_path):
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    return result.stdout

def main():
    # Define default paths for script and result files
    output_script = "gen_script.py"
    output_result = "gen_result.txt"

    response = llm.invoke(prompt)
    python_code = extract_python_code(response)

    # Review the generated code
    print("Generated Python Code:\n")
    print(python_code)

    # After reviewing, save the code to a file
    write_file(output_script, python_code)

    # Execute the script
    execution_result = execute_script(output_script)
    write_file(output_result, execution_result)
    print(f"\nExecution result written to {output_result}")

if __name__ == "__main__":
    main()
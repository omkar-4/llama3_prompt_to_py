import argparse, subprocess, re
from langchain_community.llms import Ollama

llm = Ollama(model="gurubot/llama3-alpha-centauri-uncensored:latest")

prompt = """Write a Python script that prints hello world. includr the code inside (``` #code ```) backticks"""

# read and write to file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# extract python code
def extract_python_code(response):
    code_pattern = re.compile(r"```(?:python\s*)?(.*?)```", re.DOTALL)
    match = code_pattern.search(response)
    if match:
        return match.group(1).strip()
    else:
        return response.strip()

# execute script
def execute_script(script_path):
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    return result.stdout

def main(output_script, output_result):
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
    parser = argparse.ArgumentParser(description='LLM Script Generator and Executor')
    parser.add_argument('--script', type=str, required=True, help='Path to save the generated script')
    parser.add_argument('--output', type=str, required=True, help='Path to save the execution result')
    args = parser.parse_args()

    main(args.script, args.output)
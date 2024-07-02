from langchain_community.llms import Ollama
import argparse

llm = Ollama(model="gurubot/llama3-alpha-centauri-uncensored:latest")

prompt = """
hello, can you tell me what kind of stuffs i have to do today?
"""

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# test_input = "i wanna talk to you"

# readfile = read_file("todo.md")

# response = llm(prompt + "\n\n" + test_input)
# response = llm(prompt + "\n\n" + readfile)

# def main(file_path):
def main(input_file, output_file):
        # read_data = read_file(file_path)
        read_data = read_file(input_file)
        response = llm.invoke(prompt + "\n\n" + read_data)
        # Execute the prompt using streaming method
        # write_file(output_file, response)
        write_file(output_file, response)
        # for chunks in llm.stream(response):
        #     print(chunks, end="")
        print(f"output written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LLM Assistant')
    # parser.add_argument('--file',type=str,required=True,help='Path to the File')
    parser.add_argument('--input', type=str, required=True, help='Path to the transactions file')
    parser.add_argument('--output', type=str, required=True, help='Path to the output file')
    args = parser.parse_args()

    #  main(args.file)
    main(args.input, args.output)
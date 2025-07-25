<div align="center">

<img src="https://github.com/user-attachments/assets/1f9ce2d7-8f9d-4746-bad4-acfccad74900" alt="ffufai_logo" width="400">

# `ffufai`

![GitHub top language](https://img.shields.io/github/languages/top/jthack/ffufai)
![GitHub last commit](https://img.shields.io/github/last-commit/jthack/ffufai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

<p class="align center">

ffufai is an AI-powered wrapper for the popular web fuzzer ffuf. It automatically suggests file extensions for fuzzing based on the target URL and its headers, using either OpenAI's GPT, Anthropic's Claude, or a local Ollama model.

</p>

</div>

## Features
<img width="600  " alt="image" src="https://github.com/user-attachments/assets/0384d4f0-3a07-48d9-9805-ea1e76b6b693">

- Seamlessly integrates with ffuf
- Automatically suggests relevant file extensions for fuzzing
- Supports OpenAI, Anthropic, and local Ollama AI models
- Passes through all ffuf parameters

## Prerequisites

- Python 3.6+
- ffuf (installed and accessible in your PATH)
- An OpenAI API key, Anthropic API key, or a running Ollama instance.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/jthack/ffufai
   cd ffufai
   ```

2. Install the required Python packages:
   ```
   pip install requests openai anthropic
   ```

3. Make the script executable:
   ```
   chmod +x ffufai.py
   ```

4. (Optional) To use ffufai from anywhere, you can create a symbolic link in a directory that's in your PATH. For example:
   ```
   sudo ln -s /full/path/to/ffufai.py /usr/local/bin/ffufai
   ```
   Replace "/full/path/to/ffufai.py" with the actual full path to where you cloned the repository.

5. Set up your LLM provider as an environment variable:
   For Ollama (recommended):
   ```
   export OLLAMA_MODEL='your-model-name' # e.g., 'llama3'
   ```
   For OpenAI:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```
   Or for Anthropic:
   ```
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

   You can add these lines to your `~/.bashrc` or `~/.zshrc` file to make them permanent.

## Usage

Use ffufai just like you would use ffuf, but replace `ffuf` with `python3 ffufai.py` (or just `ffufai` if you've created the symbolic link):

```
python3 ffufai.py -u https://example.com/FUZZ -w /path/to/wordlist.txt
```

Or if you've created the symbolic link:

```
ffufai -u https://example.com/FUZZ -w /path/to/wordlist.txt
```

ffufai will automatically suggest extensions based on the URL and add them to the ffuf command.

## Parameters

ffufai accepts all the parameters that ffuf does, plus a few additional ones:

- `--ffuf-path`: Specifies the path to the ffuf executable. Default is 'ffuf'.  
  Example: `ffufai --ffuf-path /usr/local/bin/ffuf -u https://example.com/FUZZ -w wordlist.txt`

- `--max-extensions`: Sets the maximum number of extensions to suggest. Default is 4.  
  Example: `ffufai --max-extensions 6 -u https://example.com/FUZZ -w wordlist.txt`

- `-u`: Specifies the target URL. This parameter is required and should include the FUZZ keyword.  
  Example: `ffufai -u https://example.com/FUZZ -w wordlist.txt`

- `-w`: Specifies the wordlist to use for fuzzing. This is a standard ffuf parameter.  
  Example: `ffufai -u https://example.com/FUZZ -w /path/to/wordlist.txt`

All other ffuf parameters can be used as normal. For a full list of ffuf parameters, refer to the ffuf documentation.

## Notes

- ffufai requires the FUZZ keyword to be at the end of the URL path for accurate extension suggestion. It will warn you if this is not the case.
- All ffuf parameters are passed through to ffuf, so you can use any ffuf option with ffufai.
- ffufai will prioritize LLM providers in the following order: Ollama, Anthropic, OpenAI. If `OLLAMA_MODEL` is set, it will be used. If not, it will check for `ANTHROPIC_API_KEY`, and finally `OPENAI_API_KEY`.

HUGE Shoutout to zlz, aka Sam Curry, for the amazing idea to make this project. He suggested it and 2 hours later, here it is :)    
<img width="744" alt="image" src="https://github.com/user-attachments/assets/9f914cc4-fe5f-4dbc-b7d9-548473ea2134">

## Troubleshooting

- If you encounter a "command not found" error, make sure you're using `python3 ffufai.py` or that you've correctly set up the symbolic link.
- If you get an API key error, ensure you've correctly set up your `OLLAMA_MODEL`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY` environment variable.
- If you see "import: command not found" errors, it means the script is being interpreted by the shell instead of Python. Make sure you're running it with `python3 ffufai.py` or that the shebang line at the top of the script is correct.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

#!/usr/bin/env python3

import argparse
import os
import subprocess
import requests
import json
from openai import OpenAI
import anthropic
from urllib.parse import urlparse

def get_llm_provider():
    if os.getenv('OLLAMA_MODEL'):
        return ('ollama', os.getenv('OLLAMA_MODEL'))
    
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    if anthropic_key:
        return ('anthropic', anthropic_key)
    elif openai_key:
        return ('openai', openai_key)
    else:
        raise ValueError("No API key or Ollama model found. Please set OLLAMA_MODEL, OPENAI_API_KEY, or ANTHROPIC_API_KEY.")

def get_headers(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return dict(response.headers)
    except requests.RequestException as e:
        print(f"Error fetching headers: {e}")
        return {"Header": "Error fetching headers."}

def get_ai_extensions(url, headers, provider, model_or_key, max_extensions):
    prompt = f"""
    Given the following URL and HTTP headers, suggest the most likely file extensions for fuzzing this endpoint.
    Respond with a JSON object containing a list of extensions. The response will be parsed with json.loads(),
    so it must be valid JSON. No preamble or yapping. Use the format: {{"extensions": [".ext1", ".ext2", ...]}}.
    Do not suggest more than {max_extensions}, but only suggest extensions that make sense. For example, if the path is 
    /js/ then don't suggest .css as the extension. Also, if limited, prefer the extensions which are more interesting.
    The URL path is great to look at for ideas. For example, if it says presentations, then it's likely there 
    are powerpoints or pdfs in there. If the path is /js/ then it's good to use js as an extension.

    Examples:
    1. URL: https://example.com/presentations/FUZZ
       Headers: {{"Content-Type": "application/pdf", "Content-Length": "1234567"}}
       JSON Response: {{"extensions": [".pdf", ".ppt", ".pptx"]}}

    2. URL: https://example.com/FUZZ
       Headers: {{"Server": "Microsoft-IIS/10.0", "X-Powered-By": "ASP.NET"}}
       JSON Response: {{"extensions": [".aspx", ".asp", ".exe", ".dll"]}}

    URL: {url}
    Headers: {headers}

    JSON Response:
    """

    if provider == 'openai':
        client = OpenAI(api_key=model_or_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that suggests file extensions for fuzzing based on URL and headers."},
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(response.choices[0].message.content.strip())
    elif provider == 'anthropic':
        client = anthropic.Anthropic(api_key=model_or_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0,
            system="You are a helpful assistant that suggests file extensions for fuzzing based on URL and headers.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(message.content[0].text)
    elif provider == 'ollama':
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model_or_key,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                }
            )
            response.raise_for_status()
            # The output from ollama is a json object, with a response key which is a string of json.
            return json.loads(json.loads(response.text)['response'])
        except requests.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='ffufai - AI-powered ffuf wrapper')
    parser.add_argument('--ffuf-path', default='ffuf', help='Path to ffuf executable')
    parser.add_argument('--max-extensions', type=int, default=4, help='Maximum number of extensions to suggest')
    args, unknown = parser.parse_known_args()

    # Find the -u argument in the unknown args
    try:
        url_index = unknown.index('-u') + 1
        url = unknown[url_index]
    except (ValueError, IndexError):
        print("Error: -u URL argument is required.")
        return

    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')

    if 'FUZZ' not in path_parts[-1]:
        print("Warning: FUZZ keyword is not at the end of the URL path. Extension fuzzing may not work as expected.")

    base_url = url.replace('FUZZ', '')
    headers = get_headers(base_url)

    provider, model_or_key = get_llm_provider()
    try:
        extensions_data = get_ai_extensions(url, headers, provider, model_or_key, args.max_extensions)
        if extensions_data is None:
            return
        
        print(extensions_data)
        extensions = ','.join(extensions_data['extensions'][:args.max_extensions])
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing AI response. Try again. Error: {e}")
        return

    ffuf_command = [args.ffuf_path] + unknown + ['-e', extensions]

    subprocess.run(ffuf_command)

if __name__ == '__main__':
    main()

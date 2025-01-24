import base64
import requests

def encode_image(image_path: str) -> str:
    '''
    Encode an image as a base64 string

    Parameters:
    - image_path: path to the image file

    Returns:
    - base64 encoded string
    '''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def to_markdown(image_path: str, markdown: str, magazine_name: str, api_key: str) -> dict:
    '''
    Use the OpenAI API to convert an image to markdown

    Parameters:
    - image_path: path to the image file
    - markdown: initial markdown to improve
    - magazine_name: name of the magazine
    - api_key: OpenAI API key

    Returns:
    - response from the OpenAI API
    '''
    # Encode the image
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f'''
                        I attach a scan of a page from the magazine {magazine_name} that I'd like converted to markdown.
                        I've also attached some markdown from an initial OCR scan, but I'd like you to improve it based on what you see in the image. 

                        Please pay particular attention to table formatting - the markdown I've provided likely gets tables wrong - please check carefully against the image.
                        Pages may begin with the name of the magazine - I do not want you to include this in the markdown as I will be rendering the document with a title at the top of the page.
                        Please be conistent with sectioning - new sections are often preceded by a double horizontal line in the image, everthing else should be a subsection.
                        USE title case for all section headings and subheadings - ie. first letter capitalised of each word.

                        DO NOT modify any images elements in the markdown I've provided, I want these kept as is.
                        
                        Do not return anything else in your response except the markdown code 
                        {markdown}
                        '''
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    return response.json()

def img_extract_front_matter(image_path: str, api_key: str) -> dict:
    '''
    Use the OpenAI API to extract front matter from a magazine cover

    Parameters:
    - image_path: path to the image file
    - api_key: OpenAI API key

    Returns:
    - dictionary of extracted front matter
    '''

    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f'''
                         Here is the front page of a magazine.  I'd like you to extract the following information from the image:
                            - The title of the magazine - use title case (e.g. "The New York Times")
                            - The date of the issue in the format YYYY-MM-DD
                            - The volume number as an integer (convert any roman numerals to integers)
                            - The issue number as an integer (convert any roman numerals to integers)
                            - The price of the magazine as a string (e.g. "$5.99") 
                            - The location of the magazine

                        Please return this information in a python dict, with the keys 'title', 'date', 'volume', 'issue', 'price', 'location'.
                        Do not return anything else in your response except the python dict.
                        '''
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    resp = response.json()['choices'][0]['message']['content']
    # remove python backticks
    resp = resp.replace('```python', '')
    resp = resp.replace('```', '')
    return eval(resp)

import requests
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer
import keys
import matplotlib.pyplot as plt



def text_extractor():

    html = """
    <html>
    <head>
    <style>
    p {
        color: red;
        font-size: 20px;
    }
    </style>
    </head>
    <body>
    <p>This is a <span style="color: blue;">paragraph</span> with inline CSS.</p>
    </body>
    </html>
    """

    with open('sample.txt', 'r') as f:
        data = f.read()

    soup = BeautifulSoup(data, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)

    return(text)



def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            with open('./data/data.txt', 'w', encoding='utf-8') as f:
                f.write(text)

            return text
        else:
            return "Failed to fetch the webpage, status code: {}".format(response.status_code)
    except Exception as e:
        return "An error occurred: {}".format(str(e))
    

def classify_text(text):
    API_URL = keys.INF
    headers = {"Authorization": f"Bearer {keys.KEY}"}

    # def query(payload):
    #     response = requests.post(API_URL, headers=headers, json=payload)
    #     return response.json()
        
    # output = query({
    #     "inputs": text,
    # })

    # try:
    #     op = output[0]
    #     return output
    # except:
    #     classify_text(text)

    tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")

    # Truncate the input text if it exceeds the maximum length
    max_length = tokenizer.model_max_length
    truncated_text = text[:max_length]

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": truncated_text,
    })

    
    
    try:
        op = output[0]
        return output
    except:
        return classify_text(text)




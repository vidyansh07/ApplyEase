from fastapi import FastAPI
from google import genai
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import uvicorn

app = FastAPI()

def call_gemini_api(prompt: str):
    client = genai.Client(api_key="AIzaSyB8UrO_ReDD1f9WLYx0TBzcd0CPmHzVnWc")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}

# in this endpoint we will call multiple gemini api parellely to get response with different most optimal prompts for finding remote job companies and startups
# i want to run all responses on multiple threads and then combine the results and return the final response

@app.get("/gemini")
async def get_gemini_response():
    prompts = [
        "Find companies and startup that offering only remote job give only their career portel links and classfy them in an Array that have a live careers portal for software engineering roles and include the link.",
        "Find startups and companies that are hiring for remote software engineering roles only provide their career portal links in an array format.",
        "List down the companies and startups that are offering remote software engineering jobs only provide their career portal links in an array format."
    ]
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        tasks = [loop.run_in_executor(executor, call_gemini_api, prompt) for prompt in prompts]
        responses = await asyncio.gather(*tasks)

    # Extract text from each response object
    texts = []
    for resp in responses:
        # Adjust this line based on the actual attribute that contains the text
        # For Google Generative AI Python client, it's usually resp.text or resp.candidates[0].content.parts[0].text
        try:
            text = resp.text
        except AttributeError:
            # Fallback for other possible response structures
            text = resp.candidates[0].content.parts[0].text
        texts.append(text)

    # Extract links from all texts
    links = []
    for text in texts:
        for line in text.split("\n"):
            if "http" in line:
                start = line.find("http")
                end = line.find(" ", start)
                if end == -1:
                    end = len(line)
                links.append(line[start:end])

    # Remove duplicates


    # Remove duplicates
    links = list(set(links))

    # Optionally, save new links to file as in your original code

    return {"texts": responses, "links": links}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
prompt_root_seed = os.environ["PROMPT_ROOT_SEED"]


class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.text_embeddings = os.environ["TEXT_EMBEDDINGS_TO_USE"]

    def get_embeddings(self, text):
        response = self.client.embeddings.create(
            input=text.replace("\n", " "),  # get rid of newlines
            model=self.text_embeddings,  # text embeddings model to use
        )
        embeddings = response  # ['data'][0]['embedding'] # Extracting the embeddings
        print(f"\n >>> Prompt's vevtor dimensions:", len(embeddings.data[0].embedding))
        return embeddings.data[0].embedding

    def generate_text(self, prompt):  # , model, prompt_root_seed):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Hello"},  # TODO: are these required?
                {
                    "role": "user",
                    "content": prompt + prompt_root_seed,
                },  # TODO: refactor limits to a dropdown
            ],
        )
        return response.choices[0].message.content

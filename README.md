# flashcards data

## description

A prototype using OpenAI text embeddings + Pinecone similarity search + Streamlit UI to represent data generation component to a flashcards web application. Bit more decontext about the idea in this [blog post](https://kamc.hashnode.dev/openai-streamlit-and-pinecone-db). 

The idea is to use this prototype to generate the seed data which will - eventually - be sent to a seprate/standalone web application, Flashcards.

## prerequisites
- OpenAI API key
- Pinecone API key

## usage

1. Clone the repository
2. Install the requirement:
    you can run `pipenv install` to install the requirements
3. Add these to a .env file in the root of the project:
    - `PROMPT_ROOT_SEED="limit to 100 words" `
        - As the name suggests I use this to control/limit the generated data to a certain number of words for a faster response time while developing and testing.
    - `TEXT_EMBEDDINGS_TO_USE="text-embedding-3-small"`
    - `OPENAI_API_KEY="replace-with-your-own--key"`
    - `PINECONE_API_KEY="replace-with-your-own-key"`
3. Run the Streamlit app
    3.1. `streamlit run main.py`


import uuid
import streamlit as st
from services.openai_service import OpenAIService
from services.pinecone_service import PineconeService

openai_service = OpenAIService()
pinecone_service = PineconeService()

# Streamlit app layout
st.title("Flashcard Generator")
user_prompt = st.text_input("Prompt:", "")
placeholder_search_similar = st.empty()

# Needs to be right before the section you want to control
col1, padding, col2, padding, col3, padding, col4 = st.columns(
    (10, 0.5, 10, 0.5, 10, 0.5, 10)
)


# TODO: need a better way to reset the inputs
def reset():
    pass

st.session_state["rq_disabled"] = False
with col1:
    if st.button(
        "Run Query", key="rq_button", disabled=st.session_state["rq_disabled"]
    ):
        embeds = openai_service.get_embeddings(user_prompt)
        placeholder_search_similar.empty()
        with placeholder_search_similar.container():
            # with st.spinner('Searching if a similar query exists...'):
            resp = pinecone_service.search_similar(embeds)
            # print('Pinecone: ', resp['matches'] )
            matches = resp["matches"]
            for match in matches:
                if match["score"] > 0.54:
                    with st.spinner("Searching if a similar query exists..."):
                        if st.session_state.get("rq_disabled", False):
                            st.session_state["rq_disabled"] = True
                        st.write("A similar query might already exist:")
                        st.text_input(
                            ":green[Prompt used:]",
                            match["metadata"]["u_prompt"],
                            disabled=True,
                        )
                        st.caption(
                            f':blue[**_similarity-score:_**] :green[**{match["score"]}**]'
                        )  # "\n"  :blue[**_pinecone id:_**] {match["id"]}**]')
                        st.text_area(
                            ":green[Generated response:]",
                            match["metadata"]["genai_text"],
                            height=275,
                            disabled=True,
                        )
                        with col3:
                            st.button("Reset", on_click=reset)
                        st.session_state["rq_disabled"] = True
                        break
                elif match["score"] < 0.6:
                    print("No similar queries found")
                    with st.spinner("Generating..."):
                        generated_text = openai_service.generate_text(
                            user_prompt
                        ).lower()
                        st.text_area("Generated Text:", generated_text, height=250)
                        with col3:
                            st.button("Send to Flashcard")  # TODO: this button
                        with col4:
                            st.button("Reset", on_click=reset)
                        embeds = openai_service.get_embeddings(user_prompt)
                        st.session_state["generated_text"] = generated_text
                        break

# button to save embbddings to pinecone
with col2:
    if st.button(
        "Save in Pinecone", disabled=not st.session_state.get("generated_text", False)
    ):
        embeds = openai_service.get_embeddings(user_prompt)
        with st.spinner("Saving..."):
            pineconeRecord = [
                {
                    "id": str(uuid.uuid4()),
                    "values": embeds,
                    "metadata": {
                        "u_prompt": user_prompt,
                        "genai_text": st.session_state["generated_text"],
                    },
                }
            ]
            resp = pinecone_service.insert(pineconeRecord)
            print(
                f"\nPinecone response: ",
                resp,
                "\nremoving generated_text from session state",
            )
            st.write("Query saved successfully!")
            del st.session_state["generated_text"]

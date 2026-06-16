import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from resources.chains import Chain
from resources.portfolio import Portfolio
from resources.utils import clean_text


st.set_page_config(
    page_title="AI-Powered Outreach Assistant",
    page_icon="🚀",
    layout="wide" 
)

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3rem;
}

.stTextInput > div > div > input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


def create_streamlit_app(llm, portfolio, clean_text):

    with st.sidebar:

        st.title("🚀 Outreach AI")

        st.markdown("---")

        st.markdown("""
### Features

✅ Job Description Analysis

✅ Skill Extraction

✅ Portfolio Matching

✅ AI Email Generation

### Tech Stack

- Streamlit
- LangChain
- Groq
- ChromaDB
- Python
""")

    st.markdown("""
# 🚀 AI-Powered Outreach Assistant

Generate personalized outreach emails from job postings using AI, portfolio matching, and LLMs.
""")

    url_input = st.text_input(
        "🔗 Enter Job Posting URL",
        value="https://jobs.nike.com/job/R-33460"
    )

    submit_button = st.button("Generate Email")

    if submit_button:

        if not url_input.strip():
            st.warning("Please enter a URL.")
            return

        try:

            with st.spinner("🔍 Analyzing Job Description..."):

                loader = WebBaseLoader([url_input])

                data = loader.load()

                if not data:
                    st.error("Unable to extract content from this URL.")
                    return

                page_content = clean_text(
                    data.pop().page_content
                )

                portfolio.load_portfolio()

                jobs = llm.extract_jobs(page_content)

                if not jobs:
                    st.warning("No job information found.")
                    return

                st.success("✅ Job Description Processed Successfully")

                for index, job in enumerate(jobs, start=1):

                    skills = job.get("skills", [])

                    links = portfolio.query_links(skills)

                    email = llm.write_mail(job, links)

                    st.markdown("---")

                    st.subheader(
                        f"📧 Generated Outreach Email #{index}"
                    )

                    st.code(
                        email,
                        language="markdown"
                    )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )

    st.markdown("---")

    st.caption(
        "Built with Streamlit • LangChain • Groq • ChromaDB"
    )


if __name__ == "__main__":

    chain = Chain()

    portfolio = Portfolio()

    create_streamlit_app(
        chain,
        portfolio,
        clean_text
    ) 
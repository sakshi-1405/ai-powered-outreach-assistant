import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv(
    dotenv_path=os.path.join(
        os.path.dirname(__file__),
        ".env"
    )
)


class Chain:

    def __init__(self):

        self.llm = ChatGroq(
            temperature=0.3,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):

        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED JOB PAGE:
            {page_data}

            ### TASK:
            Extract the job information from the text.

            Return ONLY valid JSON.

            JSON FORMAT:

            {{
                "role": "",
                "company": "",
                "location": "",
                "experience": "",
                "skills": [],
                "description": "",
                "responsibilities": [],
                "qualifications": []
            }}

            Return only JSON.
            """
        )

        chain_extract = prompt_extract | self.llm

        res = chain_extract.invoke(
            input={"page_data": cleaned_text}
        )

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)

        except OutputParserException:
            raise OutputParserException(
                "Unable to parse job information."
            )

        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DETAILS:
            {job_description}

            ### RELEVANT PROJECT LINKS:
            {link_list}

            ### TASK:

            You are an AI-powered outreach assistant.

            Write a professional and personalized cold email.

            Requirements:

            - Create a compelling subject line.
            - Mention the role and company.
            - Highlight relevant skills.
            - Reference the most relevant portfolio projects.
            - Keep the email concise and professional.
            - Sound human and natural.
            - Avoid generic AI-generated phrases.
            - Maximum 250 words.

            Format:

            Subject: ...

            Dear Hiring Team,

            ...

            Best Regards
            """
        )

        chain_email = prompt_email | self.llm

        res = chain_email.invoke(
            {
                "job_description": str(job),
                "link_list": links
            }
        )

        return res.content 
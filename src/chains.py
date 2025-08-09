from dotenv import load_dotenv
import datetime
from langchain_core.messages import HumanMessage
from schemas import AnswerQuestionSchema, RevisionSchema
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI



pydantic_tools_parser = PydanticToolsParser(tools=[AnswerQuestionSchema])
load_dotenv()

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",
         """you are an AI researcher.
         Current time is {current_time}.
         1. {first_instruction}
         2. reflect and critique your own response. be severe to maximize improvement.
         3. after reflection, **list 1-3 search queries separatly** that you would use to find more information about the topic. Do not include them inside the reflections.
        """
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "answer the user's question above using the required format. ")
    ]
).partial(current_time=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

llm = ChatOpenAI(model="gpt-4")

responder_prompt_template = actor_prompt_template.partial(
    first_instruction="answer the user's question in almost 250 words, detailed and comprehensive manner.",
)

revisor_prompt_template = actor_prompt_template.partial(
    first_instruction="""Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""
)


responder_chain = responder_prompt_template | llm.with_structered_output(AnswerQuestionSchema) | pydantic_tools_parser

revisor_chain = revisor_prompt_template | llm.with_structered_output(RevisionSchema)| pydantic_tools_parser
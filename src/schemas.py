from pydantic import BaseModel, Field

class ReflectionSchema(BaseModel):
    """
    Schema for the reflection.
    """
    missing: str = Field(description="critique of what is missing in the response")
    superfluous: str = Field(description="critique of what is superfluous in the response")


class AnswerQuestionSchema(BaseModel):
    """
    Schema for the answer question.
    """   
    answer: str =  Field(description="almost 250 words detailed answer to the question")
    search_queries: list[str] = Field(description="1-3 search queries that the user would use to find more information about the topic")
    reflection: ReflectionSchema = Field(description="reflect on the answer and critique it.")


class RevisionSchema(AnswerQuestionSchema):
    """
    Revise your original answer to the question
    """
    references: list[str] = Field(
        description="Citations motivating the answer."
    )

    
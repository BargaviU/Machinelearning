from typing import List

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    def to_dict(self):
        return {"summary": self.summary, "facts": self.facts}


class NetMeet(BaseModel):
    net_meets: List[str] = Field(description="net meet list")

    def to_dict(self):
        return {"net_meets": self.net_meets}


class TopicOfInterest(BaseModel):
    topics_of_interest: List[str] = Field(
        description="topic that might interest the person"
    )

    def to_dict(self):
        return {"topics_of_interest": self.topics_of_interest}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
net_meet_parser = PydanticOutputParser(pydantic_object=NetMeet)
topics_of_interest_parser = PydanticOutputParser(pydantic_object=NetMeet)

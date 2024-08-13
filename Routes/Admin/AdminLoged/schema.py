from pydantic import BaseModel


class TopicItem(BaseModel):
    topic_name: str
    criteria: str


# create schema -> admin can add topic
class AddTopics(BaseModel):
    data_set: list[TopicItem]


""""
{
    "data_set": [
        {"topic_name": "hello", "criteria": "david"},
        {"topic_name": "hii", "criteria": "silly"},
        {"topic_name": "hey", "criteria": "kenna"}
    ]
}
"""


# Create schema -> update topic
class UpdateTopic(BaseModel):
    topic_id: int
    topic_name: str
    criteria: str


# Create schema -> delete topic
class DeleteTopic(BaseModel):
    topic_id: int

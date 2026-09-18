from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# This practical assumes "model"
# has already been created.

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a clear AI instructor."
    ),
    (
        "user",
        "Explain {topic} in {points} short points."
    )
])

chain = prompt | model | StrOutputParser()

answer = chain.invoke({
    "topic": "vector databases",
    "points": 3
})

print(answer)
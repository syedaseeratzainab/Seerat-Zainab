from langchain_core.prompts import ChatPromptTemplate


study_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a patient AI instructor. "
        "Use simple language and do not use advanced mathematics."
    ),
    (
        "human",
        "Teach this topic to a {level} student:\n\n"
        "Topic: {topic}\n\n"
        "Use this format:\n"
        "1. Simple definition\n"
        "2. Three key points\n"
        "3. One easy example\n"
        "4. Two short review questions"
    )
])
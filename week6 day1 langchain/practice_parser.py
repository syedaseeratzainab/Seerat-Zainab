from langchain_core.output_parsers import StrOutputParser

# This practical assumes that 'model'
# has already been created.

parser = StrOutputParser()

response = model.invoke(
    "Define LangChain in one sentence."
)

plain_text = parser.invoke(response)

print("Message object:")
print(response)

print("\nParser:")
print(parser)

print("\nPlain text:")
print(plain_text)
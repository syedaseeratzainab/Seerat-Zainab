# #TASK 1
# word_count = int(input("Enter word count: "))

# if word_count < 100:
#     print("short")
# elif word_count <= 500:
#     print("medium")
# else:
#     print("large")

#TASK 2
file_type = input("Enter file type: ").lower()

supported_formats = ["pdf", "docx", "txt"]

if file_type in supported_formats:
    print("Format is supported")
else:
    print("Format is not supported")

    #task 3

sentence = input("Enter a sentence: ")

words = sentence.split()
count = 0

for word in words:
    if len(word) > 5:
        print(word)
        count += 1

print("Total long words:", count)


#TASK 4
chunks = [
    "Python is used for AI",
    "RAG works with documents",
    "Python can process text",
    "AI systems use retrieval"
]

keyword = input("Enter a keyword: ").lower()
matches = 0

for i, chunk in enumerate(chunks, 1):
    if keyword in chunk.lower():
        print("Result", i, ":", chunk)
        matches += 1

if matches > 0:
    print("Total matches:", matches)
else:
    print("No result found")

    #TASK 5 

keywords = []

while True:
    keyword = input("Enter a keyword: ")

    if keyword.lower() == "exit":
        break

    if keyword.strip() == "":
        continue

    keywords.append(keyword)

print("Accepted keywords:", keywords)
# This practical assumes that 'chain'
# has already been created.

while True:

    topic = input(
        "Enter a topic or type 'exit': "
    ).strip()

    if topic.lower() == "exit":
        break

    if not topic:
        print("Please enter a topic.")
        continue

    answer = chain.invoke({
        "topic": topic,
        "points": 3
    })

    print("\nAnswer:")
    print(answer)
    print()
import re


# ============================================================
# LLM CONCEPT ANALYZER
# ============================================================

def estimate_tokens(text):
    """Estimate token-like units using a simple regular expression."""
    
    tokens = re.findall(r"\w+|[^\w\s]", text)
    
    return len(tokens)


def check_context_budget(used_tokens, context_limit):
    """Check whether the prompt fits inside the context window."""
    
    remaining = context_limit - used_tokens
    
    return {
        "used": used_tokens,
        "remaining": remaining,
        "fits": used_tokens <= context_limit
    }


def select_next_token(probabilities):
    """Select the token with the highest probability."""
    
    return max(probabilities, key=probabilities.get)


# ============================================================
# TAKE PROMPT FROM USER
# ============================================================

print("=" * 60)
print("LLM CONCEPT ANALYZER")
print("=" * 60)

prompt = input("\nEnter your prompt: ")


# ============================================================
# TOKEN ESTIMATION
# ============================================================

token_count = estimate_tokens(prompt)

print("\n--- Token Analysis ---")
print("Prompt:", prompt)
print("Estimated token-like units:", token_count)


# ============================================================
# CONTEXT WINDOW
# ============================================================

context_limit = 20

result = check_context_budget(
    token_count,
    context_limit
)

print("\n--- Context Budget ---")
print("Context limit:", context_limit)
print("Tokens used:", result["used"])
print("Tokens remaining:", result["remaining"])
print("Fits context window:", result["fits"])


# ============================================================
# NEXT-TOKEN PREDICTION
# ============================================================

probabilities = {
    "AI": 0.50,
    "system": 0.30,
    "data": 0.15,
    "model": 0.05
}

next_token = select_next_token(probabilities)

print("\n--- Next-Token Prediction ---")

for token, probability in probabilities.items():
    print(token, "->", probability)

print("Selected next token:", next_token)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n--- Analysis Complete ---")

if result["fits"]:
    print("The prompt fits inside the context budget.")
else:
    print("The prompt exceeds the context budget.")
import ollama

# 1. Define the buggy code and the logic puzzle
code_to_audit = """
func transfer(a, b *Account, amount int) {
    a.Lock()
    b.Lock()
    a.balance -= amount
    b.balance += amount
    b.Unlock()
    a.Unlock()
}
"""

# 2. Construct a prompt that triggers "Chain of Thought" reasoning
prompt = f"""
Analyze the following Go code for a potential deadlock condition. 

Perform a step-by-step execution trace:
1. Imagine Goroutine 1 calls transfer(Account_A, Account_B, 100).
2. Imagine Goroutine 2 calls transfer(Account_B, Account_A, 50) at the exact same time.
3. Trace the locking order for both routines.
4. Explain if a deadlock occurs and why.
5. Provide a corrected version of the code using 'resource ordering' (sorting the locks).

Code:
{code_to_audit}
"""

# 3. Call the model
try:
    response = ollama.chat(
        model='gemma3:4b',
        messages=[{'role': 'user', 'content': prompt}]
    )

    # 4. Print the reasoning and the solution
    print("--- Code Logic Audit ---")
    print(response['message']['content'])

except Exception as e:
    print(f"An error occurred: {e}")
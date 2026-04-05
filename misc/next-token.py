import random
from collections import defaultdict

training_data = """
The cat sat on the mat. The cat saw a bird. 
A bird flew over the mat. The dog barked at the cat. 
The dog sat on the grass. The grass was green and soft. 
The mat was under the cat. A bird sat on the green grass.
The cat ate the bird on the mat.
"""

# --- THE "BRAIN" OF THE MODEL ---
# Think of self.model as a tally sheet of every conversation this bot has ever heard.
# It stores 'contexts' (what was just said) and 'predictions' (what usually comes next).
#
# Structure: { (context_word_1, context_word_2): { next_word: frequency_count } }
#
# Example after training:
# {
#   ('the', 'cat'): {
#       'sat': 5,    <-- Most likely (62.5% chance)
#       'ran': 2,    <-- Less likely (25% chance)
#       'slept': 1   <-- Rare (12.5% chance)
#   }
# }
#
# When we generate text, the bot looks at the last two words, finds this "map," 
# and rolls a weighted die to pick the next word!

class SimpleGPT:
    def __init__(self, context_size=2):
        self.context_size = context_size
        # Using a nested dictionary: {(context_tuple): {next_token: count}}
        self.model = defaultdict(lambda: defaultdict(int))

    def train(self, text):
        # Clean and tokenize
        tokens = text.lower().replace('.', ' .').split()
        
        for i in range(len(tokens) - self.context_size):
            context = tuple(tokens[i : i + self.context_size])
            next_token = tokens[i + self.context_size]
            self.model[context][next_token] += 1

    def generate(self, start_context, steps=10):
        current = tuple(start_context.lower().split())
        result = list(current)

        for _ in range(steps):
            options = self.model.get(current)
            if not options:
                break
            
            # Convert counts to probabilities
            words = list(options.keys())
            weights = list(options.values())
            
            # "Sample" the next token
            next_word = random.choices(words, weights=weights)[0]
            result.append(next_word)
            
            # Shift the context window forward
            current = tuple(result[-self.context_size:])
            
        return " ".join(result)

# Initialize and train
bot = SimpleGPT(context_size=2)
bot.train(training_data)

# Test different starting points
print("--- Generation 1 ---")
print(bot.generate("the cat"))

print("\n--- Generation 2 ---")
print(bot.generate("the grass"))

print("\n--- Generation 3 ---")
print(bot.generate("a bird"))
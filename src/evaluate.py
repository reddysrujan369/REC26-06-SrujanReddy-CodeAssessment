import pandas as pd

questions = pd.read_csv(
    "data/questions.csv"
)

print(
    "Questions:",
    len(questions)
)
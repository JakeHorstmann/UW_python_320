import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("results.csv")
    summary = df.groupby(by="function")["time"]
    print(summary.describe())
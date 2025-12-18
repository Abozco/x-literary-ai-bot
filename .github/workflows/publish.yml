name: AI Auto Publisher - X

on:
  schedule:
    - cron: "0 5 * * *"   # 07:00 مصر
    - cron: "0 12 * * *"  # 14:00 مصر
    - cron: "0 17 * * *"  # 19:00 مصر
    - cron: "0 21 * * *"  # 23:00 مصر
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install openai tweepy requests

      - name: Run bot
        run: python publish.py
        env:
          X_BEARER_TOKEN: ${{ secrets.X_BEARER_TOKEN }}
          X_API_KEY: ${{ secrets.X_API_KEY }}
          X_API_SECRET: ${{ secrets.X_API_SECRET }}
          X_ACCESS_TOKEN: ${{ secrets.X_ACCESS_TOKEN }}
          X_ACCESS_SECRET: ${{ secrets.X_ACCESS_SECRET }}
          AI_API_KEY: ${{ secrets.AI_API_KEY }}

import os
import tweepy
from openai import OpenAI

# ===== OpenAI =====
openai_client = OpenAI(
    api_key=os.getenv("AI_API_KEY")
)

# ===== X Client =====
client = tweepy.Client(
    bearer_token=os.getenv("X_BEARER_TOKEN"),
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_SECRET"),
    wait_on_rate_limit=True
)

# ===== أسلوب الرد =====
SYSTEM_PROMPT = """
اكتب الرد وكأنك صاحب الحساب نفسه.

الأسلوب:
- ساخر بذكاء عند اللزوم
- جدي ومحترم عند النقاش
- مختصر وطبيعي

ممنوع:
- التعريف بنفسك
- ذكر أنك مساعد أو ذكاء اصطناعي
- مشاركة أي معلومات شخصية
- السياسة أو الإساءة

الطول:
- من 1 إلى 3 جمل
"""

# ===== توليد الرد =====
def generate_reply(text):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.8,
        max_tokens=120
    )
    return response.choices[0].message.content.strip()

# ===== حفظ آخر ID تم الرد عليه =====
def get_last_id():
    try:
        with open("last_id.txt", "r") as f:
            return int(f.read().strip())
    except:
        return None

def save_last_id(tweet_id):
    with open("last_id.txt", "w") as f:
        f.write(str(tweet_id))

# ===== الرد على أي تعليق =====
def reply_to_all_comments():
    me = client.get_me().data.id
    last_id = get_last_id()

    mentions = client.get_users_mentions(
        id=me,
        since_id=last_id,
        max_results=10
    )

    if not mentions.data:
        print("📭 لا تعليقات جديدة")
        return

    for tweet in reversed(mentions.data):
        # تجاهل نفسك
        if tweet.author_id == me:
            continue

        reply = generate_reply(tweet.text)

        client.create_tweet(
            text=reply,
            in_reply_to_tweet_id=tweet.id
        )

        save_last_id(tweet.id)
        print(f"✅ تم الرد على تعليق {tweet.id}")

# ===== تشغيل =====
if __name__ == "__main__":
    reply_to_all_comments()

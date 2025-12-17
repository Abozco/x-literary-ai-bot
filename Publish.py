import os
import random
import tweepy
import openai

# إعداد حساب X
client = tweepy.Client(
    bearer_token=os.getenv("X_BEARER_TOKEN"),
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_SECRET")
)

# إعداد OpenAI
openai.api_key = os.getenv("AI_API_KEY")

SYSTEM_PROMPT = """
أنت كاتب أدبي وفيلسوف معاصر.
تكتب اقتباسات صريحة مع ذكر اسم الكاتب.
أسلوبك حكيم، فلسفي، هادئ، جريء فكرياً.

ممنوع:
- السياسة
- الجنس
- الشتائم
- الإساءة

ابدأ دائماً بـ Hook
اختم بسؤال تفاعلي
"""

def generate_post(thread=False):
    prompt = (
        "اكتب ثريد من 3 تغريدات أدبية تحفيزية، مع اقتباس صريح واسم الكاتب."
        if thread else
        "اكتب تغريدة أدبية تحفيزية قصيرة مع اقتباس صريح واسم الكاتب."
    )

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

def post():
    if random.choice([True, False]):
        tweets = generate_post(True).split("\n")
        first = client.create_tweet(text=tweets[0])
        reply_to = first.data["id"]
        for t in tweets[1:]:
            reply_to = client.create_tweet(
                text=t,
                in_reply_to_tweet_id=reply_to
            ).data["id"]
    else:
        client.create_tweet(text=generate_post())

def reply_mentions():
    me = client.get_me().data.id
    mentions = client.get_users_mentions(id=me, max_results=3)
    if not mentions.data:
        return

    for m in mentions.data:
        r = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"رد ذكي ومحترم على:\n{m.text}"}
            ],
            temperature=0.7,
            max_tokens=150
        )
        client.create_tweet(
            text=r.choices[0].message.content,
            in_reply_to_tweet_id=m.id
        )

# تشغيل البوت
post()
reply_mentions()

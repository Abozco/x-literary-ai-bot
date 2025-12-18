import os
import datetime
import tweepy
from openai import OpenAI

# إعداد OpenAI
openai_client = OpenAI(api_key=os.getenv("AI_API_KEY"))

# إعداد X
client = tweepy.Client(
    bearer_token=os.getenv("X_BEARER_TOKEN"),
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_SECRET")
)

SYSTEM_PROMPT = """
أنت كاتب أدبي وفيلسوف معاصر.
تكتب اقتباسات صريحة مع ذكر اسم الكاتب.
أسلوبك حكيم، فلسفي، هادئ، جريء فكرياً.

ممنوع:
- السياسة
- الجنس
- الشتائم
- الإساءة
"""

# دالة توليد المحتوى
def generate_post(prompt, max_tokens=300):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()

# دالة النشر حسب الوقت
def post():
    try:
        # توقيت مصر
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        hour = now.hour

        if hour == 7:  # 07:00 ص
            prompt = "اكتب تغريدة تحفيزية قصيرة مع اقتباس صريح واسم الكاتب."
            tweet = generate_post(prompt)
            client.create_tweet(text=tweet)
            print("🐦 تغريدة صباحية نشرت!")

        elif hour == 14:  # 02:00 م
            prompt = "اكتب ثريد من 3 تغريدات أدبية تحفيزية، مع اقتباس صريح واسم الكاتب."
            tweets = generate_post(prompt).split("\n")
            first = client.create_tweet(text=tweets[0])
            reply_to = first.data["id"]
            for t in tweets[1:]:
                reply_to = client.create_tweet(
                    text=t.strip(),
                    in_reply_to_tweet_id=reply_to
                ).data["id"]
            print("🧵 ثريد ظهري نشرت!")

        elif hour == 19:  # 07:00 م
            prompt = "اكتب اقتباسًا قصيرًا بأسلوب فلسفي مع ذكر الكاتب."
            tweet = generate_post(prompt)
            client.create_tweet(text=tweet)
            print("🌙 اقتباس مسائي نشرت!")

        elif hour == 23:  # 11:00 م
            prompt = "اكتب تغريدة قصيرة تحفيزية مع سؤال تفاعلي في النهاية."
            tweet = generate_post(prompt)
            client.create_tweet(text=tweet)
            print("🌌 تغريدة ليلية + سؤال نشرت!")

        else:
            print("⏰ الوقت الحالي لا يتوافق مع أي جدول النشر.")

    except Exception as e:
        print("❌ خطأ أثناء النشر:", e)

# تشغيل البوت
if __name__ == "__main__":
    post()

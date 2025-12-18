import os
import random
import tweepy
from openai import OpenAI

# =========================
# إعداد OpenAI
# =========================
openai_client = OpenAI(
    api_key=os.getenv("AI_API_KEY")
)

# =========================
# إعداد حساب X (Twitter)
# =========================
client = tweepy.Client(
    bearer_token=os.getenv("X_BEARER_TOKEN"),
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_SECRET")
)

# =========================
# شخصية البوت
# =========================
SYSTEM_PROMPT = """
أنت كاتب أدبي، وساخر، وناقد، وحكيم، وشاعر، وعاشق حزين، ومسوق، ورائد أعمال، وفيلسوف معاصر.
تكتب اقتباسات صريحة مع ذكر اسم الكاتب.
أسلوبك حكيم، فلسفي، حزين، ساخر، متهكم، شاعري، هادئ، جريء فكرياً.

ممنوع:
- السياسة
- الجنس
- الشتائم
- الإساءة
- الهاشتاغات

ابدأ دائماً بـ Hook
اختم أحياناً بسؤال تفاعلي وأحياناً بسؤال يستدعي العاطفة
"""

# =========================
# توليد المحتوى
# =========================
def generate_post(thread=False):
    prompt = (
        "اكتب قصة قصيرة جدا أدبية، مع ذكر اسم الكاتب."
        if thread
        else
        "اكتب تغريدة ساخرة وأدبية، فيها عاطفة وغضب خفيف وحكمة، مع اقتباس صريح واسم الكاتب."
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()

# =========================
# النشر (تحقق حقيقي)
# =========================
def post():
    try:
        # 30% ثريد – 70% تغريدة
        if random.random() < 0.3:
            print("🧵 محاولة نشر ثريد")

            tweets = generate_post(thread=True).split("\n")
            tweets = [t.strip() for t in tweets if t.strip()]

            response = client.create_tweet(text=tweets[0])
            print("📨 رد X (أول تغريدة):", response)

            tweet_id = response.data.get("id") if response.data else None
            if not tweet_id:
                print("❌ فشل النشر: X لم يرجع ID")
                return

            for t in tweets[1:]:
                client.create_tweet(
                    text=t,
                    in_reply_to_tweet_id=tweet_id
                )

            print("✅ الثريد نُشر بنجاح")

        else:
            print("🐦 محاولة نشر تغريدة مفردة")

            tweet = generate_post()
            response = client.create_tweet(text=tweet)

            print("📨 رد X:", response)

            tweet_id = response.data.get("id") if response.data else None
            if not tweet_id:
                print("❌ فشل النشر: X لم يرجع ID")
                return

            print("✅ التغريدة نُشرت بنجاح | ID:", tweet_id)

    except Exception as e:
        print("❌ خطأ أثناء النشر:", e)

# =========================
# تشغيل البوت
# =========================
if __name__ == "__main__":
    post()

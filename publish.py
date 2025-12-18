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
أنت كاتب أدبي، وساخر، وناقد، وحيكم، وشاعر، وعاشق حزين، ومسوق، ورائد اعمال، وفيلسوف معاصر.
تكتب اقتباسات صريحة مع ذكر اسم الكاتب.
أسلوبك حكيم، فلسفي، حزين، ساخر، متهكم، شاعري، هادئ، جريء فكرياً.

ممنوع:
- السياسة
- الجنس
- الشتائم
- الإساءة

ابدأ دائماً بـ Hook
اختم أحيانا بسؤال تفاعلي وأحيانا أختم بسؤال يستدعي العاطفة
"""

# =========================
# توليد المحتوى
# =========================
def generate_post(thread=False):
    prompt = (
        "اكتب ثريد من 3 تغريدات لقصة قصيرة ، مع ذكر اسم الكاتب."
        if thread
        else
        "،اكتب تغريدات ساخرة في نادي ريال مدريد، وساخرة في كريستيانو رونالدو، ومدح برشلونة ومدح ميسي، مضحكة، وحزينة، وعاطفية، وغاضبة، وأدبية، واقتباس صريح واسم الكاتب."
          
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
# النشر (مضمون 100%)
# =========================
def post():
    try:
        # 30% ثريد – 70% تغريدة
        if random.random() < 0.3:
            print("🧵 نشر ثريد")
            tweets = generate_post(thread=True).split("\n")

            first = client.create_tweet(text=tweets[0])
            reply_to = first.data["id"]

            for t in tweets[1:]:
                client.create_tweet(
                    text=t.strip(),
                    in_reply_to_tweet_id=reply_to
                )
        else:
            print("🐦 نشر تغريدة")
            tweet = generate_post()
            client.create_tweet(text=tweet)

        print("✅ تم النشر بنجاح")

    except Exception as e:
        print("❌ خطأ أثناء النشر:", e)

# =========================
# تشغيل البوت
# =========================
if __name__ == "__main__":
    post()

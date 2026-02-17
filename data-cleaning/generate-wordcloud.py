import os

from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS

from services.influencers_service import InfluencersService
from shared.constants import NOISE_WORDS
from shared.mongo import MongoConnection

os.environ["NUMEXPR_MAX_THREADS"] = "12"

mongo_connection = MongoConnection()
influencers_service = InfluencersService(mongo_connection)

influencers = influencers_service.get_influencers()
info_string = ""
for influencer in influencers:
    if influencer.get("Bio", "NULL") != "NULL":
        info_string += influencer["Bio"] + " "
    if influencer.get("Category", "NULL") != "NULL":
        info_string += influencer["Category"] + " "

custom_stopwords = set(STOPWORDS) | NOISE_WORDS
wordcloud = WordCloud(
    width=800, height=400, background_color="white", max_words=100, stopwords=custom_stopwords, colormap="viridis"
).generate(info_string)

# Display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
wordcloud.to_file("wordcloud.png")

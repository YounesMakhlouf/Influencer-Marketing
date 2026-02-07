import spacy

from services.influencers_service import InfluencersService
from shared.mongo import MongoConnection

mongo_connection = MongoConnection()
influencers_service = InfluencersService(mongo_connection)
influencers = influencers_service.get_influencers()

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])


def lemmatize_text(text):
    doc = nlp(text)
    new_text = []
    for word in doc:
        new_text.append(word.lemma_)
    lemmatized_text = " ".join(new_text)
    print(lemmatized_text)
    return lemmatized_text


def lemmatize_captions(influencer, post_type):
    posts = influencer.get(post_type, [])
    updated_posts = []
    for post in posts:
        captions = post.get('captions', [])
        lemmatized_captions = []
        for caption in captions:
            lemmatized_caption = lemmatize_text(caption)
            print(lemmatized_caption)
            lemmatized_captions.append(lemmatized_caption)
            post['captions'] = lemmatized_captions
            updated_posts.append(post)
            influencers_service.update_influencer(influencer, post_type, updated_posts)


def lemmatize_titles(influencer, post_type, ):
    posts = influencer.get(post_type, [])
    updated_posts = []
    for post in posts:
        title = post.get('title')
        lemmatized_title = lemmatize_text(title)
        print(lemmatized_title)
        post['title'] = lemmatized_title
        updated_posts.append(post)
        influencers_service.update_influencer(influencer, post_type, updated_posts)


def lemmatize_bio(influencer):
    bio = influencer.get('Bio')
    print(bio)
    lemmatized_bio = lemmatize_text(bio)
    print(lemmatized_bio)
    influencers_service.update_influencer(influencer, 'Bio', lemmatized_bio)


# test

i=0
for influencer in influencers:
    lemmatize_bio(influencer)
    print("treated bios so far : ",i)
    i=i+1
    # lemmatize_titles(influencer, 'images')
    # lemmatize_titles(influencer, 'videos')
    # lemmatize_captions(influencer, 'images')
    # lemmatize_captions(influencer, 'videos')

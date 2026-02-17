import spacy

from services.influencers_service import InfluencersService
from shared.mongo import MongoConnection


def lemmatize_text(text, *, nlp):
    doc = nlp(text)
    new_text = []
    for word in doc:
        new_text.append(word.lemma_)
    lemmatized_text = " ".join(new_text)
    print(lemmatized_text)
    return lemmatized_text


def lemmatize_captions(influencer, post_type, *, nlp, influencers_service):
    posts = influencer.get(post_type, [])
    updated_posts = []
    for post in posts:
        captions = post.get("captions", [])
        lemmatized_captions = []
        for caption in captions:
            lemmatized_caption = lemmatize_text(caption, nlp=nlp)
            print(lemmatized_caption)
            lemmatized_captions.append(lemmatized_caption)
            post["captions"] = lemmatized_captions
            updated_posts.append(post)
            influencers_service.update_influencer(influencer, post_type, updated_posts)


def lemmatize_titles(influencer, post_type, *, nlp, influencers_service):
    posts = influencer.get(post_type, [])
    updated_posts = []
    for post in posts:
        title = post.get("title")
        lemmatized_title = lemmatize_text(title, nlp=nlp)
        print(lemmatized_title)
        post["title"] = lemmatized_title
        updated_posts.append(post)
        influencers_service.update_influencer(influencer, post_type, updated_posts)


def lemmatize_bio(influencer, *, nlp, influencers_service):
    bio = influencer.get("Bio")
    print(bio)
    lemmatized_bio = lemmatize_text(bio, nlp=nlp)
    print(lemmatized_bio)
    influencers_service.update_influencer(influencer, "Bio", lemmatized_bio)


def main():
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    mongo_connection = MongoConnection()
    influencers_service = InfluencersService(mongo_connection)
    influencers = influencers_service.get_influencers()

    for i, influencer in enumerate(influencers):
        lemmatize_bio(influencer, nlp=nlp, influencers_service=influencers_service)
        print("treated bios so far:", i)
        # lemmatize_titles(influencer, 'images', nlp=nlp, influencers_service=influencers_service)
        # lemmatize_titles(influencer, 'videos', nlp=nlp, influencers_service=influencers_service)
        # lemmatize_captions(influencer, 'images', nlp=nlp, influencers_service=influencers_service)
        # lemmatize_captions(influencer, 'videos', nlp=nlp, influencers_service=influencers_service)


if __name__ == "__main__":
    main()

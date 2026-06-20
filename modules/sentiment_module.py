from textblob import TextBlob


def sentiment(text):


    polarity = TextBlob(

        text

    ).sentiment.polarity


    if polarity > 0.2:


        return "Positive"


    elif polarity < -0.2:


        return "Negative"


    else:


        return "Neutral"

from decimal import Decimal

import pandas as pd


def emojiConversion(file):
    data = pd.read_csv(f"emojicounts/{file}")
    emoji_counts = list(data.itertuples(index=False, name=None))

    score_data = pd.read_csv("3-way_dataset.csv", sep=";")

    emotion_dataframe = pd.DataFrame(columns=["category", "count"])

    def EmojiToEmotion(emoji):
        nonlocal emotion_dataframe
        nonlocal emoji_counts
        emoji_row = score_data[score_data["Emoji"] == emoji]
        emoji_row.reset_index(drop=True, inplace=True)
        if len(emoji_row) == 1:
            category = emoji_row.at[0, 'Category']
            score_tuple = [score_tuple for score_tuple in emoji_counts if score_tuple[0] == emoji]
            count = score_tuple[0][1]
            emotion_dataframe = emotion_dataframe.append({'category': category, "count": count}, ignore_index=True)

    for (emoji, count) in emoji_counts:
        EmojiToEmotion(emoji)

    def createAggregation():
        nonlocal emotion_dataframe

        emotion_dataframe = emotion_dataframe.groupby("category").agg(
            totaL_count=pd.NamedAgg(column="count", aggfunc=sum)
        )

        emotion_dataframe = emotion_dataframe.applymap(lambda x: float(x) if isinstance(x, Decimal) else x)
        emotion_dataframe.to_csv(f"summary/3way/{file}", decimal=',')

    createAggregation()


emojiConversion("brezen_duben.csv")
emojiConversion("kveten_cerven.csv")
emojiConversion("cervenec_srpen.csv")
emojiConversion("zari_rijen.csv")
emojiConversion("listopad_prosinec.csv")


import advertools as adv
import pandas as pd

emojis = ["😠", "😡", "😤", "😒", "👎", "👀", "💭", "💰", "😬", "✊", "😖", "😣", "😫", "💩", "😷", "😨", "😱", "😰", "😟", "👻",
          "☺", "😆", "😂", "😹", "😊", "😢", "😭", "💔", "😞", "😥", "🙈", "🎉", "😍", "😳", "🙊", "😙", "💕", "🌹", "💋", "😚"
          ]


def transformData(file):
    try:
        data = pd.read_csv(f"data/{file}", sep=";")
        tweets = data["tweet"].tolist()

        emoji_summary = adv.extract_emoji(tweets)

        all_emojis = emoji_summary['top_emoji']
        selected_emojis = []

        for (emoji, count) in all_emojis:
            if emoji in emojis:
                selected_emojis.append((emoji, count))

        data = pd.DataFrame(selected_emojis, columns=["Emoji", "Count"])
        data.to_csv(f"emojicounts/{file}", index=False)
        print(f"Transformation for file {file} done")
    except FileNotFoundError:
        print(f"File named {file} not found")


transformData("brezen_duben.csv")
transformData("kveten_cerven.csv")
transformData("cervenec_srpen.csv")
transformData("zari_rijen.csv")
transformData("listopad_prosinec.csv")

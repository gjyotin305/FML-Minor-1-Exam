from wordcloud import WordCloud
import matplotlib.pyplot as plt 

def generate_wordcloud(text: str, file_name: str):
    wc = WordCloud(background_color="white", colormap='Oranges', width=300, height=300).generate(text)
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(f"word_cloud_{file_name}.png")
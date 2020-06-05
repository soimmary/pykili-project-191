import matplotlib.pyplot as plt
import collections

FORGOTTEN_WORDS = collections.Counter()
all_words = input().split()
for word in all_words:
        FORGOTTEN_WORDS[word] += 1

def drawing_dar():
        words = list(FORGOTTEN_WORDS.values())
        number = list(FORGOTTEN_WORDS.keys())

        plt.bar(number, words, color='pink')
        plt.title('Le parole che dimentichi')
        plt.ylabel('Volte')
        plt.xlabel('Parole')
        plt.savefig(r'МАШУЛЯМОЛОДЕЦ.jpg', dpi=1000, bbox_inches=0)
        bot.send_photo(user_id, open('.jpg', 'rb'))

import random

songs = {
    "Happy": [
        ("Ilahi", "Arijit Singh"),
        ("Gallan Goodiyaan", "Dil Dhadakne Do"),
        ("Badtameez Dil", "Yeh Jawaani Hai Deewani"),
        ("London Thumakda", "Queen"),
        ("Kar Gayi Chull", "Kapoor & Sons")
    ],

    "Sad": [
        ("Channa Mereya", "Arijit Singh"),
        ("Agar Tum Saath Ho", "Tamasha"),
        ("Hamari Adhuri Kahani", "Arijit Singh"),
        ("Tum Hi Ho", "Aashiqui 2"),
        ("Tujhe Bhula Diya", "Anjaana Anjaani")
    ],

    "Angry": [
        ("Sultan", "Sultan"),
        ("Malhari", "Bajirao Mastani"),
        ("Apna Time Aayega", "Gully Boy"),
        ("Zinda", "Bhaag Milkha Bhaag"),
        ("Kar Har Maidaan Fateh", "Sanju")
    ],

    "Relaxed": [
        ("Iktara", "Wake Up Sid"),
        ("Shaam", "Aisha"),
        ("Khaabon Ke Parinday", "Zindagi Na Milegi Dobara"),
        ("Kho Gaye Hum Kahan", "Baar Baar Dekho"),
        ("Tu Bin Bataye", "Rang De Basanti")
    ]
}


def recommend_songs(emotion, number=3):
    available = songs.get(emotion, [])

    number = min(number, len(available))

    return random.sample(available, number)
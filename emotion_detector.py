def detect_emotion(text):
    text = text.lower()

    emotions = {
        "Happy": [
            "happy", "excited", "great", "amazing", "awesome",
            "good", "love", "joy", "fun", "wonderful",
            "खुश", "खुशी", "मस्त", "आनंद"
        ],

        "Sad": [
            "sad", "lonely", "cry", "depressed", "hurt",
            "alone", "upset", "broken", "pain",
            "दुखी", "उदास", "अकेला", "अकेली", "दर्द"
        ],

        "Angry": [
            "angry", "mad", "hate", "annoyed", "furious",
            "irritated", "rage", "fight",
            "गुस्सा", "नाराज़", "क्रोध", "चिढ़"
        ],

        "Relaxed": [
            "relaxed", "calm", "peace", "peaceful",
            "chill", "quiet", "comfortable", "relax",
            "शांत", "सुकून", "आराम", "निवांत"
        ]
    }

    scores = {
        "Happy": 0,
        "Sad": 0,
        "Angry": 0,
        "Relaxed": 0
    }

    for emotion, words in emotions.items():
        for word in words:
            if word in text:
                scores[emotion] += 1

    if max(scores.values()) == 0:
        return "Relaxed"

    return max(scores, key=scores.get)
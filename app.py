import streamlit as st

from emotion_detector import detect_emotion
from recommender import recommend_songs


st.set_page_config(
    page_title="Emotion Music Recommender",
    page_icon="🎵",
    layout="centered"
)


st.title("🎵 Emotion-Based Music Recommender")

st.write(
    "Tell me how you are feeling and get Hindi song recommendations."
)

st.divider()


user_text = st.text_area(
    "💭 How are you feeling?",
    placeholder="Example: I am very happy today!"
)


number = st.slider(
    "🎶 Number of songs",
    1,
    5,
    3
)


if st.button("🎧 Recommend Songs"):

    if not user_text.strip():

        st.warning("Please tell me how you are feeling.")

    else:

        emotion = detect_emotion(user_text)

        icons = {
            "Happy": "😊",
            "Sad": "😢",
            "Angry": "😡",
            "Relaxed": "😌"
        }

        st.success(
            f"Detected Emotion: {icons[emotion]} {emotion}"
        )

        st.subheader("🎵 Recommended Hindi Songs")

        recommendations = recommend_songs(
            emotion,
            number
        )

        for i, (song, artist) in enumerate(
            recommendations,
            start=1
        ):

            st.markdown(
                f"### {i}. 🎶 {song}"
            )

            st.write(
                f"Artist / Movie: **{artist}**"
            )

            st.divider()


st.caption(
    "Emotion-Based Music Recommender | Python + Streamlit"
)
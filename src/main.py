import streamlit as st
import os
import tempfile
from brain import AmadeusBrain
from emo import AmadeusEmo
from sprite import AmadeusSprite
from audio import AmadeusVoice
import subprocess

# Function to play sound
def play_sound(sound_path):
    command = ["ffplay", "-nodisp", "-autoexit", "-hide_banner", sound_path]
    subprocess.call(command)

# Function to load and display an image and play a sound based on input
def show_character_response(user_input):
    out_emo, out_text = br(user_input, "cai")

    duration = voc.make_voice(out_text, 'en', 'ja')
    print(duration)
    spr.make_sprite(out_emo, duration=duration)

    # Display the GIF
    st.image(spr.save_path)
    st.write(f"Amadeus: {out_text}")
    play_sound(voc.save_path)

# Initialize the character
br = AmadeusBrain()
emo = AmadeusEmo()
spr = AmadeusSprite()
voc = AmadeusVoice()

# Streamlit UI
st.title("Amadeus Test App")

user_input = st.text_input("You: ")

if st.button("Send"):
    show_character_response(user_input)
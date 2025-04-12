# music_player.py

import pygame

# Initialize Pygame mixer for music
pygame.mixer.init()

# List of music files with absolute paths
music_files = [
    "C:/xampp/htdocs/Connect4AIProject/assets/AyraStar_Music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/Cr&AS_Ngozi_Music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/DarkooFtRema_Music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/MohBad_Music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/music.wav",
    "C:/xampp/htdocs/Connect4AIProject/assets/Teni_Malaika_Music.wav"
]

# Music control variables
music_index = 0  # Start with the first track
playing = False  # Music is off initially

def play_music():
    global playing
    track = music_files[music_index]
    
    if not playing:
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)  # Play on loop
        playing = True
    else:
        pygame.mixer.music.pause()
        playing = False

def stop_music():
    pygame.mixer.music.stop()
    global playing
    playing = False

def next_track():
    global music_index
    music_index = (music_index + 1) % len(music_files)
    pygame.mixer.music.load(music_files[music_index])
    pygame.mixer.music.play(-1)

def previous_track():
    global music_index
    music_index = (music_index - 1) % len(music_files)
    pygame.mixer.music.load(music_files[music_index])
    pygame.mixer.music.play(-1)

import os

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import concatenate_audioclips, AudioFileClip


INPUT_PATH = "./input/demo.mp3"
assert os.path.exists(INPUT_PATH)

# TIMES[0]: the start of the first sentence
# TIMES[1]: the end of the first sentence (and also the start of the second sentence)
# TIMES[k]: the end of the kth sentence (and also the start of the (k+1)th sentence)
TIMES = [3.8, 5.9, 9.1]

OUTPUT_DIR = "./output"

# After play an English clip for T seconds, we play silence for (SILENCE_DURATION_RATE * T) seconds
SILENCE_AUDIO_PATH = "./input/silence_one_minute.mp3"
SILENCE_DURATION_RATE = 2.5

# Play CYCLE times
CYCLES = 10


def concatenate_audios(audio_clip_paths, output_path):
    clips = [AudioFileClip(path) for path in audio_clip_paths]
    concatenate_audioclips(clips).write_audiofile(output_path)

    # Each AudioFlipClip instance creates a subprocesse
    # If we do not call close(), the subresources will not be cleaned up until the process ends.
    for clip in clips:
        clip.close()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system("rm -rf '{:s}'".format(OUTPUT_DIR))
    os.system("mkdir '{:s}'".format(OUTPUT_DIR))

    for index in range(len(TIMES) - 1):
        output_path = os.path.join(OUTPUT_DIR, "{:02d}.mp3".format(index + 1))

        ffmpeg_extract_subclip(
            INPUT_PATH, TIMES[index], TIMES[index + 1], targetname="tmp_english.mp3")

        silence_duration_seconds = (
            TIMES[index + 1] - TIMES[index]) * SILENCE_DURATION_RATE
        assert silence_duration_seconds < 60 - 1
        ffmpeg_extract_subclip(
            SILENCE_AUDIO_PATH, 0, silence_duration_seconds, targetname="tmp_silence.mp3")

        concatenate_audios(
            ["tmp_english.mp3", "tmp_silence.mp3"], "tmp_combination.mp3")
        concatenate_audios(
            ["tmp_combination.mp3"] * CYCLES, output_path)

    os.system("rm -rf tmp_english.mp3 tmp_silence.mp3 tmp_combination.mp3")


if __name__ == "__main__":
    main()

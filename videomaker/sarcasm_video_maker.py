from moviepy.editor import *
import os

def main():

    # Create a directory to store output files
    output_dir = "sarcasm_output"
    os.makedirs(output_dir, exist_ok=True)

    template_image = "video/template_image_3.jpg"
    template_audio = "video/template_audio_3.mp3"

    filenames = []
    
    for root, dirs, files in os.walk("sarcasm"):
        for file in files:
            if file.endswith(".jpg"):
                filenames.append(file.split(".")[0])

    for idx, x in enumerate(filenames):
        video_output_path = os.path.join(output_dir, f"{x}.mp4")
        # video_path = f"accidents/NOT CREATED/{x}.mp4"

        # if not os.path.exists(video_path):
        #     print(f"Skipping {video_path} (file not found)")
        #     continue

        if os.path.exists(video_output_path):
            print(f"Skipping {video_output_path} (already exists)")
            continue

        if not os.path.exists(f"sarcasm/{x}.jpg"):
            print(f"Skipping {x} (file not found)")
            continue

        bg_video_duration = 10

        min_duration = 10
        template_video_clip = ImageClip(template_image, duration=min_duration).resize(height=1920)

        meme_video_clip = ImageClip(f"sarcasm/{x}.jpg", duration=min_duration).resize(width=1080) 

        # Set audio if available
        if meme_video_clip.audio:
            meme_video_clip = meme_video_clip.set_audio(meme_video_clip.audio.set_duration(min_duration))

        # Position accident video at center
        meme_video_clip = meme_video_clip.set_position(("center", "center"))

        # Add background audio
        background_audio = AudioFileClip(template_audio).set_duration(min_duration)

        # Build final video
        final_video = CompositeVideoClip([template_video_clip, meme_video_clip]).set_fps(30)
        final_video = final_video.set_audio(background_audio)

        # Export final video
        final_video.write_videofile(video_output_path, codec="libx264", audio_codec="aac")

        print(f"Video {idx + 1} processed: {video_output_path}")


if __name__ == "__main__":
    main()

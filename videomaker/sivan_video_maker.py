from moviepy.editor import *
import os

def main():

    # Create a directory to store output files
    output_dir = "sivan_output"
    os.makedirs(output_dir, exist_ok=True)

    template_image = "video/template_image_2.jpg"
    template_audio = "video/template_audio_2.mp3"

    filenames = []
    
    for root, dirs, files in os.walk("accidents"):
        for file in files:
            if file.endswith(".mp4"):
                filenames.append(file.split(".")[0])

    for idx, x in enumerate(filenames):
        video_output_path = os.path.join(output_dir, f"{x}.mp4")
        video_path = f"accidents/{x}.mp4"

        if not os.path.exists(video_path):
            print(f"Skipping {video_path} (file not found)")
            continue

        if os.path.exists(video_output_path):
            print(f"Skipping {video_output_path} (already exists)")
            continue

        # Load template image as background
        bg_video_duration = AudioFileClip(template_audio).duration  # Use audio duration as reference

        # Load accident video
        video_clip = VideoFileClip(video_path).resize(height=648)

        # Trim accident video to match background duration
        min_duration = min(bg_video_duration, video_clip.duration)
        template_video_clip = ImageClip(template_image, duration=min_duration).resize(height=1920)

        video_clip = video_clip.subclip(0, min_duration)

        # Set audio if available
        if video_clip.audio:
            video_clip = video_clip.set_audio(video_clip.audio.set_duration(min_duration))

        # Position accident video at center
        video_clip = video_clip.set_position(("center", "center"))

        # Add background audio
        background_audio = AudioFileClip(template_audio).set_duration(min_duration)

        # Build final video
        final_video = CompositeVideoClip([template_video_clip, video_clip]).set_fps(30)
        final_video = final_video.set_audio(background_audio)

        # Export final video
        final_video.write_videofile(video_output_path, codec="libx264", audio_codec="aac")

        print(f"Video {idx + 1} processed: {video_output_path}")


if __name__ == "__main__":
    main()

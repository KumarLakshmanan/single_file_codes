from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
from moviepy.video.fx.all import resize
from moviepy.video.VideoClip import ColorClip
import os
import cv2

def blur(clip, ksize=51):
    # Ensure ksize is a tuple of odd integers (required by OpenCV)
    if isinstance(ksize, int):
        ksize = (ksize, ksize)
    if ksize[0] % 2 == 0:
        ksize = (ksize[0]+1, ksize[1])
    if ksize[1] % 2 == 0:
        ksize = (ksize[0], ksize[1]+1)
    return clip.fl_image(lambda image: cv2.GaussianBlur(image, ksize, 0))

def main():

    # Create a directory to store output files
    output_dir = "murugan_output/NOT UPLOADED"
    input_dir = "murugan_output/NOT PROCESSED"
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist. Please check the path.")
        return

    os.makedirs(output_dir, exist_ok=True)

    template_image = "video/template_image_1.jpg"
    template_audio = "video/template_audio_1.mp3"
    watermark = "video/water.png"
    # template size is 1080x1920
    # center area size is 1080x720 (3:2)
    filenames = []
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".mp4"):
                filenames.append(file.split(".")[0])

    for idx, x in enumerate(filenames):
        video_output_path = os.path.join(output_dir, f"{x}.mp4")
        video_path = os.path.join(input_dir, f"{x}.mp4")

        if not os.path.exists(video_path):
            print(f"Skipping {video_path} (file not found)")
            continue

        if os.path.exists(video_output_path):
            print(f"Skipping {video_output_path} (already exists)")
            continue

        # Load template image as background
        template_img_clip = ImageClip(template_image)
        bg_w, bg_h = template_img_clip.size
        bg_video_duration = AudioFileClip(template_audio).duration  # Use audio duration as reference

        # Load accident video
        video_clip = VideoFileClip(video_path)

        # Trim accident video to match background duration
        min_duration = min(bg_video_duration, video_clip.duration)
        template_img_clip = template_img_clip.set_duration(min_duration)
        video_clip = video_clip.subclip(0, min_duration)
        watermark_video_clip = ImageClip(watermark, duration=min_duration).resize(width=350)

        # Calculate center 3:2 area size (fixed at 1080x720, but not exceeding template image)
        center_w = min(bg_w, 1080)
        center_h = min(bg_h, 720)
        # Ensure 3:2 ratio
        if center_w / 3 * 2 > center_h:
            center_w = int(center_h * 3 / 2)
        else:
            center_h = int(center_w * 2 / 3)
        center_x = (bg_w - center_w) // 2
        center_y = (bg_h - center_h) // 2

        # Blurred, zooming background video, covering the 3:2 area (object-fit: cover)
        def resize_cover(clip, target_w, target_h):
            iw, ih = clip.size
            scale = max(target_w / iw, target_h / ih)
            clip = clip.resize(scale)
            cw, ch = clip.size
            x1 = (cw - target_w) // 2
            y1 = (ch - target_h) // 2
            return clip.crop(x1=x1, y1=y1, x2=x1+target_w, y2=y1+target_h)

        # Center 3:2 area filled with blurred, zooming video
        blurred_center_clip = (
            video_clip
            .fx(resize_cover, center_w, center_h)
            .fx(blur, 51)
            .fx(resize, lambda t: 1.05 + 0.05 * t / min_duration)
            .set_position((center_x, center_y))
            .set_opacity(0.9)
        )

        # White rectangle in center (same as blur area)
        white_rect = ColorClip(size=(center_w, center_h), color=(255,255,255), duration=min_duration).set_opacity(0.3)
        white_rect = white_rect.set_position((center_x, center_y))

        # Foreground video: original aspect ratio, fit inside 3:2 area (max 1080x720), centered (no crop)
        iw, ih = video_clip.size
        scale = min(center_w / iw, center_h / ih)
        fg_w, fg_h = int(iw * scale), int(ih * scale)
        fg_x = center_x + (center_w - fg_w) // 2
        fg_y = center_y + (center_h - fg_h) // 2
        fg_y = fg_y + 20
        fg_clip = video_clip.resize(scale).set_position((fg_x, fg_y))

        watermark_video_clip = watermark_video_clip.set_position(("right", "bottom"))

        # Add background audio
        background_audio = AudioFileClip(template_audio).set_duration(min_duration)

        # Build final video
        final_video = CompositeVideoClip(
            [template_img_clip, white_rect, blurred_center_clip, fg_clip, watermark_video_clip],
            size=(bg_w, bg_h)
        ).set_fps(30)
        final_video = final_video.set_audio(background_audio)

        # Export final video
        final_video.write_videofile(video_output_path, codec="libx264", audio_codec="aac")

        print(f"Video {idx + 1} processed: {video_output_path}")


if __name__ == "__main__":
    main()

from moviepy.editor import ImageSequenceClip


def movie_save(files, fps, out_file):
    clip = ImageSequenceClip(files, fps=fps)
    clip.write_videofile(out_file)

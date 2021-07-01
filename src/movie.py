from moviepy.editor import ImageSequenceClip


def movie_save(files, fps, out_file):
    clip = ImageSequenceClip(files, fps=fps)
    if out_file[-4:] == '.avi':
        clip.write_videofile(out_file, codec='png', logger=None)
    elif out_file[-4:] == '.mp4':
        clip.write_videofile(out_file, codec='libx264', logger=None)

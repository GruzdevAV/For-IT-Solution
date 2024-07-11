from django.db import models

import cv2, numpy as np, os
from PIL import Image, ImageFont, ImageDraw, ImageColor
from base64 import b64encode
from ffmpeg.ffmpeg import FFmpeg

class Color:
    
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
    
    def __hash__(self):
        return self.code.__hash__()

colors = {
    Color('Красный','red'),
    Color('Оранжевый','orange'),
    Color('Зелёный','green'),
    Color('Синий','blue'),
    Color('Розовый','pink'),
    Color('Фиолетовый','purple'),
    Color('Белый','white'),
    Color('Чёрный','black'),
    Color('Циан','cyan'),
    Color('Маджента','magenta'),
    Color('Жёлтый','yellow'),
    Color('Серый','gray'),
    Color('Бирюзовый','turquoise'),
    }

class VideoMaker:
    # Ширина символа моноширинного шрифта с кегелем 82 примерно соответствует
    # 50 пикселям (половине ширины картинки)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    @classmethod
    def getfont(cls,italic, bold):
        match italic, bold:
            case True, True:
                return 'courbi.ttf'
            case False, True:
                return 'courbd.ttf'
            case True, False:
                return 'couri.ttf'
            case False, False:
                return 'cour.ttf'
    # https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil
    @classmethod
    def makeImageWithText(cls, text, txtClr, bgClr, italic, bold):
      # Чтобы текст появлялся и исчезал не резко, а уйдя в сторону
      font = ImageFont.truetype(cls.getfont(italic,bold),82)
      text = f'  {text}  '
      if type(bgClr) is str: bgClr = ImageColor.getrgb(bgClr)
      if type(txtClr) is str: txtClr = ImageColor.getrgb(txtClr)
      with Image.new('RGB',(50 * len(text),100),bgClr) as img:
        draw = ImageDraw.Draw(img)
        draw.text((0,0),text,txtClr,font=font)
        # img.save(filename+'.png')
        return img
    
    # https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python
    @classmethod
    def makeVideo(cls, img: Image, seconds: int = 3):
      frames = img.size[0]-99
      video = cv2.VideoWriter("temp.mp4",cls.fourcc,frames/seconds,(100,100))
      for i in range(frames):
        # Для записи кадра видео нужно, чтобы этот кадр был, например,
        # в формате np.ndarray
        # https://stackoverflow.com/questions/384759/how-do-i-convert-a-pil-image-into-a-numpy-array
        # [:, :, ::-1] нужно, чтобы преобразовать BGR в RGB (https://stackoverflow.com/questions/4661557/pil-rotate-image-colors-bgr-rgb)
        frame = np.array(img.crop((i,0,100+i,100)))[:, :, ::-1]
        video.write(frame)
      video.release()
      video_html = cls.play_video()
      os.remove("temp.mp4")
      return video_html
    
    # https://stackoverflow.com/questions/57377185/how-play-mp4-video-in-google-colab
    # Input video path
    @classmethod
    def play_video(cls):
      # Compressed video path
      # compressed_path = os.getcwd()+"\\compressed.mp4"
      compressed_path = "compressed.mp4"
      FFmpeg().input("temp.mp4").output(compressed_path, vcodec="libx264").execute()
      # os.system(f'ffmpeg -i "temp.mp4" -vcodec libx264 "{compressed_path}"')

      # Show video
      with open(compressed_path,'rb') as mp4:
        data_url = "data:video/mp4;base64," + b64encode(mp4.read()).decode()
      os.remove(compressed_path)
      return data_url
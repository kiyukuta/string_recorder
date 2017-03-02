import io
import json
import os
import PIL
from PIL import ImageFont, ImageDraw, Image, ImageColor
import re
import shutil
import subprocess
import sys
import tempfile


colors = ['gray', 'red', 'green', 'yellow',
          'blue', 'magenta', 'cyan', 'white', 'crimson']


reset_code = '\u001b[0m'


def get_font(bold=False):
    font_path = os.path.join(os.path.dirname(__file__), '../fonts',
        'source-han-code-jp-2.000R/OTF/SourceHanCodeJP-Normal.otf')
    if bold:
        font_path = font_path.replace('Normal', 'Bold')
    if not os.path.exists(font_path):
        raise RuntimeError('run `./fonts/install.sh` first')
    return font_path


class StringRecorder(object):

    def __init__(self, font=None, bold_font=None, max_frames=100000):
        self.tmp_dir = tempfile.mkdtemp()
        self.max_frames = max_frames
        if font is None:
            font = get_font()
            bold_font = get_font(bold=True)
        self.font = PIL.ImageFont.truetype(font)
        self.bold_font = PIL.ImageFont.truetype(bold_font)
        self.height = -1
        self.width = -1

        self.tmpdraw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        self._images = []
        self._sizes = []
        self._spacing = 0

        self.reg1 = re.compile(
            '((?:\u001b\[[0-9;]+?m){0,2}.+?(?:\u001b\[0m){0,2})')
        self.reg2 = re.compile(
            '((?:\u001b\[[0-9;]+?m){0,2})(.+?)(?:\u001b\[0m){0,2}')
        self.bg_reg = re.compile('\u001b\[(4[0-9;]+?)m')
        self.fg_reg = re.compile('\u001b\[(3[0-9;]+?)m')

    def __del__(self):
        self._delete_tmp_dir()

    def _delete_tmp_dir(self):
        try:
            shutil.rmtree(self.tmp_dir)
        except:
            pass
        self.tmp_dir = None

    def reset(self):
        self.height = -1
        self.width = -1
        self._images = []
        self._sizes = []

    def render(self, frame):

        splitted = [[w for w in self.reg1.split(l) if w != '']
                    for l in frame.split('\n')]
        parsed = [[self.reg2.findall(c) for c in l] for l in splitted]

        frame = '\n'.join([''.join(c[0][1] for c in l) for l in parsed])
        d = {}
        [[d.update({(row, col): c[0][0]})
          for col, c in enumerate(l) if c[0][0] != ''] for row, l
                                                       in enumerate(parsed)]

        size = self.tmpdraw.textsize(frame, self.font, spacing=self._spacing)
        image = Image.new('RGBA', size, (255,255,255,0))
        draw = ImageDraw.Draw(image, mode='RGBA')

        cw, ch = self.tmpdraw.textsize('A', self.font, spacing=self._spacing)

        for k, v in d.items():
            y, x = k
            background = self.bg_reg.findall(v)

            if background != []:
                assert background[0][0] == '4'
                color = ImageColor.getrgb(colors[int(background[0][1])]) + (0,)
                draw.rectangle((cw * x, ch * y, cw * (x + 1), ch * (y  + 1)),
                               fill=color)
                data = image.load()
                if data[cw * x, ch * y] == (0,0,0,0):
                    raise

        draw.text((0, 0), frame, font=self.font, fill=0, spacing=self._spacing)

        for k, v in d.items():
            y, x = k
            foreground = self.fg_reg.findall(v)
            bold = False

            if foreground != []:
                assert foreground[0][0] == '3'
                color = ImageColor.getrgb(colors[int(foreground[0][1])]) + (0,)
                char = parsed[y][x][0][1]

                font = self.font
                if foreground[0].endswith(';1'):
                    font = self.bold_font
                draw.text((cw * x, ch * y), char, font=font, fill=color,
                          spacing=self._spacing)

        return image, size

    def record_frame(self, frame, speed=None):
        assert type(frame) == str

        image, (width, height) = self.render(frame=frame)

        self._images.append(image)
        if self.width < width:
            self.width = width
        if self.height < height:
            self.height = height

    def make_gif(self, save_path, speed=0.3):
        if not save_path.endswith('.gif'):
            save_path += '.gif'
        size = (self.width, self.height)
        gif = Image.new('RGBA', size, (255, 255, 255))
        images = []
        for img in self._images:
            image = Image.new('RGBA', size, (255, 255, 255))
            image.paste(img, box=(0, 0))
            images.append(image)

        gif.save(save_path, save_all=True,
                 append_images=images, duration=speed * 1000)
        self.reset()

    def make_gif_from_gym_record(self, json_path):
        """convert OpenAI gym's text based video (i.e. ansi mode) to GIF

        """

        with open(json_path) as f:
            record = json.load(f)

        if record['title'] != 'gym VideoRecorder episode':
            raise RuntimeError(
                'Only data from TextEncoder of OpenAI gym is supported.')

        reg_color = re.compile(
            '\u001b\[(?P<color>[0-9;]+?)m(?P<content>.+?)\u001b\[0m')

        for duration, frame in record['stdout']:
            frame = frame.replace('\u001b[2J\u001b[1;1H', '')
            frame = frame.replace('\r', '')
            self.record_frame(frame)

        self.make_gif(json_path.replace('.json', '.gif'))

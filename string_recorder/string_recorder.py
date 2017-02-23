import json
import io
import os
import shutil
import subprocess
import tempfile


class StringRecorder(object):

    def __init__(self, font='Courier', max_frames=100000):
        self.tmp_dir = tempfile.mkdtemp()
        self.max_frames = max_frames
        self.font = font
        self.__frame_t = 0
        self.height = -1
        self.width = -1

    def __del__(self):
        self._delete_tmp_dir()

    def _delete_tmp_dir(self):
        shutil.rmtree(self.tmp_dir)
        self.tmp_dir = None

    def reset(self):
        self._delete_tmp_dir()
        self.tmp_dir = tempfile.mkdtemp()
        self.__frame_t = 0
        self.height = -1
        self.width = -1

    def record_frame(self, frame, speed=None):
        assert type(frame) == str

        output = io.StringIO()
        output.write(frame)

        lines = frame.strip().split('\n')
        width = max([len(l) for l in lines])
        height = len(lines)

        record_path = '{}/{:09d}.png'.format(self.tmp_dir, self.frame_t)

        if self.width < width:
            self.width = width
            self.width_file = record_path
        if self.height < height:
            self.height = height
            self.height_file = record_path

        command = ['convert',
                   '-font',
                   '{}'.format(self.font),
                   'label:{}'.format(output.getvalue()),
                   record_path]

        with subprocess.Popen(command) as proc:
            proc.wait()

        if self.frame_t > 0 and self.frame_t % self.max_frames == 0:
            # if the number of frames are too large.
            tmp = self.frame_t
            self.make_gif('frm{:09d}_{:09d}.gif'.format(
                self.frame_t - self.max_frames, self.frame_t - 1))
            self.__frame_t = tmp

        self.__frame_t += 1

    def get_max_size(self):

        def get(w_or_h, record_path):
            command = ['identify',
                       '-format',
                       '%[fx:{}]'.format(w_or_h),
                       record_path]
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            return proc.stdout.read().decode('utf8')

        w = get('w', self.width_file)
        h = get('h', self.height_file)
        return w, h

    def make_gif(self, save_path, speed=0.3):
        if not save_path.endswith('.gif'):
            save_path += '.gif'

        w, h = self.get_max_size()

        command = ['convert',
                   '-background',
                   'white',
                   '-delay',
                   '{}'.format(int(speed * 100)),
                   '-extent',
                   '{}x{}'.format(w, h),
                   '{}/*.png'.format(self.tmp_dir),
                   save_path]

        with subprocess.Popen(command) as proc:
            proc.wait()
            self.reset()

    def make_gif_from_gym_record(self, json_path):
        """convert OpenAI gym's text based video (i.e. ansi mode) to GIF
        """

        with open(json_path) as f:
            record = json.load(f)

        if record['title'] != 'gym VideoRecorder episode':
            raise RuntimeError(
                'Only data from TextEncoder of OpenAI gym is supported.')

        for duration, frame in record['stdout']:
            frame = frame.replace('\u001b[2J\u001b[1;1H', '')
            frame = frame.replace('\r', '')
            self.record_frame(frame)

        self.make_gif(json_path.replace('.json', '.gif'))

    @property
    def frame_t(self):
        return self.__frame_t

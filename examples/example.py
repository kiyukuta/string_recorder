import string_recorder
import random
rec = string_recorder.StringRecorder()
for i in range(10):
    x = random.randint(0, 5)
    rec.record_frame('{}{}\n{}'.format(i, '>' * x, 'v\n' * x))
rec.make_gif('test.gif')

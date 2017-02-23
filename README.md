# StringRecorder
create GIF animation from sequence of `str`s.

## Requirements
- FreeType
- ImageMagick

install FreeType first.

## Usage

For example, Run this:
```python
import string_recorder
import random
rec = string_recorder.StrRecorder()
for i in range(10):
    x = random.randint(0, 5)
    frame = '{}{}\n{}'.format(i, '>' * x, 'v\n' * x)
    rec.record_frame(frame)
rec.make_gif('test.gif')
```

And you will obtain this GIF:  
![test](test.gif)

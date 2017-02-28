# StringRecorder
create GIF animation from sequence of `str` in python .


## Requirements
- Pango
- FreeType
- ImageMagick

install Pango and FreeType before ImageMagick.


## About font

To make good GIF, we have to specify monospaced font in initializer
(`StringReorder.__init__`).

I found **Courier** for Linux and **Consolas** for Mac are monospaced.
`StringRecorder` will use one of these fonts (according to your OS)
if no font is specified in initializer.


## Usage

For example, Run this code:
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
![test](examples/test.gif)


### Connecting with OpenAI Gym.

You can also use `string_recorder` for the recrod from OpenAI gym.  
Note that the record must be done with `ansi` mode, i.e., 
only text-based environment is allowed.

```python
import subprocess
import re

import gym
from gym.monitoring import VideoRecorder

import string_recorder


env = gym.make('Taxi-v2')
rec = string_recorder.StringRecorder(font='Consolas')   #  <---

#timestep_limit = env.spec.tags.get(
#        'wrapper_config.TimeLimit.max_episode_steps')
timestep_limit = 15

# typical gym loop
for e in range(3):
    out_path = 'records/episode{}.json'.format(e)
    video = VideoRecorder(env, out_path)
    obs = env.reset()

    for t in range(timestep_limit):
        env.render()
        subprocess.call('clear', shell=False)

        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        video.capture_frame()

    video.close()  # record with json format is dumped
    rec.make_gif_from_gym_record(out_path)  # <---
```

By running above code (`examples/example_gym.py`), 
you will obtain three GIF in `records` directory
(episode0.gif, episode1.gif, and episode2.gif) .  

![episode0](examples/records/episode0.gif)


Ofcource, you can directly use `string_recorder` without
`gym.monitering.VideoRecorder` (like the first example):
```
rec = string_recorder.StringRecorder()
# loop
for t in range(timestep_limit):
  frame = env.render(mode='ansi')
  print(frame)
  rec.record_frame(frame)

rec.make_gif('gym_without_videorecoder.gif')
```

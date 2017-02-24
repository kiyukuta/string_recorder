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


### Connecting with OpenAI Gym.

You can also use `string_recorder` with the recrod from OpenAI gym.  
Note that the record must be recorded with `ansi` mode, i.e., 
only text-based environment is allowed.

```python
import gym
from gym.monitering import VideoRecorder
import string_recorder

env = gym.make('some-text-base-envrionment')
rec = string_recorder.StringRecorder()   #  <---

timestep_limit = env.spec.tags.get(
        'wrapper_config.TimeLimit.max_episode_step')

# typical gym loop
for e in range(3):
    out_path = 'records/episode{}.json'.format(e)
    video = VideoRecorder(env, out_path)
    obs = env.reset()

    for t in range(timestep_limit):
        action = env.sample_action()
        obs, reward, done, info = env.step(action)
        video.capture_frame()

    video.close()  # record with json format is dumped
    rec.make_gif_from_gym_record(out_path)  # <---
```

You wilk obtain three GIF in `records` directory (episode0.gif, episode1.gif, and episode2.gif) .

import subprocess
import re

import gym
from gym.monitoring import VideoRecorder

import string_recorder


env = gym.make('FrozenLake-v0')
rec = string_recorder.StringRecorder(font='Consolas')   #  <---

#timestep_limit = env.spec.tags.get(
#        'wrapper_config.TimeLimit.max_episode_steps')
timestep_limit = 10

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

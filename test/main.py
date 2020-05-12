from agent import Agent
from monitor import interact
import gym
import numpy as np
import envs


env = gym.make('CustomEnv-v0')
agent = Agent()
avg_rewards, best_avg_reward = interact(env, agent)

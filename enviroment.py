import gym
#from gym import spaces
import numpy as np
from gym.envs.registration import register


class MyCustomEnv(gym.Env):
    def __init__(self):
        super(MyCustomEnv, self).__init__()
        
        # Define action and observation space
        # They must be gym.spaces objects
        # Example for using discrete actions:
        self.action_space = gym.spaces.Discrete(3)  # Actions: 0 (decrease), 1 (do nothing), 2 (increase)
        
        # Example for using box observations:
        self.observation_space =  gym.spaces.Box(low=np.array([-10]), high=np.array([10]), dtype=np.float32)
        
        # Initial state
        self.state = 0.0
    
    def step(self, action):
        # Execute one time step within the environment
        if action == 0:
            self.state -= 1.0
        elif action == 2:
            self.state += 1.0
        
        # Calculate reward (for example, the reward is higher the closer the state is to zero)
        reward = -abs(self.state)
        
        # Check if the episode is done
        done = abs(self.state) > 10
        
        # Set placeholder for info (optional)
        info = {}
        
        return np.array([self.state]), reward, done, info
    
    def reset(self):
        # Reset the state of the environment to an initial state
        self.state = 0.0
        return np.array([self.state])
    
    def render(self, mode='human'):
        # Render the environment to the screen
        print(f"State: {self.state}")

    def close(self):
        # Clean up resources when the environment is closed
        pass

register(
    id='MyCustomEnv-v0',
    entry_point='path.to.module:MyCustomEnv',
    max_episode_steps=100,  # Optional: Define the max number of steps per episode
)

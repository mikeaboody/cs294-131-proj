import sys
sys.path.append("..")
from ai import Agent
from basic_doom_simulator import create_basic_simulator
from network import blank_network_builder
from abstraction import *
from util import *

config_path = "../sample_config.json"

def run_basic():
	possible_actions = [[1,0,0], [0,1,0], [0,0,1]]
	doom_simulator = create_basic_simulator()
	agent = Agent(config_path, possible_actions, blank_network_builder(len(possible_actions)))
	agent.eps = 0
	img = None
	meas = None
	terminated = None

	i = 0
	while i < 1000:
		if i == 0:
			action_taken = agent.act(training=True)
		else:
			action_taken = agent.act(Observation(img, meas), training=True)
		print(i, action_taken)
		img, meas, _, terminated = doom_simulator.step(action_taken)
		
		if (terminated):
			agent.signal_episode_end()
		else:
			agent.observe(Observation(img, meas), action_taken)
		i += 1

		print(meas)
	doom_simulator.close_game()


def train(num_iterations):
	doom_simulator = create_basic_simulator()
	possible_actions = enumerate_action_one_hots(3)
	agent = Agent(config_path, possible_actions, blank_network_builder(len(possible_actions)))

	#TODO implement decay, delete need for this line
	agent.eps = 0

	img = None
	meas = None
	terminated = None

	i = 0
	while i < num_iterations:
		if i == 0:
			action_taken_one_hot = agent.act(training=True)
		else:
			action_taken_one_hot = agent.act(Observation(img, meas), training=True)
		img, meas, _, terminated = doom_simulator.step(action_from_one_hot(action_taken_one_hot))
		
		if (terminated):
			agent.signal_episode_end()
		else:
			agent.observe(Observation(img, meas), action_taken_one_hot)
		i += 1

	doom_simulator.close_game()


train(1000)

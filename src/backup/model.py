from mesa import Model
from agent import MoneyAgent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


class MoneyModel(Model):
    """A model with some number of agents."""

    def __init__(self, number_agents, width, height):
        self.num_agents = number_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = (
            True  # required by the MESA Model Class to start and stop de simulation
        )

        self.datacollector_currents = DataCollector(
            {
                "Wealthy Agents": MoneyModel.current_wealthy_agents,
                "Non Wealthy Agents": MoneyModel.current_non_wealthy_agents,
            }
        )

        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.datacollector_currents.collect(self)  # passing the model

        if MoneyModel.current_non_wealthy_agents(self) > 20:
            self.running = False

    @staticmethod
    def current_wealthy_agents(model) -> int:
        """Returns the total number of wealthy agents.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return sum([1 for agent in model.schedule.agents if agent.wealth > 0])

    @staticmethod
    def current_non_wealthy_agents(model) -> int:
        """Returns the total number of non wealthy agents.

        Args:
            model (SimulationModel): The model instance.

        Returns:
            (Integer): Number of Agents.
        """
        return sum([1 for agent in model.schedule.agents if agent.wealth == 0])

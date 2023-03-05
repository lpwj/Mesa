from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import MoneyModel
from mesa.visualization.modules import CanvasGrid, ChartModule

NUMBER_OF_CELLS = 80
SIZE_OF_CANVAS_IN_PIXELS_X = 1280
SIZE_OF_CANVAS_IN_PIXELS_Y = 720

simulation_params = {
    "number_agents": UserSettableParameter(
        "slider",
        "Number of agents",
        50,  # default
        10,  # min
        200,  # max
        1,  # step
        description="Choose how many agents to include in the model",
    ),
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
}


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if agent.wealth > 0:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal


grid = CanvasGrid(
    agent_portrayal,
    NUMBER_OF_CELLS,
    NUMBER_OF_CELLS,
    SIZE_OF_CANVAS_IN_PIXELS_X,
    SIZE_OF_CANVAS_IN_PIXELS_Y,
)

chart_wealthy = ChartModule(
    [
        {"Label": "Wealthy Agents", "Color": "green"},
        {"Label": "Non Wealthy Agents", "Color": "red"},
    ],
    canvas_height=300,
    data_collector_name="datacollector_currents",
)


server = ModularServer(
    MoneyModel,
    [grid, chart_wealthy],
    "Money Model",
    simulation_params,
)
server.port = 8521  # The default
server.launch()

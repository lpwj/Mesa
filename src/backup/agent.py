from mesa import Agent
import math

ATTACK_DAMAGE = 50
INITIAL_HEALTH = 100
HEALING_POTION = 20

STRATEGY = 0


def set_agent_type_settings(agent, type):
    if type == 1:
        agent.health = 2 * INITIAL_HEALTH
        agent.attack_damage = 2 * ATTACK_DAMAGE
    if type == 2:
        agent.health = math.ceil(INITIAL_HEALTH / 2)
        agent.attack_damage = math.ceil(ATTACK_DAMAGE / 2)
    if type == 3:
        agent.health = math.ceil(INITIAL_HEALTH / 4)
        agent.attack_damage = ATTACK_DAMAGE * 4


class FightingAgent(Agent):
    """An agent that fights."""

    def __init__(self, unique_id, model, type):
        super().__init__(unique_id, model)
        self.type = type
        self.health = INITIAL_HEALTH
        self.attack_damage = ATTACK_DAMAGE
        self.attacked = False
        self.dead = False
        self.dead_count = 0
        self.buried = False
        set_agent_type_settings(self, type)

    def __repr__(self) -> str:
        return f"{self.unique_id} -> {self.health}"

    def step(self) -> None:
        # buried agents do not move (Do they???? :))
        if self.buried:
            return

        # dead for too long it is buried not being displayed
        if self.dead_count > 4:
            self.buried = True
            return

        # no health and not buried increment the count
        if self.dead and not self.buried:
            self.dead_count += 1
            return

        # when attacked needs one turn until be able to attack
        if self.attacked:
            self.attacked = False
            return

        self.move()

    def attackOrMove(self, cells_with_agents, possible_steps) -> None:

        should_attack = self.random.randint(0, 1)
        if should_attack:
            self.attack(cells_with_agents)
            return

        print("I chose to not attack!")
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def attack(self, cells_with_agents) -> None:

        agentToAttack = self.random.choice(cells_with_agents)
        agentToAttack.health -= self.attack_damage
        agentToAttack.attacked = True
        if agentToAttack.health <= 0:
            agentToAttack.dead = True
        print("I attacked!")

    def move(self) -> None:
        """Handles the movement behavior. Here the agent decides if it moves or attacks other agent."""

        should_take_potion = self.random.randint(0, 100)
        if should_take_potion == 1:
            self.health += HEALING_POTION
            print("Drinking my potion!")
            return

        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )

        cells_with_agents = []
        # looking for agents in the cells around the agent
        for cell in possible_steps:
            otherAgents = self.model.grid.get_cell_list_contents([cell])
            if len(otherAgents):
                for agent in otherAgents:
                    if not agent.dead:
                        cells_with_agents.append(agent)

        # if there is some agent on the
        if len(cells_with_agents):
            if STRATEGY == 1:
                self.attackOrMove(cells_with_agents, possible_steps)
            else:
                self.attack(cells_with_agents)
        else:
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

from __future__ import annotations

from minigrid.core.constants import COLOR_NAMES
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Door, Goal, Key, Lava, Wall
from minigrid.minigrid_env import MiniGridEnv
from minigrid.manual_control import ManualControl

class ParadiseEnv(MiniGridEnv):
    def __init__(
        self,
        size=44,
        agent_start_pos=(18, 6),
        agent_start_dir=0,
        max_steps: int | None = None,
        **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission)

        if max_steps is None:
            max_steps = 4 * size**2

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            see_through_walls=True,
            max_steps=max_steps,
            **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return "grand mission"

    def _gen_grid(self, width, height):
        """
        A 44×44 Minigrid environment with:

        - "PARADISE" across one row (letters at x=[3,8,13,18,23,28,32,37], y=20)
        - A row of lava under each letter (y=26)
        - A 'tree' shape made of lava near the top-left
        - A small 'flame arrow' shape in lava
        - 3 decorative keys
        - Goal at bottom-right
        - Agent near top-left
        """
        # 1) Grid + Outer Walls
        self.grid = Grid(width, height)
        self.grid.wall_rect(0, 0, width, height)

        # 2) Letter-Drawing Helpers (3 wide, 5 tall)
        def draw_p(x, y):
            for xx in range(x, x+3):
                self.grid.set(xx, y, Wall())
            self.grid.set(x+2, y+1, Wall())
            for xx in range(x, x+3):
                self.grid.set(xx, y+2, Wall())
            for yy in range(y, y+5):
                self.grid.set(x, yy, Wall())

        def draw_a(x, y):
            for xx in range(x, x+3):
                self.grid.set(xx, y, Wall())
            for yy in range(y+1, y+5):
                self.grid.set(x, yy, Wall())
                self.grid.set(x+2, yy, Wall())
            for xx in range(x, x+3):
                self.grid.set(xx, y+2, Wall())

        def draw_r(x, y):
            for xx in range(x, x+3):
                self.grid.set(xx, y, Wall())
            self.grid.set(x+2, y+1, Wall())
            for xx in range(x, x+3):
                self.grid.set(xx, y+2, Wall())
            for yy in range(y, y+5):
                self.grid.set(x, yy, Wall())
            self.grid.set(x+1, y+3, Wall())
            self.grid.set(x+2, y+4, Wall())

        def draw_d(x, y):
            for yy in range(y, y+5):
                self.grid.set(x, yy, Wall())
            for xx in range(x, x+3):
                self.grid.set(xx, y, Wall())
                self.grid.set(xx, y+4, Wall())
            for yy in range(y+1, y+4):
                self.grid.set(x+2, yy, Wall())

        def draw_i(x, y):
            for yy in range(y, y+5):
                self.grid.set(x, yy, Wall())

        def draw_s(x, y):
            for xx in range(x, x+3):
                self.grid.set(xx, y, Wall())
            self.grid.set(x, y+1, Wall())
            for xx in range(x, x+3):
                self.grid.set(xx, y+2, Wall())
            self.grid.set(x+2, y+3, Wall())
            for xx in range(x, x+3):
                self.grid.set(xx, y+4, Wall())

        def draw_e(x, y):
            for xx in range(x, x+3):
                self.grid.set(xx, y, Wall())
            for yy in range(y, y+5):
                self.grid.set(x, yy, Wall())
            for xx in range(x, x+3):
                self.grid.set(xx, y+2, Wall())
            for xx in range(x, x+3):
                self.grid.set(xx, y+4, Wall())

        # 3) Draw "PARADISE" 
        letter_positions = [3, 8, 13, 18, 23, 28, 31, 36]
        letter_draw_funcs = [draw_p, draw_a, draw_r, draw_a, draw_d, draw_i, draw_s, draw_e]
        base_y = 20

        for fn, xPos in zip(letter_draw_funcs, letter_positions):
            fn(xPos, base_y)

        # 4) Lava row under each letter
        lava_y = 26
        for xPos in letter_positions:
            self.grid.set(xPos, lava_y, Lava())


        # 7) Three decorative keys
        self.put_obj(Key("yellow"), 20, 6)
        self.put_obj(Key("blue"),   20, 15)
        self.put_obj(Key("purple"), 35, 12)

        # 8) Goal in bottom-right
        self.put_obj(Goal(), 25, 6)

        # Lava walls around the goal
        self.grid.set(22, 5, Lava())
        self.grid.set(22, 6, Lava())
        self.grid.set(20, 7, Lava())
        self.grid.set(19, 8, Lava())
        self.grid.set(18, 9, Lava())
        self.grid.set(17, 9, Lava())
        self.grid.set(17, 10, Lava())
        self.grid.set(17, 11, Lava())
        # Door
        self.grid.set(21, 7, Door(COLOR_NAMES[5], is_locked=True))

        # 9) Agent near top-left
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        self.mission = "grand mission"


def main():
    env = ParadiseEnv(render_mode="human")
    manual_control = ManualControl(env, seed=42)
    manual_control.start()


if __name__ == "__main__":
    main()

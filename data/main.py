from . import tools, prepare
from .states import title_screen, sim


def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"TITLE": title_screen.TitleScreen(),
                   "SIM": sim.SpaceSim()}
    controller.setup_states(states, "TITLE")
    controller.main()

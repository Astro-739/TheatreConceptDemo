from create_theatre import Theatre



class TheatreCommander:
    def __init__(self) -> None:
        self.own_assets = []
        self.enemy_assets = []
        self.targets = []
        # behaviour
        # take high (+1) or low (-1) risks
        self.take_risk = 1
        # offensive (+1) or defensive (-1) posture
        self.posture = -1
        # prioritise military (+1) or economical (-1) targets
        self.priority = 1
        
        
        pass
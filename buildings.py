class Buildings:
    def _init_(self, cost: int, time_building: float, health: int, surface: int, spawn: 'Unity', drop_point: bool):
        self.cost = cost
        self.time_building = time_building
        self.health = health
        self.surface = surface
        self.spawn = spawn
        self.drop_point = drop_point


    def build(self, builders_list: list):
        total_build_speed = sum([builder.building_speed for builder in builders_list])
        build_time_remaining = self.time_building

        while build_time_remaining > 0:
            build_time_remaining -= total_build_speed

        print("Building completed!")

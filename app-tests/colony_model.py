from datetime import datetime, timedelta

from . import MyTestCase, Colony, constructions, tools


class ColonyModelTests(MyTestCase):

    # Check end of build
    def test_end_construction(self):

        colony = Colony.query.first()
        _buildings = colony.buildings.get_buildings()
        _resources = colony.resources.get_resources()
        sawmill = constructions.Sawmill(level=1)

        sawmill.start_build = datetime.today() - sawmill.time_build - timedelta(minutes=1)
        colony.construction_list = [sawmill]
        colony.update()

        buildings = colony.buildings.get_buildings()
        resources = colony.resources.get_resources()

        self.assertFalse(colony.construction_list)
        self.assertNotEqual(_buildings, buildings)
        self.assertNotEqual(_resources, resources)


    # Check end of craft
    def test_end_craft(self):

        colony = Colony.query.first()
        _amount = colony.resources.saw
        saw = tools.Saw()
        saw.start_build = datetime.today() - saw.time_build - timedelta(minutes=1)
        colony.craft = saw

        colony.update()
        amount = colony.resources.saw

        self.assertFalse(colony.craft)
        self.assertNotEqual(_amount, amount)


    # Check end of active tool
    def test_end_active_tool(self):

        colony = Colony.query.first()
        saw = tools.Saw()
        saw.start_active = datetime.today() - saw.time_active - timedelta(minutes=1)
        colony.active_tool = saw
        colony.update()

        self.assertFalse(colony.active_tool)


    # Check production status
    def test_production(self):

        colony = Colony.query.first()
        _resources = colony.resources.get_resources()
        colony.buildings.sawmill = 1

        # Update production
        colony.update()
        resources = colony.resources.get_resources()
        self.assertNotEqual(_resources, resources)

        # Add resources
        colony.last_update = datetime.today() - timedelta(hours=1)
        _resources = resources
        colony.update()
        resources = colony.resources.get_resources()
        self.assertNotEqual(_resources, resources)

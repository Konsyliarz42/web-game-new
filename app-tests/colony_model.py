from datetime import datetime, timedelta

from . import MyTestCase, Colony, constructions, tools, soldiers


class ColonyModelTests(MyTestCase):

    # Check end of build
    def test_end_construction(self):

        colony = Colony.query.first()
        _buildings = colony.buildings.get_buildings()
        _resources = colony.resources.get_resources()
        _rapports = colony.rapports.copy()
        sawmill = constructions.Sawmill(level=1)

        sawmill.start_build = datetime.today() - sawmill.time_build - timedelta(minutes=1)
        colony.construction_list = [sawmill]
        colony.update()

        buildings = colony.buildings.get_buildings()
        resources = colony.resources.get_resources()
        rapports = colony.rapports

        self.assertFalse(colony.construction_list)
        self.assertNotEqual(_buildings, buildings)
        self.assertNotEqual(_resources, resources)
        self.assertNotEqual(_rapports, rapports)
        self.assertEqual(rapports[-1].category, 'build')
        self.assertEqual(rapports[-1].content, {'sawmill': 1})


    # Check end of craft
    def test_end_craft(self):

        colony = Colony.query.first()
        _amount = colony.resources.saw
        _rapports = colony.rapports.copy()
        saw = tools.Saw()
        saw.start_build = datetime.today() - saw.time_build - timedelta(minutes=1)
        colony.craft = saw

        colony.update()
        amount = colony.resources.saw
        rapports = colony.rapports

        self.assertFalse(colony.craft)
        self.assertNotEqual(_amount, amount)
        self.assertNotEqual(_rapports, rapports)
        self.assertEqual(rapports[-1].category, 'craft')
        self.assertEqual(rapports[-1].content, 'saw')


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
        _rapports = colony.rapports.copy()
        colony.update()
        resources = colony.resources.get_resources()
        rapports = colony.rapports
        self.assertNotEqual(_resources, resources)
        self.assertNotEqual(_rapports, rapports)
        self.assertEqual(rapports[-1].category, 'production')
        self.assertEqual(int(rapports[-1].content['wood']), int(constructions.Sawmill(level=1).production['wood']))


    # Check end of training
    def test_end_training(self):

        colony = Colony.query.first()
        _army = colony.army.get_army()
        _rapports = colony.rapports.copy()
        swordman = soldiers.Swordman()
        swordman.start_training = datetime.today() - swordman.time_training - timedelta(minutes=1)
        colony.training = [swordman]

        colony.update()
        army = colony.army.get_army()
        rapports = colony.rapports
        self.assertFalse(colony.training)
        self.assertNotEqual(_army, army)
        self.assertNotEqual(_rapports, rapports)
        self.assertEqual(rapports[-1].category, 'training')
        self.assertEqual(rapports[-1].content, {'swordman': 1})
        
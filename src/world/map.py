from math import ceil
import random
from entity.apple import Apple
from entity.bear import Bear
from entity.chicken import Chicken
from lib.graphik.src.graphik import Graphik
from entity.rock import Rock
from entity.wood import Wood
from lib.pyenvlib.entity import Entity
from entity.grass import Grass
from entity.leaves import Leaves
from world.room import Room


# @author Daniel McCoy Stephenson
# @since August 15th, 2022
class Map:
    def __init__(self, gridSize, graphik: Graphik):
        self.rooms = []
        self.gridSize = gridSize
        self.graphik = graphik
        self.spawnRoom = self.generateNewRoom(0, 0)
    
    def getRooms(self):
        return self.rooms
    
    def getRoom(self, x, y):
        for room in self.getRooms():
            if room.getX() == x and room.getY() == y:
                return room
        return -1
    
    def getSpawnRoom(self):
        return self.spawnRoom

    def getLocation(self, entity: Entity, room: Room):
        locationID = entity.getLocationID()
        grid = room.getGrid()
        return grid.getLocation(locationID)

    def generateNewRoom(self, x, y):
        newRoomColor = ((random.randrange(200, 210), random.randrange(130, 140), random.randrange(60, 70)))
        newRoom = Room(("(" + str(x) + ", " + str(y) + ")"), self.gridSize, newRoomColor, x, y, self.graphik)

        # generate grass
        self.spawnGrass(newRoom)

        # generate food
        maxTrees = ceil(self.gridSize/3)
        for i in range(0, maxTrees):
            self.spawnTree(newRoom)

        # generate rocks
        self.spawnRocks(newRoom)

        # generate chickens
        self.spawnChickens(newRoom)

        # generate bears
        self.spawnBears(newRoom)

        self.rooms.append(newRoom)
        return newRoom

    def spawnGrass(self, room: Room):
        for locationId in room.getGrid().getLocations():
            location = room.getGrid().getLocation(locationId)
            if random.randrange(1, 101) > 5: # 95% chance
                room.addEntityToLocation(Grass(), location)
    
    def spawnRocks(self, room: Room):
        for locationId in room.getGrid().getLocations():
            location = room.getGrid().getLocation(locationId)
            if random.randrange(1, 101) == 1: # 1% chance
                room.addEntityToLocation(Rock(), location)

    def spawnTree(self, room: Room):
        wood = Wood()
        room.addEntity(wood)

        location = self.getLocation(wood, room)

        locationsToSpawnApples = []
        locationsToSpawnApples.append(room.grid.getUp(location))
        locationsToSpawnApples.append(room.grid.getLeft(location))
        locationsToSpawnApples.append(room.grid.getDown(location))
        locationsToSpawnApples.append(room.grid.getRight(location))
        
        # spawn leaves and apples around the tree
        for appleSpawnLocation in locationsToSpawnApples:
            if appleSpawnLocation == -1 or self.locationContainsEntityType(appleSpawnLocation, Wood):
                continue
            room.addEntityToLocation(Leaves(), appleSpawnLocation)
            if random.randrange(0, 2) == 0:
                room.addEntityToLocation(Apple(), appleSpawnLocation)
    
    def spawnChickens(self, room: Room):
        for i in range(0, 5):
            if random.randrange(1, 101) > 75: # 25% chance
                newChicken = Chicken()
                room.addEntity(newChicken)
                room.addLivingEntity(newChicken)
    
    def spawnBears(self, room: Room):
        for i in range(0, 2):
            if random.randrange(1, 101) > 90: # 10% chance
                newBear = Bear()
                room.addEntity(newBear)
                room.addLivingEntity(newBear)

    def locationContainsEntityType(self, location, entityType):
        for entityId in location.getEntities():
            entity = location.getEntity(entityId)
            if isinstance(entity, entityType):
                return True
        return False
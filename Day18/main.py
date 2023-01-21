# too low 2496
# 2505 is wrong :(

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from voxelLoader import *

app = Ursina()


def floodFill(v):
    count = 0
    for x in range(v.maxx):
        for y in range(v.maxy):
            for z in range(v.maxz):
                # is this a space? if so check to see if its surrounded
                # by rock - if so we need to fill to mark it as flood filled
                if v.space[x][y][z] == '.': #or v.space[x][y][z] == 'o':
                    count = checkForFF(v, x, y, z)
                    if count == 6:
                        v.space[x][y][z] = 'o'
                        print("checking...{} ".format([x, y, z]), end='')
                        print("[FILLING]", end='')
                        print(count)


def checkForFF(v, x, y, z):
    count = 0

    # search to see how in how many directions we hit a rock
    # if we hit rock in all directions then we're "inside" and we should
    # fill the space

    for i in range(x+1, v.maxx):
        if v.space[i][y][z] == '#':
            count += 1
            break

    for i in range(x-1, -1, -1):
        if v.space[i][y][z] == '#':
            count += 1
            break

    for i in range(y+1, v.maxy):
        if v.space[x][i][z] == '#':
            count += 1
            break

    for i in range(y-1, -1, -1):
        if v.space[x][i][z] == '#':
            count += 1
            break

    for i in range(z+1, v.maxz):
        if v.space[x][y][i] == '#':
            count += 1
            break

    for i in range(z-1, -1, -1):
        if v.space[x][y][i] == '#':
            count += 1
            break

    return count


def clearErrors(v):

    error=True

    while error==True:
        error=False
        
        for x in range(v.maxx):
            for y in range(v.maxy):
                for z in range(v.maxz):
                    if v.space[x][y][z] == 'o':
                        if checkVoxelP2Faces(v, x, y, z)>0:
                            print("Clearing error at:{}".format([x,y,z]))
                            v.space[x][y][z] = '.'
                            error=True

def checkAllVoxels(v):
    count = 0
    error =0
    for x in range(v.maxx):
        for y in range(v.maxy):
            for z in range(v.maxz):
                if v.space[x][y][z] == '#':
                    count += checkVoxelP2Faces(v, x, y, z)
                elif v.space[x][y][z] == 'o':
                    if checkVoxelP2Faces(v, x, y, z)>0:
                        error+=1

    print("error:{}".format(error))
    return count


def checkVoxelP2Faces(v, x, y, z):
    count = 0

    # check each voxel in the x plane postive and negative to see if this is "inside" or "outside"

    # is there an air pocket next to us?
    if v.space[x+1][y][z] == '.':
        count += 1
    if v.space[x-1][y][z] == '.':
        count += 1
    if v.space[x][y+1][z] == '.':
        count += 1
    if v.space[x][y-1][z] == '.':
        count += 1
    if v.space[x][y][z+1] == '.':
        count += 1
    if v.space[x][y][z-1] == '.':
        count += 1

    return count


# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.

class Floor(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.blue,
        )


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), c=color.red):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            scale=(0.5, 0.5, 0.5),
            color=c,
            highlight_color=color.blue,
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                #voxel = Voxel(position=self.position + mouse.normal)
                destroy(self)

            if key == 'right mouse down':
                destroy(self)


v = VoxelLoader('Day18/data/input.txt')
v.loadFile()
v.parseFile()

floodFill(v)
clearErrors(v)
count = checkAllVoxels(v)
v.printVoxels()


for z in range(15):
    for x in range(15):
        floor = Floor(position=(x, 0, z))

for x in range(v.maxx):
    for y in range(v.maxy):
        for z in range(v.maxz):
            if v.space[x][y][z] == '#':
                voxel = Voxel(position=(x/2, (y/2)+(v.maxy/4), z/2), c=color.green)
                pass
            elif v.space[x][y][z] == 'o':
                voxel = Voxel(position=(x/2, (y/2)+(v.maxy/4), z/2), c=color.red)




print("P2 Answer: {}".format(count))
# for i in range(10,0,-1):
#     print(i)

# print()
# for i in range(2,10):
#     print(i)


# def input(key):
#     if key == 'left mouse down':
#         hit_info = raycast(camera.world_position, camera.forward, distance=5)
#         if hit_info.hit:
#             Voxel(position=hit_info.entity.position + hit_info.normal)


player = FirstPersonController()
app.run()

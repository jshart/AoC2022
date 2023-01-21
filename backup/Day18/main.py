'''
Disclaimer: This solution is not scalable for creating a big world.
Creating a game like Minecraft requires specialized knowledge and is not as easy
to make as it looks.
You'll have to do some sort of chunking of the world and generate a combined mesh
instead of separate blocks if you want it to run fast. You can use the Mesh class for this.
You can then use blocks with colliders like in this example in a small area
around the player so you can interact with the world.
'''

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from voxelLoader import *

app = Ursina()


def floodFill(v):
    count = 0
    for x in range(v.maxx):
        for y in range(v.maxy):
            for z in range(v.maxz):
                if v.space[x][y][z] == '.':
                    count += checkForFF(v, x, y, z)
                    if count == 4:
                        v.space[x][y][z] = 'o'

    return count


def checkForFF(v, x, y, z):
    count = 0

    # is there an air pocket next to us?
    if v.space[x+1][y][z] == '.' or v.space[x+1][y][z] == 'o':
        for i in range(x+1, v.maxx):
            if v.space[i][y][z] == '#':
                break
        else:
            count += 1

    if v.space[x-1][y][z] == '.' or v.space[x-1][y][z] == 'o':
        for i in range(x-1, -1, -1):
            if v.space[i][y][z] == '#':
                break
        else:
            count += 1

    # is there an air pocket next to us?
    if v.space[x][y+1][z] == '.' or v.space[x][y+1][z] == 'o':
        for i in range(y+1, v.maxy):
            if v.space[x][i][z] == '#':
                break
        else:
            count += 1

    if v.space[x][y-1][z] == '.' or v.space[x][y-1][z] == 'o':
        for i in range(y-1, -1, -1):
            if v.space[x][i][z] == '#':
                break
        else:
            count += 1

    # is there an air pocket next to us?
    if v.space[x][y][z+1] == '.' or v.space[x][y][z+1] == 'o':
        for i in range(z+1, v.maxz):
            if v.space[x][y][i] == '#':
                break
        else:
            count += 1

    # is there an air pocket next to us?
    if v.space[x][y][z-1] == '.' or v.space[x][y][z]-1 == 'o':
        for i in range(z-1, -1, -1):
            if v.space[x][y][i] == '#':
                break
        else:
            count += 1

    return count


def checkAllVoxels(v):
    count = 0
    for x in range(v.maxx):
        for y in range(v.maxy):
            for z in range(v.maxz):
                if v.space[x][y][z] == '#':
                    count += checkVoxelP2Faces(v, x, y, z)

    return count


def checkVoxelP2Faces(v, x, y, z):
    count = 0

    # check each voxel in the x plane postive and negative to see if this is "inside" or "outside"

    # is there an air pocket next to us?
    if v.space[x+1][y][z] == '.':
        for i in range(x+1, v.maxx):
            if v.space[i][y][z] == '#':
                break
        else:
            count += 1
    # else:
    #     count += 1

    if v.space[x-1][y][z] == '.':
        for i in range(x-1, -1, -1):
            if v.space[i][y][z] == '#':
                break
        else:
            count += 1
    # else:
    #     count += 1

    # is there an air pocket next to us?
    if v.space[x][y+1][z] == '.':
        for i in range(y+1, v.maxy):
            if v.space[x][i][z] == '#':
                break
        else:
            count += 1
    # else:
    #     count += 1

    if v.space[x][y-1][z] == '.':
        for i in range(y-1, -1, -1):
            if v.space[x][i][z] == '#':
                break
        else:
            count += 1
    # else:
    #     count += 1

    # is there an air pocket next to us?
    if v.space[x][y][z+1] == '.':
        for i in range(z+1, v.maxz):
            if v.space[x][y][i] == '#':
                break
        else:
            count += 1
    # else:
    #     count += 1

    # is there an air pocket next to us?
    if v.space[x][y][z-1] == '.':
        for i in range(z-1, -1, -1):
            if v.space[x][y][i] == '#':
                break
        else:
            count += 1
    # else:
    #     count += 1

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
            highlight_color=color.lime,
        )


class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            scale=(0.5, 0.5, 0.5),
            color=color.light_gray,
            highlight_color=color.lime,
        )

    # def input(self, key):
    #     if self.hovered:
    #         if key == 'left mouse down':
    #             voxel = Voxel(position=self.position + mouse.normal)
    #
    #         if key == 'right mouse down':
    #             destroy(self)


v = VoxelLoader('Day18/data/input_test.txt')
v.loadFile()
v.parseFile()
v.printVoxels()

for z in range(15):
    for x in range(15):
        floor = Floor(position=(x, 0, z))

for x in range(v.maxx):
    for y in range(v.maxy):
        for z in range(v.maxz):
            if v.space[x][y][z] == '#':
                voxel = Voxel(position=(x/2, (y/2)+(v.maxy/4), z/2))

count = checkAllVoxels(v)

print("P2 Answer: {}".format(count))
# for i in range(10,0,-1):
#     print(i)

# print()
# for i in range(2,10):
#     print(i)


def input(key):
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal)


player = FirstPersonController()
app.run()

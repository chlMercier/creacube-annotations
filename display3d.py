from vpython import *
from configurations import CONFIGURATIONS
import argparse

cubes = {}
cube_size = 4

def init(scene):
  global cubes

  scene.background = color.gray(0.8)
  scene.camera.rotate(angle=1.2, axis=vector(1,0,0), origin=vector(0,0,0))
  scene.camera.rotate(angle=2, axis=vector(0,0,1), origin=vector(0,0,0))

  scene.title = "Visualize CreaCube configurations in 3D"

  scene.append_to_caption("""
  To rotate "camera", ctrl-drag with the mouse.
  To zoom, use scroll wheel (or pinch/extend on touch screens).""")

  # wheels (white)
  cubeW = box(color=color.white, pos=vector(0,0,0), length=cube_size, height=cube_size, width=cube_size, opacity=1)
  # inverter (red)
  cubeI = box(color=color.red, pos=vector(cube_size + 2,0,0), length=cube_size, height=cube_size, width=cube_size, opacity=1)
  # battery (blue)
  cubeB = box(color=color.blue, pos=vector(cube_size + 2,cube_size + 2,0), length=cube_size, height=cube_size, width=cube_size, opacity=1)
  # sensor(black)
  cubeS = box(color=color.black, pos=vector(0,cube_size + 2,0), length=cube_size, height=cube_size, width=cube_size, opacity=1)

  cubes = {
    "W": cubeW,
    "S": cubeS,
    "B": cubeB,
    "I": cubeI
  }

  return cubes

def get_orientation_vector(orientation):
  if orientation == 'x':
    return cube_size * vector(1,0,0)
  elif orientation == 'y':
    return cube_size * vector(0,1,0)
  elif orientation == 'z':
    return cube_size * vector(0,0,1)
  else:
    print("unknown orientation")
    return vector(0,0,0)

# a brick can be either a cube or a structure of 2,3,4 cubes
def connect(brick1,brick2,orientation, pos1, pos2):
  brick2.pos = brick2.pos + (pos1-pos2) + get_orientation_vector(orientation)
  brick = compound([brick1,brick2])
  return brick

theta=0.1
framerate=20

def display(config):
  global cubes

  bricks = {}
  connections = [conn for conn in CONFIGURATIONS[config].keys()]
  print(connections)
  for connection in connections[1:]:
    cube1,orientation,cube2 = tuple(connection)
    brick1 = cubes[cube1]
    brick2 = cubes[cube2]
    if cube1 in bricks:
      brick1 = bricks[cube1]
    if cube2 in bricks:
      brick2 = bricks[cube2]
    brick = connect(brick1,brick2,orientation, cubes[cube1].pos, cubes[cube2].pos)
    bricks[cube1] = brick
    bricks[cube2] = brick
    cubes[cube2].pos = cubes[cube1].pos + get_orientation_vector(orientation)
    for cube,old_brick in bricks.items():
      if (old_brick == brick1 or old_brick == brick2):
        bricks[cube] = brick
        if old_brick == brick2 and (not cube == cube2):
          cubes[cube].pos = cubes[cube].pos + (cubes[cube1].pos - cubes[cube2].pos) + get_orientation_vector(orientation)
    #print("Cubes coordinates:")
    # for cube, obj in cubes.items():
    #   print(f"cube {cube}: {obj.pos}")
    print(bricks)

def mainloop(cubeconfig):
  while True:
    rate(framerate)
    cubes = init(scene)
    scene.pause("Click to connect")
    display(cubeconfig)
    scene.pause("Click to exit")
    scene.delete()

# Command line use
def parse():
  parser = argparse.ArgumentParser(description='Display a cube configuration in 3D')
  parser.add_argument('-cc', '--cubeconfig', metavar='"Fxxx-xxxx"', type=str, help='the code of the cube configuration to display')
  args = parser.parse_args()
  if args.cubeconfig is not None:
    print(args.cubeconfig)
    mainloop(args.cubeconfig)

#parse()
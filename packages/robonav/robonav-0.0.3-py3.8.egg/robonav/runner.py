from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
from robonav.robot import Robot

def navigator(debug=False):

    this_folder = dirname(__file__)

    robot_mm = metamodel_from_file(join(this_folder, 'robot.tx'), debug=False)

    robot_model = robot_mm.model_from_file(join(this_folder, 'program.rbt'))

    robot = Robot(robot_model)
    robot.interpret()


# if __name__ == "__main__":
#     navigator()

"""
This file run the cryoloBM project. Its structure is based on the model-view-controller design pattern for theoretical
info visit https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
It contains also  a parser for collecting data from CLI and the 'start_boxmanager' function, which create the object for
 the model-view-controller design pattern
"""


from cryoloBM import helper,boxmanager_view,boxmanager_controller,boxmanager_model,helper_GUI
from sys import argv as sys_argv

def start_boxmanager(image_dir:str, box_dir:str, wildcard:str, is_tomo:bool)->None:
    app = helper_GUI.QtG.QApplication(sys_argv)
    view = boxmanager_view.Boxmanager_view(font=app.font())
    model = boxmanager_model.Boxmanager_model(image_dir=image_dir, box_dir=box_dir, wildcard=wildcard, is_tomo=is_tomo)
    c = boxmanager_controller.Boxmanager_controller(view=view, model=model, app=app)
    c.run()

def run()->None:
    # collect args from cli
    args = helper.create_parser().parse_args()

    start_boxmanager(args.image_dir, args.box_dir, args.wildcard, is_tomo=args.is_tomo)


if __name__ == "__main__":
    run()

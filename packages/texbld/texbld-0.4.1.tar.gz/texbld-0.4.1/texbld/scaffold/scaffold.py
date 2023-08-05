import os
from texbld.common.image import Image
from texbld.config import PROJECT_CONFIG_FILE
from texbld.scaffold.copy import copy_image
from texbld.scaffold.project import project_toml_gen
from texbld.common.solver import Solver
import texbld.logger as logger


def scaffold_project(image: Image, directory: str):
    directory = os.path.abspath(directory)
    name = os.path.basename(directory)
    if os.path.exists(directory):
        raise FileExistsError(directory)
    os.makedirs(directory)
    for img in reversed(Solver(image).images()):
        if not img.is_base():
            logger.progress("copying image", img.package_dir())
            copy_image(img, directory)
            logger.done("copied", img.package_dir())
    configpath = os.path.join(directory, PROJECT_CONFIG_FILE)
    with open(configpath, "w") as w:
        w.write(project_toml_gen(name, image))


def scaffold_image(directory: str):
    directory = os.path.abspath(directory)
    name = os.path.basename(directory)
    if os.path.exists(directory):
        raise FileExistsError(directory)
    os.makedirs(directory)
    src_path = os.path.join(os.path.dirname(__file__), "sample_image.toml")
    text = open(src_path).read()
    open(os.path.join(directory, "image.toml"), "w").write(
        text.replace("image_name", name))

from diagrams import Node
import os

cwd = os.getcwd()

class OnPremExtension(Node):
    _provider = "onprem"
    _icon_dir = cwd + '/extensions/images'
    fontcolor = "#ffffff"

class Scheduler(OnPremExtension):
    _icon = "scheduler-1.png"

class DockerNodejs(OnPremExtension):
    _icon = "nodejs-docker.png"
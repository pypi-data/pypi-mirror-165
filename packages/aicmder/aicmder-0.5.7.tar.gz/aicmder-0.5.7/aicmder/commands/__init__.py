from aicmder.commands.utils import register, get_command, execute, _commands


import aicmder.commands.fastai
import aicmder.commands.help
import aicmder.commands.utils
import aicmder.commands.version
import aicmder.commands.init
try:
    import aicmder.commands.onnx
    import aicmder.commands.pb
except:
    pass
import aicmder.commands.serve
import aicmder.commands.stop
import aicmder.commands.extract
import aicmder.commands.power 
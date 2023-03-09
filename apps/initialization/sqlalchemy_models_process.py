from entities.entities import *

"""解决循环引用问题
TODO:纯纯多此一举,为了显得结构更清晰一些,需要显示引用后才能被迁移到

db->sqlalchemy_process->entities->models->services
                        entities->sqlalchemy_models_process->__init__
"""


def init_sqlalchemy_models():
    pass

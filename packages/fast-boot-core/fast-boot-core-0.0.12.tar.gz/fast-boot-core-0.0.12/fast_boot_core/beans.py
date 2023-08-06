from typing import Dict, Callable


class Beans:
    MSG_TEMPLATE: Dict = None
    SESSION_DEPENDENCY: Callable = None

    @staticmethod
    def init_beans(
            msg_templates: Dict,
            session_dependency
    ):
        Beans.MSG_TEMPLATE = msg_templates
        Beans.SESSION_DEPENDENCY = session_dependency

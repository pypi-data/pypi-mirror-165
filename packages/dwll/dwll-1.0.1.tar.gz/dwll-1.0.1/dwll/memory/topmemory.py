from dwll.memory import memory
from dwll.memory import constants as C

class TopMemory(memory.Memory):

    """

    Top Memory
    ===================

    Description
        Helper/Manager que funciona como especializacion de Memory
        para proceder con limpiezas de memoria escalares.

    """

    def clean_by_step(self, request, step=C.MAIN):
        """

        Clean By Step

        Description
            Limpia la memoria por pasos, la limpieza des pasos iniciales
            hace que los posteriores pasos tambien sean limpiados.

        :param request:
        :param step:
        :return:
        """

        if step == C.MAIN:
            self.clean_main(request)

    def clean_main(self, request):
        """

        Clean Step 0

        Description
            Limpieza paso 0 (HOME)

        :param request:
        :return:
        """
        self.clean(request, C.MAIN)

top = TopMemory()
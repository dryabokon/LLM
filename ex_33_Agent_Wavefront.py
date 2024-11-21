# ----------------------------------------------------------------------------------------------------------------------
from LLM2 import llm_interaction,llm_Agent_Wavefront
import tools_GL_creator
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_OBJ/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
U = tools_GL_creator.OBJ_Utils(folder_out)
# ----------------------------------------------------------------------------------------------------------------------
def create_examples():
    U.test_01_plane()
    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_offline():

    A = llm_Agent_Wavefront.Agent_Wavefront(folder_in, folder_out)

    q = 'Create ground plane. Add cube of scale 1 shifted left 10 and evevated 20 above the ground. Add Pyramid of scale 2 shifted forward 30 and elevated on 5 above the ground.'
    # q = ('Create ground plane. '
    #      'Add cube of scale 3 shifted left 1 and elevated 20 above the ground. '
    #      'Add Pyramid of scale 4 shifted forward 30 and elevated on 5 above the ground. '
    #      'Add Tetrahedron of scale 2 shifted right 10 and elevated 20 above the ground.')
    llm_interaction.interaction_offline(A, [q], do_debug=True, do_spinner=True)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_agent_live():
    A = llm_Agent_Wavefront.Agent_Wavefront()
    llm_interaction.interaction_live(A, do_debug=True,do_spinner=False)
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #create_examples()
    ex_agent_offline()


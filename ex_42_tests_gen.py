from halo import Halo
import warnings
warnings.filterwarnings( 'ignore', module = 'langchain_core' )
from LLM2 import llm_Asistant_OPENAI
from LLM2 import llm_interaction
# ----------------------------------------------------------------------------------------------------------------------
folder_out = './tests/'
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_offline(A,query,filename_in,assistant_id=None):
    file = A.client.files.create(file=open(filename_in, 'rb'), purpose='assistants')
    do_cleanup = False

    if assistant_id is None:
        assistant_id = A.create_assistant_book_reader(file.id)
        A.assistant_id = assistant_id
        do_cleanup = True

    llm_interaction.interaction_offline(A,query,do_debug=False,do_spinner=True)

    if do_cleanup:
        A.delete_assistant(assistant_id)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_live(A,filename_in=None,assistant_id=None):
    do_cleanup = False
    if assistant_id is None:
        assistant_id = A.create_assistant_book_reader(A.client.files.create(file=open(filename_in, 'rb'), purpose='assistants').id)
        do_cleanup = True

    should_be_closed = False

    while not should_be_closed:

        print('\033[92m'+'>'+'\033[0m',end='')
        q = input()
        if len(q)==0:
            should_be_closed = True

        try:
            res = A.Q_assistant(q,assistant_id=assistant_id)
        except:
            res = 'Error'

        res = A.pretify_string(res)
        print(res)
        print(''.join(['='] * 20))

    if do_cleanup:
        A.delete_assistant(assistant_id)
    return
# ----------------------------------------------------------------------------------------------------------------------
queries_GF = [ 'What was the favorite horse of the movie producer and passionate about racing?',
            'How Sonny was killed ?',
            'What is Mike\'s hobby?',
            'Name 5 families of NY mafia',
            'Name all Casinos mentioned in the book',
            'Name the favorite horse of the Hollywood producer',
            'Who is Amerigo Bonasera?']
# ----------------------------------------------------------------------------------------------------------------------
def ex_code_unit_test(A,filename_in, function_name, folder_out,filename_example=None):
    do_cleanup = False

    file_id = A.client.files.create(file=open(filename_in, 'rb'), purpose='assistants').id
    assistant_id = A.create_assistant_code_analyzer([file_id])
    example =''
    if filename_example is not None:
        example = open(filename_example).read()
        example ='\nTake below as an example: \n'+example+'\n'

    # 'Boundary Tests', 'Edge Cases', 'Data Type Tests', 'Corner Cases', 'Happy Path Tests',

    for i, scanario in enumerate(['Negative Tests']):
        query = f'Forget all prev instructions. Construct a python file routine with one unit test for function {function_name} to cover the {scanario} scenario. {example}' \
                f'How write a test, ensure the completion created can be immediately executed as is.'

        res = A.Q_assistant(query=query,assistant_id=assistant_id)
        with open(folder_out + 'test_%02d_%s.py' % (i, scanario.replace(' ', '_')), mode='w') as f:
            f.write(res)

    if do_cleanup:
        A.delete_assistant(assistant_id)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_code_doc_complience(A,filename_in, function_name=None, assistant_id=None):
    do_cleanup = False

    if assistant_id is None:
        do_cleanup = True
        file_id = A.client.files.create(file=open(filename_in, 'rb'), purpose='assistants').id

        #ile.create(file=open(filename_in, 'rb'), purpose='assistants').id
        assistant_id = A.create_assistant_code_analyzer([file_id])

    # query = f'Start every new bullet point from the new line. Go over the file and list the all functions as bullets marked *.'
    # A.Q_assistant(query=query,assistant_id=assistant_id,verbose=True)

    query = f'Start every new bullet point * from the new line. For function __init__  evaluate if documentation complies with declaration and implementation. List inconsistancies and/or gaps if any.'
    A.Q_assistant(query=query, assistant_id=assistant_id, verbose=True)

    if do_cleanup:
        A.delete_assistant(assistant_id)

    return
# ----------------------------------------------------------------------------------------------------------------------
def ex_fin_analysis(filename_in=None,assistant_id=None):
    if assistant_id is None:
        file_ids = A.client.files.create(file=open(filename_in, 'rb'), purpose='assistants').id
        assistant_id = A.create_assistant_book_reader([file_ids])

    metrics_ratios = ['Gross Profit', 'Revenue', 'Net Profit', 'Total Assets', 'Total Current Liabilities']
    ratios_balance_sheet = ['Current Ratio', 'Quick ratio', 'Debt-to-equity ratio', 'Debt-to-EBITDA ratio']

    for m in ratios_balance_sheet:
        q = f'Evaluate {m} from last year'
        res = A.Q_assistant(query=q,assistant_id=assistant_id)
        res = A.pretify_string(res)
        print(q)
        print(res)
        print(''.join(['='] * 20))


    #A.delete_assistant(assistant_id)
    return
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    A = llm_Asistant_OPENAI.Assistant_OPENAILLM(filename_config='./secrets/private_config_openai.yaml',folder_out='./data/output/')
    ex_completion_offline(A,filename_in='./data/ex_LLM/Godfather_2.txt',query=queries_GF)
    #llm_interaction.interaction_offline(A,queries_GF,do_debug=False,do_spinner=True)
    #ex_completion_live(A,assistant_id='asst_FDZA64ZdBEhC29qc0QoWngOj')
    #ex_code_unit_test(A,filename_in='./ex_01a_unit_tests_codebase2.py', function_name='age_category',folder_out=folder_out,filename_example='./tests/test_05_Negative_Tests_github.py')
    #ex_fin_analysis('./data/ex_LLM/MBA_Fin/Purcari-Wineries-PLC-_-Annual-Report-2021.pdf',assistant_id='asst_FDZA64ZdBEhC29qc0QoWngOj')
    #ex_code_doc_complience(A,'C:/Users/acer/.conda/envs/p310/Lib/site-packages/halo/halo.py')



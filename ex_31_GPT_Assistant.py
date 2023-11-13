import cv2
import os
from LLM import tools_LLM_OPENAI
# ----------------------------------------------------------------------------------------------------------------------
folder_out = './tests/'
# ----------------------------------------------------------------------------------------------------------------------
def ex_completion_offline(A,query,filename_in,assistant_id=None):
    file = A.client.files.create(file=open(filename_in, 'rb'), purpose='assistants')
    do_cleanup = False

    if assistant_id is None:
        assistant_id = A.create_assistant_book_reader(file.id)
        do_cleanup = True

    if not isinstance(query,list):
        query = [query]

    for q in query:
        print(q)
        spinner = Halo(text='Processing', spinner='dots')
        spinner.start()
        res = A.Q_assistant(q,assistant_id=assistant_id)
        spinner.stop()
        print(res)
        print(''.join(['=']*20))

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
def ex_code_unit_test(A,filename_in, function_name, folder_out):
    do_cleanup = False

    file_id = A.client.files.create(file=open(filename_in, 'rb'), purpose='assistants').id
    assistant_id = A.create_assistant_code_interpreter([file_id])

    for i, scanario in enumerate(['Boundary Tests', 'Edge Cases', 'Data Type Tests', 'Corner Cases', 'Happy Path Tests','Negative Tests']):
        query = f'Focus on testing the logic to cover the {scanario} scenario.' \
                f'Construct a python file routine with one unit test for function {function_name} ' \
                f'so it can be executed in with single command in console.'

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

    A = tools_LLM_OPENAI.Assistant_OPENAILLM(filename_config='./secrets/private_config_openai.yaml',folder_out='./data/output/')
    # ex_completion_offline(A,filename_in='./data/ex_LLM/Godfather_2.txt',query=queries_GF)
    #ex_completion_live(A,assistant_id='asst_FDZA64ZdBEhC29qc0QoWngOj')
    #ex_code_unit_test(A,filename_in='./ex_01a_unit_tests_codebase.py', function_name='json_to_pandas_v01',folder_out=folder_out)
    #ex_fin_analysis('./data/ex_LLM/MBA_Fin/Purcari-Wineries-PLC-_-Annual-Report-2021.pdf',assistant_id='asst_FDZA64ZdBEhC29qc0QoWngOj')
    ex_code_doc_complience(A,'C:/Users/Anna/.conda/envs/p39/Lib/site-packages/halo/halo.py')




# https://python.langchain.com/docs/integrations/vectorstores/chroma
from langchain.schema.document import Document
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
# ----------------------------------------------------------------------------------------------------------------------
# texts = ['What was the favorite horse of the movie producer passionate about racing?',
#             'How Sonny was killed ?',
#             'What is Mike\'s hobby?',
#             'Name 5 families of NY mafia',
#             'Name all Casinos mentioned in the book',
#             'Name the favorite horse of the Hollywood producer',
#             'Who is Amerigo Bonasera?']
# ----------------------------------------------------------------------------------------------------------------------
def file_to_texts(filename_in):
    with open(filename_in, 'r') as f:
        text_document = f.read()
    texts = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=500,chunk_overlap=100).create_documents([text_document])
    texts = [text.page_content for text in texts]
    return texts
# ----------------------------------------------------------------------------------------------------------------------
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    texts = file_to_texts('./data/ex_LLM/Godfather.txt')
    docs = [Document(page_content=t, metadata={}) for t in texts]
    db = Chroma.from_documents(docs, embedding_function)
    #query = "Sonny"
    queries1 = ['What was the favorite horse of the movie producer passionate about racing?',
                'How Sonny was killed ?',
                'What is Mike\'s hobby?',
                'Name 5 families of NY mafia',
                'Name all Casinos mentioned in the book',
                'Name the favorite horse of the Hollywood producer',
                'Who is Amerigo Bonasera?']

    docs = db.similarity_search(queries1[0])
    embeddings = db._collection.get(include=['embeddings'])['embeddings']

    print(docs)
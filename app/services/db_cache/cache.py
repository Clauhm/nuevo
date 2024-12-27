import chromadb
import uuid
from loguru import logger

chroma_client = chromadb.PersistentClient(path="app\services\db_cache")
collection = chroma_client.get_or_create_collection(name="dbcache")

def check_cache(question):

    cache_result = collection.query(
        query_texts=[question],
        n_results=1
    )

    if not cache_result["documents"] or not cache_result["documents"][0]:
        logger.info('No hit in cache')
        return None
    
    distance = cache_result["distances"][0][0]
    if distance > 0.7:
        logger.info(f'Cache results distant: [{distance}]')
        return None

    answer = cache_result["metadatas"][0][0].get('answer')
    if answer:
        logger.info(f'Cache hit: [{distance}] {answer[:30]}...')
        return answer + '\n\n`cached`'
    
    logger.info('No answer found in cache metadata')
    return None

def save_answer(question, response):

    logger.info(f"Saving to cache: {question[:30]}...") 
    random_id = str(uuid.uuid4())[:8] 
    
    collection.add(
        documents=[question],
        ids=[random_id],
        metadatas=[{"answer": response}]
    )
    logger.info(f"Saved response for question: {question[:30]}...") 
    return None


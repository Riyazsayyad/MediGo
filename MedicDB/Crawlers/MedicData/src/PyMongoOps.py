from pymongo import MongoClient
import logging

connection_string = "mongodb://localhost:27017/medigo"
client = MongoClient(connection_string)
db = client['MediGo']

logging.basicConfig(
    filename='D:\Medic\MediGo\ProgramLog.log',  
    level=logging.INFO,  
    format='MONGO-DB %(asctime)s - %(levelname)s - %(message)s',  
    filemode='a'
)

def insertUrlAndPageCount(linkAndPageCountDict):
    collection = db['DrugsPageInfoAlpha'] 
    
    logging.info("Starting to insert URL and page count data into MongoDB.")
    
    for key, value in linkAndPageCountDict.items():
        try:
            record = {
                "url": key,
                "page_count": value
            }

            insert_result = collection.insert_one(record)
            
            logging.info(f"Inserted record with URL: {key}, Page Count: {value} into MongoDB.")
        
        except Exception as e:
            logging.error(f"Error inserting record for URL {key}: {e}")

    logging.info("Completed inserting all records into MongoDB.")
    
def getUrlAndPageCountFromDB():
    collection = db['DrugsPageInfoAlpha']  
    
    logging.info("Fetching URL and page count data from MongoDB.")
    
    try:
        cursor = collection.find()
        
        result_dict = {record['url']: record['page_count'] for record in cursor}        
        
        return result_dict
    
    except Exception as e:
        logging.error(f"Error fetching data from MongoDB: {e}")
        return {}

def insertDrugName(drugName):
    collection = db['DrugsName'] 
    
    try:
        record = {
            "drugname" : drugName
        }

        insert_result = collection.insert_one(record)
        
        logging.info(f"Inserted record  {drugName}")
    
    except Exception as e:
        logging.error(f"Error inserting record for  {drugName}: {e}")

    logging.info("Completed inserting all records into MongoDB.")

def getMedicNames():
    try:
        collection = db['DrugsName']

        logging.info("Connected to MongoDB and starting to fetch drug names.")
        cursor = collection.find({}, {"_id": 0, "drugname": 1})

        for record in cursor:
            drug_name = record['drugname'].strip()
            logging.info(f"Fetched drug name: {drug_name}")
            yield drug_name
    except Exception as e:
        logging.error(f"Error occurred while fetching drug names from MongoDB: {e}")
        raise

def insertDrugDetails1Mg(drugDetails):
    try:
        collection = db['OneMgDrugLinks'] 

        insert_result = collection.insert_one(drugDetails)
        
        logging.info(f"Inserted drug details: {drugDetails}. Inserted document ID: {insert_result.inserted_id}")
    
    except Exception as e:
        logging.error(f"Error occurred while inserting drug details: {e}")
        raise

def find_and_store_unique_urls():
    try:        
        unique_urls = set()
        collection = db['OneMgDrugLinks'] 
                
        logging.info("Fetching documents from the collection...")
        for document in collection.find():
            for key in document.keys():
                if key.startswith("https://"):  
                    unique_urls.add(key)  
        
        logging.info("Inserting unique URLs into 'OneMgUniqueUrls' collection...")
        for url in unique_urls:
            db["OneMgUniqueUrls"].insert_one({"url": url})

        logging.info("Unique URLs have been successfully stored in 'OneMgUniqueUrls' collection.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

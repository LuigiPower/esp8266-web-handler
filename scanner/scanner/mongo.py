from pymongo import MongoClient

################################################################################
# MONGO DB INIT
################################################################################

mongodb = MongoClient()
db = mongodb.net_scanner
gcm_collection = db.gcm_collection

def insert_gcm(registration_id):
    print "Inserting GCM %s" % registration_id
    element = {
            "registration_id": registration_id
            }
    gcm_collection.insert_one(element)

def remove_gcm(registration_id):
    print "Removing GCM %s" % registration_id
    element = {
            "registration_id": registration_id
            }
    gcm_collection.delete_one(element)

def get_gcm_list():
    cursor = gcm_collection.find()
    reg_id_list = []
    for regid in cursor:
        reg_id_list.append(regid['registration_id'])

    return reg_id_list

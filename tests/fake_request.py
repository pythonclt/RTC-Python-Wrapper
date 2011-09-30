import os

def alter_response(json_path, collection): 
    file_dir = os.path.abspath(os.path.dirname(__file__)) #constant at top of file
    collection.test_response = open('%s/json/%s' % (file_dir, json_path)).read() 
    return collection

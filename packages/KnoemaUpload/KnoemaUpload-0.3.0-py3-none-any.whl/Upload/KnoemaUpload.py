import requests
import os, sys
import json


class KnoemaDocumentUploader():
    UPL_URL='https://tmt.knoema.com/document/upload'
    DOCID_URL = 'https://tmt.knoema.com/document/getlink?id='
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    PUBLIC_URL = 'https://tmt.knoema.com/resource/share'
    def __init__(self,filepath,cookies):
        self.filepath= filepath
        self.cookies=cookies
        self.filename=os.path.basename(filepath)
        #print(self.filename)
        
    def FileUpload(self,headers=headers):
        files_ = {'file': (self.filename, open(self.filepath, 'rb'))}
        response = requests.post(KnoemaDocumentUploader.UPL_URL, cookies=self.cookies, files=files_)
        print('response status code: ', response.status_code, '\n')
        #sys.exit()
        json_ = json.loads(response.text)
        
        if 'error' in json_.keys():
            raise Exception(str(json_['error']))
        else:
            pass
            #print('id: ', json_['id'])
            #print('path: ', json_['path'])
            #print('type: ', json_['type'])
        #print('\nFind file path from id')
        
        res = requests.get(KnoemaDocumentUploader.DOCID_URL + json_['id'],  cookies=self.cookies)
        file_url = res.json()
        #print('File url :', file_url)
        
        #print('>>>Making it public')
        payload = {"IsPublic": "true", "Id": json_['id']}
        r = requests.post(KnoemaDocumentUploader.PUBLIC_URL, cookies=self.cookies, data=json.dumps(payload), headers = {'Content-Type': 'application/json'})
        #print('>>>Now the status is :',r.json())

        test_url = 'https://tmt.knoema.com/' + json_['id']
        #print(">>>Test URL for developer to delete test files",test_url)
        download_url = 'https://tmt.knoema.com/'+file_url
        print('>>>Download file url for users :', download_url)

        file = open('Download.txt', 'a')
        file.writelines(download_url + '\n')
        file.close()
        
    

This package is used for only internal purpose of the knoema employees to upload documents to the portal via API.

##Sample Script:##

from Upload import KnoemaUpload 

filepath=r"Path_Of_Your_Document_Upload" # Fill your own Path and Cookies <br />

cookies= {Your_Cookies} # Generate your own cookies. <br />
obj=KnoemaUpload.KnoemaDocumentUploader(filepath,cookies) <br />
obj.FileUpload() # There is an option to pass 'headers' as parameter in FileUpload() <br />

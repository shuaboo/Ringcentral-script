# RingCentral Download and Google Drive Upload

These two scripts download voicemails from RingCentral and then upload them to Google Drive.

## Prerequisites and Dependencies

Python3 must be installed
RingCentral must be installed `pip install ringcentral`
dateutil must be installed `pip install python_dateutil`
PyDrive must be installed  `pip install pydrive`

RingCentral and PyDrive API applications must be set up. RingCentral application must have Read Message and Call Log permissions.


RingCentral ClientID, Secret, user and password must be specified in config_template.yml, and then the file should be renamed config.yml. monthstart must also be set in config_template.yml, in ISO8601 time. monthstart is the start time of the month in ISO8601 which will be where the script will search starting from (monthstart can be set to earlier to pull from earlier voicemails) downloadpath must also be set to the directory where voicemails are to be downloaded to

In the GDriveUpload folder, change the id value to the id of the corresponding folder in GDrive (last section of the URL) and the dir value to the directory that download.py downloaded to in config_template.yml and then change the name to config.yml in the same folder as upload.py

## How To

Run download.py to download files locally to the download folder (default is RingCentral-script/RCDownload/download/, can rename DOWNLOADPATH in download.py to change download folder) in mp3 format, and then run upload.py to upload the files to Google Drive. When running upload.py, you will be prompted to log in to Google Drive.

import os
import ftplib
import time

def file_list():
    folder_path = 'E://sunjray job documents//projects//National-Hydrological-project-WRD//Backend//WRD_Received//'
    # Get a list of file names in the folder
    file_names = os.listdir(folder_path)
    return file_names
def file_upload():
    # Create a 'WRD_Sent' folder if it doesn't exist
    sent_folder = 'E://sunjray job documents//projects//National-Hydrological-project-WRD//Backend//WRD_Sent//'
    if not os.path.exists(sent_folder):
        os.makedirs(sent_folder)
     # Iterate over the file names and perform the desired action
    for filename in file_list():
     remotefile = filename
     ftp = ftplib.FTP('45.114.48.182')
     ftp.login('ftp_user1', 'Fu@0124&')
     ftp.cwd('/rtdassw_150')
     localfile = os.path.join('E://sunjray job documents//projects//National-Hydrological-project-WRD//Backend//WRD_Received//', filename)
     with open(localfile,"rb") as file:
         ftp.storbinary('STOR %s' % remotefile, file)

     # Move the uploaded file to the 'WRD_Sent' folder
     received_filepath = os.path.join(sent_folder, filename)
     os.rename(localfile, received_filepath)
     
     

if __name__ == "__main__":
    while True:
        try:
            file_upload()
            #time.sleep(900)
            print('file sent')
        except Exception as e:
            print("An error occurred:", e)
            print("Restarting the code...")
            #time.sleep(10)  # Delay before rerunning the code
            continue
        else:
            print("File sent")
            time.sleep(60)  # Delay between each iteration












import os
import ftplib
import time

def file_list():
    #time.sleep(60)
    folder_path = 'E://sunjray job documents//projects//National-Hydrological-project-WRD//Backend//Sunjray_Received//'
    # Get a list of file names in the folder
    file_names = os.listdir(folder_path)
    return file_names

def file_upload():
    # Create a 'Sent' folder if it doesn't exist
    received_folder = 'E://sunjray job documents//projects//National-Hydrological-project-WRD//Backend//Sunjray_Sent//'
    if not os.path.exists(received_folder):
        os.makedirs(received_folder)

    # Iterate over the file names and perform the desired action
    for filename in file_list():
        ftp = ftplib.FTP("192.168.0.177")
        ftp.login("Sunjray", "sunjray123")
        localfile = os.path.join('E://sunjray job documents//projects//National-Hydrological-project-WRD//Backend//Sunjray_Received//', filename)
        remotefile = filename

        with open(localfile, "rb") as file:
            ftp.storbinary('STOR %s' % remotefile, file)

        # Move the uploaded file to the 'Received' folder
        received_filepath = os.path.join(received_folder, filename)
        os.rename(localfile, received_filepath)


if __name__ == "__main__":
    while True:
        try:
            file_upload()
        except Exception as e:
            print("An error occurred:", e)
            print("Restarting the code...")
            #time.sleep(10)  # Delay before rerunning the code
            continue
        else:
            print("File sent")
        finally:
            time.sleep(60)  # Delay between each iteration

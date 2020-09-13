"""
This script is used to copy a specified template file to a specified destination folder in Google Drive.
"""
import sys
import helpers.imports as helpers
from apiclient import errors


def copy_file_request(service, origin_file_id, file_parent_id, file_name):
    """
    Creates and executes a request to copy a file to a specified directory.

    :param service: Google Drive v3 authentication object.
    :param origin_file_id: string id of original file to copy.
    :param file_parent_id: string id of folder to copy file to.
    :param file_name: string name for newly copied file.
    :return: copied file, if successful. none otherwise.
    """
    # setup request body
    copy_request_body = {
        'name': file_name,
        'parents': [file_parent_id]
    }

    # attempt to copy file
    try:
        return service.files().copy(fileId=origin_file_id, body=copy_request_body).execute()
    except errors.HttpError as error:
        print('An error occurred: {}'.format(error))

    # return none if file copy failed
    return None


def copy_file(service, file_url, folder_url, file_name):
    """
    Copies a file to a specified direction given a file and folder url.

    :param service: Google Drive v3 authentication object.
    :param file_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
    :param file_name: string name for newly copied file.
    :return: copied file, if successful. none otherwise.
    """
    # parse out file and folder ids for specified URLs
    file_id = helpers.get_file_id_from_url(file_url)
    folder_id = helpers.get_folder_id_from_url(folder_url)

    return copy_file_request(service, file_id, folder_id, file_name)


def main(file_url, folder_url, file_name):
    """
    Generates auth token and copies file.

    :param file_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
    :param file_name: string name for newly copied file.
    :return: copied file, if successful. none otherwise.
    """
    # auth client
    service = helpers.auth()

    # attempt to make a file copy
    return copy_file(service, file_url, folder_url, file_name)


if __name__ == '__main__':
    # get command line args
    arg_count = len(sys.argv) - 1

    # check for correct number of arguments
    if arg_count != 3:
        raise Exception("Invalid number of arguments. Expected 3 (file URL, folder URL, file name) got {}."
                        .format(arg_count))

    # parse each argument
    input_file_url = sys.argv[1]
    input_folder_url = sys.argv[2]
    input_file_name = sys.argv[3]

    # copy file to destination
    main(input_file_url, input_folder_url, input_file_name)

#TODO: function to iterate through all sub-directories in a directory, print file paths and file keys
import os


def get_keys(path, g_path):
    # list content
    for elem in os.listdir(path):
        new_path = os.path.join(path, elem)
        new_g_path = os.path.join(g_path, elem)
        if os.path.isdir(new_path):
            get_keys(new_path, new_g_path)
        else:
            if os.path.islink(new_path):
                key = os.readlink(new_path)
                print("'" + str(key.split('--')[-1].split('.')[0]) + "':'" + new_g_path + "',")
            else:
                pass


dir_path = '/home/giuly/test/test_FRDR_dataset'
globus_path = '/5/published/publication_170/submitted_data'
get_keys(dir_path, globus_path)


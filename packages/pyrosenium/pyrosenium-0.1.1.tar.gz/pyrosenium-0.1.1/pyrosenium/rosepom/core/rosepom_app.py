import os
import sys
import shutil


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WORKING_DIR =  os.getcwd()

TEMPLATE_CLS_NAME = "TPLTemplateLPT"


def _rewrite_file_cls_name(cls_name, input_filepath, output_filepath):
    '''
    Rewrite file
    '''
    with \
        open(input_filepath, 'r', encoding="utf-8") as input_file, \
        open(output_filepath, 'w+', encoding="utf-8") as output_file:
        for line in input_file:
            if TEMPLATE_CLS_NAME in line:
                line = line.replace(TEMPLATE_CLS_NAME, cls_name)
            output_file.write(line)

def _rewrite_cls_name_of_each_files(cls_name, loop_folder, des_folder):
    '''
    Recursive loop each folders and files
    '''
    for filename in os.listdir(loop_folder):
        input_filepath = f"{loop_folder}/{filename}"
        output_filepath = f"{des_folder}/{filename}"
        if not os.path.isfile(input_filepath):
            os.mkdir(output_filepath)
            _rewrite_cls_name_of_each_files(cls_name, input_filepath, output_filepath)
        else:
            _rewrite_file_cls_name(cls_name, input_filepath, output_filepath)

def create_rosepom_app():
    '''
    create_rose_pom_app
    '''
    app_name = list(sys.argv)[-1]

    src_folder = f"{BASE_DIR}/template"
    tmp_des_folder = f"{WORKING_DIR}/tmp"
    shutil.copytree(src_folder, tmp_des_folder, ignore=shutil.ignore_patterns("__pycache__"))

    cls_name = app_name.replace("_", ' ')
    cls_name = cls_name.title().replace(' ', '')
    des_folder = f"{WORKING_DIR}/{app_name}"
    os.mkdir(des_folder)

    _rewrite_cls_name_of_each_files(cls_name, tmp_des_folder, des_folder)

    shutil.rmtree(tmp_des_folder)

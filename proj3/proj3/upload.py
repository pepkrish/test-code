import os
from os import listdir
from os.path import isfile, join
import webbrowser
import shutil
from pyramid.view import view_config
from pyramid.request import Request
from pyramid.response import Response

ALLOWED_EXTENSIONS = set(['pdf','jpg'])
src_dir = "../proj3/proj3/uploaded_files"
upld_path = "proj3/uploaded_files"

@view_config(route_name='upload', renderer="proj3:templates/index.html")
#@view_config(route_name='upload')
def upload(request):
    message = ""
    row_arr = []
    if 'upload_file' in request.POST:
        if request.POST['file'] != '':
            filename = request.POST['file'].filename
            filename = filename.replace(" ", "")
            input_file = request.POST['file'].file
            if input_file and allowed_file(filename):
                file_exist = os.path.exists(upld_path+"/"+filename)
                #print file_exist
                if file_exist :
                    message = "File already exist."
                else:
                    file_path = os.path.join(src_dir, filename)
                    with open(file_path, 'wb') as output_file:
                        shutil.copyfileobj(input_file, output_file)
                        message = "File uploaded successfully."
            else:
                message = "File is not an valid format."
        else:
            message = "Please select the file to upload."
    for f in listdir(src_dir):
        file_path = join(join(os.path.abspath(""),upld_path),f)
        file_name = f
        arr_cols = [file_path,file_name]
        row_arr.append(arr_cols)
    template_vals = {
        "row_arr":row_arr,
        "message":message
    }
    return template_vals

@view_config(route_name='del_file', renderer="json")
def del_file(request):
    message = "Delete not successful."
    if 'file_name' in request.POST:
        file_name = request.POST['file_name']
        os.remove(src_dir+"/"+file_name)
        message = "File removed successfully."
    template_vals = {
        "message":message
    }
    return dict(template_vals)

@view_config(route_name='view_file', renderer="json")
def view_file(request):
    message = ""
    if 'view_file' in request.POST:
        file_name = request.POST['file_name']
        file_path = os.path.join(src_dir, file_name)
        url = file_path
        webbrowser.open_new(url)
        template_vals = {
            "message":message
        }
        return dict(template_vals)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

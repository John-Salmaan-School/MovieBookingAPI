# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

# Function to check whether the uploaded file is allowed based on extension
def allowed_file(filename: str, ext_list: list):
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ext_list
def create_file_object(filename: str = "", path: str = "", type: str = ""):
    """
    Create a file object.
    filename: str, the filename of the attachment.
    path: str, the path of the attachment.
    type: str, the type of the attachment, example: 'text/plain'.
    """
    file_object = (filename, open(path, 'rb'), type)
    
    return file_object


def create_attachment(id: int = 0, description: str = "", filename: str = ""):
    """
    Create an attachment object.
    id: int, the attachment ID.
    description: str, the description of the attachment.
    filename: str, the filename of the attachment.
    """
    attachment = {
        "id": id,
        "description": description,
        "filename": filename
    }
    return attachment
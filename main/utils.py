from uuid import uuid4

def create_avatar_name(instance, filename):
    """
    Function for creating hash name for user uploaded avatar files.
    """
    extension = filename.split('.')[-1]
    hashed_file_name = f'{uuid4()}.{extension}'
    return f'avatars/{hashed_file_name}'

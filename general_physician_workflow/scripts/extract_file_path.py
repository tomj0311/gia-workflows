"""Extracts file_path from uploaded media_data. | Inputs: media_data | Outputs: file_path"""

def get_file_path(data):
    path = None
    if isinstance(data, dict):
        path = data.get('file_path') or data.get('path')
    else:
        try:
            path = getattr(data, 'file_path', None) or getattr(data, 'path', None)
        except Exception:
            pass
    return path

# Main block: Variables defined here are GLOBAL and VISIBLE in UI
file_path = get_file_path(media_data)
"""Extracts file_path from uploaded media_data. | Inputs: media_data | Outputs: file_path"""
# Assumes media_data is a dict or object with a 'file_path' or similar attribute
file_path = None
if isinstance(media_data, dict):
    file_path = media_data.get('file_path') or media_data.get('path')
else:
    try:
        file_path = getattr(media_data, 'file_path', None) or getattr(media_data, 'path', None)
    except Exception as e:
        _error_extract = str(e)
_debug_input = f"media_data={media_data}"
_info_result = f"file_path={file_path}"
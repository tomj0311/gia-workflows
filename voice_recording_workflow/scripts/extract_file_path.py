"""Extract File Path from Media Upload | Inputs: media_data | Outputs: file_path"""

# Direct variable access - media_data comes from the user task form field
# The media_data variable contains the uploaded file information

# Extract the file path from the media_data
# The file is uploaded to the form and stored with metadata including the path
if media_data and hasattr(media_data, 'get'):
    # If media_data is a dictionary with file information
    file_path = media_data.get('file_path') or media_data.get('path')
    
    if not file_path and 'name' in media_data:
        # Fallback: construct path from filename if direct path not available
        file_path = f"/uploads/{media_data.get('name')}"
        
    _info_extraction = f"Extracted file path: {file_path}"
    
elif isinstance(media_data, str):
    # If media_data is already a file path string
    file_path = media_data
    _info_extraction = f"Using direct file path: {file_path}"
    
else:
    # Handle unexpected format
    file_path = None
    _error_extraction = f"Unable to extract file path from media_data type: {type(media_data)}"
    raise ValueError(f"Invalid media_data format: {type(media_data)}")

# Validate the extracted file path
if not file_path:
    _error_extraction = "File path is empty or None"
    raise ValueError("Failed to extract valid file path from media_data")

_debug_input = f"media_data type: {type(media_data)}"

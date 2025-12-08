"""Converts uploaded PDF to images. | Inputs: pdf_file, token | Outputs: images_data, pdf_name"""

def convert_pdf(pdf_input, auth_token):
    import pypdfium2 as pdfium
    import io
    import os
    import requests
    import urllib.parse

    def get_file_info(data):
        path = None
        name = "document.pdf"
        
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        
        if isinstance(data, dict):
            path = data.get('file_path') or data.get('path')
            name = data.get('filename') or data.get('name') or name
        else:
            try:
                path = getattr(data, 'file_path', None) or getattr(data, 'path', None)
                name = getattr(data, 'filename', None) or getattr(data, 'name', None) or name
            except Exception:
                pass
        return path, name

    file_path, pdf_name = get_file_info(pdf_input)
    images_data = []

    if file_path:
        # Download from MinIO via API
        api_host = os.environ.get("CLIENT_URL", "http://localhost:4000")
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        encoded_path = '/'.join(urllib.parse.quote(segment, safe='') for segment in file_path.split('/'))
        url = f"{api_host.rstrip('/')}/api/download/{encoded_path}"
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        # Load PDF from bytes
        pdf = pdfium.PdfDocument(response.content)
        for i in range(len(pdf)):
            page = pdf[i]
            # scale=1 is ~72 DPI, scale=2 is ~144 DPI
            bitmap = page.render(
                scale=2,  # Higher resolution
                rotation=0,
            )
            pil_image = bitmap.to_pil()
            img_byte_arr = io.BytesIO()
            # Save with maximum quality and no compression
            pil_image.save(img_byte_arr, format='PNG', optimize=False, compress_level=0)
            images_data.append(img_byte_arr.getvalue())
            
    return images_data, pdf_name, file_path

def upload_images_to_minio(images_data, pdf_name, origin_path, auth_token):
    """Upload extracted images to MinIO and return the list of uploaded paths."""
    import os
    import requests
    import urllib.parse
    
    uploaded_paths = []
    
    # Get the folder where the PDF is located
    pdf_folder = os.path.dirname(origin_path)
    extracted_folder = f"{pdf_folder}/extracted_files"
    
    # API endpoint for upload (use the path-based endpoint)
    api_host = os.environ.get("CLIENT_URL", "http://localhost:4000")
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    for i, img_bytes in enumerate(images_data):
        safe_name = os.path.splitext(pdf_name)[0]
        img_filename = f"{safe_name}_page_{i+1}.png"
        
        # Encode the path for the URL
        encoded_path = urllib.parse.quote(extracted_folder, safe='')
        upload_url = f"{api_host.rstrip('/')}/api/upload/{encoded_path}"
        
        # Prepare multipart form data (just the file)
        files = {
            'files': (img_filename, img_bytes, 'image/png')
        }
        response = requests.post(upload_url, headers=headers, files=files)
        response.raise_for_status()
        result = response.json()
        uploaded_files = result.get('files', [])
        if uploaded_files:
            uploaded_path = uploaded_files[0].get('path', '')
            uploaded_paths.append(uploaded_path)
    
    return uploaded_paths

# Main block
try:
    current_token = user["token"]
    
    # 1. Convert PDF to List of Bytes
    raw_images, pdf_filename, pdf_path = convert_pdf(pdf_file, current_token)
    
    # 2. Upload those bytes to MinIO so they have paths
    images_data = upload_images_to_minio(raw_images, pdf_filename, pdf_path, current_token)
    
    # Provide pdf_name for downstream
    pdf_name = pdf_filename
    
except Exception as e:
    import traceback
    traceback.print_exc()
    raise

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
            # scale=1 is ~72 DPI, scale=4.17 ≈ 300 DPI
            bitmap = page.render(
                scale=2,  # Higher resolution
                rotation=0,
            )
            pil_image = bitmap.to_pil()
            img_byte_arr = io.BytesIO()
            # Save with maximum quality and no compression
            pil_image.save(img_byte_arr, format='PNG', optimize=False, compress_level=0)
            images_data.append(img_byte_arr.getvalue())
            
    return images_data, pdf_name

def upload_images_to_minio(images_data, pdf_name, pdf_file, auth_token):
    """Upload extracted images to MinIO and return the list of uploaded paths."""
    import os
    import requests
    import urllib.parse
    
    uploaded_paths = []
    
    # Get the folder where the PDF is located
    pdf_folder = os.path.dirname(pdf_file["file_path"])
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
            print(f"Uploaded to MinIO: {uploaded_path}")
        else:
            print(f"Uploaded {img_filename} successfully")
    
    return uploaded_paths

def process_images(images, auth_token_val):
    import requests
    import io
    import os

    results = []
    
    # Get API host from environment variable
    api_host = os.environ.get("CLIENT_URL", "http://localhost:4000")
    url = f"{api_host.rstrip('/')}/api/agent-runtime/run_non_streaming"
    
    headers = {"Authorization": f"Bearer {auth_token_val}"}

    for i, image_bytes in enumerate(images):
        data = {
            "agent_name": "Image to Markdown", 
            "prompt": "Perform OCR on the attached image. Return only the result text in markdown format without any comments. Preserve tabular formats if any."
        }
        
        files = {
            'files': (f'page_{i+1}.png', io.BytesIO(image_bytes), 'image/png')
        }
        response = requests.post(url, headers=headers, data=data, files=files, stream=False)
        response.raise_for_status()
        json_data = response.json()
        markdown_text = json_data.get("content", "")
        results.append(markdown_text)
            
    return results

if __name__ == "__main__":
    user = {
        "id": "M6OXV3z7DTsLzzv7naJXRQ",
        "role": "user",
        "tenantId": "da88b6a1-5288-4527-af6b-679c311aece3",
        "email": "tomj0311@gmail.com",
        "type": "access",
        "exp": 1763896151,
        "iat": 1763867351,
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ik02T1hWM3o3RFRzTHp6djduYUpYUlEiLCJyb2xlIjoidXNlciIsInRlbmFudElkIjoiZGE4OGI2YTEtNTI4OC00NTI3LWFmNmItNjc5YzMxMWFlY2UzIiwiZW1haWwiOiJ0b21qMDMxMUBnbWFpbC5jb20iLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzOTYyNDkzLCJpYXQiOjE3NjM5MzM2OTN9.zJXEyMKa2Qeb1WMH177XeOZhCQ79HKwYXymwV1HT9e4"
    }

    pdf_file = {
        "filename": "MyStatement.pdf",
        "file_path": "uploads/M6OXV3z7DTsLzzv7naJXRQ/69228bcae13dc93a369a752f/40e565/MyStatement.pdf",
        "content_type": "application/pdf"
    }

    current_token = user["token"]
    try:
        current_token = user["token"]
        images_data, pdf_name = convert_pdf(pdf_file, current_token)
        print(f"PDF Name: {pdf_name}")
        print(f"Number of images: {len(images_data)}")

        ocr_results = process_images(images_data, current_token)
        print(ocr_results)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise

"""Converts uploaded PDF to images. | Inputs: pdf_file | Outputs: images_data, pdf_name"""
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
        
        try:
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
                
        except Exception as e:
            print(f"Error processing PDF: {e}")
            
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
        
        try:
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
        except Exception as e:
            print(f"Error uploading {img_filename}: {e}")
    
    return uploaded_paths

def process_images(images, auth_token_val):
    import requests
    import io
    import os

    results = []
    
    # Get API host from environment variable
    api_host = os.environ.get("CLIENT_URL", "http://localhost:4000")
    url = f"{api_host.rstrip('/')}/api/agent-runtime/run"
    
    headers = {"Authorization": f"Bearer {auth_token_val}"}

    for i, image_bytes in enumerate(images):
        data = {
            "agent_name": "OCR Agent", 
            "prompt": "Perform OCR on the attached image. Return the text in markdown format, prserve tabular formats if any."
        }
        
        files = {
            'files': (f'page_{i+1}.png', io.BytesIO(image_bytes), 'image/png')
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, files=files, stream=False)
            response.raise_for_status()
            results.append(response.text)
        except Exception as e:
            print(f"Error processing page {i+1}: {e}")
            results.append(f"Error processing page {i+1}: {str(e)}")
            
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
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ik02T1hWM3o3RFRzTHp6djduYUpYUlEiLCJyb2xlIjoidXNlciIsInRlbmFudElkIjoiZGE4OGI2YTEtNTI4OC00NTI3LWFmNmItNjc5YzMxMWFlY2UzIiwiZW1haWwiOiJ0b21qMDMxMUBnbWFpbC5jb20iLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzOTI0OTkyLCJpYXQiOjE3NjM4OTYxOTJ9.61K-gXmdw9sNBfaxqL7do1QLPSjyWIdMceGNsqrmIN0"
    }

    pdf_file = {
        "filename": "DPR (1).pdf",
        "file_path": "uploads/M6OXV3z7DTsLzzv7naJXRQ/69228bcae13dc93a369a752f/8437b2/DPR (1).pdf",
        "file_size": 13938975,
        "content_type": "application/pdf"
    }

    current_token = user["token"]
    images_data, pdf_name = convert_pdf(pdf_file, current_token)
    print(f"PDF Name: {pdf_name}")
    print(f"Number of images: {len(images_data)}")

    ocr_results = process_images(images_data, current_token)

    # ONLY for debugging 
    # user = {
    #     "id": "M6OXV3z7DTsLzzv7naJXRQ",
    #     "role": "user",
    #     "tenantId": "da88b6a1-5288-4527-af6b-679c311aece3",
    #     "email": "tomj0311@gmail.com",
    #     "type": "access",
    #     "exp": 1763896151,
    #     "iat": 1763867351,
    #     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ik02T1hWM3o3RFRzTHp6djduYUpYUlEiLCJyb2xlIjoidXNlciIsInRlbmFudElkIjoiZGE4OGI2YTEtNTI4OC00NTI3LWFmNmItNjc5YzMxMWFlY2UzIiwiZW1haWwiOiJ0b21qMDMxMUBnbWFpbC5jb20iLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYzODk2MTUxLCJpYXQiOjE3NjM4NjczNTF9.idbLBL9AAsjGVvo25XFYJZYsX4qab2WmXl42S5QQD6w"
    # }
    # pdf_file = {
    #     "filename": "DPR (1).pdf",
    #     "file_path": "uploads/M6OXV3z7DTsLzzv7naJXRQ/69228bcae13dc93a369a752f/8437b2/DPR (1).pdf",
    #     "file_size": 13938975,
    #     "content_type": "application/pdf"
    # }
    # current_token = user["token"]
    # images_data, pdf_name = convert_pdf(pdf_file, current_token)
    # print(f"PDF Name: {pdf_name}")
    # print(f"Number of images: {len(images_data)}")

    # # Upload images to MinIO and get the paths
    # uploaded_paths = upload_images_to_minio(images_data, pdf_name, pdf_file, current_token)
    # print(f"\nSuccessfully uploaded {len(uploaded_paths)} images to MinIO")
    # print(f"Uploaded paths: {uploaded_paths}")

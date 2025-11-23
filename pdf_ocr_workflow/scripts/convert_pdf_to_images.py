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
                bitmap = page.render()
                pil_image = bitmap.to_pil()
                img_byte_arr = io.BytesIO()
                pil_image.save(img_byte_arr, format='PNG')
                images_data.append(img_byte_arr.getvalue())
                
        except Exception as e:
            print(f"Error processing PDF: {e}")
            
    return images_data, pdf_name, len(images_data)


if __name__ == "__main__":
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
    current_token = user["token"]
    images_data, pdf_name, num_images = convert_pdf(pdf_file, current_token)
    print(f"PDF Name: {pdf_name}")
    print(f"Number of images: {num_images}")

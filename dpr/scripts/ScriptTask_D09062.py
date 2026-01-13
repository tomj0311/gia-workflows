"""Converts PDF to images and processes them with AI agent. | Inputs: pdf_file | Outputs: ocr_results, pdf_name"""

import os
import io
import requests
import json
import urllib.parse
from dotenv import load_dotenv

# Try importing pypdfium2, handle if missing
try:
    import pypdfium2 as pdfium
except ImportError:
    pdfium = None
    print("Warning: pypdfium2 not installed. PDF conversion will fail.")

def convert_pdf(pdf_path):
    auth_token = os.getenv("GIA_API_TOKEN")
    pdf_name = os.path.basename(pdf_path)
    images_data = []

    if not pdfium:
        raise ImportError("pypdfium2 is required for PDF conversion")

    # Download from MinIO via API
    api_host = os.environ.get("API_URL", "http://localhost:4000")
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Simple URL encoding
    encoded_path = urllib.parse.quote(pdf_path)
    # The API seems to expect the path to be somewhat encoded or just appended. 
    # Based on original code: encoded_path = '/'.join(urllib.parse.quote(segment, safe='') for segment in file_path.split('/'))
    # Let's keep the split/quote logic to be safe as it works for the existing backend
    encoded_path = '/'.join(urllib.parse.quote(segment, safe='') for segment in pdf_path.split('/'))
    
    url = f"{api_host.rstrip('/')}/api/uploads/download/{encoded_path}"
    print(f"Downloading PDF from: {url}")
    
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()

    # Load PDF from bytes
    pdf = pdfium.PdfDocument(response.content)
    for i in range(len(pdf)):
        page = pdf[i]
        # scale=2 is ~144 DPI
        bitmap = page.render(scale=2, rotation=0)
        pil_image = bitmap.to_pil()
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='PNG', optimize=False, compress_level=0)
        images_data.append(img_byte_arr.getvalue())
            
    return images_data, pdf_name

def upload_images_to_minio(images_data, pdf_name, origin_path):
    """Upload extracted images to MinIO."""
    auth_token = os.getenv("GIA_API_TOKEN")
    uploaded_paths = []
    
    pdf_folder = os.path.dirname(origin_path)
    extracted_folder = f"{pdf_folder}/extracted_files"
    
    api_host = os.environ.get("API_URL", "http://localhost:4000")
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    for i, img_bytes in enumerate(images_data):
        safe_name = os.path.splitext(pdf_name)[0]
        img_filename = f"{safe_name}_page_{i+1}.png"
        
        encoded_path = urllib.parse.quote(extracted_folder, safe='')
        upload_url = f"{api_host.rstrip('/')}/api/uploads/upload/{encoded_path}"
        
        files = {'files': (img_filename, img_bytes, 'image/png')}
        response = requests.post(upload_url, headers=headers, files=files)
        response.raise_for_status()
        
        result = response.json()
        if result.get('files'):
            uploaded_paths.append(result['files'][0].get('path', ''))
    
    return uploaded_paths

def process_images(image_paths):
    auth_token_val = os.getenv("GIA_API_TOKEN")
    results = []
    api_host = os.environ.get("API_URL", "http://localhost:4000")
    tool_url = f"{api_host.rstrip('/')}/api/tools/execute-method"
    
    headers = {
        "Authorization": f"Bearer {auth_token_val}",
        "Content-Type": "application/json"
    }

    for index, img_path in enumerate(image_paths):
        print(f"Processing page {index + 1}: {img_path}")
        payload = {
            "config_name": "OpenAI Vision",
            "method_name": "analyze_image_standalone",
            "parameters": {
                "file_path": img_path,
                "prompt": "Analyze the image and transcribe the text if any. Do not add any conversational commentary."
            }
        }
        
        try:
            response = requests.post(tool_url, headers=headers, json=payload, timeout=120.0)
            if response.ok:
                result_json = response.json()
                if result_json.get('success'):
                    results.append(result_json.get('result', ''))
                else:
                    results.append(f"Error: {result_json.get('error')}")
            else:
                results.append(f"Error: HTTP {response.status_code}")
                
        except Exception as e:
            results.append(f"Exception: {str(e)}")
            
    return "\n\n".join(results)

# Main Execution
if __name__ == "__main__":
    try:
        load_dotenv()
        
        # Handle variable name mismatch (file_path vs pdf_file)
        pdf_file = dpr_file[0]["file_path"]
        print(pdf_file)
        
        # 1. Convert PDF to images
        raw_images, pdf_filename = convert_pdf(pdf_file)
        
        # 2. Upload images to MinIO
        images_paths = upload_images_to_minio(raw_images, pdf_filename, pdf_file)
        
        # 3. Clean up memory
        del raw_images
        
        # 4. Process with AI Agent
        pdf_read_results = process_images(images_paths)
               
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Re-raise exception so the task fails and we see the error in the workflow
        raise e

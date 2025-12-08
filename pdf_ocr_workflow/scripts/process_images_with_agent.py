"""Processes images with AI agent. | Inputs: images_data, token | Outputs: ocr_results"""

def process_images(image_paths, auth_token_val):
    import requests
    import io
    import os
    import urllib.parse
    
    results = []
    
    # Get API host from environment variable
    api_host = os.environ.get("CLIENT_URL", "http://localhost:4000")
    
    # Agent Runtime URL
    run_url = f"{api_host.rstrip('/')}/api/agent-runtime/run"
    
    headers = {"Authorization": f"Bearer {auth_token_val}"}

    for i, img_path in enumerate(image_paths):
        # 1. Download the image first to get bytes
        encoded_path = '/'.join(urllib.parse.quote(segment, safe='') for segment in img_path.split('/'))
        download_url = f"{api_host.rstrip('/')}/api/download/{encoded_path}"
        
        try:
            dl_response = requests.get(download_url, headers=headers)
            dl_response.raise_for_status()
            image_bytes = dl_response.content
            
            # 2. Send bytes to Agent
            data = {
                "agent_name": "Image to Markdown", 
                "prompt": "Perform OCR on the attached image. Return only the result text in markdown format without any comments. Preserve tabular formats if any."
            }
            
            files = {
                'files': (f'page_{i+1}.png', io.BytesIO(image_bytes), 'image/png')
            }
            
            response = requests.post(run_url, headers=headers, data=data, files=files, stream=False)
            response.raise_for_status()
            json_data = response.json()
            markdown_text = json_data.get("content", "")
            results.append(markdown_text)
            
        except Exception as e:
            print(f"Error processing page {i+1} ({img_path}): {e}")
            results.append(f"<!-- Error processing page {i+1}: {str(e)} -->")
            
    # Join all pages with newlines
    return "\n\n".join(results)

# Main block
try:
    current_token = user["token"]
    
    # images_data is passed from the previous step (List of strings/paths)
    ocr_results = process_images(images_data, current_token)
    
except Exception as e:
    import traceback
    traceback.print_exc()
    raise

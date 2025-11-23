"""Processes images with AI agent. | Inputs: images_data, token | Outputs: ocr_results"""
"""Processes images with AI agent. | Inputs: images_data, token | Outputs: ocr_results"""

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
            "agent_name": "MyAgent", 
            "prompt": "Perform OCR on this image. Return the text in markdown format. Return only the text content."
        }
        
        files = {
            'files': (f'page_{i+1}.png', io.BytesIO(image_bytes), 'image/png')
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, files=files, stream=True)
            response.raise_for_status()
            results.append(response.text)
        except Exception as e:
            print(f"Error processing page {i+1}: {e}")
            results.append(f"Error processing page {i+1}: {str(e)}")
            
    return results

# Main block: Variables defined here are GLOBAL and VISIBLE in UI

# Resolve token in main block to pass to function
current_token = user["token"]

ocr_results = process_images(images_data, current_token)

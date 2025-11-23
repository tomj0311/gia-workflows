"""Processes images with AI agent. | Inputs: images_data, token | Outputs: ocr_results"""
"""Processes images with AI agent. | Inputs: images_data, token | Outputs: ocr_results"""

def process_images(images, auth_token_val):
    import requests
    import io

    results = []
    url = "http://localhost:8000/api/agent-runtime/run"
    
    # Handle token resolution inside function or pass it in
    # Here we use the passed value
    
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
            if response.status_code == 200:
                results.append(response.text)
            else:
                results.append(f"Error processing page {i+1}: {response.status_code}")
        except Exception as e:
            results.append(f"Exception processing page {i+1}: {str(e)}")
            
    return results

# Main block: Variables defined here are GLOBAL and VISIBLE in UI

# Resolve token in main block to pass to function
current_token = token if 'token' in globals() else ''
if not current_token and 'user' in globals() and hasattr(user, 'token'):
    current_token = user.token
elif not current_token and 'user' in globals() and isinstance(user, dict):
    current_token = user.get('token')

ocr_results = process_images(images_data, current_token)

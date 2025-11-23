"""Creates knowledge config from OCR results. | Inputs: ocr_results, pdf_name, token | Outputs: upload_response"""
"""Creates knowledge config from OCR results. | Inputs: ocr_results, pdf_name, token | Outputs: upload_response"""

def create_config(results, name, auth_token_val):
    import requests
    import json

    markdown_content = f"# {name}\n\n" + "\n\n".join(results)

    config_payload = {
        "name": name,
        "category": "Uploaded Documents",
        "model_id": "gemini-embedding-001", 
        "type": "knowledgeConfig"
    }

    base_url = "http://localhost:8000"
    collection_name = name.replace(" ", "_").replace(".", "_") 

    files = {
        'files': ('memory_doc.md', markdown_content, 'text/markdown')
    }

    data = {
        'payload': json.dumps(config_payload)
    }

    params = {
        'collection': collection_name
    }

    headers = {
        'Authorization': f'Bearer {auth_token_val}'
    }

    try:
        response = requests.post(
            f"{base_url}/api/knowledge/upload",
            params=params,
            headers=headers,
            data=data,
            files=files
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Main block: Variables defined here are GLOBAL and VISIBLE in UI

# Resolve token in main block to pass to function
current_token = token if 'token' in globals() else ''
if not current_token and 'user' in globals() and hasattr(user, 'token'):
    current_token = user.token
elif not current_token and 'user' in globals() and isinstance(user, dict):
    current_token = user.get('token')

upload_response = create_config(ocr_results, pdf_name, current_token)

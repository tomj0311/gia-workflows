"""Creates knowledge config from OCR results. | Inputs: ocr_results, pdf_name, token | Outputs: upload_response"""

def create_config(results, name, auth_token_val):
    import requests
    import json
    import io

    # results is now a single markdown string
    markdown_content = f"# {name}\n\n{results}"

    config_payload = {
        "name": f"_{name}",
        "category": "ocr-results",
        "model_name": "MiniLML6", 
        "type": "knowledgeConfig",
        "overwrite": True
    }

    base_url = "http://localhost:8000"
    
    # Safe collection name
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
        import os
        api_host = os.environ.get("CLIENT_URL", "http://localhost:4000")
        
        # Override base_url to be safe and consistent with the "complete" script reference
        url = f"{api_host.rstrip('/')}/api/knowledge/upload"
        
        response = requests.post(
            url,
            params=params,
            headers=headers,
            data=data,
            files=files
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error: {e}"

# Main block
try:
    current_token = user["token"]

    # ocr_results is the markdown string from the User Task (or previous step)
    # pdf_name is passed through
    
    upload_response = create_config(ocr_results, pdf_name, current_token)
    
except Exception as e:
    import traceback
    traceback.print_exc()
    raise

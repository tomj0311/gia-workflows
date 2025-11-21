"""Extracts specialist_name from analysis_result. | Inputs: analysis_result | Outputs: specialist_name"""
import re

def find_specialist(result_text):
    name_found = None
    if result_text:
        # Try to extract a known specialist name from the agent's reply
        known_specialists = ["Dr. Philip", "Dr. Eleena", "Dr. Hima", "Dr. Eliyaz"]
        for name in known_specialists:
            if name in result_text:
                name_found = name
                break
        
        if not name_found:
            # Fallback: try to extract a Dr. Name pattern
            match = re.search(r"Dr\.\s+[A-Za-z]+", result_text)
            if match:
                name_found = match.group(0)
    return name_found

# Main block: Variables defined here are GLOBAL and VISIBLE in UI
specialist_name = find_specialist(analysis_result)
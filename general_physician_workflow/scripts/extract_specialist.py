"""Extracts specialist_name from analysis_result. | Inputs: analysis_result | Outputs: specialist_name"""
import re
specialist_name = None
if analysis_result:
    # Try to extract a known specialist name from the agent's reply
    for name in ["Dr. Philip", "Dr. Eleena", "Dr. Hima", "Dr. Eliyaz"]:
        if name in analysis_result:
            specialist_name = name
            break
    if not specialist_name:
        # Fallback: try to extract a Dr. Name pattern
        match = re.search(r"Dr\.\s+[A-Za-z]+", analysis_result)
        if match:
            specialist_name = match.group(0)
_debug_input = f"analysis_result={analysis_result}"
_info_result = f"specialist_name={specialist_name}"
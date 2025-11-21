"""Creates analysis prompt for agent. | Inputs: transcription_result | Outputs: analysis_prompt"""

def generate_prompt(transcription):
    specialists = [
        "Dr. Philip (Endocrinologist)",
        "Dr. Eleena (Dermatologist)",
        "Dr. Hima (Eye Specialist)",
        "Dr. Eliyaz (ENT Specialist)"
    ]
    
    prompt = f"""
You are a General Physician. Analyze the following patient transcription and suggest the most relevant consultant from this list: {', '.join(specialists)}.\n\nIf more than one could be relevant, pick the most appropriate.\n\nPatient transcription:\n{transcription}\n\nReply with the specialist's name only (e.g., Dr. Priya), and a brief reason for your choice.\n"""
    return prompt

# Main block: Variables defined here are GLOBAL and VISIBLE in UI
analysis_prompt = generate_prompt(transcription_result)

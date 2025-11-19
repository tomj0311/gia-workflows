"""Creates analysis prompt for agent. | Inputs: transcription_result | Outputs: analysis_prompt"""
specialists = [
    "Dr. Priya (General Physician)",
    "Dr. Philip (Endocrinologist)",
    "Dr. Eleena (Dermatologist)",
    "Dr. Hima (Eye Specialist)",
    "Dr. Eliyaz (ENT Specialist)"
]

analysis_prompt = f"""
You are a hospital triage assistant. Analyze the following patient transcription and suggest the most relevant specialist from this list: {', '.join(specialists)}.\n\nIf more than one could be relevant, pick the most appropriate.\n\nPatient transcription:\n{transcription_result}\n\nReply with the specialist's name only (e.g., Dr. Priya), and a brief reason for your choice.\n"""
_debug_input = f"transcription_result={transcription_result}"
_info_result = f"analysis_prompt={analysis_prompt}"
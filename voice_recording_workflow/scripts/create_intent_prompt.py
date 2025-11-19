"""
Script to create a prompt for validating the speaker's intent.
This script takes the transcribed response and creates a validation prompt.

Inputs: transcription_result, mobile_number
Outputs: prompt
"""

# Direct variable access from workflow context
# transcription_result comes from the transcribe_audio service task
# mobile_number comes from the collect_mobile_number user task

# Create the intent validation prompt
prompt = f"""Analyze the following transcribed video message and determine the speaker's intent.

Mobile Number: {mobile_number}
Transcribed Message: {transcription_result}

Please identify:
1. The main intent or purpose of the message
2. Any specific requests or actions mentioned
3. The sentiment and tone of the speaker
4. Key information or details provided

Provide a structured analysis of the speaker's intent."""

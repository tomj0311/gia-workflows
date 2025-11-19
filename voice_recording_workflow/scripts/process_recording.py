"""
Process Transcribed Recording Results
Processes the transcribed text from the Whisper service task and agent results.
Combines metadata with transcription results for final output.

Inputs: file_path, transcription_result, agent_result
Outputs: status, message, transcription, agent_analysis, file_path, timestamp
Logging: _info_process, _info_transcription, _warning_empty, _error_process
"""

import json
from datetime import datetime

# Direct variable access from workflow context
# file_path (str): File path extracted from media_data
# transcription_result (str): Transcribed text from Whisper service task
# agent_result (str): Agent analysis from execute_agent service task

# Validate required variables
try:
    file_path
except NameError:
    raise Exception("Required variable 'file_path' not found in workflow context")

try:
    transcription_result
except NameError:
    raise Exception("Required variable 'transcription_result' not found in workflow context")

try:
    agent_result
except NameError:
    raise Exception("Required variable 'agent_result' not found in workflow context")

# Additional validation
if file_path is None:
    raise Exception("Required variable 'file_path' is None")

if transcription_result is None:
    raise Exception("Required variable 'transcription_result' is None")

if agent_result is None:
    raise Exception("Required variable 'agent_result' is None")

try:
    # Generate timestamp
    timestamp = datetime.utcnow().isoformat()
    
    # Process transcription results
    transcription = transcription_result.strip() if transcription_result else ""
    agent_analysis = agent_result.strip() if agent_result else ""
    
    if transcription:
        # Successful transcription
        status = "success"
        message = "Voice recording transcribed and analyzed successfully"
        
        # Logging variables for workflow visibility
        _info_process = f"Processing complete - File: {file_path}"
        _info_transcription = f"Transcribed {len(transcription)} characters, analyzed by agent"
        
        # Warning for very short transcriptions
        if len(transcription) < 10:
            _warning_empty = f"Transcription is very short ({len(transcription)} chars) - may be empty or unclear audio"
        else:
            _warning_empty = None
            
        _error_process = None
        
        print(f"✓ Voice recording transcribed and analyzed successfully")
        print(f"  File: {file_path}")
        print(f"  Transcription length: {len(transcription)} characters")
        print(f"  Preview: {transcription[:100]}..." if len(transcription) > 100 else f"  Text: {transcription}")
        print(f"  Agent analysis available: {len(agent_analysis)} characters")
    else:
        # Empty transcription
        status = "warning"
        message = "Transcription completed but no text was extracted"
        transcription = ""
        
        _info_process = "Processing completed with empty result"
        _info_transcription = None
        _warning_empty = "No text was transcribed from the audio file"
        _error_process = None
        
        print(f"⚠ No text transcribed from audio file")
        print(f"  File: {file_path}")
        
except Exception as e:
    status = "error"
    message = f"Error processing transcription: {str(e)}"
    transcription = ""
    agent_analysis = ""
    
    _info_process = None
    _info_transcription = None
    _warning_empty = None
    _error_process = f"Exception during processing: {str(e)}"
    
    print(f"✗ Error: {str(e)}")


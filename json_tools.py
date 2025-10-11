"""
Utility functions for handling JSON files.
"""

def resolve_json_file_path(filename):
    import os
    # If it's already an absolute path or contains path separators, use as-is
    if os.path.isabs(filename) or os.sep in filename or '/' in filename:
        if os.path.exists(filename):
            return filename
        else:
            raise FileNotFoundError(f"File not found: {filename}")
    
    # Check current directory first
    if os.path.exists(filename):
        return filename
    
    # Check json_samples directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_samples_path = os.path.join(script_dir, "json_samples", filename)
    
    if os.path.exists(json_samples_path):
        return json_samples_path
    
    # If not found in either location, raise FileNotFoundError
    raise FileNotFoundError(f"File '{filename}' not found in current directory or json_samples directory")
...

def load_json_file(file_path):
    import json, sys
    try:
        with open(file_path, "r") as f:
            file_content = f.read()
            if not file_content.strip():
                raise ValueError("The provided file is empty.")
            return json.loads(file_content)
    except ValueError as e:
        sys.exit(f"Error reading JSON file: {e}")
    except FileNotFoundError:
        sys.exit(f"File not found: {file_path}")
    except json.JSONDecodeError:
        sys.exit(f"Error decoding JSON from file: {file_path}")
    return
...

# Updated app.py for error handling

def process_data(data):
    if not data:
        raise ValueError("Data cannot be empty")
    # Existing processing logic goes here
    return processed_data

# Example use
try:
    process_data(data)
except ValueError as e:
    print(e)
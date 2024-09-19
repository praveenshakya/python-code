import requests
import pandas as pd

def call_api(api_name: str, base_url: str, endpoint: str, method: str, token: str = None, headers: dict = None, data: dict = None):
    """
    A generic function to call different APIs.
    
    Parameters:
    - api_name: str - Name or identifier for the API.
    - base_url: str - Base URL of the API.
    - endpoint: str - API endpoint.
    - method: str - HTTP method (GET, POST, etc.).
    - token: str - Optional authorization token.
    - headers: dict - Optional additional headers.
    - data: dict - Optional data for POST requests.
    """
    # Construct the full API URL
    api_url = f"{base_url}{endpoint}"
    
    # Add Authorization token to headers if provided
    if token:
        if headers is None:
            headers = {}
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        # Perform the request based on the method
        if method.upper() == 'GET':
            response = requests.get(api_url, headers=headers, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(api_url, headers=headers, json=data, timeout=10)
        else:
            print(f"Unsupported HTTP method: {method}")
            return None
        
        # Return response data
        return {
            'api_name': api_name,
            'status_code': response.status_code,
            'response_text': response.text[:100]  # Truncate for readability
        }

    except requests.exceptions.Timeout:
        print(f"Timeout occurred for API {api_name} ({api_url})")
    except Exception as e:
        print(f"Error calling API {api_name}: {e}")
        return None


# Example of calling the generic function for all APIs from the Excel sheet
file_path = '/mnt/data/Book1.xlsx'
excel_data = pd.read_excel(file_path)

# Define a token (this can be dynamic based on user input or environment)
auth_token = "your_token_here"

# Iterate over the rows of the Excel sheet
for index, row in excel_data.iterrows():
    api_name = row['NameofAPI']
    base_url = row['URL']
    endpoint = row['Endpoint']
    method = row['Method']

    # Optionally pass any additional headers or data
    headers = {'Content-Type': 'application/json'}  # Example header
    
    # Call the generic API function
    result = call_api(api_name, base_url, endpoint, method, token=auth_token, headers=headers)
    
    if result:
        print(f"API Name: {result['api_name']}, Status Code: {result['status_code']}")
        print(f"Response (truncated): {result['response_text']}...\n")

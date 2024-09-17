import os
import requests
from dotenv import load_dotenv
from urllib.parse import urljoin
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

class TheBrainAPI:
    """
    A class to interact with TheBrain API.
    """

    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.getenv('THEBRAIN_API_KEY')
        self.base_url = base_url or os.getenv('THEBRAIN_API_BASE_URL', 'https://api.thebrain.com/v1')

        if not self.api_key:
            raise ValueError("TheBrain API key is not set. Please check your environment variables.")

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def make_request(self, endpoint, method='GET', params=None, data=None):
        """
        Makes an HTTP request to TheBrain API.

        Parameters:
        - endpoint (str): The API endpoint.
        - method (str): HTTP method ('GET', 'POST', etc.).
        - params (dict): Query parameters.
        - data (dict): Request payload.

        Returns:
        - dict: JSON response if successful.
        - None: If an error occurred.
        """
        url = urljoin(self.base_url + '/', endpoint)
        try:
            response = requests.request(method, url, headers=self.headers, params=params, json=data)
            if response.status_code in (200, 201):
                return response.json()
            else:
                error_message = f"Error {response.status_code}: {response.text}"
                logging.error(error_message)
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None

    def create_thought(self, brain_id, thought_name, thought_description=None):
        """
        Creates a new thought in the specified brain.
        """
        endpoint = f'brains/{brain_id}/thoughts'
        data = {'name': thought_name}
        if thought_description:
            data['description'] = thought_description

        result = self.make_request(endpoint, method='POST', data=data)
        if result:
            logging.info(f"Thought '{thought_name}' created successfully.")
        else:
            logging.error(f"Failed to create thought '{thought_name}'.")
        return result

    def search_thoughts(self, brain_id, query):
        """
        Searches for thoughts in a brain.
        """
        endpoint = f'brains/{brain_id}/thoughts/search'
        params = {'query': query}

        result = self.make_request(endpoint, params=params)
        if result:
            logging.info(f"Search results for '{query}':")
            for thought in result.get('thoughts', []):
                logging.info(f" - {thought['name']} (ID: {thought['id']})")
        else:
            logging.error(f"Search failed for query '{query}'.")
        return result

    def get_thought_details(self, brain_id, thought_id):
        """
        Retrieves details about a specific thought.
        """
        endpoint = f'brains/{brain_id}/thoughts/{thought_id}'

        result = self.make_request(endpoint)
        if result:
            logging.info(f"Thought details for ID '{thought_id}':")
            logging.info(f"Name: {result['name']}")
            logging.info(f"Description: {result.get('description', 'No description available.')}")
        else:
            logging.error(f"Failed to retrieve details for thought ID '{thought_id}'.")
        return result

if __name__ == "__main__":
    # Initialize TheBrainAPI instance
    brain_api = TheBrainAPI()

    # Prompt user for brain ID
    brain_id = input("Enter your Brain ID: ").strip()

    # Create a new thought
    thought_name = 'AI Integration Test'
    thought_description = 'This is a test thought created via the AI Assistant.'
    brain_api.create_thought(brain_id, thought_name, thought_description)

    # Search for thoughts in the brain
    search_query = input("Enter your search query: ").strip()
    brain_api.search_thoughts(brain_id, search_query)

    # Get details of a specific thought
    thought_id = input("Enter the Thought ID to retrieve details: ").strip()
    brain_api.get_thought_details(brain_id, thought_id)

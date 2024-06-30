import time
import requests
import base64
import logging
from pycti import OpenCTIConnectorHelper, get_config_variable
import os

class LoboGuaraConnector:
    def __init__(self):
        config = {
            'opencti': {
                'url': os.getenv('OPENCTI_URL'),
                'token': os.getenv('OPENCTI_TOKEN')
            },
            'connector': {
                'id': os.getenv('CONNECTOR_ID'),
                'type': 'EXTERNAL_IMPORT',
                'name': 'Lobo Guara Connector',
                'scope': 'lobo-guara',
                'interval': int(os.getenv('LOBOGUARA_INTERVAL_SEC', 3600))
            }
        }
        self.helper = OpenCTIConnectorHelper(config)
        self.api_url = os.getenv('OPENCTI_URL')
        self.lobo_guara_url = os.getenv('LOBOGUARA_URL')
        self.token_url = os.getenv('LOBOGUARA_TOKEN_URL')
        self.username = os.getenv("LOBOGUARA_USERNAME")
        self.password = os.getenv("LOBOGUARA_PASSWORD")
        self.interval_sec = int(os.getenv("LOBOGUARA_INTERVAL_SEC", 3600))
        self.verify_ssl = os.getenv("LOBOGUARA_VERIFY_SSL", "true").lower() == "true"
        self.tlp_marking = os.getenv("LOBOGUARA_TLP", "TLP:AMBER")
        self.observable_score = int(os.getenv("LOBOGUARA_SCORE", 50))
        log_level = os.getenv("CONNECTOR_LOG_LEVEL", "INFO").upper()
        
        # Configure logging
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)
        
        if self.interval_sec < 600:
            raise ValueError("LOBOGUARA_INTERVAL_SEC must be at least 600 seconds")
        
        # Create organization "Lobo Guara"
        self.organization_id = self.create_organization()

    def get_token(self):
        auth_str = f"{self.username}:{self.password}"
        auth_bytes = auth_str.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Basic {auth_base64}"
        }
        response = requests.post(self.token_url, headers=headers, verify=self.verify_ssl)
        if response.status_code != 200:
            self.logger.error(f"Error getting token: {response.status_code} {response.text}")
            response.raise_for_status()
        return response.json().get("token")

    def fetch_certificates(self):
        token = self.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(self.lobo_guara_url, headers=headers, verify=self.verify_ssl)
        if response.status_code != 200:
            self.logger.error(f"Error fetching certificates: {response.status_code} {response.text}")
            response.raise_for_status()
        return response.json().get("monitored_certificate_domains", [])

    def get_or_create_label(self, label):
        query = """
        query Labels($search: String) {
          labels(search: $search) {
            edges {
              node {
                id
                value
              }
            }
          }
        }
        """
        variables = {"search": label}
        headers = {
            'Authorization': f'Bearer {self.helper.opencti_token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(
            f"{self.api_url}/graphql",
            json={'query': query, 'variables': variables},
            headers=headers
        )
        response_data = response.json()
        self.logger.info(f"Label query response for {label}: {response_data}")

        if 'data' in response_data and response_data['data']['labels']['edges']:
            return response_data['data']['labels']['edges'][0]['node']['id']
        else:
            mutation = """
            mutation LabelAdd($input: LabelAddInput!) {
              labelAdd(input: $input) {
                id
                value
              }
            }
            """
            variables = {"input": {"value": label}}
            response = requests.post(
                f"{self.api_url}/graphql",
                json={'query': mutation, 'variables': variables},
                headers=headers
            )
            response_data = response.json()
            self.logger.info(f"Label creation response for {label}: {response_data}")

            if 'errors' in response_data:
                self.logger.error(f"GraphQL errors while creating label: {response_data['errors']}")
                return None
            return response_data['data']['labelAdd']['id']

    def get_or_create_marking_definition(self, definition):
        query = """
        query MarkingDefinitions($search: String) {
          markingDefinitions(search: $search) {
            edges {
              node {
                id
                definition
              }
            }
          }
        }
        """
        variables = {"search": definition}
        headers = {
            'Authorization': f'Bearer {self.helper.opencti_token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(
            f"{self.api_url}/graphql",
            json={'query': query, 'variables': variables},
            headers=headers
        )
        response_data = response.json()
        self.logger.info(f"Marking definition query response for {definition}: {response_data}")

        if 'data' in response_data and response_data['data']['markingDefinitions']['edges']:
            return response_data['data']['markingDefinitions']['edges'][0]['node']['id']
        else:
            self.logger.error(f"Marking definition {definition} not found.")
            return None

    def create_organization(self):
        query = """
        query CheckOrganization($filters: [OrganizationsFiltering!]) {
            organizations(filters: $filters) {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
        }
        """
        variables = {
            "filters": [
                {"key": "name", "values": ["Lobo Guara"], "mode": "and"}
            ]
        }
        response = requests.post(
            f"{self.api_url}/graphql",
            json={'query': query, 'variables': variables},
            headers={
                'Authorization': f'Bearer {self.helper.opencti_token}',
                'Content-Type': 'application/json'
            }
        )
        result = response.json()

        if len(result.get('data', {}).get('organizations', {}).get('edges', [])) > 0:
            return result['data']['organizations']['edges'][0]['node']['id']

        mutation = """
        mutation CreateOrganization($input: OrganizationAddInput!) {
            organizationAdd(input: $input) {
                id
                name
            }
        }
        """
        variables = {
            "input": {
                "name": "Lobo Guara",
                "x_opencti_organization_type": "Other",
                "x_opencti_reliability": "A"
            }
        }
        response = requests.post(
            f"{self.api_url}/graphql",
            json={'query': mutation, 'variables': variables},
            headers={
                'Authorization': f'Bearer {self.helper.opencti_token}',
                'Content-Type': 'application/json'
            }
        )
        result = response.json()
        return result['data']['organizationAdd']['id']

    def create_observable(self, domain, certificate_id, register_date):
        if domain.startswith("*."):
            domain = domain[2:]

        labels = ["loboguara", "new_certificate"]
        label_ids = [self.get_or_create_label(label) for label in labels]
        marking_id = self.get_or_create_marking_definition(self.tlp_marking)

        query = """
        mutation StixCyberObservableCreationMutation(
          $type: String!
          $x_opencti_description: String
          $createdBy: String
          $objectMarking: [String]
          $objectLabel: [String]
          $x_opencti_score: Int
          $DomainName: DomainNameAddInput
        ) {
          stixCyberObservableAdd(
            type: $type
            x_opencti_description: $x_opencti_description
            createdBy: $createdBy
            objectMarking: $objectMarking
            objectLabel: $objectLabel
            x_opencti_score: $x_opencti_score
            DomainName: $DomainName
          ) {
            id
            standard_id
            entity_type
            observable_value
          }
        }
        """
        variables = {
            "type": "Domain-Name",
            "x_opencti_description": f"Certificate ID: {certificate_id}, Register Date: {register_date}",
            "createdBy": self.organization_id,
            "objectMarking": [marking_id] if marking_id else [],
            "objectLabel": label_ids,
            "x_opencti_score": self.observable_score,
            "DomainName": {
                "value": domain
            }
        }

        headers = {
            'Authorization': f'Bearer {self.helper.opencti_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            f"{self.api_url}/graphql",
            json={'query': query, 'variables': variables},
            headers=headers
        )

        response_data = response.json()
        self.logger.info(f"Observable creation response for {domain}: {response_data}")

        if 'errors' in response_data:
            self.logger.error(f"GraphQL errors: {response_data['errors']}")
        else:
            self.logger.info(f"Created domain observable in OpenCTI for domain: {domain}")
            self.logger.debug(f"Full response from OpenCTI: {response_data}")

    def run(self):
        while True:
            try:
                self.logger.info("Fetching certificates from Lobo Guará...")
                certificates = self.fetch_certificates()
                self.logger.info(f"Successfully fetched {len(certificates)} certificates:")
                for certificate in certificates:
                    domain = certificate['domain']
                    certificate_id = certificate['certificate_id']
                    register_date = certificate['register_date']
                    self.logger.info(f"- Domain: {domain}, Certificate ID: {certificate_id}, Register Date: {register_date}")
                    self.create_observable(domain, certificate_id, register_date)
            except Exception as e:
                self.logger.error(f"Error fetching certificates: {e}")
            time.sleep(self.interval_sec)

if __name__ == "__main__":
    try:
        connector = LoboGuaraConnector()
        connector.run()
    except Exception as e:
        print(f"Error initializing connector: {e}")

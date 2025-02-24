### Library Imports
import requests
import os
import json
import pandas as pd

# example from Rewiring America incentive API documentation
household_income = "80000"
household_size = "2"
zip_code = "98103"
owner_status = "homeowner"
tax_filing = "joint"

api_key = os.environ.get('REWIRING_AMERICA_API_KEY')

url = f"https://api.rewiringamerica.org/api/v1/calculator?household_income={household_income}&household_size={household_size}&zip={zip_code}&owner_status={owner_status}&tax_filing={tax_filing}&language=en&include_beta_states=false"

headers = {"Authorization": f"Bearer {api_key}"}

response = requests.get(url, headers=headers)

data = json.loads(response.text)

incentives_df = pd.DataFrame(data["incentives"])

# dateframe of incentives available
print(incentives_df.head())
# import os
# import braintrust
#
# os.environ["BRAINTRUST_API_KEY"] = "sk-a0kjYiK0WiMPqc644epprVD7DtcO8Xr6Wf1DgbYb78FREJmI"
#
# result = braintrust.invoke(
#   project_name="Retool_Rp",
#   slug="hotel-enrichment-domainandpublicemails-63f7",
#   input={
#     "ADDRESS": "109 Leoforos Alexandrou Papanastasiou, Piraeus, 18533, Greece",
#     "HOTEL_NAME": "The Alex Monte Kastella",
#     "STAR_RATING": 4
#   },
#   messages=[
#     {
#       "role": "user",
#       "content": "Process this hotel information",
#     }
#   ],
# )
#
# print(result)

import os, json, requests

API = "https://api.braintrust.dev/v1"
API_KEY = "sk-a0kjYiK0WiMPqc644epprVD7DtcO8Xr6Wf1DgbYb78FREJmI"  # rotate your key first!

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

project_name = "Retool_Rp"
slug = "hotel-enrichment-domainandpublicemails-63f7"

# 1) Look up the prompt to get its id
r = requests.get(f"{API}/prompt", headers=headers, params={
    "project_name": project_name,
    "slug": slug,
    "limit": 1
})
r.raise_for_status()

# Parse response with proper error handling
response_data = r.json()
print("API Response:", json.dumps(response_data, indent=2))

# Try to extract the prompt data from 'objects' field
items = response_data.get("objects", [])
if not items:
    # Fallback: check if there's a 'data' field (alternative API structure)
    items = response_data.get("data", [])

if not items:
    raise ValueError(f"No prompts found for project '{project_name}' with slug '{slug}'")

prompt = items[0] if isinstance(items, list) else items

# Validate that prompt has an 'id' field
if not isinstance(prompt, dict) or "id" not in prompt:
    raise ValueError(f"Invalid prompt structure. Expected dict with 'id' field, got: {prompt}")

prompt_id = prompt["id"]
print(f"Found prompt ID: {prompt_id}")

# 2) Patch: set Gemini model + add Google Search tool under params
payload = {
  "prompt_data": {
    "options": {
      "model": "gemini-2.5-flash",
      "params": {
        # keep the knobs you’re using; example mirrors your UI (temp 0, topP 0.7)
        "temperature": 0,
        "topP": 0.7,
        # 👇 enables Google Search grounding
        "tools": [ { "google_search": {} } ]
      }
    }
  }
}

r2 = requests.patch(f"{API}/prompt/{prompt_id}", headers=headers, data=json.dumps(payload))
r2.raise_for_status()
print("Updated prompt version:", r2.json().get("prompt_data", {}).get("origin", {}))

# 3) Invoke the prompt with input data and messages
invoke_payload = {
    "project_name": project_name,
    "slug": slug,
    "input": {
        "address": "109 Leoforos Alexandrou Papanastasiou, Piraeus, 18533, Greece",
        "name": "The Alex Monte Kastella",
        "rating": 4
    },
    "messages": [
        {
            "role": "user",
            "content": "Process this hotel information"
        }
    ]
}

r3 = requests.post(f"{API}/invoke", headers=headers, data=json.dumps(invoke_payload))
r3.raise_for_status()
result = r3.json()
print("\nInvoke Result:", json.dumps(result, indent=2))

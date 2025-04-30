import requests

def get_studies_for_company(company_name, fields, max_results=500):
    """Fetch studies related to a company by querying the ClinicalTrials.gov Data API."""
    studies = []

    API_ENDPOINT = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.spons": company_name,
        "fields": ",".join(fields),
        "pageSize": max_results,
        "format": "json"
    }

    response = requests.get(API_ENDPOINT, params=params)
    print(f"Request URL: {response.url}")  # Debugging information
    if response.status_code == 200:
        data = response.json()
        print(f"Response Data: {data}")  # Debugging information
        studies.extend(data.get('studies', []))
    else:
        print(f"Failed to fetch studies for {company_name}: {response.status_code}")
        print(response.text)

    return studies



# Specify fields recognized by the API for retrieval
fields = [
    "NCTId", "BriefTitle", "InterventionName", "Condition",
    "StudyType", "OverallStatus", "Phase", "EnrollmentCount",
    "LeadSponsorName", "ResultsFirstPostDate", "StartDate", "CompletionDate",
    "LastUpdatePostDate", "LocationFacility", "PrimaryOutcomeMeasure", "LocationStatus",
    "ResponsiblePartyInvestigatorAffiliation", "CollaboratorName", "OverallOfficialAffiliation"
]

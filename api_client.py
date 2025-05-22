import requests
import time # Recommended for adding small delays if hitting API limits frequently

# Specify fields recognized by the API for retrieval
# This list is taken from your original file. Verify it against the
# "Study Data Structure" document if you need to make changes.
#
fields = [
    "NCTId", "BriefTitle", "InterventionName", "Condition",
    "StudyType", "OverallStatus", "Phase", "EnrollmentCount",
    "LeadSponsorName", "ResultsFirstPostDate", "StartDate", "CompletionDate",
    "LastUpdatePostDate", "LocationFacility", "PrimaryOutcomeMeasure", "LocationStatus",
    "ResponsiblePartyInvestigatorAffiliation", "CollaboratorName", "OverallOfficialAffiliation"
]

API_ENDPOINT = "https://clinicaltrials.gov/api/v2/studies"

def get_studies_for_company(company_name, field_list, page_size=100):
    """
    Fetch studies related to a company by querying the ClinicalTrials.gov Data API,
    implementing pagination and a 'contains' search for the company name in
    LeadSponsorName, CollaboratorName, and OrgFullName fields.
    """
    all_studies = []
    next_page_token = None
    page_count = 0

    # If company_name might contain spaces or special characters,
    # ensure it's properly quoted for the API query.
    # For simple names, this might not be strictly necessary, but it's safer.
    # As per "Constructing Complex Search Queries", phrases are quoted.
    #
    quoted_company_name = f'"{company_name}"' if ' ' in company_name else company_name

    # Construct the query expression to search for the company name within specific fields.
    # This uses information from "Search Areas" and "Constructing Complex Search Queries" documents.
    #
    # It targets LeadSponsorName, CollaboratorName, and OrgFullName as identified in the
    query_expression = (
        f"(AREA[LeadSponsorName] COVERAGE[Contains] {quoted_company_name}) OR "
        f"(AREA[CollaboratorName] COVERAGE[Contains] {quoted_company_name}) OR "
        f"(AREA[OrgFullName] COVERAGE[Contains] {quoted_company_name}) OR "
        f"(AREA[LocationFacility] COVERAGE[Contains] {quoted_company_name})"  # Added location search
    )

    print(f"Fetching studies for '{company_name}' using query: {query_expression}")

    while True:
        page_count += 1
        params = {
            "query.term": query_expression,
            "fields": ",".join(field_list),
            "pageSize": page_size,
            "format": "json"
        }
        if next_page_token:
            params["pageToken"] = next_page_token

        # print(f"Requesting Page {page_count} - URL: {requests.Request('GET', API_ENDPOINT, params=params).prepare().url}")

        try:
            response = requests.get(API_ENDPOINT, params=params, timeout=30) # Added timeout
            response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)

            data = response.json()
            # print(f"Page {page_count} - Response Data Snippet: {str(data)[:200]}") # Debugging

            current_studies = data.get('studies', [])
            if current_studies:
                all_studies.extend(current_studies)
                print(f"Page {page_count}: Fetched {len(current_studies)} studies. Total fetched so far: {len(all_studies)}")
            else:
                print(f"Page {page_count}: No studies found on this page.")


            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                print("No more pages to fetch.")
                break
            else:
                print(f"Next page token found: {next_page_token[:20]}...")
                # Optional: Add a small delay to be polite to the API
                # time.sleep(0.5)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
            print(f"Response content: {response.text}")
            break # Exit loop on HTTP error
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            break # Exit loop on other request errors
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


    if not all_studies:
         print(f"No studies found for '{company_name}' with the given criteria after checking all pages.")
    else:
        print(f"Finished fetching. Total studies retrieved for '{company_name}': {len(all_studies)}")
    return all_studies

# Example of how you might call this from elsewhere (e.g., your main.py)
# if __name__ == '__main__':
# company_to_search = "Biofortis" # Or another company name
# print(f"Globally defined fields: {fields}")
#    studies_data = get_studies_for_company(company_to_search, fields, page_size=50) # Use a smaller page size for testing if needed
#    if studies_data:
#        print(f"\nSuccessfully fetched {len(studies_data)} studies for {company_to_search}.")
# for i, study in enumerate(studies_data[:3]): # Print details of the first 3 studies
#            print(f"\nStudy {i+1}:")
#            print(f"  NCTId: {study.get('protocolSection', {}).get('identificationModule', {}).get('nctId', 'N/A')}")
#            print(f"  BriefTitle: {study.get('protocolSection', {}).get('identificationModule', {}).get('briefTitle', 'N/A')}")
#            print(f"  LeadSponsorName: {study.get('protocolSection', {}).get('sponsorCollaboratorsModule', {}).get('leadSponsor', {}).get('name', 'N/A')}")
#            collaborators = study.get('protocolSection', {}).get('sponsorCollaboratorsModule', {}).get('collaborators', [])
# if collaborators:
#                print(f"  Collaborators: {', '.join([collab.get('name', 'N/A') for collab in collaborators])}")
# else:
# print("No studies data returned.")
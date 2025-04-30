import requests
def parse_api_response(response):
    """Parse and filter relevant information from the API response."""
    filtered_data = []
    for study in response:
        protocol = study.get('protocolSection', {})
        print(f"Protocol Section: {protocol}")  # Debugging information
        identification = protocol.get('identificationModule', {})
        status = protocol.get('statusModule', {})
        sponsor = protocol.get('sponsorCollaboratorsModule', {})
        conditions = protocol.get('conditionsModule', {})
        design = protocol.get('designModule', {})
        arms = protocol.get('armsInterventionsModule', {})
        outcomes = protocol.get('outcomesModule', {})
        contacts = protocol.get('contactsLocationsModule', {})

        filtered_data.append({
            'NCT Number': identification.get('nctId', ''),
            'Title': identification.get('briefTitle', ''),
            'Study Status': status.get('overallStatus', ''),
            'Sponsor Name': sponsor.get('leadSponsor', {}).get('name', ''),
            'Collaborator': ", ".join([collab.get('name', '') for collab in sponsor.get('collaborators', [])]),
            'Condition': ", ".join(conditions.get('conditions', [])),
            'Study Type': design.get('studyType', ''),
            'Phase': ", ".join(design.get('phases', [])),
            'Enrollment Number': design.get('enrollmentInfo', {}).get('count', ''),
            'Intervention/Treatment': ", ".join([intervention.get('interventionName', '') for intervention in arms.get('interventions', [])]),
            'Primary Outcome Measure': ", ".join([outcome.get('primaryOutcomeMeasure', '') for outcome in outcomes.get('primaryOutcomes', [])]),
            'Location Facility': ", ".join([location.get('locationFacility', '') for location in contacts.get('locations', [])]),
            'Responsible Party Affiliation': contacts.get('overallOfficials', [{}])[0].get('officialAffiliation', ''),
            'Start Date': status.get('startDateStruct', {}).get('startDate', ''),
            'Completion Date': status.get('completionDateStruct', {}).get('completionDate', ''),
            'Last Update Post Date': status.get('lastUpdatePostDateStruct', {}).get('lastUpdatePostDate', ''),
        })
    return filtered_data

# data_processor.py

def format_study_data(studies):
    formatted_data = []
    for study in studies:
        protocol = study.get('protocolSection', {})
        identification = protocol.get('identificationModule', {})
        status = protocol.get('statusModule', {})
        sponsor = protocol.get('sponsorCollaboratorsModule', {})
        conditions = protocol.get('conditionsModule', {})
        design = protocol.get('designModule', {})
        interventions = protocol.get('armsInterventionsModule', {})
        outcomes = protocol.get('outcomesModule', {})
        locations = protocol.get('contactsLocationsModule', {})

        formatted_study = {
            "NCT Number": identification.get('nctId', ''),
            "Study Status": status.get('overallStatus', ''),
            "Sponsor Name": sponsor.get('leadSponsor', {}).get('name', ''),
            "Collaborator": ', '.join([collaborator.get('name', '') for collaborator in sponsor.get('collaborators', [])]),
            "Title": identification.get('briefTitle', ''),
            "Phase": ', '.join(design.get('phases', [])),
            "Intervention/Treatment": ', '.join([intervention.get('name', '') for intervention in interventions.get('interventions', [])]),
            "Enrollment Number": design.get('enrollmentInfo', {}).get('count', ''),
            "Condition/Disease": ', '.join(conditions.get('conditions', [])),
            "Last Update Post Date": status.get('lastUpdatePostDateStruct', {}).get('date', ''),
            "Results First Post Date": status.get('resultsFirstPostDateStruct', {}).get('date', ''),
            "Location": ', '.join([location.get('facility', '') for location in locations.get('locations', [])]),
            "Location Status": ', '.join([location.get('status', '') for location in locations.get('locations', [])]),
            "Study Start Date": status.get('startDateStruct', {}).get('date', ''),
            "Study Completion Date": status.get('completionDateStruct', {}).get('date', ''),
            "Primary Endpoint": ', '.join([outcome.get('measure', '') for outcome in outcomes.get('primaryOutcomes', [])]),
            "Investigator": sponsor.get('responsibleParty', {}).get('investigatorAffiliation', ''),
            "Affiliation": ', '.join([official.get('affiliation', '') for official in locations.get('overallOfficials', [])])
        }
        formatted_data.append(formatted_study)
    print(f"Formatted Data: {formatted_data}")  # Debugging information
    return formatted_data




# Use this function in the get_studies_data_for_company function
def get_studies_data_for_company(company):
    # Construct the request URL
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.spons": company,
        "fields": "NCTId,BriefTitle,InterventionName,Condition,StudyType,OverallStatus,Phase,EnrollmentCount,LeadSponsorName,ResultsFirstPostDate,StartDate,CompletionDate,LastUpdatePostDate,LocationFacility,PrimaryOutcomeMeasure,LocationStatus,ResponsiblePartyInvestigatorAffiliation,CollaboratorName,OverallOfficialAffiliation",
        "pageSize": 500,
        "format": "json"
    }
    response = requests.get(base_url, params=params)
    response_data = response.json()
    print(f"Request URL: {response.url}")
    print(f"Response Data: {response_data}")

    # Parse the response data
    studies = response_data.get('studies', [])
    formatted_data = format_study_data(studies)
    return formatted_data





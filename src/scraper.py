from datetime import datetime
from bs4 import BeautifulSoup  # To clean HTML tags
from db import db, Event, Organization  # Importing models from your db.py
import requests

# Scraper function to fetch and process events
def scrape_events():
    """Scrape events and save them to the database."""
    try:
        url = "https://cornell.campusgroups.com/mobile_ws/v17/mobile_events_list?range=0&limit=40&filter4_contains=OR&filter4_notcontains=OR&order=undefined&search_word=&&1733532882139"
        response = requests.get(url)
        events_data = response.json()
        for item in events_data:
            try:
                name = item.get("p3")
                if name == "False" or item.get("p5") == "Private Event":
                    continue
                event = Event.query.filter_by(name=name).first()
                if event:
                    continue
                location = item.get("p6")
                organization_name = item.get("p9")

                # Extract description from event url
                event_url = "https://cornell.campusgroups.com/crea" + item.get("p18")
                event_response = requests.get(event_url)
                soup = BeautifulSoup(event_response.content, "html.parser")
                event_details = soup.find('div', attrs = {'id':'event_details'})
                event_details_block = event_details.find('div', attrs={'class':'card-block'})
                unwanted = event_details_block.find_all('div')
                for elem in unwanted:
                    elem.extract()
                description = event_details.get_text().strip()

                # Extract date and time using different formats
                formats = ["%a, %b %d, %Y %I:%M %p", "%a, %b %d, %Y%I:%M %p", "%a, %b %d, %Y %I %p", "%a, %b %d, %Y%I %p", "%I:%M %p", "%I %p"]
                clean_date = BeautifulSoup(item.get("p4"), "html.parser").get_text()
                date_time = clean_date.split("\u2013") # Use \u2013 for &ndash;
                start_date = None
                start_time = None
                end_date = None
                end_time = None
                for format in formats:
                    try: 
                        start_date = datetime.strptime(date_time[0].strip(), format).date()
                        start_time = datetime.strptime(date_time[0].strip(), format).time()
                        break
                    except ValueError:
                        continue
                for format in formats:
                    try: 
                        end_date = datetime.strptime(date_time[1].strip(), format).date()
                        end_time = datetime.strptime(date_time[1].strip(), format).time()
                        break
                    except ValueError:
                        continue
                if end_date is None or end_date == datetime(1900, 1, 1).date():
                    end_date = start_date
                time_zone = item.get("p28")

                # Find or create the organization
                organization = Organization.query.filter_by(name=organization_name).first()
                if not organization:
                    organization = Organization(name=organization_name, org_type="Unknown")
                    db.session.add(organization)
                    db.session.commit()

                # Create the event object
                event = Event(
                    name=name,
                    start_date=start_date,
                    start_time=start_time,
                    end_date=end_date,
                    end_time=end_time,
                    timezone = time_zone,
                    location=location,
                    description=description,
                    event_url=event_url,
                    organization_id=organization.id
                )
                db.session.add(event)
                db.session.commit()
            
            except Exception as e:
                continue

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:
        print(f"JSON parsing error: {e}")

if __name__ == "__main__":
    scrape_events()

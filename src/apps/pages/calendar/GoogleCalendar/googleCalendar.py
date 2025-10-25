
import streamlit as st
import os
import pickle
from datetime import datetime, timedelta, time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
import pytz
import requests

COMMON_TIMEZONE = [
    'UTC',
    'Africa/Lagos',
    'Asia/Kolkata',
    'Europe/London',
    'America/New_York',
    'Asia/Tokyo',
    'Australia/Sydney',
]


CLIENT_ID = st.secrets["auth"]["google"]["client_id"]
CLIENT_SECRET = st.secrets["auth"]["google"]["client_secret"]
REDIRECT_URI = st.secrets["google_calendar"]["redirect_uri"]
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/calendar",
    "openid",
]
TOKEN_DIR = "tokens"
os.makedirs(TOKEN_DIR, exist_ok=True)

def get_auth_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def fetch_user_email(credentials):
    """Fetch the user's email from the credentials."""
    try:
        token = credentials.token
        resp = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token}"}
        )
        if resp.status_code == 200:
            return resp.json().get("email")
    except Exception as e:
        st.error(f"Failed to get user email: {e}")
    return None

def save_credentials(email, credentials):
    path = os.path.join(TOKEN_DIR, f"{email}.pkl")
    with open(path, "wb") as f:
        pickle.dump(credentials, f)

def load_credentials(email):
    path = os.path.join(TOKEN_DIR, f"{email}.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def get_google_calendar_service():
    query_params = st.query_params
    user_email = st.session_state.get("user_email")
    if "code" in query_params and not user_email:
        flow = get_auth_flow()
        try:
            flow.fetch_token(code=query_params["code"])
            credentials = flow.credentials
            email = fetch_user_email(credentials)
            if email:
                save_credentials(email, credentials)
                st.session_state.user_email = email
                st.session_state['show_auth_toast'] = True
                st.rerun()
            else:
                st.error("Failed to retrieve user email.")
        except Exception as e:
            st.error(f"Auth error: {e}")
        return None

    #Use stored credentials if available
    if user_email:
        credentials = load_credentials(user_email)
        if credentials:
            return build("calendar", "v3", credentials=credentials)
        else:
            st.warning("Session expired or no token found.")
            del st.session_state.user_email
            st.rerun()

    #Begin new OAuth flow
    flow = get_auth_flow()
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline", include_granted_scopes="true")
    st.write(f"""
        <p>
            🔐 <a href="{auth_url}" target="_self">Click here to authorize Google Calendar access</a>
        </p>
    """, unsafe_allow_html=True)
    st.stop()



def create_event(service, summary, start_time, duration_minutes, timezone_str):
    end = start_time + timedelta(minutes=duration_minutes)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': timezone_str},
        'end': {'dateTime': end.isoformat(), 'timeZone': timezone_str},
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event

def list_upcoming_events(service, timezone_str='Asia/Kolkata', max_results=5):
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz).isoformat()
    events_result = service.events().list(
        calendarId='primary', timeMin=now, maxResults=max_results,
        singleEvents=True, orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

def delete_event(service, event_id):
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    return True

def update_event(
    service,
    event_id,
    summary=None,
    start_time=None,
    duration_minutes=None,
    timezone="Asia/Kolkata"
):
    
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    end_time = start_time + timedelta(minutes=duration_minutes)

    if summary:
        event['summary'] = summary
    if start_time:
        event["start"] = {
            "dateTime": start_time.isoformat(),
            "timeZone": timezone,
        }
    if end_time:
        event['end'] = {
            "dateTime": end_time.isoformat(),
            "timeZone": timezone,
        }
    
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    return updated_event.get("htmlLink")
    
def get_event_id_by_summary(service, summary, max_results=50):
    events = list_upcoming_events(service, max_results=max_results)
    for event in events:
        if event['summary'].lower() == summary.lower():
            return event['id']
        return None

def googleCalendar():
    st.set_page_config(page_title="Google Calendar Manager", layout="centered")

    service = get_google_calendar_service()
    if "events_loaded" not in st.session_state:
        st.session_state["events_loaded"] = False
    if "deleted_event_id" not in st.session_state:
        st.session_state["deleted_event_id"] = None

    if st.session_state.get('show_auth_toast'):
        st.toast("✅ Google Calendar authorization complete!", icon="🎉")
        del st.session_state['show_auth_toast']


    if service:
        st.title("📅 Google Calendar Event")
        timezone_str = st.selectbox("🌍 Select Your Timezone", COMMON_TIMEZONE, index=COMMON_TIMEZONE.index("Asia/Kolkata"))
        timezone = pytz.timezone(timezone_str)

        st.header("➕ Add New Event")
        summary = st.text_input("Event Title")
        date_part = st.date_input("Start Date")
        time_part = st.time_input("Start Time", value=time(9, 0))
        duration = st.number_input("Duration (minutes)", min_value=15, step=15)

        if st.button("Create Event"):
            naive_start = datetime.combine(date_part, time_part)
            timezone = pytz.timezone(timezone_str)
            aware_start = timezone.localize(naive_start)
            event = create_event(service, summary, aware_start, duration, timezone_str)
            st.success(f"Event created: [View in Calendar]({event['htmlLink']})")
        
        st.subheader("📋 Upcoming Events")
        if st.button("Load Events"):
            st.session_state["events_loaded"] = True
            st.session_state["deleted_event_id"] = None
        
        if st.session_state["events_loaded"]:
            events = list_upcoming_events(service, timezone_str=timezone_str)
            if not events:
                st.info("No upcoming events.")
            else:
                for event in events:
                    event_id = event['id']
                    if event_id == st.session_state["deleted_event_id"]:
                        continue

                    st.markdown(
                        """
                        <hr style="
                            border: none;
                            height: 1px;
                            background-color: #333;
                            margin-top: 16px;
                            margin-bottom: 16px;
                        ">
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(f"### {event.get('summary', '(No Title)')}")
                    start_raw = event['start'].get('dateTime', event['start'].get('date'))
                    try:
                        start_dt = datetime.fromisoformat(start_raw.replace("Z", "+00:00"))
                        readable_time = start_dt.strftime("%A, %B %d, %Y at %I:%M %p")
                    except Exception:
                        readable_time = start_raw

                    st.markdown(f"🕒 {readable_time}")

                    with st.form(key=f"form_{event['id']}", clear_on_submit=True):
                        col1, col2 = st.columns([5, 1])

                        with col1:

                            st.markdown(
                                f"""
                                
                                <a href="{event['htmlLink']}" target="_blank" style="
                                    text-decoration: none;
                                    background-color: #0F9D58;
                                    color: white;
                                    padding: 8px 14px;
                                    border-radius: 8px;
                                    font-weight: 600;
                                    display: inline-block;
                                    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                                    transition: background-color 0.3s ease;
                                " onmouseover="this.style.backgroundColor='#0c7a43'" onmouseout="this.style.backgroundColor='#0F9D58'">
                                    📅 View in Google Calendar
                                </a>
                                
                                """,
                                unsafe_allow_html=True
                            )
                        
                        with col2:
                            submit = st.form_submit_button(label="🗑️ Delete", use_container_width=True)

                        if submit:
                            delete_event(service, event['id'])
                            st.session_state["deleted_event_id"] = event_id
                            st.warning(f"Deleted: {event['summary']}")
                            st.rerun()
        
        st.subheader("✏️ Update Event")
        events = list_upcoming_events(service, max_results=50, timezone_str=timezone_str)

        if not events:
            st.info("No upcoming events found to update.")
        else:
            event_options = {f"{event['summary']}": event['id'] for event in events}
            selected_event_label = st.selectbox("Select Event to Update", list(event_options.keys()))
            selected_event_id = event_options[selected_event_label]
            new_title = st.text_input("New Title (optional)")
            new_date = st.date_input("New Event Date", key="update_date")
            new_start = st.time_input("Start Time", value=time(9, 0), key="update_start")
            new_duration = st.number_input("Duration (minutes)", min_value=15, step=15, key="update_end")


            if st.button("Update Event"):
                try:
                    new_start_dt = timezone.localize(datetime.combine(new_date, new_start))
                    updated_link = update_event(
                        service,
                        selected_event_id,
                        summary=new_title,
                        start_time=new_start_dt,
                        duration_minutes=new_duration,
                        timezone=timezone_str
                    )
                    st.success(f"✅ Event updated! [View it here]({updated_link})")
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
        

                
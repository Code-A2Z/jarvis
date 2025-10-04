from datetime import datetime

import pytz


def GreetUser(name):
  india_tz = pytz.timezone("Asia/Kolkata")
  hour = datetime.now(india_tz).hour
  if 5 <= hour < 11:
    return f"Good Morning, {name}"
  elif 11 <= hour < 17:
    return f"Good Afternoon, {name}"
  elif 17 <= hour < 21:
    return f"Good Evening, {name}"
  return f"Good Night, {name}"

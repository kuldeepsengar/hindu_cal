from jhora.panchanga import drik
from jhora.horoscope.chart import charts
from jhora import utils, const
from datetime import datetime, timedelta
import json

start_date = datetime.today()
num_days = 30  # Generate for 30 days

lunar_months = {
    0: "Chaitra",
    1: "Vaishakha",     
    2: "Jyeshtha",
    3: "Ashadha",
    4: "Shravana",
    5: "Bhadrapada",
    6: "Ashwin",
    7: "Kartika",
    8: "Margashirsha",
    9: "Pushya",
    10: "Magha",
    11: "Phalguna"
}


systems = {
        "Amanta": False,
        "Purnimanta": True,
    }

def generate_cal():
    """
    Generate a calendar for the next 30 days with tithi events.
    """
    for sys in systems:
        print(f"Generating calendar for {sys} system...")
        generate_calendar_for_system(sys)
            
    

def generate_calendar_for_system(system):    
    tithi = get_tithi(start_date, systems[system])  # Example coordinates for Shillong, India
    if tithi:
      data = {
          "summary": tithi['name'],
          "month": lunar_months[tithi['month']],
          "day": tithi['day'],
          "year": tithi['year'],
          "tithi": tithi['name'],
          "paksha": tithi['paksha'],
          "date": start_date.strftime("%Y-%m-%d"),
      }
      with open(f"docs/{system}/{start_date.year}_{start_date.month}_{start_date.day}.json","w") as f:
          json.dump(data, f, indent=2)  
      
      with open(f"docs/{system}/today.json","w") as f:
          json.dump(data, f, indent=2)  
    

def get_tithi(date_dt, is_purnimanta=False):
    place = drik.Place('shillong',25.569, 91.883, +5.5)
    date = utils.gregorian_to_jd(drik.Date(date_dt.year, date_dt.month, date_dt.day))
    # Create a Jhora object with the given date and place
    tithi = drik.lunar_month_date(date, place, is_purnimanta)    
    tithi_names = [
        "Purnima/Amavasya", "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami",
        "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi"]
    paksha_icons = {"Shukla": "🌔", "Krishna": "🌘"}
    special_icons = {"Purnima": "🌕", "Amavasya": "🌑"}  # Full moon and new moon


    paksha_names = ["Krishna","Shukla", "Krishna","Shukla"] if is_purnimanta else ["Shukla","Krishna", "Shukla","Krishna"]
    tithi_num = tithi[1] % 15
    # print(f"tithi: {tithi[1] // 15}")
    paksha = paksha_names[tithi[1] // 15]
    paksha_icon = paksha_icons[paksha]

    tithi_name = tithi_names[tithi_num if tithi_num < 14 else 14]
    
    # For tithi 0 we need to check
    
    # For tithi 14, decide Purnima or Amavasya
    if (tithi_num == 0):
        tithi_name = "Amavasya" if paksha == "Shukla" else "Purnima"
        paksha_icon = special_icons[tithi_name]
    return {"name": f"{tithi_name}", "month": tithi[0]-1, "day": tithi[1], "year": tithi[2], "paksha": paksha, "paksha_icon": paksha_icon}


if __name__ == "__main__":
    # get_tithi(start_date, 25.569, 91.883)
    generate_cal()
    print("Tithi calendar generated successfully.")
    # This will create a file named 'tithi_events.ics' with the tithi events for the next 30 days.
    # You can then import this file into any calendar application that supports ICS format.
    # For example, Google Calendar, Outlook, etc.
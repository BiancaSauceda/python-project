# our main program file!
# As long as we have our Flask setup initialized inside main.py (with app = Flask(__name__) and a few
# route definitions), there’s no need to create a separate app.py!

# importing Python's built-in calendar module, which contains classes like HTMLCalendar to make calendar data 
# & HTML markup.
import calendar
import datetime
import random  # new addition to enable random quote selection!

# importing Flask (the main class used to create the app) & render_template (links html files w/ Python logic &
# renders dynamic content).
from flask import Flask, render_template

# initializing the Flask app instance & the __name__ var ensure the app knows where it's running (helps when
# importing/deploying).
app = Flask(__name__)

# creating a custom calendar class based on HTMLCalendar from the calendar module!
# it will override the formatday() method so we can style the current day differently with a CSS class!
class StyledCalendar(calendar.HTMLCalendar):
    def __init__(self, firstweekday=6):
        # initializing the calendar with Sunday as the first day of the week!
        super().__init__(firstweekday)
        # grabbing today’s date so we can check each cell against it!
        self.today = datetime.date.today()

    def formatday(self, day, weekday):
        # calendar module uses 0 to represent padding days (blank cells), so we add a non-breaking space
        if day == 0:
            return '<td class="noday">&nbsp;</td>'

        # constructing a date object for the current cell to compare against today!
        current_day = datetime.date(self.today.year, self.today.month, day)

        # Add special class if the day matches today, so we can style it in CSS!
        if current_day == self.today:
            return f'<td class="today {self.cssclasses[weekday]}">{day}</td>'
        else:
            return f'<td class="{self.cssclasses[weekday]}">{day}</td>'

# home route definition - decorator @app.route("/") tells Flask to run this func when root URL (/) is accessed
# the home() func defines what happens when a user visits the site’s home page!
@app.route("/")
def home():
    # --- Calendar Setup ---
    # creating an HTMLCalendar object with Sunday as the first day of the week!
    cal = StyledCalendar(firstweekday=6)
    # generating an html <table> for July 2025 using the formatmonth() method. The html is then stored as a
    # string in html_calendar!
    html_calendar = cal.formatmonth(2025, 7)

    # --- Inspirational Quote Setup ---
    # defining a list of short motivational quotes to randomly display each page refresh!
    quotes = [
        "Progress lives in every bug you fix.",
        "Code boldly — the magic’s in the mess.",
        "You’re not stuck; you’re just pre-compile brilliance."
    ]
    # randomly selecting one quote from the list for dynamic inspiration!
    quote = random.choice(quotes)

    # rendering index.html from the templates folder, passing both the calendar & quote to the template.
    # Access calendar with {{ calendar_html | safe }} and quote with {{ quote }} in html!
    return render_template("index.html", calendar_html=html_calendar, quote=quote)

# runs the Flask development server when the script is executed directly.
# debug=True enables automatic restarts and helpful error messages during development!
if __name__ == "__main__":
    app.run(debug=True)

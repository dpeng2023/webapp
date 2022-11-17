# from calc_stats import calc_mph
# - from terminal venv in Intellij
# $ sudo -H python3.10 -m pip3.10 install flask
from flask import Flask, render_template, request, escape, Markup
from calc_stats import calc_time_per_mile

from DBcm import UseDatabase;

app = Flask(__name__)

app_log = 'calc_stats.log'

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'admin',
                          'password': 'G0FwdM@m@',
                          'database': 'crosscountryDB', }

def db_race_log(first_name, last_name, grade, race, miles, sec_per_race, sec_per_mile) -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into race_log
                  (first_name, last_name, grade, race, miles, sec_per_race, sec_per_mile)
                  values
                  (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (first_name, last_name, grade, race, miles, sec_per_race, sec_per_mile))

#TEST4 writes flask request and result details to the app's log file
#TODO:  add exception-handling
def log_request(req: 'flask_request', race_result: tuple) -> None:
    # with context will close automatically at the end of suite
    with open(app_log, 'a') as log:
        print(req.form, req.remote_addr, req.user_agent.browser, race_result, file=log, sep='|')

#TEST5 loads data from the app's log file
#TODO:  add exception-handling
def load_log(infile:str)->'list of lists':
    table = []
    # with context will close automatically at end of suite
    with open(infile) as log:
        for line in log:
            esc_line = escape(line)
            columns = esc_line.split('|')
            # TODO:  serialize dict and tuple from string with literal_eval from ast
            """
            print("DEBUG HERE 1")
            race_entry = Markup(columns[0]).unescape()
            race_results = Markup(columns[3]).unescape()
            print('race_entry is:  ', race_entry)
            print('race_results is:  ', race_results)
            race_entry = dict(race_entry)
            race_results = tuple(race_results)
            print("race_entry is:  ", race_entry['in_last_name'])
            print("race results is:  ", race_results[0])
            """
            table.append(columns)
    return table

#TEST1
"""
@app.route('/')
def hello() -> str:
    return 'Hello World from Flask!'
"""

#TEST2 Input data from prior GET request via HTML Form
@app.route('/')
@app.route('/entry')
def capture_racer_results() -> 'html':
    return render_template('entry.html',
                           out_title='Welcome to the Bayside Cross Country Stats Master!')


#TEST3 Output results from prior POST request action from HTML Form
@app.route('/mile_time', methods=['POST'])
def do_calc_mile_time() -> 'html':
    try:
        first_name = request.form['in_first_name']
        last_name = request.form['in_last_name']
        race = request.form['in_race']
        miles = request.form['in_miles']
        minutes = request.form['in_minutes']
        seconds = request.form['in_seconds']
        grade = request.form['in_grade']
    except Exception as err:
        err_str = "INPUT ERROR:  All fields (including grade) are required input.  Try again at '/entry'"
        print('********** do_calc_mile_time failed with this error:', str(err))
        return err_str

    race_stats = calc_time_per_mile(miles, minutes, seconds)

    mile_time = race_stats[0]
    sec_per_mile = race_stats[1]
    sec_per_race = race_stats[2]

    log_request(request, race_stats)

    db_race_log(first_name, last_name, grade, race, miles, sec_per_race, sec_per_mile)

    return render_template('results.html',
                            out_first_name = first_name,
                            out_last_name = last_name,
                            out_mile_time = mile_time,)


#TEST 6:  Load the app log file and print it to a results page
@app.route('/viewlog')
def view_log() -> str:
    contents = load_log(app_log)
    column_titles = ('Form Data', 'Remote Addr', 'User Agent', 'Results')
    # return str(contents)
    return render_template('viewlog.html',
                           out_title = 'View Log',
                           out_column_titles = column_titles,
                           out_data = contents
                           )

# DEBUG runs the webserver with auto-restart if code changes
# ALSO, for DEPLOYMENT:  check against main to see if app is run from THIS main entrypoint module,
# otherwise, will suppress app.run as this module is being imported and run to be invoked by deployment environment
if __name__ == '__main__':
    app.run(debug=True)
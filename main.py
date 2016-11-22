from bottle import static_file, route, error, run, template
import threading
import time

##Parameters
#Default times in seconds
default_pomodoro = 25 * 60
default_short_break = 5 * 60
default_long_break = 30 * 60

#Decrement value of the timer, default 1 second
decrement_val = 1

#Number of short breaks before long break
short_breaks_tresh = 3

##Pomodoro states
class States:
	pomodoro, short_break, long_break = range(3)

current_state = States.pomodoro
short_breaks = 0

@route('/')
def index():
    return template('webpage.html', timer=time_left, status=status, breaks=short_breaks)

@route('/bell/<name>')
def sound(name):
   return static_file(name , root="sounds")

@error(404)
def error404(error):
    return 'Stop breaking things >:('

##Timer stuff
#The used timer, in seconds
time_left = default_pomodoro
status = "pomodoro"

#Decrement it every second
def decrement():

	#The only way to modify the global variables
	global time_left
	global short_breaks
	global status
	global current_state

	time_left -= 1

	#The timer has run out
	if time_left <= 0:

		#For the pomodoro ending sound on the webpage
		time.sleep(5)

		#When finishing a pause, redo the pomodoro
		if current_state == States.short_break or current_state == States.long_break:

			time_left = default_pomodoro
			status = "pomodoro"
			current_state = States.pomodoro

			print "Break -> Pomodoro"

		elif current_state == States.pomodoro and short_breaks < short_breaks_tresh:

			short_breaks += 1
			time_left = default_short_break
			status = "short break"
			current_state = States.short_break

			print "Pomodoro -> Short Break"

		else: #Long break

			short_breaks = 0
			time_left = default_long_break
			status = "long break"
			current_state = States.long_break

			print "Pomodoro -> Long Break"

	#Restart the timer
	threading.Timer(decrement_val, decrement).start()

#Start the timer
threading.Timer(decrement_val, decrement).start()

run(host='0.0.0.0', port=8080, debug=False)
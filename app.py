"""
library(shiny)
library(countdown)

server <- function(input, output, session) {
  output$debug <- renderPrint({
    str(input$countdown)
  })

  timer_is_running <- reactiveVal(FALSE)

  observeEvent(input$countdown, {
    req(input$countdown)
    is_running <- input$countdown$timer$is_running
    if (is_running != timer_is_running()) {
      timer_is_running(is_running)
    }
  })

  output$buttons <- renderUI({
    is_running <- timer_is_running()

    div(
      class = "btn-group",
      actionButton("start", "Start", icon = icon("play")),
      actionButton("stop",  "Stop",  icon = icon("pause")),
      actionButton("reset", "Reset", icon = icon("sync")),
      if (is_running) {
        actionButton("bumpUp", "Bump Up", icon = icon("arrow-up"))
      },
      if (is_running) {
        actionButton("bumpDown", "Bump Down", icon = icon("arrow-down"))
      }
    )
  })

  observeEvent(input$start,    countdown_action("countdown", "start"))
  observeEvent(input$stop,     countdown_action("countdown", "stop"))
  observeEvent(input$reset,    countdown_action("countdown", "reset"))
  observeEvent(input$bumpUp,   countdown_action("countdown", "bumpUp"))
  observeEvent(input$bumpDown, countdown_action("countdown", "bumpDown"))
}
"""
# rewrite the above R code as Python code using shiny for python. this will go in the server function

"""
library(shiny)
library(countdown)

ui <- fluidPage(
  title = "{countdown} - Example Shiny App",
  div(
    class = "container",
    h2("Simple {countdown} Timer App"),
    p("Here's a simple timer, created with the {countdown} package."),
    HTML('<pre><code>countdown(id = "countdown")</code></pre>'),
    countdown(
      id = "countdown",
      style = "position:relative;width: 5em;max-width: 100%;"
    ),
    p(
      "The countdown timer reports the state of the timer whenever key actions",
      "are performed. On the Shiny side, the input ID is the same as the timer's",
      "ID - in this case", code("input$countdown"), "— and the data sent to",
      "Shiny reports both the action taken by the user and the current state",
      "of the timer."
    ),
    verbatimTextOutput("debug"),
    p(
      "You may also use the", code("countdown_action()"), "button to trigger",
      "actions with the timer from Shiny. Interact with the timer directly or",
      "use the buttons below to start, stop, reset, or bump the timer up or down."
    ),
    uiOutput("buttons", inline = TRUE),
    tags$style("body, pre, .btn { font-size: 16px }")
  )
)

"""
# use the folowing code to create the ui for the app

import os
import sys
import time
import traceback
import logging
import threading
import asyncio
import functools
import random
import json
import uuid
import datetime
import math

from shiny import App, reactive, render, ui

# app_ui = ui.page_fluid(
app_ui = ui.page_bootstrap(
    # add ui components here
	# ui.head_content('<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>'),
	# ui.include_css('styles.css'),
	# ui.page_bootstrap()(
		# {"style": "align-items: center"},
	# ),
	ui.h1("Workout Timer"),
	ui.p("This is a simple timer app for workouts."),
    
	# ui.output_text_verbatim(
	# 	id = "countdown",
	# ),
	ui.p(
		"The countdown timer reports the state of the timer whenever key actions",
		"are performed. On the Shiny side, the input ID is the same as the timer's",
		"ID - in this case", ui.code("input$countdown"), "— and the data sent to",
		"Shiny reports both the action taken by the user and the current state",
		"of the timer."
	),
	ui.output_text_verbatim("debug"),
	ui.p(
		"You may also use the", ui.code("countdown_action()"), "button to trigger",
		"actions with the timer from Shiny. Interact with the timer directly or",
		"use the buttons below to start, stop, reset, or bump the timer up or down."
	),
	ui.output_text_verbatim("time_remaining"),

	ui.output_ui("buttons", inline = True),
	# ui.tags({
	# 	"style": "body, pre, .btn { font-size: 16px }"
	# })
	

		ui.div(
			# class_ = "btn-group",
			ui.input_action_button(
				"start",
				"Start",
				icon =ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 512 192"><path fill="#00ACD7" d="m292.533 13.295l1.124.75c13.212 8.725 22.685 20.691 28.917 35.15c1.496 2.243.499 3.49-2.493 4.237l-5.063 1.296c-11.447 2.949-20.53 5.429-31.827 8.378l-6.443 1.678c-2.32.574-2.96.333-5.428-2.477l-.348-.399c-3.519-3.988-6.155-6.652-10.817-9.03l-.899-.443c-15.705-7.727-30.911-5.484-45.12 3.74c-16.952 10.968-25.677 27.172-25.428 47.364c.25 19.942 13.96 36.395 33.654 39.137c16.951 2.244 31.16-3.739 42.378-16.452c2.244-2.743 4.238-5.734 6.73-9.224h-48.11c-5.235 0-6.481-3.24-4.736-7.478l.864-2.035c3.204-7.454 8.173-18.168 11.4-24.294l.704-1.319c.862-1.494 2.612-3.513 5.977-3.513h80.224c3.603-11.415 9.449-22.201 17.246-32.407c18.198-23.931 40.135-36.396 69.8-41.63c25.427-4.488 49.359-1.995 71.046 12.713c19.694 13.461 31.909 31.66 35.15 55.59c4.237 33.654-5.485 61.075-28.668 84.508c-16.453 16.702-36.645 27.172-59.829 31.908c-6.73 1.247-13.461 1.496-19.942 2.244c-22.685-.499-43.376-6.98-60.826-21.937c-12.273-10.61-20.727-23.648-24.928-38.828a104.937 104.937 0 0 1-10.47 16.89c-17.949 23.683-41.381 38.39-71.046 42.38c-24.43 3.24-47.115-1.497-67.058-16.454c-18.447-13.96-28.917-32.407-31.66-55.34c-3.24-27.173 4.737-51.603 21.19-73.041c17.7-23.184 41.132-37.891 69.8-43.126c22.999-4.16 45.037-1.595 64.936 11.464ZM411.12 49.017l-.798.178c-23.183 5.235-38.14 19.942-43.624 43.375c-4.488 19.444 4.985 39.138 22.934 47.115c13.71 5.983 27.421 5.235 40.633-1.496c19.694-10.22 30.413-26.175 31.66-47.613c-.25-3.24-.25-5.734-.749-8.227c-4.436-24.401-26.664-38.324-50.056-33.332ZM116.416 94.564c.997 0 1.496.748 1.496 1.745l-.499 5.983c0 .997-.997 1.745-1.745 1.745l-54.344-.249c-.997 0-1.246-.748-.748-1.496l3.49-6.232c.499-.748 1.496-1.496 2.493-1.496h49.857ZM121.9 71.63c.997 0 1.496.748 1.247 1.496l-1.995 5.983c-.249.997-1.246 1.495-2.243 1.495l-117.912.25c-.997 0-1.246-.499-.748-1.247l5.235-6.73c.499-.748 1.745-1.247 2.742-1.247H121.9Zm12.963-22.934c.997 0 1.246.748.748 1.496l-4.238 6.481c-.499.748-1.745 1.496-2.493 1.496l-90.24-.25c-.998 0-1.247-.498-.749-1.246l5.235-6.73c.499-.748 1.745-1.247 2.742-1.247h88.995Z"/></svg>'),
				),
			ui.input_action_button(
				"stop",
				"Stop",
				 icon = ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 512 512"><path fill="red" d="M389.917 128.73v100.836h-22.802v-158.5a17.11 17.11 0 0 0-17.11-17.11h-11.863a17.11 17.11 0 0 0-17.11 17.11v158.5h-22.698V46.993a17.11 17.11 0 0 0-17.11-17.11h-11.863a17.11 17.11 0 0 0-17.11 17.11v182.573H229.5V77.33a17.11 17.11 0 0 0-17.108-17.11h-11.864a17.11 17.11 0 0 0-17.11 17.11v263.873l-63.858-51.14a23.385 23.385 0 0 0-30.743 1.32l-5.567 5.31a23.385 23.385 0 0 0-2.01 31.678l102.19 125.647a72.028 72.028 0 0 0 57.092 28.1h60.85A134.637 134.637 0 0 0 436 347.5V128.73a17.11 17.11 0 0 0-17.11-17.108h-11.864a17.11 17.11 0 0 0-17.11 17.11z"/></svg>')
				 ),
			ui.input_action_button(
				"reset",
				"Reset",
				icon = ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24"><path fill="yellow" d="M7.85 19.125q-2.6-1.2-4.237-3.625t-1.638-5.475q0-.65.075-1.275t.225-1.225l-1.15.675l-1-1.725L4.9 3.725l2.75 4.75l-1.75 1l-1.35-2.35q-.275.675-.412 1.4T4 10.025q0 2.425 1.325 4.413t3.525 2.937l-1 1.75ZM15.5 7V5h2.725q-1.15-1.425-2.775-2.212T12 2q-1.375 0-2.6.425t-2.25 1.2l-1-1.75Q7.4 1 8.863.5t3.112-.5q1.975 0 3.788.738T19 2.875V1.5h2V7h-5.5Zm-.65 15l-4.775-2.75l2.75-4.75l1.725 1l-1.425 2.45q2.95-.425 4.913-2.663T20 10.026q0-.275-.013-.525t-.062-.5h2.025q.025.25.038.488T22 10q0 3.375-2.013 6.038t-5.237 3.587l1.1.65l-1 1.725Z"/></svg>')
				),
			ui.input_action_button(
				"previous",
				"Previous",
				icon = ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 32 32"><path fill="orange" d="M16 2a14 14 0 1 0 14 14A14 14 0 0 0 16 2Zm8 15H11.85l5.58 5.573L16 24l-8-8l8-8l1.43 1.393L11.85 15H24Z"/><path fill="none" d="m16 8l1.43 1.393L11.85 15H24v2H11.85l5.58 5.573L16 24l-8-8l8-8z"/></svg>')
				),
			ui.input_action_button(
				"next",
				"Next",
				icon = ui.HTML('<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 32 32"><path fill="blue" d="M2 16A14 14 0 1 0 16 2A14 14 0 0 0 2 16Zm6-1h12.15l-5.58-5.607L16 8l8 8l-8 8l-1.43-1.427L20.15 17H8Z"/><path fill="none" d="m16 8l-1.43 1.393L20.15 15H8v2h12.15l-5.58 5.573L16 24l8-8l-8-8z"/></svg>')
				),
			ui.HTML('<div style="display: flex; flex-direction: row; justify-content: center; align-items: center; width: 100%; height: 100%;"><div style="font-size: 100px; font-weight: bold; color: white;">{countdown}</div></div>'),
		)
	
)
	

def server(input, output, session):

	# @reactive.value(input.countdown)
	# timer_is_running = False
	# time_remaining = 60

	@output
	@render.text
	def time_remaining():
		# return 60 - input.countdown.timer.time_remaining
		return arrow.now(). - datetime.timedelta(seconds = 10)
		# return input.countdown
	
	
	def tick():
		pass
	
	def current_exercise():
		exercise_names = ["Squats","Push ups","Pull ups","Leg raises"]
		total_sets = 3
	
		exercises = {x+1:y for x,y in zip(range(total_sets * len(exercise_names)), exercise_names * total_sets)}
	@reactive.event(input.countdown)
	def countdown_action():
		pass

	@reactive.event(input.countdown)
	def countdown_event():
		# nonlocal timer_is_running
		# if input.countdown:
		# 	is_running = input.countdown.timer.is_running
		# 	if is_running != timer_is_running():
		# 		timer_is_running(is_running)
		pass

	# output.buttons = render.ui({
	# 	is_running == timer_is_running()

	# })

	@reactive.event(input.start)
	def start():
		countdown_action("countdown", "start")
		

	@reactive.event(input.stop)
	def stop():
		countdown_action("countdown", "stop")

	@reactive.event(input.reset)
	def reset():
		countdown_action("countdown", "reset")

	@reactive.event(input.previous)
	def previous():
		countdown_action("countdown", "previous")

	@reactive.event(input.next)
	def next():
		countdown_action("countdown", "next")


app = App(app_ui, server)

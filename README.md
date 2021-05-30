[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


# Pynetstation-Plug-In

Plug-in for OpenSesame to use EGI's Netstation EEG software. This has been modified from [imnotamember](https://github.com/imnotamember)'s version to work with Python 3 (including pip files), and to just generally look a lot like the PyGaze plugin. 'Tested' (so to speak) with OpenSesame 3.3.9 with Python 3.9 on Windows 10, with Netstation 5.4. Timing has not been tested. 

Includes:
* ##### pynetstation
   
   Formerly egi, includes the guts of the egi package translated to Python 3. Mainly syntax translation, but also some stuff to do with how network traffic is packaged.

* ##### opensesame_plugins

   Plugins for OpenSesame, includes:
   * `pynetstation_init`
   
      This should be used once in any experiment (will throw an error if used more than that) if you want to create multiple Netstation recordings in a single experiment use the pynetstation reinit item after you end any sessions in your experiment. Set to Dummy and you can try out your experiment and get feedback without actually being connected to Netstation, really useful if you are like me and don’t have an EGI set up at home to work with and would rather not live in your lab space.
   * `pynetstation_start_recording`
   
      Pretty straight forward, presses record in Netstation
   * `pynetstation_pause_recording`
   
      Pretty straight forward, presses pause in Netstation
   * `pynetstation_begin_trial`
   
      This tells Netstation to synchronize its clock with Opensesame, which is crucial during experiments as the clock drifts over time. Make sure this is within the loop you want to record events from.
   * `pynetstation_send_tags`
   
      Sends Netstation events from OpenSesame, fill in the blanks with your information for your event. Disctionary events currently do not work.
    * `pynetstation_end`
   
      Pretty straight forward, saves and closes the Netstation session.
    * `pynetstation_reinit`
   
      Use this after you use `pynetstation_end` in your experiment to reconnect to Netstation. Just make sure you open a new recording session in Netstation before running this, or you’ll crash the experiment.
      
* ##### examples

   Not particularly well tested, just converted in syntax.
* ##### icons_svg

   Slightly jazzy icons for OpenSesame


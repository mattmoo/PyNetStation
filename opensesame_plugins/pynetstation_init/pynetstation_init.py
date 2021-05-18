#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas

class pynetstation_init(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = 'Initialize connection with Netstation'

	def reset(self):

		"""
		desc:
			Resets plug-in to initial values.
		"""

		# Here we provide default values for the variables that are specified
		# in info.json. If you do not provide default values, the plug-in will
		# work, but the variables will be undefined when they are not explicitly
		# set in the GUI.
		self.threadoption = 'Threaded'
		self.iptext = '11.0.0.42'
		self.porttext = '55513'
		self.nsOnOff = 'yes'

	def prepare(self):

		"""The preparation phase of the plug-in goes here."""

		# Call the parent constructor.
		item.prepare(self)
 	
	def run(self):

		"""The run phase of the plug-in goes here."""

		# self.set_item_onset() sets the time_[item name] variable. Optionally,
		# you can pass a timestamp, such as returned by canvas.show().
		self.set_item_onset(self.time())
		
		self.experiment.set('nsOnOff', self.get('nsOnOff'))
		self.experiment.set('threadoption', self.get('threadoption'))
		if(self.experiment.get('nsOnOff') == 'yes'):
			self.experiment.set('ip', self.get('iptext').encode('utf-8'))
			self.experiment.set('port', int(self.get('porttext')))
			print(self.experiment.get('ip'), type(self.experiment.get('ip')), self.experiment.get('port'), type(self.experiment.get('port')))
			if(self.experiment.get('threadoption')=='Simple'):
				import pynetstation.simple as pynetstation
				self.experiment.pynetstation = pynetstation
				ms_localtime = self.experiment.pynetstation.ms_localtime
				self.experiment.ns = self.experiment.pynetstation.Netstation()
				self.experiment.ns.connect(self.experiment.get('ip'), self.experiment.get('port'))
			else:
				if(self.experiment.get('threadoption')=='Threaded'):
					import pynetstation.threaded as pynetstation
				else:
					import pynetstation.fake as pynetstation
					print('Fake Session!!!!!!!!!!!!')
				self.experiment.pynetstation = pynetstation
				ms_localtime = self.experiment.pynetstation.ms_localtime
				self.experiment.ns = self.experiment.pynetstation.Netstation()
				self.experiment.ns.initialize(self.experiment.get('ip'), self.experiment.get('port'))
			self.experiment.ns.BeginSession()
			self.experiment.ns.sync()
		else:
			print("PyNetStation plug-in disabled!")
			
			
class qtpynetstation_init(pynetstation_init, qtautoplugin):
	
	"""
	This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
	usually need to do hardly anything, because the GUI is defined in info.json.
	"""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.
		
		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# We don't need to do anything here, except call the parent
		# constructors.
		pynetstation_init.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)
	
	def apply_edit_changes(self):

		"""
		desc:
			Applies the controls.
		"""

		if not qtautoplugin.apply_edit_changes(self) or self.lock:
			return False
		self.custom_interactions()
		return True

	def edit_widget(self):

		"""
		Refreshes the controls.

		Returns:
		The QWidget containing the controls
		"""

		if self.lock:
			return
		self.lock = True
		w = qtautoplugin.edit_widget(self)
		self.custom_interactions()
		self.lock = False
		return w

	def custom_interactions(self):

		"""
		desc:
			Activates the relevant controls for each tracker.
		"""

		onOrOffNS = self.get('nsOnOff')=='yes'
		self.threaded_combobox_widget.setEnabled(onOrOffNS)
		self.ip_line_edit_widget.setEnabled(onOrOffNS)
		self.port_line_edit_widget.setEnabled(onOrOffNS)

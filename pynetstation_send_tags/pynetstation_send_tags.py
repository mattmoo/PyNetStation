# -*- coding:utf-8 -*-

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

blankText = 'Enter Variable Name Here'
blankID = '****'


def make_fit(k):
    n = len(k)
    d = n - 4
    if d > 0:
        return k[0:4]
    else:
        return k + ' ' * abs(d)


class pynetstation_send_tags(item):
    """
    This class (the class with the same name as the module) handles the basic
    functionality of the item. It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = 'Send event tags to Netstation'

    def reset(self):

        """
        desc:
            Resets plug-in to initial values.
        """

        # Here we provide default values for the variables that are specified
        # in info.json. If you do not provide default values, the plug-in will
        # work, but the variables will be undefined when they are not explicitly
        # set in the GUI.

        self.eventTag = 'evt-'
        self.labelCheck = 'yes'
        self.labelText = 'Description of events or somesuch'
        self.descriptionCheck = 'yes'
        self.descriptionText = 'Description of events or somesuch'
        self.tag1check = 'yes'
        self.tagText1 = blankText
        self.tagID1 = blankID
        self.tag2check = 'no'
        self.tagText2 = blankText
        self.tagID2 = blankID
        self.tag3check = 'no'
        self.tagText3 = blankText
        self.tagID3 = blankID
        self.tag4check = 'no'
        self.tagText4 = blankText
        self.tagID4 = blankID
        self.tag5check = 'no'
        self.tagText5 = blankText
        self.tagID5 = blankID

    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        item.prepare(self)

    def run(self):

        """The run phase of the plug-in goes here."""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().
        self.set_item_onset(self.time())

        if self.get('nsOnOff') == 'yes':
            tagTable = {}
            if self.get('labelCheck') != 'yes':
                self.labelText = ''
            if self.get('descriptionCheck') != 'yes':
                self.descriptionText = ''
            for i in range(1, 6):
                if self.get('tag%dcheck' % i) == 'yes':
                    #
                    # Force all keys to become a utf-8 string, regardless of whether they're an int or string.
                    # keyI = ('%s' % self.get(u'tagID%d' % i)).encode('utf-8')
                    keyI = str(self.get('tagID%d' % i))
                    #
                    # check if variable exists. If not, use the literal.
                    try:
                        valueI = self.get(self.get('tagText%d' % i))
                    except:
                        valueI = self.get('tagText%d' % i)
                    #
                    # Differentiate between integers and strings while encoding strings in utf-8 for pynetstation.
                    if type(valueI) == int or type(valueI) == int or type(valueI) == float:
                        tagTable[keyI] = (valueI)
                    else:
                        tagTable[keyI] = str(valueI)
            '''
            for i in tagTable:
                print "\nKey %s is type: %s" % (i, type(i))
                print "\nValue %s is type: %s" % (tagTable[i], type(tagTable[i]))
            print tagTable
            '''
            #
            # Encode everything to 'utf-8' before sending the message to NetStation.
            # event = ('%s' % self.experiment.get(u'eventTag')).encode('utf-8')
            # event = ('%s' % self.get(u'eventTag')).encode('utf-8')
            # label = ('%s' % self.get(u'labelText')).encode('utf-8')
            # description = ('%s' % self.get(u'descriptionText')).encode('utf-8')
            event = str(self.get('eventTag'))
            label = str(self.get('labelText'))
            description = str(self.get('descriptionText'))
            timestamp = self.experiment.egi.ms_localtime()
            table = tagTable
            self.experiment.window.callOnFlip(self.experiment.ns.send_timestamped_event, event, label, description,
                                              table, pad=True)
            self.experiment.ns.send_event('evtT', timestamp, label, description, table, pad=True)


class qtpynetstation_send_tags(pynetstation_send_tags, qtautoplugin):
    """
    This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json.
    """

    def __init__(self, name, experiment, script=None):

        """
        Constructor.
        
        Arguments:
        name	    --	The name of the plug-in.
        experiment	--	The experiment object.
        
        Keyword arguments:
        script		--	A definition script. (default=None)
        """

        # We don't need to do anything here, except call the parent
        # constructors.
        pynetstation_send_tags.__init__(self, name, experiment, script)
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
        self.eventTag = make_fit(str(self.eventTag))
        self.event_line_edit_widget.setEnabled(True)

        for i in range(1, 6):
            self.set('tagID%d' % i, make_fit(str(self.get('tagID%d' % i))))

        onOffLabel = self.get('labelCheck') == 'yes'
        self.label_line_edit_widget.setEnabled(onOffLabel)

        onOffDesc = self.get('descriptionCheck') == 'yes'
        self.description_line_edit_widget.setEnabled(onOffDesc)

        onOffTag1 = self.get('tag1check') == 'yes'
        self.tag1_line_edit_widget.setEnabled(onOffTag1)
        self.tagid1_line_edit_widget.setEnabled(onOffTag1)
        onOffTag2 = self.get('tag2check') == 'yes'
        self.tag2_line_edit_widget.setEnabled(onOffTag2)
        self.tagid2_line_edit_widget.setEnabled(onOffTag2)
        onOffTag3 = self.get('tag3check') == 'yes'
        self.tag3_line_edit_widget.setEnabled(onOffTag3)
        self.tagid3_line_edit_widget.setEnabled(onOffTag3)
        onOffTag4 = self.get('tag4check') == 'yes'
        self.tag4_line_edit_widget.setEnabled(onOffTag4)
        self.tagid4_line_edit_widget.setEnabled(onOffTag4)
        onOffTag5 = self.get('tag5check') == 'yes'
        self.tag5_line_edit_widget.setEnabled(onOffTag5)
        self.tagid5_line_edit_widget.setEnabled(onOffTag5)

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
from gettext import gettext as _

from gi.repository import Gtk
from gi.repository import WebKit

from sugar3.activity import activity
from sugar3.activity.widgets import ActivityButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton

from viewtoolbar import ViewToolbar

HOME = "file://"+os.path.join(activity.get_bundle_path(), 'sugarizehelp/Introduction')
#HOME = "http://website.com/something.html"

class SugarizeHelp(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.props.max_participants = 1

        self._web_view = WebKit.WebView()

        toolbox = ToolbarBox()
        self.set_toolbar_box(toolbox)
        toolbox.show()

        toolbar = toolbox.toolbar
        toolbar.show()

        activity_button = ActivityButton(self)
        toolbar.insert(activity_button, -1)

        viewtoolbar = ViewToolbar(self)
        viewtoolbar_button = ToolbarButton(
            page=viewtoolbar, icon_name='toolbar-view')
        toolbar.insert(viewtoolbar_button, -1)
        toolbar.show_all()

        self._back = ToolButton('go-previous-paired')
        self._back.set_tooltip(_('Back'))
        self._back.props.sensitive = False
        self._back.connect('clicked', self._go_back_cb)
        toolbar.insert(self._back, -1)
        self._back.show()
        
        self._forward = ToolButton('go-next-paired')
        self._forward.set_tooltip(_('Forward'))
        self._forward.props.sensitive = False
        self._forward.connect('clicked', self._go_forward_cb)
        toolbar.insert(self._forward, -1)
        self._forward.show()
        
        home = ToolButton('go-home')
        home.set_tooltip(_('Home'))
        home.connect('clicked', self._go_home_cb)
        toolbar.insert(home, -1)
        home.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar.insert(separator, -1)

        stopbtn = StopButton(self)
        toolbar.insert(stopbtn, -1)
        toolbar.show_all()

        self._web_view.connect('load-finished', self.update_navigation_buttons)

        self.set_canvas(self._web_view)
        self._web_view.show()

        self._web_view.load_uri(HOME)

    def _go_back_cb(self, button):
        self._web_view.go_back()
        pass
    
    def _go_forward_cb(self, button):
        self._web_view.go_forward()
        pass
        
    def _go_home_cb(self, button):
        self._web_view.load_uri(HOME)
        pass

    def update_navigation_buttons(self, *args):
        can_go_back = self._web_view.can_go_back()
        self._back.props.sensitive = can_go_back

        can_go_forward = self._web_view.can_go_forward()
        self._forward.props.sensitive = can_go_forward


#!python

from kivymd.app import MDApp

from kivy.core.window import Window

from kivy.clock import Clock, mainthread

from kivy.logger import Logger

from kivy.base import platform
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from kivy.uix.label import Label
kv="""
<LoginScreen>:
	MDFloatLayout:
		md_bg_color:rgba('#000000')
		MDLabel:
			text:"Welcome To Minervas"
			pos_hint:{'x':.3,'top':1.45}
			text_size:cm(100),cm(100)
			#size_hint:1.5,1.5
			#halign:'center'
			color:rgba('#FF8C00')
		Image:
			source:'data/pic5.jpg'
			size_hint:.5,.5
			pos_hint:{'center_x':.5,'center_y':.2}
		MDRoundFlatIconButton:
			icon:'google'
			text:'LOGIN/SIGNUP'
			pos_hint:{'center_x':.5}
			on_release:root.signin()
<IndexScreen>:
	MDFloatLayout:
		md_bg_color:rgba('#ffffff')
		"""
class LoginScreen(MDScreen):
	pass
class IndexScreen(MDScreen):
	pass
class MinervasApp(MDApp):

    processing_uri = False

    def build(self):
    		Builder.load_string(kv)
    		sm = ScreenManager()
    		sm.add_widget(LoginScreen(name='login'))
    		sm.add_widget(IndexScreen(name='index'))
    		sm.current='login'
    		return sm

    def on_start(self):

        if platform == "android":

            self.verify_message_at_startup()

    def verify_message_at_startup(self):

        from jnius import autoclass

        PythonActivity = autoclass('org.kivy.android.PythonActivity')

        activity = PythonActivity.mActivity

        intent = activity.getIntent()

        self.android_message(intent)

    def on_pause(self):

        pass

        # Important! on_dropfile events are not received while the event loop is

        # paused! This ensures that the event loop will resume before any

        # on_dropfile event is fired. Many Bothans died to  bring us this information...

        if platform == 'ios':

            # Set this to True elsewhere in your code if you are pausing to wait for a

            # deeplink redirect back to your app (e.g. after FB OAUTH)

            if self.processing_uri:

                self.processing_uri = False

                Clock.schedule_once(self.resume_tasks, -1)

                Clock.schedule_once(self.on_resume, -1)

        return True

    def resume_tasks(self, *args):

        Window._pause_loop = False

    def on_resume(self):

        pass

    @mainthread

    def android_message(self, intent):

        intent_data = intent.getData()

        try:

            uri = intent_data.toString()

            # send full URI to a cross-platform function to process if there is one

            self.process_deep_link(uri)

        except AttributeError:

            self.process_deep_link('')

    def ios_message(self, window, uri):

        # send full URI to a cross-platform function to process

        self.process_deep_link(uri)

    def process_deep_link(self, uri):

        # Validate, parse, do things...

        Logger.info("URI INTENT FILTER: " + uri)

        if uri == '':

            self.root.text = 'No Intent Data ! (no uri)'

        else:

            self.root.text = uri

if __name__ == '__main__':

    app_instance = MinervasApp()

    if platform == 'android':

        import android.activity

        android.activity.bind(on_new_intent=app_instance.android_message)

    elif platform == 'ios':

        Window.bind(on_dropfile=app_instance.ios_message)

    app_instance.run()

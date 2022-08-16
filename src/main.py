#!python
from jnius import cast
from jnius import autoclass
from kivymd.app import MDApp

from kivy.core.window import Window

from kivy.clock import Clock, mainthread

from kivy.logger import Logger

from kivy.base import platform
from kivy.uix.screenmanager import ScreenManager,SwapTransition
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from kivy.uix.label import Label
class LoginScreen(MDScreen):
	def signin(self):
		PythonActivity = autoclass('org.kivy.android.PythonActivity')
		Intent = autoclass('android.content.Intent')
		Uri = autoclass('android.net.Uri')
		intent = Intent()
		intent.setAction(Intent.ACTION_VIEW)
		intent.setData(Uri.parse('https://minervasapi.herokuapp.com/mobilelogin'))
		currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
		currentActivity.startActivity(intent)
class IndexScreen(MDScreen):
	pass
sm = ScreenManager(transition=SwapTransition())
token=None
class MinervasApp(MDApp):

    processing_uri = False
    path=os.path.dirname(os.path.abspath(__file__))

    def build(self):
    		Builder.load_file(self.path+'/minervas.kv')
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
        #later on, id add a check to see if a token already exists.
        if uri == '' or token==None:
        	pass
        else:
        	from urllib import parse
        	parse.urlsplit(uri)
        	token=parse.parse_qs(parse.urlsplit(url).query).get('token',[''])[0]
        	sm.current='index'
        	
if __name__ == '__main__':

    app_instance = MinervasApp()

    if platform == 'android':

        import android.activity

        android.activity.bind(on_new_intent=app_instance.android_message)

    elif platform == 'ios':

        Window.bind(on_dropfile=app_instance.ios_message)

    app_instance.run()

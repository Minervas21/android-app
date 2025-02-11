#!python

from kivymd.app import MDApp

from kivy.core.window import Window

from kivy.clock import Clock, mainthread

from kivy.logger import Logger

from kivy.base import platform

from kivy.uix.label import Label

class MinervasApp(MDApp):

    processing_uri = False

    def build(self):

        return Label()

    def on_start(self):

        if platform == "android":

            self.verify_message_at_startup()

    def verify_message_at_startup(self):

        from jnius import autoclass

        PythonActivity = autoclass('org.renpy.android.PythonActivity')

        activity = PythonActivity.mActivity

        intent = activity.getIntent()

        self.android_message(intent)

    def on_pause(self):

        pass

        # Important! on_dropfile events are not received while the event loop is

        # paused! This ensures that the event loop will resume before any

        # on_dropfile event is fired. Many Bothans died to  bring us this information...

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
    app_instance.run()

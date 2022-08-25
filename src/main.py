#!python
from jnius import cast
from jnius import autoclass
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock, mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.base import platform
from kivy.uix.screenmanager import ScreenManager,SwapTransition
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from kivy.uix.label import Label
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
import certifi
sm = ScreenManager(transition=SwapTransition())
token=None
class IndexScreen(MDScreen):
	gender=None
	email=None
	full_name=None
	is_admin=None
	matric_no=None
	mode=None
	nickname=None
	personal_email=None
	phone_number=None
	profile_pic=None
	reg_no=None
	signature=None
	theme=None
	verified=None
	nav_drawer = ObjectProperty()
	screen_manager = ObjectProperty()
	def exit(self,*args):
		MinervasApp().stop()
	def relogin(self,*args):
		sm.current='login'
	def error1(self,req,result):
		self.ids.spinner.active=False
		return MDDialog(text="Check your internet connection and try again.",on_dismiss=self.exit,radius=[20,0,20,0],buttons=[MDFlatButton(text="Exit",on_release=self.exit)]).open()
	def faliure(self,req,result):
		status=req._resp_status
		if(status==401 or status==422):
			snackbar=Snackbar(text='Token expired or absent.')
			snackbar.buttons=[MDFlatButton(text='Exit',on_release=self.exit),MDFlatButton(text='Login Again',on_press=snackbar.dismiss and self.relogin)]
			snackbar.open()
			self.ids.spinner.active=False
		elif(status==500):
			snackbar=Snackbar(text='Internal server error. The error has been received and would be adressed shortly.')
			snackbar.open()
			self.ids.spinner.active=False
	def add_swiper(self,req,result):
		print(result)
		from kivymd.uix.swiper import MDSwiperItem
		from kivymd.uix.toolbar import MDToolbar
		from kivymd.uix.card import MDCard
		from kivy.utils import get_color_from_hex
		data=result.get('data')
		#later on, check scheduled date before adding.
		for key in data:
			print(key)
			print(data[key])
			value=data[key]
			si=MDSwiperItem()
			title=MDToolbar(title="Class Schedule Update",md_bg_color=get_color_from_hex('#FF8C00'))
			title.ids.label_title.font_size='15sp'
			course=MDLabel(text="Course: "+value['course'],font_style="H6",valign='top',pos_hint={'top':1.4},color=get_color_from_hex('#FF8C00'))
			time=MDLabel(text="Time: "+value['time'],font_style="H6",valign='top',pos_hint={'top':1.2},color=get_color_from_hex('#FF8C00'))
			additional_info=MDLabel(text=value['additional_info'],font_style="H6",valign='top',pos_hint={'top':1.0},color=get_color_from_hex('#FF8C00'))
			card=MDCard(orientation='vertical',elevation=0,padding='8dp',md_bg_color=get_color_from_hex('#1c6a7b'),radius=[20,20,20,20])
			card_=MDCard(orientation='vertical',elevation=0,md_bg_color=get_color_from_hex('#1c6a7b'), pos_hint={'top':2.5})
			card.add_widget(title)
			card_.add_widget(course)
			card_.add_widget(time)
			card_.add_widget(additional_info)
			card.add_widget(card_)
			si.add_widget(card)
			self.ids.zoom.add_widget(si)
	def gotten_info(self,req,result):
		print(result)
		#resp=json.loads(result.decode())
		resp=result
		self.gender=resp['Gender']
		self.email=resp['email']
		self.full_name=resp['full_name']
		self.is_admin=resp['is_admin']
		self.matric_no=resp['matric_no']
		self.mode=resp['mode']
		self.nickname=resp['nickname']
		self.personal_email=resp['personal_email']
		self.phone_number=resp['phone_number']
		self.profile_pic=resp['profile_pic']
		self.reg_no=resp['reg_no']
		self.signature=resp['signature']
		self.theme=resp['theme']
		self.verified=resp['verified']
		profile_pic=self.profile_pic
		self.ids.spinner.active=False
		self.ids.avatar.source=self.profile_pic
		self.ids.name.text=self.full_name
		self.ids.email.text=self.email
		#toast(resp['Gender'])
	def on_enter(self):
		url = "https://minervasapi.herokuapp.com/get_info"
		headers = {}
		headers["Accept"] = "application/json"
		headers["Authorization"] = f"Bearer {token}"
		#headers["Content-Type"] = "application/json"
		data="{}"
		#resp = requests.get(url, headers=headers)
		resp=UrlRequest(url,on_success=self.gotten_info,on_error=self.error1,on_failure=self.faliure,req_headers=headers,ca_file=certifi.where())
		resp2=UrlRequest('https://minervasapi.herokuapp.com/class_schedule/get',on_success=self.add_swiper,on_failure=self.faliure,on_error=self.error1,req_headers=headers,ca_file=certifi.where())
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
class MinervasApp(MDApp):

    processing_uri = False
    path=os.path.dirname(os.path.abspath(__file__))

    def build(self):
    		Builder.load_file(self.path+'/main.kv')
    		sm.add_widget(LoginScreen(name='login'))
    		sm.add_widget(IndexScreen(name='index'))
    		sm.current='login'
    		return sm

    def on_start(self):

        if platform == "android":

            self.verify_message_at_startup()

    def verify_message_at_startup(self):

        from jnius import autoclass

        """PythonActivity = autoclass('org.kivy.android.PythonActivity')

        activity = PythonActivity.mActivity

        intent = activity.getIntent()

        self.android_message(intent)"""

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
        if uri == '':
        	pass
        else:
        	global token
        	token=uri.split('=')[1]
        	#toast(token)
        	sm.current='index'
        	
if __name__ == '__main__':

    app_instance = MinervasApp()

    if platform == 'android':

        import android.activity

        android.activity.bind(on_new_intent=app_instance.android_message)

    elif platform == 'ios':

        Window.bind(on_dropfile=app_instance.ios_message)

    app_instance.run()

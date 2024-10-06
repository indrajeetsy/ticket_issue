# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, ValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import requests
from rasa_sdk.events import SlotSet

from datetime import datetime as dt
import itertools

base_domain = 'http://127.0.0.1:8000/'

class ValidatePredefinedSlots(ValidationAction):
    def validate_name(
        self,
        slot_value: any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print(slot_value)
        if isinstance(slot_value, str):
            return {"name": slot_value.capitalize()}
        else:
            return {"name": None}


def update_tracker(tracker):    
    return tracker

class ActionFetchUsername(Action):
    def name(self) -> Text:
        return 'action_fetch_username'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(self.name())
        api_url = base_domain+'api/get_username/'
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            user_data = response.json()
            print(user_data)
            username = user_data.get('logged_in', None)
            print('slots',tracker.slots)
            print('logged_in',username)
            if username:
                return [SlotSet('username', username)]
            else:
                dispatcher.utter_message(text='could not fetch the username.')
                return [SlotSet("username", None)]
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f'failed to connect to the server. Error: {str(e)}')
            return [SlotSet("username", None)]

class ActionRaiseTicket(Action):

    def name(self) -> Text:
        return 'action_raise_ticket'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(self.name())
        print('slots',tracker.slots)
        issue = tracker.latest_message['text']
        dispatcher.utter_message(text=f"issue - {tracker.slots['issue']}")
        # return [SlotSet("issue", issue)]
        return []

class ActionNewTicket(Action):

    def name(self) -> Text:
        return 'action_new_ticket'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(self.name())
        print('slots',tracker.slots)
        if tracker.slots['issue']:
            issue = tracker.slots['issue']
        print('issue',issue)
        for i in tracker.latest_message['entities']:
            tracker.slots[i['entity']]=i['value']
        print('slots',tracker.slots)
        user_data = {
            'issue': issue,
        }
        try:
            response = requests.post(base_domain+'api/raise_ticket/', json=user_data)
            response.raise_for_status()
            data = response.json()
            print('data',data)
            if data:
                dispatcher.utter_message(text=f'{data["ticket"]}.')
                dispatcher.utter_message(text=f'Please save the ticket ID for further tracking.')
            else:
                dispatcher.utter_message(text=f'Please login or relogin to continue.')
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f'Failed to save details. Error: {str(e)}')
        tracker=update_tracker(tracker)
        return []
    
class ActionTicketStatus(Action):

    def name(self) -> Text:
        return 'action_ticket_status'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(self.name())
        print('slots',tracker.slots)
        try:
            response = requests.get(base_domain+'api/ticket_status/')
            response.raise_for_status()
            data = response.json()
            print('data',data)
            if data['tickets']=='No active tickets.':
                dispatcher.utter_message(text=data['tickets'])
            else:
                for i in data['tickets']:
                    dispatcher.utter_message(text=i)
        #     else:
        #         dispatcher.utter_message(text=f'Please login or relogin to continue.')
        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f'Failed to save details. Error: {str(e)}')
        tracker=update_tracker(tracker)
        return []

#################################################################################################################################
#################################################################################################################################
# rasa nlp natural language processing deep learning machine learning data science c++
interview_links = {
    'python' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiapJPYkZX3AhV_8HMBHVOkDdsQFnoECAMQAQ&url=https%3A%2F%2Fwww.interviewbit.com%2Fpython-interview-questions%2F&usg=AOvVaw3j4_VZ2URpp5DKPLuUtBEb",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiSi-jk9pf3AhWnyzgGHbx9BykQFnoECAcQAQ&url=https%3A%2F%2Fwww.edureka.co%2Fblog%2Finterview-questions%2Fpython-interview-questions%2F&usg=AOvVaw1aPl7TD6kUgsO9blAoXy7Y"
        ],
    'java' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiN7b3whpj3AhX_l1YBHeENCLMQFnoECAsQAw&url=https%3A%2F%2Fwww.simplilearn.com%2Ftutorials%2Fjava-tutorial%2Fjava-interview-questions&usg=AOvVaw31ik4l80RaRAMhxnidiDpz",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiN7b3whpj3AhX_l1YBHeENCLMQFnoECAUQAQ&url=https%3A%2F%2Fwww.javatpoint.com%2Fcorejava-interview-questions&usg=AOvVaw3mSiJ-Vfgl-HcPR6gA4ZWt"
    ],
    'rasa' :[
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjkh7HohZj3AhVXmFYBHVcVC7UQFnoECA0QAQ&url=https%3A%2F%2Fwww.glassdoor.co.in%2FInterview%2FRasa-Technologies-Interview-Questions-E1888472.htm&usg=AOvVaw1OuUPlDZcvH-mWw4dDa90J",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjkh7HohZj3AhVXmFYBHVcVC7UQFnoECAoQAQ&url=https%3A%2F%2Fwww.justcrackinterview.com%2Finterviews%2Frasa%2F&usg=AOvVaw2a4Ell9BDUn6FsUahsL1i9",
    ],
    'natural language processing' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiynIr6hZj3AhX9tVYBHbrnALUQFnoECAUQAQ&url=https%3A%2F%2Fwww.interviewbit.com%2Fnlp-interview-questions%2F&usg=AOvVaw2pzvEbI0eoW9xtfAnQ5LKG",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiynIr6hZj3AhX9tVYBHbrnALUQFnoECBwQAQ&url=https%3A%2F%2Fwww.analytixlabs.co.in%2Fblog%2Fnlp-interview-questions%2F&usg=AOvVaw3hyYiCv8DqLlYnoVwq9Uyl"
    ],
    'deep learning' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiOx7-phpj3AhUwpVYBHcFJBbUQtwJ6BAgFEAE&url=https%3A%2F%2Fwww.simplilearn.com%2Ftutorials%2Fdeep-learning-tutorial%2Fdeep-learning-interview-questions&usg=AOvVaw2zwcgh1UPemBrbaH5nqjTv",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiOx7-phpj3AhUwpVYBHcFJBbUQFnoECAIQAQ&url=https%3A%2F%2Fwww.interviewbit.com%2Fdeep-learning-interview-questions%2F&usg=AOvVaw13II0mVJ8m8YT2uRCwE0gw"
    ],
    'machine learning' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi0zPaph5j3AhXhmVYBHdoKDrUQFnoECAYQAQ&url=https%3A%2F%2Fwww.interviewbit.com%2Fmachine-learning-interview-questions%2F&usg=AOvVaw2HwT_r9c_7QXrcNQtJ-6Pm",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi0zPaph5j3AhXhmVYBHdoKDrUQFnoECDwQAQ&url=https%3A%2F%2Fwww.edureka.co%2Fblog%2Finterview-questions%2Fmachine-learning-interview-questions%2F&usg=AOvVaw356NyC7cqEOcod5FtMgEr0",
    ],
    'data science' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiZ9M3Ch5j3AhU2mFYBHQn5D7UQtwJ6BAgDEAE&url=https%3A%2F%2Fwww.interviewbit.com%2Fdata-science-interview-questions%2F&usg=AOvVaw3wnZ3XEvUvfuvoH2twZknU",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiZ9M3Ch5j3AhU2mFYBHQn5D7UQFnoECEMQAQ&url=https%3A%2F%2Ftowardsdatascience.com%2Fover-100-data-scientist-interview-questions-and-answers-c5a66186769a&usg=AOvVaw3P13mYmhCElQKFoTZ2dp1Z"
    ],
    'c++' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjmmLnWh5j3AhVislYBHerND7UQFnoECAMQAQ&url=https%3A%2F%2Fwww.interviewbit.com%2Fcpp-interview-questions%2F&usg=AOvVaw3tHV1nMKIO8yTIRItxcqMK",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjmmLnWh5j3AhVislYBHerND7UQFnoECAoQAQ&url=https%3A%2F%2Fwww.tutorialspoint.com%2Fcplusplus%2Fcpp_interview_questions.htm&usg=AOvVaw1Z3_1KVTGNIal5Jf6vrieS"
    ],
    'sql' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjH_sjjh5j3AhWsgFYBHdDHCz0QFnoECAYQAQ&url=https%3A%2F%2Fwww.interviewbit.com%2Fsql-interview-questions%2F&usg=AOvVaw2Dv716lP0A0tpPCYRFAzJU",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjH_sjjh5j3AhWsgFYBHdDHCz0QFnoECA0QAQ&url=https%3A%2F%2Fwww.javatpoint.com%2Fsql-interview-questions&usg=AOvVaw0LUa4gDDRpCXWZks0QjuS0"
    ],
    'power bi' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjw_qH2h5j3AhX_p1YBHWu5BbQQFnoECAIQAQ&url=https%3A%2F%2Fwww.interviewbit.com%2Fpower-bi-interview-questions%2F&usg=AOvVaw1oZFSz5jsFsmGu5FkPAbMv",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjw_qH2h5j3AhX_p1YBHWu5BbQQFnoECAoQAQ&url=https%3A%2F%2Fwww.simplilearn.com%2Fpower-bi-interview-questions-and-answers-article&usg=AOvVaw2vQMllqVxvM9kfOP7BmjnN",
    ],
    'artificial intelligence' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjC5J2HiJj3AhX8tlYBHbuyC7MQFnoECAkQAQ&url=https%3A%2F%2Fwww.interviewbit.com%2Fartificial-intelligence-interview-questions%2F&usg=AOvVaw3VxWd10Y7Az7tpTZL0ye_B",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjC5J2HiJj3AhX8tlYBHbuyC7MQFnoECAIQAw&url=https%3A%2F%2Fwww.simplilearn.com%2Fartificial-intelligence-ai-interview-questions-and-answers-article&usg=AOvVaw2aIL5EWTRMQzbjOPS9ouUg"
    ]
    }

tutorial_links = {
    'python' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiC_f6iiJj3AhVLqlYBHbyyBLUQyCl6BAgDEAM&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D_uQrJ0TkZlc%26vl%3Den&usg=AOvVaw0pRn_FOUgjCc59k7uEsc5l",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiC_f6iiJj3AhVLqlYBHbyyBLUQtwJ6BAghEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dt8pPdKYpowI&usg=AOvVaw04l4t4uhfhUYsOhhzGafhp"
    ],
    'java' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi2utW6iJj3AhVislYBHerND7UQtwJ6BAgKEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DCFD9EFcNZTQ&usg=AOvVaw10QhZIELkjpiscDCjg-0cg",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi2utW6iJj3AhVislYBHerND7UQtwJ6BAgGEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DeIrMbAQSU34&usg=AOvVaw0YCsoDtTnlA5yAHU8fmUPI"
    ],
    'rasa' :[
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiGhLHIiJj3AhXnplYBHdFqBs0QtwJ6BAgJEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D-F6h43DRpcU&usg=AOvVaw0gqFd7SFwDjHYpoUkzxAAu",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiGhLHIiJj3AhXnplYBHdFqBs0QtwJ6BAgFEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dxu6D_vLP5vY&usg=AOvVaw3F8dZhLIucjhAjYYi19Q6y"
    ],
    'natural language processing' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiig4vjiJj3AhWkqFYBHS9rBbUQtwJ6BAgEEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D68lIfswwG2A&usg=AOvVaw2hVQlUPAvZ1B2acwzTAS0Q",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiig4vjiJj3AhWkqFYBHS9rBbUQtwJ6BAgDEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DwCXOi_k3kyY&usg=AOvVaw0LW_9gyumMuuPD-4QwVKaX"
    ],
    'deep learning' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjwiNPxiJj3AhX6plYBHU66ALIQtwJ6BAgFEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DVyWAvY2CF9c&usg=AOvVaw2lwZ_-Gomg7w5Gk_aJk2SY",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjwiNPxiJj3AhX6plYBHU66ALIQtwJ6BAgEEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DDooxDIRAkPA&usg=AOvVaw2d5ALQtdDwYJZKRHGFsbr2",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjwiNPxiJj3AhX6plYBHU66ALIQtwJ6BAgGEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DJMxbypF825w&usg=AOvVaw2DsDttDkzZVIEEKvW1cM8G"
    ],
    'machine learning' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwj8ibCQiZj3AhXbqFYBHReRBbUQtwJ6BAgJEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DGwIo3gDZCVQ&usg=AOvVaw1alFC7Th6w4DLpFqU4ejHR",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwj8ibCQiZj3AhXbqFYBHReRBbUQtwJ6BAgEEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D9f-GarcDY58&usg=AOvVaw2gV8Jn6UPq2rT580AgEela",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwj8ibCQiZj3AhXbqFYBHReRBbUQtwJ6BAgWEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Deq7KF7JTinU&usg=AOvVaw0qPqcSpg_Mco3wp8Mpyhu-"
    ],
    'data science' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwislOCoiZj3AhWDtlYBHf_wCLUQwqsBegQIAhAB&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D-ETQ97mXXF0&usg=AOvVaw0D1gOVSKu0Q_9XNBPMMceE",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwislOCoiZj3AhWDtlYBHf_wCLUQwqsBegQIBRAB&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dua-CiDNNj30&usg=AOvVaw3OR8ERoiWyALr8TaBaQeVc",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwislOCoiZj3AhWDtlYBHf_wCLUQwqsBegQIBBAB&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Du2zsY-2uZiE&usg=AOvVaw0OLoNY6r5BiyIZ78JpZqIy",
    ],
    'c++' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjwhby-iZj3AhU3p1YBHUXGD7QQyCl6BAgDEAM&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DvLnPwxZdW4Y%26vl%3Den&usg=AOvVaw154xmQUateNl6Sq0H-FWI1",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjwhby-iZj3AhU3p1YBHUXGD7QQtwJ6BAgWEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D_bYFu9mBnr4&usg=AOvVaw2oqMDhoIpPkp-wJTVIMVrq",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjwhby-iZj3AhU3p1YBHUXGD7QQtwJ6BAgTEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DGQp1zzTwrIg&usg=AOvVaw33OjYYMec3seFu4xk7Ylsd"
    ],
    'sql' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi8v9XYiZj3AhVMglYBHQmGDrQQyCl6BAgDEAM&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DHXV3zeQKqGY&usg=AOvVaw28qyHvdQya8x1gV53cnV7s",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi8v9XYiZj3AhVMglYBHQmGDrQQtwJ6BAgEEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DAA7i2GcTGwU&usg=AOvVaw3ngDlSk3xijkH3E1BhjE8O",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi8v9XYiZj3AhVMglYBHQmGDrQQtwJ6BAgOEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DLGTbdjoEBVM&usg=AOvVaw1kNgPAEs0gXwWIKUKp2nFb"
    ],
    'power bi' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwizrJTuiZj3AhWJm1YBHWF7A7UQwqsBegQIBRAB&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Di3CSD7bMMbg&usg=AOvVaw15GptDQ6B7dzdGAx6RvF0X",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwizrJTuiZj3AhWJm1YBHWF7A7UQwqsBegQIBBAB&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D3u7MQz1EyPY&usg=AOvVaw0N-UVjwWMq7kbybJSP_621",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwizrJTuiZj3AhWJm1YBHWF7A7UQwqsBegQIBBAB&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D3u7MQz1EyPY&usg=AOvVaw0N-UVjwWMq7kbybJSP_621"
    ],
    'artificial intelligence' : [
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjpi4eBipj3AhWPgFYBHaBKDrUQtwJ6BAgIEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DJMUxmLyrhSk&usg=AOvVaw1OnjT6N_LcNvaacHgTSeUz",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjpi4eBipj3AhWPgFYBHaBKDrUQtwJ6BAgCEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dsp_OMFCfGMw&usg=AOvVaw1tBTb6UZXRo5VhYsOlwgbv",
        "https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjpi4eBipj3AhWPgFYBHaBKDrUQtwJ6BAgDEAI&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D0lmQEo3NIJ4&usg=AOvVaw0kevFyzjIJKBjK8IKaovnr"
    ],
    }

links = {'interview':interview_links,'tutorial':tutorial_links}
#################################################################################################################################
#################################################################################################################################

def answer(subject,material_type):
    counter = itertools.count(1)
    text = "".join([f"\n{next(counter)}.\t{i}\n" for i in links[material_type][subject]])
    return f'Here are some links to {subject.capitalize()} {material_type} material to get started \n{text}'

class ActionStudyMaterial(Action):

    def name(self) -> Text:
        return "action_study_material"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            print(f'Tracked : \n\n{tracker.latest_message}\n\n')
            entities = tracker.latest_message['entities']
            for entity in entities:
                if entity['entity']=='subject':
                    subject = entity['value']
                if entity['entity']=='material_type':
                    material_type = entity['value']
            if subject=='python':
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='java':
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='rasa':
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='natural language processing' or subject=='nlp':
                subject = 'natural language processing'
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='deep learning':
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='machine learning':
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='data science':
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='c++' or subject=='c':
                subject='c++'
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='sql':
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='power bi':
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
            if subject=='artificial intelligence' or subject=='ai':
                subject = "artificial intelligence"
                if material_type=='interview':
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
                if material_type=='tutorial' or material_type=='tutorials':
                    material_type='tutorial'
                    dispatcher.utter_message(
                        text=answer(subject,material_type)
                        )
        except UnboundLocalError:
            dispatcher.utter_message(text=f"I didn't understand you.\nTry again.\nMay be you meant ex. - python tuorial videos or python interview questions")
        return []

class ActionSubjectsAvailable(Action):

    def name(self) -> Text:
        return "action_subjects_available"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        counter = itertools.count(1)
        text = "".join([f"{next(counter)}\t{i.capitalize()}\n" for i in interview_links.keys()])
        dispatcher.utter_message(text=f"Availabe Topics:- \n{text}")
        return []

class ActionTrackConversation(Action):

    def name(self) -> Text:
        return "action_track_conversations"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        counter = itertools.count(1)
        for i in tracker.events_after_latest_restart():
            print(next(counter),i,end='\n\n\n',sep='\t')
        dispatcher.utter_message(text=f"Check the action server")
        return []
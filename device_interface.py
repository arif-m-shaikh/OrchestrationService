from datetime import datetime
from tb_rest_client.rest_client_ce import *
from tb_rest_client.models.models_ce import *
from tb_rest_client.rest import ApiException

temp_device_id="d53a8e90-7d59-11ee-931c-7b5876965e1c"

# ThingsBoard REST API URL
class DeviceInterface():
    '''Device Interface Class'''
    
    def __init__(self):
        '''Constructor'''
        self.url = "http://localhost:8080"
        self.username = "tenant@thingsboard.org"
        self.password = "tenant"
        self.client = None

        try:
            if self.client is None:
                self.client = RestClientCE(self.url)
                self.client.login(username=self.username, password=self.password)

        except ApiException as e:
                print(e)

    def update_value(self, device_id: str, data_value: int):
        '''Update value on the dashboard'''

        if self.client is None:
            print("Client is empty. Hence skipping")
            return
            
        try:
            device = self.client.get_device_by_id(device_id)
            date= datetime.utcnow() - datetime(1970, 1, 1)
            seconds = date.total_seconds()
            curr_time_ms = round(seconds*1000)

            self.client.save_entity_telemetry(
                device.id, 'ANY',
                body={"ts": curr_time_ms,
                "values": {"temperature": data_value}})
            
        except ApiException as e:
            print(e)
            
    def enter_alarm(self, device_id: str, alarm_severity: str):
        '''Enter alarm on the dashboard'''

        if self.client is None:
            print("Client is empty. Hence skipping")
            return

        try:
            device = self.client.get_device_by_id(device_id)
            
            test_alarm = Alarm(name='Test', 
                            type='default',
                            originator=device.id,
                            severity = alarm_severity, 
                            status='CLEARED_UNACK', 
                            acknowledged=False, 
                            cleared=False)

            test_alarm = self.client.save_alarm(test_alarm)

        except ApiException as e:
            print(e)
            

    def clear_alarm(self, device_id: str):
        '''Clear alarm on the dashboard'''

        if self.client is None:
            print("Client is empty. Hence skipping")
            return
            
        try:
            device = self.client.get_device_by_id(device_id)
            alarms = self.client.get_alarms(device.id, 10, 0)
            if alarms: 
                for each_alarm in alarms.data: 
                    self.client.clear_alarm(each_alarm.id.id)

        except ApiException as e:
            print(e)


def update_device (temp_value: int, temp_alarm: str = ""):
    '''Function - Update Dashboard'''

    #temp_value = 24
    #temp_severity='CRITICAL'
    
    device_interface = DeviceInterface()
    device_interface.update_value(temp_device_id, temp_value)
    if temp_alarm:
        device_interface.enter_alarm(temp_device_id, temp_alarm)
    
    #deviceInterface.clear_alarm(temp_device_id)
   
            
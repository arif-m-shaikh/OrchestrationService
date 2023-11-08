 
from prefect import task, flow
from modbus_interface import read_data
from device_interface import update_device

@task(name="ReadTemparatureSensorData", log_prints=True)
def read_temparature_sensor_data (modbus_port, register_address = 0):
    '''Extract Task - Extract data from modbus'''
    return read_data(modbus_port, register_address)

@task(name="ProcessTemparatureSensorData", log_prints=True)
def process_temperature_sensor_data (sensor_data_value: int):
    '''Process Task - Generate alarm'''
    alarm = ""
    print("Temperature value ==============> " + str(sensor_data_value))
    if 45 < sensor_data_value: 
        alarm = "CRITICAL"
    return alarm

@task(name="LoadTemparatureSensorData", log_prints=True)
def load_temperature_sensor_data(sensor_data_value:int, sensor_alarm: str):
    '''Load Task - Update the dashboard'''
    print("Temperature value ==============> " + str(sensor_data_value))
    print("Temperature alarm, ==============> " + sensor_alarm)
    update_device(sensor_data_value, sensor_alarm)

@flow(name="ETLTempSensor", log_prints=True)
def temperature_sensor_data_flow():
    '''Flow Function '''
    modbus_data = read_temparature_sensor_data("COM2", register_address = 0)
    if modbus_data:
        temp_value = modbus_data[0]
        temp_alarm = process_temperature_sensor_data(temp_value)
        load_temperature_sensor_data(temp_value, temp_alarm)

if __name__ == "__main__":
    temperature_sensor_data_flow()
    #temperature_sensor_data_flow.serve(name="tempdevice", schedule=IntervalSchedule(interval=timedelta(minutes=1), anchor_date=datetime(2023, 11, 7, 0, 0)))
    

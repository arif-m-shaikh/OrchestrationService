# OrchestrationService

## WORKSPACE CREATION
1. Create a folder and then change to that folder.
2. Create the virtual environment
python -m venv prefect-env
3. Activate the environment
source prefect-env/Scripts/activate
4. Install prefect
pip install -U prefect
6. Check the installation
prefect version
7. Copy the files app.py, device_interface.py and modbus_interface.py to the folder

## SETUP

## DEVICE SIMULATION:
1. Install Virtual Serial Port Emulator (VSPE) on the machine.
Map COM1 to COM2.
2. Install Modbus Slave on the machine
Use Address 0 for generating Sensor data

## DEVICE DASHBOARD on THINGSBOARD.IO:
3. Create an Ubuntu VM on virtual box.
4. Map the following HOST => VM ports
22560 => 22
8080 => 8080
5. Run the Thingsboard docker to create the dashboard.
6. Configure the following.
- Create a temperature device => Get the id of the device and paste it in device_interface.py
- Create an asset called building, create a relation building contain device.
- Create a dashboard, add a Chart -> TimeSeries line chart , Digital Gauge -> Digital Thermometer, Table -> Alarm table widgets on the dashboard. Configure these widgets

## TESTING
- Set the value 25 in cell 0 of Modbus Slave
- Test by running py app.py. The value should be displayed in the console.
- Test by checking the value 25 on the dashboard 
- Now change the value to 50.
- Test by running py app.py. The value should be displayed in the console.
- Test by checking the value 50 on the dashboard
- Also Test alarm will be generated. Acknowledge and clear that alarm

## DEPLOYMENT
1. We can create the deployment using the following command
prefect deployment build app:temperature_sensor_data_flow -n temperature_sensor_data_flow
- Where app => filename, temperature_sensor_data_flow => flow name in file app.py
- Together they form the entry point
- n represents the anem of the deployment file.
2. We can add the schedule in the deployment
    name: temperature_sensor_flow
    . . .
    schedule: 
        interval: 60
- Interval specify the number of seconds
3. We can apply the deployment using the follwing command
prefect deployment apply temperature_sensor_data_flow-deployment.yaml
- It automaticallys add -deployment.yaml to the name.
4. These deployment will not execute unless we run the agent
prefect agent start -q default
- We specify the default queue

## PREFECT DASHBOARD
1. Prefect provide a web server that is optional and can be used for checking the flow. We can run the server using the command
prefect server start
2. After applying the deployment we can get it in deployment tab
- We can check the flow runs scheduled also.
- We can even check the dashboard to understand the flow of tasks.
- We can even check the log containing the details.
NOTE: We have added an attribute to display the detail logs.
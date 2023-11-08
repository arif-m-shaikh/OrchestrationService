import pymodbus.client as ModbusClient
from pymodbus import pymodbus_apply_logging_config

def read_data(port_address, register_address = 0, register_count = 1):
    """Run sync client."""
    # activate debugging
    pymodbus_apply_logging_config("DEBUG")

    #comm == "serial":
    client = ModbusClient.ModbusSerialClient(
        port_address,
        #framer=ModbusRtuFramer,
        # timeout=10,
        # retries=3,
        # retry_on_empty=False,
        # close_comm_on_error=False,.
        # strict=True,
        baudrate=9600,
        bytesize=8,
        parity="N",
        stopbits=1,
        # handle_local_echo=False,
    )
    print("connect to server")
    client.connect()

    print("get and verify data")
    try:
        modbusResponse = client.read_holding_registers(register_address, register_count, slave=1)
        if modbusResponse.isError():  # pragma no cover
            print(f"Received Modbus library error({modbusResponse})")
            client.close()
            return ""
        
        return modbusResponse.registers
    
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return

    # if isinstance(rr, ExceptionResponse):  # pragma no cover
    #     print(f"Received Modbus library exception ({rr})")
    #     # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
    #     client.close()

    print("close connection")  # pragma no cover
    client.close()  # pragma no cover


# if __name__ == "__main__":
#     port_address = "COM2"
#     register_address = 2
#     device_response = read_data(port_address, register_address)  # pragma: no cover
#     if device_response:
#         print (device_response)
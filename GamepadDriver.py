import serial
import os

if os.name == 'posix':
	from evdev import UInput, UInputError, AbsInfo, ecodes

	global device
	device = UInput()

	global syskeymap
	syskeymap = {
				'up':			ecodes.KEY_UP,
				'left':			ecodes.KEY_LEFT,
				'down':			ecodes.KEY_DOWN,
				'right':		ecodes.KEY_RIGHT,
				'lshift':		ecodes.KEY_LEFTSHIFT,
				'rshift':		ecodes.KEY_RIGHTSHIFT,
				'esc':			ecodes.KEY_ESC,
				'space':		ecodes.KEY_SPACE,
				'enter':		ecodes.KEY_ENTER,
				'lalt':			ecodes.KEY_LEFTALT,
				'ralt':			ecodes.KEY_RIGHTALT,
				'lctrl':		ecodes.KEY_LEFTCTRL,
				'rctrl':		ecodes.KEY_RIGHTCTRL,
				'backspace':	ecodes.KEY_BACKSPACE,
				'tab':			ecodes.KEY_TAB,
				'a':ecodes.KEY_A,
				'b':ecodes.KEY_B,
				'c':ecodes.KEY_C,
				'd':ecodes.KEY_D,
				'e':ecodes.KEY_E,
				'f':ecodes.KEY_F,
				'g':ecodes.KEY_G,
				'h':ecodes.KEY_H,
				'i':ecodes.KEY_I,
				'j':ecodes.KEY_J,
				'k':ecodes.KEY_K,
				'l':ecodes.KEY_L,
				'm':ecodes.KEY_M,
				'n':ecodes.KEY_N,
				'o':ecodes.KEY_O,
				'p':ecodes.KEY_P,
				'q':ecodes.KEY_Q,
				'r':ecodes.KEY_R,
				's':ecodes.KEY_S,
				't':ecodes.KEY_T,
				'u':ecodes.KEY_U,
				'v':ecodes.KEY_V,
				'w':ecodes.KEY_W,
				'x':ecodes.KEY_X,
				'y':ecodes.KEY_Y,
				'z':ecodes.KEY_Z}
else:
	import win32com.client

	global shell
	shell = win32com.client.Dispatch("WScript.Shell")


def evdevKey(key,state):
	device.write(ecodes.EV_KEY, syskeymap[key], state)
	device.syn()

def winKey(key,state):
	shell.SendKeys(key)

def setKeyState(key,state):
	if os.name == 'posix':
		evdevKey(key,state)
	else:
		winKey(key,state)

def getSerialConnection():
	if os.name == 'posix':
		nonlocal device_list
		possible_device_list = ["/dev/ttyUSB{0}".format(i) for i in range(0,4)]
		device_list = list(filter(os.path.exists,possible_device_list))
	else
		nonlocal device_list
		device_list = ["COM3","COM5"]

	print(device_list)

	for device in device_list:
		print("Trying to open port #{0}".format(device))
		prt = serial.Serial()
		prt.baudrate = 115200;
		prt.timeout = 1
		prt.port = device #int(device[-1])

		try:
			prt.open()
			print("Serial port {0} succesfully opened\n".format(prt.portstr))
			return prt
		except serial.SerialException as e:
			print("Unable to open serial port ({0},{1})\n".format(prt.portstr,e))
			continue
	else:
		exit(1)
		# raise Exception("No acceptable devices found")

serialPort = getSerialConnection()

def main():

	try:

		while serialPort.isOpen():
			line = serialPort.readline()
			if len(line) > 0:
				print(line)
				keynum = line[0] - ord('a')
				keystate = 0
				if line[1] == ord('h'):
					keystate = 1
				# FEZ keymap
				keymap = [
					'up','right','down','left',
					'lshift','l','space','j',
					'esc','backspace','lctrl','enter',
					'lalt','a','d','ralt']

				if keynum in range(0,16):
					setKeyState(keymap[keynum],keystate)
				else:
					print("some invalid keycode")

		print("Serial port closed")
		device.close()

	except KeyboardInterrupt:
		print("driver terminated by key-press")
		if serialPort.isOpen():
			serialPort.close()

		device.close()
		return
	except serial.SerialException as e:
		print("Serial port error")
		device.close()

if __name__ == '__main__':
	main()

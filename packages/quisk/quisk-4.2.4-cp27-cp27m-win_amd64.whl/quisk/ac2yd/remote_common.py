# THIS FILE IS FOR USE ON A REMOTELY CONTROLLED "REMOTE_RADIO" COMPUTER
#    RUNNING QUISK TO CONTROL ATTACHED ACTUAL/REAL RADIO HARDWARE.
# IT CONNECTS BY NETWORK TO A SEPARATE "CONTROL_HEAD" COMPUTER ALSO RUNNING QUISK.
#
# This software is Copyright (C) 2021 by Ben Cahill and 2006-2021 by James C. Ahlstrom.,
# and is licensed for use under the GNU General Public License (GPL).
# See http://www.opensource.org.
# Note that there is NO WARRANTY AT ALL.  USE AT YOUR OWN RISK!!
#
# This file, quisk_hardware_remote_radio.py, allows a radio-less (control_head) Quisk,
# running on a separate computer, to connect to this (remote_radio) instance of Quisk,
# which has an actual, real radio attached.
#
# The control_head Quisk must use quisk_hardware_control_head.py to communicate
# with this remote_radio Quisk via network connection.
#
# Set up the remote_radio Quisk by creating a new Radio, then configuring that Radio's
# Hardware (tab) --> "Hardware File Path" to point to this file (use the "Change"
# button to help you find it:  quisk_hardware_remote_radio.py).  Edit this file to:
#
# 1).  Import your usual radio's quisk_hardware_*.py file as BaseHardware, so that
#      quisk_hardware_remote_radio.py is "installed on top of" your usual radio,
#      e.g. for SoftRock USB:
#
#      from softrock.hardware_usb import Hardware as BaseHardware
#
#      NOTE:  You may need to consider how the two radio "layers" interact.
#             e.g. for Softrock, quisk_hardware_remote_radio.py replaces the
#             HeartBeat() and PollCwKey() functions in Softrock's hardware_usb.py
#             This is fine, since Softrock's HeartBeat() is empty, and we won't use the
#             Softrock hardware's built-in paddle port for keying because we will get
#             CW keying from the control_head Quisk computer.  However, other radios
#             might possibly require a call from quisk_hardware_remote_radio.py
#             to invoke the corresponding function in the BaseHardware, e.g.
#             call BaseHardware.PollCwKey() from within this file's PollCwKey()
#
# 2).  Agree with the control_head computer regarding range of ports used, e.g.:
#
#      self.remote_ctl_base_port = 4585		# Remote Control base port
#
# This remote_radio computer should be set up with a static IP address, so that you know
# where to point the control_head.  The control head computer may, however, use dynamic
# addressing; this remote_radio computer will read the control head address when the
# remote control connection is made.
#
# The main control interface between control_head and remote_radio is via a TCP port;
# this uses very low bandwidth.  All functional control, including CW keyihg, is done via this port.
#
# There are 3 additional ports, all UDP, using low to moderate bandwidth:
# -- Send graph/waterfall data to the control_head Quisk
# -- Send radio sound to the control_head Quisk
# -- Receive mic sound from the control_head Quisk
# These use sequential port numbers based on the TCP port number self.remote_ctl_base_port.
#
# The TCP control interface is based on hamlib/rigctld protocol.  However, this is
# not a generic interface to rigctld; it is separate from all other Quisk support for
# hamlib/rigctl, and specific to communicating between quisk_hardware_control_head.py
# and quisk_hardware_remote_radio.py.  It uses generic rigctl protocol when it can;
# however, for best operation, Quisk requires certain information to be passed
# that is awkward for generic rigctl protocol.  For example, frequency control uses a
# "Raw" send_cmd (rigctl 'w'), to enable efficient conveyance of not just the tuning
# frequency, but also VFO frequency, reason for change ("source"), and sometimes band.
#
# The remote_radio Quisk/computer is assumed to track the local control_head Quisk/computer;
# no attempt is made by the control_head to track the remote_radio Quisk's tuning frequency, mode, etc.
# Snap-to Rx tuning for CW works on the control_head Quisk by virtue of graph/waterfall data
# received from the remote_radio Quisk.
#
# To see detailed log output of CW key timing, set DEBUG_CW_JITTER = 1.
# To additionally see, when CW commands are pending, timestamps of when PollCwKey is called
# (e.g. to check thread scheduling behavior), set DEBUG_CW_JITTER = 2.
# To send "perfect" bursts of CW dits from the control_head, set DEBUG_CW_SEND_DITS = 1
# in the control_head's quisk_hardware_control_head.py.
#

DEBUG_CW_JITTER = 0
DEBUG = 0

from collections import deque	# for CW event queue
import socket, time, traceback, string, hmac, secrets
import _quisk as QS
from quisk_widgets import *

class Remot:	# Remote comtrol base class
  def __init__(self, app, conf):
    self.app = app			# Access Quisk class App (Python) functions
    app.remote_control_slave = True
    self.conf = conf
    self.token = "abc"
    self.token_time = 0

    self.control_head_ip = None		# IP of control_head compter (read upon connection)
    self.remote_ctl_base_port = 4585	# Base of ports for remote connection (maybe edit this)
    self.remote_ctl_socket = None
    self.remote_ctl_connection = None
    self.remote_ctl_heartbeat_ts = None
    self.remote_ctl_heartbeat_timeout = 10.0	# Close our connection if we don't hear heartbeat from Control Head
    self.graph_data_port = self.remote_ctl_base_port + 1
    self.graph_data_socket = None
    self.remote_radio_sound_port = self.remote_ctl_base_port + 2
    self.remote_mic_sound_port = self.remote_ctl_base_port + 3

    self.cw_delay = 0.020	# time delay to absorb WiFi jitter, in secs
    self.cw_phrase_begin_ts = None	# timestamp of beginning of cw phrase
    self.cw_next_event_ts = None
    self.cw_next_keydown = None
    self.cw_event_queue = deque()
    self.cw_key_down = 0		# Tx-enable management
    self.cw_tx_enable = 0

    self.received = ''
    self.cmd_text = None	# cmd received from client (remote head)
    self.cmd = None		# cmd received from client (remote head)
    self.params = None		# params = the string following the command
    self.extended = None
    self.split_mode = 0
    QS.set_sparams(remote_control_head=0, remote_control_slave=1)

    print('Remote Overlay Initialized!')

  def open(self):
    self.token = "abc"
    self.remote_ctl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.remote_ctl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.remote_ctl_socket.bind(('', self.remote_ctl_base_port))	# '' == INADDR_ANY
    self.remote_ctl_socket.settimeout(0.0)
    self.remote_ctl_socket.listen(1)	# listen for TCP connection from just one client
    print('Remote Overlay Opened!')
    # Return an informative message for the config screen.
    # This method must return a string showing whether the open succeeded or failed.
    # Here, we are over-writing the string set by quisk_hardware_model.py
    t = f'Quisk Remote Controlled Radio {self.app.width}x{self.app.height} {self.app.graph_width} {self.app.data_width}'
    return t
    #BMC return ret

  def close(self):	# Close the listening socket, then the connection socket
    if self.remote_ctl_socket:
      self.remote_ctl_socket.close()
      self.remote_ctl_socket = None
    self.token = "abc"
    if self.remote_ctl_connection:
      print('Closing Remote Control connection: close')
    self.RemoteCtlClose(True)

  def RemoteCtlOpen(self):
    try:
      self.remote_ctl_connection, address = self.remote_ctl_socket.accept()
    except:
      return
    else:
      self.token = secrets.token_hex(32)
      self.remote_ctl_connection.settimeout(0.0)
      self.remote_ctl_heartbeat_ts = time.time()
      if DEBUG: print('Remote Control connection: ', self.remote_ctl_connection, ' address: ', address)
      self.control_head_ip = address[0]
      print ("Remote control connection from", self.control_head_ip)
      self.RemoteCtlSend("TOKEN;" + self.token + "\n")
      self.token_time = time.time()

  def RemoteCtlClose(self, send_quit):
    self.StopTransmit()
    if self.remote_ctl_connection:
      if send_quit:
        self.RemoteCtlSend('Q\n')
    if self.remote_ctl_connection:
      self.remote_ctl_connection.close()
    self.remote_ctl_connection = None
    if self.graph_data_socket:
      self.graph_data_socket.close()
    self.graph_data_socket = None
    QS.stop_remote_radio_remote_sound()

  def RemoteCtlSend(self, text):
    # Send text back to the client
    if not self.remote_ctl_connection:
      return
    if isinstance(text, str):
      text = text.encode('utf-8', errors='ignore')
    try:
      self.remote_ctl_connection.sendall(text)
    except socket.error:
      print('Closing Remote Control connection: sendall() failed.  Sent text:\n    '  + text.decode('utf-8'))
      # NOTE:  Cannot send 'Q' to Control Head here; sendall() isn't working!
      self.RemoteCtlClose(False)

  def ErrParam(self):		# Invalid parameter
    t = 'ERR_PARAM: ' + self.cmd_text + '\n'
    print(t)
    self.RemoteCtlSend(t)
  def ErrUnsupported(self):	# Command recognized but not supported (because of either H/W or configuration)
    t = 'ERR_UNSUPPORTED: ' + self.cmd_text + '\n'
    print(t)
    self.RemoteCtlSend(t)
  def ErrUnrecognized(self):	# Unrecognized command
    t = 'ERR_UNRECOGNIZED_CMD: ' + self.cmd_text + '\n'
    print(t)
    self.RemoteCtlSend(t)
  def ErrBadFormat(self):	# Something wrong with format of command
    t = 'ERR_BADFORMAT: ' + self.cmd_text + '\n'
    print(t)
    self.RemoteCtlSend(t)

  def HeartBeat(self):	# Called at about 10 Hz by the GUI thread
    if self.remote_ctl_connection:
      # Monitor the remote connection via periodic heartbeat from Control Head
      ts = time.time()
      if (ts - self.remote_ctl_heartbeat_ts) > self.remote_ctl_heartbeat_timeout:
        print('Closing Remote Control connection: Lost HEARTBEAT from Control Head')
        self.RemoteCtlClose(True)
    else:
      # Continually try to connect with Control Head
      self.RemoteCtlOpen()

  def FastHeartBeat(self):	# Called frequently by the GUI thread
    """This is the remote slave processing loop, and is called frequently.  It reads and satisfies requests."""
    if not self.remote_ctl_connection:
      return
    try:	# Read any data from the socket
      text = self.remote_ctl_connection.recv(1024)
    except:
      #traceback.print_exc()
      return
    else:					# We got some characters
      if not isinstance(text, str):
        text = text.decode('utf-8')
      self.received += text
    if not '\n' in self.received:	# A complete command ending with newline is not available
      return
    while '\n' in self.received:	# At least one complete command ending with newline *is* available
      cmd_text, self.received = self.received.split('\n', 1)	# Split off the command, save any further characters
      cmd_text = cmd_text.strip()	# Here is our command
      if not cmd_text:
        continue
      self.cmd_text = cmd_text
      args = cmd_text.split(';')	# Split at ';' because some control names have blanks
      command = args[0]
      param = args[1:]
      # TOKEN
      if self.token:
        if command == "TOKEN":
          passw = self.app.local_conf.globals.get("remote_radio_password", "")
          passw = passw.strip()
          if not passw:
            self.RemoteCtlSend("TOKEN_MISSING\n")
            print ("Error: Missing password on remote radio")
            continue
          H = hmac.new(passw.encode('utf-8'), self.token.encode('utf-8'), 'sha3_256')
          del passw
          if hmac.compare_digest(H.hexdigest(), args[1]):
            self.token = None
            print ("Security challenge passed")
            self.RemoteCtlSend("TOKEN_OK\n")
            self.remote_ctl_heartbeat_ts = time.time()
            self.graph_data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.graph_data_socket.settimeout(0.0)
            QS.start_remote_radio_remote_sound(self.control_head_ip, self.remote_radio_sound_port, self.remote_mic_sound_port)
          else:
            time.sleep(1)
        elif time.time() - self.token_time > 5:
          self.RemoteCtlSend("TOKEN_BAD\n")
          self.RemoteCtlClose(TRUE)
          print ("Security failed")
        continue
      # Check for Quit and Heartbeat before any other commands
      if command == 'QUIT':
        print('Closing Remote Control connection: QUIT from Control Head')
        # NOTE:  Do not send 'Q' to Control Head; sendall() will fail because Control Head already disconnected
        self.RemoteCtlClose(False)
        continue
      # HEARTBEAT
      if command == 'HEARTBEAT':
        self.remote_ctl_heartbeat_ts = time.time()
        continue
      # buttons in idName2Button
      btn = self.app.idName2Button.get(args[0], None)
      if btn:
        #print ("Slave process button", cmd_text, btn.__class__)
        value = int(args[1])
        btn.SetIndex(value, True)
        continue
      # controls in midiControls
      if command in self.app.midiControls:
        ctrl, func = self.app.midiControls[command]
        #print ("Slave Process control", cmd_text, ctrl.__class__, func)
        value = int(args[1])
        if isinstance(ctrl, WrapSlider):
          ctrl.ChangeSlider(value)
        else:
          ctrl.SetValue(value)
          func()
        continue
      # FREQ
      if command == 'FREQ':
        freq, vfo, source, band, rxFreq, var_decim_index = args[1:]
        freq = int(freq)
        vfo = int(vfo)
        rxFreq = int(rxFreq)
        new_rxfreq = (rxFreq != self.app.rxFreq)
        self.app.rxFreq = rxFreq
        var_decim_index = int(var_decim_index)
        self.app.ChangeDisplayFrequency(freq - vfo, vfo, new_rxfreq)
        if source == "NewDecim":
          self.app.config_screen.config.btn_decimation.SetSelection(var_decim_index)
          sample_rate = self.VarDecimSet(var_decim_index)
          print ("sample_rate", sample_rate)
          self.app.OnBtnDecimation(rate=sample_rate)
      # AGC and Squelch levels
      elif command == 'AGCSQLCH':
        ctrl = self.app.midiControls["AGCSlider"][0]
        ctrl.SetSlider(value_off=int(args[1]), value_on=int(args[2]))
        self.app.levelSquelch = int(args[3])
        self.app.levelSquelchSSB = int(args[4])
        self.app.split_offset = int(args[5])
      # CW Keying
      elif command == 'CW':
        ts = time.time()
        if len(params) < 2:
          self.ErrParam()
          return
        if params[0] in '01':
          keydown = int(params[0])
        else:
          print('Bad keydown value in CW command:', params[0])
          self.ErrParam()
          return
        cw_event_ts = float(params[1]) / 1000.0     # int msecs to float secs
        if cw_event_ts == 0.0:
          if keydown != 1:
            # 'CW 0 0' == "Force Stop of CW"; clear all queued CW commands, and force CW key up
            print('Forcing stop of CW')
            while len(self.cw_event_queue):
              self.cw_event_queue.popleft()
            self.cw_next_event_ts = None
            self.cw_next_keydown = None
            self.cw_key_down = 0
            QS.set_cwkey(0)
          else:
            # Begin new cw phrase; any prior phrase should be done by now.
            # Set up first cw event to be ready to execute.
            self.cw_begin_phrase_ts = ts + self.cw_delay
        cw_new_event_ts = self.cw_begin_phrase_ts + cw_event_ts 
        if not self.cw_next_event_ts:
          self.cw_next_event_ts = cw_new_event_ts
          self.cw_next_keydown = keydown
          if DEBUG_CW_JITTER: print(f'{ts:10.4f} setting: {keydown} {cw_event_ts:2.3f} {cw_new_event_ts:10.4f}')
        else:
          self.cw_event_queue.append((cw_new_event_ts, keydown))
          if DEBUG_CW_JITTER: print(f'{ts:10.4f} queing:  {keydown} {cw_event_ts:2.3f} {cw_new_event_ts:10.4f}')
      # Menu
      elif command == 'MENU':
        menu_name, item_text, checked = args[1:]
        if item_text == 'Reverse Rx and Tx':
          continue	# No need to call handler, as rxFreq and txFreq are already handled
        menu = getattr(self.app, menu_name)
        nid = menu.item_text2id[item_text]
        menu.Handler(None, nid)
        menu_item = menu.FindItemById(nid)
        if menu_item.IsCheckable():
          menu_item.Check(int(checked))
      # Main window and graph/waterfall dimensions; graph data_width of control_head and remote_radio must match.
      elif command == 'X':
        ctl_width = int(param[0])
        ctl_height = int(param[1])
        ctl_graph_width = int(param[2])
        ctl_data_width = int(param[3])
        if self.app.data_width != ctl_data_width:
          print('WARNING:  Control head graph data width', ctl_data_width, 'different from remote radio graph data width', self.app.data_width)
        # Return remote_radio window and graph dimensions to control_head, so it can verify graph data_width is same
        t = f'X;{self.app.width};{self.app.height};{self.app.graph_width};{self.app.data_width}\n'
        self.RemoteCtlSend(t)
      # Help buttons ".."
      elif command == '..':
        pass
      else:
        t = 'ERR_UNRECOGNIZED_CMD: %s\n' % cmd_text
        print(t)
        self.RemoteCtlSend(t)
      continue

  def PollCwKey(self):	# Called periodically at HW Poll usec period (typ. 50-200 Hz) by the sound thread
    cw_queue_len = len(self.cw_event_queue)
    if self.cw_next_event_ts or cw_queue_len > 0:
      # We have at least one CW event. If it's time to do so, set the next CW key down/up, look for next CW event.
      ts = time.time()
      if DEBUG_CW_JITTER > 1: print(f'{ts:10.4f}')
      if not self.cw_next_event_ts:
        # Nothing "on deck", but there is something on the cw event queue, so pop it off queue and put it "on deck".
        self.cw_next_event_ts, self.cw_next_keydown = self.cw_event_queue.popleft()
        if DEBUG_CW_JITTER: print(f'{ts:10.4f} queue len: {cw_queue_len}, popping: {self.cw_next_keydown} {self.cw_next_event_ts:10.4f}')
      if ts >= self.cw_next_event_ts:
        if DEBUG_CW_JITTER: print(f'{ts:10.4f} set_cwkey: {self.cw_next_keydown}')
        QS.set_cwkey(self.cw_next_keydown)
        self.cw_key_down = self.cw_next_keydown
        cw_queue_len = len(self.cw_event_queue)
        if cw_queue_len > 0:
          self.cw_next_event_ts, self.cw_next_keydown = self.cw_event_queue.popleft()
          if DEBUG_CW_JITTER: print(f'{ts:10.4f} queue len: {cw_queue_len}, popping: {self.cw_next_keydown} {self.cw_next_event_ts:10.4f}')
        else:
          self.cw_next_event_ts = None
          self.cw_next_keydown = None

  def StopTransmit(self):
    # TODO:  Add code for modes other than CW
    while len(self.cw_event_queue):
      self.cw_event_queue.popleft()
    self.cw_next_event_ts = None
    self.cw_next_keydown = None
    self.cw_key_down = 0
    QS.set_cwkey(0)

  def GetGraph(self, k, zoom, deltaf):
    data = QS.get_graph(k, zoom, deltaf)	# get FFT data
    if data:
      self.RemoteCtlSend("M;%s\n" % self.app.smeter.GetLabel())
      if self.graph_data_socket:
        # Convert from tuple of floats to packed array of int8 (bytes)
        # Floats are -200.0 to 0.0; change sign to +, reverse on reception
        barray = bytearray()
        for d in data:
          barray.append(int( - d + 0.5))
        try:
          self.graph_data_socket.sendto(barray, (self.control_head_ip, self.graph_data_port))
        except socket.timeout:	# This does not work
          pass
        except socket.error:	# No write capacity(?) ... this avoids Python throwing error
          pass
    return data

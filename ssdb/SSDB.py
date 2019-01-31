# encoding=utf-8
# Generated by cpy
# 2016-04-11 20:40:38.174634
import os, sys
from sys import stdin, stdout

import socket
class SSDB_Response(object):
	pass


	def __init__(self, code='', data_or_message=None):
		pass
		self.type = 'none'
		self.code = code
		self.data = None
		self.message = None
		self.set(code, data_or_message)

	def set(self, code, data_or_message=None):
		pass
		self.code = code

		if code=='ok':
			pass
			self.data = data_or_message
		else:
			pass

			if isinstance(data_or_message, list):
				pass

				if len(data_or_message)>0:
					pass
					self.message = data_or_message[0]
			else:
				pass
				self.message = data_or_message

	def __repr__(self):
		pass
		return ((((str(self.code) + ' ') + str(self.message)) + ' ') + str(self.data))

	def ok(self):
		pass
		return self.code=='ok'

	def not_found(self):
		pass
		return self.code=='not_found'

	def str_resp(self, resp):
		pass
		self.type = 'val'

		if resp[0]=='ok':
			pass

			if len(resp)==2:
				pass
				self.set('ok', resp[1])
			else:
				pass
				self.set('server_error', 'Invalid response')
		else:
			pass
			self.set(resp[0], resp[1 : ])
		return self

	def int_resp(self, resp):
		pass
		self.type = 'val'

		if resp[0]=='ok':
			pass

			if len(resp)==2:
				pass
				try:
					pass
					val = int(resp[1])
					self.set('ok', val)
				except Exception as e:
					pass
					self.set('server_error', 'Invalid response')
			else:
				pass
				self.set('server_error', 'Invalid response')
		else:
			pass
			self.set(resp[0], resp[1 : ])
		return self

	def float_resp(self, resp):
		pass
		self.type = 'val'

		if resp[0]=='ok':
			pass

			if len(resp)==2:
				pass
				try:
					pass
					val = float(resp[1])
					self.set('ok', val)
				except Exception as e:
					pass
					self.set('server_error', 'Invalid response')
			else:
				pass
				self.set('server_error', 'Invalid response')
		else:
			pass
			self.set(resp[0], resp[1 : ])
		return self

	def list_resp(self, resp):
		pass
		self.type = 'list'
		self.set(resp[0], resp[1 : ])
		return self

	def int_map_resp(self, resp):
		pass
		self.type = 'map'

		if resp[0]=='ok':
			pass

			if len(resp) % 2==1:
				pass
				data = {'index': [],'items': {},}
				i = 1

				while i<len(resp):
					pass
					k = resp[i]
					v = resp[(i + 1)]
					try:
						pass
						v = int(v)
					except Exception as e:
						pass
						v = - (1)
					data['index'].append(k)
					data['items'][k] = v
					pass
					i += 2
				self.set('ok', data)
			else:
				pass
				self.set('server_error', 'Invalid response')
		else:
			pass
			self.set(resp[0], resp[1 : ])
		return self

	def str_map_resp(self, resp):
		pass
		self.type = 'map'

		if resp[0]=='ok':
			pass

			if len(resp) % 2==1:
				pass
				data = {'index': [],'items': {},}
				i = 1

				while i<len(resp):
					pass
					k = resp[i]
					v = resp[(i + 1)]
					data['index'].append(k)
					data['items'][k] = v
					pass
					i += 2
				self.set('ok', data)
			else:
				pass
				self.set('server_error', 'Invalid response')
		else:
			pass
			self.set(resp[0], resp[1 : ])
		return self

class SSDB(object):
	pass


	def __init__(self, host, port):
		pass
		self.recv_buf = ''
		self._closed = False
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(tuple([host, port]))
		self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

	def close(self):
		pass

		if not (self._closed):
			pass
			self.sock.close()
			self._closed = True

	def closed(self):
		pass
		return self._closed

	def request(self, cmd, params=None):
		pass

		if params==None:
			pass
			params = []
		params = ([cmd] + params)
		self.send(params)
		resp = self.recv()

		if resp==None:
			pass
			return SSDB_Response('error', 'Unknown error')

		if len(resp)==0:
			pass
			return SSDB_Response('disconnected', 'Connection closed')
		ret = SSDB_Response()

		# {{{ switch: cmd
		_continue_1 = False
		while True:
			if False or ((cmd) == 'ping') or ((cmd) == 'set') or ((cmd) == 'del') or ((cmd) == 'qset') or ((cmd) == 'zset') or ((cmd) == 'hset') or ((cmd) == 'qpush') or ((cmd) == 'qpush_front') or ((cmd) == 'qpush_back') or ((cmd) == 'zdel') or ((cmd) == 'hdel') or ((cmd) == 'multi_set') or ((cmd) == 'multi_del') or ((cmd) == 'multi_hset') or ((cmd) == 'multi_hdel') or ((cmd) == 'multi_zset') or ((cmd) == 'multi_zdel'):
				pass

				if len(resp)>1:
					pass
					return ret.int_resp(resp)
				else:
					pass
					return SSDB_Response(resp[0], None)
				break

			if False or ((cmd) == 'version') or ((cmd) == 'substr') or ((cmd) == 'get') or ((cmd) == 'getset') or ((cmd) == 'hget') or ((cmd) == 'qfront') or ((cmd) == 'qback') or ((cmd) == 'qget'):
				pass
				return ret.str_resp(resp)

			if False or ((cmd) == 'qpop') or ((cmd) == 'qpop_front') or ((cmd) == 'qpop_back'):
				pass
				size = 1
				try:
					pass
					size = int(params[2])
				except Exception as e:
					pass

				if size==1:
					pass
					return ret.str_resp(resp)
				else:
					pass
					return ret.list_resp(resp)
				break

			if False or ((cmd) == 'dbsize') or ((cmd) == 'getbit') or ((cmd) == 'setbit') or ((cmd) == 'countbit') or ((cmd) == 'bitcount') or ((cmd) == 'strlen') or ((cmd) == 'ttl') or ((cmd) == 'expire') or ((cmd) == 'setnx') or ((cmd) == 'incr') or ((cmd) == 'decr') or ((cmd) == 'zincr') or ((cmd) == 'zdecr') or ((cmd) == 'hincr') or ((cmd) == 'hdecr') or ((cmd) == 'hsize') or ((cmd) == 'zsize') or ((cmd) == 'qsize') or ((cmd) == 'zget') or ((cmd) == 'zrank') or ((cmd) == 'zrrank') or ((cmd) == 'zsum') or ((cmd) == 'zcount') or ((cmd) == 'zremrangebyrank') or ((cmd) == 'zremrangebyscore') or ((cmd) == 'hclear') or ((cmd) == 'zclear') or ((cmd) == 'qclear') or ((cmd) == 'qpush') or ((cmd) == 'qpush_front') or ((cmd) == 'qpush_back') or ((cmd) == 'qtrim_front') or ((cmd) == 'qtrim_back'):
				pass
				return ret.int_resp(resp)

			if False or ((cmd) == 'zavg'):
				pass
				return ret.float_resp(resp)

			if False or ((cmd) == 'keys') or ((cmd) == 'rkeys') or ((cmd) == 'zkeys') or ((cmd) == 'zrkeys') or ((cmd) == 'hkeys') or ((cmd) == 'hrkeys') or ((cmd) == 'list') or ((cmd) == 'hlist') or ((cmd) == 'hrlist') or ((cmd) == 'zlist') or ((cmd) == 'zrlist'):
				pass
				return ret.list_resp(resp)

			if False or ((cmd) == 'scan') or ((cmd) == 'rscan') or ((cmd) == 'hgetall') or ((cmd) == 'hscan') or ((cmd) == 'hrscan'):
				pass
				return ret.str_map_resp(resp)

			if False or ((cmd) == 'zscan') or ((cmd) == 'zrscan') or ((cmd) == 'zrange') or ((cmd) == 'zrrange') or ((cmd) == 'zpop_front') or ((cmd) == 'zpop_back'):
				pass
				return ret.int_map_resp(resp)

			if False or ((cmd) == 'auth') or ((cmd) == 'exists') or ((cmd) == 'hexists') or ((cmd) == 'zexists'):
				pass
				return ret.int_resp(resp)

			if False or ((cmd) == 'multi_exists') or ((cmd) == 'multi_hexists') or ((cmd) == 'multi_zexists'):
				pass
				return ret.int_map_resp(resp)

			if False or ((cmd) == 'multi_get') or ((cmd) == 'multi_hget'):
				pass
				return ret.str_map_resp(resp)

			if False or ((cmd) == 'multi_hsize') or ((cmd) == 'multi_zsize') or ((cmd) == 'multi_zget'):
				pass
				return ret.int_map_resp(resp)

			### default
			return ret.list_resp(resp)

			if _continue_1:
				continue
		# }}} switch

		return SSDB_Response('error', 'Unknown error')

	def send(self, data):
		pass
		ps = []

		_cpy_r_0 = _cpy_l_1 = data
		if type(_cpy_r_0).__name__ == 'dict': _cpy_b_3=True; _cpy_l_1=_cpy_r_0.iterkeys()
		else: _cpy_b_3=False
		for _cpy_k_2 in _cpy_l_1:
			if _cpy_b_3: p=_cpy_r_0[_cpy_k_2]
			else: p=_cpy_k_2
			pass
			p = str(p)
			ps.append(str(len(p)))
			ps.append(p)
		nl = '\n'
		s = (nl.join(ps) + '\n\n')
		try:
			pass

			while True:
				pass
				ret = self.sock.send(s)

				if ret==0:
					pass
					return - (1)
				s = s[ret : ]

				if len(s)==0:
					pass
					break
		except socket.error as e:
			pass
			return - (1)
		return ret

	def net_read(self):
		pass
		try:
			pass
			data = self.sock.recv(1024 * 8)
		except Exception as e:
			pass
			data = ''

		if data=='':
			pass
			self.close()
			return 0
		self.recv_buf += data
		return len(data)

	def recv(self):
		pass

		while True:
			pass
			ret = self.parse()

			if ret==None:
				pass

				if self.net_read()==0:
					pass
					return []
			else:
				pass
				return ret

	def parse(self):
		pass
		ret = []
		spos = 0
		epos = 0

		while True:
			pass
			spos = epos
			epos = self.recv_buf.find('\n', spos)

			if epos==- (1):
				pass
				break
			epos += 1
			line = self.recv_buf[spos : epos]
			spos = epos

			if line.strip()=='':
				pass

				if len(ret)==0:
					pass
					continue
				else:
					pass
					self.recv_buf = self.recv_buf[spos : ]
					return ret
			try:
				pass
				num = int(line)
			except Exception as e:
				pass
				return []
			epos = (spos + num)

			if epos>len(self.recv_buf):
				pass
				break
			data = self.recv_buf[spos : epos]
			ret.append(data)
			spos = epos
			epos = self.recv_buf.find('\n', spos)

			if epos==- (1):
				pass
				break
			epos += 1
		return None

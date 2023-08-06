####################################################################
#/ Nom du projet: py-zpp_args                                     /#
#/ Nom du fichier: args.py                                        /#
#/ Type de fichier: fichier principal                             /#
#/ Fichier annexe:                                                /#
#/                                                                /#
#/ Auteur: ZephyrOff  (Alexandre Pajak)                           /#
#/ Version: 1.2.2                                                 /#
#/ Description: Module pour le traitement des arguments d'une     /#
#/              ligne de commande                                 /#
#/ Date: 29/08/2022                                               /#
####################################################################

import sys
import inspect
import re

def get_origin_value():
	frame = inspect.currentframe()
	frame = inspect.getouterframes(frame)[2]
	string = inspect.getframeinfo(frame[0]).code_context[0].strip()
	args = string[string.find('(') + 1:-1].split(',')

	names = []
	for i in args:
		if i.find('=') != -1:
			names.append(i.split('=')[1].strip())
		else:
			names.append(i)
	return names


def digit(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

class StoreArgument():
	def __init__(self):
		pass

	def list_all(self):
		return self.__dict__

	def __contains__(self, key):
		return key in self.__dict__


class parser():
	def __init__(self, source=None, error_lock=False):
		self.available_arg = []
		self.available_param = []
		self.error_lock = error_lock
		self.check_parameter = True

		if source==None:
			self.command = sys.argv[0]
			self.source=sys.argv[1:]
		else:
			if "sys.argv" in get_origin_value()[0]:
				self.command = source[0]
				self.source = source[1:]
			else:
				self.command, self.source = self.arg_parse(source)

	def search(self, option):
		for element in self.available_arg:
			if element['longname']==option:
				return element
		return None


	def find_short(self, name):
		for element in self.available_arg:
			if element['shortcut']==name:
				return element
		return None


	def set_param(self,option,val,store):
		if not hasattr(self.argument, option):
			if store=="digit":
				if isinstance(val, str):
					if val.isdigit():
						val = int(val)
					else: 
						val = float(val)
				elif isinstance(val, int) or isinstance(val, float):
					pass
				else:
					return False
			setattr(self.argument, option, val)
			return True
		else:
			print(f"Argument {option} already set")
			return False


	def set_result(self,option):
		if option['longname']:
			name = option['longname']
		else:
			name = option['shortcut']

		if option['store']=="value":
			if len(self.source)>0 and self.source[0].startswith('-')==False:
				if option['type']!=None:
					val_arg = self.source.pop(0)
					if option['type']=="str" or (option['type']=="digit" and digit(val_arg)):
						if not self.set_param(name,val_arg,option['type']):
							return None
					else:
						print(f"Argument {name}: Bad value type")
						if "default" in option.keys():
							if not self.set_param(name,option['default'],option['type']):
								return None
						else:
							return None
				else:
					if not self.set_param(name,self.source.pop(0),option['type']):
						return None
			else:
				print(f"Argument {name}: Missing value")
				if "default" in option.keys() and option['default']!=None:
					if not self.set_param(name,option['default'],option['type']):
						return None
				else:
					return None

		elif option['store']=="bool":
			if not self.set_param(name,True,option['type']):
				return None
		return 1


	def load(self):
		self.parameter = []
		self.argument = StoreArgument()

		msg_error = "\nError: "

		while(len(self.source)!=0):
			element = self.source.pop(0)
			if element.startswith('--'):
				option = element[2:]
				if option=="help":
					self.help()
					return None, None
				else:
					find = self.search(option)
					if find!=None:
						status_code = self.set_result(find)
						if status_code==None and self.error_lock:
							return None, None
					else:
						msg_error += f"\n  Argument {option} not available"

			elif element.startswith('-'):
				if "h" in element[1:]:
					self.help()
					return None, None
				else:
					for option in element[1:]:
						f = self.find_short(option)
						if f!=None:
							status_code = self.set_result(f)
							if status_code==None and self.error_lock:
								return None, None
						else:
							msg_error += f"\n  Argument {option} not available"

			else:
				self.parameter.append(element)

		msg=""
		for ar in self.available_arg:
			if not (hasattr(self.argument, ar['shortcut']) or hasattr(self.argument, ar['longname'])):
				if ar['longname']:
					name = ar['longname']
				else:
					name = ar['shortcut']
				if "default" in ar.keys():
					self.set_param(name,ar['default'],ar['type'])

				elif ar['store']=="bool":
					self.set_param(name,False,"str")


				if ar['required']==True and not (hasattr(self.argument, ar['shortcut']) or hasattr(self.argument, ar['longname'])):
					set_default=False
					if "default" in ar.keys():
						if ar['longname']:
							name = ar['longname']
						else:
							name = ar['shortcut']

						if self.set_param(name,ar['default'],ar['type']):
							set_default=True

					if set_default==False:
						if ar['shortcut']=="":
							n = ar['longname']
						else:
							n = ar['shortcut']
						if len(msg)==0:
							msg=n
						else:
							msg+=", "+n

		if self.check_parameter==True and len(self.available_param)<len(self.parameter):
			msg_error+=f"Missing parameter ({len(self.available_param)} needed but {len(self.parameter)} received)"

		if len(msg)!=0:
			msg_error += f"\n  Argument {msg} not initialized"
			self.help()
			print(msg_error)
			return None, None

		if msg_error!="\nError: ":
			print(msg_error)
			if self.error_lock:
				return None, None

		return self.parameter, self.argument


	def arg_parse(self, string):
		command = string[0]
		del string[0]
		array = []

		if len(string)>=1:
			arg = ""
			lock = None
			if isinstance(string, list):
				string = " ".join(string)
			for i,caracter in enumerate(string):
				if (caracter=="'" or caracter=='"') and (lock==None or caracter==lock):
					if lock==None:
						lock=caracter
					else:
						array.append(arg)
						arg=""
						lock=None
				else:
					if caracter==" " and lock!=None:
						arg+=caracter
					elif caracter==" " and len(arg)>=1 and lock==None:
						array.append(arg)
						arg=""
					elif caracter!=" ":
						arg+=caracter
						if i==len(string)-1:
							array.append(arg)
							arg=""

		return command, array


	def already_exist(self,shortcut,longname):
		for el in self.available_arg:
			if shortcut!="" and shortcut==el['shortcut']:
				return True

			if longname!=None and longname!="" and longname==el['longname']:
				return True
		return False

	def param_exist(self,name):
		for el in self.available_param:
			if el['name']==name:
				return True
		return False

	def set_parameter(self, name, description=None):
		if not self.param_exist(name):
			insert = {'name': name, 'description': description}
			self.available_param.append(insert)
		else:
			print(f"Parameter {name} already set")


	def set_argument(self, shortcut="", longname=None, type=None, default="", description=None, required=False, store="bool"):
		if self.already_exist(shortcut,longname):
			print("Error for setting argument")
		else:
			if shortcut!="" or longname!=None:
				if shortcut!="h" and longname!="help":
					insert = {'shortcut': shortcut, 'longname': longname}
					if default!="":
						insert['default'] = default
					insert['description'] = description

					if type=="str" or type=="digit":
						insert['type'] = type
					else:
						insert['type'] = None
					
					if isinstance(required,bool):
						insert['required'] = required
					else:
						insert['required'] = False

					if store=="value" or store=="bool":
						insert['store'] = store
					else:
						insert['store'] = "bool"
					self.available_arg.append(insert)
				else:
					print("Argument h(help) not authorized")
			else:
				print("Error for setting argument")
			

	def set_description(self, description):
		if len(description)!=0:
			self.main_description = description

	def disable_check(self):
		self.check_parameter = False

	def help(self):
		mm = self.command + " [-h]"

		for a in self.available_arg:
			if a['shortcut']!="":
				val = a['shortcut']
			else:
				val = "-"+a['longname']

			if a['required']:
				if a['store']=="value":
					mm+=" -"+val+" VALUE"
				else:
					mm+=" -"+val

			else:
				mm+=" ["
				if a['store']=="value":
					mm+="-"+val+" VALUE"
				else:
					mm+="-"+val

				mm+="]"

		for a in self.available_param:
			mm+=" "+a['name'].upper()

		print("\nUsage: "+mm)

		if hasattr(self, "main_description"):
			print("\nDescription:\n  "+self.main_description)

		if len(self.available_arg)!=0:
			ar = []
			maxsize = 0
			print("\nArguments:")
			for a in self.available_arg:
				ins = ["",""]
				if a['shortcut']!="":
					ins[0]="  -"+a['shortcut']
					if a['longname']:
						ins[0]+=", --"+a['longname']
				else:
					ins[0]="  --"+a['longname']
				if a['store']=="value":
					ins[0]+=" VALUE"

				if a['description']:
					ins[1]+=a['description']

				if a['required']:
					if len(ins[1])!=0:
						ins[1]+=" "
					ins[1]+="(Required)"

				if a['type']=="digit":
					if len(ins[1])!=0:
						ins[1]+=" "
					ins[1]+=" (Type: digit)"
					
				if "default" in a.keys() and a['default']:
					if len(ins[1])!=0:
						ins[1]+=" "

					if a['default']==True:
						ins[1]+=" (Default Value: True)"
					elif a['default']==False:
						ins[1]+=" (Default Value: False)"
					else:
						ins[1]+=" (Default Value: "+a['default']+")"

				if len(ins[0])>maxsize:
					maxsize = len(ins[0])

				ar.append(ins)

			for a in ar:
				print(a[0]+" "*((maxsize-len(a[0]))+3)+a[1])

		if len(self.available_param)!=0:
			ar = []
			maxsize = 0
			print("\nParameters:")
			for a in self.available_param:
				ar.append([a['name'],a['description']])

				if len(a['name'])>maxsize:
					maxsize = len(a['name'])

			for a in ar:
				print("  "+a[0].upper()+" "*((maxsize-len(a[0]))+3)+a[1])

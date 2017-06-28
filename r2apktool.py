import r2pipe
import argparse
import os
import codecs
import errno
import sys
import shutil
from subprocess import Popen, PIPE
from datetime import datetime

def mkdir_p(path):
	try:
		os.makedirs (path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir (path):
			pass
		else:
			raise

def getPathFromClassname(classname):
	return os.path.dirname (classname)

def parseSymbols(symbols):
	a = {}
	for symbol in symbols:
		if symbol['size'] > 0 and symbol['type'] == "FUNC":
			a[symbol['paddr']] = symbol['size']
	return a


def printFields(F, fields, ftype = "ifield"):
	for field in fields:
		if ftype in field['name']:
			name = field['name'][field['name'].index ("field")+6:]
			if not "flags" in field or len (field['flags']) == 0:
				field['flags'] = ["private"]
			flags = "".join (field['flags'])
			F.write (".field %s %s \n" % (flags, name))

def printMethod(F, r2, method, size = None):
	F.write (".method %s %s\n" % (" ".join (method['flags']), method['name'].split (".")[2]))
	if size:
		pdj = r2.cmdj ("pDj %d @ %d" % (size, method['addr']))
		for op in pdj:
			F.write ("    %s\n\n" % op['opcode'])
	else:
		r2.cmd("af @ %d" % method['addr'])
		pdf = r2.cmdj ("pdfj @ %d" % (method['addr']))
		for op in pdf['ops']:
			F.write ("    %s\n\n" % op['opcode'])

def printMethods(F, r2, methods, sizes, direct = True):
	for method in methods:
		if not "flags" in method or len (method['flags']) == 0:
			method['flags'] = ["private"]
		if "abstract" in method['flags']:
			continue
		elif direct and ("static" in method['flags'] or "private"  in method['flags'] or "constructor" in method['flags']):
			printMethod (F, r2, method, sizes[method['addr']])
		elif not direct and not ("static" in method['flags'] or "private"  in method['flags'] or "constructor" in method['flags']):
			printMethod (F, r2, method, sizes[method['addr']])


def decompileSmali(apk_file, out_path):
	os.makedirs (out_path)

	try:
		r2 = r2pipe.open ("apk://" + apk_file)
	except Exception as e:
		print e
		sys.exit()

	r2.cmd ("e asm.comments = false")
	r2.cmd ("e asm.slow = false")
	r2.cmd ("e asm.demangle = false")

	sizes = parseSymbols (r2.cmdj ("isj"))

	classes = r2.cmdj ("icj")

	for clazz in classes:
		mkdir_p (out_path + "/" + getPathFromClassname (clazz['classname'][1:]))
		smali_file = out_path+"/"+clazz['classname'][1:]+".smali"
		with codecs.open (smali_file, mode="w", encoding="UTF-8") as F:
			F.write (".class %s %s;\n" % ("public", clazz['classname']) )
			
			if "super" in clazz:
				F.write (".super %s\n" % (clazz['super']) )

			F.write ("\n\n# instance fields\n")
			printFields (F, clazz['fields'], "ifield")

			F.write ("\n\n# static fields\n")
			printFields (F, clazz['fields'], "sfield")

			F.write ("\n\n# direct methods\n")
			printMethods (F, r2, clazz['methods'], sizes, True)			

			F.write ("\n# virtual methods\n")
			printMethods (F, r2, clazz['methods'], sizes, False)


	r2.quit ()

def main():

	parser = argparse.ArgumentParser (description='r2apktool.')
	parser.add_argument ('file', type=str, help='apk file to decompile')
	parser.add_argument ('-f', action='store_true', help='sum the integers (default: find the max)')

	args = parser.parse_args ()
	apk_file = os.path.abspath (args.file)

	filename = os.path.basename (apk_file)
	out_path = os.path.splitext (filename)[0]

	if os.path.exists (out_path):
		if args.f:
			shutil.rmtree (out_path)
		else:
			print "The path already exists. You can overwrite it with -f option."
			sys.exit ()


	cmd = ["radare2", "-v"]
	try:
		process = Popen(cmd, shell=False, stdin=PIPE, stdout=PIPE)
		r2_version = process.stdout.read()
	except:
		print("ERROR: Cannot find radare2 in PATH")
		sys.exit()

	r2_build_date = r2_version[-21:-11]
	r2_build_date = datetime.strptime(r2_build_date, '%Y-%m-%d')
	delta = r2_build_date - datetime.today()
	if delta.days < -7:
		print "WARNING: Your version of radare2 is quite old, please consider upgrade it to the last version from git."

	decompileSmali (apk_file, out_path)


if __name__ == '__main__':
	main ()

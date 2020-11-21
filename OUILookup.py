import getopt, sys, requests
from getmac import get_mac_address

# Use: ./OUILookup --ip <IP> | --mac <IP> [--help]
# Parametros: 
# --ip    : specify the IP of the host to query.
# --mac   : specify the MAC address to query. P.e. aa:bb:cc:00:00:00.
# --help  : show this message and quit.

# CUERPO PRINCIPAL :
def main():
    try:
        if (len(sys.argv)==1):															# Si no se ingreso ningun parametro
        	help()																		# Se llama a la funcion help
        	return(0)
        options, args = getopt.getopt(sys.argv[1:],"ip,mac",['ip=','mac=','help'])		# Se definen los parametros 

    except:																				# En caso de error
        print("\n ¡Error!: Parametros incorrectos.")
        help()
        return(1)
    
    for opt, arg in options:
        if opt in ('--help'):
            help()
        elif opt in ('--ip'):
            if(verificarip(arg)):
                ip(arg)
            else:
                print("ERROR EN ARGUMENTOS")

        elif opt in ('--mac'):
            if(verificarmac(arg)):
                mac(arg)
            else:
                print("\n\tERROR EN ARGUMENTOS\n\t")	

# FUNCION HELP : Muestra el mensaje inicial y sale.
def help():
	print("\n Use: ./OUILookup --ip <IP> | --mac <IP> [--help]")
	print("\t--ip : specify the IP of the host to query.\n\t--mac: specify the MAC address to query. P.e. aa:bb:cc:00:00:00.\n\t--help: show this message and quit.\n")

# FUNCION MAC : 
def mac(macAdress):
	try:
		url = "https://gitlab.com/wireshark/wireshark/-/raw/master/manuf"		# url de base de datos de direcciones MAC
		respuesta = requests.get(url)											# se obtiene respuesta de sitio web 
		if (respuesta.status_code==200):										# si hubo respuesta 
			contenido = respuesta.content										# se guarda el contenido 
			file = open("direcciones.txt", "wb")								# se genera unsdsd archivo txt 
			file.write(contenido)												# se escribe el contenido en el archivo
			file.close()
		pass

	#En caso de que no exista conexion 
	#Para ejecutar sin conexion se requiere que el archivo de direcciones se encuentre en la misma carpeta que el archivo.py
	except:	
		print("\n\t404 Not Found.")

	#Se abre el archivo para analizar linea por linea las respectivas direcciones mac.
	finally:
		file = open("direcciones.txt", encoding="utf8")			#Se abre el archivo, UTF-8 es una codificación de caracteres de ancho variable que se utiliza para la comunicación electrónica
		encontrada=False

		while(True):
			linea = file.readline()
			datos = linea.split("\t")			#Se obtienen los datos de la linea, los cuales se encuentran separados por una tabulacion 
			dirMac = linea[0:8]
			macAdress = macAdress.upper()

			if (dirMac==macAdress[0:8]):				
					vendor = datos[1:]						#Datos del fabricante se encuentran desde la posicion 1 en adelante
					print("\n\tMAC address\t:",macAdress)
					print("\tVendor   \t:",vendor[1])
					encontrada=True
					break

			if not linea:			#Si no hay mas lineas 	
				break				#Se rompe el ciclo

		file.close()

		if not encontrada:
			print("\n\tMAC address\t:",macAdress)
			print("\tVendor  \t: Not found\n")

# Funcion IP
# Se utilizo la libreria getmac para encontrar la MAC de la IP ingresada, si existe la IP dentro de la red local, 
# se registra dicha direccion MAC para luego utilizar la función MAC para encontrar a su fabricante.
def ip(dirIp):
	try:
		
		dirMac = get_mac_address(ip = dirIp)
		if not (dirMac == "00:00:00:00:00:00"):
			mac(dirMac.upper())
		else:
			print("\n\t¡Error! ip is outside the host network.\n")

	except:
		print("\n\t¡Error! ip is outside the host network.\n")

def verificarmac(argv):
	lista = ["0","1","2","3","4","5","6","7", "8","9","A","B","C", "D", "E", "F",":","a","b","c", "d", "e", "f"]
	if(len(argv) != 8):
		
		return False
	for i in range(len(argv)):
		if not argv[i] in lista:
			
			return False
	return True
def verificarip(argv):
	
	
	if not "." in argv:
		return False
	arg = argv.split(".")
	for i in range(len(arg)):
		if not (arg[i].isdigit()):
			return False
		if not ((0 <= int(arg[i]))and(int(arg[i]) <= 255)):
			return False
			
	return True
#Esto se utiliza para poder importar este codigo en otro script para utilizar sus funciones.
if __name__ == '__main__':
	main()
    
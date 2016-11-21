from funciones import*

cfg = pickconf("Basic")
titulo = "Bateria Electronica"
msgbox("Bienvenido a la Bateria Eletronica", titulo, "Continuar")

while True:
	opcion = buttonbox("Que desea hacer?", titulo, ["Comenzar a Tocar","Elegir Perfil", "Agregar Nuevo Perfil", "Borrar Perfil", "Salir"])
	if opcion == "Comenzar a Tocar":
		main(cfg)
	elif opcion == "Elegir Perfil":
		botones = searchconf()
		boton = buttonbox("Elija uno", titulo, botones)
		cfg = pickconf(boton)
	elif opcion == "Agregar Nuevo Perfil":
		try:
			nuevoperfil = enterbox("Ingrese el nombre de su nuevo perfil: ", titulo)
			writeconf(nuevoperfil,titulo)
		except:
			pass
	elif opcion == "Borrar Perfil":
		botones = searchconf()
		boton = buttonbox("Elija uno", titulo,botones)
		delconf(boton)
	else:
		sys.exit(0)

import pygame, time
from convertirclass import calculadora


class General():
    """
    Clase base para objetos boton, texto_numeros y texto_general
    Contiene los valores básicos de cualquier objeto
    text --> Corresponde al texto asociado al objeto, también
    es utilizado como valor
    x_pos --> Eje x para dibujo 
    x_pos --> Eje y para dibujo
    font --> Font que utilizará el objeto
    screen --> Objeto screen hererado de la inicialización de pygame
    tx --> Desplazamiento extra sobre x_pos en caso de ser requerido
    ty --> Desplazamiento extra sobre y_pos en caso de ser requerido
    Por default tx, ty se definen en 0
    """
    def __init__(self,text,x_pos,y_pos,font,screen,tx=0,ty=0):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.screen = screen
        self.tx = x_pos + tx
        self.ty = y_pos + ty

class Boton(General):
    """
    Clase boton, representa todo objeto de tipo botón con interacción
    Hereda de clase general y añade:
    enabled --> Si es true permite la operación de check_click
    posee dos métodos expuestos, dibuja y check_click
    """ 
    def __init__(self,text,x_pos,y_pos,font, screen,tx, ty,enabled):
        super().__init__(text,x_pos,y_pos,font, screen,tx,ty)
        self.enabled = enabled

    def dibuja(self):
        """
        Dibuja el objeto en pantalla
        Controla el color en que se despliega
        Si está habilitado
            Si se hace clic sobre el objeto, dibuja dark cyan
            Sino, cyan
        Si está deshabilitado dibuja blue
        """
        Boton_Texto = self.font.render(self.text,True,'Black')
        Boton_recto = pygame.rect.Rect((self.x_pos,self.y_pos),(40,25))
        if self.enabled:
            if self.check_click():
                pygame.draw.rect(self.screen,'dark cyan',Boton_recto,0,5)
            else:
                pygame.draw.rect(self.screen,'cyan',Boton_recto,0,5)
        else:
            pygame.draw.rect(self.screen,'blue',Boton_recto,0,5)
        pygame.draw.rect(self.screen,'blue',Boton_recto,2,5)
        self.screen.blit(Boton_Texto,(self.tx,self.ty))

    def check_click(self):
        """
        Detecta si se hace clic sobre el objeto
        retorna boolean con la suma de clic, si fue sobre el área y
        si está habilitado
        """
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        Boton_recto = pygame.rect.Rect((self.x_pos,self.y_pos),(40,25))
        return (left_click and Boton_recto.collidepoint(mouse_pos) and self.enabled)

class texto_numeros(General):
    """
    Clase texto_numeros, representa los numeros de operandos y resultados
    Hereda de clase general y añade:
    ancho_extra --> Por default en 175, si se asigna puede modificar
    la caja del texto
    Posee un método expuesto, dibuja
    """
    def __init__(self,text,x_pos,y_pos, font, screen, tx, ty, ancho_extra=175):
        super().__init__(text,x_pos,y_pos,font, screen,tx,ty)
        self.ancho_extra=ancho_extra

    def dibuja(self):
        """
        Dibuja el objeto en pantalla
        """
        Boton_Texto = self.font.render(self.text,True,'Black')
        Boton_recto = pygame.rect.Rect((self.x_pos,self.y_pos),(self.ancho_extra,25))
        pygame.draw.rect(self.screen,'white',Boton_recto,0,5)
        pygame.draw.rect(self.screen,'blue',Boton_recto,2,5)
        self.screen.blit(Boton_Texto,(self.tx,self.ty))

class texto_general(General):
    """
    Clase texto_general, representa cualquier texto sin interacción
    Hereda de clase general y añade:
    color --> Color del texto a mostrar
    dibuja --> Dibuja en la pantalla el objeto, reescrita
    """
    def __init__(self,text,x_pos,y_pos,font,screen,color):
        super().__init__(text,x_pos,y_pos,font, screen)
        self.color = color

    def dibuja(self):
        """
        Dibuja el objeto en pantalla
        """
        img = self.font.render(self.text,True,self.color)
        self.screen.blit(img, (self.x_pos,self.y_pos))

class Frontend_Calculadora():
    """
    Clase Frontend_Calculadora reprsenta toda la operación gráfica
    No recibe parámetros
    Todos sus métodos son internos a excepción de 
    ejecuta --> Sin parámetros, retorna True si el usuario solicitó 
    reset del objeto, controla el flujo de ejecución interno
    """
    def __init__(self):
        # Dibuja la pantalla , autoescalada y llenándola
        #flags se intercambia si se compila con buildozer en android
        #flags = pygame.SCALED | pygame.FULLSCREEN 
        flags = pygame.SCALED
        self.screen = pygame.display.set_mode((375, 400), flags)
        #Título de la caja de la calculadora
        pygame.display.set_caption('Calculadora Multi Bases')
        #Frequencia y control de la pantalla
        self.fps = 60
        self.timer = pygame.time.Clock()
        #Tipos de font a utilizar
        self.font = pygame.font.Font("freesansbold.ttf",24)
        self.font_text = pygame.font.Font("freesansbold.ttf",14)
        self.font_num = pygame.font.Font("freesansbold.ttf",18)
        # Diccionario utilizado para controlar el flujo del programa
        self.control_flujo = self.__genera_control_flujo()
        # Invocación método para crear todos los botones y textos
        self.__genera_objetos()

    def __genera_control_flujo(self):
        """
        __genera_control_flujo --> método que retona
        el diccionario de control de flujo del programa
        Primer --> representa si se debe proceder con primer operando
        Segundo --> representa si se debe proceder con segundo operando
        Resultado --> representa si las acciones de resultado deben
        ser ejecutadas
        """
        return {
            "Primer": True,
            "Segundo": False,
            "Resultado": False
        }

    def __crea_botones_hex(self,x,y,status):
        """
        __crea_botones_hex --> Crea botones de bases numéricas
        Recibe parámetros:
        x --> Posición en el eje x
        y --> Posición en el eje y
        status --> Booleano para saber si habilitar o no
        Retorna diccionario con los 4 botones generados
        cada key representa a una base + estado de click
        """
        dict={}
        for elemento in ["Bin","Dec","Hex","Oct"]:
            dict[elemento]=Boton(elemento,x,y,self.font_text,self.screen,4,2,status)
            x+=45
        return dict   
    
    def __crea_botones_numericos(self):
        """
        ___crea_botones_numericos --> Crea todos los botones de números
        no recibe parámetros y retorna lista con todos los botones
        """
        botones = []
        x = 5
        y = 200
        for i in range(1,17,1):
            botones.append(Boton("0123456789ABCDEF"[i-1],x,y,self.font,self.screen,6,2,False))
            #i+=1
            x+=45
            if i%4 == 0 and i>0:
                x=5
                y+=30
        return botones

    def __genera_objetos(self):
        """
        __genera_objetos --> Método utilizado para generar todos
        los objetos que utilizará el front end, incluídos diccionarios
        de objetos
        """
        # Bases Primer Operando
        self.boton_opa_p = self.__crea_botones_hex(5,30,True)
        # Bases Segundo Operando
        self.boton_opa_s = self.__crea_botones_hex(198,30,False)
        # Bases Resultado
        self.boton_opa_r = self.__crea_botones_hex(100,125,False)        
        # Botones numéricos
        self.botones_numericos = self.__crea_botones_numericos()
        # Botones Operaciones matemáticas
        self.boton_opers={}
        self.boton_opers["+"] = Boton('+',200,200,self.font,self.screen,12,2,False)
        self.boton_opers["-"] = Boton('-',200,230,self.font,self.screen,12,2,False)
        self.boton_opers["*"] = Boton('*',200,260,self.font,self.screen,12,2,False)
        self.boton_opers["/"] = Boton('/',200,290,self.font,self.screen,12,2,False)
        # Boton negativo
        self.boton_neg = Boton('Neg',300,290,self.font_text,self.screen,6,2,False)
        # Boton punto
        self.boton_punto = Boton('.',250,260,self.font,self.screen,14,2,False)
        # Boton ClS
        self.boton_clear = Boton('CLS',250,230,self.font_text,self.screen,8,2,False)        
        # Boton Reset    
        self.boton_reset = Boton('Rest',250,200,self.font_text,self.screen,3,2,True)
        # Boton Igual
        self.boton_igual = Boton('=',250,290,self.font,self.screen,14,2,False)
        # Boton salir
        self.boton_exit = Boton('Salir',330,350,self.font_text,self.screen,4,2,True)
        # Define Textos estáticos
        self.texto_primer_operando = texto_general("Primer Operando", 5, 10, self.font_text,self.screen, "black")
        self.texto_segundo_operando = texto_general("Segundo Operando", 198, 10, self.font_text,self.screen,"black")
        self.texto_resultado_operando = texto_general("Resultado", 150, 110, self.font_text,self.screen, "black")
        # Define textos dinámicos
        self.texto_accion = texto_general("Clic en base del primer operando", 10, 350, self.font_text,self.screen, "red")
        self.resultado = texto_numeros("",70,155,self.font_num,self.screen,6,2,250)
        # Textos utilizados para alimentar a la clase convertirclass
        self.baseoperando_a = texto_general("", 10, 85,self.font_num,self.screen, "blue")
        self.operando_a = texto_numeros("",5,60,self.font_num,self.screen,6,2)
        self.baseoperando_b = texto_general("", 205, 85,self.font_num,self.screen, "blue")
        self.operando_b = texto_numeros("",198,60,self.font_num,self.screen,6,2)
        self.operacion = texto_general("", 185, 60,self.font_num,self.screen, "red")
        self.base_resultado=texto_general("", 40, 160, self.font_text,self.screen, "blue")
    
    def __Revisa_si_hay_un_boton_presionado(self,botones):
        """
        ___Revisa_si_hay_un_boton_presionado --> Método que
        recibe un diccionario de botones de bases numéricas
        Retorna otro diccionario con dos valores
        Status --> False por default
        Si un botón tuvo clic, cambia Status a True,
        además de generar key "Base" con el texto del botón
        base seleccionado
        """
        Diccionario_respuesta= {
        "Status": False
        }
        for boton in botones:
            if botones[boton].check_click():
                Diccionario_respuesta["Status"]=True
                Diccionario_respuesta["Base"]=botones[boton].text
                break
        return Diccionario_respuesta
    
    def __cambia_estado_botones_numericos(self,base):
        """
        __cambia_estado_botones_numericos --> El proceso
        recorre la lista de botones numéricos y cambia
        estado enabled según condición con parámetro
        base --> que puede tomar los valores
        "Habilitar" --> Todos los botones a True
        "Deshabilitar" --> Todos los botones a False
        "Bin" --> Los botones no binarios a False
        "Oct" --> Los botones no octales a False
        "Dec" --> Los botones no decimales a False
        "Hex" --> Define todos los botones en True
        """
        for index,boton in enumerate(self.botones_numericos):
            if base == "Habilitar" or "Hex":
                boton.enabled=True
            if base == "Deshabilitar":
                boton.enabled=False
            if base == "Bin" and index > 1:
                boton.enabled=False
            if base == "Oct" and index > 7:
                boton.enabled=False
            if base == "Dec" and index > 9:
                boton.enabled=False
    
    def __cambia_estado_boton_bases_calculo(self,botones):
        """
        __cambia_estado_boton_bases_calculo -> Recibe
        botones --> Diccionario de bases numéricas
        El proceso cambia el estado enabled al valor 
        que tenga el método check_click de cada objeto
        """
        for boton in botones.values():
            boton.enabled=boton.check_click()

    def __cambia_punto_y_negativo(self,status):
        """
        ___cambia_punto_y_negativo --> Cambia la
        propiedad enabled de los botones punto y negativo
        al status recibido
        """
        self.boton_punto.enabled = status
        self.boton_neg.enabled = status
   
    def __cambia_base_y_estado_botones(self,boton_opa,base,status):
        """
        __cambia_base_y_estado_botones --> Este método recibe
        boton_opa --> Diccionario con botones bases numéricas
        base --> Base numérica anteriormente seleccionada
        status --> Orden de habilitar o deshabilitar botones
        Primero cambia el estado del boton punto, cls y neg
        Segundo, solicita deshabilitar botones numericos
        qe no pertenecen a la base recibida
        Tercero, solo si se estan procesando operandos
        solicita cambiar el estado enabled al diccionario de bases
        """
        self.__cambia_punto_y_negativo(status)
        self.boton_clear.enabled = status
        self.__cambia_estado_botones_numericos(base)
        if not self.control_flujo.get("Resultado"):
            self.__cambia_estado_boton_bases_calculo(boton_opa)

    def __revisa_bases_operandos(self):
        """
        __revisa_bases_operandos --> Este método funciona
        solo si las bases numéricas de los operandos no han
        sido seleccionadas.
        De acuerdo a control_flujo opera sobre primer o segundo
        operando
        En cada uno invoca a método __Revisa_si_hay_un_boton_presionado
        Retonar salida sobre diccionario condición
        Si el key "Status" es True  
        Asigna el valor contenido en key "Base" al texto de la base 
        operando a.
        Cambia el texto de acción para que el usuario sepa
        que puede digitar el número 
        Invoca a método __cambia_base_y_estado_botones 
        con el diccionario asociado a las bases de dicho operando
        Nota: El método check_clic de dicho diccionario aún
        mantiene el estado de clic en True para la base
        seleccionada al invocar al método
        """
        if self.control_flujo.get("Primer"):
            condicion = self.__Revisa_si_hay_un_boton_presionado(self.boton_opa_p)
            if condicion["Status"]:
                self.baseoperando_a.text=condicion["Base"]                
                self.texto_accion.text="Ingrese primer operando y clic en '+ - * o /'"
                self.__cambia_base_y_estado_botones(self.boton_opa_p,self.baseoperando_a.text,True)
    
        if self.control_flujo.get("Segundo"):
            condicion = self.__Revisa_si_hay_un_boton_presionado(self.boton_opa_s)
            if condicion["Status"]:
                self.baseoperando_b.text=condicion["Base"]                
                self.texto_accion.text="Ingrese segundo operando y clic igual"
                self.__cambia_base_y_estado_botones(self.boton_opa_s,self.baseoperando_b.text,True)
    
    def __crea_pool_de_objetos(self):
        """
        __crea_pool_de_objetos --> Genera una lista con todos
        los objetos ya creados
        retorna la lista con el fin de reducir la operación de dibujo
        """
        pool_objetos=[]
        pool_objetos.extend(self.boton_opa_p.values())
        pool_objetos.extend(self.boton_opa_s.values())        
        pool_objetos.extend(self.boton_opa_r.values())        
        pool_objetos.extend(self.botones_numericos)
        pool_objetos.extend(self.boton_opers.values())
        pool_objetos.append(self.boton_neg)
        pool_objetos.append(self.boton_punto)
        pool_objetos.append(self.boton_clear)
        pool_objetos.append(self.boton_reset)
        pool_objetos.append(self.boton_igual)
        pool_objetos.append(self.texto_primer_operando)
        pool_objetos.append(self.texto_segundo_operando)
        pool_objetos.append(self.texto_resultado_operando)
        pool_objetos.append(self.base_resultado)
        pool_objetos.append(self.texto_accion)
        pool_objetos.append(self.baseoperando_a)
        pool_objetos.append(self.baseoperando_b)
        pool_objetos.append(self.operando_a)
        pool_objetos.append(self.operando_b)
        pool_objetos.append(self.resultado)
        pool_objetos.append(self.operacion)
        pool_objetos.append(self.boton_exit)
        return pool_objetos

    def __dibuja_pantalla(self):
        """
        __dibuja_pantalla --> método que invoca el método dibuja
        de cada objeto y de esta forma crea el 100% de la pantalla
        """
        # Limpia la pantalla
        self.screen.fill('white')    
        self.timer.tick(self.fps)
        for boton in self.__crea_pool_de_objetos():
            boton.dibuja()

    def __revisa_boton_negativo(self):
        """
        __revisa_boton_negativo --> No recibe parametros
        Si se hace click en boton negativo
        Cambia la propiedad enabled del botón a False
        Si el key control_flujo es "Primer" define
        operando_a en "-"
        Si el key control_flujo es "Segundo" define 
        operando_b en "-"
        """
        if self.boton_neg.check_click():
            self.boton_neg.enabled = False
            if self.control_flujo.get("Primer"):
                self.operando_a.text="-"
            if self.control_flujo.get("Segundo"):
                self.operando_b.text="-"

    def __no_todo_el_conjunto_botones_base_activos(self,botones_base):
        """
        ___no_todo_el_conjunto_botones_base_activos --> método que
        revisa un diccionario de botones de bases numéricas
        Retorna True si al menos un botón de base está deshabilitado
        False, si todos están habilitados
        """
        for boton in botones_base.values():
            if not boton.enabled:
                return True
        return False   
    
    def __cambia_estado_botones_matematicos(self,status):
        """
        __cambia_estado_botones_matematicos --> revisa
        el los valores del diccionario de botones matemáticos
        Recibe como parámetro status booleano
        Asigna status en la propiedad enabled de cada
        boton
        """
        for boton in self.boton_opers.values():
            boton.enabled=status

    def __revisa_botones_numericos(self,resultado):
        """
        __revisa_botones_numericos --> Revisa la lista de botones
        numéricos
        Recibe resultado --> texto del operando
        Si se hizo clic en alguno o el resultado no supera 12
        caracteres, añade el texto del objeto boton al resultado
        Cambia el estado enable del boton negativo a False
        retorna la variable resultado operada
        """
        for boton in self.botones_numericos:
            if boton.enabled and boton.check_click() and len(resultado)<12:
                resultado+=boton.text
                self.boton_neg.enabled=False
        return resultado

    def __escribe_operandos(self):
        """
        __escribe_operandos --> No recibe parámetros
        Para el diccionario control_flujo, keys, "Primer" y "Segundo" (ambos)
        y solo si no todas las bases numéricas están activas
        asigna en el operando el resultado del método
        __revisa_botones_numéricos, entregandole como parámetro al operando
        Luego, solo si el key es "Primer"
        Habilita todos los botones matemáticos
        Solo si el key es "Segundo2"
        Habilita el boton igual
        Siempre invoca la revisión del botón punto
        a través del método __revisa_boton_punto
        """
        if self.control_flujo.get("Primer") and self.__no_todo_el_conjunto_botones_base_activos(self.boton_opa_p):
            self.operando_a.text=self.__revisa_botones_numericos(self.operando_a.text)
            self.__cambia_estado_botones_matematicos(True)
        if self.control_flujo.get("Segundo")and self.__no_todo_el_conjunto_botones_base_activos(self.boton_opa_s):
            self.operando_b.text=self.__revisa_botones_numericos(self.operando_b.text)
            self.boton_igual.enabled=True
    
    def __revisa_boton_punto(self):
        """
        __revisa_boton_punto --> revisa si se hizo click
        sobre el botón punto
        Si los key "Primer" o "Segundo" del control de flujo
        están en True y el largo del operando no excede 12
        Agrega un punto al operando
        Deshabilita los botones punto y negativo
        """
        if self.boton_punto.check_click():
            if self.control_flujo.get("Primer") and len(self.operando_a.text)<12:
               self.operando_a.text+="."
               self.__cambia_punto_y_negativo(False)
            if self.control_flujo.get("Segundo") and len(self.operando_b.text)<12:
               self.operando_b.text+="."
               self.__cambia_punto_y_negativo(False)

    def __revisa_no_cero(self,operando):
        """
        __revisa_no_cero --> recibe un operando
        Cambia el texto de acción a "Error" y retorna False 
        en dos condiciones:
        A.- Si el largo del operando es 0 o solo contiene un "."
        B.- Si el operando es numérico (no contiene letras)
        Valida si el valor float del operando es 0 y
        el contenido de la operación es división
        (si se invoca con el primer operando el valor viene
        en blanco)
        Si ninguna de estas condiciones se cumple retorna True
        """
        if len(operando)==0 or operando==".":
            self.texto_accion.text="Error"
            return False
        try:
            if float(operando)==0 and self.operacion.text=="/":
                self.texto_accion.text="Error"
                return False
        except:
            pass
        return True
    
    def __corrige_operando(self,operando):
        """
        __corrige_operando --> Recibe operando como parámetro
        Si el operando viene vacío le asigna 0
        Si el último caracter del operando es "." se lo quita
        Si el primer caracter del operando es "." añade
        un 0 adelante
        Intenta Si el float del operando es 0 le asigna "0"
        Si falla ignora
        retorna el operando corregido
        """
        if len(operando) == 0:
            operando="0"
        if operando[-1] == ".":
            operando=operando[:-1]
        if operando[0] == ".":
            operando="0"+operando
        try:
            if float(operando) == 0:
                operando="0"
        except:
            pass
        return operando

    def __revisa_botones_operaciones_matematicas(self):
        """
        __revisa_botones_operaciones_matematicas --> 
        No recibe parametros
        Invoca a __Revisa_si_hay_un_boton_presionado enviado
        como parámetro el diccionario de bases numéricas 
        Almacena resultado en diccionario condición
        Si el key "Status" es True (había un boton cliqueado)
        Almacena el botón presionado en la propiedad text de la operación
        Corrige el contenido del operando_a
        Deshabilita botones punto, negativo y botones_matemáticos
        Habilita todos los botones numéricos
        Cambia las key de control de flujo para continuar con segundo operador
        Cambia el texto de acción a seleccionar base segundo operando
        Deshabilita los botones de bases numéricas del primer operando
        Habilita los botones de bases numéricas del segundo operando
        Deshabilita todos los botones numéricos
        """
        condicion = self.__Revisa_si_hay_un_boton_presionado(self.boton_opers)
        if condicion["Status"]:
            if self.__revisa_no_cero(self.operando_a.text):
                #Almacena el botón presionado en la propiedad text de la operación
                self.operacion.text=condicion["Base"]
                #Corrige el contenido del operando_a
                self.operando_a.text=self.__corrige_operando(self.operando_a.text)
                #Deshabilita botones punto, negativo y botones_matemáticos
                self.__cambia_punto_y_negativo(False)
                self.__cambia_estado_botones_matematicos(False)
                #Habilita todos los botones numéricos
                self.__cambia_estado_botones_numericos("Habilitar")
                #Cambia las key de control de flujo para continuar con segundo operador
                self.control_flujo["Primer"]=False
                self.control_flujo["Segundo"]=True
                #Cambia el texto de acción a seleccionar base segundo operando
                self.texto_accion.text="Clic en base del segundo operando"
                #Deshabilita los botones de bases numéricas del primer operando
                self.__cambia_estado_boton_bases_calculo(self.boton_opa_p)
                #Habilita bases numéricas de segundo operando
                self.__habilita_bases_numericas(self.boton_opa_s)
                #Deshabilita todos los botones numéricos
                self.__cambia_estado_botones_numericos("Deshabilitar")
                
    def __deshabilita_algunos_botones(self):
        """
        __deshabilita_algunos_botones --> No recibe parametros
        Define propiedades en enabled en False de
        boton igual, clear, punto, negativo y todos los botones
        matemáticos
        """
        self.boton_igual.enabled=False
        self.boton_clear.enabled=False
        self.__cambia_punto_y_negativo(False)
        self.__cambia_estado_botones_matematicos(False)

    def __revisa_boton_igual(self):
        """
        __revisa_boton_igual --> No recibe parametros
        Si hubo click en boton igual
        Si __revisa_no_cero de operando_b propiedad text es True
        Deshabilita algunos botones
        Habilita las bases numéricas del resultado
        Deshabilita el boton base numérica del segundo operando
        Cambia diccionario control_flujo, solo key "Resultado" es True
        Cambia texto de acción para indicar al usuario que presione base
        resultado
        Corrige el formato del segundo operando 
        """
        if self.boton_igual.check_click():
            if self.__revisa_no_cero(self.operando_b.text):
                self.__deshabilita_algunos_botones()
                self.__habilita_bases_numericas(self.boton_opa_r)
                self.boton_opa_s[self.baseoperando_b.text].enabled=False
                self.control_flujo["Primer"]=False
                self.control_flujo["Segundo"]=False
                self.control_flujo["Resultado"]=True
                self.texto_accion.text="Clic en base resultado"
                self.operando_b.text=self.__corrige_operando(self.operando_b.text)

    def __habilita_bases_numericas(self,base_opa):
        """
        __habilita_bases_numericas --> Recibe diccionario
        de bases numericas de operandos
        Para todos los botones define la propiedad enabled en True
        """
        for boton in base_opa.values():
            boton.enabled=True

    def __revisa_boton_clear(self):
        """
        __revisa_boton_clear --> No recibe parámetros
        Si se hizo click en boton clear
        Para las key "Primer" o "Segundo" en True
        Deja en blanco las propiedades text de baseoperando y
        operando respectivos
        Habilita las bases_numericas respectivas
        Solo si el key "Resultado" es False
        Habilita todos los botones numéricos
        Deshabilita los botones de operación que no deben ser operados
        antes de seleccionar la base numérica
        """
        if self.boton_clear.check_click():
            if self.control_flujo.get("Primer"):
               self.baseoperando_a.text=""
               self.operando_a.text=""
               self.texto_accion.text="Seleccione base del primer operando"
               self.__habilita_bases_numericas(self.boton_opa_p)
            if self.control_flujo.get("Segundo"):
               self.baseoperando_b.text=""
               self.operando_b.text=""
               self.texto_accion.text="Seleccione base del segundo operando"
               self.__habilita_bases_numericas(self.boton_opa_s)
            if not self.control_flujo.get("Resultado"):
                self.__cambia_estado_botones_numericos("Habilitar")
                self.__deshabilita_algunos_botones()

    def __asigna_resultado(self):
        """
        __asigna_resultado --> No recibe parámetros
        Genera objeto calculo de clase Calculadora
        en base a los parámetros recolectados
        Almacena resultado en variable resultado
        Borra objeto calculo
        retorna el resultado
        """
        calculo=calculadora(self.baseoperando_a.text,self.operando_a.text,self.operacion.text,self.baseoperando_b.text,self.operando_b.text,self.base_resultado.text)
        resultado = calculo.resultado
        del calculo
        return resultado

    def __revisa_si_procesar_resultado(self):
        """
        __revisa_si_procesar_resultado --> No recibe parametros
        Si el key de control flujo es "Resultado"
        Deshabilita todos los botones numéricos y otros de operación
        Invoca __revisa_si_hay_un_boton_presionado enviando como
        parametro el diccionario de bases numericas de resultado
        Si el key "Status" es True
        Captura desde el key "Base", la base numérica seleccionada 
        y la deja en la propiedad base_resultado.text
        Invoca a __asigna_resultado retornando en propiedad
        resultado.text el número calculado
        Si el largo excede 22 modifica resultado en base a
        Si hay decimal
        A.- Si hay un punto en 22 caracteres y no es el último
        trunca a 22 caracteres
        B.- Caso contrario almacena error en la propiedad text 
        de resultado
        Si no hay decimal
        Si el largo excede 25 , almacena error en la propiedad 
        text de resultado
        """
        if self.control_flujo.get("Resultado"):
            self.__cambia_base_y_estado_botones("","Deshabilitar",False)
            condicion=self.__Revisa_si_hay_un_boton_presionado(self.boton_opa_r)
            if condicion["Status"]:
                self.base_resultado.text=condicion["Base"]
                self.resultado.text= self.__asigna_resultado()
                if len(self.resultado.text)>22:
                    if "." in self.resultado.text:
                        if "." in self.resultado.text[:22] and self.resultado.text[:22][-1]!=".":
                            self.resultado.text=self.resultado.text[:22]
                        else:
                            self.resultado.text="ERROR"
                    else:
                        if len(self.resultado.text)>25:
                            self.resultado.text="ERROR"

    def ejecuta(self):
        """
        ejecuta --> método que ejecuta los otros métodos
        en orden para el flujo del objeto FrontEnd_Calculadora
        Retorna un diccionario con 2 key
        "Reconstruir" --> Estado de click en botón reset
        "Salir" --> Estado de click en botón salir
        """
        self.__dibuja_pantalla()
        self.__revisa_boton_negativo()
        self.__revisa_bases_operandos()
        self.__escribe_operandos()
        self.__revisa_boton_punto()
        self.__revisa_botones_operaciones_matematicas()
        self.__revisa_boton_igual()
        self.__revisa_boton_clear()
        self.__revisa_si_procesar_resultado()
        return {"Reconstruir": self.boton_reset.check_click(), "Salir": self.boton_exit.check_click()}

# Programa Principal

# Inicia Pygame
pygame.init()

# Dibuja la pantalla y crea objeto del Front End
Front_Calculadora = Frontend_Calculadora()

# Variable que controla si se itera o no
run = True

while run:
    #Diccionario de respuestas invoca a método ejecuta
    Respuestas = Front_Calculadora.ejecuta()

    #Si key "Reconstruir" es True,
    # ReDibuja la pantalla y Recrea objeto del Front End
    if Respuestas["Reconstruir"]:
        Front_Calculadora = Frontend_Calculadora()

    #Si el key "Salir" es True cambia bool run a False
    if Respuestas["Salir"]:
        run = False
    
    #Si se hace clic en X , run se cambia a False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           run = False
    
    pygame.display.flip()
    time.sleep(0.16)
   

pygame.quit()
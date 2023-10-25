from decimal import Decimal

class calculadora():
    hex="0123456789ABCDEF"
    bases = {
        "Hex" : 16,
        "Bin" : 2,
        "Oct" : 8,
    }
    limite = 14

    def __init__(self,base_operando_a,operando_a,operacion,base_operando_b,operando_b,base_resultado):
        self.baseoperando_a= base_operando_a
        self.baseoperando_b= base_operando_b
        self.base_resultado = base_resultado
        self.operando_a = operando_a
        self.operando_b = operando_b
        self.operacion = operacion

    def __dec_a_base(self,base,numero):

        entero = numero // base
        if base == 16:
            strresto = self.hex[int(numero % base)]
        else:
            strresto = str(numero % base)
        if entero != 0:
            return str(self.__dec_a_base(base,entero))+strresto
        return strresto

    def __base_a_dec(self,base,string):
        sum=0
    
        if "." in string:
            separa = string.split(".")
            entero = separa[0]
            decimal = separa[1]
        else:
            entero = string

        ## proceso entero
        for index, letter in enumerate(entero[::-1]):
            sum += self.hex.index(letter) * (base**index)

        ## proceso decimal
        if "." in string:
            acumdec=0
            for index, letter in enumerate(decimal):
                acumdec += self.hex.index(letter) * (base**((index + 1)*-1))

            sum += acumdec

        return sum

    def __convertir(self,base,numero,funcion):
        if base != "Dec":
            return funcion(self.bases.get(base),numero)
        else:
            return float(numero)
        
    def __fix_operandos_negativos(self):
        operandos={
            "a":False,
            "b":False
        }
        if self.operando_a[0]=="-" and self.baseoperando_a != "Dec":
            self.operando_a=self.operando_a[1:]
            operandos["a"]=True
        if self.operando_b[0]=="-" and self.baseoperando_b != "Dec":
            self.operando_b=self.operando_b[1:]
            operandos["b"]=True
        
        return operandos
    
    def __fix_decimal(self,numero):
        if numero > 0 and numero < 1:
            return Decimal(str(numero))
        return numero
        
    def __operar(self):
        # Fix para manejo de negativo
        operandos=self.__fix_operandos_negativos()
        
        a = self.__convertir(self.baseoperando_a,self.operando_a,self.__base_a_dec)
        b = self.__convertir(self.baseoperando_b,self.operando_b,self.__base_a_dec)

        if operandos["a"]:
            a=a*-1
        if operandos["b"]:
            b=b*-1

        a = self.__fix_decimal(a)    
        b = self.__fix_decimal(b)
        
        if self.operacion == "/":
            return a/b
        if self.operacion == "*":
           return a*b
        if self.operacion == "-":
           return a-b
    
        return a+b

    def __fraccion_a_base(self,fraction,limite,base,maximo):
        entero = int(fraction*base)
        resto = (fraction*base) - entero

        if base == 16:
            fraccion = self.hex[entero]
        else:
            fraccion = str(entero)

        if resto!=0 and self.limite != 0 and maximo>0:
            return fraccion+self.__fraccion_a_base(resto,limite - 1,base,maximo-1)

        return fraccion
  

    @property
    def resultado(self):
        intermedio = self.__operar()
        resultado = str(intermedio)

        if self.base_resultado != "Dec":
            # Corrige resultado negativo
            negativo = False
            if intermedio<0:
                negativo=True
                intermedio=intermedio*-1
            # Fin Fix negativo
            resultado = str(self.__convertir(self.base_resultado,int(intermedio),self.__dec_a_base))
            dife = intermedio - int(intermedio)
            if dife >0:
                resultado += "." + self.__fraccion_a_base(dife,self.limite,self.bases.get(self.base_resultado),200)
            if negativo:
                resultado= "-"+resultado
        else:
            if len(resultado)>2:
                if resultado[len(resultado)-2:]==".0":
                    resultado=resultado[:-2]

        return resultado


#calculo=calculadora("Dec","0.24","+","Dec","0.22","Bin")
#print(calculo.resultado)






    

    
    
    



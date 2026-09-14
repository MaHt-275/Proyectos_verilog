import cocotb
import random
from cocotb.triggers import Timer
#iniciar test
@cocotb.test() #Decorador para indicar que es un test
async def test_alu_top(dut):
    """Test Para el modulo ALU Top"""#comentario de la funcion visible para Cocotb
    await Timer(50, unit='ns')
    for i in range(200):
        a=random.randint(0, 255)
        # ==========================================
        #          Testeo del desplazador
        # ==========================================
        cocotb.log.info("Testeo del desplazador")
        await Timer(50, unit='ns')
        n=0
        # ==========================================
        #      caso 1: Desplazamiento a la izquierda
        # ==========================================
        cocotb.log.info("Caso 1: Desplazamiento a la izquierda")
        while n <= 7:
            E_a = (a << n) & 0xFF
            carry_esperado = (a >> (8 - n)) & 1 if n != 0 else 0
            zero_esperado = 1 if E_a == 0 else 0
            negative_esperado = (E_a >> 7) & 1
            dut.in_a.value = a
            dut.shift_amount.value = n
            dut.SHIFT_IZ_DER.value = 0
            dut.SHIFT_ARIT_RIGHT.value = 0
            dut.select.value = 0b00

            await Timer(50, unit='ns')

            cocotb.log.info(f"Desplazamiento a la izquierda {n} veces")
            assert dut.out.value == E_a, f"Error en desplazamiento izq {n}: esperado {E_a}, dio {dut.out.value}"
            assert dut.zero_flag.value == zero_esperado, f"Error en zero izq {n}: esperado {zero_esperado}, dio {dut.zero_flag.value}"
            assert dut.carry_out.value == carry_esperado, f"Error en carry izq {n}: esperado {carry_esperado}, dio {dut.carry_out.value}"
            assert dut.negative_flag.value == negative_esperado, f"Error en negative izq {n}: esperado {negative_esperado}, dio {dut.negative_flag.value}"
            n = n + 1
        # ==========================================
        #      caso 2: Desplazamiento a la derecha logico
        # ==========================================
        cocotb.log.info("Caso 2: Desplazamiento a la derecha logico")
        n = 0
        while n <= 7:
            E_a = (a >> n) & 0xFF
            carry_esperado = (a >> (n - 1)) & 1 if n != 0 else 0
            zero_esperado = 1 if E_a == 0 else 0
            negative_esperado = (E_a >> 7) & 1
            dut.in_a.value = a
            dut.shift_amount.value = n
            dut.SHIFT_IZ_DER.value = 1
            dut.SHIFT_ARIT_RIGHT.value = 0
            dut.select.value = 0b00

            await Timer(50, unit='ns')

            cocotb.log.info(f"Desplazamiento a la derecha {n} veces")
            assert dut.out.value == E_a, f"Error en desplazamiento der {n}: esperado {E_a}, dio {dut.out.value}"
            assert dut.carry_out.value == carry_esperado, f"Error en carry der {n}: esperado {carry_esperado}, dio {dut.carry_out.value}"
            assert dut.zero_flag.value == zero_esperado, f"Error en zero der {n}: esperado {zero_esperado}, dio {dut.zero_flag.value}"
            assert dut.negative_flag.value == negative_esperado, f"Error en negative der {n}: esperado {negative_esperado}, dio {dut.negative_flag.value}"
            n = n + 1
        # ==========================================
        #      caso 3: Desplazamiento a la derecha aritmetico
        # ==========================================
        cocotb.log.info("Caso 3: Desplazamiento a la derecha aritmetico")
        a_arith = a - 256 if a > 127 else a
        n=0
        while n <= 7:
            E_a = (a_arith >> n) & 0xFF
            carry_esperado = (a >> (n - 1)) & 1 if n != 0 else 0
            zero_esperado = 1 if E_a == 0 else 0
            negative_esperado = 1 if (E_a>>7) & 1 == 1 else 0
            dut.in_a.value = a
            dut.shift_amount.value = n
            dut.SHIFT_IZ_DER.value = 1
            dut.SHIFT_ARIT_RIGHT.value = 1
            dut.select.value = 0b00

            await Timer(50, unit='ns')

            cocotb.log.info(f"Desplazamiento a la derecha aritmetico {n} veces")
            assert dut.out.value == E_a, f"Error en desplazamiento aritmetico der {n}: esperado {E_a}, dio {dut.out.value}"
            assert dut.carry_out.value == carry_esperado, f"Error en carry aritmetico der {n}: esperado {carry_esperado}, dio {dut.carry_out.value}"
            assert dut.zero_flag.value == zero_esperado, f"Error en zero aritmetico der {n}: esperado {zero_esperado}, dio {dut.zero_flag.value}"
            assert dut.negative_flag.value == negative_esperado, f"Error en negative aritmetico der {n}: esperado {negative_esperado}, dio {dut.negative_flag.value}"
            n = n + 1

    for i in range(200):
        # ==========================================
        #          Testeo del aritmético
        # ==========================================
        # ==========================================
        # CASO 1: Suma aleatoria con CarryIn = 0
        #==========================================
        cocotb.log.info("Caso 1 inicio: Suma aleatoria con Carry In = 0")
        a=random.randint(0, 255) #entrada A aleatoria
        b=random.randint(0, 255) #entrada B aleatoria
        c_in=0 #Carry In en 0
        cocotb.log.info(f"[CASO 1] Operación: {a} + {b} + {c_in} (Mod_sub = 0)")
        dut.in_a.value=a #asignar valor a la entrada A
        dut.in_b.value=b #asignar valor a la entrada B
        dut.carry_in.value=c_in #asignar valor a la entrada Carry_In
        dut.mod_sub.value=0 #asignar valor a la entrada mod_sub
        dut.select.value=0b01 #seleccionamos la operacion aritmetica
        await Timer(10, unit='ns') #esperar 10 ns para que se propague la señal
        #Verificar la salida de la suma
        #calculamos la suma real
        suma_real=(a+b+c_in) & 0xFF #truncar a 8bits
        a_s = a - 256 if a > 127 else a
        b_s = b - 256 if b > 127 else b
        R_carry=0 if (a+b+c_in) <= 255 else 1 #calcular el carry real
        R_overflow=1 if (a_s+b_s+c_in) < -128 or (a_s+b_s+c_in) > 127 else 0
        R_zero=1 if suma_real == 0 else 0
        R_negative=1 if (suma_real >> 7) & 1 == 1 else 0
        #Verificamos que la salida del DUT sea igual a la suma real
        cocotb.log.info(f"  -> [Esperado] Suma: {suma_real}, Carry: {R_carry}, Overflow: {R_overflow}, Zero: {R_zero}, Negative: {R_negative} \n [Obtenido DUT] Suma: {dut.out.value}, Carry: {dut.carry_out.value}, Overflow: {dut.overflow_flag.value}, Zero: {dut.zero_flag.value}, Negative: {dut.negative_flag.value}")
        assert dut.out.value == suma_real, f"Error en la suma: {a} + {b} + {c_in} = {suma_real}, pero dio {dut.out.value}"
        assert dut.overflow_flag.value == R_overflow, f"Error en el Overflow Out, el esperado es {R_overflow}, pero dio {dut.overflow_flag.value}"
        assert dut.carry_out.value == R_carry, f"Error en el Carry Out, el esperado es {R_carry}, pero dio {dut.carry_out.value}"
        assert dut.zero_flag.value == R_zero, f"Error en el Zero Flag, el esperado es {R_zero}, pero dio {dut.zero_flag.value}"
        assert dut.negative_flag.value == R_negative, f"Error en el Negative Flag, el esperado es {R_negative}, pero dio {dut.negative_flag.value}"
        await Timer(50, unit='ns') 
        # ==========================================
        # CASO 2: Suma aleatoria con Carry In = 0
        # ==========================================
        cocotb.log.info("Caso 2 inicio: Suma aleatoria con Carry In = 1")
        a=random.randint(0, 255) #entrada A aleatoria
        b=random.randint(0, 255) #entrada B aleatoria
        c_in=1 #Carry In en 1
        cocotb.log.info(f"[CASO 2] Operación: {a} + {b} + {c_in} (Mod_sub = 0)")
        dut.in_a.value=a 
        dut.in_b.value=b 
        dut.carry_in.value=c_in 
        dut.mod_sub.value=0
        dut.select.value=0b01 
        await Timer(10, unit='ns')
        suma_real=(a+b+c_in) & 0xFF
        a_s = a - 256 if a > 127 else a
        b_s = b - 256 if b > 127 else b
        R_carry=0 if (a+b+c_in) <= 255 else 1
        R_overflow=1 if (a_s+b_s+c_in) < -128 or (a_s+b_s+c_in) > 127 else 0
        R_zero=1 if suma_real == 0 else 0
        R_negative=1 if (suma_real >> 7) & 1 == 1 else 0
        cocotb.log.info(f"  -> [Esperado] Suma: {suma_real}, Carry: {R_carry}, Overflow: {R_overflow}, Zero: {R_zero}, Negative: {R_negative} \n [Obtenido DUT] Suma: {dut.out.value}, Carry: {dut.carry_out.value}, Overflow: {dut.overflow_flag.value}, Zero: {dut.zero_flag.value}, Negative: {dut.negative_flag.value}")
        assert dut.out.value == suma_real, f"Error en la suma: {a} + {b} + {c_in} = {suma_real}, pero dio {dut.out.value}"
        assert dut.overflow_flag.value == R_overflow, f"Error en el Overflow Out, el esperado es {R_overflow}, pero dio {dut.overflow_flag.value}"
        assert dut.carry_out.value == R_carry, f"Error en el Carry Out, el esperado es {R_carry}, pero dio {dut.carry_out.value}"
        assert dut.zero_flag.value == R_zero, f"Error en el Zero Flag, el esperado es {R_zero}, pero dio {dut.zero_flag.value}"
        assert dut.negative_flag.value == R_negative, f"Error en el Negative Flag, el esperado es {R_negative}, pero dio {dut.negative_flag.value}"
        await Timer(50, unit='ns')
        # ==========================================
        # CASO 3: resta aleatoria con Carry In = 1
        # ==========================================
        cocotb.log.info("Caso 3 inicio: Resta aleatoria con Carry In = 1")
        a=random.randint(-128, 127) #cambio los limites al ser un bit de signo
        b=random.randint(-128, 127) 
        c_in=1
        cocotb.log.info(f"[CASO 3] Operación: {a} - {b} (Mod_sub = 1)")
        dut.in_a.value=a 
        dut.in_b.value=b 
        dut.carry_in.value=c_in 
        dut.mod_sub.value=1
        dut.select.value=0b01
        await Timer(10, unit='ns') 
        resta_real=(a-b) & 0xFF
        R_overflow=1 if (a-b) < -128 or (a-b) > 127 else 0
        Ac=a&0xFF
        Bc=b&0xFF
        R_carry=1 if Ac >= Bc else 0
        R_zero=1 if resta_real == 0 else 0
        R_negative=1 if (resta_real >> 7) & 1 == 1 else 0
        cocotb.log.info(f"  -> [Esperado] Resta: {resta_real}, Carry: {R_carry}, Overflow: {R_overflow}, Zero: {R_zero}, Negative: {R_negative} \n [Obtenido DUT] Resta: {dut.out.value}, Carry: {dut.carry_out.value}, Overflow: {dut.overflow_flag.value}, Zero: {dut.zero_flag.value}, Negative: {dut.negative_flag.value}")
        assert dut.out.value == resta_real, f"Error en la resta: {a} - {b} = {resta_real}, pero dio {dut.out.value}"
        assert dut.carry_out.value == R_carry, f"Error en el Carry Out, el esperado es {R_carry}, pero dio {dut.carry_out.value}"
        assert dut.overflow_flag.value == R_overflow, f"Error en el Overflow Out, el esperado es {R_overflow}, pero dio {dut.overflow_flag.value}"
        assert dut.zero_flag.value == R_zero, f"Error en el Zero Flag, el esperado es {R_zero}, pero dio {dut.zero_flag.value}"
        assert dut.negative_flag.value == R_negative, f"Error en el Negative Flag, el esperado es {R_negative}, pero dio {dut.negative_flag.value}"
        await Timer(50, unit='ns')
        # ==========================================
        # CASO 4: resta aleatoria con Carry In = 0
        # ==========================================
        cocotb.log.info("Caso 4 inicio: Resta aleatoria con Carry In = 0")
        a=random.randint(-128, 127) #cambio los limites al ser un bit de signo
        b=random.randint(-128, 127) 
        c_in=0 
        cocotb.log.info(f"[CASO 4] Operación: {a} - {b} - 1 (Mod_sub = 1)")
        dut.in_a.value=a 
        dut.in_b.value=b 
        dut.carry_in.value=c_in 
        dut.mod_sub.value=1
        dut.select.value=0b01
        await Timer(10, unit='ns') 
        resta_real=(a-b-1) & 0xFF
        Ac=a&0xFF
        Bc=b&0xFF
        R_carry=1 if Ac > Bc else 0
        R_overflow=1 if (a-b-1) < -128 or (a-b-1) > 127 else 0
        R_zero=1 if resta_real == 0 else 0
        R_negative=1 if (resta_real >> 7) & 1 == 1 else 0
        cocotb.log.info(f"  -> [Esperado] Resta: {resta_real}, Carry: {R_carry}, Overflow: {R_overflow}, Zero: {R_zero}, Negative: {R_negative} \n [Obtenido DUT] Resta: {dut.out.value}, Carry: {dut.carry_out.value}, Overflow: {dut.overflow_flag.value}, Zero: {dut.zero_flag.value}, Negative: {dut.negative_flag.value}")
        assert dut.out.value == resta_real, f"Error en la resta: {a} - {b} = {resta_real}, pero dio {dut.out.value}"
        assert dut.carry_out.value == R_carry, f"Error en el Carry Out, el esperado es {R_carry}, pero dio {dut.carry_out.value}"
        assert dut.overflow_flag.value == R_overflow, f"Error en el Overflow Out, el esperado es {R_overflow}, pero dio {dut.overflow_flag.value}"
        assert dut.zero_flag.value == R_zero, f"Error en el Zero Flag, el esperado es {R_zero}, pero dio {dut.zero_flag.value}"
        assert dut.negative_flag.value == R_negative, f"Error en el Negative Flag, el esperado es {R_negative}, pero dio {dut.negative_flag.value}"
        await Timer(50, unit='ns')

    for i in range(200):
        # ==========================================
        #          Testeo del logico
        # ==========================================

        # ==========================================
        #                caso and
        # ==========================================
        a=random.randint(0, 255) #entrada A aleatoria
        b=random.randint(0, 255) #entrada B aleatoria
        dut.in_a.value=a
        dut.in_b.value=b
        dut.select.value=0b10 #seleccionamos modo logico
        dut.op.value=0b00 #seleccionamos operacion and
        await Timer(10, unit='ns')
        E_a = a & b
        R_zero=1 if E_a == 0 else 0
        R_negative=1 if (E_a >> 7) & 1 == 1 else 0
        cocotb.log.info(f"  -> [Esperado] AND: {E_a}, Zero: {R_zero}, Negative: {R_negative} \n [Obtenido DUT] AND: {dut.out.value}, Zero: {dut.zero_flag.value}, Negative: {dut.negative_flag.value}")
        assert dut.out.value == E_a, f"Error en la operacion AND: {a} & {b} = {E_a}, pero dio {dut.out.value}"
        assert dut.zero_flag.value == R_zero, f"Error en el Zero Flag, el esperado es {R_zero}, pero dio {dut.zero_flag.value}"
        assert dut.negative_flag.value == R_negative, f"Error en el Negative Flag, el esperado es {R_negative}, pero dio {dut.negative_flag.value}"
        await Timer(50, unit='ns')
        # ==========================================
        #                caso or
        # ==========================================
        a=random.randint(0, 255) #entrada A aleatoria
        b=random.randint(0, 255) #entrada B aleatoria
        dut.in_a.value=a
        dut.in_b.value=b
        dut.select.value=0b10 #seleccionamos modo logico
        dut.op.value=0b01 #seleccionamos operacion or
        await Timer(10, unit='ns')
        E_a = a | b
        R_zero=1 if E_a == 0 else 0
        R_negative=1 if (E_a >> 7) & 1 == 1 else 0
        cocotb.log.info(f"  -> [Esperado] OR: {E_a}, Zero: {R_zero}, Negative: {R_negative} \n [Obtenido DUT] OR: {dut.out.value}, Zero: {dut.zero_flag.value}, Negative: {dut.negative_flag.value}")
        assert dut.out.value == E_a, f"Error en la operacion OR: {a} | {b} = {E_a}, pero dio {dut.out.value}"
        assert dut.zero_flag.value == R_zero, f"Error en el Zero Flag, el esperado es {R_zero}, pero dio {dut.zero_flag.value}"
        assert dut.negative_flag.value == R_negative, f"Error en el Negative Flag, el esperado es {R_negative}, pero dio {dut.negative_flag.value}"
        await Timer(50, unit='ns')
        # ==========================================
        #                caso Xor
        # ==========================================
        a=random.randint(0, 255) #entrada A aleatoria
        b=random.randint(0, 255) #entrada B aleatoria
        dut.in_a.value=a
        dut.in_b.value=b
        dut.select.value=0b10 #seleccionamos modo logico
        dut.op.value=0b10 #seleccionamos operacion xor
        await Timer(10, unit='ns')
        E_a = a ^ b
        R_zero=1 if E_a == 0 else 0
        R_negative=1 if (E_a >> 7) & 1 == 1 else 0
        cocotb.log.info(f"  -> [Esperado] XOR: {E_a}, Zero: {R_zero}, Negative: {R_negative} \n [Obtenido DUT] XOR: {dut.out.value}, Zero: {dut.zero_flag.value}, Negative: {dut.negative_flag.value}")
        assert dut.out.value == E_a, f"Error en la operacion XOR: {a} ^ {b} = {E_a}, pero dio {dut.out.value}"
        assert dut.zero_flag.value == R_zero, f"Error en el Zero Flag, el esperado es {R_zero}, pero dio {dut.zero_flag.value}"
        assert dut.negative_flag.value == R_negative, f"Error en el Negative Flag, el esperado es {R_negative}, pero dio {dut.negative_flag.value}"
        await Timer(50, unit='ns')
        # ==========================================
        #                caso Not
        # ==========================================
        a = random.randint(0, 255)
        dut.in_a.value = a
        dut.select.value = 0b10       # modo lógico
        dut.op.value = 0b11           # operación NOT
        await Timer(10, unit='ns')
        E_a = (~a) & 0xFF
        R_zero = 1 if E_a == 0 else 0
        R_negative = 1 if (E_a >> 7) & 1 == 1 else 0
        cocotb.log.info(f"  -> [Esperado] NOT: {E_a}, Zero: {R_zero}, Negative: {R_negative} \n [Obtenido DUT] NOT: {dut.out.value}, Zero: {dut.zero_flag.value}, Negative: {dut.negative_flag.value}")
        assert dut.out.value == E_a, f"Error en la operacion NOT: ~{a} = {E_a}, pero dio {dut.out.value}"
        assert dut.zero_flag.value == R_zero, f"Error en el Zero Flag, el esperado es {R_zero}, pero dio {dut.zero_flag.value}"
        assert dut.negative_flag.value == R_negative, f"Error en el Negative Flag, el esperado es {R_negative}, pero dio {dut.negative_flag.value}"
        await Timer(50, unit='ns')

    for i in range(200):
        # ==========================================
        #                caso Bypass
        # ==========================================
        a = random.randint(0, 255)
        
        dut.in_a.value = a
        dut.select.value = 0b11       # modo bypass
        await Timer(10, unit='ns')
        E_a = a
        R_zero = 1 if E_a == 0 else 0
        R_negative = 1 if (E_a >> 7) & 1 == 1 else 0
        cocotb.log.info(f"  -> [Esperado] Bypass: {E_a}, Zero: {R_zero}, Negative: {R_negative} \n [Obtenido DUT] Bypass: {dut.out.value}, Zero: {dut.zero_flag.value}, Negative: {dut.negative_flag.value}")
        assert dut.out.value == E_a, f"Error en bypass: esperado {E_a}, dio {dut.out.value}"
        assert dut.zero_flag.value == R_zero, f"Error en el Zero Flag, el esperado es {R_zero}, pero dio {dut.zero_flag.value}"
        assert dut.negative_flag.value == R_negative, f"Error en el Negative Flag, el esperado es {R_negative}, pero dio {dut.negative_flag.value}"
        await Timer(50, unit='ns')
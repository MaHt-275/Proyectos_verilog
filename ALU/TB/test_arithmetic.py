#Importar las librerias
import cocotb
import random
from cocotb.triggers import Timer
#iniciar test
@cocotb.test() #Decorador para indicar que es un test
async def test_arithmetic(dut):
    """Test para el modulo de aritmetica"""#comentario de la funcion visible para Cocotb
  
    # ==========================================
    # CASO 1: Suma aleatoria con CarryIn = 0
    # ==========================================
    cocotb.log.info("Caso 1 inicio: Suma aleatoria con Carry In = 0")
    a=random.randint(0, 255) #entrada A aleatoria
    b=random.randint(0, 255) #entrada B aleatoria
    c_in=0 #Carry In en 0
    cocotb.log.info(f"[CASO 1] Operación: {a} + {b} + {c_in} (Mod_sub = 0)")
    dut.in_a.value=a #asignar valor a la entrada A
    dut.in_b.value=b #asignar valor a la entrada B
    dut.carry_in.value=c_in #asignar valor a la entrada Carry_In
    dut.mod_sub.value=0 #asignar valor a la entrada mod_sub
    await Timer(10, unit='ns') #esperar 10 ns para que se propague la señal
    #Verificar la salida de la suma
    #calculamos la suma real
    suma_real=(a+b+c_in) & 0xFF #truncar a 8bits
    a_s = a - 256 if a > 127 else a
    b_s = b - 256 if b > 127 else b
    R_carry=0 if (a+b+c_in) <= 255 else 1 #calcular el carry real
    R_overflow=1 if (a_s+b_s+c_in) < -128 or (a_s+b_s+c_in) > 127 else 0
    #Verificamos que la salida del DUT sea igual a la suma real
    cocotb.log.info(f"  -> [Esperado] Suma: {suma_real}, Carry: {R_carry} | [Obtenido DUT] Suma: {dut.arit_out.value}, Carry: {dut.carry_out.value}")
    assert dut.arit_out.value == suma_real, f"Error en la suma: {a} + {b} + {c_in} = {suma_real}, pero dio {dut.arit_out.value}"
    assert dut.overflow_flag.value == R_overflow, f"Error en el Overflow Out, el esperado es {R_overflow}, pero dio {dut.overflow_flag.value}"
    assert dut.carry_out.value == R_carry, f"Error en el Carry Out, el esperado es {R_carry}, pero dio {dut.carry_out.value}"
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
    await Timer(10, unit='ns')
    suma_real=(a+b+c_in) & 0xFF
    a_s = a - 256 if a > 127 else a
    b_s = b - 256 if b > 127 else b
    R_carry=0 if (a+b+c_in) <= 255 else 1
    R_overflow=1 if (a_s+b_s+c_in) < -128 or (a_s+b_s+c_in) > 127 else 0
    cocotb.log.info(f"  -> [Esperado] Suma: {suma_real}, Carry: {R_carry} | [Obtenido DUT] Suma: {dut.arit_out.value}, Carry: {dut.carry_out.value}")
    assert dut.arit_out.value == suma_real, f"Error en la suma: {a} + {b} + {c_in} = {suma_real}, pero dio {dut.arit_out.value}"
    assert dut.overflow_flag.value == R_overflow, f"Error en el Overflow Out, el esperado es {R_overflow}, pero dio {dut.overflow_flag.value}"
    assert dut.carry_out.value == R_carry, f"Error en el Carry Out, el esperado es {R_carry}, pero dio {dut.carry_out.value}"
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
    await Timer(10, unit='ns') 
    resta_real=(a-b) & 0xFF
    R_overflow=1 if (a-b) < -128 or (a-b) > 127 else 0
    Ac=a&0xFF
    Bc=b&0xFF
    R_carry=1 if Ac >= Bc else 0
    cocotb.log.info(f"  -> [Esperado] Resta: {resta_real}, Overflow: {R_overflow} | [Obtenido DUT] Resta: {dut.arit_out.value}, Overflow: {dut.overflow_flag.value}")
    assert dut.arit_out.value == resta_real, f"Error en la resta: {a} - {b} = {resta_real}, pero dio {dut.arit_out.value}"
    assert dut.carry_out.value == R_carry, f"Error en el Carry Out, el esperado es {R_carry}, pero dio {dut.carry_out.value}"
    assert dut.overflow_flag.value == R_overflow, f"Error en el Overflow Out, el esperado es {R_overflow}, pero dio {dut.overflow_flag.value}"
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
    await Timer(10, unit='ns') 
    resta_real=(a-b-1) & 0xFF
    Ac=a&0xFF
    Bc=b&0xFF
    R_carry=1 if Ac >= Bc else 0
    R_overflow=1 if (a-b-1) < -128 or (a-b-1) > 127 else 0
    cocotb.log.info(f"  -> [Esperado] Resta: {resta_real}, Overflow: {R_overflow} | [Obtenido DUT] Resta: {dut.arit_out.value}, Overflow: {dut.overflow_flag.value}")
    assert dut.arit_out.value == resta_real, f"Error en la resta: {a} - {b} = {resta_real}, pero dio {dut.arit_out.value}"
    assert dut.carry_out.value == R_carry, f"Error en el Carry Out, el esperado es {R_carry}, pero dio {dut.carry_out.value}"
    assert dut.overflow_flag.value == R_overflow, f"Error en el Overflow Out, el esperado es {R_overflow}, pero dio {dut.overflow_flag.value}"
    await Timer(50, unit='ns')
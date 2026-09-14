import cocotb
import random
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock

# ==========================================
# Función auxiliar para enviar datos al decoder
# ==========================================
async def enviar_datos(dut, inst, a, b):
    # Asegurarnos de que el puerto de entrada "in" reciba los datos correctamente.
    # Usamos getattr porque "in" es una palabra reservada en Python.
    puerto_in = getattr(dut, "in")
    
    # CICLO 0: Enviar Instrucción
    puerto_in.value = inst
    await RisingEdge(dut.clk)
    
    # CICLO 1: Enviar Dato A
    puerto_in.value = a
    await RisingEdge(dut.clk)
    
    # CICLO 2: Enviar Dato B
    puerto_in.value = b
    await RisingEdge(dut.clk)
    
    # Esperamos al siguiente ciclo donde el contador vuelve a 0
    # y la ALU tiene los datos A y B estables
    await RisingEdge(dut.clk)
    await Timer(1, unit='ns') # Pequeño retardo para propagación combinacional


@cocotb.test()
async def test_decoder(dut):
    """Test para el modulo Decoder + ALU Top"""
    
    # 1. Iniciar el reloj (Periodo de 10 ns)
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    
    # 2. Secuencia de Reset
    dut.rst.value = 1
    getattr(dut, "in").value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    
    for i in range(200):
        a = random.randint(0, 255)
        # ==========================================
        #           Testeo del desplazador
        # ==========================================
        cocotb.log.info("Testeo del desplazador")
        
        # caso 1: Desplazamiento a la izquierda
        cocotb.log.info("Caso 1: Desplazamiento a la izquierda")
        for n in range(8):
            E_a = (a << n) & 0xFF
            carry_esperado = (a >> (8 - n)) & 1 if n != 0 else 0
            zero_esperado = 1 if E_a == 0 else 0
            negative_esperado = (E_a >> 7) & 1
            
            # Construir instrucción: Select=00, dir=0, arit=0, amount=n
            instruccion = (0b00 << 6) | (0 << 5) | (0 << 4) | (n << 1)
            await enviar_datos(dut, instruccion, a, 0) # b no importa en shifts

            cocotb.log.info(f"Desplazamiento izq {n} veces")
            assert dut.out.value == E_a, f"Error en desplazamiento izq {n}: esperado {E_a}, dio {dut.out.value}"
            assert dut.zeros_flag.value == zero_esperado, f"Error en zero izq {n}"
            assert dut.carry_flag.value == carry_esperado, f"Error en carry izq {n}"
            assert dut.negative_flag.value == negative_esperado, f"Error en negative izq {n}"

        # caso 2: Desplazamiento a la derecha lógico
        cocotb.log.info("Caso 2: Desplazamiento a la derecha logico")
        for n in range(8):
            E_a = (a >> n) & 0xFF
            carry_esperado = (a >> (n - 1)) & 1 if n != 0 else 0
            zero_esperado = 1 if E_a == 0 else 0
            negative_esperado = (E_a >> 7) & 1
            
            # Construir instrucción: Select=00, dir=1, arit=0, amount=n
            instruccion = (0b00 << 6) | (1 << 5) | (0 << 4) | (n << 1)
            await enviar_datos(dut, instruccion, a, 0)

            assert dut.out.value == E_a, f"Error en desplazamiento der {n}"
            assert dut.carry_flag.value == carry_esperado, f"Error en carry der {n}"
            assert dut.zeros_flag.value == zero_esperado, f"Error en zero der {n}"
            assert dut.negative_flag.value == negative_esperado, f"Error en negative der {n}"

        # caso 3: Desplazamiento a la derecha aritmético
        cocotb.log.info("Caso 3: Desplazamiento a la derecha aritmetico")
        a_arith = a - 256 if a > 127 else a
        for n in range(8):
            E_a = (a_arith >> n) & 0xFF
            carry_esperado = (a >> (n - 1)) & 1 if n != 0 else 0
            zero_esperado = 1 if E_a == 0 else 0
            negative_esperado = 1 if (E_a >> 7) & 1 == 1 else 0
            
            # Construir instrucción: Select=00, dir=1, arit=1, amount=n
            instruccion = (0b00 << 6) | (1 << 5) | (1 << 4) | (n << 1)
            await enviar_datos(dut, instruccion, a, 0)

            assert dut.out.value == E_a, f"Error en aritmético der {n}"
            assert dut.carry_flag.value == carry_esperado, f"Error en carry aritmetico der {n}"
            assert dut.zeros_flag.value == zero_esperado, f"Error en zero aritmetico der {n}"
            assert dut.negative_flag.value == negative_esperado, f"Error en negative aritmetico der {n}"

    for i in range(200):
        # ==========================================
        #           Testeo del aritmético
        # ==========================================
        
        # CASO 1: Suma aleatoria con CarryIn = 0
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c_in = 0
        
        # Instrucción: Select=01, mod_sub=0, carry_in=0
        instruccion = (0b01 << 6) | (0 << 5) | (c_in << 4)
        await enviar_datos(dut, instruccion, a, b)
        
        suma_real = (a + b + c_in) & 0xFF
        a_s = a - 256 if a > 127 else a
        b_s = b - 256 if b > 127 else b
        R_carry = 0 if (a + b + c_in) <= 255 else 1
        R_overflow = 1 if (a_s + b_s + c_in) < -128 or (a_s + b_s + c_in) > 127 else 0
        R_zero = 1 if suma_real == 0 else 0
        R_negative = 1 if (suma_real >> 7) & 1 == 1 else 0
        
        assert dut.out.value == suma_real, f"Error en suma: {a}+{b}+{c_in}"
        assert dut.overflow_flag.value == R_overflow, "Error Overflow Suma"
        assert dut.carry_flag.value == R_carry, "Error Carry Suma"
        assert dut.zeros_flag.value == R_zero, "Error Zero Suma"
        assert dut.negative_flag.value == R_negative, "Error Negative Suma"

        # CASO 3: Resta aleatoria con Carry In = 1 (mod_sub = 1)
        a = random.randint(-128, 127)
        b = random.randint(-128, 127)
        c_in = 1
        
        # Instrucción: Select=01, mod_sub=1, carry_in=1
        instruccion = (0b01 << 6) | (1 << 5) | (c_in << 4)
        await enviar_datos(dut, instruccion, a & 0xFF, b & 0xFF)
        
        resta_real = (a - b) & 0xFF
        R_overflow = 1 if (a - b) < -128 or (a - b) > 127 else 0
        R_carry = 1 if (a & 0xFF) >= (b & 0xFF) else 0
        R_zero = 1 if resta_real == 0 else 0
        R_negative = 1 if (resta_real >> 7) & 1 == 1 else 0
        
        assert dut.out.value == resta_real, f"Error en resta: {a}-{b}"
        assert dut.carry_flag.value == R_carry, "Error Carry Resta"
        assert dut.overflow_flag.value == R_overflow, "Error Overflow Resta"
        assert dut.zeros_flag.value == R_zero, "Error Zero Resta"
        assert dut.negative_flag.value == R_negative, "Error Negative Resta"

    for i in range(200):
        # ==========================================
        #           Testeo Lógico
        # ==========================================
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        
        # AND (Select = 10, OP = 00)
        instruccion = (0b10 << 6) | (0b00 << 4)
        await enviar_datos(dut, instruccion, a, b)
        E_a = a & b
        assert dut.out.value == E_a, "Error AND"
        assert dut.zeros_flag.value == (1 if E_a == 0 else 0), "Error Zero AND"
        
        # OR (Select = 10, OP = 01)
        instruccion = (0b10 << 6) | (0b01 << 4)
        await enviar_datos(dut, instruccion, a, b)
        E_a = a | b
        assert dut.out.value == E_a, "Error OR"
        
        # XOR (Select = 10, OP = 10)
        instruccion = (0b10 << 6) | (0b10 << 4)
        await enviar_datos(dut, instruccion, a, b)
        E_a = a ^ b
        assert dut.out.value == E_a, "Error XOR"
        
        # NOT (Select = 10, OP = 11)
        instruccion = (0b10 << 6) | (0b11 << 4)
        await enviar_datos(dut, instruccion, a, b)
        E_a = (~a) & 0xFF
        assert dut.out.value == E_a, "Error NOT"

    for i in range(200):
        # ==========================================
        #           Testeo Bypass
        # ==========================================
        a = random.randint(0, 255)
        
        # BYPASS (Select = 11)
        instruccion = (0b11 << 6)
        await enviar_datos(dut, instruccion, a, 0)
        
        E_a = a
        assert dut.out.value == E_a, "Error Bypass"
        assert dut.zeros_flag.value == (1 if E_a == 0 else 0)
        assert dut.negative_flag.value == (1 if (E_a >> 7) & 1 == 1 else 0)
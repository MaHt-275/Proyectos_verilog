// ============================================================
// barrel_shifter
// ------------------------------------------------------------
// Bloque combinacional de desplazamiento (shift) para la ALU.
// Recibe un dato de 8 bits y lo desplaza 0 a 7 posiciones,
// hacia la izquierda o la derecha, con relleno logico (0s)
// o aritmetico (extiende el bit de signo) segun corresponda.
// ============================================================
module barrel_shifter (
    input  [7:0] IN_A_BUS_8bits,   // Dato de entrada a desplazar

    input        SHIFT_IZ_DER,     // Direccion: 0 = izquierda, 1 = derecha
    input        SHIFT_ARIT_RIGHT, // Solo aplica si es a la derecha:
                                    // 0 = logico (rellena con 0s)
                                    // 1 = aritmetico (extiende el bit de signo)

    input        SHIFT_1,          // Suma 1 a la cantidad de desplazamiento
    input        SHIFT_2,          // Suma 2 a la cantidad de desplazamiento
    input        SHIFT_4,          // Suma 4 a la cantidad de desplazamiento

    output reg [7:0] OUT_BUS_8bits, // Dato ya desplazado
    output reg       Carry_flag     // Ultimo bit expulsado por el desplazamiento
);

    // --------------------------------------------------------
    // Cantidad total a desplazar (0 a 7)
    // Se arma juntando los 3 bits de control en un solo numero:
    // shift_amount = SHIFT_4*4 + SHIFT_2*2 + SHIFT_1*1
    // Es un "wire" porque es una conexion combinacional directa,
    // se recalcula sola apenas cambia cualquiera de las 3 entradas.
    // --------------------------------------------------------
    wire [2:0] shift_amount = {SHIFT_4, SHIFT_2, SHIFT_1};

    always @(*) begin

        // ----------------------------------------------------
        // Caso 1: no hay desplazamiento (shift_amount = 0)
        // El dato pasa igual y no hay bit expulsado.
        // ----------------------------------------------------
        if (shift_amount == 3'd0) begin
            OUT_BUS_8bits = IN_A_BUS_8bits;
            Carry_flag    = 1'b0;
        end

        // ----------------------------------------------------
        // Caso 2: desplazamiento a la izquierda
        // Siempre rellena con 0s por la derecha.
        // El bit que "se cae" por la izquierda es el que estaba
        // en la posicion (8 - shift_amount) del dato original.
        // Ej: shift_amount=1 -> se cae el bit 7 (el MSB original).
        // ----------------------------------------------------
        else if (SHIFT_IZ_DER == 1'b0) begin
            OUT_BUS_8bits = IN_A_BUS_8bits << shift_amount;
            Carry_flag    = IN_A_BUS_8bits[8 - shift_amount];
        end

        // ----------------------------------------------------
        // Caso 3: desplazamiento a la derecha (logico o aritmetico)
        // El bit que "se cae" por la derecha es el que estaba
        // en la posicion (shift_amount - 1) del dato original.
        // Ej: shift_amount=1 -> se cae el bit 0 (el LSB original).
        // Esta formula del Carry_flag es la misma sin importar
        // si el relleno es logico o aritmetico.
        // ----------------------------------------------------
        else begin

            // El operador ternario decide como se rellena
            // el hueco que deja el desplazamiento:
            OUT_BUS_8bits = SHIFT_ARIT_RIGHT
                             // Aritmetico: $signed(...) hace que Verilog
                             // trate el bus como numero con signo, y >>>
                             // repite el bit de signo (MSB) al rellenar.
                             ? ($signed(IN_A_BUS_8bits) >>> shift_amount)
                             // Logico: >> normal, rellena siempre con 0s.
                             : (IN_A_BUS_8bits >> shift_amount);

            Carry_flag    = IN_A_BUS_8bits[shift_amount - 1];
        end

    end

endmodule
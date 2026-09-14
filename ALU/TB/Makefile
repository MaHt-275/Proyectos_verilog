#===========================================================================#
#						Makefile para ALU Testbench							#
#===========================================================================#

#declaro que usare icarus como simulador por defecto y el lenguaje es verilog
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

#indicar direcciones de los archivos fuente y de testbench
 #le decimos que vuelva un paso atras y busque la carpeta RTL
VERILOG_SOURCES = ../RTL/arithmetic.v\
                  ../RTL/logic.v\
                  ../RTL/barrel_shifter.v\
                  ../RTL/alu_top.v\
                  ../RTL/decoder_alu.v
#iniciar la conexion con los TB
TOPLEVEL ?= decoder_alu #el ?= indica que no es un valor fijo, de esta manera puedo cambiarlo desde la linea de comandos si quiero
COCOTB_TEST_MODULES ?= test_decoder_alu
LOGFILE ?= resultado_test.log
#digo que usare cocotb para la simulacion y que busque el makefile de cocotb en la carpeta donde se instalo
include $(shell cocotb-config --makefiles)/Makefile.sim 
.PHONY: log
log:
	@bash -o pipefail -c '$(MAKE) 2>&1 | tee $(LOGFILE)'
#NOTAS: Usar make TOPLEVEL=modulo a probar COCOTB_TEST_MODULES= TB del modulo a probar
#de esta forma este Makefile es generico para el proyecto
#===========================================================================#
#						Makefile para ALU Testbench							#
#===========================================================================#
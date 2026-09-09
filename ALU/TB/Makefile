#===========================================================================#
#						Makefile para ALU Testbench							#
#===========================================================================#

#declaro que usare icarus como simulador por defecto y el lenguaje es verilog
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

#indicar direcciones de los archivos fuente y de testbench
direccion_RTL =$(CURDIR)/../RTL #le decimos que vuelva un paso atras y busque la carpeta RTL
VERILOG_SOURCES = $(direccion_RTL)/arithmetic.v \
                  $(direccion_RTL)/logic.v \
                  $(direccion_RTL)/barrel_shifter.v \
                  $(direccion_RTL)/alu_top.v \
#iniciar la conexion con los TB
TOPLEVEL ?= alu_top #el ?= indica que no es un valor fijo, de esta manera puedo cambiarlo desde la linea de comandos si quiero
MODULE ?= test_alu_top

#digo que usare cocotb para la simulacion y que busque el makefile de cocotb en la carpeta donde se instalo
include $(shell cocotb-config --makefiles)/Makefile.sim 

#NOTAS: Usar make TOPLEVEL=modulo a probar MODULE= TB del modulo a probar
#de esta forma este Makefile es generico para el proyecto
#===========================================================================#
#						Makefile para ALU Testbench							#
#===========================================================================#
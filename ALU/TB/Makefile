# ==============================================================================
# MAKEFILE PARA VERIFICACIÓN DE ALU CON COCOTB 2.0+ E ICARUS VERILOG
# Ubicación: Proyectos/ALU/TB/Makefile
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DEL ENTORNO DE SIMULACIÓN
# ------------------------------------------------------------------------------
# Simulador por defecto (Icarus Verilog)
SIM ?= icarus

# Lenguaje del diseño de hardware
TOPLEVEL_LANG ?= verilog

# Ruta absoluta hacia el directorio con los archivos de diseño RTL
RTL_DIR = $(PWD)/../RTL

# Flags de compilación para Icarus (habilita estándar Verilog-2012 / SystemVerilog)
ifeq ($(SIM), icarus)
  COMPILE_ARGS += -g2012
endif

# ------------------------------------------------------------------------------
# 2. DEFINICIÓN DE OBJETIVOS (TARGETS) DISPONIBLES
# ------------------------------------------------------------------------------
# Si ejecutas solo 'make', correrá el objetivo por defecto (la ALU completa)
.DEFAULT_GOAL := test_top

# Declaración de objetivos que no representan archivos físicos
.PHONY: all test_top test_logic test_arithmetic test_shifter clean

# Ejecuta todas las pruebas unitarias y la integración de forma secuencial
all: test_logic test_arithmetic test_shifter test_top

# --- TARGET 1: Prueba de Integración (Top-Level ALU) ---
# Compila todos los submódulos porque alu_top los instancia internamente
test_top:
	@echo "=== Ejecutando Testbench de Integración: alu_top ==="
	$(MAKE) -f $(lastword $(MAKEFILE_LIST)) sim \
		VERILOG_SOURCES="$(RTL_DIR)/alu_top.v $(RTL_DIR)/arithmetic.v $(RTL_DIR)/barrel_shifter.v $(RTL_DIR)/logic.v" \
		TOPLEVEL=alu_top \
		COCOTB_TEST_MODULES=test_alu_top

# --- TARGET 2: Prueba Unitaria del Módulo Lógico ---
test_logic:
	@echo "=== Ejecutando Testbench Unitario: logic ==="
	$(MAKE) -f $(lastword $(MAKEFILE_LIST)) sim \
		VERILOG_SOURCES=$(RTL_DIR)/logic.v \
		TOPLEVEL=logic \
		COCOTB_TEST_MODULES=test_logic

# --- TARGET 3: Prueba Unitaria del Módulo Aritmético ---
# NOTA: Asegúrate de que el archivo Python se llame test_arithmetic.py
test_arithmetic:
	@echo "=== Ejecutando Testbench Unitario: arithmetic ==="
	$(MAKE) -f $(lastword $(MAKEFILE_LIST)) sim \
		VERILOG_SOURCES=$(RTL_DIR)/arithmetic.v \
		TOPLEVEL=arithmetic \
		COCOTB_TEST_MODULES=test_arithmetic

# --- TARGET 4: Prueba Unitaria del Barrel Shifter ---
test_shifter:
	@echo "=== Ejecutando Testbench Unitario: barrel_shifter ==="
	$(MAKE) -f $(lastword $(MAKEFILE_LIST)) sim \
		VERILOG_SOURCES=$(RTL_DIR)/barrel_shifter.v \
		TOPLEVEL=barrel_shifter \
		COCOTB_TEST_MODULES=test_barrel_shifter

# ------------------------------------------------------------------------------
# 3. LIMPIEZA DE ARTEFACTOS DE SIMULACIÓN
# ------------------------------------------------------------------------------
# Elimina ejecutables temporales, carpetas de compilación y archivos de ondas
clean::
	rm -rf sim_build results.xml *.vcd *.fst __pycache__

# ------------------------------------------------------------------------------
# 4. INCLUSIÓN DE LAS REGLAS MAESTRAS DE COCOTB
# ------------------------------------------------------------------------------
# Carga las reglas internas de Cocotb que gestionan la compilación VPI y el runtime
include $(shell cocotb-config --makefiles)/Makefile.sim
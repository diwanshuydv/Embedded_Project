# ==========================================
# Standalone STM32F429ZI Makefile
# ==========================================

PROJECT = my_lcd_firmware

# Setup libopencm3 dependency local to project
OPENCM3_DIR = libopencm3

# All the source files from the libopencm3 example
SOURCES = main.c clock/clock.c console/console.c font/font-7x12.c gfx/gfx.c lcd_driver/lcd-spi.c sdram/sdram.c
OBJS = $(SOURCES:.c=.o)

PREFIX = arm-none-eabi-
CC = $(PREFIX)gcc
OBJCOPY = $(PREFIX)objcopy
SIZE = $(PREFIX)size

INCLUDES = -I$(OPENCM3_DIR)/include -Ilcd_driver -Iclock -Iconsole -Igfx -Isdram -Ifont -I.

CFLAGS = -Os -g3 -Wall -Wextra $(INCLUDES) \
         -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -DSTM32F4 \
         -fdata-sections -ffunction-sections -fno-exceptions -fno-unwind-tables

LDSCRIPT = stm32f429zi.ld

LDFLAGS = -L$(OPENCM3_DIR)/lib -T$(LDSCRIPT) -nostartfiles \
          -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 \
          -specs=nano.specs -specs=nosys.specs -Wl,--gc-sections

LDLIBS = -lopencm3_stm32f4 -lm

# ==========================================
# Build Targets
# ==========================================

all: $(OPENCM3_DIR)/lib/libopencm3_stm32f4.a $(PROJECT).elf $(PROJECT).bin size

# libopencm3 fetch and build targeting stm32f4
$(OPENCM3_DIR)/Makefile:
	git submodule update --init

$(OPENCM3_DIR)/lib/libopencm3_stm32f4.a: $(OPENCM3_DIR)/Makefile
	$(MAKE) -C $(OPENCM3_DIR) TARGETS=stm32/f4

# Compile objects, ensure libopencm3 is ready first for headers
$(OBJS): $(OPENCM3_DIR)/lib/libopencm3_stm32f4.a

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

$(PROJECT).elf: $(OBJS) $(LDSCRIPT)
	$(CC) $(OBJS) $(LDFLAGS) $(LDLIBS) -o $@

$(PROJECT).bin: $(PROJECT).elf
	$(OBJCOPY) -O binary $< $@

size: $(PROJECT).elf
	$(SIZE) $<

clean:
	rm -f *.elf *.bin *.o lcd_driver/*.o clock/*.o console/*.o gfx/*.o sdram/*.o font/*.o

clobber: clean
	rm -rf $(OPENCM3_DIR)

flash: $(PROJECT).elf
	openocd -f board/stm32f429discovery.cfg -c "program $(PROJECT).elf verify reset exit"

.PHONY: all clean clobber flash size

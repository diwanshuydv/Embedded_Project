# Embedded Project - STM32F429ZI LCD Firmware with TensorFlow Lite Micro

## Overview

This project implements a comprehensive firmware solution for the STM32F429ZI microcontroller, specifically designed for the STM32F429I-DISCOVERY development board. The firmware provides full control over the onboard LCD display, integrates machine learning capabilities via TensorFlow Lite Micro, and includes various peripheral drivers for a complete embedded system.

The project demonstrates advanced embedded development techniques, including real-time graphics rendering, serial communication, memory management, and on-device AI inference.

## Features

### Core Functionality
- **LCD Display Control**: Full-color LCD driver with SPI interface for high-resolution graphics output
- **Graphics Engine**: Custom graphics library supporting drawing primitives, text rendering, and image display
- **Machine Learning Integration**: TensorFlow Lite Micro for on-device inference with pre-trained models
- **Image Processing**: STB image libraries for loading and resizing images
- **Real-time Clock**: Hardware clock management for timing operations
- **Serial Communication**: USART driver for data transmission and reception
- **SDRAM Controller**: External memory management for larger data buffers
- **Console Interface**: Text-based console for debugging and user interaction

### Hardware Interfaces
- SPI LCD interface
- USART serial communication
- GPIO pin control
- External SDRAM
- Onboard LEDs and buttons (STM32F429I-DISCOVERY)

### Software Components
- Modular architecture with separate drivers for each peripheral
- Custom font rendering (7x12 pixel font)
- Image conversion utilities (convert_to_h.c)
- Python host scripts for data transfer and testing

## Architecture

The project is organized into the following modules:

- **main.cpp**: Main application entry point and initialization
- **clock/**: Real-time clock management
- **console/**: Text console implementation
- **font/**: Font data and rendering functions
- **gfx/**: Graphics primitives and drawing functions
- **lcd_driver/**: LCD hardware interface and control
- **sdram/**: External SDRAM memory controller
- **usart/**: Serial communication driver
- **tflite-micro/**: TensorFlow Lite Micro library for ML inference
- **libopencm3/**: Hardware abstraction layer for STM32 peripherals

## Hardware Requirements

- **STM32F429I-DISCOVERY Board**: Primary development platform
  - STM32F429ZI microcontroller (180 MHz Cortex-M4 with FPU)
  - 2.4" QVGA TFT LCD (320x240 resolution)
  - 64 MB SDRAM
  - USB OTG interface
  - User LEDs and push-buttons

- **USB Cable**: For programming and serial communication
- **ST-Link Programmer**: Integrated on the discovery board

## Software Requirements

### Development Environment
- **Operating System**: Linux, macOS, or Windows (with appropriate toolchain)
- **ARM GCC Toolchain**: Version 9.0 or later
- **OpenOCD**: Version 0.11.0 or later
- **Git**: For submodule management
- **Python 3**: For host scripts (version 3.6+)

### Dependencies
- **libopencm3**: Hardware abstraction library (included as submodule)
- **TensorFlow Lite Micro**: Machine learning inference engine (included)
- **STB Image Libraries**: Image loading and processing (included)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Embedded_Project
```

### 2. Initialize Submodules

```bash
git submodule update --init --recursive
```

### 3. Install ARM Toolchain

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install gcc-arm-none-eabi binutils-arm-none-eabi build-essential git openocd
```

#### macOS (using Homebrew)
```bash
brew install arm-none-eabi-gcc openocd
```

#### Windows
- Download and install ARM GCC toolchain from [Arm Developer](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm)
- Install OpenOCD from [OpenOCD website](http://openocd.org/)

### 4. Install Python Dependencies

```bash
pip install pyserial  # For serial communication scripts
```

## Build Instructions

### Standard Build
```bash
make
```

This command will:
1. Initialize and build libopencm3 if necessary
2. Compile all source files
3. Link the firmware
4. Generate `my_lcd_firmware.elf` and `my_lcd_firmware.bin`

### Clean Build
```bash
make clean
make
```

### Verbose Build
```bash
make V=1
```

## Flashing the Firmware

### Using OpenOCD (Recommended)
1. Connect the STM32F429I-DISCOVERY board via USB
2. Ensure the board is in programming mode (BOOT0 jumper set appropriately)
3. Run the flash command:

```bash
make flash
```

### Manual Flashing
```bash
openocd -f interface/stlink-v2-1.cfg -f target/stm32f4x.cfg -c "program my_lcd_firmware.elf verify reset exit"
```

## Usage

### Running the Firmware
1. Flash the firmware as described above
2. Reset the board or power cycle it
3. The LCD should display the application interface
4. Use serial communication for data transfer (see Python scripts)

### Python Host Scripts

#### Port Checking
```bash
python python_scripts/check_port.py
```

#### Data Echo Test
```bash
python python_scripts/echo.py
```

#### Main Communication Script
```bash
python python_scripts/main.py
```

### Serial Communication
- **Baud Rate**: 115200
- **Data Bits**: 8
- **Stop Bits**: 1
- **Parity**: None
- **Flow Control**: None

## Model Integration

The firmware includes TensorFlow Lite Micro for machine learning inference:

- Pre-trained models stored in `model_data.h`
- Inference can be performed on image data or sensor inputs
- Results displayed on LCD or transmitted via serial

## Troubleshooting

### Current Known Issues

1. **Serial Communication Hang**: Python scripts may hang after sending data to the ACM port.
   - **Workaround**: Ensure proper USB device detection
   - **Debug**: Check device permissions and serial port configuration
   - **Status**: Urgent fix required

### Common Problems

#### Build Errors
- Ensure all submodules are initialized: `git submodule update --init --recursive`
- Verify ARM GCC toolchain installation: `arm-none-eabi-gcc --version`
- Check for missing dependencies

#### Flashing Issues
- Confirm ST-Link connection: `openocd -f interface/stlink-v2-1.cfg -f target/stm32f4x.cfg -c "init; reset; shutdown"`
- Verify board power and jumper settings
- Try different USB ports

#### Serial Communication Problems
- Check device permissions: `ls -la /dev/ttyACM*`
- Verify baud rate and serial settings in both firmware and host scripts
- Test with simple echo script first

#### LCD Display Issues
- Ensure proper SPI pin connections
- Check LCD power supply
- Verify initialization sequence timing

### Debug Tips
- Use `make V=1` for verbose build output
- Enable debug prints in firmware for serial monitoring
- Use OpenOCD for GDB debugging: `make debug`

## Development

### Code Structure
- **Headers (.h)**: Function declarations and type definitions
- **Sources (.c/.cpp)**: Implementation files
- **Makefile**: Build configuration and rules
- **Linker Script**: Memory layout definition

### Adding New Features
1. Create module in appropriate directory
2. Add header and source files
3. Update Makefile with new sources
4. Include headers in main application

### Testing
- Unit tests can be added using the existing test framework
- Hardware testing on STM32F429I-DISCOVERY board
- Serial communication testing with Python scripts

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -am 'Add feature'`
5. Push to branch: `git push origin feature-name`
6. Submit a pull request

### Code Style
- Follow C/C++ best practices
- Use consistent naming conventions
- Add comments for complex logic
- Test on target hardware before committing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **STMicroelectronics**: For the STM32F429I-DISCOVERY board and documentation
- **libopencm3**: Open-source ARM Cortex-M microcontroller library
- **TensorFlow**: For TensorFlow Lite Micro
- **STB Libraries**: For image processing utilities

## Contact

For questions, issues, or contributions, please open an issue on the GitHub repository or contact the maintainers.

---

**Note**: This firmware is designed for educational and development purposes. Ensure proper testing before deploying in production environments.

## Clean

To clean the project objects and binaries:
```bash
make clean
```

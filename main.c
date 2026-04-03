#include <stdint.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include "usart/usart.h" 

#define IMG_MAX 4096
uint8_t buffer[IMG_MAX];

int main(void) {
    // 1. Initialize hardware
    usart_clock_setup();
    gpio_setup();
    usart_setup();

    // 2. Send boot message
    usart_send_string("STM32 Ready to Buffer and Echo!\r\n");

    // 3. Infinite Echo Loop
    while (1) {
        // --- STEP 1: Wait for Header (\xAA \x55) ---
        // We cast to uint8_t to handle raw binary data safely
        if ((uint8_t)usart_read_char() != 0xAA) continue;
        if ((uint8_t)usart_read_char() != 0x55) continue;

        // --- STEP 2: Read Size (Little Endian) ---
        uint8_t size_low = usart_read_char();
        uint8_t size_high = usart_read_char();
        
        // Reconstruct the 16-bit integer size
        uint16_t expected_size = (size_high << 8) | size_low;

        // Safety Check: Prevent buffer overflow if the size is corrupted
        if (expected_size > IMG_MAX) {
            continue; // Abort and wait for the next valid header
        }

        // --- STEP 3: Buffer the Image Payload ---
        for (uint16_t i = 0; i < expected_size; i++) {
            buffer[i] = usart_read_char();
        }

        // Turn ON LED to show we finished reading
        gpio_set(GPIOG, GPIO13);

        // --- STEP 4: Echo the entire packet back ---
        
        // 4a. Echo Header
        usart_send_blocking(USART1, 0xAA);
        usart_send_blocking(USART1, 0x55);
        
        // 4b. Echo Size
        usart_send_blocking(USART1, size_low);
        usart_send_blocking(USART1, size_high);
        
        // 4c. Echo Data Payload
        for (uint16_t i = 0; i < expected_size; i++) {
            usart_send_blocking(USART1, buffer[i]);
        }

        // Turn OFF LED to show we finished transmitting
        gpio_clear(GPIOG, GPIO13);
    }

    return 0;
}
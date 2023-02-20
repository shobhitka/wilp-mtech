#include "stm32f10x.h"  	   	// Device header
#include <stdio.h>

// Global sync flag to indicate when adc data
// is ready to be read. We dont want to process
// the data in interrupt handler
int adc_data_ready = 0;

void uart_init()
{
	// Enable the GPIO and UART1 clocks
	RCC->APB2ENR |= 0xFC | (1 << 14);
	
	// Uart configuration using GPIO Port A
	// RX1 input with pull - Port A.10
	GPIOA->ODR |= (1<<10);

	// RX1 input with pull up PA.10, TX1 = PA.9 - Alt Function output
	GPIOA->CRH = 0x444448B4;  
	
	// Enable UART with TX and RX
	USART1->CR1 = 0x200C;  
	
	// Set the UART baudrate. APB2 = 72 MHz, setting baud rate of 9600bos
	// BRR value to set = 72000000/9600 = 7500
	USART1->BRR = 7500;  
}

void uart_write_byte(unsigned char c)  
{  
	// Wait for TC flag to be set, to ensure last transmit is complete
	while((USART1->SR & (1 << 6)) == 0);  
	
	// send the byte
	USART1->DR = c;  
} 

/* Write null terminated strings on uart */  
void uart_write_str(char *str)  
{  
	while(*str != 0) { 
		uart_write_byte(*str);
		str++;  
	}  
}

void uart_write_int(unsigned int i)  
{  
	char str[10];  
	sprintf(str, "%d", i);
	uart_write_str(str);
}

void uart_write_float(float f)  
{  
	char str[10];  
	sprintf(str, "%0.2f", f);
	uart_write_str(str);
}

void setup_timer(int sec)
{
	// Enable TIM2 Clock
	RCC->APB1ENR |= (1<<0);

	// APB2 is set as 72 MHz, Set Prescalar to 7199
	// giving 0.1ms
	TIM2->PSC = 7200 - 1;
	
	// For 1 sec we need ARR to be set as 10000 - 1 = 9999
	// multiply that with number of seconds delay needed
	TIM2->ARR = sec * 10000 - 1;  
	
	// Clear the UIF flag
	TIM2->SR = 0;
	
	// Enable timer interrupts for TIM2
	TIM2->DIER = (1 << 0);
	NVIC->ISER[0] |= (1 << 28);
	
	// Enable the timer with upward counting(bit 4 is 0 for upward)
	TIM2->CR1 = 1;
}

void delay_us(uint16_t t)  
{  
	for(int i = 0; i < t; i++)  
	{  
		for(volatile uint16_t a = 0; a < 6; a++)  
			{
			}  
	}  
}

void setup_temp_adc()
{
	// Enable the ADC1 interface clock and GPIO Clocks
	RCC->APB2ENR |= 0xFC | (1 << 9);

	// Enable the ADC Presclar PCLK2 divided by 6
	// In the project settings the Crystal is configred at 8 MHz
	// This gives PCLK2 = 72 MHz. Setting ADCPrescalar divisor as 
	// 6 gives as ADCCLK of 12 MHz
	RCC->CFGR = (RCC->CFGR & 0xFF3F) | (2 << 14);

	// Use Port A, Pin 1 as ADC_IN1 analog input
	GPIOA->CRL = 0x44444404;
	
	// Power on the converter block
	ADC1->CR2 = 1;
	
	// Set the sampling time for ADC_IN1, we want to have a little
	// higher sampling time for samplig temperature sensor. Keeping
	// it 28.5 Cycles
	ADC1->SMPR2 = (3 << 3);
	
	// Enable ADC_IN1 as input for 1st conversion 
	ADC1->SQR3 = 1;
	
	// Allow the ADC block to stabalise after power up
	delay_us(1);
	
	// Enable interrupts for ADC1
	ADC1->CR1 |= (1 << 5);
	NVIC->ISER[0] |= (1 << 18);
}

float read_temperature_sensor()
{
	adc_data_ready = 0;
	return ADC1->DR;
}
	
void adc_trigger_conv()
{
	ADC1->CR2 |= 0x1;
}

// Timer2 interrupt handler to timer update interrupt
void timer_irq_handler()
{
	if (TIM2->SR & 1) {
		TIM2->SR &= ~(1<<0);      // clear UIF flag
		
		// stop the timer, will be restarted again after ADC conversion
		TIM2->CR1 = 0;
		
		// Trigger the ADC conversion
		adc_trigger_conv();
	}	 
}

// IRQ Handler for handling the EOC interrupt
void adc_irq_handler()
{
	if (ADC1->SR & (1 << 1)) {
		// clear the interrupt flag
		ADC1->SR &= ~(1 << 1);
		
		// conversion complete, set ADC data ready variable
		adc_data_ready = 1;
	}
}

void startup_msg()
{
	uart_write_str("Simulated Temperature Sensor charachetrisics: \n");
	uart_write_str("Measuring range 0 Deg to ~64 Deg\n");
	uart_write_str("VRef 20 Deg = 1280 ADC Value => 1.031 Volts\n");
	uart_write_str("Every 64 units or 0.052 Volts increase amounts to 1 Deg\n");
	uart_write_str("Starting timer to read temeprature value every 2s\n");
}

float convert_to_temp(int vsense)
{
	float raw_data = vsense;
	return (raw_data * 20) / 1280;
}

int main()
{
	uart_init();
	setup_temp_adc();
	startup_msg();
	
	// setup a timer for 2 seconds
	setup_timer(2);
	
	while (1) {
		if (adc_data_ready == 0)
			continue;
		
		int vsense = read_temperature_sensor();
		float temp = convert_to_temp(vsense);
		uart_write_str("Current temperature: ");
		uart_write_float(temp);
		uart_write_str(" Deg\n");
		
		// restart the timer
		setup_timer(2);
	}
}

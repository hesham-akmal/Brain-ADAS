#include "Can_PBcfg.h"
#include "Can_Cfg.h"

#include "inc/hw_memmap.h"
#include "driverlib/gpio.h"
#include "driverlib/pin_map.h"
#include "driverlib/sysctl.h"

Can_ControllerConfigType Can0ControllerConfig = {
	SYSCTL_PERIPH_GPIOB,
	GPIO_PB4_CAN0RX,
	GPIO_PB5_CAN0TX,
	GPIO_PORTB_BASE,
	GPIO_PIN_4 | GPIO_PIN_5,
	SYSCTL_PERIPH_CAN0,
	CAN0_BASE,
	500000
};
Can_ControllerConfigType *CanControllersConfigs[2] = {&Can0ControllerConfig, 0};
Can_ConfigType CanConfig = {CanControllersConfigs};

uint32 CAN_BASES[2] = {CAN0_BASE, CAN1_BASE};

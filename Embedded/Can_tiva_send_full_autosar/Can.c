//Can driver includes
#include "Can.h"
#include "CanIf_Cbk.h"
#include "EcuM_Cbk.h"
#include "Os.h"
#include "Spi.h"
#include "SchM_Can.h"
#include "MemMap.h"
#include "Det.h"
#include "Dem.h"
#include "Can_PBcfg.h"

#include <stdbool.h>

#include "inc/hw_can.h"
#include "inc/hw_ints.h"
#include "inc/hw_memmap.h"
#include "driverlib/can.h"
#include "driverlib/gpio.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.h"

#include "inc/hw_types.h"
#include "driverlib/debug.h"
#include "driverlib/fpu.h"
#include "driverlib/rom.h"

/**
 * Initialize software and hardware configurations for one CAN controller.
 *
 * @param canx_config			----- CAN controller configuration
 */
void Can_InitController(Can_ControllerConfigType *canx_config) {
	
	// Enable GPIO port
	SysCtlPeripheralEnable(canx_config->ui32GpioPeripheral);
	
	// Configure the GPIO pin muxing to select CAN functions for the pins.
	GPIOPinConfigure(canx_config->ui32RxPinConfig);
	GPIOPinConfigure(canx_config->ui32TxPinConfig);
	
	// Enable the alternate function on the GPIO pins.
	GPIOPinTypeCAN(canx_config->ui32Port, canx_config->ui8Pins);
	
	// Enable the CAN peripheral.
	SysCtlPeripheralEnable(canx_config->ui32CanPeripheral);
	
	// Initialize the CAN controller.
	CANInit(canx_config->ui32CanBase);
	
	// Set up the bit rate for the CAN bus.
	CANBitRateSet(canx_config->ui32CanBase, SysCtlClockGet(), canx_config->ui32BitRate);
	
	// Enable the CAN for operation.
	CANEnable(canx_config->ui32CanBase);
	
}

/**
 * Initialize software and hardware configurations for all attached CAN controllers.
 *
 * @param Config			----- CAN driver configuration
 */
void Can_Init(const Can_ConfigType* Config) {
	
	for(int i=0; i<2; i++) {
		if(Config->canx_config[i]) {
			Can_InitController(Config->canx_config[i]);
		}
	}
	
}

/**
 *  Perform polling of TX confirmation, and send confirmation to CanIf
 */
void Can_MainFunction_Write(void) {
	while((CANStatusGet(CAN0_BASE, CAN_STS_TXREQUEST) & 1)) {}
	//Send confirmation to CanIf	
}

/**
 *  Perform polling of RX indication, read the message from RX buffers, and send it to CanIf
 */
void Can_MainFunction_Read(void) {
	
	while((CANStatusGet(CAN0_BASE, CAN_STS_NEWDAT) & 1) == 0) {}

	tCANMsgObject sCANMessage;
	uint8_t pui8MsgData[8];
	sCANMessage.pui8MsgData = pui8MsgData;
	
	//
	// Read the message from the CAN.  Message object number 1 is used
	// (which is not the same thing as CAN ID).  The interrupt clearing
	// flag is not set because this interrupt was already cleared in
	// the interrupt handler.
	//
	CANMessageGet(CAN0_BASE, 1, &sCANMessage, 0);

	//
	// Check to see if there is an indication that some messages were
	// lost.
	//
	if(sCANMessage.ui32Flags & MSG_OBJ_DATA_LOST)
	{
			UARTprintf("CAN message loss detected\n");
	}

	//
	// Print out the contents of the message that was received.
	//
	UARTprintf("A new message arrived!\n");
	UARTprintf("Msg ID=0x%08X len=%u data=0x",
						 sCANMessage.ui32MsgID, sCANMessage.ui32MsgLen);
	unsigned int uIdx;
	for(uIdx = 0; uIdx < sCANMessage.ui32MsgLen; uIdx++)
	{
			UARTprintf("%02X ", pui8MsgData[uIdx]);
	}
	UARTprintf("\n");
	
	//Send message to CanIf
}

/**
 * Transmit PDU to CAN bus
 *
 * @param hth 				----- hardware transmit handle (HTH)
 * @param pduInfo  		----- PDU (protocol data unit), consists of: CanIf Id, Can Id, data, DLC
 * @return 						----- result status
 */
Can_ReturnType Can_Write(Can_HwHandleType hth, Can_PduType *pduInfo) {
	
	//Get CAN controller's base address
	uint32 CAN_BASE = CAN_BASES[hth];
	
	//Build the CAN message
  tCANMsgObject sCANMessage;
	sCANMessage.ui32MsgID = pduInfo->id;
  sCANMessage.ui32MsgIDMask = 0;
  sCANMessage.ui32MsgLen = pduInfo->length;
  sCANMessage.pui8MsgData = pduInfo->sdu;
	
	// Send the CAN message using object number 1 (not the same thing as CAN ID).
	// This function will cause the message to be transmitted right away.
	CANMessageSet(CAN_BASE, 1, &sCANMessage, MSG_OBJ_TYPE_TX);
	
	return CAN_OK;
}

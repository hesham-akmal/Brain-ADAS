#include <stdio.h>
#include <stdlib.h>

#include "Com.h"
#include "PduR.h"
#include "CanIf.h"

#include "inc/hw_memmap.h"
#include "driverlib/can.h"
#include "driverlib/sysctl.h"
#include "utils/uartstdio.h"
#include "uart.h"

#include "Can_PbCfg.h"
#include "Can.h"

/*
int main() {

	//Initialize all the modules
  ConfigureUART();
	
  SysCtlClockSet(SYSCTL_SYSDIV_1 | SYSCTL_USE_OSC | SYSCTL_OSC_MAIN |
                   SYSCTL_XTAL_16MHZ);
  InitConsole();
	PduR_Init(&PBPduRConfig);
	CanIf_Init(&canIf_Config);
  //Init CAN module
	Can_Init(&CanConfig);
	
	while(1) {
		uint32 Id = 1;
		uint8 length = 8;
		char buff[21];
		UARTgets(buff, 21);
		uint64 lmsg = atoll(buff);
		uint8 *msg = (uint8*)(&lmsg);
		ComSendSignal(Id, msg, length);
	}
	

	return 0;
}

*/

int main(void)
{
	//
    // Initialize the UART.
    //
    ConfigureUART();

    //
    // Set the clocking to run directly from the external crystal/oscillator.
    // TODO: The SYSCTL_XTAL_ value must be changed to match the value of the
    // crystal used on your board.
    //
    SysCtlClockSet(SYSCTL_SYSDIV_1 | SYSCTL_USE_OSC | SYSCTL_OSC_MAIN |
                   SYSCTL_XTAL_16MHZ);

    //
    // Set up the serial console to use for displaying messages.  This is
    // just for this example program and is not needed for CAN operation.
    //
    InitConsole();

		PduR_Init(&PBPduRConfig);
		CanIf_Init(&canIf_Config);
    //Enable CAN module
		Can_Init(&CanConfig);
		
    //
    // Enter loop to process received messages.  This loop just checks a flag
    // that is set by the interrupt handler, and if set it reads out the
    // message and displays the contents.  This is not a robust method for
    // processing incoming CAN data and can only handle one messages at a time.
    // If many messages are being received close together, then some messages
    // may be dropped.  In a real application, some other method should be used
    // for queuing received messages in a way to ensure they are not lost.  You
    // can also make use of CAN FIFO mode which will allow messages to be
    // buffered before they are processed.
    //
    for(;;)
    {

				UARTprintf("Waiting for a message...\n");
			
				Can_MainFunction_Read();
    }

    //
    // Return no errors
    //
    return(0);
}

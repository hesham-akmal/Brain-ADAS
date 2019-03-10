#include "types.h"

typedef enum Can_ReturnType {
	CAN_OK, /* Successful operation */
	CAN_NOT_OK, /* Error occurred or wakeup event occurred during sleep transition */
	CAN_BUSY /* Transmit request not processed because no transmit object was available*/
} Can_ReturnType;


typedef enum Can_StateTransitionType {
	CAN_T_STOP, /* Cannot request mode CAN_UNINIT */
	CAN_T_START,
	CAN_T_SLEEP,
	CAN_T_WAKEUP
} Can_StateTransitionType;


Can_ReturnType Can_SetControllerMode( uint8 Controller, Can_StateTransitionType Transition);
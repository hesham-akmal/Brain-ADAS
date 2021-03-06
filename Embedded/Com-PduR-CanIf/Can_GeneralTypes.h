#ifndef CAN_GENERAL_TYPES_H
#define CAN_GENERAL_TYPES_H



typedef uint16 Can_IdType; /* Assuming extended IDs are used, revert to uint16 for standard IDs, 0x Std ID, 1x Ext ID*/

/* Use uint16 if more than 255 H/W handles otherwise, uint8*/
typedef uint16 Can_HwHandleType;

typedef enum Can_StateTransitionType {
	CAN_T_STOP, /* Cannot request mode CAN_UNINIT */
	CAN_T_START,
	CAN_T_SLEEP,
	CAN_T_WAKEUP
} Can_StateTransitionType;

typedef enum Can_ReturnType {
	CAN_OK, /* Successful operation */
	CAN_NOT_OK, /* Error occurred or wakeup event occurred during sleep transition */
	CAN_BUSY /* Transmit request not processed because no transmit object was available*/
} Can_ReturnType;

typedef enum Can_ProcessingType {
	INTERRUPT,
	POLLING
} Can_ProcessingType;

typedef enum CanHandleType {
	BASIC,
	FULL
} CanHandleType;

typedef struct {
	uint16 canObjectId;
	CanHandleType canHandleType;
} CanHardwareObject;

typedef struct Can_ControllerType {
	/* @req CAN315 */
	bool CanControllerActivation;

	/* @req CAN382 */
	uint32 CanControllerBaseAddress;

	/* @req CAN316 */
	uint8 CanControllerId;

	/* @req CAN314 */
	Can_ProcessingType CanBusOffProcessing;

	/* @req CAN317 */
	Can_ProcessingType CanRxProcessing;

	/* @req CAN318 */
	Can_ProcessingType CanTxProcessing;
} Can_ControllerType;

typedef struct Can_HardwareObjectType {
	CanHandleType CanHandleType;
} Can_HardwareObjectType;

typedef struct Can_ConfigSetType {
	Can_ControllerType CanController;
	Can_HardwareObjectType CanHardwareObject;
} Can_ConfigSetType;

typedef struct Can_HwType {
	Can_IdType CanId; /* Standard/Extended CAN ID of CAN LPDU */
	Can_HwHandleType Hoh; /* ID of the corresponding HardwareObject Range */
	uint8 ControllerId; /* ControllerId provided by CanIf clearly identify the corresponding controller */
} Can_HwType;

typedef struct Can_PduType {
	PduIdType swPduHandle; /*CanIf private data , may be used by Callback */
	uint8 length; /* Length (8 bytes max) */
	Can_IdType id; /* the CAN ID, 29 or 11-bit */
	const uint8 *sdu; /* Data pointer */
} Can_PduType; /* here? */

typedef struct Can_MainFunctionRWPeriodType {
	float CanMainFunctionPeriod;
} Can_MainFunctionRWPeriodType;

typedef struct Can_Type {
	Can_ConfigSetType CanConfigSet;
} Can_Type;

typedef enum Can_TrcvModeType {
	CANTRCV_TRCVMODE_NORMAL = 0, /* Transceiver mode NORMAL */
	CANTRCV_TRCVMODE_STANDBY, /* Transceiver mode STANDBY */
	CANTRCV_TRCVMODE_SLEEP /* Transceiver mode SLEEP */
} Can_TrcvModeType;

typedef enum Can_TrcvWakeupReasonType {
	CANTRCV_WU_ERROR = 0, /* This value may only be reported when error was reported to DEM before. Wake-up reason was not detected */
	CANTRCV_WU_NOT_SUPPORTED, /* The transceiver does not support any information for the wakeup reason. */
	CANTRCV_WU_BY_BUS, /* Network has caused the wake up of the ECU */
	CANTRCV_WU_BY_PIN, /* Wake-up event at one of the transceiver's pins (not at the CAN bus). */
	CANTRCV_WU_INTERNALLY, /* Network has woken the ECU via a request to NORMAL mode */
	CANTRCV_WU_RESET, /* Wake-up is due to an ECU reset */
	CANTRCV_WU_POWER_ON /* Wake-up is due to an ECU reset after power on. */
} Can_TrcvWakeupReasonType;

typedef enum Can_TrcvWakeupModeType {
	CANTRCV_WUMODE_ENABLE = 0, /* Wakeup events notifications are enabled on the addressed network. */
	CANTRCV_WUMODE_DISABLE, /* Wakeup events notifications are disabled on the addressed network. */
	CANTRCV_WUMODE_CLEAR /* A stored wakeup event is cleared on the addressed network */
} Can_TrcvWakeupModeType;



#endif /* CAN_GENERAL_TYPES_H */

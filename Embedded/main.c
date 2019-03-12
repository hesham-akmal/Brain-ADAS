#include <stdio.h>
#include <stdlib.h>

#include "ComStack/PduR.h"
#include "ComStack/EcuC.h"
#include "ComStack/CanIf.h"
#include "ComStack/Com.h"
#include "ComStack/CanIf_Cbk.h"
#include "ComStack/Can_GeneralTypes.h"
#include "ComStack/CanIf.h"
#include "test.h"

int main()
{
	///Test autosar com stack (pdur, canif)
	///Initialization of router
	PduR_Init(&PBPduRConfig);
	///Initialization of can interface
	CanIf_Init(&CanIf_Config);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		///Start controller 0
	if (CanIf_SetControllerMode(0, CAN_CS_STARTED) == E_NOT_OK) {
		printf("error");
	}
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		///Start channel 0
	if (CanIf_SetPduMode(0, CANIF_ONLINE) == E_NOT_OK) {
		printf("error");
	}
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	printf("\nrouter COM -> CAN  . transmit& CancelTransmit functions \n");
	PduR_ComTransmit_Test();
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		///Transmit confirmation test
	CanIf_TxConfirmation(0);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		/*printf("\nrouter COM -> CANTP . transmit, Copy TX Data, TX confirmation functions and\nCancelTransmit, ChangeParameter, CancelReceive functions \n");
		PduR_ComTransmit_Test2();*/

	printf("\nrouter CANTP -> COM . StartOfReception , CopyRxData, RX indication  functions \n");
	PduR_CanTpStartOfReception_Test();
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	printf("\nrouter DCM -> CANTP . transmit, Copy TX Data, TX confirmation functions and\nCancelTransmit, ChangeParameter, CancelReceive functions \n");
	PduR_DcmTransmit_Test();

	printf("\nrouter CANTP -> DCM . StartOfReception , CopyRxData, RX indication  functions \n");
	PduR_CanTpStartOfReception_Test2();
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		///Receive indication test Can to Com
		///Create PDU message
	printf("\n CAN -> COM . RX Indication function \n");
	uint8 text[] = "mohamed";
	PduInfoType PduInfo = {
		.SduDataPtr = text,
		.SduLength = 7,
	};
	///Create mailbox
	Can_HwType Mailbox = {
		.CanId = 0,
		.Hoh = 0,
		.ControllerId = 0,
	};
	CanIf_RxIndication(&Mailbox, &PduInfo);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		///Trigger transmit indication test
	CanIf_TriggerTransmit(0, &PduInfo);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		///Controller check error test
	Can_ErrorStateType ErrorState;
	CanIf_GetControllerErrorState(0, &ErrorState);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		///Controller bus off test (can to upper layer)
	CanIf_ControllerBusOff(0);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if ( CANIF_INF_RUNTIME_PDU_CONFIGURATION == STD_ON )
	CanIf_SetDynamicTxId(0, 2);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	uint8 TransceiverId = 0;
	CanIf_SetTrcvMode(TransceiverId, CANTRCV_TRCVMODE_NORMAL);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	CanTrcv_TrcvModeType TransceiverMode;
	CanIf_GetTrcvMode(TransceiverId, &TransceiverMode);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	CanTrcv_TrcvWakeupReasonType TrcvWuReason;
	CanIf_GetTrcvWakeupReason(TransceiverId, &TrcvWuReason);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	CanIf_SetTrcvWakeupMode(TransceiverId, CANTRCV_WUMODE_ENABLE);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if (CANIF_INF_WAKEUP_SUPPORT == STD_ON)
	CanIf_CheckWakeup(0);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if (CANIF_PUBLIC_WAKEUP_CHECK_VALIDATION_SUPPORT == STD_ON)
	CanIf_CheckValidation(0);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	uint8 ControllerId = 0;
#if ( CANIF_INF_PUBLIC_TX_CONFIRMATION_POLLING_SUPPORT == STD_ON )
	CanIf_GetTxConfirmationState(ControllerId);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if (CANIF_INF_CAN_TRCV_SUPPORT == STD_ON && CANIF_PUBLIC_PN_SUPPORT == STD_ON )
	CanIf_ClearTrcvWufFlag(TransceiverId);
	CanIf_CheckTrcvWakeFlag(TransceiverId);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if(CANIF_SET_BAUDRATE_API == STD_ON)
	CanIf_SetBaudrate(ControllerId, 0);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if(CANIF_PUBLIC_ICOM_SUPPORT == STD_ON)
	CanIf_SetIcomConfiguration(ControllerId, 0);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if (CANIF_PUBLIC_PN_SUPPORT == STD_ON)
	CanIf_ConfirmPnAvailability(TransceiverId);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if (CANIF_PUBLIC_PN_SUPPORT == STD_ON)
	CanIf_ClearTrcvWufFlagIndication(TransceiverId);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if (CANIF_PUBLIC_PN_SUPPORT == STD_ON)
	CanIf_CheckTrcvWakeFlagIndication(TransceiverId);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	CanIf_ControllerModeIndication(ControllerId, CAN_CS_STARTED);
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if (CANIF_INF_CAN_TRCV_SUPPORT == STD_ON)
	CanIf_TrcvModeIndication(TransceiverId, CANTRCV_TRCVMODE_NORMAL);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#if(CANIF_PUBLIC_ICOM_SUPPORT == STD_ON)
	CanIf_CurrentIcomConfiguration(ControllerId, 0, ICOM_SWITCH_E_OK);
#endif
	//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

	printf("o_o\n");
	return 0;
}

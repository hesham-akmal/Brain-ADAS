#include "../headers/CanIf.h"
#include "../headers/CanIf_Cbk.h"
#include "../headers/PduR_CanIf.h"
#include "../headers/PduR_Cbk.h"
#include "../headers/MemMap.h"

//-----------------------------------------------------------------------------------------
/*
in: ConfigPtr Pointer to configuration parameter set, used e.g. for post build parameters

This service Initializes internal and external interfaces of the CAN Interface for the further processing.
*/

void CanIf_Init(const CanIf_ConfigType *ConfigPtr)
{
}

//-----------------------------------------------------------------------------
//initiates a transition to the requested CAN controller mode ControllerMode of the CAN controller which is as-signed by parameter ControllerId.
Std_ReturnType CanIf_SetControllerMode(uint8 ControllerId, CanIf_ControllerModeType ControllerMode)
{

    return E_NOT_OK;
}

//-----------------------------------------------------------------------------

/*
CanIfTxSduId L-SDU handle to be transmitted.This handle specifies the corresponding CAN L-SDU ID and implicitly the CAN Driver instance as
well as the corresponding CAN controller device.

CanIfTxInfoPtr Pointer to a structure with CAN L-SDU related data: DLC and pointer to CAN L-SDU buffer including the MetaData of dynamic L-PDUs.

This service initiates a request for transmission of the CAN L-PDU specified by the CanTxSduId and CAN related data in the L-SDU structure.
*/

Std_ReturnType CanIf_Transmit(PduIdType CanIfTxSduId, const PduInfoType *CanIfTxInfoPtr)
{

    return E_NOT_OK;
}

//-----------------------------------------------------------------------------
/*

in: CanIfRxSduId Receive L-SDU handle specifying the corresponding CAN L-SDU ID and implicitly the CAN Driver in-
stance as well as the corresponding CAN controller device.

out :Pointer to a structure with CAN L-SDU related data: DLC and pointer to CAN L-SDU buffer including the MetaData of dynamic L-PDUs.
return : Std_ReturnType

This service provides the CAN DLC and the received data of the requested CanIfRxSduId to the calling upper layer.

*/

Std_ReturnType CanIf_ReadRxPduData(PduIdType CanIfRxSduId, PduInfoType *CanIfRxInfoPtr)
{

    return E_NOT_OK;
}
//-------------------------------------------------------------

/*

in : Mailbox Identifies the HRH and its corresponding CAN Controller
     PduInfoPtr Pointer to the received L-PDU

This service indicates a successful reception of a received CAN Rx L-PDU to the CanIf after passing all filters and validation checks.
*/

void CanIf_RxIndication(const Can_HwType *Mailbox, const PduInfoType *PduInfoPtr)
{
}

//-----------------------------------------------------------------

/*


in : CanTxPduId L-PDU handle of CAN L-PDU successfully transmitted.This ID specifies the corresponding CAN L-PDU ID 
                and implicitly the CAN Driver instance as well as the corresponding CAN controller device.


This service confirms a previously successfully processed transmission of a CAN TxPDU.

*/

void CanIf_TxConfirmation(PduIdType CanTxPduId)
{
    
}
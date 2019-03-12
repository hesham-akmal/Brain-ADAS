#include "../headers/CanIf.h"
#include "../headers/CanIf_Cbk.h"
#include "../headers/PduR_CanIf.h"
#include "../headers/PduR_Cbk.h"
#include "../headers/Can.h"

//---------------------------------------------------------------------------

CanIf_ControllerModeType currentControllerMode;
const CanIf_ConfigType *canIf_ConfigPtr;

//-----------------------------------------------------------------------------------------
/*
in: ConfigPtr Pointer to configuration parameter set, used e.g. for post build parameters

This service Initializes internal and external interfaces of the CAN Interface for the further processing.
*/

void CanIf_Init(const CanIf_ConfigType *ConfigPtr)
{
    /** When function CanIf_Init() is called, CanIf shall initialize
        every Transmit L-PDU Buffer assigned to CanIf.
    */
    if (ConfigPtr != NULL)
    {
        canIf_ConfigPtr = ConfigPtr;
        currentControllerMode = CANIF_CS_UNINIT;
    }
    else
    {
        printf("CanIf_Init fn -> ConfigPtr = NULL")
    }

    // for(uint8 i=0; i<CANIF_INF_CAN_DRIVER_0_CONTROLER_CNT; i++){
    //     CanIf_SetPduMode(i, CANIF_OFFLINE);
    // }
}

Std_ReturnType CanIf_GetControllerMode(uint8 ControllerId, CanIf_ControllerModeType *ControllerModePtr)
{
    if (canIf_ConfigPtr == NULL || ControllerModePtr == NULL)
    {
        return E_NOT_OK;
    }
    ControllerModePtr = &currentControllerMode;
    return E_OK;
}
//-----------------------------------------------------------------------------
//initiates a transition to the requested CAN controller mode ControllerMode of the CAN controller
// which is assigned by parameter ControllerId.

Std_ReturnType CanIf_SetControllerMode(uint8 ControllerId, CanIf_ControllerModeType ControllerMode)
{

    if (ControllerMode == currentControllerMode)
    {
        printf("Already in This State");
        return E_OK;
    }

    switch (ControllerMode)
    {
    case CANIF_CS_SLEEP:
        if (currentControllerMode == CANIF_CS_STOPPED)
        {
            if (Can_SetControllerMode(Controller, CAN_T_SLEEP) == CAN_OK)
            {
                currentControllerMode = CANIF_CS_SLEEP;
                printf("current Controller mode is CANIF_CS_SLEEP");
                return E_OK;
            }
            else
            {
                return E_NOT_OK;
            }
        }
        break;

    case CANIF_CS_STARTED:
        if (currentControllerMode == CANIF_CS_STOPPED)
        {
            if (Can_SetControllerMode(Controller, CAN_T_START) == CAN_OK)
            {
                currentControllerMode = CANIF_CS_STARTED;
                printf("current Controller mode is CANIF_CS_STARTED");
                return E_OK;
            }
            else
                return E_NOT_OK;
        }
        break;

    case CANIF_CS_STOPPED:
        if (currentControllerMode == CANIF_CS_STARTED)
        {
            if (Can_SetControllerMode(Controller, CAN_T_STOP) == CAN_OK)
            {
                currentControllerMode = CANIF_CS_STOPPED;
                printf("current Controller mode is CANIF_CS_STOPPED");
                return E_OK;
            }
            else
                return E_NOT_OK;
        }
        else if (currentControllerMode == CANIF_CS_SLEEP)
        {
            if (Can_SetControllerMode(Controller, CAN_T_WAKEUP) == CAN_OK)
            {
                currentControllerMode = CANIF_CS_STOPPED;
                printf("current Controller mode is CANIF_CS_STOPPED");
                return E_OK;
            }
            else
                return E_NOT_OK;
        }
        break;

    case CANIF_CS_UNINIT:
        printf("CanIf_SetControllerMode : CANIF_CS_UNINIT case") break;
        break;

    default:
        printf("CanIf_SetControllerMode : default case") break;
    }

    return E_OK;
}

//-----------------------------------------------------------------------------

/*
CanIfTxSduId L-SDU handle to be transmitted.This handle specifies the corresponding CAN L-SDU ID and
implicitly the CAN Driver instance as well as the corresponding CAN controller device.

CanIfTxInfoPtr Pointer to a structure with CAN L-SDU related data: DLC and pointer to 
CAN L-SDU buffer including the MetaData of dynamic L-PDUs.

This service initiates a request for transmission of the CAN L-PDU specified by the CanTxSduId and CAN related 
data in the L-SDU structure.
*/

Std_ReturnType CanIf_Transmit(PduIdType CanIfTxSduId, const PduInfoType *CanIfTxInfoPtr)
{
    //check if CANIF is initialized OR currentController is not CANIF_CS_STARTED or
    if (canIf_ConfigPtr == NULL || CanIfTxInfoPtr == NULL)
        return E_NOT_OK;
    //identify CAN drv

    //determine HTH to access CAN Hardware Obj

    CanIf_PduModeType PduMode;

    CanIfTxPduCfg canIfTxPduPtr = canIf_ConfigPtr->canIfInitCfg->canIfTxPduCfg[CanIfTxSduId];

    uint8 CtrlId = canIfTxPduPtr->canIfTxPduBufferRef->canIfBufferHthRef->CanIfHthCanCtrlIdRef->canIfCtrlId;

    Can_ControllerStateType ControllerState;
    Can_PduType canPdu;

    if (CanIf_GetControllerMode(CtrlId, &ControllerState) == E_NOT_OK)
        return E_NOT_OK;

    if (ControllerState != CAN_CS_STARTED)
        return E_NOT_OK;

    if (CanIf_GetPduMode(CtrlId, &PduMode) == E_NOT_OK)
        return E_NOT_OK;

    CanIfTxPduCanIdType CanIdType = canIfTxPduPtr->CanIfTxPduCanIdType;
    if (CanIfTxInfoPtr->SduLength > 8 && (CanIdType == STANDARD_CAN || CanIdType == EXTENDED_CAN))
    {
        ///Report an error CANIF_E_DATA_LENGTH_MISMATCH to the Det_ReportError
        ///shall transmit as much data as possible and discard the rest.
        canPdu.length = 8;
    }
    else if (CanIfTxInfoPtr->SduLength > 64)
    {
        ///Report an error CANIF_E_DATA_LENGTH_MISMATCH to the Det_ReportError
        ///shall transmit as much data as possible and discard the rest.
        canPdu.length = 64;
    }
    else
    {
        canPdu.length = CanIfTxInfoPtr->SduLength;
    }

    canPdu.id = CanIfTxInfoPtr->CanIfTxPduCanId & CanIfTxInfoPtr->CanIfTxPduCanIdMask;
    canPdu.sdu = CanIfTxInfoPtr->SduDataPtr;
    canPdu.swPduHandle = CanIfTxSduId;

    if (Can_Write(canIfTxPduPtr->CanIfTxPduBufferRef->CanIfBufferHthRef->CanIfHthIdSymRef->CanObjectId, &canPdu) == CAN_OK)
        return E_OK;
    else
        return E_NOT_OK;
}

/*
in : CanTxPduId L-PDU handle of CAN L-PDU successfully transmitted.This ID specifies the corresponding CAN L-PDU ID 
                and implicitly the CAN Driver instance as well as the corresponding CAN controller device.


This service confirms a previously successfully processed transmission of a CAN TxPDU.

*/

void CanIf_TxConfirmation(PduIdType CanTxPduId)
{

    if (canIf_ConfigPtr == NULL)
    {
        printf("CanIf_TxConfirmation : The CanIf is not intialized");
        return;
    }

    if (canTxPduId > canIf_ConfigPtr->canIfInitCfg->canIfMaxTxPduCfg)
    {
        printf("CanIf_TxConfirmation : Excedded THE MAX Number of IDs");
        return;
    }

    const CanIf_TxPduCfgType *TxPduCfgPtr = canIf_ConfigPtr->canIfInitCfg->canIfTxPduCfg[CanTxPduId];

    if (TxPduCfgPtr == NULL)
    {
        printf("CanIf_TxConfirmation : TxPduCfgPtr = NULL ");
        return;
    }

    // uint8 CtrlId = TxPduCfgPtr->CanIfTxPduBufferRef->CanIfBufferHthRef->CanIfHthCanCtrlIdRef->CanIfCtrlId;

    (TxPduCfgPtr->canIfTxPduUserTxConfirmationName)(CanTxPduId, E_OK);
}

/*

in : Mailbox Identifies the HRH and its corresponding CAN Controller
     PduInfoPtr Pointer to the received L-PDU

This service indicates a successful reception of a received CAN Rx L-PDU to the CanIf after passing all filters and validation checks.
*/

static CanIfRxPduCfg *findRxPduCfg(Can_HwHandleType Hoh)
{
    for (uint32 i = 0; i != canIf_ConfigPtr->canIfInitCfg->canIfMaxRxPduCfg; ++i)
    {
        if (Hoh == canIf_ConfigPtr->canIfInitCfg->canIfRxPduCfg[i].canIfRxPduHrhIdRef->canIfHrhIdSymRef->CanObjectId)
        {
            return (CanIfRxPduCfgType *const)(&canIf_ConfigPtr->canIfInitCfg->canIfRxPduCfg[i]);
        }
    }
    return NULL;
}

void CanIf_RxIndication(const Can_HwType *Mailbox, const PduInfoType *PduInfoPtr)
{
    const CanIfRxPduCfg *RxPduCfgPtr;
    CanIf_PduModeType PduMode;
    PduIdType RxPduId;

    if (Mailbox == NULL || PduInfoPtr == NULL)
    {
        ///Report an error CANIF_E_PARAM_POINTER to the Det_ReportError
        return;
    }

    RxPduCfgPtr = findRxPduCfg(Mailbox->Hoh);

    if (RxPduCfgPtr == NULL)
    {
        ///report development error code CANIF_E_PARAM_HOH to the Det
        return;
    }

    if (PduInfoPtr->SduLength != RxPduCfgPtr->CanIfRxPduDataLength)
    {
        ///report development error code CANIF_E_INVALID_DATA_LENGTH to the Det
        return;
    }

    (RxPduCfgPtr->CanIfRxPduUserRxIndicationName)(RxPduId, PduInfoPtr);
}




}

    //-----------------------------------------------------------------

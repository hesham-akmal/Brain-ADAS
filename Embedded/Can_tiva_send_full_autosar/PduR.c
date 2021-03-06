#include "PduR_PbCfg.h"
/*
#include "Dem.h"
#include "Det.h"
*/
#if PDUR_CANIF_SUPPORT == STD_ON
#include "CanIf.h"
#endif
#if PDUR_COM_SUPPORT == STD_ON
#include "Com.h"
#endif

/* ========================================================================== */
/*                         PDUR MODULE INITIALIZATION                         */
/* ========================================================================== */

//PDUR Initial State
PduR_StateType PduRState = PDUR_UNINIT;

//Global PDUR coniguration pointer
const PduR_PBConfigType* PduRConfig;

/*
  Description:  Initialize the PDU router
  Parameters:   ConfigPtr => Pointer to post build configuration
  Return Value: Nothing
*/
void PduR_Init(const PduR_PBConfigType* ConfigPtr) {
	if (ConfigPtr == NULL) {
		PduRState = PDUR_REDUCED;
	}
	else if (PduRState != PDUR_UNINIT) {
		PduRState = PDUR_REDUCED;
	}
	else {
		PduRState = PDUR_ONLINE;
		PduRConfig = ConfigPtr;
	}
}



/**
	Description  : query global I-PDU reference in PDUR configuration (routing paths sources)
	inputs       : Pdu            | Reference to global PDU .
	output       : PduHandleIdPtr | Identifier to local I-PDU .
	I/O          : None
	return value : Std_ReturnType | Determine if I-PDU is exist or not .

Std_ReturnType PduR_INF_GetSourcePduHandleId(Pdu_Type *Pdu, PduIdType *PduHandleIdPtr) {
	Std_ReturnType Std_Ret = E_NOT_OK;

	if (PduRConfig->RoutingPaths[0] == NULL || Pdu == NULL) {
		//detect error
		return E_NOT_OK;
	}
	for (uint8_t i = 0; PduRConfig->RoutingPaths[i] != NULL; i++) {
		if (PduRConfig->RoutingPaths[i]->PduRSrcPduRef->SrcPduRef == Pdu) {
			Std_Ret = E_OK;
			*PduHandleIdPtr = PduRConfig->RoutingPaths[i]->PduRSrcPduRef->SourcePduHandleId;
		}
	}
	return Std_Ret;
}*/

/* ========================================================================== */
/*                          UPPER LAYER - COM MODULE                          */
/* ========================================================================== */

#if (PDUR_ZERO_COST_OPERATION == STD_OFF) && (PDUR_COM_SUPPORT == STD_ON)
/*
  Description:  Requests the transmission of a PDU
  Parameters:   TxPduId     => The ID of the transmitted PDU
				PduInfoPtr  => The length and data of the transmitted PDU
  Return Value: The transmission request succeded or failed
*/
Std_ReturnType PduR_ComTransmit(PduIdType TxPduId, const PduInfoType* PduInfoPtr) {
	
	return PduR_INF_RouteTransmit(TxPduId, PduInfoPtr);
}
#endif

Std_ReturnType PduR_INF_RouteTransmit(PduIdType TxPduId, const PduInfoType* PduInfoPtr) {
	Std_ReturnType result = E_OK;
	//PduIdType PduHandleId;

	//Pointer to routing paths
	PduRRoutingPath_type ** routes = PduRConfig->RoutingPaths;
	if (routes[0] == NULL) {
		//ERROR
		return E_NOT_OK;
	}

	//printf("\nPduR_INF_RouteTransmit with payload: %s", PduInfoPtr->SduDataPtr);
	//printf("\nPduR_INF_RouteTransmit with PduID: %d\n", TxPduId);
	/*
	//Query routing paths for target path
	for (uint8_t i = 0; routes[i] != NULL; i++)
		if (routes[i]->PduRSrcPduRef->SourcePduHandleId == TxPduId)
		{
			result |= CanIf_Transmit(TxPduId, PduInfoPtr);
			return result;
		}*/
	uint32 interfaceId = TxPduId & 0xF;
	if (interfaceId == CAN_IF_ID) {
		result |= CanIf_Transmit((TxPduId & (~(uint32)0xF)) >> 4, PduInfoPtr);
		return result;
	}
	return result;
}

/* ========================================================================== */
/*                          LOWER LAYER - CANIF MODULE                        */
/* ========================================================================== */

#if (PDUR_ZERO_COST_OPERATION == STD_OFF) && (PDUR_CANIF_SUPPORT == STD_ON)
/*
  Description:  CanIF module confirms the transmission of a PDU
  Parameters:   TxPduId => The ID of the transmitted PDU,
				result => Transmission result
  Return Value: Nothing
*/
void PduR_CanIfTxConfirmation(PduIdType TxPduId, Std_ReturnType result) {
	PduR_INF_TxConfirmation(TxPduId, result);
}

/*
  Description:  Indication of a received PDU from a CanIF module
  Parameters:   RxPduId     => The ID of the received PDU,
				PduInfoPtr  => The length and data of the received PDU
  Return Value: Nothing
*/
void PduR_CanIfRxIndication(PduIdType RxPduId, const PduInfoType* PduInfoPtr) {
	PduR_INF_RxIndication(RxPduId, PduInfoPtr);
}
#endif

void PduR_INF_TxConfirmation(PduIdType PduId, Std_ReturnType result) {
	//Pointer to routing paths
	PduRRoutingPath_type ** routes = PduRConfig->RoutingPaths;
	if (routes[0] == NULL) {
		//ERROR
		return;
	}

	//Query routing paths for target path
	for (uint8_t i = 0; routes[i] != NULL; i++) {
		if (routes[i]->PduRDestPduRef->DestPduHandleId == PduId) {
			PduR_INF_RouteTxConfirmation(PduId, result);
			return;
		}
	}
}
void PduR_INF_RouteTxConfirmation(PduIdType PduId, Std_ReturnType result) {
	//PduIdType PduHandleId; TTTT
	printf("PduR_INF_RouteTxConfirmation\n");

#if PDUR_COM_SUPPORT == STD_ON
	//	if (Com_INF_GetPduHandleId(route->PduRSrcPduRef->SrcPduRef, &PduHandleId) == E_OK) {
	Com_TxConfirmation(PduId, result);
	//	}
#endif
}
void PduR_INF_RxIndication(PduIdType pduId, const PduInfoType* pduInfoPtr) {

	//Pointer to routing paths
	PduRRoutingPath_type ** routes = PduRConfig->RoutingPaths;
	if (routes[0] == NULL) {
		//ERROR
		return;
	}
	//Query routing paths for target path
	for (uint8_t i = 0; routes[i] != NULL; i++) {
		if (routes[i]->PduRSrcPduRef->SourcePduHandleId == pduId) {
			PduR_INF_RouteRxIndication(pduId, pduInfoPtr);
			return;
		}
	}
}
void PduR_INF_RouteRxIndication(PduIdType pduId, const PduInfoType *PduInfo) {
	//PduIdType PduHandleId;

#if PDUR_COM_SUPPORT == STD_ON
	//if (Com_INF_GetPduHandleId(destination->DestPduRef, &PduHandleId) == E_OK) {
	Com_RxIndication(pduId, PduInfo);
	//}
#endif
#if PDUR_CANIF_SUPPORT == STD_ON


	//TTTT
	//if (CanIf_INF_GetPduHandleId(destination->DestPduRef, &PduHandleId) == E_OK) {
	Std_ReturnType retVal = CanIf_Transmit(pduId, PduInfo);
	if (retVal != E_OK) {
		//raise an error
	}
	//}
	printf("CanIf_Transmit2");


#endif
}

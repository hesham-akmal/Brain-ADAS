#include "MemMap.h"
#include "PduR_PbCfg.h"
/*
#include "Dem.h"
#include "Det.h"
*/
#if PDUR_CANIF_SUPPORT == STD_ON
//#include "CanIf.h"
#endif
#if PDUR_COM_SUPPORT == STD_ON
//#include "Com.h"
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
void PduR_Init(const PduR_PBConfigType* ConfigPtr){
  if(ConfigPtr == NULL){
    PduRState = PDUR_REDUCED;
  }
  else if(PduRState != PDUR_UNINIT){
    PduRState = PDUR_REDUCED;
  }
  else{
    PduRState = PDUR_ONLINE;
    PduRConfig = ConfigPtr;
  }
}

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
Std_ReturnType PduR_ComTransmit(PduIdType TxPduId, const PduInfoType* PduInfoPtr){
	return PduR_INF_RouteTransmit(TxPduId, PduInfoPtr);
}
#endif

Std_ReturnType PduR_INF_RouteTransmit(PduIdType TxPduId, const PduInfoType* PduInfoPtr){
	Std_ReturnType result =	E_OK;
	PduIdType PduHandleId;

    //Pointer to routing paths
    PduRRoutingPath_type ** routes = PduRConfig->RoutingPaths;
    if (routes[0] == NULL){
        //ERROR
        return E_NOT_OK;
    }
    //Query routing paths for target path
    for (uint8_t i=0 ; routes[i] != NULL ; i++){
        if ( routes[i]->PduRSrcPduRef->SourcePduHandleId == TxPduId){
#if PDUR_CANIF_SUPPORT == STD_ON
            if( CanIf_INF_GetPduHandleId(routes[i]->PduRDestPduRef->DestPduRef, &PduHandleId) == E_OK ){
                result |= CanIf_Transmit(PduHandleId, PduInfoPtr);
            }
#endif
            return result;
        }
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
void PduR_CanIfTxConfirmation(PduIdType TxPduId, Std_ReturnType result){
	PduR_INF_TxConfirmation(TxPduId, result);
}

/*
  Description:  Indication of a received PDU from a CanIF module
  Parameters:   RxPduId     => The ID of the received PDU,
                PduInfoPtr  => The length and data of the received PDU
  Return Value: Nothing
*/
void PduR_CanIfRxIndication(PduIdType RxPduId, const PduInfoType* PduInfoPtr){
	PduR_INF_RxIndication(RxPduId, PduInfoPtr);
}
#endif

void PduR_INF_TxConfirmation(PduIdType PduId, Std_ReturnType result){
    //Pointer to routing paths
    PduRRoutingPath_type ** routes = PduRConfig->RoutingPaths;
    if (routes[0] == NULL){
        //ERROR
        return;
    }

    //Query routing paths for target path
    for (uint8_t i=0 ; routes[i] != NULL ; i++){
        if ( routes[i]->PduRDestPduRef->DestPduHandleId == PduId){
            PduR_INF_RouteTxConfirmation(routes[i], result);
            return;
        }
    }
}
void PduR_INF_RouteTxConfirmation(const PduRRoutingPath_type *route, Std_ReturnType result){
    PduIdType PduHandleId;

#if PDUR_COM_SUPPORT == STD_ON
    if (Com_INF_GetPduHandleId (route->PduRSrcPduRef->SrcPduRef ,&PduHandleId) == E_OK){
		Com_TxConfirmation(PduHandleId, result);
    }
#endif
}
void PduR_INF_RxIndication(PduIdType pduId, const PduInfoType* pduInfoPtr){

  	//Pointer to routing paths
    PduRRoutingPath_type ** routes = PduRConfig->RoutingPaths;
    if (routes[0] == NULL){
        //ERROR
        return;
    }
    //Query routing paths for target path
    for (uint8_t i=0 ; routes[i] != NULL ; i++){
        if ( routes[i]->PduRSrcPduRef->SourcePduHandleId == pduId){
            PduR_INF_RouteRxIndication(routes[i]->PduRDestPduRef , pduInfoPtr);
            return;
        }
    }
}
void PduR_INF_RouteRxIndication(const PduRDestPdu_type *destination, const PduInfoType *PduInfo){
    PduIdType PduHandleId;

#if PDUR_COM_SUPPORT == STD_ON
    if (Com_INF_GetPduHandleId (destination->DestPduRef, &PduHandleId) == E_OK){
        Com_RxIndication(PduHandleId ,PduInfo);
    }
#endif
#if PDUR_CANIF_SUPPORT == STD_ON
//    if (CanIf_INF_GetPduHandleId (destination->DestPduRef ,&PduHandleId) == E_OK){
//        Std_ReturnType retVal = CanIf_Transmit(PduHandleId, PduInfo);
//        if (retVal != E_OK) {
//            //raise an error
//        }
//    }
#endif
}

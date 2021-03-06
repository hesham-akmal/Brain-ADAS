/** incomplete COM header file used as a test to PDUR module */

#ifndef COM_H_INCLUDED
#define COM_H_INCLUDED

#include "Com_Types.h"
#include "Com_PbCfg.h"

#include "PduR.h"

#include <string.h>

void Com_RxIndication(PduIdType, const PduInfoType *);
void Com_TxConfirmation(PduIdType, Std_ReturnType);
void Com_TpRxIndication(PduIdType, Std_ReturnType);
void Com_TpTxConfirmation(PduIdType, Std_ReturnType);

Std_ReturnType Com_TriggerTransmit(PduIdType, PduInfoType *);

void ComSendSignal(uint8_t PduId, uint8_t Msg[]);

BufReq_ReturnType Com_StartOfReception(PduIdType, const PduInfoType*,
	PduLengthType, PduLengthType*);
BufReq_ReturnType Com_CopyRxData(PduIdType, const PduInfoType*,
	PduLengthType*);
BufReq_ReturnType Com_CopyTxData(PduIdType, const PduInfoType*,
	RetryInfoType*, PduLengthType*);

//Std_ReturnType Com_INF_GetPduHandleId(Pdu_Type *, PduIdType *);

#endif // COM_H_INCLUDED

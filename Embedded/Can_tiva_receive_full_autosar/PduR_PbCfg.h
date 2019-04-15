#ifndef PDUR_PBCFG_H_INCLUDED
#define PDUR_PBCFG_H_INCLUDED

#include "Std_Types.h"

//Global PDU
typedef struct {
    uint32 PduLength;
}Pdu_Type;

#include "PduR.h"
#include "PduR_Types.h"

extern PduR_PBConfigType PBPduRConfig;

#define PDUR_PDU_ID_CANIF_RX_COM_MESSAGE_1      1
#define PDUR_PDU_ID_COM_TX_CANIF_MESSAGE_2      2

#endif

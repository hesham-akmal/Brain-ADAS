#include "PduR.h"
#include "Std_Types.h"

extern Pdu_Type Pdus[];

Pdu_Type Pdus[] = {
    {
        .PduLength = 8
    },
    {
        .PduLength = 8
    },
};

//PDU transmission from COM module to CANIF module
//Source (COM):
PduRSrcPdu_type PduR_Message_2_Src = {
   .SourcePduHandleId = PDUR_PDU_ID_COM_TX_CANIF_MESSAGE_2,
   .SrcPduRef = &Pdus[1]
};

//Destination (CANIF):
PduRDestPdu_type PduR_Message_2_Dest = {
   .DestPduHandleId = PDUR_PDU_ID_COM_TX_CANIF_MESSAGE_2,
   .DestPduRef = &Pdus[1]
};

//Routing path:
PduRRoutingPath_type PduRRoutingPath_Com_Tx_CanIf_Pdu_Message2 = {
   .PduRSrcPduRef = &PduR_Message_2_Src,
   .PduRDestPduRef = &PduR_Message_2_Dest
};


//PDU reception from CANIF module to COM module
//Source (CANIF):
PduRSrcPdu_type PduR_Message_1_Src = {
   .SourcePduHandleId = PDUR_PDU_ID_CANIF_RX_COM_MESSAGE_1,
   .SrcPduRef = &Pdus[0]
};

//Destination (COM):
PduRDestPdu_type PduR_Message_1_Dest = {
   .DestPduHandleId = PDUR_PDU_ID_CANIF_RX_COM_MESSAGE_1,
   .DestPduRef = &Pdus[0]
};

//Routing path:
PduRRoutingPath_type PduRRoutingPath_CanIf_Rx_Com_Pdu_Message1 = {
   .PduRSrcPduRef = &PduR_Message_1_Src,
   .PduRDestPduRef = &PduR_Message_1_Dest
};

PduRRoutingPath_type * RoutingPaths[] = {
   &PduRRoutingPath_Com_Tx_CanIf_Pdu_Message2,
   &PduRRoutingPath_CanIf_Rx_Com_Pdu_Message1,
   NULL
};

PduR_PBConfigType PBPduRConfig = {
    .PduRConfigurationId = 0,
    .PduRMaxRoutingPathCnt = 2,
    .RoutingPaths = RoutingPaths
};

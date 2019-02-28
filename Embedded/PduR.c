#include <stdlib.h>
#include <string.h>
#include "Det.h"

/* @req PDUR232 */
#if defined(USE_DEM)
#include "Dem.h"
#endif
#include "PduR.h"
#include "debug.h"


#if !(((PDUR_SW_MAJOR_VERSION == 1) && (PDUR_SW_MINOR_VERSION == 2)) )
#error PduR: Expected BSW module version to be 1.2.*
#endif


/* @req PDUR0774 */
#if !(((PDUR_AR_RELEASE_MAJOR_VERSION == 4) && (PDUR_AR_RELEASE_MINOR_VERSION == 0)) )
#error PduR: Expected AUTOSAR version to be 4.0.*
#endif


/*
 * The state of the PDU router.
 */

/* @req PDUR644 */
/* @req PDUR325 */
PduR_StateType PduRState = PDUR_UNINIT;


#if PDUR_ZERO_COST_OPERATION == STD_OFF

const PduR_PBConfigType * PduRConfig;

/*
 * Initializes the PDU Router.
 */
void PduR_Init (const PduR_PBConfigType* ConfigPtr) {

	//Enter(0);

	/* !req PDUR106 */
	/* !req PDUR709 */

	// Make sure the PDU Router is uninitialized.
	// Otherwise raise an error.
	if (PduRState != PDUR_UNINIT) {
		// Raise error and return.
		PDUR_DET_REPORTERROR(MODULE_ID_PDUR, PDUR_INSTANCE_ID, 0x00, PDUR_E_INVALID_REQUEST);
	}

	/* @req PDUR0776 */
	else if (ConfigPtr == NULL) {
		PDUR_DET_REPORTERROR(MODULE_ID_PDUR, PDUR_INSTANCE_ID, 0x00, PDUR_E_NULL_POINTER);
	} else {
		PduRConfig = ConfigPtr;

		// Start initialization!
		DEBUG(DEBUG_LOW,"--Initialization of PDU router--\n");

		//uint8 failed = 0;

        // Initialize buffers
        /* @req PDUR308 */
        if (PduRConfig->DefaultValues != NULL && PduRConfig->DefaultValueLengths != NULL) {
            for (uint32 i = 0u; i < PduR_RamBufCfg.NTxBuffers; i++) {
                if (*PduRConfig->DefaultValueLengths[i] > 0u) {
                    memcpy(PduR_RamBufCfg.TxBuffers[i], PduRConfig->DefaultValues[i], *PduRConfig->DefaultValueLengths[i]);
                }
            }
        }

        // The initialization succeeded!

        /* @req PDUR326 */
        PduRState = PDUR_ONLINE;
        DEBUG(DEBUG_LOW,"--Initialization of PDU router completed --\n");
	}

}

/* @req PDUR764 */
#if (PDUR_ZERO_COST_OPERATION == STD_OFF) && (PDUR_CANIF_SUPPORT == STD_ON)

// Autosar4 API

void PduR_CanIfRxIndication(PduIdType pduId, PduInfoType* pduInfoPtr) {
	PduR_LoIfRxIndication(pduId, pduInfoPtr, 0x01);
}

void PduR_CanIfTxConfirmation(PduIdType pduId) {
	PduR_LoIfTxConfirmation(pduId, 0x02);
}

#endif


/* @req PDUR764 */
#if (PDUR_ZERO_COST_OPERATION == STD_OFF) && (PDUR_COM_SUPPORT == STD_ON)

Std_ReturnType PduR_ComTransmit(PduIdType pduId, const PduInfoType* pduInfoPtr) {
	return PduR_UpTransmit(pduId, pduInfoPtr, 0x89);
}

#endif

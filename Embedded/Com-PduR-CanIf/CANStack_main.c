#include <stdio.h>
#include <stdlib.h>

#include "Com.h"
#include "PduR.h"
#include "CanIf.h"

int main() {
	/*
	Initialize all the modules
	*/
	PduR_Init(&PBPduRConfig);
	CanIf_Init(&canIf_Config);

	//assuming msgId = 7, hth = 0, driverId = 1, interfacId = 2
	//msgId: 11 bits, hth: 8 bits, driverId: 4 bits, interfaceId: 4 bits
	uint32 Id = ((uint32)7 << 16) | ((uint32)0 << 8) | ((uint32)1 << 4) | 2;
	ComSendSignal(Id, "LMFAO");

	return 0;
}

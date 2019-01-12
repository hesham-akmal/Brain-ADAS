 #!/bin/bash
for (( COUNTER=280; COUNTER>0; COUNTER-=20 )); do
    echo $COUNTER
    python allElectrodesDiffmsTraining.py $COUNTER > "resultsOF_${COUNTER}_ColperElectrodeAllPCAs.txt"
done


#!/bin/bash
# Invoke as: generate.sh <book directory>

CALABASH_HOME="../calabash-0.9.41/"

JAVA_CP="$CALABASH_HOME/calabash.jar:."
for file in "$CALABASH_HOME/lib/"*; do 
    JAVA_CP="$file:$JAVA_CP"
done

java -classpath "$JAVA_CP" com.xmlcalabash.drivers.Main --debug --with-param book_directory="$1" ./bookmaker.xpl

#!/bin/bash
# Invoke as: generate.sh <book directory>

PANDOC_ARGS="-f markdown --html5 --section-divs"
CALABASH_HOME="../calabash-0.9.41/"

JAVA_CP="$CALABASH_HOME/calabash.jar:."
for file in "$CALABASH_HOME/lib/"*; do 
    JAVA_CP="$file:$JAVA_CP"
done

pandoc $PANDOC_ARGS "$1/book.md" | java --classpath "$JAVA_CP" com.xmlcalabash.drivers.Main ./bookmaker.xpl

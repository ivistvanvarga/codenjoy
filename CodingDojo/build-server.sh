#!/bin/bash
export ROOT=$(pwd)

export GAMES_TO_RUN=tetris,snake,bomberman

if [[ "${GAMES_TO_RUN}" == "" ]] ; then 
    ${ROOT}/mvnw clean install -DskipTests
    
    cd ${ROOT}/server
    ${ROOT}/mvnw clean package -DskipTests -DallGames
 else 
    cd ${ROOT}/games
    ${ROOT}/mvnw clean install -N
    
    cd ${ROOT}/games/engine
    ${ROOT}/mvnw clean install -DskipTests
    
    for a in $(echo ${GAMES_TO_RUN} | sed -e 's/,/ /g'); do
        cd ${ROOT}/games/${a}
        ${ROOT}/mvnw clean install -DskipTests
    done
    
    cd ${ROOT}/server
    ${ROOT}/mvnw clean package -DskipTests -P${GAMES_TO_RUN}
fi


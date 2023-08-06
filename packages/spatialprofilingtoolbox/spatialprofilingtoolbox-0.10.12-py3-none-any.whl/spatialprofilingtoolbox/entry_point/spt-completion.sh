#!/bin/bash

_spt_completions()
{
    if [[ "${#COMP_WORDS[@]}" -eq "2" ]]; then
        COMPREPLY=($(compgen -W "control countsserver db workflow" "${COMP_WORDS[1]}"));
    else
        if [[ "${#COMP_WORDS[@]}" -eq "3" ]]; then
            case ${COMP_WORDS[1]} in
                control)
                    COMPREPLY=($(compgen -W "configure guess-channels report-on-logs" "${COMP_WORDS[2]}"));
                ;;
                countsserver)
                    COMPREPLY=($(compgen -W "cache-expressions-data-array start" "${COMP_WORDS[2]}"));
                ;;
                db)
                    COMPREPLY=($(compgen -W "create-schema modify-constraints" "${COMP_WORDS[2]}"));
                ;;
                workflow)
                    COMPREPLY=($(compgen -W "aggregate-core-results core-job extract-compartments generate-run-information initialize merge-performance-reports merge-sqlite-dbs report-run-configuration" "${COMP_WORDS[2]}"));
                ;;
            esac
        fi
    fi
}

complete -F _spt_completions spt
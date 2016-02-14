SCRIPT_NAME=${0##*/}

export LC_ALL=C
export PATH="/usr/sbin:/usr/bin:/sbin:/bin"

# The return values of a plugin.
CODE_OK=0
CODE_WARNING=1
CODE_CRITICAL=2
CODE_UNKNOWN=3

if ! TEMP=$(getopt -o 'p' -l 'print-exit-code' -n "$SCRIPT_NAME" -- "$@")
then
    echo "Syntax error with $SCRIPT_NAME command." >&2
    exit "$CODE_UNKNOWN"
fi

eval set -- "$TEMP"
unset TEMP

PRINT_EXIT_CODE='false'

while true
do
    case "$1" in

        --print-exit-code|-p)
            PRINT_EXIT_CODE='true'
            shift 1
        ;;

        --)
            shift 1
            break
        ;;

    esac
done

end () {
    local exit_code="$1"
    shift
    "$PRINT_EXIT_CODE" && printf '%s\n' "$exit_code"
    printf "$@"
    exit "$exit_code"
}



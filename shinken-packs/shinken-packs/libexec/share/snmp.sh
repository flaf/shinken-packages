# Variables and functions from the specific script:
#
#   - SCRIPT_NAME
#   - SCRIPT_DIRECTORY
#   - SPECIFIC_SHORT_OPTION
#   - SPECIFIC_LONG_OPTION
#   - SPECIFIC_SYNOPSIS
#   - GET_SPECIFIC_OPTIONS (this is a function)
#
# Convention: all the variables defined here are in upper case.
#
# Variables defined here and useful to the specific script:
#
#   - SNMP_CMD_OPTIONS
#   - HOSTNAME
#   - CODE_{OK,WARNING,CRITICAL,UNKWNOWN}
#
# No check options for performance reasons.

export LC_ALL=C
export PATH='/usr/sbin:/usr/bin:/sbin:/bin'

# The return values of a plugin.
CODE_OK=0
CODE_WARNING=1
CODE_CRITICAL=2
CODE_UNKNOWN=3

COMMON_SYNOPSIS="(--v2c -C <community> | -l <login> -x <passwd> -X <privpass> -L <authproto>,<privproto>) [-t <timeout>] [-r <retries>] -H <hostname>"
COMMON_SHORT_OPTIONS='h,C:,l:,x:,X:,L:,t:,r:,H:'
COMMON_LONG_OPTIONS='help,community:,login:,passwd:,privpasswd:,protocols:,timeout:,retries:,hostname:'

print_help () {
    cat <<EOF
The syntax is:
    $SCRIPT_NAME --help
    $SCRIPT_NAME $COMMON_SYNOPSIS $SPECIFIC_SYNOPSIS
EOF
}

if ! TEMP=$(getopt -o "$COMMON_SHORT_OPTIONS,$SPECIFIC_SHORT_OPTIONS" \
                   -l "$COMMON_LONG_OPTIONS,$SPECIFIC_LONG_OPTIONS"   \
                   -n "$SCRIPT_NAME" -- "$@")
then
    echo "Syntax error with $SCRIPT_NAME command." >&2
    print_help
    exit "$CODE_UNKNOWN"
fi

eval set -- "$TEMP"
unset TEMP

# Default value for the options which are not mandatory.
SNMP_VERSION='' # default is not 'v2c', then v3
SNMP_TIMEOUT=10
SNMP_RETRIES=1

while true
do
    case "$1" in
        --v2c)
            SNMP_VERSION="2c"
            shift 1
        ;;

        --community|-C)
            SNMP_COMMUNITY="$2"
            shift 2
        ;;

        --login|-l)
            SNMP_LOGIN="$2"
            shift 2
        ;;

        --passwd|-x)
            SNMP_PASSWD="$2"
            shift 2
        ;;

        --privpasswd|-X)
            SNMP_PRIVPASSWD="$2"
            shift 2
        ;;

        --protocols|-L)
            SNMP_AUTH_PROTO=$(echo "$2" | cut -d"," -f1)
            SNMP_PRIV_PROTO=$(echo "$2" | cut -d"," -f2)
            shift 2
        ;;

        --timeout|-t)
            SNMP_TIMEOUT="$2"
            shift 2
        ;;

        --retries|-r)
            SNMP_RETRIES="$2"
            shift 2
        ;;

        --hostname|-H)
            HOSTNAME="$2"
            shift 2
        ;;

        --help|-h)
            print_help
            exit "$CODE_OK"
        ;;

        --)
            shift 1
            break
        ;;

        *)
            GET_SPECIFIC_OPTIONS "$1" "$2" || shift "$?"
        ;;
    esac
done

# The timemout of snmpcmd commands is not a global timeout :
#
#   o<----timeout---->o<----timeout---->o<----timeout---->|
#
# 'o' is a SNMP request. Here, number of retries is 2,
# so there is 3 SNMP requests (1 request + 2 retries).
SNMP_TIMEOUT=$((SNMP_TIMEOUT/(SNMP_RETRIES+1)))
if [ "$SNMP_TIMEOUT" -lt 2 ]
then
    echo "Number of retries is too high compared to the global timeout. Check aborted."
    exit "$CODE_UNKNOWN"
fi

# Options used in the snmp* commands.
SNMP_CMD_OPTIONS="-r $SNMP_RETRIES -t $SNMP_TIMEOUT"
if [ "$SNMP_VERSION" = "2c" ]
then
    SNMP_CMD_OPTIONS="$SNMP_CMD_OPTIONS -v 2c -c $SNMP_COMMUNITY"
else
    SNMP_CMD_OPTIONS="$SNMP_CMD_OPTIONS -v 3 -u $SNMP_LOGIN -l authPriv -A $SNMP_PASSWD -a $SNMP_AUTH_PROTO -X $SNMP_PRIVPASSWD -x $SNMP_PRIV_PROTO"
fi



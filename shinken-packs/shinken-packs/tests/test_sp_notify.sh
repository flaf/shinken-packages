#!/bin/sh

script_dir="${0%/*}"
sp_notify_bin=$(readlink -f "$script_dir/../bin/sp_notify")

blacklist=$(mktemp)

cat > "$blacklist" <<'EOF'

# A comment...
    # Another comment...
bad line...

!^lafont$:.*:^reboot$:[00h00;23h59]:[3,4,5,6,7]


EOF

# Just print, no message is sent.
"$sp_notify_bin" by-email --print-only         \
    --contact-name='bob'                       \
    --black-list="$blacklist"                  \
    --host-name='srv-1'                        \
    --host-address='172.31.10.10'              \
    --service-description='reboot'             \
    --notification-type='PROBLEM'              \
    --state='CRITICAL'                         \
    --business-impact='3'                      \
    --additional-info='The host has rebooted.' \
    --notification-number='3'                  \
    --rarefaction-threshold='10'               \
    --contact-email='bob@dom.tld'              \
    --contact-number='0676553219'              \
    --sms-threshold='4'                        \
    --sms-url='http://foo/sms/'

rm "$blacklist"



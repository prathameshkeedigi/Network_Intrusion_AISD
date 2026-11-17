#!/bin/bash
# Benign background traffic from the INNOCENT user 10.10.10.3 (a normal user, NOT an attacker).
# It only browses the web server and logs in over SSH, exactly like run_normal.sh,
# but bound to source address 10.10.10.3 so the detector sees a second, legitimate source.
# usage: ./innocent.sh 700        (seconds to run)
T=10.10.10.2
SRC=10.10.10.3
D=${1:-700}
end=$(( $(date +%s) + D ))
echo "[$(date +%T)] innocent user $SRC -> $T for $D s"
while [ $(date +%s) -lt $end ]; do
  case $((RANDOM % 3)) in
    0) curl -s --interface $SRC -o /dev/null http://$T/ 2>/dev/null ;;
    1) curl -s --interface $SRC -o /dev/null http://$T/page$RANDOM.html 2>/dev/null ;;
    2) sshpass -p 'Summer2024' ssh -b $SRC -o StrictHostKeyChecking=no -o ConnectTimeout=5 victim@$T 'uptime' >/dev/null 2>&1 ;;
  esac
  sleep $(( RANDOM % 3 + 1 ))
done
echo "[$(date +%T)] INNOCENT DONE"

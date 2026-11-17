#!/bin/bash
# usage: ./run_normal.sh 600   (seconds)
T=10.10.10.2; D=${1:-600}
worker(){
  end=$(( $(date +%s) + D ))
  while [ $(date +%s) -lt $end ]; do
    case $((RANDOM % 3)) in
      0) curl -s -o /dev/null http://$T/ ;;
      1) curl -s -o /dev/null http://$T/page$RANDOM.html ;;
      2) sshpass -p 'Summer2024' ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 victim@$T 'ls -la; uptime' >/dev/null 2>&1 ;;
    esac
    sleep $(( RANDOM % 3 + 1 ))
  done
}
echo "[$(date +%T)] normal-only traffic for $D s (3 workers)"
worker & worker & worker & wait
echo "NORMAL FINISHED"

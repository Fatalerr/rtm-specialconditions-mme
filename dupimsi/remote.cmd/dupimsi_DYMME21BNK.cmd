ZDDS:MMDU,0;
solsql -e 'select imsi_string from subscriber where RA_ACCESS_TYPE=3' -a 'tcp 169.254.255.1 2315' subscriber root > MMDU0.txt;sleep 2
solsql -e 'select imsi_string from subscriber where RA_ACCESS_TYPE=3' -a 'tcp 169.254.255.2 2325' subscriber root > MMDU1.txt;sleep 2
echo '*****MMDU-0*****';cat MMDU0.txt;sleep 2
echo '*****MMDU-1*****';cat MMDU1.txt;sleep 2
exit
ZDDS:MMDU,2;
solsql -e 'select imsi_string from subscriber where RA_ACCESS_TYPE=3' -a 'tcp 169.254.255.6 2315' subscriber root > MMDU2.txt;sleep 2
solsql -e 'select imsi_string from subscriber where RA_ACCESS_TYPE=3' -a 'tcp 169.254.255.7 2325' subscriber root > MMDU3.txt;sleep 2
echo '*****MMDU-2*****';cat MMDU2.txt;sleep 2
echo '*****MMDU-3*****';cat MMDU3.txt;sleep 2
exit
ZDDS:MMDU,4;
solsql -e 'select imsi_string from subscriber where RA_ACCESS_TYPE=3' -a 'tcp 169.254.255.9 2315' subscriber root > MMDU4.txt;sleep 2
solsql -e 'select imsi_string from subscriber where RA_ACCESS_TYPE=3' -a 'tcp 169.254.255.10 2325' subscriber root > MMDU5.txt;sleep 2
echo '*****MMDU-4*****';cat MMDU4.txt;sleep 2
echo '*****MMDU-5*****';cat MMDU5.txt;sleep 2
exit


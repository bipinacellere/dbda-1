num1=$1
num2=$2
while [ $num1 <= $num2 ]
do
	echo "$num1 "
	num1=$(($num1+1))
done

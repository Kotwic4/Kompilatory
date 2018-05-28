a = 1 + 2;
b = a + 1;
print b, a;

print b;
b -= 1;
print b;

c = [1, 2; 3, 4];

print c';

print zeros(5);

print - 6;

print c[1, 1];

if (a == 2)
print "ala";
else{
  print "ola";
}

if (a > 2)
print "ela";


print "tutaj";

i = 0;
while (i < 10){
  i += 1;
  if (i == 3)
  continue;
  print i;
  if (i == 4)
  return i;
}

print "tutaj tez";

i = 9;
print i;

for i = 1 : 5 {
  for j = i : 5 {
    print i, j;
  }
}

print i;

A = ones(5);
B = eye(5);
D1 = B ./ A';
print D1';

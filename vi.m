function [ key ] = vi( cipher )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
[freq,relfreq]=zfrequency(cipher);
temp = [];
key = [];
size = -2;
keylength = 5;
sum = 0;
for i=1:26
      sum = sum + freq(i) * (freq(i) - 1); 
end
freq
sum
length(cipher)
sum = sum  / length(cipher) / (length(cipher)-1)
swq = (0.067 - 0.0385) / (sum  - 0.0385)
str = '';
key_length = 5
for i=1:key_length
    counter = 0;
    str = '';
    while ((counter+i) <= length(cipher))
        str = [str cipher(counter+i)];
        counter = counter + keylength;
        
        
    end
    [freq,relfreq]=zfrequency(str);
    greatest = 0;
    index = -2;
    for j = 1:26
        if (freq(j) > greatest)
            greatest = freq(j);
            index = j;
        end
    end
    key(i) = mod((index - 5),26)
end



end


function [ key ] = Vigenere_cipher( cipher )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
temp = [];
key = [];
size = -2;
keylength = 0;
%First find the length of the key
for i=1:length(cipher)
      temp=[temp; i coinc(cipher,i)];
       if (size <  coinc(cipher,i))
           keylength = i;
           size = coinc(cipher,i);
       end
           
end
str = '';
key_length = keylength;
%Now use frequency to find out keys
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
    % E is the most common letter in english
    key(i) = mod((index - 4),26);
    
end



end


Problem 4 

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




Vigenere_cipher(ciphertext1)

ans =

    13    20    19     6    10     8    13     5    19     5    10     4

Vigenere_cipher(ciphertext2)

ans =

  Columns 1 through 14

     2    21    13    20     7    22     3     2    16    18    20    18    11    11

  Columns 15 through 28

    13     6    18     4    18    25    11     3    24     4     3     8     6    22

  Columns 29 through 35

    18    21    19    20    21     6    16

Vigenere_cipher(ciphertext3)

ans =

  Columns 1 through 14

     9     8     4     0     0    14    20     8    19     1    11     0    17    23

  Columns 15 through 28

     7    20     8     4    13    17     3    20    18    19     6     5     0     0

  Columns 29 through 42

     7     4     4     0     7    13    23     4     5     7     4     1    23     0

Vigenere_cipher(ciphertext4)

ans =

    10    10     8    11    23    16     7     8     3    12     2

diary off



Problem 5
In the lecture, we discussed the possibility that any two randomly chosen source-language letters are the same(0.067) and the probability of a coincidence for a uniform random selection from the alphabet is 1/26 - 0.0385.  For this problem, the method we talked from lecture would still work. It is just that the probability that any two random chosen source-language letters are gonna be different and the probability of a coincidence for a uniform random selection from the language is going to be different as well.  These two numbers are going to be different from English because they have a population relative frequency of 0.05, 0.20,0.25, 0.35, 0.15.

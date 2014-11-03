function [plaintext,Key]=crackhill(knownplaintextsnippet,ciphertext,blocklength)

temp=block(knownplaintextsnippet,1,blocklength)-97; 
[rows,cols]=size(temp); %get row and column
booleanInvert=0; % boolean to see if we have found the inverse of plaintext.
while booleanInvert==0                                  
    indices=ceil((cols-1)*rand(1,blocklength)) ;
    M=temp(:,indices);
    d=det(M);
    d=round(d);
    if ~[mod(d,2)==0 | mod(d,13)==0]            %check if we can the inverse matrix of plaintext
        booleanInvert=1;
    end
end

Ci=block(ciphertext,1,blocklength)-97;
C=Ci(:,indices);

recipd=powermod(d,-1,26);     
invM=inv(M);
invM=recipd*d*invM;
invM=round(invM);
invM=mod(invM,26);          
Key=mod(C*invM,26);         

dKey=det(Key);            
dKey=round(dKey);
recipdKey=powermod(dKey,-1,26);
invKey=inv(Key);
invKey=recipdKey*dKey*invKey;
invKey=round(invKey);
invKey=mod(invKey,26);       %Find the inverse of the key

MM=char(mod(invKey*Ci,26)+97);   % use the found Key to decrypt ciphertext
plaintext=block(MM,-1,blocklength);


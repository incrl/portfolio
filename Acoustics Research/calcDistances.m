function [ Rd, Ri ] = calcDistances( x,y,zMin,zMax,dist,micPositions )
%CalcDistances Calculate the distances between the sources and the rig

sources = zMin:dist:zMax;

[~,numSources] = size(sources);
[rows,columns,~] = size(micPositions);

%Preallocation
Rd = zeros(rows,columns,numSources);
Ri = zeros(rows,columns,numSources);

%Get coordinates of microphone
x2 = micPositions(:,:,1);
y2 = micPositions(:,:,2);
z2 = micPositions(:,:,3);

x1 = x;
y1 = y;

%Caculate the Rd and Ri values
for s = 1:numSources
    
    %Get coordinates of source
    z1 = sources(s);
    
    %Determine the Magnitude of Rd for all positions on the rig
    %given the position of the source;
    Rd(:,:,s) = sqrt((x2-x1).^2 + (y2-y1).^2 + (z2-z1).^2);
    
    %Determine the Magnitude of Ri where y1 is negative
    Ri(:,:,s) = sqrt((x2-x1).^2 + (y2+y1).^2 + (z2-z1).^2);
    
end


end


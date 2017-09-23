function [ measurement ] = simulation(sourcesU,sourcesC,micPositions,k)
%simulation Simulation of a microphone measurement
%   Use this function to simulate what the microphone
% array, defined by micPostions, would pick up with given uncorrelated
% and uncorrelated sources

[sizeU,~] = size(sourcesU);
[sizeC,~,numf] = size(sourcesC);
[rows,columns,~] = size(micPositions);

pLevelU = zeros(rows,columns,numf);
pLevelC = zeros(rows,columns,numf);
measurement = zeros(rows,columns);

%How far up the nozzle is used in the calculation
inset = -20;

%The threshold for calculated sources
threshold = 0.01;
limitU = threshold*max(sourcesU(:,4));
limitC = threshold*max(abs(sourcesC(:,4)));

%Calculate the square of the pressures

for r = 1:rows
    for c = 1:columns
        
        %Get coordinates of microphone
        x2 = micPositions(r,c,1);
        y2 = micPositions(r,c,2);
        z2 = micPositions(r,c,3);
        
        for s = 1:sizeU
            
            if sourcesU(s,4) > limitU
                
                %Get coordinates of source
                x1 = sourcesU(s,1);
                y1 = sourcesU(s,2);
                z1 = sourcesU(s,3);
                
                %Check to make sure the source is not inside the jet plume
                if z1 >= inset
                    %Determine the Magnitude of Rd
                    Rd = sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2);
                    
                    %Determine the Magnitude of Ri where y1 is negative
                    Ri = sqrt((x2-x1)^2 + (y2+y1)^2 + (z2-z1)^2);
                    
                    
                    %Calculate Pressure Uncorrelated by equation 5. This is
                    %done separately for each frequency
                    %sourcesU(s,4) = Amplitude and sourcesU(s,5) = Q
                    for f = 1:numf
                        pLevelU(r,c,f) = pLevelU(r,c,f) + abs(sourcesU(s,4)*...
                            (exp(-1i*k(f)*Rd)/Rd + sourcesU(s,5) *...
                            exp(-1i*k(f)*Ri)/Ri))^2;
                    end
                end
            end
        end
        
        
        
        for s = 1:sizeC
            
            if abs(sourcesC(s,4)) > limitC
                
                %Get coordinates of source
                x1 = sourcesC(s,1);
                y1 = sourcesC(s,2);
                z1 = sourcesC(s,3);
                
                %Check to make sure the source is not inside the jet plume
                if z1 >= inset
                    %Determine the Magnitude of Rd
                    Rd = sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2);
                    
                    %Determine the Magnitude of Ri where y1 is negative
                    Ri = sqrt((x2-x1)^2 + (y2+y1)^2 + (z2-z1)^2);
                    
                    %Calculate Pressure Correleated by equation 8
                    %sourcesC(s,4) = amplitude, sourcesC(s,5) = Q
                    for f = 1:numf
                        pLevelC(r,c,f) = pLevelC(r,c,f) + (sourcesC(s,4)*...
                            (exp(-1i*k(f)*Rd)/Rd + sourcesC(s,5)...
                            * exp(-1i*k(f)*Ri)/Ri));
                    end
                end
            end
        end
    end
end

%Square the Correlated Pressure
pLevelC = abs(pLevelC).^2;

%Total Pressure Levels summed over frequency
measurement = sum(pLevelU,3) + sum(pLevelC,3);

end

% %Tests used when comparing to Jessica Morgan's Code
% save('ComparisonU.mat');



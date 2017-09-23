function [ measurement ] = simulation_opt(sourcesU,sourcesC,Rd,Ri,k)
%simulation Simulation of a microphone measurement
%   Use this function to simulate what the microphone
% array, defined by micPostions, would pick up with given uncorrelated
% and uncorrelated sources

[sizeU,~] = size(sourcesU);
[sizeC,~,numf] = size(sourcesC);
[rows,columns,~] = size(Rd);

%Preallocation
pLevelU = zeros(rows,columns,numf);
pLevelC = zeros(rows,columns,numf);

%The threshold for calculated sources
threshold = 0.01;
limitU = threshold*max(sourcesU(:,4));
limitC = threshold*max(abs(sourcesC(:,4)));

%Split ups for ease of processing
%sourcesU(:,4) = Amplitude and sourcesU(:,5) = Q
AuList = sourcesU(:,4);
QuList = sourcesU(:,5);
AcList = sourcesC(:,4);
QcList = sourcesC(:,5);


%For right now, assume that the correlated and uncorrelated
%sources are in the same spot
for s = 1:sizeU
    
    Au = AuList(s);
    Qu = QuList(s);
    Ac = AcList(s);
    Qc = QcList(s);
    
    for f = 1:numf
        %processing optimization
        kf = k(f);
        
        %Calculate Pressure Uncorrelated by equation 5. This is
        %done separately for each frequency
        if Au > limitU
            pLevelU(:,:,f) = pLevelU(:,:,f) + abs(Au*...
                (exp(-1i*kf*Rd(:,:,s))./Rd(:,:,s) + Qu*...
                exp(-1i*kf*Ri(:,:,s))./Ri(:,:,s))).^2;
        end
        if abs(Ac) > limitC
            pLevelC(:,:,f) = pLevelC(:,:,f) + (Ac*...
                (exp(-1i*kf*Rd(:,:,s))./Rd(:,:,s) + Qc *...
                exp(-1i*kf*Ri(:,:,s))./Ri(:,:,s)));
        end
    end
end

%Sum up over the sources
pLevelC = abs(pLevelC).^2;

%Total Pressure Levels summed over frequency
measurement = sum(pLevelU,3) + sum(pLevelC,3);

end

% %Tests used when comparing to Jessica Morgan's Code
% save('ComparisonU.mat');



close all;

%Error Function Type
err = 1;

%Data of interest
freq = 800;
eng = 3;
plane = 2;

load(['BOA Results\BOA_Results_plane_',num2str(plane),'_engcond_',...
    num2str(eng),'_freq_',num2str(freq),'.mat']);

%Plane of interest
planeTemp = 4;

%Load the microphone array
temp = load('F22Holloman2009Geometry7.mat');
micPositionsTemp = temp.F22Geometry{1,planeTemp};

%Load the measurements
[measurementsTemp,~] = loadData(eng_cond,planeTemp,fc,'data\');

%Plot the Rayleigh Distrbutions
plotDistribution(sourcesU,sourcesC);

%simulate measurement
solution = simulation(sourcesU,sourcesC,micPositionsTemp,k);

%Calculate Sound Pressure Levels
SPLctemp = takeSPL(solution,Pref);

%Match the two SPL's to each other according to the 100th percentile
SPLtemp = matchSPL(SPLctemp, measurementsTemp, 1);
          

[errorMap, errorTotal] = errorFunction(SPLtemp,measurementsTemp,Pref,15,err);

errorTotal

plotSPL(SPLtemp,micPositionsTemp,'Caculated SPL')

plotSPL(measurementsTemp,micPositionsTemp,'Measured SPL')

figure('Color',[1,1,1])
pcolor(micPositionsTemp(:,:,3),micPositionsTemp(:,:,2),errorMap);
shading interp
axis image
caxis([0,10])
colorbar
title('Error Map')

clear planeTemp temp micPositionsTemp measurmentsTemp solution SPLctemp SPLtemp errorMap
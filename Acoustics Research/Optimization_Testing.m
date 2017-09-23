clear all;
close all;

%Equivalent Source Method
close all
clear all

%Select plane number,engine condition, and octave band
plane = 2;
eng_cond = 4;
f = 315;

%Load the microphone array
temp = load('F22Holloman2009Geometry7.mat');
micPositions = temp.F22Geometry{1,plane};

%Load the measurements
[measurements,fc,angle] = loadData(eng_cond,plane,f,'data\');

%set reference mics pressure
Pref = 20 * 10^(-6);

%set Speed of Sound in m/s
c = 343;

%error function type. 0 = Jessica Morgans, 1 = Least Squares
err = 0;

%set the low and high frequency bounds in the third octave band in Hz
flow = fc/(2^(1/6));
fhigh = fc*2^(1/6);
%These values are for a 315 center frequency

%Set the number of frequencies in the third octave band
nf = 10;

%Calculate the third octave band based on a logarithmic spacing.
freqs = logspace(log10(flow), log10(fhigh), nf);

%calculate wavenumber
k = 2 * pi * freqs/c;

%the distance between monopole sources in meters
dist = .02;

%number of monopole sources
n = 400;

zMin = -2;
zMax = 8;

[Rd,Ri] = calcDistances(0,2.1,zMin,zMax,dist,micPositions);

errorDiff = zeros(100,1);

%set initial guesses for sources
zpU = 2.2;
zpC = 2.2;
sdU = 1.7;
sdC = 1.7;
AmaxU = 1;
AmaxC = .6;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Unoptimized Result%%%%%%%%%%%%%%%%%%%%%%%%%%%
%initialize monopole sources
[sourcesU1,sourcesC1] = initSources(0,2.1,zpU,sdU,AmaxU,zpC,sdC,AmaxC,n,...
    dist,angle,freqs,c);

%initialize monopole sources
[sourcesU2,sourcesC2] = initSources_opt(0,2.1,zpU,sdU,AmaxU,zpC,sdC,AmaxC,zMin,zMax,...
    dist,angle,freqs,c);


%Plot the Rayleigh Distrbutions
%plotDistribution(sourcesU1,sourcesC1);
%plotDistribution(sourcesU2,sourcesC2);
%pause

%simulate measurement
tic;
solution1 = simulation(sourcesU1,sourcesC1,micPositions,k);
toc
%Calculate Sound Pressure Levels
SPLc1 = takeSPL(solution1,Pref);

%Match the two SPL's to each other according to the 100th percentile
SPL1 = matchSPL(SPLc1, measurements, 1);


[~, errorTotal1] = errorFunction(SPL1,measurements,Pref,25,err);


%simulate measurement
tic;
solution2 = simulation_opt(sourcesU2,sourcesC2,Rd,Ri,k);
toc
%Calculate Sound Pressure Levels
SPLc2 = takeSPL(solution2,Pref);

%Match the two SPL's to each other according to the 100th percentile
SPL2 = matchSPL(SPLc2, measurements, 1);


[~, errorTotal2] = errorFunction(SPL2,measurements,Pref,25,err);

display(['error1 = ',num2str(errorTotal1),'  error2 = ', num2str(errorTotal2)])

%Plot the SPL Distrbutions
plotSPL(SPL1,micPositions,'1');
plotSPL(SPL2,micPositions,'2');
pause

for i = 1:100;
    
    i
    
    %set initial guesses for sources
    zpU = rand*8;
    zpC = rand*8;
    sdU = rand*2;
    sdC = rand*2;
    AmaxU = 1;
    AmaxC = rand;
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Unoptimized Result%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %initialize monopole sources
    [sourcesU1,sourcesC1] = initSources(0,2.1,zpU,sdU,AmaxU,zpC,sdC,AmaxC,n,...
        dist,angle,freqs,c);
    
    %simulate measurement
    solution1 = simulation(sourcesU1,sourcesC1,micPositions,k);
    
    %Calculate Sound Pressure Levels
    SPLc = takeSPL(solution1,Pref);
    
    %Match the two SPL's to each other according to the 100th percentile
    SPL = matchSPL(SPLc, measurements, 1);
    
    
    [~, errorTotal1] = errorFunction(SPL,measurements,Pref,25,err);
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%Optimized Result%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %initialize monopole sources
    [sourcesU2,sourcesC2] = initSources_opt(0,2.1,zpU,sdU,AmaxU,zpC,sdC,AmaxC,zMin,zMax,...
        dist,angle,freqs,c);
    
    
    
    %simulate measurement
    solution = simulation_opt(sourcesU2,sourcesC2,Rd,Ri,k);
    
    %Calculate Sound Pressure Levels
    SPLc = takeSPL(solution,Pref);
    
    %Match the two SPL's to each other according to the 100th percentile
    SPL = matchSPL(SPLc, measurements, 1);
    
    
    [~, errorTotal2] = errorFunction(SPL,measurements,Pref,25,err);
    
    display(['error1 = ',num2str(errorTotal1),'  error2 = ', num2str(errorTotal2)])
    errorDiff(i) = errorTotal2 - errorTotal1;
end

'done'
%}
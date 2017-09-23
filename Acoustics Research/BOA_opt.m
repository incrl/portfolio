%The Bayesian Optimization Algorithm
close all
clear all

%Select plane number,engine condition, and octave band
plane = 2;
eng_cond = 4;
f = 1250;

%Load the microphone array
temp = load('F22Holloman2009Geometry7.mat');
micPositions = temp.F22Geometry{1,plane};

%Load the measurements
[measurements,fc] = loadData(eng_cond,plane,f,'Data\');

%Set nozzle position
x = 0;
y = 2.1;

%set reference mics pressure
Pref = 20 * 10^(-6);

%set Speed of Sound in m/s
c = 343;

% define source distances
dist = .02;
zMin = -2;
zMax = 8;

%Caculate distances from sources
[Rd,Ri] = calcDistances(x,y,zMin,zMax,dist,micPositions);

%set the low and high frequency bounds in the third octave band in Hz
flow = fc/(2^(1/6));
fhigh = fc*2^(1/6);
%These values are for a 315 center frequency 

%Set the number of frequencies in the third octave band
nf =10;

%Calculate the third octave band based on a logarithmic spacing.
freqs = logspace(log10(flow), log10(fhigh), nf);

%Ranges
zpUmin = 0;
zpUmax = 8;
zpCmin = 0;
zpCmax = 8;
AmaxMin = 0;
AmaxMax = 1;
sdUmin = .1;
sdUmax = 8;
sdCmin = .1;
sdCmax = 8;
angleMin = 115 * pi/180;
angleMax = 140 * pi/180;

%Put all boundary conditions into one container called boundaries for
%passing into the Simulated Annealing
boundaries = [zpUmin,zpUmax,zpCmin,zpCmax,AmaxMin,AmaxMax,...
                        sdUmin,sdUmax,sdCmin,sdCmax,angleMin,angleMax];
                    
%Put all of the physical description into a container called geometry
geometry = [x,y,c,Pref,dist,zMin,zMax];
tic;
%Grab the starting position for the FGS from the Simulated Annealing
start = simAnnealing_opt(boundaries,geometry,freqs,Rd,Ri,measurements);

%Temporary for testing
%start = [7,2.2,.6,1.7,1.7,.02,.006];

%Grab information for the PPDs from the Fast Gibbs Sampler
values = FGS_opt(boundaries,geometry,start,freqs,Rd,Ri,measurements);
toc

%Generate the SPL map
k = 2 * pi * freqs/c;
[sourcesU,sourcesC] = initSources_opt(x,y,start(1),start(4),1,start(2),start(5),...
    start(3),dist,zMin,zMax,start(6),freqs,c);
solution = simulation(sourcesU,sourcesC,micPositions,k);
SPLc = takeSPL(solution,Pref);
SPL = matchSPL(SPLc, measurements, 1);
%Figure out how much everything was shifted by
shift = SPL(1,1) - SPLc(1,1);

clear geometry Rd Ri boundaries f SPLc solution temp

save(['BOA_Log_plane_',num2str(plane),'_engcond_',num2str(eng_cond),'_freq_',...
    num2str(fc),'_Gaussian.mat'])
                   

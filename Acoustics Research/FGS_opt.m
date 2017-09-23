function values = FGS_opt(boundaries,geometry,start,freqs,Rd,Ri,SPLm)
%simAnnealing The simulated anealing function
%   This function uses the statistics behind annealing metals inorder to
%   determine the optimal solution.

%The number of steps taken during the sampler
numsteps = 10000;
SPL_Range = 25;
%How strict the criteria is
strictness = 500;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Remember to preallocate%%%%%%%%%%%%%%%%%

%Extract boundary values
zpUmin = boundaries(1,1);
zpUmax = boundaries(1,2);
zpCmin = boundaries(1,3);
zpCmax = boundaries(1,4);
AmaxMin = boundaries(1,5);
AmaxMax = boundaries(1,6);
sdUmin = boundaries(1,7);
sdUmax = boundaries(1,8);
sdCmin = boundaries(1,9);
sdCmax = boundaries(1,10);
angleMin = boundaries(1,11);
angleMax = boundaries(1,12);

%Extract geometry values
x = geometry(1,1);
y = geometry(1,2);
c = geometry(1,3);
Pref = geometry(1,4);
dist = geometry(1,5);
zMin = geometry(1,6);
zMax = geometry(1,7);

%calculate wavenumber
k = 2 * pi * freqs/c;

%Extract the starting point
zpU = start(1,1);
zpC = start(1,2);
Amax = start(1,3);
sdU = start(1,4);
sdC = start(1,5);
angle = start(1,6);
errorPrev = start(1,7);

%Analysis and Testing Parameters
accepted_values = zeros(numsteps,7);
low_values = zeros(1000,7);

%select initial lowest error values
zpUlow = zpU;
zpClow = zpC;
AmaxLow = Amax;
sdUlow = sdU;
sdClow = sdC;
angleLow = angle;
errorLow = errorPrev;

%use a random stepsize to select a
%new random point in the variable space
%if the point is out of bounds, go to the boundary

check = 1;
%Each variable is will check to see if the step is in bounds
while(check)
    check = 0;
    step = 2*rand - 1; % Creates a random step between -1 and 1
    zpUnext = step*(zpUmax - zpUmin) + zpU;
    if(zpUnext > zpUmax || zpUnext < zpUmin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = 2*rand - 1; % Creates a random step between -1 and 1
    zpCnext = step*(zpCmax - zpCmin) + zpC;
    if(zpCnext > zpCmax || zpCnext < zpCmin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = 2*rand - 1; % Creates a random step between -1 and 1
    AmaxNext = step*(AmaxMax - AmaxMin) + Amax;
    if(AmaxNext > AmaxMax || AmaxNext < AmaxMin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = 2*rand - 1; % Creates a random step between -1 and 1
    sdUnext = step*(sdUmax - sdUmin) + sdU;
    if(sdUnext > sdUmax || sdUnext < sdUmin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = 2*rand - 1; % Creates a random step between -1 and 1
    sdCnext = step*(sdCmax - sdCmin) + sdC;
    if(sdCnext > sdCmax || sdCnext < sdCmin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = 2*rand - 1; % Creates a random step between -1 and 1
    angleNext = step*(angleMax - angleMin) + angle;
    if(angleNext > angleMax || angleNext < angleMin)
        check = 1;
    end
end

%End Initial Simulation

a = 1;
b = 1;

for count = 1:numsteps
    
    %Display current state
    count
    
    %Begin a simuluation
    [sourcesU,sourcesC] = initSources_opt(x,y,zpUnext,sdUnext,1,zpCnext,sdCnext,AmaxNext,dist,zMin,zMax,angleNext,freqs,c);
    solution = simulation_opt(sourcesU,sourcesC,Rd,Ri,k);
    SPLc = takeSPL(solution,Pref);
    SPLc = matchSPL(SPLc,SPLm,1);
    [~, errorNext] = errorFunction(SPLc,SPLm,Pref,SPL_Range,1);
    
    %Determine if the point is accepeted based on the two cases
    % 1. The change in error is negative
    % 2. A random number is less than the temperature dependant acceptance
    if (errorNext < errorPrev)
        
        %Make it the new point in the next loop
        errorPrev = errorNext;
        zpU = zpUnext;
        zpC = zpCnext;
        Amax = AmaxNext;
        sdU = sdUnext;
        sdC = sdCnext;
        angle = angleNext;
        
        %store values in a log
        accepted_values(a,:) = [zpU,zpC,Amax,sdU,sdC,angle,errorPrev];
        a = a + 1;
        
        %Keep track of the best solution
        if(errorNext < errorLow)
            zpUlow = zpUnext;
            zpClow = zpCnext;
            AmaxLow = AmaxNext;
            sdUlow = sdUnext;
            sdClow = sdCnext;
            angleLow = angleNext;
            errorLow = errorNext;
            %store values in a log
            low_values(b,:) = [zpUlow,zpClow,AmaxLow,sdUlow,sdClow,angleLow,errorLow];
            b = b + 1;
        end
        
    elseif(rand < exp(-strictness*tan(pi/2 *(errorNext - errorPrev))))
        
        %Make it the new point in the next loop
        errorPrev = errorNext;
        zpU = zpUnext;
        zpC = zpCnext;
        Amax = AmaxNext;
        sdU = sdUnext;
        sdC = sdCnext;
        angle = angleNext;
        
        %store values in a log
        accepted_values(a,:) = [zpU,zpC,Amax,sdU,sdC,angle,errorPrev];
        a = a + 1;
        
    end
    
    errorLow
    errorNext
    
    %use a random stepsize to select a
    %new random point in the variable space
    %if the point is out of bounds, go to the boundary
    check = 1;
    %Each variable is will check to see if the step is in bounds
    while(check)
        check = 0;
        step = 2*rand - 1; % Creates a random step between -1 and 1
        zpUnext = step*(zpUmax - zpUmin) + zpU;
        if(zpUnext > zpUmax || zpUnext < zpUmin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = 2*rand - 1; % Creates a random step between -1 and 1
        zpCnext = step*(zpCmax - zpCmin) + zpC;
        if(zpCnext > zpCmax || zpCnext < zpCmin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = 2*rand - 1; % Creates a random step between -1 and 1
        AmaxNext = step*(AmaxMax - AmaxMin) + Amax;
        if(AmaxNext > AmaxMax || AmaxNext < AmaxMin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = 2*rand - 1; % Creates a random step between -1 and 1
        sdUnext = step*(sdUmax - sdUmin) + sdU;
        if(sdUnext > sdUmax || sdUnext < sdUmin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = 2*rand - 1; % Creates a random step between -1 and 1
        sdCnext = step*(sdCmax - sdCmin) + sdC;
        if(sdCnext > sdCmax || sdCnext < sdCmin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = 2*rand - 1; % Creates a random step between -1 and 1
        angleNext = step*(angleMax - angleMin) + angle;
        if(angleNext > angleMax || angleNext < angleMin)
            check = 1;
        end
    end
    
end

%Truncate the accepted_values so that zeros don't sit at the end
values = accepted_values(1:a-1,:);

save('FGS_Log.mat');

end


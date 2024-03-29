function results = simAnnealing(boundaries,geometry,...
                                         freqs, micPositions, SPLm)
%simAnnealing The simulated anealing function
%   This function uses the statistics behind annealing metals inorder to
%   determine the optimal solution.

%initizalize simulated annealing parameters
T = 1;
Tfinal = .001;
rate = .75;
num_steps = 100;
SPL_Range = 25;

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
distMin = boundaries(1,11);
distMax = boundaries(1,12);

%Extract geometry values
x = geometry(1,1);
y = geometry(1,2);
angle = geometry(1,3);
c = geometry(1,4);
Pref = geometry(1,5);
n = geometry(1,6);

%calculate wavenumber
k = 2 * pi * freqs/c;

%Analysis and Testing Parameters
accepted_values = zeros(10000,8);
low_values = zeros(1000,8);

%Simulate once so that there is a reference error for the while loop

%select a random point in the variable space
zpU = rand*(zpUmax - zpUmin) + zpUmin;
zpC = rand*(zpCmax - zpCmin) + zpCmin;
Amax = rand*(AmaxMax - AmaxMin) + AmaxMin;
sdU = rand*(sdUmax - sdUmin) + sdUmin;
sdC = rand*(sdCmax - sdCmin) + sdCmin;
dist = rand*(distMax-distMin) + distMin;

[sourcesU,sourcesC] = initSources(x,y,zpU,sdU,1,zpC,sdC,Amax,n,dist,angle,freqs,c);

solution = simulation(sourcesU,sourcesC,micPositions,k);

SPLc = takeSPL(solution,Pref);

SPLc = matchSPL(SPLc,SPLm,1);

[~, errorPrev] = errorFunction(SPLc,SPLm,Pref,SPL_Range,1);

%select initial lowest error values
zpUlow = zpU;
zpClow = zpC;
AmaxLow = Amax;
sdUlow = sdU;
sdClow = sdC;
distLow = dist;
errorLow = errorPrev;

%use a random stepsize to select a
%new random point in the variable space
%if the point is out of bounds, go to the boundary

check = 1;
%Each variable is will check to see if the step is in bounds
while(check)
    check = 0;
    step = normrnd(0,.33); % Creates a random step between -1 and 1
    zpUnext = step*(zpUmax - zpUmin) + zpU;
    if(zpUnext > zpUmax || zpUnext < zpUmin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = normrnd(0,.33); % Creates a random step between -1 and 1
    zpCnext = step*(zpCmax - zpCmin) + zpC;
    if(zpCnext > zpCmax || zpCnext < zpCmin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = normrnd(0,.33); % Creates a random step between -1 and 1
    AmaxNext = step*(AmaxMax - AmaxMin) + Amax;
    if(AmaxNext > AmaxMax || AmaxNext < AmaxMin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = normrnd(0,.33); % Creates a random step between -1 and 1
    sdUnext = step*(sdUmax - sdUmin) + sdU;
    if(sdUnext > sdUmax || sdUnext < sdUmin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = normrnd(0,.33); % Creates a random step between -1 and 1
    sdCnext = step*(sdCmax - sdCmin) + sdC;
    if(sdCnext > sdCmax || sdCnext < sdCmin)
        check = 1;
    end
end

check = 1;
while(check)
    check = 0;
    step = normrnd(0,.33); % Creates a random step between -1 and 1
    distNext = step*(distMax - distMin) + dist;
    if(distNext > distMax || distNext < distMin)
        check = 1;
    end
end

%End Initial Simulation

count = 1;
a = 1;
b = 1;

while T > Tfinal
    
    %Display current state
    T
    count
    
    %Begin a simuluation
    [sourcesU,sourcesC] = initSources(x,y,zpUnext,sdUnext,1,zpCnext,sdCnext,AmaxNext,n,distNext,angle,freqs,c);
    solution = simulation(sourcesU,sourcesC,micPositions,k);
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
        dist = distNext;
        
        %store values in a log
        accepted_values(a,:) = [zpU,zpC,Amax,sdU,sdC...
            ,dist,errorPrev,T];
        a = a + 1;
        
        %Keep track of the best solution
        if(errorNext < errorLow)
            zpUlow = zpUnext;
            zpClow = zpCnext;
            AmaxLow = AmaxNext;
            sdUlow = sdUnext;
            sdClow = sdCnext;
            distLow = distNext;
            errorLow = errorNext;
            %store values in a log
            low_values(b,:) = [zpUlow,zpClow,AmaxLow,sdUlow,sdClow...
                ,distLow,errorLow,T];
            b = b + 1;
        end
        
    elseif(rand < exp(-100*tan(pi/2 *(errorNext - errorPrev))/T))
        
        %Make it the new point in the next loop
        errorPrev = errorNext;
        zpU = zpUnext;
        zpC = zpCnext;
        Amax = AmaxNext;
        sdU = sdUnext;
        sdC = sdCnext;
        dist = distNext;
        
        %store values in a log
        accepted_values(a,:) = [zpU,zpC,Amax,sdU,sdC...
            ,dist,errorPrev,T];
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
        step = normrnd(0,.33); % Creates a random step between -1 and 1
        zpUnext = step*(zpUmax - zpUmin) + zpU;
        if(zpUnext > zpUmax || zpUnext < zpUmin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = normrnd(0,.33); % Creates a random step between -1 and 1
        zpCnext = step*(zpCmax - zpCmin) + zpC;
        if(zpCnext > zpCmax || zpCnext < zpCmin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = normrnd(0,.33); % Creates a random step between -1 and 1
        AmaxNext = step*(AmaxMax - AmaxMin) + Amax;
        if(AmaxNext > AmaxMax || AmaxNext < AmaxMin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = normrnd(0,.33); % Creates a random step between -1 and 1
        sdUnext = step*(sdUmax - sdUmin) + sdU;
        if(sdUnext > sdUmax || sdUnext < sdUmin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = normrnd(0,.33); % Creates a random step between -1 and 1
        sdCnext = step*(sdCmax - sdCmin) + sdC;
        if(sdCnext > sdCmax || sdCnext < sdCmin)
            check = 1;
        end
    end
    
    check = 1;
    while(check)
        check = 0;
        step = normrnd(0,.33); % Creates a random step between -1 and 1
        distNext = step*(distMax - distMin) + dist;
        if(distNext > distMax || distNext < distMin)
            check = 1;
        end
    end
    
    count = count + 1;
    
    if count > num_steps
        %Lower the temperature
        T = rate*T;
        count = 1;
    end
end

%Return the best solution
zpU = zpUlow;
zpC = zpClow;
Amax = AmaxLow;
sdU = sdUlow;
sdC = sdClow;
dist = distLow;
error = errorLow;

save('Simulated_Anealling_Log.mat');

results = [zpU,zpC,Amax,sdU,sdC,dist,error];

end


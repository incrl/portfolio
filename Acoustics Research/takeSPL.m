function [ SPL ] = takeSPL( sqpressure, Pref )
%takeSPL Finds the sound pressure level from a squared pressure

SPL = 10*(log10(sqpressure/(Pref^2)));

end


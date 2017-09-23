function [ SPL, fc] = loadData( eng_cond, plane, f, pathname )
%LOADDATA Loads the measurement data
%   This function loads the pressure squared data for
%   the plane number 'plane' and for the octave band number 'fnum'
%   and the engine condition 'eng_cond'. It returns the SPL map,
%   the center frequency, and the angle of projection. It looks
%   for the data in the given pathname.

Pref = 20*10^(-6);

% If type is not provided, assume it is log error function
if nargin < 4
    pathname = '';
end

condition = '';

if eng_cond == 1
    condition = 'Idle';
end
if eng_cond == 2
    condition = 'Interm';
end
if eng_cond == 3
    condition = 'Mil';
end
if eng_cond == 4
    condition = 'AB';
end



%Load the data
data = load(strcat(pathname,'OneThird_Maps_',condition,'_plane',num2str(plane),'.mat'));

%Find the center frequency number
ind = data.spec3_data.oct_c >= f;
fnum = find(ind,1);

%Load the SPL map
psquared = data.spec3_data.spec3;
SPL = takeSPL(squeeze(psquared(fnum,:,:)),Pref);

%Load the center frequency
fc = data.spec3_data.oct_c(fnum);

end


% FUNCTION [resolution,legendfontsize,small_marker,large_marker,...
%     minor_line,green] = ...
%     FigureDefaults_20110623(scaling,fig_width,fig_height,...
%     cust_fig_height)
%
% Description:
%
%  This function sets the defaults
%  for plotting figures that will go 
%  into my dissertation.
%
% Inputs:
%
%   scaling         :   For fitting figure to screen size.  Has no effect on
%                       saved figure.
%   fig_width       :   Width of the figure may be:
%                           'full'      (6.5 in.)
%                           'wide'      (5.5 in.)
%                           'medium'    (4 in.)
%                           'narrow'    (2.5 in.)
%   fig_height      :   Height of the figure may be:
%                           'full'      (6.5 in.)
%                           'tall'      (5.5 in.)
%                           'medium'    (4 in.)
%                           'short'     (2.5 in.)
%                           'custom'    (see 'cust_fig_height')
%   cust_fig_height :   Custom height of figure in inches.
%
% Outputs:
%
%   

%
% Author: Alan Wall (alantwall@gmail.com)
%
% Date: 06/23/2011
%

function [resolution,small_marker,large_marker,...
    minor_line,darkgreen,minor_fontsize,major_line,colors,...
    lines,markers,phot] = ...
    FigureDefaults_20110623(scaling,fig_width,fig_height,...
    cust_fig_height)

addpath('\\KIRCHHOFF\Acoustics\Students\Alan Wall\HollomanF22_2009\CoreFiles')
phot = p_hot_generator4;
resolution = round(1000/scaling);   %dpi

fig_width_names = {'full','wide','medium','JASA','narrow'};
fig_width_values = [6.5, 5.5, 4, 3.375 2.5];
fig_height_names = {'full','tall','medium','JASA','short','custom'};
fig_height_values = fig_width_values;

width = fig_width_values(strcmp(fig_width,fig_width_names));

if strcmp(fig_height,'custom')
    height = cust_fig_height;
else
    height = fig_height_values(strcmp(fig_height,fig_height_names));
end

%INITIALIZE PLOT DEFAULTS
set(0,'DefaultAxesFontName','Times New Roman');
set(0,'DefaultTextFontName','Times New Roman');
set(0,'DefaultAxesFontSize',10*scaling);
set(0,'DefaultTextFontSize',10*scaling);
set(0,'DefaultAxesFontWeight','demi');
set(0,'DefaultTextFontWeight','demi');
set(0,'DefaultAxesLineWidth',1*scaling);
set(0,'DefaultLineLineWidth',1*scaling);
set(0,'DefaultLineMarkersize',4*scaling);
set(0,'DefaultFigureUnits','inches');
set(0,'DefaultAxesUnits','inches');
set(0,'DefaultFigurePosition',[1 1 width*scaling height*scaling]);
small_marker = 7*scaling;
large_marker = 4*scaling;
minor_line = .6*scaling;

minor_fontsize = 8*scaling;
major_line = get(0,'DefaultAxesLineWidth');
lines = {'-','--','-.',':'};
markers = {'o','^','+','s','v','p','d','>','x','h','<'};

pink = [255	192	203]/255; 
darkviolet = [148 0 211]/255;
slategray = [112 128 144]/255;
dodgerblue = [30 144 255]/255;
turquoise = [0 245 255]/255;
darkgreen = [0 100 0]/255;
chartreuse3 = [102	205	0]/255;
gold2 = [238 201 0]/255;
orange = [255 128 0]/255;
chocolate = [139 69 19]/255;
colors = {'k','r','b',gold2,darkgreen,orange,darkviolet,dodgerblue,pink,...
    chartreuse3,slategray,chocolate,turquoise};

colvect = [0,0,0; 1,0,0; 0,0,1; gold2; darkgreen; orange; darkviolet; ...
    dodgerblue; pink; chartreuse3; slategray; chocolate; turquoise];

set(0, 'DefaultAxesColorOrder', colvect);






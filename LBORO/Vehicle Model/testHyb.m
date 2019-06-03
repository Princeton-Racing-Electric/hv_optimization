clf; clc; clear all; close all;

%driveCycle = readmatrix('DriveCycles/nedc2_kph.tsv','FileType','text');
driveCycle = readmatrix('DriveCycles/nedc2_short_kph.tsv','FileType','text');
%driveCycle = readmatrix('DriveCycles/step_quick_kph.tsv','FileType','text');

pascalOrd = 5;
nSeries   = 3;
ptr       = 1;

iDivisor  = 50.0;
tDivisor  = 0.1;
tStep     = 10.0;

vStart    = 8.0;
farads    = 2.0;
bCapacity = 0.5; % Ah
bSoc      = 90; % pc 8.2v

current   = @(ampsIn)  -ampsIn ./ iDivisor;
time      = @(t)       t      ./ tDivisor;

for i=1:length(driveCycle)
    driveCycle(i, 1) = time(driveCycle(i, 1));
    driveCycle(i, 2) = current(driveCycle(i, 2));
end

%tStep     = (driveCycle(2, 1) - driveCycle(1, 1)) ./ tStep;

mySc      = Sc(pascalOrd, nSeries, vStart, farads, tStep);
mySc      = mySc.setupBattery(bCapacity, bSoc);

%% Drive
mySc = mySc.runCycle( driveCycle(:, 1), driveCycle(:, 2), tStep );
%[sim_time, amps_in, distribution_in, capacitance,...
%                            bCapacity, bSoc, resolution, tStep, v_init]...
%                                                = mySc.fakeRun( 10, 0.1 );

%% Save
save('model_out.mat', 'mySc');

%% Plot surface
mySc.plotSoc(1);
mySc.plotSoc(2);
mySc.plotSoc(3);
%mySc.plotSurface(2);
%mySc.plotSurface(3);

%% Plot movie
%mySc.plotMovie('pretty_vid', 100);

%% End
load('handel.mat');
player = audioplayer(y, Fs);
play(player);
disp('Finished!');
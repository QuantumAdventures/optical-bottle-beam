% Here we will calculate the forces acting on the particle trapped inside the OBB
% Forces are saved in a txt file for a variety of NA 
% We also calculate the dynamics of the trapped particle and save it in a txt file for a variety of NA 

% Add the toolbox to the path (assuming we are in ott/examples)
addpath('../');

% Close open figures
close all;


kb = 1.38e-23; % Boltzmann cte. in J / K
T = 293.0; % temperature in Kelvin
t_max = 1; % [s] max simulation time
dt = 1e-5; %1e-6; % time interval for the simulation [s]
dt_s = 1; %4e-5; %sampling dt [s] - it simulates the sampling of an osciloscope
radius = 1.150e-6/2; % Radius of particle [m]
%viscosity = 0.0008538; % water [N/m^2] https://www.omnicalculator.com/physics/water-viscosity
viscosity = 6.6e-3;   %viscosity of clove oil (https://www.ijset.net/journal/208.pdf)
%viscosity = 1.6e-5; %air
gamma =  6*pi*viscosity*radius; % # damping coef. [N.s/m]
n_medium = 1.53; % Medium refractive index (1.53 para óleo cravo)
n_particle = 1.46; % Particle refractive index
wavelength0 = 780e-9; % Wavelength of light in vacuum [m]
c = 299792458; %Speed of light [m/s]

transmission_rate = 0.85; %transmission rate of the clove oil
P_trapping= 106e-3; %Laser power of the trapping [W]
P_probe=10e-3; %Laser power of the probe beam [W]
F_trapping= transmission_rate* P_trapping*n_medium/c; % force factor [N] 
F_probe=transmission_rate* P_probe*n_medium/c;%e-3; % force factor [N]
%P = 100e-3; %Laser power [W]
%P = (P_trapping + P_probe)*1e-3; %Laser power [W]
trials = 1; %Number of traces

kbT = kb*T;
wavelength_medium = wavelength0/n_medium;


list_of_NA= (28 : 60 )/100;
for j = 1:length(list_of_NA)
    NA=list_of_NA(j);
    % Create a T-matrix for a sphere
    T_matrix = ott.Tmatrix.simple('sphere', radius, 'wavelength0', wavelength0, ...
        'index_medium', n_medium, 'index_particle', n_particle);


    %%%%% Create the OBB %%%%%%%%%%%%%%%%%%%%
    % Create a simple Gaussian beam with linear polarisation
    beam1 = ott.BscPmGauss('NA', NA, 'polarisation', [ 1 0 ], ...
        'index_medium', n_medium, 'wavelength0', wavelength0);

    % Create a simple LG10 beam with linear polarisation
    beam2 = ott.BscPmGauss('lg', [ 1 0 ], ...
            'index_medium', n_medium, 'wavelength0',  wavelength0, ...
            'NA', NA, 'polarisation', [ 1 0 ]);

    % Join the beams to create our beam (adding a phase shift to the 2nd beam)
    %beam = beam1 - 2.27*beam2 * exp(0 * pi * 1i * 1/2);    
    beam = beam1 - 1.81*beam2 * exp(0 * pi * 1i * 1/2); 


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %force_factor = n_medium*P/(c);

    timestamps = linspace(0,t_max,t_max/dt);
    N = size(timestamps,2);
    simulationPositions_x = {}; %where the simulated traces are going to be stored
    simulatedSignal_x = {}; %where the simulated oscilloscope signals are going to be stores
    simulationPositions_z = {}; %where the simulated traces are going to be stored
    simulatedSignal_z = {}; %where the simulated oscilloscope signals are going to be stores
    simulationPositions_y = {}; %where the simulated traces are going to be stored
    simulatedSignal_y = {}; %where the simulated oscilloscope signals are going to be stores


    %Creating the OBB with the probe beam as a pertubation 
    ratio = 0.9; %This ratio demonstrates how much one of the beams are greater than the other.  
    % Create a simple Gaussian beam with linear polarisation
    probe_beam = ott.BscPmGauss('NA', NA, 'polarisation', [ 0 1 ], ...
        'index_medium', n_medium, 'wavelength0', wavelength0);
    z = [0;0;1]*linspace(-10,10,500)*wavelength_medium;
    fz = (F_trapping * ott.forcetorque(beam, T_matrix, 'position', z)) +  (F_probe* ott.forcetorque(probe_beam, T_matrix, 'position', z)) ;

    % Find the equilibrium along the z axis
    zeq = ott.find_equilibrium(z(3, :), fz(3, :));
    if isempty(zeq)
      warning('No axial equilibrium in range!')
      zeq=0;
    end

    r = [1;1;0]*linspace(-10,10,500)*wavelength_medium + [0;0;zeq];
    fr =(F_trapping * ott.forcetorque(beam, T_matrix, 'position', r)) + (F_probe* ott.forcetorque(probe_beam, T_matrix, 'position', r)); 

    xeq = ott.find_equilibrium(r(1, :), fr(1, :));
    if isempty(xeq)
      warning('No equilibrium in x-direction')
      xeq=0;
    end
    
    x = r(1,:);
    y = r(2,:);
    z = z(3,:);
    fx = fr(1,:);
    fy = fr(2,:);
    fz = fz(3,:);

    %% Fit: 'force_x and force_y'.
    [xData, yData] = prepareCurveData( x, fx );
    [xData_y, yData_y] = prepareCurveData( y, fy );

    % Set up fittype and options.
    ft = fittype( 'smoothingspline' );

    % Fit model to data.
    [fit_fx, gof] = fit( xData, yData, ft );
    [fit_fy, gof_y] = fit( xData_y, yData_y, ft );

    %% Fit: 'force_z'.
    [xData_z, yData_z] = prepareCurveData( z, fz );

    % Set up fittype and options.
    ft = fittype( 'smoothingspline' );

    % Fit model to data.
    [fit_fz, gof] = fit( xData_z, yData_z, ft );


    %wb = waitbar(0, 'Starting');


    positions = zeros([1,N]);
    positions_y=zeros([1,N]);

    positions_z = zeros([1,N]);
    positions_z(1,1) = zeq;



    for experiment = 1:5
        positions = zeros([1,N]);
        positions_y=zeros([1,N]);
        positions_z = zeros([1,N]);
        positions_z(1,1) = zeq;

        wb = waitbar(0, 'Starting');
        for M = 1:trials

            positions = zeros([1,N]);
            positions_y=zeros([1,N]);

            positions_z = zeros([1,N]);
            positions_z(1,1) = zeq;


            for i = 2:N

                f = fit_fx(positions(1,i-1));%*force_factor;
                W = sqrt(2.0 * kbT * dt / gamma) * normrnd(0,1,[1,1]);
                positions(1,i) = positions(1,i-1) +f*dt/gamma + W;

                f = fit_fy(positions_y(1,i-1));%*force_factor;
                W = sqrt(2.0 * kbT * dt / gamma) * normrnd(0,1,[1,1]);
                positions_y(1,i) = positions_y(1,i-1) +f*dt/gamma + W;


                f = fit_fz(positions_z(1,i-1));%*force_factor;
                W = sqrt(2.0 * kbT * dt / gamma) * normrnd(0,1,[1,1]);
                positions_z(1,i) = positions_z(1,i-1) +f*dt/gamma + W;


            end


         %simulationPositions_x{end+1} = positions;
         %simulatedSignal_x{end+1} = positions(1:dt_s/dt:end);


         %simulationPositions_z{end+1} = positions_z;
         %simulatedSignal_z{end+1} = positions_z(1:dt_s/dt:end);

         %simulationPositions_y{end+1} = positions_y;
         %simulatedSignal_y{end+1} = positions_y(1:dt_s/dt:end);
         waitbar(M/trials, wb, sprintf('Progress: %d %%', floor(M/trials*100)));

         f_storage=[fx,fy,fz];
         positions_storage=[positions; positions_y; positions_z];%[simulationPositions_x{end+1},simulationPositions_y{end+1},simulationPositions_z{end+1}];

         filename_positions = sprintf('OBB_positions_NA_%d_exp_%d.txt',int16(NA*100), experiment);
         filename_forces = sprintf('OBB_forces_NA_%d_exp_%d.txt',int16(NA*100), experiment);

         writematrix(f_storage, filename_forces);
         writematrix(positions_storage, filename_positions);

         sprintf('Experimento %d com NA %d  salvo!', experiment, int16(NA*100))

         waitbar(M/trials, wb, sprintf('Progress: %d %%', floor(M/trials*100)));
         close(wb) %testing it

        end
        %close(wb)

    end
    
    %Use essas linhas 4 linhas a seguir para salvar o experimento
    %f_storage=[fx;fy;fz];
    %filename_forces = sprintf('OBB_forces_NA_%d.txt',int16(NA*100));
    %writematrix(f_storage, filename_forces); 
    %sprintf(' Simulação  NA %d  concluido!', int16(NA*100))
end


beep
